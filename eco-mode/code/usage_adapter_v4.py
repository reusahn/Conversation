"""Declared usage-contract prototype; NOT a validated provider adapter.

The declared Chat-Completions-shaped contract defines completion_tokens as
including reasoning_tokens and prompt_tokens as including cached_tokens. Only
authoritative final snapshots count. This is not a claim about any live API.

No timing, power, energy, effective-budget, billing, manifest-authentication, or
participant provenance is inferred here. Caller must retain the original inputs.
"""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

SCHEMA_VERSION = "eco-usage-declared-v4.1"


def _id(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    return value


def _canonical(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (ValueError, TypeError) as exc:
        raise ValueError("events must contain finite JSON values") from exc


def _count(value: Any) -> bool:
    # bool is an int subclass, but is never a valid observed token count.
    return type(value) is int and value >= 0


def _usage(value: Any) -> tuple[str, dict[str, int | None] | None, list[str]]:
    if value is None:
        return "missing", None, ["final_usage_missing"]
    if not isinstance(value, dict):
        return "malformed", None, ["usage_not_object"]
    required = ("prompt_tokens", "completion_tokens", "total_tokens")
    absent = [key for key in required if value.get(key) is None]
    invalid = [key for key in required if value.get(key) is not None and not _count(value[key])]
    if invalid:
        return "malformed", None, ["invalid_count:" + key for key in invalid]
    if absent:
        return "missing", None, ["required_field_missing:" + key for key in absent]
    result = {key: value[key] for key in required}
    if result["prompt_tokens"] + result["completion_tokens"] != result["total_tokens"]:
        return "malformed", None, ["total_not_prompt_plus_completion"]
    for container, key, parent in (
        ("prompt_tokens_details", "cached_tokens", "prompt_tokens"),
        ("completion_tokens_details", "reasoning_tokens", "completion_tokens"),
    ):
        details = value.get(container)
        if details is not None and not isinstance(details, dict):
            return "malformed", None, ["details_not_object:" + container]
        component = None if details is None else details.get(key)
        if component is not None and not _count(component):
            return "malformed", None, ["invalid_count:" + key]
        if component is not None and component > result[parent]:
            return "malformed", None, ["subset_exceeds_parent:" + key]
        result[key] = component
    return "complete", result, []


def _energy_boundary() -> dict[str, Any]:
    return {
        "energy_valid": None,
        "energy_unknown_reason": "not_measured_by_usage_adapter",
        "energy_measurement_performed": False,
    }


def aggregate_usage(attempt_manifest: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate a declared attempt manifest, preserving missingness and conflicts.

    Manifest entries require unique attempt_id and nonempty session_id. Events
    require event_id, attempt_id, kind ('chunk'/'final'); final requires response_id.
    Optional event session_id must agree with the manifest. Unknown identities or
    malformed event envelopes raise ValueError; missing/malformed usage and known
    identity conflicts invalidate affected attempts, never silently dropping them.

    Final snapshots with different normalized counts/details are conflicts, even
    if one only adds previously missing details. Providers with legitimate final
    enrichment need their own validated policy; this prototype does not support it.
    No zero-attempt sessions can be established from an attempt-only manifest.
    """
    if not isinstance(attempt_manifest, list) or not isinstance(events, list):
        raise ValueError("attempt_manifest and events must be lists")
    attempts: dict[str, str] = {}
    for item in attempt_manifest:
        if not isinstance(item, dict):
            raise ValueError("manifest entries must be objects")
        aid = _id(item.get("attempt_id"), "attempt_id")
        sid = _id(item.get("session_id"), "session_id")
        if aid in attempts:
            raise ValueError("duplicate attempt_id in manifest: " + aid)
        attempts[aid] = sid

    by_attempt: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_events: dict[str, tuple[str, str]] = {}
    response_attempts: dict[str, set[str]] = defaultdict(set)
    attempt_responses: dict[str, set[str]] = defaultdict(set)
    conflicts: dict[str, set[str]] = defaultdict(set)
    malformed_envelopes: dict[str, set[str]] = defaultdict(set)
    duplicate_event_count = 0
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("events must be objects")
        aid = _id(event.get("attempt_id"), "attempt_id")
        eid = _id(event.get("event_id"), "event_id")
        if aid not in attempts:
            raise ValueError("event outside attempt manifest: " + aid)
        if "session_id" in event and event["session_id"] != attempts[aid]:
            raise ValueError("event session_id conflicts with manifest: " + aid)
        kind = event.get("kind")
        if kind not in ("chunk", "final"):
            raise ValueError("event kind must be chunk or final")
        rid = event.get("response_id")
        if kind == "final" or rid is not None:
            rid = _id(rid, "response_id")
            response_attempts[rid].add(aid)
            attempt_responses[aid].add(rid)
        # JSON envelope validation is strict; usage validation is separate below.
        # NaN/Infinity are malformed counts, not accepted JSON transport values.
        try:
            signature = _canonical(event)
        except ValueError:
            # Preserve known identities even when a numeric payload is invalid,
            # so an invalid retransmission cannot hide a cross-attempt collision.
            try:
                signature = json.dumps(event, sort_keys=True, separators=(",", ":"), allow_nan=True)
            except (ValueError, TypeError) as exc:
                raise ValueError("events must be JSON-serializable objects") from exc
            malformed_envelopes[aid].add("nonfinite_json_event")
        prior = seen_events.get(eid)
        if prior:
            prior_aid, prior_signature = prior
            if prior_signature == signature:
                duplicate_event_count += 1
                continue
            conflicts[prior_aid].add("conflicting_event_id:" + eid)
            conflicts[aid].add("conflicting_event_id:" + eid)
        else:
            seen_events[eid] = (aid, signature)
        by_attempt[aid].append(event)

    for rid, owners in response_attempts.items():
        if len(owners) > 1:
            for aid in owners:
                conflicts[aid].add("response_id_reused_across_attempts:" + rid)
    for aid, responses in attempt_responses.items():
        if len(responses) > 1:
            conflicts[aid].add("multiple_response_ids_in_attempt")

    results = []
    for aid, sid in attempts.items():
        accepted_events = by_attempt[aid]
        finals = [event for event in accepted_events if event["kind"] == "final"]
        status = "missing"
        values: dict[str, int | None] | None = None
        reasons = ["authoritative_final_missing"]
        if finals:
            parsed = [_usage(event.get("usage")) for event in finals]
            signatures = {_canonical(item) for item in parsed}
            if len(signatures) > 1:
                status, reasons = "conflict", ["conflicting_final_snapshots"]
            else:
                status, values, reasons = parsed[0]
        if malformed_envelopes[aid]:
            status, values = "malformed", None
            reasons = sorted(set(reasons) | malformed_envelopes[aid])
        if conflicts[aid]:
            status, values = "conflict", None
            reasons = sorted(set(reasons) | conflicts[aid])
        if status != "complete":
            values = None
        result = {
            "attempt_id": aid,
            "session_id": sid,
            "status": status,
            "token_complete": status == "complete",
            "reported_tokens": values["total_tokens"] if values else None,
            "prompt_tokens": values["prompt_tokens"] if values else None,
            "completion_tokens": values["completion_tokens"] if values else None,
            "cached_tokens": values["cached_tokens"] if values else None,
            "reasoning_tokens": values["reasoning_tokens"] if values else None,
            "reasons": reasons,
            "source_event_ids": sorted(set(event["event_id"] for event in finals)),
            "observed_event_ids": sorted(set(event["event_id"] for event in accepted_events)),
            "response_ids": sorted(attempt_responses[aid]),
            "token_completeness_scope": "declared_attempt_manifest_only",
            "manifest_completeness_authenticated": False,
            **_energy_boundary(),
        }
        results.append(result)

    sessions = []
    session_ids = list(dict.fromkeys(attempts.values()))
    for sid in session_ids:
        members = [row for row in results if row["session_id"] == sid]
        complete = all(row["token_complete"] for row in members)
        component_complete = {
            key: complete and all(row[key] is not None for row in members)
            for key in ("prompt_tokens", "completion_tokens", "cached_tokens", "reasoning_tokens")
        }
        sessions.append({
            "session_id": sid,
            "attempt_ids": [row["attempt_id"] for row in members],
            "token_complete": complete,
            "reported_tokens": sum(row["reported_tokens"] for row in members) if complete else None,
            **{key: sum(row[key] for row in members) if component_complete[key] else None
               for key in component_complete},
            "unknown_attempt_ids": [row["attempt_id"] for row in members if not row["token_complete"]],
            "token_completeness_scope": "declared_attempt_manifest_only",
            "manifest_completeness_authenticated": False,
            **_energy_boundary(),
        })

    return {
        "schema_version": SCHEMA_VERSION,
        "metric": "reported_tokens",
        "metric_definition": {
            "unit": "declared_provider_reported_tokens",
            "source_field": "final.usage.total_tokens",
            "formula": "prompt_tokens + completion_tokens",
            "cached_tokens_scope": "subset_of_prompt_tokens_do_not_add_again",
            "reasoning_tokens_scope": "subset_of_completion_tokens_do_not_add_again",
            "authority": "declared_final_snapshot_only",
            "provider_semantics_verified": False,
        },
        "attempts": results,
        "sessions": sessions,
        "duplicate_event_count": duplicate_event_count,
        "input_event_count": len(events),
        "actual_model_inference": False,
        "actual_provider_conformance_validated": False,
        "human_participants": False,
        "confirmatory_allowed": False,
        "manifest_completeness_authenticated": False,
        "raw_event_retention_required": True,
        "zero_attempt_sessions_supported": False,
        "final_detail_enrichment_supported": False,
        **_energy_boundary(),
    }
