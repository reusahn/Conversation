"""Development-only v4 analysis; no quality noninferiority gate.

Inputs are caller-supplied session totals, NOT authenticated model/meter data.
See research/v4-analysis-contract.md. This module does not freeze a human study,
choose its sample size, or validate distributional assumptions. SciPy 1.17.0.
"""

from __future__ import annotations

import math
import statistics
from collections import Counter

from scipy import stats


ARMS = ("Eco", "Low", "Fast")
ENDPOINTS = ("reported_tokens", "energy_j")
DEFINITION_KEYS = {
    "reported_tokens": "token_definition_id",
    "energy_j": "energy_scope_id",
}
OUTCOMES = ("success", "failure", "unknown")


def _identifier(value, label):
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError(f"{label} must be a nonempty, unpadded string")
    return value


def _value(value, endpoint):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{endpoint} must be a finite nonnegative number or null")
    if endpoint == "reported_tokens" and not isinstance(value, int):
        raise ValueError("reported_tokens must be an integer or null")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite or value < 0:
        raise ValueError(f"{endpoint} must be finite and nonnegative")
    return value


def _normalize(manifest, rows):
    if not isinstance(manifest, list) or not manifest:
        raise ValueError("manifest must be a nonempty list")
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    assigned = {}
    common_tasks = None
    for entry in manifest:
        if not isinstance(entry, dict):
            raise ValueError("each manifest entry must be a mapping")
        pid = _identifier(entry.get("participant_id"), "participant_id")
        if pid in assigned:
            raise ValueError(f"duplicate manifest participant: {pid}")
        if entry.get("arm") not in ARMS:
            raise ValueError(f"invalid arm for {pid}")
        tasks = entry.get("task_ids")
        if not isinstance(tasks, list) or not tasks:
            raise ValueError("task_ids must be a nonempty list")
        tasks = [_identifier(t, "task_id") for t in tasks]
        if len(set(tasks)) != len(tasks):
            raise ValueError("duplicate task_id within participant")
        task_set = frozenset(tasks)
        if common_tasks is None:
            common_tasks = task_set
        if task_set != common_tasks:
            raise ValueError("development contract requires the same task set for all")
        assigned[pid] = {"participant_id": pid, "arm": entry["arm"], "task_ids": sorted(tasks)}
    if not {"Eco", "Low"}.issubset({a["arm"] for a in assigned.values()}):
        raise ValueError("Eco and Low must both occur in the assignment manifest")

    indexed = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each row must be a mapping")
        pid = _identifier(row.get("participant_id"), "participant_id")
        if pid not in assigned or pid in indexed:
            raise ValueError(f"unknown or duplicate data participant: {pid}")
        if "arm" in row and row["arm"] != assigned[pid]["arm"]:
            raise ValueError("data arm conflicts with original assignment")
        outcome_map = row.get("outcomes", {})
        if not isinstance(outcome_map, dict) or not set(outcome_map).issubset(common_tasks):
            raise ValueError("outcomes must map only assigned task IDs")
        if any(outcome not in OUTCOMES for outcome in outcome_map.values()):
            raise ValueError("outcome must be success, failure, or unknown")
        normalized = dict(assigned[pid])
        for endpoint in ENDPOINTS:
            normalized[endpoint] = _value(row.get(endpoint), endpoint)
            key = DEFINITION_KEYS[endpoint]
            definition = row.get(key)
            normalized[key] = None if definition is None else _identifier(definition, key)
        normalized["outcomes"] = {t: outcome_map.get(t, "unknown") for t in sorted(common_tasks)}
        indexed[pid] = normalized

    missing = sorted(set(assigned) - set(indexed))
    for pid in missing:
        indexed[pid] = {
            **assigned[pid],
            "reported_tokens": None,
            "energy_j": None,
            "token_definition_id": None,
            "energy_scope_id": None,
            "outcomes": {t: "unknown" for t in sorted(common_tasks)},
        }
    return [indexed[pid] for pid in sorted(indexed)], sorted(common_tasks), missing


