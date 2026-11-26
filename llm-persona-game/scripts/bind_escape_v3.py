"""Bind whole v3 episodes to a frozen local plan. Single-writer prototype.

No external model adapter is supplied. A pending run without a saved result
requires manual reconciliation; it is never automatically called again.
Use --check for synthetic interruption checks.
"""

import hashlib
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from copy import deepcopy

from reconcile_escape_v3 import reconcile
from run_escape_v3 import run_episode
from replay_escape_v3 import VERSION, audit


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def create(path, value):
    with Path(path).open("xb") as f:
        f.write(canonical(value))
        f.flush()
        os.fsync(f.fileno())


def freeze(root, plan):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    reconcile(plan, [])
    envelope = {"plan_sha256": digest(plan), "plan": deepcopy(plan)}
    path = root / "plan.json"
    if path.exists():
        if read(path) != envelope:
            raise ValueError("Frozen plan differs; use a new execution directory")
    else:
        create(path, envelope)
    return envelope["plan_sha256"]


def execute(root, plan, run_id, provider, *, fault=None):
    root = Path(root)
    frozen = read(root / "plan.json")
    if frozen != {"plan_sha256": digest(plan), "plan": plan}:
        raise ValueError("Plan content or digest changed")
    reconcile(plan, [])
    rows = [r for r in plan["runs"] if r["run_id"] == run_id]
    if len(rows) != 1:
        raise ValueError("Unknown planned run")
    row = rows[0]
    prefix = hashlib.sha256(run_id.encode("utf-8")).hexdigest()
    pending, result = root / (prefix + ".pending.json"), root / (prefix + ".result.json")
    identity = {"plan_sha256": frozen["plan_sha256"], "run_id": run_id,
                "max_attempts": row["max_attempts"]}
    if pending.exists() and read(pending) != identity:
        raise ValueError("Pending identity differs")
    if result.exists():
        saved = read(result)
        if {k: saved.get(k) for k in identity} != identity:
            raise ValueError("Saved episode identity differs")
        if saved["episode"]["run_id"] != run_id:
            raise ValueError("Saved run differs")
        reconcile(plan, [saved["episode"]])
        if pending.exists():
            pending.unlink()
        return saved
    if pending.exists():
        raise RuntimeError("Unresolved execution; reconcile provider records before retry")
    create(pending, identity)
    if fault == "before_call":
        raise RuntimeError("Synthetic interruption before provider")
    episode = run_episode(run_id, row["powered"], row["profiles"], provider,
                          evidence=plan["evidence"], max_attempts=row["max_attempts"])
    reconcile(plan, [episode])
    if fault == "before_save":
        raise RuntimeError("Synthetic interruption after provider, before result save")
    saved = {**identity, "episode": episode}
    temporary = root / (prefix + ".result.tmp")
    create(temporary, saved)
    os.replace(temporary, result)
    if fault == "after_save":
        raise RuntimeError("Synthetic interruption after result save")
    pending.unlink()
    return saved


def check():
    plan = {"version": VERSION, "evidence": "synthetic", "runs": [{
        "run_id": "unicode/attempt-1", "condition": "free-text-fixture", "powered": True,
        "max_attempts": 11,
        "profiles": {"holder": "舞台技師。\n説明する。  ", "partner": "학생. 동료에게 질문한다."},
    }]}
    checks = []
    with TemporaryDirectory() as directory:
        root = Path(directory)
        calls = []
        def provider(_):
            calls.append(1)
            return json.dumps({"speech": "", "action": next(events)["action"]})

        normal = root / "normal"
        sha = freeze(normal, plan)
        assert freeze(normal, plan) == sha
        reordered = {k: plan[k] for k in reversed(plan)}
        assert digest(reordered) == sha
        events = iter(audit(True)["paths"][0]["events"])
        saved = execute(normal, plan, plan["runs"][0]["run_id"], provider)
        count = len(calls)
        assert execute(normal, plan, plan["runs"][0]["run_id"], provider) == saved
        assert len(calls) == count == 7
        assert saved["max_attempts"] == 11 and saved["episode"]["profiles"] == plan["runs"][0]["profiles"]
        checks.append("completed replay adds zero provider calls")

        for field in ("profiles", "max_attempts", "version", "powered"):
            changed = deepcopy(plan)
            if field == "profiles":
                changed["runs"][0][field]["holder"] += "変更"
            elif field == "max_attempts":
                changed["runs"][0][field] = 12
            elif field == "powered":
                changed["runs"][0][field] = False
            else:
                changed[field] = "other-version"
            for operation in (lambda: freeze(normal, changed),
                              lambda: execute(normal, changed, plan["runs"][0]["run_id"], provider)):
                try:
                    operation()
                except ValueError:
                    pass
                else:
                    raise AssertionError(field)
            assert len(calls) == count
            checks.append(field + " change rejected before provider")

        for fault in ("before_call", "before_save", "after_save"):
            target = root / fault
            freeze(target, plan)
            events = iter(audit(True)["paths"][0]["events"])
            before = len(calls)
            try:
                execute(target, plan, plan["runs"][0]["run_id"], provider, fault=fault)
            except RuntimeError:
                pass
            else:
                raise AssertionError(fault)
            after = len(calls)
            assert after - before == (0 if fault == "before_call" else 7)
            if fault == "after_save":
                assert execute(target, plan, plan["runs"][0]["run_id"], provider) == saved
            else:
                try:
                    execute(target, plan, plan["runs"][0]["run_id"], provider)
                except RuntimeError:
                    pass
                else:
                    raise AssertionError("Ambiguous execution retried")
            assert len(calls) == after
            checks.append(fault + " recovery adds zero provider calls")
        result_path = next(normal.glob("*.result.json"))
        corrupt = deepcopy(saved)
        corrupt["max_attempts"] = 99
        result_path.write_bytes(canonical(corrupt))
        try:
            execute(normal, plan, plan["runs"][0]["run_id"], provider)
        except ValueError:
            pass
        else:
            raise AssertionError("Changed saved budget accepted")
        checks.append("saved budget mismatch rejected")
        frozen_path = normal / "plan.json"
        frozen = read(frozen_path)
        frozen["plan_sha256"] = "corrupted"
        frozen_path.write_bytes(canonical(frozen))
        try:
            execute(normal, plan, plan["runs"][0]["run_id"], provider)
        except ValueError:
            pass
        else:
            raise AssertionError("Changed digest accepted")
        checks.append("frozen digest mismatch rejected")
        assert len(calls) == 21
    return {"evidence": "synthetic", "checks": checks, "provider_response_calls": len(calls),
            "actual_model_calls": 0, "participants": 0}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    print(json.dumps(check(), ensure_ascii=False, indent=2))
