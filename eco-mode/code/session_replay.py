"""Replay an append-only experimental event log. No model or sensor is invoked."""
import argparse
import hashlib
import json
from pathlib import Path

SCALE = {"J": 1.0, "mJ": 0.001, "uJ": 0.000001}
ARMS = {"Low", "Fast", "Eco"}
MODES = {"low", "high"}
OUTCOMES = {"success", "failure", "abandoned", "timeout", "not_started", "unknown"}

def canonical_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode()).hexdigest()

def mode_hash(config, mode):
    if mode not in MODES:
        raise ValueError("unrecognised mode")
    return canonical_hash({"common": config["common"], "mode": config["modes"][mode]})

def response_observation(payload, schema):
    """Validate a PINNED response field; never turn a missing field into 0 tokens."""
    key = schema["reasoning_field"]
    count_key = schema["reasoning_token_field"]
    schema_ok = isinstance(payload.get(key), str)
    count = payload.get(count_key)
    count_ok = type(count) is int and count >= 0
    return {"response_schema_version": schema["version"],
            "payload_schema_valid": schema_ok and count_ok,
            "observed_reasoning_tokens": count if schema_ok and count_ok else None,
            "reason": None if schema_ok and count_ok else "missing_or_invalid_pinned_field"}

def replay(doc):
    if doc.get("measurement_kind") not in {"synthetic", "device_counter"}:
        raise ValueError("measurement_kind must be explicit")
    config, events = doc["backend_config"], doc["events"]
    if not isinstance(events, list) or not events:
        raise ValueError("nonempty events required")
    if set(config["modes"]) != MODES:
        raise ValueError("exactly low and high modes required")
    for mode in MODES:
        spec = config["modes"][mode]
        if (set(spec) != {"thinking_token_budget"} or
                type(spec["thinking_token_budget"]) is not int or spec["thinking_token_budget"] <= 0):
            raise ValueError("only a positive intended thinking_token_budget may vary")
    if config["modes"]["low"]["thinking_token_budget"] >= config["modes"]["high"]["thinking_token_budget"]:
        raise ValueError("intended low budget must be below high; this does not verify execution")
    issues, seen, clean = [], {}, []
    def flag(code):
        if code not in issues:
            issues.append(code)
    for event in events:
        if (not isinstance(event, dict) or type(event.get("t_ns")) is not int
                or event["t_ns"] < 0 or type(event.get("server_seq")) is not int
                or event["server_seq"] <= 0 or not isinstance(event.get("session_id"), str)
                or not event["session_id"].strip()):
            raise ValueError("invalid event schema: nonempty session ID and integer time/sequence required")
        ident = event.get("event_id")
        if not isinstance(ident, str) or not ident:
            flag("invalid_event_id"); continue
        if ident in seen:
            if seen[ident] != event:
                flag("conflicting_duplicate_event")
            continue
        seen[ident] = event
        clean.append(event)
    if not clean:
        raise ValueError("no usable events")
    start = clean[0]
    if start.get("type") != "session_start":
        raise ValueError("first event must be session_start")
    sid = start.get("session_id")
    participant_id = start.get("participant_id")
    if not isinstance(participant_id, str) or not participant_id.strip():
        raise ValueError("explicit pseudonymous participant_id required")
    tasks = start.get("assigned_task_ids", [])
    if (not tasks or any(not isinstance(x, str) for x in tasks)
            or len(set(tasks)) != len(tasks)):
        raise ValueError("unique assigned tasks required")
    if start.get("assigned_arm") not in ARMS:
        raise ValueError("unknown arm")
    if start.get("backend_hash") != canonical_hash(config):
        flag("backend_hash_mismatch")
    if any(x in config["common"] for x in ("label", "assigned_arm", "arm")):
        flag("label_in_backend_config")
    state, active, attempts, requests = "allocated", {}, {}, {}
    last_seq, last_t = 0, -1
    counters, first_mode = [], None
    finish, drained_t, close_reason = None, None, None
    overlap = False

    def counter(event):
        sample = event.get("counter")
        if not isinstance(sample, dict):
            flag("missing_counter"); return None
        value = sample.get("value_raw")
        read_start, read_end = sample.get("read_start_ns"), sample.get("read_end_ns")
        identity = [sample.get(k) for k in ("source", "device", "scope", "epoch", "unit")]
        if (type(value) is not int or value < 0 or
                type(read_start) is not int or type(read_end) is not int or
                not 0 <= read_start <= read_end <= event["t_ns"] or
                any(not isinstance(x, str) or not x for x in identity) or
                sample.get("unit") not in SCALE):
            flag("invalid_counter"); return None
        counters.append(sample)
        return sample

    start_counter = None
    for event in clean:
        seq, stamp = event.get("server_seq"), event.get("t_ns")
        if type(seq) is not int or seq != last_seq + 1:
            flag("sequence_gap_or_reorder")
        if type(stamp) is not int or stamp < last_t or stamp < 0:
            flag("nonmonotonic_event_clock")
            stamp = last_t
        if type(seq) is int:
            last_seq = seq
        last_t = stamp
        if event.get("session_id") != sid:
            flag("mixed_session")
        kind = event.get("type")
        if state == "closed":
            flag("event_after_session_end")
        if kind == "session_start":
            if event is not start:
                flag("multiple_session_start")
            start_counter = counter(event)
        elif kind == "request_submitted":
            rid, mode, task = event.get("request_id"), event.get("mode"), event.get("task_id")
            if state not in {"allocated", "active"}:
                flag("request_after_close")
            if not isinstance(rid, str) or not rid or rid in requests:
                flag("request_id_invalid_or_reused")
            if mode not in MODES or task not in tasks:
                flag("invalid_request")
            else:
                if event.get("effective_config_hash") != mode_hash(config, mode):
                    flag("mode_config_hash_mismatch")
                requests[rid] = {"mode": mode, "task": task, "t_ns": stamp}
                if first_mode is None:
                    first_mode = mode
        elif kind == "attempt_start":
            aid, rid = event.get("attempt_id"), event.get("request_id")
            sample = counter(event)
            if state not in {"allocated", "active"}:
                flag("attempt_after_close")
            if active:
                flag("overlapping_attempts"); overlap = True
            if not isinstance(aid, str) or not aid or aid in attempts:
                flag("attempt_id_reused")
            req = requests.get(rid)
            if not req:
                flag("attempt_without_submission")
            elif event.get("effective_config_hash") != mode_hash(config, req["mode"]):
                flag("mode_config_hash_mismatch")
            attempt = {"start": sample, "end": None, "start_t": stamp,
                       "request_id": rid, "cancel_requested": False, "stop_t": None}
            active[aid] = attempt
            attempts[aid] = attempt
            state = "active" if state in {"allocated", "active"} else state
        elif kind == "cancel_requested":
            aid = event.get("attempt_id")
            if aid not in active:
                flag("cancel_unknown_attempt")
            else:
                active[aid]["cancel_requested"] = True
        elif kind == "attempt_end":
            aid = event.get("attempt_id")
            sample = counter(event)
            if aid not in active:
                flag("end_unknown_attempt")
            else:
                active[aid]["end"] = sample
                active[aid]["stop_t"] = stamp
                active[aid]["status"] = event.get("status")
                if event.get("status") not in {"success", "failure", "cancelled"}:
                    flag("invalid_attempt_status")
                del active[aid]
        elif kind == "close_requested":
            if state not in {"allocated", "active"}:
                flag("duplicate_close")
            close_reason = event.get("reason")
            if close_reason not in {"complete", "abandoned", "timeout"}:
                flag("invalid_close_reason")
            state = "draining"
        elif kind == "backend_drained":
            if state != "draining" or active:
                flag("drained_with_active_or_without_close")
            drained_t = stamp
            state = "drained"
        elif kind == "session_end":
            sample = counter(event)
            if state != "drained" or active:
                flag("end_before_backend_drained")
            if sample and (drained_t is None or sample["read_start_ns"] < drained_t):
                flag("final_read_before_backend_drained")
            finish = {**event, "_counter": sample}
            state = "closed"
        elif kind != "transport_disconnected":
            flag("unknown_event_type")

    complete = bool(finish and finish.get("logging_complete") is True
                    and "sequence_gap_or_reorder" not in issues
                    and "conflicting_duplicate_event" not in issues)
    if not complete:
        flag("event_log_incomplete")
    if active:
        flag("active_at_log_end")
    if not finish:
        flag("session_end_missing")

    def same(a, b):
        return bool(a and b and all(a[k] == b[k] for k in
                    ("source", "device", "scope", "epoch", "unit")))
    end_counter = finish["_counter"] if finish else None
    raw_delta = None
    if same(start_counter, end_counter):
        delta = end_counter["value_raw"] - start_counter["value_raw"]
        if delta >= 0:
            raw_delta = delta
        else:
            flag("counter_decreased")
    else:
        flag("counter_identity_or_epoch_changed")
    previous = None
    for sample in counters:
        if previous:
            if not same(previous, sample):
                flag("counter_identity_or_epoch_changed")
            elif sample["value_raw"] < previous["value_raw"]:
                flag("counter_decreased")
            if sample["read_start_ns"] < previous["read_end_ns"]:
                flag("overlapping_read_brackets")
        previous = sample

    active_raw, active_complete, previous_stop = 0, True, None
    for attempt in attempts.values():
        a, b = attempt["start"], attempt["end"]
        if (not same(a, b) or not same(start_counter, a) or not same(start_counter, b)
                or b["value_raw"] < a["value_raw"]):
            active_complete = False; continue
        if a["read_end_ns"] > b["read_start_ns"]:
            flag("attempt_counter_bracket_reversed")
        if start_counter and start_counter["read_end_ns"] > a["read_start_ns"]:
            flag("attempt_before_session_boundary")
        if end_counter and b["read_end_ns"] > end_counter["read_start_ns"]:
            flag("attempt_after_session_boundary")
        if previous_stop is not None and a["read_start_ns"] < previous_stop:
            flag("overlapping_attempt_brackets"); overlap = True
        previous_stop = b["read_end_ns"]
        active_raw += b["value_raw"] - a["value_raw"]
    if raw_delta is not None and active_complete and active_raw > raw_delta:
        flag("active_energy_exceeds_session")
    valid = raw_delta is not None and not issues
    scale = SCALE[start_counter["unit"]] if start_counter else None
    total = raw_delta * scale if valid else None
    active_j = active_raw * scale if scale and active_complete and not overlap else None
    if "active_energy_exceeds_session" in issues:
        active_j = None
    outcomes = finish.get("outcomes", {}) if finish else {}
    if set(outcomes) - set(tasks):
        flag("unassigned_task_outcome")
    for task in tasks:
        result = outcomes.get(task, "unknown")
        if result not in OUTCOMES:
            flag("invalid_task_outcome")
        if result == "not_started" and any(r["task"] == task for r in requests.values()):
            flag("not_started_has_submission")
    quality = {task: outcomes.get(task, "unknown") if complete else "unknown" for task in tasks}
    if any(x not in OUTCOMES for x in quality.values()):
        quality = {task: "unknown" for task in tasks}
    # Energy physical validity and quality-schema validity are distinct audits.
    if any(x in issues for x in ("unassigned_task_outcome", "not_started_has_submission",
                                  "invalid_task_outcome")):
        quality = {task: "unknown" for task in tasks}
    semantic_issues = {"mixed_session", "nonmonotonic_event_clock", "multiple_session_start",
        "backend_hash_mismatch", "mode_config_hash_mismatch", "label_in_backend_config",
        "request_after_close", "request_id_invalid_or_reused", "invalid_request",
        "attempt_after_close", "attempt_without_submission", "attempt_id_reused",
        "cancel_unknown_attempt", "end_unknown_attempt", "duplicate_close",
        "event_after_session_end", "unknown_event_type", "invalid_attempt_status",
        "invalid_close_reason", "drained_with_active_or_without_close", "end_before_backend_drained"}
    trustworthy_events = complete and not semantic_issues.intersection(issues)
    if not trustworthy_events:
        quality = {task: "unknown" for task in tasks}
    first_choice = (first_mode or "none") if trustworthy_events else "unknown"
    # A partial sum is not a lower bound if identity, order or boundaries failed.
    floor_unsafe = {"counter_identity_or_epoch_changed", "counter_decreased", "invalid_counter",
        "overlapping_read_brackets", "attempt_counter_bracket_reversed",
        "attempt_before_session_boundary", "attempt_after_session_boundary",
        "overlapping_attempts", "overlapping_attempt_brackets", "active_energy_exceeds_session"}
    if floor_unsafe.intersection(issues) or not trustworthy_events:
        active_j = None
    modes = [r["mode"] for r in requests.values()]
    sensor = doc.get("sensor_evidence", {})
    return {
        "schema_version": 2, "session_id": sid, "participant_id": participant_id,
        "assigned_arm": start["assigned_arm"],
        "frozen_backend_hash": canonical_hash(config),
        "measurement_boundary": ({k:start_counter[k] for k in ("source", "device", "scope", "unit")}
                                 if start_counter else None),
        "measurement_kind": doc["measurement_kind"], "assigned_task_ids": tasks,
        "raw_first_submitted_mode": first_mode, "reported_outcomes": outcomes,
        "protocol_observation_valid": trustworthy_events,
        "first_choice": first_choice, "outcomes": quality,
        "attempts": len(attempts), "requests": len(requests),
        "additional_requests": max(0, len(requests) - 1),
        "mode_switches": sum(a != b for a, b in zip(modes, modes[1:])),
        "event_log_complete": complete, "energy_valid": valid,
        "measured_total_energy_j": total if doc["measurement_kind"] == "device_counter" else None,
        "synthetic_total_energy_j": total if doc["measurement_kind"] == "synthetic" else None,
        "raw_session_counter_delta_j": raw_delta * scale if raw_delta is not None and scale else None,
        "secondary_active_energy_j": active_j,
        "secondary_residual_energy_j": total - active_j if total is not None and active_j is not None else None,
        "known_floor_j": active_j if active_j is not None else None,
        "missing_energy_upper_j": None,
        "timing_uncertainty_known": sensor.get("timing_uncertainty_known") is True,
        "epoch_evidence": sensor.get("epoch_evidence"),
        "sensor_evidence_independently_verified": False,
        "close_reason": close_reason, "audit_passed": not issues, "issues": issues,
        "confirmatory_ready": False,
        "notice": "Input provenance is declared, not independently authenticated. Synthetic values are not sensor measurements."
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(json.loads(args.log.read_text())), indent=2, allow_nan=False))

if __name__ == "__main__":
    main()