def _arm_summary(rows, endpoint):
    values = [r[endpoint] for r in rows if r[endpoint] is not None]
    key = DEFINITION_KEYS[endpoint]
    total = sum(values) if endpoint == "reported_tokens" else math.fsum(values)
    mean = statistics.fmean(values) if values else None
    if mean is not None and (not math.isfinite(mean) or not math.isfinite(total)):
        raise ValueError("numeric overflow in endpoint summary")
    return {
        "n_assigned": len(rows),
        "n_observed": len(values),
        "n_unknown": len(rows) - len(values),
        "observed_total": total if values else None,
        "observed_mean": mean,
        "mean_scope": "all_assigned" if values and len(values) == len(rows) else "observed_only",
        "definition_ids": sorted({r[key] for r in rows if r[key] is not None}),
    }


def _inference(rows, endpoint):
    primary = [r for r in rows if r["arm"] in ("Eco", "Low")]
    key = DEFINITION_KEYS[endpoint]
    result = {
        "computable": False,
        "unavailable_reasons": [],
        "estimate": None,
        "standard_error": None,
        "df": None,
        "p_value_two_sided": None,
        "ci95_marginal": None,
        "ci_scope": "unadjusted_marginal_95_percent_not_familywise",
        "p_value_holm_two_endpoints": None,
        "reject_holm_005": None,
    }
    if any(r[endpoint] is None for r in primary):
        result["unavailable_reasons"].append("missing_primary_endpoint_value")
    if any(r[endpoint] is not None and r[key] is None for r in primary):
        result["unavailable_reasons"].append("missing_declared_metric_definition")
    if len({r[key] for r in primary if r[endpoint] is not None and r[key] is not None}) > 1:
        result["unavailable_reasons"].append("inconsistent_declared_metric_definition")
    if result["unavailable_reasons"]:
        return result
    x = [r[endpoint] for r in primary if r["arm"] == "Eco"]
    y = [r[endpoint] for r in primary if r["arm"] == "Low"]
    result["estimate"] = statistics.fmean(x) - statistics.fmean(y)
    if min(len(x), len(y)) < 2:
        result["unavailable_reasons"].append("fewer_than_two_participants_in_a_primary_arm")
        return result
    vx = statistics.variance(x)
    vy = statistics.variance(y)
    se2 = vx / len(x) + vy / len(y)
    if not math.isfinite(se2) or se2 <= 0:
        result["unavailable_reasons"].append("nonpositive_or_nonfinite_standard_error")
        return result
    test = stats.ttest_ind(x, y, equal_var=False, alternative="two-sided", nan_policy="raise")
    interval = test.confidence_interval(confidence_level=0.95)
    numbers = [test.pvalue, test.df, interval.low, interval.high]
    if not all(math.isfinite(v) for v in numbers):
        result["unavailable_reasons"].append("nonfinite_statistic")
        return result
    result.update({
        "computable": True,
        "standard_error": math.sqrt(se2),
        "df": float(test.df),
        "p_value_two_sided": float(test.pvalue),
        "ci95_marginal": [float(interval.low), float(interval.high)],
    })
    return result


def holm_two(pvalues):
    """Fixed two-hypothesis family; None reserves an untested slot at 1 internally.

    Untested outputs remain None. The internal placeholder is never an observed
    p-value, an imputed measurement, or evidence for a null effect.
    """
    if len(pvalues) != 2:
        raise ValueError("v4 development family has exactly two hypotheses")
    for p in pvalues:
        if p is not None and (isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p) or not 0 <= p <= 1):
            raise ValueError("p-value must be finite in [0,1] or None")
    internal = [1.0 if p is None else p for p in pvalues]
    order = sorted(range(2), key=lambda i: (internal[i], i))
    adjusted = [None, None]
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (2 - rank) * internal[index]))
        if pvalues[index] is not None:
            adjusted[index] = running
    return adjusted


