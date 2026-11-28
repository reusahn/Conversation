"""Audit a provider-neutral receipt contract against v3 episode turns.

Usage: python3 scripts/audit_provider_calls_v3.py bundle.json
Bundle fields: plan, episodes, receipts. The plan adds provider_config with
provider, model_snapshot and generation. This checks local consistency only;
receipts must be retained by a future real adapter. No network is used here.
"""

import argparse
import json
from copy import deepcopy

from bind_escape_v3 import digest
from reconcile_escape_v3 import reconcile
from replay_escape_v3 import VERSION, audit
from run_escape_v3 import run_episode


def audit_calls(plan, episodes, receipts):
    report = reconcile(plan, episodes)
    config = plan["provider_config"]
    if set(config) != {"provider", "model_snapshot", "generation"} or any(
        not isinstance(config[k], str) or not config[k].strip()
        for k in ("provider", "model_snapshot")
    ) or not isinstance(config["generation"], dict):
        raise ValueError("Declare provider, model snapshot and generation settings")
    digest(config)  # Require JSON values, including finite numeric settings.
    turns = {}
    for episode in episodes:
        for turn in episode["turns"]:
            if turn["turn_id"] in turns:
                raise ValueError("Duplicate turn ID")
            turns[turn["turn_id"]] = turn
    seen, request_ids, response_ids = set(), set(), set()
    known_usage = {"input_tokens": 0, "output_tokens": 0}
    unknown_usage = 0
    outcomes = {"returned": 0, "unknown": 0}
    for receipt in receipts:
        turn_id = receipt["turn_id"]
        if turn_id not in turns or turn_id in seen:
            raise ValueError("Unplanned or duplicate receipt turn")
        seen.add(turn_id)
        turn = turns[turn_id]
        if receipt["evidence"] != plan["evidence"] or receipt["plan_sha256"] != digest(plan):
            raise ValueError("Evidence or plan digest mismatch")
        expected_request = digest({"messages": turn["messages"], "config": config})
        if receipt["request_sha256"] != expected_request:
            raise ValueError("Request content/settings mismatch")
        transport_error = "transport_error" in turn
        outcome = "unknown" if transport_error else "returned"
        if receipt["outcome"] != outcome:
            raise ValueError("Transport outcome mismatch")
        outcomes[outcome] += 1
        for field, identifiers in (("provider_request_id", request_ids), ("response_id", response_ids)):
            value = receipt[field]
            if value is None:
                if not transport_error:
                    raise ValueError("Returned response needs provider identifiers")
            elif not isinstance(value, str) or not value.strip() or value in identifiers:
                raise ValueError("Invalid or reused provider identifier")
            else:
                identifiers.add(value)
        if transport_error:
            if receipt["raw_response"] is not None or receipt["response_id"] is not None:
                raise ValueError("Unknown outcome cannot invent a returned response")
        elif receipt["raw_response"] != turn["raw_response"]:
            raise ValueError("Raw response mismatch")
        if receipt["reported_model"] is not None and receipt["reported_model"] != config["model_snapshot"]:
            raise ValueError("Reported model differs from requested snapshot")
        if not transport_error and receipt["reported_model"] is None:
            raise ValueError("Returned model identity missing")
        usage = receipt["usage"]
        if usage is None:
            unknown_usage += 1
        else:
            if not isinstance(usage, dict) or set(usage) != set(known_usage) or any(
                type(n) is not int or n < 0 for n in usage.values()
            ):
                raise ValueError("Usage must be unknown or reported nonnegative integer counters")
            for k in known_usage:
                known_usage[k] += usage[k]
    if seen != set(turns):
        raise ValueError("Missing call receipt")
    return {"evidence": plan["evidence"], "turns_with_receipts": len(seen),
            "outcomes": outcomes, "usage_known_subtotal": known_usage,
            "usage_unknown_calls": unknown_usage,
            "usage_total": known_usage if unknown_usage == 0 else None,
            "episode_report": report}


