"""Reconcile an explicit v3 plan with recorded episodes.

Usage: python3 scripts/reconcile_escape_v3.py plan.json episodes.jsonl
Use --check for synthetic checks. This does not execute a model or certify
provider provenance. Plans must be retained before execution by the caller.
"""

import argparse
import json
from collections import Counter
from copy import deepcopy

from report_escape_v3 import summarize
from run_escape_v3 import run_episode
from replay_escape_v3 import VERSION, audit


def reconcile(plan, episodes):
    if plan.get("version") != VERSION or plan.get("evidence") not in ("synthetic", "model"):
        raise ValueError("Declare v3 version and evidence")
    planned = {}
    for row in plan["runs"]:
        if not isinstance(row.get("run_id"), str) or not row["run_id"].strip():
            raise ValueError("Nonempty run ID required")
        if row["run_id"] in planned:
            raise ValueError("Duplicate planned ID")
        if not isinstance(row.get("condition"), str) or not row["condition"].strip():
            raise ValueError("Condition label required")
        if type(row.get("powered")) is not bool:
            raise ValueError("Boolean power required")
        if type(row.get("max_attempts")) is not int or row["max_attempts"] <= 0:
            raise ValueError("Positive attempt budget required")
        profiles = row.get("profiles", {})
        if set(profiles) != {"holder", "partner"} or any(
            not isinstance(t, str) or not t.strip() for t in profiles.values()
        ):
            raise ValueError("Two verbatim free-text profiles required by this fixture")
        planned[row["run_id"]] = row
    records = {}
    for episode in episodes:
        run_id = episode["run_id"]
        if run_id not in planned or run_id in records:
            raise ValueError("Unplanned or duplicate recorded ID")
        row = planned[run_id]
        if any(episode.get(k) != row[k] for k in ("profiles", "powered")) or any(
            episode.get(k) != plan[k] for k in ("version", "evidence")
        ):
            raise ValueError("Episode metadata differs from plan")
        summary = summarize(episode)
        attempts = summary["response_attempts"]
        if attempts > row["max_attempts"] or (
            summary["status"] == "budget_exhausted" and attempts != row["max_attempts"]
        ):
            raise ValueError("Observed attempts conflict with planned budget")
        records[run_id] = summary
    groups = []
    for condition, powered in sorted({(r["condition"], r["powered"]) for r in planned.values()}):
        rows = [r for r in planned.values() if (r["condition"], r["powered"]) == (condition, powered)]
        observed = [records[r["run_id"]] for r in rows if r["run_id"] in records]
        missing = sorted(r["run_id"] for r in rows if r["run_id"] not in records)
        choices = Counter(s["battery_choice"] or "not_observed" for s in observed)
        groups.append({
            "evidence": plan["evidence"], "condition": condition, "powered": powered,
            "planned_runs": len(rows), "recorded_runs": len(observed), "missing_ids": missing,
            "status_counts": dict(Counter(s["status"] for s in observed)),
            "battery_choice_counts_recorded": dict(choices),
            "choice_observed_runs": sum(s["battery_choice"] is not None for s in observed),
            "escaped_runs": sum(s["status"] == "escaped" for s in observed),
            "completed_team_actions": [s["completed_team_actions"] for s in observed
                                       if s["completed_team_actions"] is not None],
        })
    return {"version": VERSION, "evidence": plan["evidence"], "groups": groups,
            "runs": [{"run_id": r["run_id"], "condition": r["condition"],
                      "powered": r["powered"], "record": records.get(r["run_id"])}
                     for r in planned.values()]}


