"""Audit a first-action pilot JSONL ledger against the 80 planned requests.

Each row has run_id and attempts (one or two entries). Each attempt is either
{"response": "<raw model text>"} or {"transport_error": "<error category>"}.
Only a transport error may precede a second attempt. Absent rows remain
unrecorded. Run with --check for synthetic verification.
"""

import argparse
import json
import sys
from collections import Counter

from plan_handoff_pilot import interpret_response, make_plan


OUTCOMES = (
    "handoff", "no_handoff", "illegal_action", "malformed_response",
    "transport_failure", "retry_pending", "unrecorded",
)


def audit(records):
    plan = {row["run_id"]: row["condition"] for row in make_plan()}
    seen = set()
    counts = {condition: Counter() for condition in dict.fromkeys(plan.values())}
    for record in records:
        run_id = record["run_id"]
        if run_id not in plan or run_id in seen:
            raise ValueError(f"Unknown or duplicate run ID: {run_id}")
        seen.add(run_id)
        attempts = record["attempts"]
        if not isinstance(attempts, list) or len(attempts) not in (1, 2):
            raise ValueError(f"Expected one or two attempts: {run_id}")
        for attempt in attempts:
            if (not isinstance(attempt, dict) or len(attempt) != 1
                    or not attempt.keys() <= {"transport_error", "response"}
                    or not all(isinstance(value, str) for value in attempt.values())):
                raise ValueError(f"Malformed attempt record: {run_id}")
        if len(attempts) == 2 and "transport_error" not in attempts[0]:
            raise ValueError(f"Only a transport error permits a retry: {run_id}")
        last = attempts[-1]
        if "transport_error" in last:
            outcome = "retry_pending" if len(attempts) == 1 else "transport_failure"
        else:
            outcome, _ = interpret_response(last["response"])
        counts[plan[run_id]][outcome] += 1

    for run_id in plan.keys() - seen:
        counts[plan[run_id]]["unrecorded"] += 1

    conditions = {}
    bounds = {}
    for condition, count in counts.items():
        planned = sum(count.values())
        valid = count["handoff"] + count["no_handoff"]
        handoffs = count["handoff"]
        unknown = planned - valid
        bounds[condition] = (handoffs, handoffs + unknown, planned)
        conditions[condition] = {
            "planned": planned,
            "valid": valid,
            "outcomes": {key: count[key] for key in OUTCOMES},
            "valid_handoff_rate": handoffs / valid if valid else None,
            "planned_handoff_rate_bounds": [handoffs / planned, (handoffs + unknown) / planned],
        }

    close_low, close_high, close_total = bounds["close"]
    awkward_low, awkward_high, awkward_total = bounds["awkward"]
    denominator = close_total * awkward_total
    lower = close_low * awkward_total - awkward_high * close_total
    upper = close_high * awkward_total - awkward_low * close_total
    close_rate = conditions["close"]["valid_handoff_rate"]
    awkward_rate = conditions["awkward"]["valid_handoff_rate"]
    return {
        "conditions": conditions,
        "close_minus_awkward_valid_rate": (
            close_rate - awkward_rate if close_rate is not None and awkward_rate is not None else None
        ),
        "close_minus_awkward_bounds": [lower / denominator, upper / denominator],
        "direction_under_all_missing_assignments": (
            "positive" if lower > 0 else "negative" if upper < 0
            else "zero" if lower == upper == 0 else "unresolved"
        ),
    }


def check():
    def row(request, action):
        return {"run_id": request["run_id"], "attempts": [
            {"response": json.dumps({"speech": "열쇠를 줄게.", "action": action})}
        ]}

    plan = list(make_plan())
    close = [r for r in plan if r["condition"] == "close"]
    awkward = [r for r in plan if r["condition"] == "awkward"]
    complete = [row(r, "hand_key" if r["condition"] == "close" else "prepare_holder_exit") for r in plan]
    positive = audit(complete)
    assert positive["close_minus_awkward_bounds"] == [1, 1]
    assert positive["direction_under_all_missing_assignments"] == "positive"
    negative = [row(r, "hand_key" if r["condition"] == "awkward" else "prepare_holder_exit")
                for r in plan]
    assert audit(negative)["close_minus_awkward_bounds"] == [-1, -1]
    assert audit(negative)["direction_under_all_missing_assignments"] == "negative"
    assert audit([row(r, "hand_key") for r in plan])["direction_under_all_missing_assignments"] == "zero"
    assert audit([])["close_minus_awkward_bounds"] == [-1, 1]
    assert audit([])["close_minus_awkward_valid_rate"] is None

    partial = [row(r, "hand_key") for r in close[:20]]
    partial += [row(r, "prepare_holder_exit") for r in awkward[:20]]
    assert audit(partial)["close_minus_awkward_valid_rate"] == 1
    assert audit(partial)["close_minus_awkward_bounds"] == [0, 1]
    assert audit(partial)["direction_under_all_missing_assignments"] == "unresolved"
    assert audit(partial[1:])["close_minus_awkward_bounds"] == [-0.025, 1]

    transport = {"transport_error": "synthetic_timeout"}
    mixed = [
        {"run_id": close[0]["run_id"], "attempts": [transport]},
        {"run_id": close[1]["run_id"], "attempts": [transport, transport]},
        {"run_id": close[2]["run_id"], "attempts": [transport, *row(close[2], "hand_key")["attempts"]]},
        {"run_id": close[3]["run_id"], "attempts": [{"response": "열쇠를 줄게."}]},
        row(close[4], "invent_exit"),
        row(close[5], "prepare_holder_exit"),
    ]
    assert audit(mixed)["conditions"]["close"]["outcomes"] == dict.fromkeys(OUTCOMES, 1) | {
        "unrecorded": 34
    }
    bad_retry = dict(complete[0], attempts=[*complete[0]["attempts"], transport])
    for invalid in ([bad_retry], [complete[0]] * 2, [{"run_id": "unknown", "attempts": [transport]}]):
        try:
            audit(invalid)
        except ValueError:
            continue
        raise AssertionError("Invalid ledger accepted")
    print("PASS: complete, empty, mixed, boundary and invalid synthetic ledgers")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        records = (json.loads(line) for line in sys.stdin if line.strip())
        print(json.dumps(audit(records), ensure_ascii=False, indent=2))
