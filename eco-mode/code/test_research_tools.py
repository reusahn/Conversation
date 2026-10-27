import copy
import math
import unittest
from scipy import stats
from session_replay import replay, canonical_hash, mode_hash, response_observation
from synthetic_fixture import fixture, no_call_fixture
from analysis_prepare import bounded_difference, welch_energy, analyse, participant_row, ALPHA

class ReplayInvariants(unittest.TestCase):
    def test_primary_total_not_sum_twice(self):
        r = replay(fixture())
        self.assertTrue(r["audit_passed"])
        self.assertEqual((r["synthetic_total_energy_j"],r["secondary_active_energy_j"],
                          r["secondary_residual_energy_j"]), (22,17,5))
        self.assertIsNone(r["measured_total_energy_j"])
        self.assertFalse(r["confirmatory_ready"])
    def test_cancel_includes_drain(self):
        r = replay(fixture())
        self.assertEqual(r["attempts"],2)
        self.assertEqual(r["synthetic_total_energy_j"],22)
        self.assertEqual(r["close_reason"],"abandoned")
    def test_first_committed_not_latest_mode(self):
        r = replay(fixture())
        self.assertEqual(r["first_choice"],"low")
        self.assertEqual((r["additional_requests"],r["mode_switches"]),(1,1))
    def test_no_call_still_idle(self):
        r = replay(no_call_fixture())
        self.assertTrue(r["audit_passed"])
        self.assertEqual((r["attempts"],r["first_choice"],r["synthetic_total_energy_j"]),(0,"none",3))
    def test_no_call_missing_final_sensor_not_zero(self):
        d = no_call_fixture(); del d["events"][-1]["counter"]
        r = replay(d)
        self.assertIsNone(r["synthetic_total_energy_j"])
        self.assertIn("missing_counter",r["issues"])
    def test_identical_duplicate_deduplicates(self):
        d = fixture(); d["events"].insert(4,copy.deepcopy(d["events"][3]))
        self.assertEqual(replay(d),replay(fixture()))
    def test_conflicting_duplicate_blocks(self):
        d = fixture(); e = copy.deepcopy(d["events"][3]); e["status"]="failure"; d["events"].append(e)
        r = replay(d)
        self.assertIn("conflicting_duplicate_event",r["issues"])
        self.assertIsNone(r["synthetic_total_energy_j"])
        self.assertEqual(r["first_choice"],"unknown")
    def test_sequence_loss_not_none_or_failure(self):
        d = fixture(); del d["events"][1]
        r = replay(d)
        self.assertEqual(r["first_choice"],"unknown")
        self.assertEqual(set(r["outcomes"].values()),{"unknown"})
    def test_epoch_reset_not_negative_saving(self):
        d = fixture(); d["events"][-1]["counter"]["epoch"]="reloaded"
        r = replay(d)
        self.assertIsNone(r["synthetic_total_energy_j"])
        self.assertIn("counter_identity_or_epoch_changed",r["issues"])
    def test_counter_decrease_blocks(self):
        d = fixture(); d["events"][3]["counter"]["value_raw"]=1
        self.assertIn("counter_decreased",replay(d)["issues"])
    def test_mixed_scope_blocks(self):
        d = fixture(); d["events"][-1]["counter"]["scope"]="server_input"
        self.assertIsNone(replay(d)["synthetic_total_energy_j"])
    def test_overlap_invalid(self):
        d = fixture()
        # Start a second attempt before ending the first, preserving a complete event sequence.
        second = copy.deepcopy(d["events"][5]); second["attempt_id"]="parallel"
        second["t_ns"]=7; second["request_id"]="r1"
        second["effective_config_hash"]=mode_hash(d["backend_config"],"low")
        second["counter"].update(value_raw=102000,read_start_ns=6,read_end_ns=7)
        second["event_id"]="parallel-start"
        d["events"].insert(3,second)
        for i,e in enumerate(d["events"],1): e["server_seq"]=i
        r = replay(d)
        self.assertIn("overlapping_attempts",r["issues"])
        self.assertIsNone(r["synthetic_total_energy_j"])
    def test_end_before_backend_stop_invalid(self):
        d = fixture(); del d["events"][-2]
        for i,e in enumerate(d["events"],1): e["server_seq"]=i
        self.assertIn("end_before_backend_drained",replay(d)["issues"])
    def test_new_request_after_close_blocks(self):
        d=fixture(); e=copy.deepcopy(d["events"][1]); e.update(event_id="late",request_id="late",t_ns=23)
        d["events"].insert(8,e)
        for i,x in enumerate(d["events"],1): x["server_seq"]=i
        self.assertIn("request_after_close",replay(d)["issues"])
    def test_bracket_does_not_prove_fresh_sensor(self):
        r=replay(fixture())
        self.assertFalse(r["timing_uncertainty_known"])
        self.assertFalse(r["sensor_evidence_independently_verified"])
    def test_integer_delta_before_conversion(self):
        d=fixture()
        for e in d["events"]:
            if "counter" in e:e["counter"]["value_raw"] += 2**60
        self.assertEqual(replay(d)["synthetic_total_energy_j"],22)
    def test_configuration_is_arm_invariant(self):
        d=fixture(); base=replay(d)
        for arm in ("Low","Fast","Eco"):
            c=copy.deepcopy(d); c["events"][0]["assigned_arm"]=arm
            self.assertEqual(replay(c)["synthetic_total_energy_j"],base["synthetic_total_energy_j"])
            self.assertEqual(canonical_hash(c["backend_config"]),canonical_hash(d["backend_config"]))
    def test_config_mutation_detected(self):
        d=fixture(); d["backend_config"]["common"]["temperature"]=0.7
        self.assertIn("backend_hash_mismatch",replay(d)["issues"])
    def test_mode_mutation_detected(self):
        d=fixture(); d["events"][2]["effective_config_hash"]="wrong"
        self.assertIn("mode_config_hash_mismatch",replay(d)["issues"])
    def test_schema_missing_not_zero_tokens(self):
        s={"version":"fixture-1","reasoning_field":"reasoning","reasoning_token_field":"count"}
        r=response_observation({"reasoning_content":"legacy","count":0},s)
        self.assertFalse(r["payload_schema_valid"]); self.assertIsNone(r["observed_reasoning_tokens"])
    def test_explicit_zero_tokens_is_not_missing(self):
        s={"version":"fixture-1","reasoning_field":"reasoning","reasoning_token_field":"count"}
        self.assertEqual(response_observation({"reasoning":"","count":0},s)["observed_reasoning_tokens"],0)
    def test_bool_counter_not_integer_measurement(self):
        d=fixture(); d["events"][0]["counter"]["value_raw"]=True
        self.assertIn("invalid_counter",replay(d)["issues"])
    def test_no_unsupported_provenance(self):
        d=fixture(); del d["measurement_kind"]
        with self.assertRaises(ValueError):replay(d)
    def test_omitted_outcome_unknown(self):
        d=fixture(); del d["events"][-1]["outcomes"]["T02"]
        self.assertEqual(replay(d)["outcomes"]["T02"],"unknown")
    def test_called_task_cannot_be_not_started(self):
        d=fixture(); d["events"][-1]["outcomes"]["T01"]="not_started"
        r=replay(d); self.assertFalse(r["audit_passed"])
        self.assertEqual(r["outcomes"]["T01"],"unknown")
    def test_mixed_attempt_scope_not_a_lower_bound(self):
        d=fixture()
        for i in (5,8): d["events"][i]["counter"]["scope"]="server_input"
        r=replay(d)
        self.assertIsNone(r["known_floor_j"])
        self.assertIsNone(r["secondary_active_energy_j"])
    def test_mixed_attempt_device_not_a_lower_bound(self):
        d=fixture()
        for i in (5,8): d["events"][i]["counter"]["device"]="another-device"
        self.assertIsNone(replay(d)["known_floor_j"])
    def test_submission_after_close_not_first_choice(self):
        d=no_call_fixture(); e=copy.deepcopy(fixture()["events"][1])
        e.update(event_id="late",request_id="late",t_ns=23)
        d["events"].insert(2,e)
        for i,x in enumerate(d["events"],1): x["server_seq"]=i
        self.assertEqual(replay(d)["first_choice"],"unknown")
    def test_foreign_session_does_not_produce_known_choice(self):
        d=fixture();d["events"][1]["session_id"]="foreign"
        r=replay(d)
        self.assertEqual(r["first_choice"],"unknown")
        self.assertEqual(set(r["outcomes"].values()),{"unknown"})
    def test_invalid_clock_schema_rejected_explicitly(self):
        for value in (None,"bad",True):
            d=fixture();d["events"][2]["t_ns"]=value
            with self.assertRaisesRegex(ValueError,"invalid event schema"):replay(d)
    def test_blank_session_id_rejected(self):
        d=fixture()
        for e in d["events"]:e["session_id"]=""
        with self.assertRaises(ValueError):replay(d)
    def test_same_intended_modes_rejected_despite_valid_hashes(self):
        d=fixture();d["backend_config"]["modes"]["high"]=copy.deepcopy(d["backend_config"]["modes"]["low"])
        d["events"][0]["backend_hash"]=canonical_hash(d["backend_config"])
        with self.assertRaisesRegex(ValueError,"low budget must be below"):replay(d)
    def test_mode_cannot_change_model(self):
        d=fixture();d["backend_config"]["modes"]["high"]["model"]="different"
        with self.assertRaises(ValueError):replay(d)
    def test_mode_hash_conflict_quarantines_axes_preserves_raw(self):
        d=fixture();d["events"][2]["effective_config_hash"]="other-backend"
        r=replay(d)
        self.assertEqual(r["first_choice"],"unknown")
        self.assertEqual(set(r["outcomes"].values()),{"unknown"})
        self.assertEqual(r["raw_first_submitted_mode"],"low")
        self.assertEqual(r["reported_outcomes"]["T01"],"success")
        self.assertFalse(r["protocol_observation_valid"])
    def test_backend_hash_conflict_quarantines_axes(self):
        d=fixture();d["events"][0]["backend_hash"]="different"
        self.assertEqual(replay(d)["first_choice"],"unknown")
    def test_label_in_server_config_quarantines_axes(self):
        d=fixture();d["backend_config"]["common"]["label"]="Eco"
        d["events"][0]["backend_hash"]=canonical_hash(d["backend_config"])
        self.assertEqual(replay(d)["first_choice"],"unknown")

