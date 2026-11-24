"""Replay and summarize v3 episode JSONL records.

Usage: python3 scripts/report_escape_v3.py < episodes.jsonl
Use --check for synthetic verification. Episodes with inconsistent records
are rejected. Synthetic and model evidence and gate states stay separate.
"""

import argparse
import json
import sys
from collections import Counter
from copy import deepcopy

from run_escape_v3 import run_episode
from replay_escape_v3 import audit


def summarize(episode):
    turns = episode["turns"]
    if not turns:
        raise ValueError("An episode must contain at least one response attempt")
    recorded = iter(turns)

    def replay_response(_):
        turn = next(recorded)
        if "transport_error" in turn:
            errors = {"TimeoutError": TimeoutError, "ConnectionError": ConnectionError}
            if turn["transport_error"] not in errors:
                raise ValueError("Unknown recorded transport error")
            raise errors[turn["transport_error"]]()
        return turn["raw_response"]

    replayed = run_episode(
        episode["run_id"], episode["powered"], episode["profiles"], replay_response,
        evidence=episode["evidence"], max_attempts=len(turns),
    )
    if replayed != episode:
        raise ValueError("Recorded episode differs from replay of raw responses")
    accepted = [t["event"] for t in turns if t.get("event", {}).get("accepted")]
    choices = [e["action"] for e in accepted if e["action"] in ("lend_battery", "keep_battery")]
    observed = episode["final"]["escape"]["route"]["actions"]
    assert observed == len(accepted) and len(choices) <= 1
    return {
        "run_id": episode["run_id"], "evidence": episode["evidence"],
        "powered": episode["powered"], "status": episode["status"],
        "response_attempts": len(turns), "accepted_actions_observed": observed,
        "completed_team_actions": observed if episode["status"] == "escaped" else None,
        "battery_choice": choices[0] if choices else None,
        "battery_final": episode["final"]["escape"]["battery"],
    }


def report(episodes):
    summaries = []
    seen = set()
    for episode in episodes:
        if episode["run_id"] in seen:
            raise ValueError("Duplicate run ID")
        seen.add(episode["run_id"])
        summaries.append(summarize(episode))
    groups = []
    for evidence, powered in sorted({(s["evidence"], s["powered"]) for s in summaries}):
        rows = [s for s in summaries if (s["evidence"], s["powered"]) == (evidence, powered)]
        groups.append({
            "evidence": evidence, "powered": powered, "recorded_runs": len(rows),
            "status_counts": dict(Counter(s["status"] for s in rows)),
            "battery_choice_counts": dict(Counter(s["battery_choice"] or "not_observed" for s in rows)),
            "battery_consumed_observed": sum(s["battery_final"] == "consumed" for s in rows),
            "completed_team_actions": [s["completed_team_actions"] for s in rows
                                       if s["completed_team_actions"] is not None],
        })
    return {"episodes": summaries, "groups": groups}


def check():
    profiles = {"holder": "교수. 결정을 설명하고 다른 의견을 듣는다.",
                "partner": "학생. 불확실한 부분에 질문한다."}
    episodes = []
    for powered in (True, False):
        for number, path in enumerate(audit(powered)["paths"]):
            events = iter(path["events"])

            def provider(_):
                return json.dumps({"speech": "배터리를 건넸다.", "action": next(events)["action"]})

            episode = run_episode(f"complete-{powered}-{number}", powered, profiles, provider,
                                  evidence="synthetic")
            summary = summarize(episode)
            assert summary["completed_team_actions"] == path["team_actions"]
            assert summary["battery_choice"] == path["battery_choice"]
            assert summary["battery_final"] == path["battery_final"]
            episodes.append(episode)

    responses = (
        ("malformed", "형식이 틀린 응답", "malformed_response"),
        ("illegal", '{"speech":"","action":"invent_exit"}', "illegal_action"),
    )
    for run_id, raw, status in responses:
        episode = run_episode(run_id, True, profiles, lambda _: raw, evidence="synthetic")
        assert summarize(episode)["status"] == status
        episodes.append(episode)

    def timeout(_):
        raise TimeoutError()

    episodes.append(run_episode("timeout", True, profiles, timeout, evidence="synthetic"))
    prepare = lambda _: '{"speech":"","action":"prepare_holder_exit"}'
    episodes.append(run_episode("budget", True, profiles, prepare, evidence="synthetic", max_attempts=1))
    partial_actions = iter(("prepare_holder_exit", "keep_battery"))

    def partial(_):
        action = next(partial_actions, None)
        if action is None:
            raise TimeoutError()
        return json.dumps({"speech": "", "action": action})

    stopped = run_episode("stopped-after-choice", False, profiles, partial, evidence="synthetic")
    s = summarize(stopped)
    assert s["battery_choice"] == "keep_battery" and s["completed_team_actions"] is None
    assert s["accepted_actions_observed"] == 2 and s["battery_final"] == "partner"
    episodes.append(stopped)
    result = report(episodes)
    assert len(result["episodes"]) == 15
    assert sum(g["recorded_runs"] for g in result["groups"]) == 15
    assert sum(len(g["completed_team_actions"]) for g in result["groups"]) == 10
    for change in ("final", "status", "event"):
        bad = deepcopy(episodes[0])
        if change == "final":
            bad["final"]["escape"]["battery"] = "invented"
        elif change == "status":
            bad["status"] = "budget_exhausted"
        else:
            bad["turns"][0]["event"]["accepted"] = False
        try:
            summarize(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("Inconsistent episode accepted")
    try:
        report([episodes[0], episodes[0]])
    except ValueError:
        pass
    else:
        raise AssertionError("Duplicate episode accepted")
    assert report([]) == {"episodes": [], "groups": []}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = check() if args.check else report(json.loads(line) for line in sys.stdin if line.strip())
    print(json.dumps(result, ensure_ascii=False, indent=2))
