"""Export reproducible SYNTHETIC engineering artifacts and source checksums."""
import hashlib
import io
import json
import platform
from pathlib import Path
import unittest
import scipy
from synthetic_fixture import fixture
from session_replay import replay
from analysis_prepare import analyse

BASE = Path(__file__).resolve().parent

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+"\n")

def main():
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(BASE), pattern="test_research_tools.py")
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (BASE/"results").mkdir(exist_ok=True)
    (BASE/"results/tests.txt").write_text(stream.getvalue())
    report = {"kind":"synthetic_engineering_only", "tests_run":result.testsRun,
        "failures":len(result.failures),"errors":len(result.errors),
        "all_passed":result.wasSuccessful(),"python":platform.python_version(),
        "scipy":scipy.__version__,"device_energy_measurement":False,
        "actual_model_inference":False,"human_participants":False,
        "source_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(BASE.glob("*.py"))},
        "notice":"Tests validate synthetic cases and selected invariants, not complete system correctness or research effects."}
    write_json(BASE/"results/research-tools.json",report)
    if not result.wasSuccessful():
        print(json.dumps(report)); return 1
    example=fixture()
    write_json(BASE/"fixtures/synthetic-session.json",example)
    write_json(BASE/"results/synthetic-replay.json",replay(example))
    reports=[]
    assignments=[]
    for arm in ("Low","Fast","Eco"):
        for i in range(4):
            d=fixture()
            d["events"][0]["assigned_arm"]=arm
            d["events"][0]["participant_id"]=f"synthetic-person-{arm}-{i}"
            for e in d["events"]: e["session_id"]=f"synthetic-session-{arm}-{i}"
            d["events"][-1]["counter"]["value_raw"] += i*1000
            r=replay(d)
            reports.append(r)
            assignments.append({"participant_id":r["participant_id"],"assigned_arm":arm,
                                "assigned_task_ids":r["assigned_task_ids"]})
    dataset={"notice":"Entirely synthetic engineering data, no people or sensors.",
             "reports":reports,"strata":{"overall":["T01","T02"]},
             "assignment_manifest":assignments,"delta_by_stratum":None}
    write_json(BASE/"fixtures/synthetic-dataset.json",dataset)
    analysis=analyse(reports,dataset["strata"],assignment_manifest=assignments)
    write_json(BASE/"results/synthetic-analysis.json",analysis)
    print(json.dumps(report,indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
