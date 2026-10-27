"""Conservative participant-level analysis PREPARATION, not a preregistered study."""
import argparse
import json
import math
import statistics
from pathlib import Path
from scipy import stats

FAMILY_ALPHA = 0.05
CLAIMS = 4
ALPHA = FAMILY_ALPHA / CLAIMS

def bounded_difference(eco, control, alpha=ALPHA, two_sided=False):
    """Hoeffding confidence bound for independent [0,1] participant outcomes.
    Each input is a (lower, upper) interval; missing is (0,1), not zero.
    Independence is an assumption, not verified by this function.
    """
    if not 0 < alpha < 1 or not eco or not control:
        raise ValueError("valid alpha and nonempty groups required")
    for lo, hi in list(eco) + list(control):
        if not 0 <= lo <= hi <= 1:
            raise ValueError("invalid bounded outcome interval")
    lo = statistics.mean(x[0] for x in eco) - statistics.mean(x[1] for x in control)
    hi = statistics.mean(x[1] for x in eco) - statistics.mean(x[0] for x in control)
    factor = math.log((2 if two_sided else 1) / alpha)
    radius = math.sqrt(0.5 * (1/len(eco) + 1/len(control)) * factor)
    return {"identification_lower": lo, "identification_upper": hi,
            "confidence_lower": max(-1.0, lo-radius) if two_sided else None,
            "confidence_upper": min(1.0, hi+radius),
            "radius": radius, "alpha": alpha,
            "method": "bounded_hoeffding_all_assigned_participants",
            "simultaneous_intervals": False}

def welch_energy(eco, control, alpha=ALPHA):
    """Raw-Joule Welch upper bound. Approximate, not distribution-free."""
    if any(x is None for x in list(eco)+list(control)):
        return {"status": "blocked_missing_energy", "upper_j": None}
    if min(len(eco), len(control)) < 2:
        return {"status": "blocked_insufficient_n", "upper_j": None}
    if any(not math.isfinite(x) or x < 0 for x in list(eco)+list(control)):
        raise ValueError("energy must be finite and nonnegative")
    delta = statistics.mean(eco)-statistics.mean(control)
    a, b = statistics.variance(eco)/len(eco), statistics.variance(control)/len(control)
    se2 = a+b
    if se2 <= 0:
        return {"status": "blocked_zero_variance", "difference_j": delta, "upper_j": None}
    df = se2**2/(a*a/(len(eco)-1)+b*b/(len(control)-1))
    se = math.sqrt(se2)
    return {"status": "approximate_only", "difference_j": delta, "standard_error_j": se,
            "df": df, "upper_j": delta+float(stats.t.ppf(1-alpha,df))*se,
            "p_less": float(stats.t.cdf(delta/se,df)), "alpha": alpha,
            "notice": "Finite-sample skew/variance robustness requires independent pilot checks."}

def participant_row(report, strata):
    tasks = report["assigned_task_ids"]
    if not tasks or len(set(tasks)) != len(tasks):
        raise ValueError("unique assigned tasks required")
    first = report["first_choice"]
    if first not in {"low", "high", "none", "unknown"}:
        raise ValueError("invalid first choice")
    choice = (0.0,1.0) if first == "unknown" else ((1.0,1.0) if first == "low" else (0.0,0.0))
    failures = {}
    for name, subset in strata.items():
        if not subset or len(set(subset)) != len(subset) or set(subset)-set(tasks):
            raise ValueError("strata must refer to unique assigned tasks")
        lower, upper = 0, 0
        for task in subset:
            status = report["outcomes"].get(task,"unknown")
            if status == "unknown":
                upper += 1
            elif status == "success":
                pass
            elif status in {"failure","abandoned","timeout","not_started"}:
                lower += 1; upper += 1
            else:
                raise ValueError("invalid outcome")
        failures[name] = (lower/len(subset),upper/len(subset))
    field = ("synthetic_total_energy_j" if report["measurement_kind"] == "synthetic"
             else "measured_total_energy_j")
    energy = report.get(field) if report.get("energy_valid") is True else None
    return {"session_id":report["session_id"],"arm":report["assigned_arm"],
            "choice":choice,"failure_intervals":failures,"energy_j":energy,
            "measurement_kind":report["measurement_kind"],"first_choice_state":first}

