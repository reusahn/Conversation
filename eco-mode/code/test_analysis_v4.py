"""Synthetic boundary/contract tests. No LLM, meter, or human experiment."""

import copy
import hashlib
import io
import json
import math
from pathlib import Path
import platform
import statistics
import sys
import unittest

import scipy
from scipy.stats import t

from analysis_v4 import analyze, holm_two


def fixture():
    manifest, rows = [], []
    tokens = {"Eco": [84, 100, 116], "Low": [140, 168, 196], "Fast": [170]}
    energy = {"Eco": [20, 24, 28], "Low": [30, 38, 46], "Fast": [35]}
    for arm in tokens:
        for i, value in enumerate(tokens[arm]):
            pid = f"{arm}-{i}"
            manifest.append({"participant_id": pid, "arm": arm, "task_ids": ["t1", "t2"]})
            rows.append({
                "participant_id": pid,
                "reported_tokens": value,
                "energy_j": energy[arm][i],
                "outcomes": {"t1": "success", "t2": "success"},
                "token_definition_id": "synthetic-declaration-tokens-v1",
                "energy_scope_id": "synthetic-declaration-J-v1",
            })
    return manifest, rows


class AnalysisV4Tests(unittest.TestCase):
    def test_welch_matches_manual_formulas(self):
        m, r = fixture()
        answer = analyze(m, r)["endpoints"]["reported_tokens"]["inference"]
        x, y = [84, 100, 116], [140, 168, 196]
        ax, ay = statistics.variance(x) / len(x), statistics.variance(y) / len(y)
        se = math.sqrt(ax + ay)
        df = (ax + ay) ** 2 / (ax**2 / (len(x)-1) + ay**2 / (len(y)-1))
        effect = statistics.mean(x) - statistics.mean(y)
        expected_p = 2 * t.sf(abs(effect / se), df)
        margin = t.ppf(.975, df) * se
        self.assertTrue(answer["computable"])
        for key, expected in [("estimate", effect), ("standard_error", se), ("df", df), ("p_value_two_sided", expected_p)]:
            self.assertAlmostEqual(answer[key], expected, places=12)
        self.assertAlmostEqual(answer["ci95_marginal"][0], effect - margin, places=12)
        self.assertAlmostEqual(answer["ci95_marginal"][1], effect + margin, places=12)
        self.assertIn("not_familywise", answer["ci_scope"])

    def test_performance_loss_or_unknown_never_gates_resources(self):
        m, r = fixture()
        baseline = analyze(m, r)
        for outcome in ("failure", "unknown"):
            altered = copy.deepcopy(r)
            for row in altered:
                if row["participant_id"].startswith("Eco"):
                    row["outcomes"] = {"t1": outcome, "t2": outcome}
            result = analyze(m, altered)
            self.assertEqual(baseline["endpoints"], result["endpoints"])
            self.assertEqual(result["quality"]["Eco"][f"{outcome}_count"], 6)
            self.assertFalse(result["quality_is_resource_inference_gate"])

    def test_endpoint_missing_independence_and_family_retained(self):
        m, r = fixture()
        base = analyze(m, r)
        for absent, kept in (("energy_j", "reported_tokens"), ("reported_tokens", "energy_j")):
            changed = copy.deepcopy(r)
            changed[0][absent] = None
            result = analyze(m, changed)
            self.assertFalse(result["endpoints"][absent]["inference"]["computable"])
            self.assertIsNone(result["endpoints"][absent]["inference"]["estimate"])
            valid = result["endpoints"][kept]["inference"]
            self.assertEqual(valid["p_value_two_sided"], base["endpoints"][kept]["inference"]["p_value_two_sided"])
            self.assertAlmostEqual(valid["p_value_holm_two_endpoints"], min(1, 2*valid["p_value_two_sided"]))
            self.assertIsNone(result["endpoints"][absent]["inference"]["p_value_two_sided"])
            self.assertEqual(result["multiple_testing"]["family_size"], 2)

    def test_missing_assigned_row_stays_in_denominator(self):
        m, r = fixture()
        result = analyze(m, r[1:])
        self.assertEqual(result["missing_row_participant_ids"], ["Eco-0"])
        self.assertEqual(result["quality"]["Eco"]["n_assigned_tasks"], 6)
        self.assertEqual(result["quality"]["Eco"]["unknown_count"], 2)
        self.assertEqual(result["quality"]["Eco"]["success_rate_bounds"], [4/6, 1])
        self.assertEqual(result["quality"]["Eco"]["failure_rate_bounds"], [0, 2/6])
        self.assertEqual(result["endpoints"]["energy_j"]["arms"]["Eco"]["n_assigned"], 3)
        self.assertFalse(result["endpoints"]["energy_j"]["inference"]["computable"])

    def test_fast_missing_does_not_gate_primary_comparison(self):
        m, r = fixture()
        base = analyze(m, r)
        changed = analyze(m, r[:-1])
        for endpoint in ("reported_tokens", "energy_j"):
            self.assertEqual(base["endpoints"][endpoint]["inference"], changed["endpoints"][endpoint]["inference"])
        self.assertEqual(changed["quality"]["Fast"]["unknown_count"], 2)

    def test_bad_identities_and_assignment_are_rejected(self):
        m, r = fixture()
        with self.assertRaises(ValueError):
            analyze(m + [m[0]], r)
        with self.assertRaises(ValueError):
            analyze(m, r + [r[0]])
        for bad_row in ({**r[0], "participant_id": "unassigned"}, {**r[0], "arm": "Low"}):
            with self.assertRaises(ValueError):
                analyze(m, [bad_row] + r[1:])

    def test_task_denominator_and_outcomes_are_validated(self):
        m, r = fixture()
        for bad_tasks in (["t1"], ["t1", "t1"], []):
            with self.assertRaises(ValueError):
                analyze([{**m[0], "task_ids": bad_tasks}] + m[1:], r)
        for bad_outcome in ({"unassigned_task": "success"}, {"t1": "pending"}):
            with self.assertRaises(ValueError):
                analyze(m, [{**r[0], "outcomes": bad_outcome}] + r[1:])

    def test_invalid_values_rejected_not_silently_imputed(self):
        m, r = fixture()
        for endpoint, values in (("reported_tokens", [True, 1.5, -1, float("nan"), float("inf")]), ("energy_j", [False, -1, "1", float("nan"), float("inf")])):
            for value in values:
                with self.subTest(endpoint=endpoint, value=repr(value)), self.assertRaises(ValueError):
                    analyze(m, [{**r[0], endpoint: value}] + r[1:])

    def test_metric_definition_is_endpoint_specific_and_unverified(self):
        m, r = fixture()
        for key, endpoint, kept in (("token_definition_id", "reported_tokens", "energy_j"), ("energy_scope_id", "energy_j", "reported_tokens")):
            for value in (None, "other-declared-definition"):
                result = analyze(m, [{**r[0], key: value}] + r[1:])
                self.assertFalse(result["endpoints"][endpoint]["inference"]["computable"])
                self.assertTrue(result["endpoints"][kept]["inference"]["computable"])
                self.assertFalse(result["provenance_verified"])

    def test_constant_samples_never_become_spurious_certainty(self):
        m, r = fixture()
        for row in r:
            row["reported_tokens"] = 100 if row["participant_id"].startswith("Eco") else 200
        result = analyze(m, r)["endpoints"]["reported_tokens"]["inference"]
        self.assertEqual(result["estimate"], -100)
        self.assertFalse(result["computable"])
        self.assertIsNone(result["p_value_two_sided"])
        r[3]["reported_tokens"] = 201
        self.assertTrue(analyze(m, r)["endpoints"]["reported_tokens"]["inference"]["computable"])

    def test_small_sample_has_description_without_inference(self):
        m, r = fixture()
        subset = [0, 3]
        result = analyze([m[i] for i in subset], [r[i] for i in subset])
        self.assertEqual(result["endpoints"]["reported_tokens"]["inference"]["estimate"], -56)
        self.assertFalse(result["endpoints"]["reported_tokens"]["inference"]["computable"])

    def test_holm_fixed_family_and_no_imputed_observed_p(self):
        cases = [([.03, .04], [.06, .06]), ([.001, .1], [.002, .1]), ([.01, None], [.02, None]), ([None, .8], [None, 1.0]), ([.05, .01], [.05, .02]), ([None, None], [None, None])]
        for inputs, expected in cases:
            self.assertEqual(holm_two(inputs), expected)
        for bad in ([.2], [True, .2], [-1, .1], [float("nan"), .1]):
            with self.assertRaises(ValueError):
                holm_two(bad)

    def test_flags_and_inputs_are_preserved(self):
        m, r = fixture()
        before = copy.deepcopy((m, r))
        result = analyze(m, r)
        self.assertEqual((m, r), before)
        for flag in ("confirmatory_allowed", "statistical_assumptions_verified", "actual_model_inference_performed_by_tool", "device_energy_measurement_performed_by_tool", "human_experiment_performed_by_tool", "provenance_verified"):
            self.assertFalse(result[flag])
        json.dumps(result, allow_nan=False)


if __name__ == "__main__":
    stream = io.StringIO()
    run = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(AnalysisV4Tests))
    root = Path(__file__).resolve().parent
    receipt = {
        "evidence_type": "synthetic_development_unit_tests",
        "test_methods_run": run.testsRun,
        "failures": len(run.failures), "errors": len(run.errors), "passed": run.wasSuccessful(),
        "python_version": platform.python_version(), "scipy_version": scipy.__version__,
        "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (root / "analysis_v4.py", Path(__file__).resolve())},
        "actual_model_inference": False, "device_energy_measurement": False,
        "human_participants": False, "confirmatory_allowed": False,
        "output": stream.getvalue(),
    }
    (root / "results").mkdir(exist_ok=True)
    (root / "results" / "v4-analysis-check.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(stream.getvalue(), end="")
    sys.exit(0 if run.wasSuccessful() else 1)
