"""C-role independent synthetic contract checks; not real model/energy evidence.

Run from this directory: python adversarial_v4.py
This checker owns its fixtures and numerical oracle. It does not import the
implementation's private helpers or reuse the implementation's test fixtures.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path
import statistics
import traceback

from scipy import stats

from analysis_v4 import analyze


HERE = Path(__file__).resolve().parent
CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-11, abs_tol=1e-12), (actual, expected)


def fixture():
    manifest, rows = [], []
    values = {
        "Eco": ([10, 20, 30], [100.0, 140.0, 180.0]),
        "Low": ([40, 50, 60], [210.0, 300.0, 390.0]),
        "Fast": ([999], [9999.0]),
    }
    for arm, (tokens, energy) in values.items():
        for i, (token, joules) in enumerate(zip(tokens, energy), 1):
            pid = f"{arm}-{i}"
            manifest.append({"participant_id": pid, "arm": arm, "task_ids": ["t1", "t2"]})
            rows.append({
                "participant_id": pid,
                "reported_tokens": token,
                "energy_j": joules,
                "token_definition_id": "synthetic-declared-token-v1",
                "energy_scope_id": "synthetic-declared-joule-v1",
                "outcomes": {"t1": "success", "t2": "success"},
            })
    return manifest, rows


def inference(result, endpoint):
    return result["endpoints"][endpoint]["inference"]


def must_reject(fn):
    try:
        fn()
    except (ValueError, TypeError):
        return
    raise AssertionError("invalid identity/value was not rejected")


@check
def independent_welch_and_holm_oracle():
    manifest, rows = fixture()
    result = analyze(manifest, rows)
    raw_p = {}
    for endpoint in ("reported_tokens", "energy_j"):
        x = [r[endpoint] for r in rows if r["participant_id"].startswith("Eco-")]
        y = [r[endpoint] for r in rows if r["participant_id"].startswith("Low-")]
        v_x = statistics.variance(x) / len(x)
        v_y = statistics.variance(y) / len(y)
        expected_se = math.sqrt(v_x + v_y)
        expected_df = (v_x + v_y) ** 2 / (v_x ** 2 / (len(x)-1) + v_y ** 2 / (len(y)-1))
        expected_difference = statistics.mean(x) - statistics.mean(y)
        expected_p = float(stats.ttest_ind(x, y, equal_var=False).pvalue)
        raw_p[endpoint] = expected_p
        inf = inference(result, endpoint)
        assert inf["computable"] is True
        close(inf["estimate"], expected_difference)
        close(inf["standard_error"], expected_se)
        close(inf["df"], expected_df)
        close(inf["p_value_two_sided"], expected_p)
        half_width = float(stats.t.ppf(0.975, expected_df)) * expected_se
        close(inf["ci95_marginal"][0], expected_difference-half_width)
        close(inf["ci95_marginal"][1], expected_difference+half_width)
    ordered = sorted(raw_p, key=raw_p.get)
    first = min(1.0, 2 * raw_p[ordered[0]])
    second = min(1.0, max(first, raw_p[ordered[1]]))
    close(inference(result, ordered[0])["p_value_holm_two_endpoints"], first)
    close(inference(result, ordered[1])["p_value_holm_two_endpoints"], second)


@check
def severe_performance_loss_does_not_gate_resources():
    manifest, rows = fixture()
    baseline = analyze(manifest, rows)
    for row in rows:
        if row["participant_id"].startswith("Eco-"):
            row["outcomes"] = {"t1": "failure", "t2": "failure"}
    changed = analyze(manifest, rows)
    assert changed["endpoints"] == baseline["endpoints"]
    assert changed["quality"] != baseline["quality"]


@check
def unknown_performance_does_not_gate_resources():
    manifest, rows = fixture()
    baseline = analyze(manifest, rows)
    for row in rows:
        row["outcomes"] = {}
    changed = analyze(manifest, rows)
    assert changed["endpoints"] == baseline["endpoints"]
    assert changed["quality"] != baseline["quality"]


@check
def missing_energy_does_not_gate_tokens_or_shrink_holm_family():
    manifest, rows = fixture()
    baseline = analyze(manifest, rows)
    rows[0]["energy_j"] = None
    changed = analyze(manifest, rows)
    token = inference(changed, "reported_tokens")
    energy = inference(changed, "energy_j")
    assert token["computable"] is True
    assert energy["computable"] is False
    assert energy["p_value_two_sided"] is None
    assert energy["estimate"] is None
    close(token["p_value_two_sided"], inference(baseline, "reported_tokens")["p_value_two_sided"])
    close(token["p_value_holm_two_endpoints"], min(1.0, 2*token["p_value_two_sided"]))


@check
def missing_tokens_does_not_gate_energy():
    manifest, rows = fixture()
    baseline = analyze(manifest, rows)
    rows[0]["reported_tokens"] = None
    changed = analyze(manifest, rows)
    token = inference(changed, "reported_tokens")
    energy = inference(changed, "energy_j")
    assert token["computable"] is False
    assert token["p_value_two_sided"] is None
    assert energy["computable"] is True
    close(energy["p_value_two_sided"], inference(baseline, "energy_j")["p_value_two_sided"])
    close(energy["p_value_holm_two_endpoints"], min(1.0, 2*energy["p_value_two_sided"]))


@check
def fast_missing_row_does_not_gate_primary_contrast():
    manifest, rows = fixture()
    baseline = analyze(manifest, rows)
    changed = analyze(manifest, [r for r in rows if not r["participant_id"].startswith("Fast-")])
    for endpoint in ("reported_tokens", "energy_j"):
        assert inference(changed, endpoint) == inference(baseline, endpoint)


@check
def missing_assigned_row_is_not_complete_case_analysis():
    manifest, rows = fixture()
    changed = analyze(manifest, rows[1:])
    assert inference(changed, "reported_tokens")["computable"] is False
    assert inference(changed, "energy_j")["computable"] is False
    assert changed["quality"]["Eco"]["unknown_count"] == 2
    assert changed["quality"]["Eco"]["success_count"] == 4


@check
def participant_identity_conflicts_are_rejected():
    manifest, rows = fixture()
    must_reject(lambda: analyze(manifest+[copy.deepcopy(manifest[0])], rows))
    must_reject(lambda: analyze(manifest, rows+[copy.deepcopy(rows[0])]))
    outsider = copy.deepcopy(rows[0])
    outsider["participant_id"] = "not-assigned"
    must_reject(lambda: analyze(manifest, rows+[outsider]))


@check
def invalid_resource_scalars_are_rejected():
    manifest, rows = fixture()
    for endpoint, values in {
        "reported_tokens": [True, -1, 1.5, float("nan"), float("inf")],
        "energy_j": [True, -1, float("nan"), float("inf")],
    }.items():
        for value in values:
            malformed = copy.deepcopy(rows)
            malformed[0][endpoint] = value
            must_reject(lambda: analyze(manifest, malformed))


@check
def endpoint_definition_unknown_or_conflict_blocks_only_its_endpoint():
    manifest, rows = fixture()
    for key, endpoint, other in [
        ("token_definition_id", "reported_tokens", "energy_j"),
        ("energy_scope_id", "energy_j", "reported_tokens"),
    ]:
        for value in (None, "different-declaration"):
            changed_rows = copy.deepcopy(rows)
            changed_rows[0][key] = value
            result = analyze(manifest, changed_rows)
            assert inference(result, endpoint)["computable"] is False
            assert inference(result, other)["computable"] is True


@check
def all_constant_resources_do_not_produce_fake_inference():
    manifest, rows = fixture()
    for row in rows:
        row["reported_tokens"] = 0
        row["energy_j"] = 0.0
    result = analyze(manifest, rows)
    for endpoint in ("reported_tokens", "energy_j"):
        inf = inference(result, endpoint)
        assert inf["computable"] is False
        assert inf["p_value_two_sided"] is None


@check
def one_constant_arm_is_allowed_when_standard_error_is_positive():
    manifest, rows = fixture()
    for row in rows:
        if row["participant_id"].startswith("Eco-"):
            row["reported_tokens"] = 0
    result = analyze(manifest, rows)
    assert inference(result, "reported_tokens")["computable"] is True
    assert inference(result, "reported_tokens")["standard_error"] > 0


@check
def too_few_independent_people_do_not_become_task_replicates():
    manifest, rows = fixture()
    keep = {"Eco-1", "Low-1", "Fast-1"}
    result = analyze([m for m in manifest if m["participant_id"] in keep],
                     [r for r in rows if r["participant_id"] in keep])
    for endpoint in ("reported_tokens", "energy_j"):
        assert inference(result, endpoint)["computable"] is False


@check
def mismatched_assigned_task_set_is_rejected():
    manifest, rows = fixture()
    manifest[0]["task_ids"] = ["t1", "different-task"]
    must_reject(lambda: analyze(manifest, rows))


def main():
    reports = []
    for fn in CHECKS:
        try:
            fn()
        except Exception as exc:
            reports.append({"name": fn.__name__, "passed": False,
                            "error": f"{type(exc).__name__}: {exc}",
                            "traceback": traceback.format_exc()})
        else:
            reports.append({"name": fn.__name__, "passed": True})
    files = ["analysis_v4.py", "usage_adapter_v4.py", "adversarial_v4.py"]
    result = {
        "schema_version": 1,
        "review_role": "fictional_C_separate_contract_audit_not_external_replication",
        "fixture_origin": "independently_authored_synthetic_values",
        "actual_model_inference": False,
        "device_energy_measurement": False,
        "human_participants": False,
        "provenance_verified": False,
        "confirmatory_allowed": False,
        "passed": sum(row["passed"] for row in reports),
        "total": len(reports),
        "all_passed": all(row["passed"] for row in reports),
        "files_sha256": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                         for name in files if (HERE/name).exists()},
        "checks": reports,
    }
    destination = HERE/"results"/"v4-independent-check.json"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("passed", "total", "all_passed")}, ensure_ascii=False))
    for report in reports:
        if not report["passed"]:
            print(report["name"], report["error"])
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
