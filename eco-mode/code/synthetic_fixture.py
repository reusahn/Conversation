"""All numbers, tasks and observations below are synthetic engineering data."""
from copy import deepcopy
from session_replay import canonical_hash, mode_hash

def fixture():
    config = {"common":{"model":"Qwen/Qwen3-4B-CANDIDATE-NOT-RUN",
                        "revision":"UNPINNED","runtime_version":"UNPINNED",
                        "parser":"UNVERIFIED","response_schema_version":"UNVERIFIED",
                        "max_tokens":8192,"temperature":0.6,"top_p":0.95,
                        "precision":"UNVERIFIED","cache_policy":"synthetic_off",
                        "tokenizer_revision":"UNPINNED","prompt_sha256":"synthetic_only"},
              "modes":{"low":{"thinking_token_budget":256},
                       "high":{"thinking_token_budget":2048}}}
    def ctr(t,value):
        return {"source":"fixture","device":"synthetic-device","scope":"gpu",
                "epoch":"synthetic-epoch-1","unit":"mJ","value_raw":value,
                "read_start_ns":t-1,"read_end_ns":t}
    events = [
        {"type":"session_start","t_ns":1,"counter":ctr(1,100000),
         "assigned_arm":"Eco","participant_id":"synthetic-participant-1",
         "assigned_task_ids":["T01","T02"],
         "backend_hash":canonical_hash(config)},
        {"type":"request_submitted","t_ns":3,"request_id":"r1","task_id":"T01",
         "mode":"low","effective_config_hash":mode_hash(config,"low")},
        {"type":"attempt_start","t_ns":5,"request_id":"r1","attempt_id":"a1",
         "counter":ctr(5,101000),"effective_config_hash":mode_hash(config,"low")},
        {"type":"attempt_end","t_ns":10,"attempt_id":"a1","status":"success",
         "counter":ctr(10,106000)},
        {"type":"request_submitted","t_ns":15,"request_id":"r2","task_id":"T02",
         "mode":"high","effective_config_hash":mode_hash(config,"high")},
        {"type":"attempt_start","t_ns":17,"request_id":"r2","attempt_id":"a2",
         "counter":ctr(17,109000),"effective_config_hash":mode_hash(config,"high")},
        {"type":"cancel_requested","t_ns":20,"attempt_id":"a2"},
        {"type":"close_requested","t_ns":21,"reason":"abandoned"},
        {"type":"attempt_end","t_ns":25,"attempt_id":"a2","status":"cancelled",
         "counter":ctr(25,121000)},
        {"type":"backend_drained","t_ns":26},
        {"type":"session_end","t_ns":28,"counter":ctr(28,122000),
         "logging_complete":True,"outcomes":{"T01":"success","T02":"abandoned"}}
    ]
    for i,e in enumerate(events,1):
        e.update(event_id=f"e{i}",server_seq=i,session_id="synthetic-session-1")
    return {"measurement_kind":"synthetic","backend_config":config,"events":events,
            "sensor_evidence":{"timing_uncertainty_known":False,
                               "epoch_evidence":"fixture assumption only, no real sensor"}}

def no_call_fixture():
    doc = fixture()
    events = [deepcopy(doc["events"][i]) for i in (0,7,9,10)]
    events[-1]["outcomes"] = {"T01":"not_started","T02":"not_started"}
    events[-1]["counter"]["value_raw"] = 103000
    for i,e in enumerate(events,1):
        e["event_id"] = f"none-{i}"
        e["server_seq"] = i
    doc["events"] = events
    return doc

