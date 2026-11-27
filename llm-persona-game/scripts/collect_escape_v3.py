"""Read-only inventory of one frozen v3 execution directory.

Usage: python3 scripts/collect_escape_v3.py ROOT
Use --check for synthetic checks. Run only when the single writer is stopped.
No provider is called and no pending file is removed by collection.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory

from bind_escape_v3 import canonical, digest, execute, freeze, read
from reconcile_escape_v3 import reconcile
from replay_escape_v3 import VERSION, audit


def collect(root):
    root = Path(root)
    frozen = read(root / "plan.json")
    plan = frozen["plan"]
    if frozen["plan_sha256"] != digest(plan):
        raise ValueError("Frozen plan digest mismatch")
    reconcile(plan, [])
    expected, episodes, storage = {"plan.json"}, [], []
    for row in plan["runs"]:
        run_id = row["run_id"]
        stem = hashlib.sha256(run_id.encode("utf-8")).hexdigest()
        pending = root / (stem + ".pending.json")
        result = root / (stem + ".result.json")
        temporary = root / (stem + ".result.tmp")
        expected.update(p.name for p in (pending, result, temporary))
        identity = {"plan_sha256": frozen["plan_sha256"], "run_id": run_id,
                    "max_attempts": row["max_attempts"]}
        if pending.exists() and read(pending) != identity:
            raise ValueError("Pending identity differs")
        if temporary.exists() and (not pending.exists() or result.exists()):
            raise ValueError("Unexpected temporary/result combination")
        if result.exists():
            saved = read(result)
            if {k: saved.get(k) for k in identity} != identity:
                raise ValueError("Saved identity differs")
            if saved["episode"]["run_id"] != run_id:
                raise ValueError("Saved episode ID differs")
            episodes.append(saved["episode"])
            phase = "saved_pending_cleanup" if pending.exists() else "saved"
        elif pending.exists():
            phase = "unresolved"
        else:
            phase = "no_artifact"
        storage.append({"run_id": run_id, "condition": row["condition"],
                        "powered": row["powered"], "storage_phase": phase,
                        "temporary_present": temporary.exists()})
    unexpected = sorted(p.name for p in root.iterdir() if p.name not in expected)
    if unexpected:
        raise ValueError("Unexpected execution artifacts: " + ", ".join(unexpected))
    report = reconcile(plan, episodes)
    for group in report["groups"]:
        rows = [r for r in storage if (r["condition"], r["powered"]) ==
                (group["condition"], group["powered"])]
        group["storage_phase_counts"] = dict(Counter(r["storage_phase"] for r in rows))
    return {"plan_sha256": frozen["plan_sha256"], "storage": storage, "report": report}


def check():
    plan = {"version": VERSION, "evidence": "synthetic", "runs": [{
        "run_id": f"run/{i}", "condition": "fixture", "powered": True,
        "max_attempts": 11,
        "profiles": {"holder": "舞台技師。\n説明する。  ", "partner": "학생. 모르면 질문한다."},
    } for i in range(5)]}
    rejected = []
    with TemporaryDirectory() as directory:
        root = Path(directory)
        freeze(root, plan)
        calls = []
        for i, row in enumerate(plan["runs"][:4]):
            events = iter(audit(True)["paths"][0]["events"])
            def provider(_):
                calls.append(1)
                return "malformed" if i == 1 else json.dumps(
                    {"speech": "", "action": next(events)["action"]})
            try:
                execute(root, plan, row["run_id"], provider,
                        fault={2: "after_save", 3: "before_call"}.get(i))
            except RuntimeError:
                assert i in (2, 3)
        def snapshot():
            return {p.name: p.read_bytes() for p in root.iterdir()}
        before = snapshot()
        result = collect(root)
        assert collect(root) == result and snapshot() == before and len(calls) == 15
        assert [r["storage_phase"] for r in result["storage"]] == [
            "saved", "saved", "saved_pending_cleanup", "unresolved", "no_artifact"]
        group = result["report"]["groups"][0]
        assert group["planned_runs"] == 5 and group["recorded_runs"] == 3
        assert group["escaped_runs"] == 2 and group["choice_observed_runs"] == 2
        assert group["missing_ids"] == ["run/3", "run/4"]
        assert group["status_counts"] == {"escaped": 2, "malformed_response": 1}
        assert group["completed_team_actions"] == [7, 7]
        pending_path = next(p for p in root.glob("*.pending.json") if read(p)["run_id"] == "run/3")
        temp_path = root / pending_path.name.replace(".pending.json", ".result.tmp")
        temp_path.write_bytes(b"partial JSON")
        assert collect(root)["storage"][3]["temporary_present"]
        assert collect(root)["report"] == result["report"]
        temp_path.unlink()
        for case in ("unknown_file", "duplicate_result", "pending_mismatch", "budget_mismatch",
                     "hash_mismatch", "episode_mismatch", "truncated_result", "orphan_temp"):
            result_path = next(root.glob("*.result.json"))
            if case == "unknown_file":
                (root / "unplanned.pending.json").write_bytes(b"{}")
            elif case == "duplicate_result":
                (root / "copy.result.json").write_bytes(result_path.read_bytes())
            elif case == "pending_mismatch":
                value = read(pending_path)
                value["run_id"] = "other"
                pending_path.write_bytes(canonical(value))
            elif case == "budget_mismatch":
                value = read(result_path)
                value["max_attempts"] = 12
                result_path.write_bytes(canonical(value))
            elif case == "hash_mismatch":
                value = read(root / "plan.json")
                value["plan_sha256"] = "corrupt"
                (root / "plan.json").write_bytes(canonical(value))
            elif case == "episode_mismatch":
                value = read(result_path)
                value["episode"]["final"]["escape"]["battery"] = "invented"
                result_path.write_bytes(canonical(value))
            elif case == "truncated_result":
                result_path.write_bytes(b"{")
            else:
                stem = hashlib.sha256(b"run/4").hexdigest()
                (root / (stem + ".result.tmp")).write_bytes(b"partial")
            try:
                collect(root)
            except (ValueError, KeyError):
                rejected.append(case)
            else:
                raise AssertionError(case)
            for p in root.iterdir():
                p.unlink()
            for name, data in before.items():
                (root / name).write_bytes(data)
        assert snapshot() == before and collect(root) == result and len(calls) == 15
    return {"evidence": "synthetic", "planned": 5, "saved": 3, "missing": 2,
            "storage_phases": [r["storage_phase"] for r in result["storage"]],
            "fixture_response_calls": 15, "collection_provider_calls": 0,
            "rejected_checks": rejected, "actual_model_calls": 0, "participants": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("root", nargs="?")
    args = parser.parse_args()
    if not args.check and not args.root:
        parser.error("Provide an execution directory")
    print(json.dumps(check() if args.check else collect(args.root), ensure_ascii=False, indent=2))