def check():
    profiles = {"holder": "舞台技師。\n理由を説明する。  ",
                "partner": "학생. 상대와 서먹하다. 모르면 질문한다."}
    plan = {"version": VERSION, "evidence": "synthetic", "runs": []}
    for condition in ("text-a", "text-b"):
        for powered in (True, False):
            for repetition in range(2):
                p = dict(profiles)
                if condition == "text-b":
                    p["partner"] = p["partner"].replace("서먹하다", "친밀하다")
                plan["runs"].append({"run_id": f"{condition}-{powered}-{repetition}",
                                     "condition": condition, "powered": powered,
                                     "profiles": p, "max_attempts": 11})
    episodes = []
    for i, row in enumerate(plan["runs"][::2]):
        events = iter(audit(row["powered"])["paths"][0]["events"])
        if i == 0:
            def provider(_):
                return json.dumps({"speech": "", "action": next(events)["action"]})
        elif i == 1:
            actions = iter(("prepare_holder_exit", "keep_battery"))
            def provider(_):
                action = next(actions, None)
                if action is None:
                    raise TimeoutError()
                return json.dumps({"speech": "", "action": action})
        elif i == 2:
            provider = lambda _: "malformed"
        else:
            row["max_attempts"] = 1
            provider = lambda _: '{"speech":"","action":"prepare_holder_exit"}'
        episodes.append(run_episode(row["run_id"], row["powered"], row["profiles"], provider,
                                    evidence="synthetic", max_attempts=row["max_attempts"]))
    result = reconcile(plan, episodes)
    assert sum(g["planned_runs"] for g in result["groups"]) == 8
    assert sum(g["recorded_runs"] for g in result["groups"]) == 4
    assert sum(len(g["missing_ids"]) for g in result["groups"]) == 4
    assert sum(g["escaped_runs"] for g in result["groups"]) == 1
    assert sum(g["choice_observed_runs"] for g in result["groups"]) == 2
    assert all(len(g["missing_ids"]) == 1 for g in result["groups"])
    partial = result["runs"][2]["record"]
    assert partial["battery_choice"] == "keep_battery" and partial["completed_team_actions"] is None
    assert sum(r["record"] is None for r in result["runs"]) == 4
    assert all(g["recorded_runs"] == 0 for g in reconcile(plan, [])["groups"])
    assert reconcile({**plan, "runs": []}, [])["groups"] == []
    rejected = []
    for case in ("duplicate_plan", "duplicate_record", "unknown_id", "profile_drift",
                 "power_drift", "evidence_drift", "version_drift", "over_budget",
                 "premature_budget_end", "invalid_budget", "tampered_final"):
        p, es = deepcopy(plan), deepcopy(episodes)
        if case == "duplicate_plan":
            p["runs"].append(deepcopy(p["runs"][0]))
        elif case == "duplicate_record":
            es.append(deepcopy(es[0]))
        elif case == "unknown_id":
            es[0]["run_id"] = "unplanned"
        elif case == "profile_drift":
            p["runs"][0]["profiles"]["holder"] += "changed"
        elif case == "power_drift":
            p["runs"][0]["powered"] = False
        elif case == "evidence_drift":
            p["evidence"] = "model"
        elif case == "version_drift":
            es[0]["version"] = "other"
        elif case == "over_budget":
            p["runs"][0]["max_attempts"] = 1
        elif case == "premature_budget_end":
            p["runs"][6]["max_attempts"] = 11
        elif case == "invalid_budget":
            p["runs"][0]["max_attempts"] = True
        else:
            es[0]["final"]["escape"]["battery"] = "invented"
        try:
            reconcile(p, es)
        except ValueError:
            rejected.append(case)
        else:
            raise AssertionError(case)
    return {"evidence": "synthetic", "planned": 8, "recorded": 4, "missing": 4,
            "rejected_checks": rejected, "report": result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("plan", nargs="?")
    parser.add_argument("episodes", nargs="?")
    args = parser.parse_args()
    if args.check:
        result = check()
    else:
        if not args.plan or not args.episodes:
            parser.error("Provide plan JSON and episode JSONL")
        with open(args.plan, encoding="utf-8") as f:
            plan = json.load(f)
        with open(args.episodes, encoding="utf-8") as f:
            result = reconcile(plan, [json.loads(line) for line in f if line.strip()])
    print(json.dumps(result, ensure_ascii=False, indent=2))