class AnalysisInvariants(unittest.TestCase):
    def analyse(self, rows, strata, delta=None, manifest=None):
        if manifest is None:
            manifest = [{"participant_id":r["participant_id"],"assigned_arm":r["assigned_arm"],
                         "assigned_task_ids":list(r["assigned_task_ids"])} for r in self.dataset()]
        return analyse(rows,strata,delta,assignment_manifest=manifest)
    def test_all_success_not_automatic_noninferiority(self):
        r=bounded_difference([(0,0)]*10,[(0,0)]*10)
        self.assertGreater(r["confidence_upper"],0.05)
    def test_missing_opposite_worst_cases(self):
        r=bounded_difference([(0,1)],[(0,1)],two_sided=True)
        self.assertEqual((r["identification_lower"],r["identification_upper"]),(-1,1))
    def test_bounded_formula_hand_calculation(self):
        r=bounded_difference([(0,0)]*100,[(0,0)]*100,alpha=0.01)
        self.assertAlmostEqual(r["radius"],math.sqrt(math.log(100)/100))
    def test_welch_matches_independent_scipy_api(self):
        a,b=[1,2,3,4,8],[8,9,13,15,18,20]
        r=welch_energy(a,b)
        reference=stats.ttest_ind(a,b,equal_var=False,alternative="less")
        self.assertAlmostEqual(r["p_less"],reference.pvalue)
        self.assertAlmostEqual(r["upper_j"],reference.confidence_interval(1-ALPHA).high)
    def test_missing_energy_no_complete_case_pass(self):
        self.assertEqual(welch_energy([1,None],[4,5])["status"],"blocked_missing_energy")
    def test_constant_energy_not_certain(self):
        self.assertIsNone(welch_energy([1,1],[10,10])["upper_j"])
    def test_assigned_task_fixed_denominator(self):
        r=replay(fixture()); p=participant_row(r,{"overall":["T01","T02"]})
        self.assertEqual(p["failure_intervals"]["overall"],(0.5,0.5))
    def test_missing_quality_is_interval(self):
        r=replay(fixture()); r["outcomes"]["T02"]="unknown"
        self.assertEqual(participant_row(r,{"overall":["T01","T02"]})["failure_intervals"]["overall"],(0,0.5))
    def test_first_choice_unknown_not_none(self):
        r=replay(fixture()); r["first_choice"]="unknown"
        self.assertEqual(participant_row(r,{"overall":["T01","T02"]})["choice"],(0,1))
    def dataset(self):
        rows=[]
        for arm in ("Low","Fast","Eco"):
            for i in range(4):
                r=replay(fixture());r["assigned_arm"]=arm;r["session_id"]=f"{arm}-{i}";r["participant_id"]=f"participant-{arm}-{i}"
                r["synthetic_total_energy_j"]=20+i+(3 if arm!="Eco" else 0)
                rows.append(r)
        return rows
    def test_synthetic_never_unlocks_confirmatory(self):
        result=self.analyse(self.dataset(),{"overall":["T01","T02"]},{"overall":0.05})
        self.assertFalse(result["confirmatory_allowed"])
        self.assertEqual(result["participant_n"],{"Low":4,"Fast":4,"Eco":4})
        self.assertEqual(result["per_claim_alpha"],0.0125)
    def test_delta_missing_blocks_joint_rule(self):
        result=self.analyse(self.dataset(),{"overall":["T01","T02"]})
        self.assertIsNone(result["comparisons"]["Eco-Low"]["numeric_quality_rule"])
        self.assertFalse(result["comparisons"]["Eco-Low"]["numeric_joint_rule"])
    def test_duplicate_participant_rejected(self):
        rows=self.dataset();rows.append(rows[0])
        with self.assertRaises(ValueError):self.analyse(rows,{"overall":["T01","T02"]})
    def test_mixed_provenance_rejected(self):
        rows=self.dataset();rows[0]["measurement_kind"]="device_counter"
        with self.assertRaises(ValueError):self.analyse(rows,{"overall":["T01","T02"]})
    def test_changing_tasks_rejected(self):
        rows=self.dataset();rows[0]["assigned_task_ids"].append("T03")
        with self.assertRaises(ValueError):self.analyse(rows,{"overall":["T01","T02"]})
    def test_unjustified_partial_delta_rejected(self):
        with self.assertRaises(ValueError):self.analyse(self.dataset(),{"overall":["T01","T02"]},{"other":0.05})
    def test_empty_quality_strata_rejected(self):
        with self.assertRaises(ValueError):self.analyse(self.dataset(),{},{})
    def test_omitting_hard_tasks_from_quality_rejected(self):
        with self.assertRaises(ValueError):self.analyse(self.dataset(),{"overall":["T01"]},{"overall":0.05})
    def test_same_person_different_sessions_rejected(self):
        rows=self.dataset()
        for r in rows:r["participant_id"]="same-person"
        with self.assertRaises(ValueError):self.analyse(rows,{"overall":["T01","T02"]})
    def test_across_arm_backend_change_rejected(self):
        rows=self.dataset();rows[-1]["frozen_backend_hash"]="different"
        with self.assertRaisesRegex(ValueError,"backend hash"):self.analyse(rows,{"overall":["T01","T02"]})
    def test_across_arm_measurement_boundary_change_rejected(self):
        rows=self.dataset();rows[-1]["measurement_boundary"]["scope"]="server_input"
        with self.assertRaisesRegex(ValueError,"must not be mixed"):self.analyse(rows,{"overall":["T01","T02"]})
    def test_no_silent_loss_of_assigned_participant(self):
        rows=self.dataset();rows.pop()
        with self.assertRaisesRegex(ValueError,"COMPLETE"):self.analyse(rows,{"overall":["T01","T02"]})

if __name__ == "__main__":
    unittest.main(verbosity=2)

