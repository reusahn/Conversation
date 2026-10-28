"""Synthetic boundary checks for the declared v4 usage contract."""

import copy
import unittest

from usage_adapter_v4 import aggregate_usage


def manifest(*attempt_ids):
    return [{"attempt_id": aid, "session_id": "s1"} for aid in attempt_ids]


def final(aid="a1", eid="e1", prompt=10, completion=5, **extra):
    event = {
        "attempt_id": aid, "event_id": eid, "kind": "final",
        "response_id": "response-" + aid,
        "usage": {"prompt_tokens": prompt, "completion_tokens": completion,
                  "total_tokens": prompt + completion},
    }
    event.update(extra)
    return event


class UsageContractTests(unittest.TestCase):
    def test_nested_subsets_are_not_added_again(self):
        event = final()
        event["usage"]["prompt_tokens_details"] = {"cached_tokens": 8}
        event["usage"]["completion_tokens_details"] = {"reasoning_tokens": 4}
        out = aggregate_usage(manifest("a1"), [event])
        row = out["sessions"][0]
        self.assertEqual(row["reported_tokens"], 15)
        self.assertEqual((row["cached_tokens"], row["reasoning_tokens"]), (8, 4))
        self.assertIsNone(row["energy_valid"])
        self.assertFalse(row["energy_measurement_performed"])
        self.assertNotIn("energy_j", row)
        self.assertFalse(out["actual_provider_conformance_validated"])
        self.assertFalse(out["confirmatory_allowed"])

    def test_missing_details_preserve_total_but_are_not_zero(self):
        row = aggregate_usage(manifest("a1"), [final()])["sessions"][0]
        self.assertTrue(row["token_complete"])
        self.assertEqual(row["reported_tokens"], 15)
        self.assertIsNone(row["cached_tokens"])
        self.assertIsNone(row["reasoning_tokens"])

    def test_valid_zero_is_not_missing_usage(self):
        zero = aggregate_usage(manifest("a1"), [final(prompt=0, completion=0)])["attempts"][0]
        absent = aggregate_usage(manifest("a1"), [final(usage=None)])["attempts"][0]
        self.assertEqual((zero["status"], zero["reported_tokens"]), ("complete", 0))
        self.assertEqual((absent["status"], absent["reported_tokens"]), ("missing", None))
        self.assertIsNone(zero["energy_valid"])

    def test_invalid_numeric_and_subset_counts(self):
        for field in ("prompt_tokens", "completion_tokens", "total_tokens"):
            for value in (True, False, -1, 1.5, float("nan"), float("inf"), "10"):
                with self.subTest(field=field, value=value):
                    event = final()
                    event["usage"][field] = value
                    row = aggregate_usage(manifest("a1"), [event])["attempts"][0]
                    self.assertEqual(row["status"], "malformed")
                    self.assertIsNone(row["reported_tokens"])
        for details, key, invalid in (
            ("prompt_tokens_details", "cached_tokens", 11),
            ("completion_tokens_details", "reasoning_tokens", 6),
            ("completion_tokens_details", "reasoning_tokens", True),
        ):
            event = final()
            event["usage"][details] = {key: invalid}
            self.assertEqual(aggregate_usage(manifest("a1"), [event])["attempts"][0]["status"], "malformed")

    def test_total_mismatch_and_missing_required_are_distinct(self):
        bad, missing = final(), final()
        bad["usage"]["total_tokens"] = 999
        del missing["usage"]["completion_tokens"]
        self.assertEqual(aggregate_usage(manifest("a1"), [bad])["attempts"][0]["status"], "malformed")
        self.assertEqual(aggregate_usage(manifest("a1"), [missing])["attempts"][0]["status"], "missing")

    def test_stream_chunks_never_substitute_or_add_to_final(self):
        chunk = final(eid="chunk", kind="chunk")
        only = aggregate_usage(manifest("a1"), [chunk])["sessions"][0]
        self.assertFalse(only["token_complete"])
        self.assertIsNone(only["reported_tokens"])
        for order in ([chunk, final()], [final(), chunk]):
            self.assertEqual(aggregate_usage(manifest("a1"), order)["sessions"][0]["reported_tokens"], 15)

    def test_exact_retransmission_and_equivalent_final_snapshots(self):
        event = final()
        same = final(eid="e2")
        out = aggregate_usage(manifest("a1"), [event, copy.deepcopy(event), same])
        self.assertEqual(out["duplicate_event_count"], 1)
        self.assertEqual(out["sessions"][0]["reported_tokens"], 15)
        self.assertEqual(out["attempts"][0]["source_event_ids"], ["e1", "e2"])

    def test_conflicting_event_id_invalidates_both_attempts(self):
        one, two = final(), final(aid="a2")
        out = aggregate_usage(manifest("a1", "a2"), [one, two])
        self.assertTrue(all(row["status"] == "conflict" for row in out["attempts"]))
        self.assertIsNone(out["sessions"][0]["reported_tokens"])
        # An invalid payload with a colliding ID must not rescue the original.
        two["usage"]["total_tokens"] = float("nan")
        out = aggregate_usage(manifest("a1", "a2"), [one, two])
        self.assertTrue(all(row["status"] == "conflict" for row in out["attempts"]))

    def test_conflicting_final_or_later_detail_enrichment_is_unknown(self):
        first, second = final(), final(eid="e2", completion=6)
        for value in (second, final(eid="e2")):
            if value["usage"]["completion_tokens"] == 5:
                value["usage"]["completion_tokens_details"] = {"reasoning_tokens": 2}
            for events in ([first, value], [value, first]):
                row = aggregate_usage(manifest("a1"), events)["attempts"][0]
                self.assertEqual(row["status"], "conflict")
                self.assertIsNone(row["reported_tokens"])

    def test_actual_retries_sum_and_missing_retry_is_unknown(self):
        events = [final(), final(aid="a2", eid="e2", prompt=20, completion=10)]
        self.assertEqual(aggregate_usage(manifest("a1", "a2"), events)["sessions"][0]["reported_tokens"], 45)
        missing = aggregate_usage(manifest("a1", "a2"), events[:1])["sessions"][0]
        self.assertIsNone(missing["reported_tokens"])
        self.assertEqual(missing["unknown_attempt_ids"], ["a2"])
        # A late final belongs to the original attempt, independent of event order.
        self.assertEqual(aggregate_usage(manifest("a1", "a2"), list(reversed(events)))["sessions"][0]["reported_tokens"], 45)

    def test_response_identity_conflicts_within_and_across_attempts(self):
        same_attempt = [final(), final(eid="e2", response_id="other")]
        cross_attempt = [final(), final(aid="a2", eid="e2", response_id="response-a1")]
        self.assertEqual(aggregate_usage(manifest("a1"), same_attempt)["attempts"][0]["status"], "conflict")
        out = aggregate_usage(manifest("a1", "a2"), cross_attempt)
        self.assertTrue(all(row["status"] == "conflict" for row in out["attempts"]))

    def test_identity_errors_fail_closed(self):
        invalid_cases = [
            (manifest("a1", "a1"), []),
            (manifest("a1"), [final(aid="outside")]),
            (manifest("a1"), [final(session_id="outside")]),
            (manifest("a1"), [final(kind="canceled")]),
            (manifest("a1"), [final(response_id="")]),
            ([{"attempt_id": "a1", "session_id": ""}], []),
        ]
        for declared, events in invalid_cases:
            with self.subTest(declared=declared, events=events):
                with self.assertRaises(ValueError):
                    aggregate_usage(declared, events)

    def test_session_boundary_and_manifest_missingness_are_preserved(self):
        declared = manifest("a1", "a2")
        declared[1]["session_id"] = "s2"
        out = aggregate_usage(declared, [final()])
        self.assertEqual(len(out["sessions"]), 2)
        self.assertEqual(out["sessions"][0]["reported_tokens"], 15)
        self.assertIsNone(out["sessions"][1]["reported_tokens"])
        self.assertFalse(out["sessions"][0]["manifest_completeness_authenticated"])
        empty = aggregate_usage([], [])
        self.assertEqual(empty["sessions"], [])
        self.assertFalse(empty["zero_attempt_sessions_supported"])

    def test_input_objects_are_not_mutated(self):
        declared, events = manifest("a1"), [final()]
        before = copy.deepcopy((declared, events))
        aggregate_usage(declared, events)
        self.assertEqual((declared, events), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