def check():
    profiles = {"holder": "舞台技師。\n説明する。  ", "partner": "학생. 질문한다."}
    config = {"provider": "synthetic-fixture", "model_snapshot": "fake-snapshot-1",
              "generation": {"temperature": 0, "max_output_tokens": 128}}
    plan = {"version": VERSION, "evidence": "synthetic", "provider_config": config,
            "runs": [{"run_id": name, "condition": "fixture", "powered": True,
                      "profiles": profiles, "max_attempts": 11}
                     for name in ("complete", "malformed", "timeout")]}
    events = iter(audit(True)["paths"][0]["events"])
    def provider(_):
        return json.dumps({"speech": "", "action": next(events)["action"]})
    def timeout(_):
        raise TimeoutError()
    episodes = [run_episode("complete", True, profiles, provider, evidence="synthetic"),
                run_episode("malformed", True, profiles, lambda _: "not JSON", evidence="synthetic"),
                run_episode("timeout", True, profiles, timeout, evidence="synthetic")]
    receipts = []
    for episode in episodes:
        for turn in episode["turns"]:
            unknown = "transport_error" in turn
            receipts.append({
                "turn_id": turn["turn_id"], "evidence": "synthetic", "plan_sha256": digest(plan),
                "request_sha256": digest({"messages": turn["messages"], "config": config}),
                "provider_request_id": None if unknown else "req-" + turn["turn_id"],
                "response_id": None if unknown else "resp-" + turn["turn_id"],
                "outcome": "unknown" if unknown else "returned",
                "raw_response": None if unknown else turn["raw_response"],
                "reported_model": None if unknown else config["model_snapshot"],
                "usage": None if unknown else {"input_tokens": 10, "output_tokens": 2},
            })
    result = audit_calls(plan, episodes, receipts)
    assert result["turns_with_receipts"] == 9 and result["outcomes"] == {"returned": 8, "unknown": 1}
    assert result["usage_total"] is None and result["usage_unknown_calls"] == 1
    assert result["usage_known_subtotal"] == {"input_tokens": 80, "output_tokens": 16}
    assert result["episode_report"]["groups"][0]["status_counts"] == {
        "escaped": 1, "malformed_response": 1, "infrastructure_error": 1}
    assert audit_calls(plan, episodes, list(reversed(receipts))) == result
    known = audit_calls(plan, episodes[:2], receipts[:-1])
    assert known["usage_total"] == {"input_tokens": 80, "output_tokens": 16}
    assert known["episode_report"]["groups"][0]["missing_ids"] == ["timeout"]
    missing_usage = deepcopy(receipts)
    missing_usage[0]["usage"] = None
    assert audit_calls(plan, episodes, missing_usage)["usage_unknown_calls"] == 2
    rejected = []
    for case in ("missing", "duplicate_turn", "unknown_turn", "reused_request", "reused_response",
                 "settings_hash", "plan_hash", "raw_response", "reported_model", "evidence",
                 "negative_usage", "boolean_usage", "invented_timeout_response", "false_outcome"):
        rs = deepcopy(receipts)
        if case == "missing":
            rs.pop()
        elif case == "duplicate_turn":
            rs.append(deepcopy(rs[0]))
        elif case == "unknown_turn":
            rs[0]["turn_id"] = "absent"
        elif case == "reused_request":
            rs[1]["provider_request_id"] = rs[0]["provider_request_id"]
        elif case == "reused_response":
            rs[1]["response_id"] = rs[0]["response_id"]
        elif case == "settings_hash":
            rs[0]["request_sha256"] = digest({"messages": episodes[0]["turns"][0]["messages"],
                                              "config": {**config, "generation": {"temperature": 1}}})
        elif case == "plan_hash":
            rs[0]["plan_sha256"] = "other"
        elif case == "raw_response":
            rs[0]["raw_response"] += "changed"
        elif case == "reported_model":
            rs[0]["reported_model"] = "other-model"
        elif case == "evidence":
            rs[0]["evidence"] = "model"
        elif case == "negative_usage":
            rs[0]["usage"]["input_tokens"] = -1
        elif case == "boolean_usage":
            rs[0]["usage"]["input_tokens"] = True
        elif case == "invented_timeout_response":
            rs[-1]["raw_response"] = "success"
        else:
            rs[-1]["outcome"] = "returned"
        try:
            audit_calls(plan, episodes, rs)
        except ValueError:
            rejected.append(case)
        else:
            raise AssertionError(case)
    return {k: v for k, v in result.items() if k != "episode_report"} | {
        "rejected_checks": rejected, "actual_model_calls": 0, "participants": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("bundle", nargs="?")
    args = parser.parse_args()
    if args.check:
        result = check()
    else:
        if not args.bundle:
            parser.error("Provide bundle JSON")
        with open(args.bundle, encoding="utf-8") as f:
            bundle = json.load(f)
        result = audit_calls(bundle["plan"], bundle["episodes"], bundle["receipts"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