def analyze(manifest, rows):
    """Return descriptive outcomes and development calculations for Eco minus Low.

    Rows: participant_id, reported_tokens, energy_j, outcomes, token_definition_id,
    energy_scope_id. Missing rows/values/outcomes become unknown. Bad identities,
    values or outcomes raise ValueError. Opaque definition IDs are declarations,
    not real measurement certification. Fast summaries never gate Eco–Low.
    """
    normalized, task_ids, missing_rows = _normalize(manifest, rows)
    endpoints = {}
    try:
        for endpoint in ENDPOINTS:
            endpoints[endpoint] = {
                "unit": "provider_reported_tokens" if endpoint == "reported_tokens" else "J",
                "arms": {
                    arm: _arm_summary([r for r in normalized if r["arm"] == arm], endpoint)
                    for arm in ARMS
                },
                "inference": _inference(normalized, endpoint),
            }
    except (OverflowError, FloatingPointError) as exc:
        raise ValueError("numeric overflow; no finite analysis produced") from exc
    pvalues = [endpoints[e]["inference"]["p_value_two_sided"] for e in ENDPOINTS]
    adjusted = holm_two(pvalues)
    for endpoint, p in zip(ENDPOINTS, adjusted):
        endpoints[endpoint]["inference"]["p_value_holm_two_endpoints"] = p
        endpoints[endpoint]["inference"]["reject_holm_005"] = p <= 0.05 if p is not None else None
    quality = {}
    for arm in ARMS:
        assigned_rows = [r for r in normalized if r["arm"] == arm]
        counts = Counter(o for r in assigned_rows for o in r["outcomes"].values())
        n_tasks = len(assigned_rows) * len(task_ids)
        quality[arm] = {
            "n_assigned_participants": len(assigned_rows),
            "n_assigned_tasks": n_tasks,
            **{f"{o}_count": counts[o] for o in OUTCOMES},
            "success_rate_bounds": [counts["success"] / n_tasks, (counts["success"] + counts["unknown"]) / n_tasks] if n_tasks else None,
            "failure_rate_bounds": [counts["failure"] / n_tasks, (counts["failure"] + counts["unknown"]) / n_tasks] if n_tasks else None,
            "bounds_type": "missing_outcome_identification_bounds_not_confidence_intervals",
        }
    return {
        "schema_version": "v4-development-1",
        "primary_contrast": ["Eco", "Low"],
        "effect_direction": "Eco_minus_Low",
        "n_manifest_participants": len(normalized),
        "task_ids": task_ids,
        "missing_row_participant_ids": missing_rows,
        "endpoints": endpoints,
        "quality": quality,
        "multiple_testing": {
            "method": "Holm",
            "alpha": 0.05,
            "family_size": 2,
            "endpoint_order": list(ENDPOINTS),
            "internal_p_inputs": [1.0 if p is None else p for p in pvalues],
            "untested_placeholder_rule": "1 internally only; observed p and adjusted p stay null",
        },
        "quality_is_resource_inference_gate": False,
        "confirmatory_allowed": False,
        "statistical_assumptions_verified": False,
        "actual_model_inference_performed_by_tool": False,
        "device_energy_measurement_performed_by_tool": False,
        "human_experiment_performed_by_tool": False,
        "provenance_verified": False,
        "input_evidence_kind": "caller_supplied_unverified",
        "limits": [
            "Calculability is not proof of study validity, randomization, sample adequacy, or causal identification.",
            "Metric ID agreement checks declarations, not the complete backend manifest or real sensors.",
            "Marginal 95% intervals are unadjusted; Holm-adjusted p-values cover the fixed two-test family only.",
            "Quality outcomes do not gate resource outcomes; no quality noninferiority or environmental certification is implemented.",
            "Tokens are not converted to energy, carbon, water, or avoided ecological harm.",
        ],
    }