def analyse(reports, strata, delta_by_stratum=None, *, assignment_manifest):
    if not reports:
        raise ValueError("nonempty all-assigned participant records required")
    if len({r["session_id"] for r in reports}) != len(reports):
        raise ValueError("one row per participant/session; duplicate IDs")
    participant_ids = [r.get("participant_id") for r in reports]
    if (any(not isinstance(p,str) or not p.strip() for p in participant_ids)
            or len(set(participant_ids)) != len(reports)):
        raise ValueError("one explicit unique pseudonymous participant ID per assigned row required")
    if len({tuple(sorted(r["assigned_task_ids"])) for r in reports}) != 1:
        raise ValueError("this fixed-task analysis requires identical task assignments")
    assigned_tasks = set(reports[0]["assigned_task_ids"])
    if (not strata or "overall" not in strata
            or set(strata["overall"]) != assigned_tasks):
        raise ValueError("nonempty strata and overall containing all assigned tasks required")
    manifest_ids = [x["participant_id"] for x in assignment_manifest]
    if len(set(manifest_ids)) != len(manifest_ids) or set(manifest_ids) != set(participant_ids):
        raise ValueError("reports must match the COMPLETE supplied assignment manifest")
    manifest = {x["participant_id"]:x for x in assignment_manifest}
    for r in reports:
        a = manifest[r["participant_id"]]
        if (a["assigned_arm"] != r["assigned_arm"]
                or set(a["assigned_task_ids"]) != set(r["assigned_task_ids"])):
            raise ValueError("report assignment differs from supplied manifest")
    hashes = {r.get("frozen_backend_hash") for r in reports}
    if len(hashes) != 1 or None in hashes or "" in hashes:
        raise ValueError("frozen common+two-mode backend hash must match across arms")
    boundaries = {json.dumps(r["measurement_boundary"],sort_keys=True)
                  for r in reports if r.get("measurement_boundary") is not None}
    if len(boundaries) > 1:
        raise ValueError("measurement source/device/scope/unit must not be mixed")
    kinds = {r["measurement_kind"] for r in reports}
    if len(kinds) != 1 or not kinds <= {"synthetic","device_counter"}:
        raise ValueError("do not mix synthetic and declared device-counter datasets")
    if delta_by_stratum is not None and (set(delta_by_stratum) != set(strata)
            or any(not 0 < x < 1 for x in delta_by_stratum.values())):
        raise ValueError("a prespecified 0<delta<1 for every stratum is required")
    rows = [participant_row(r,strata) for r in reports]
    arms = {arm:[r for r in rows if r["arm"] == arm] for arm in ("Low","Fast","Eco")}
    if sum(map(len,arms.values())) != len(rows) or any(not v for v in arms.values()):
        raise ValueError("all three valid arms required")
    comparisons = {}
    for arm in ("Low","Fast"):
        e, c = arms["Eco"], arms[arm]
        choice = bounded_difference([r["choice"] for r in e],[r["choice"] for r in c],two_sided=True)
        quality = {s:bounded_difference([r["failure_intervals"][s] for r in e],
                                       [r["failure_intervals"][s] for r in c]) for s in strata}
        energy = welch_energy([r["energy_j"] for r in e],[r["energy_j"] for r in c])
        quality_rule = (all(quality[s]["confidence_upper"] < delta_by_stratum[s] for s in strata)
                        if delta_by_stratum is not None else None)
        energy_rule = energy.get("upper_j") is not None and energy["upper_j"] < 0
        comparisons["Eco-"+arm] = {"choice":choice,"energy":energy,"failure":quality,
            "numeric_quality_rule":quality_rule,"numeric_energy_rule":energy_rule,
            "numeric_joint_rule": bool(energy_rule and quality_rule),
            "confirmatory_allowed":False}
    return {"dataset_kind":next(iter(kinds)),"participant_n":{k:len(v) for k,v in arms.items()},
            "supplied_manifest_matched":True,"manifest_independently_authenticated":False,
            "first_choice_states":{k:{s:sum(r["first_choice_state"] == s for r in v)
                                     for s in ("low","high","none","unknown")} for k,v in arms.items()},
            "family_alpha":FAMILY_ALPHA,"claims":CLAIMS,"per_claim_alpha":ALPHA,
            "delta_by_stratum":delta_by_stratum,"comparisons":comparisons,
            "confirmatory_allowed":False,
            "blocks":["Preparation only: actual resources, margin justification, pilot, N and preregistration remain unverified.",
                      "Welch energy inference is approximate; bounded-outcome bounds do not validate it.",
                      "Input provenance and randomization/participant independence are not authenticated by this script."]}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset",type=Path)
    args = parser.parse_args()
    data = json.loads(args.dataset.read_text())
    print(json.dumps(analyse(data["reports"],data["strata"],data.get("delta_by_stratum"),
                             assignment_manifest=data["assignment_manifest"]),
                     indent=2,allow_nan=False))

if __name__ == "__main__":
    main()

