"""Connect v3 observations, raw responses and engine events for one escape run.

A provider accepts messages and returns raw JSON text. TimeoutError and
ConnectionError stop the run as infrastructure_error. Malformed responses
and illegal actions are preserved and stop the run without regeneration.
Run this file for scripted checks only. It calls no external model.
"""

import json
from copy import deepcopy
from dataclasses import asdict

from observe_escape_v3 import messages
from replay_escape_v3 import GateState, VERSION, audit, transition


def run_episode(run_id, powered, profiles, provider, *, evidence, max_attempts=11):
    if evidence not in ("synthetic", "model"):
        raise ValueError("Declare synthetic or model evidence")
    if type(powered) is not bool or type(max_attempts) is not int or max_attempts <= 0:
        raise ValueError("Set gate power and a positive attempt budget")
    snapshot = dict(profiles)
    if set(snapshot) != {"holder", "partner"} or any(
        not isinstance(text, str) or not text.strip() for text in snapshot.values()
    ):
        raise ValueError("This fixture needs two free-text profiles")
    state = GateState(powered=powered, gate_ready=powered)
    turns, dialogue = [], []
    status = "budget_exhausted"

    for number in range(1, max_attempts + 1):
        actor = state.escape.route.next_actor
        request = messages(state, snapshot[actor], dialogue)
        turn = {
            "turn_id": f"{run_id}:{number}", "actor": actor,
            "messages": deepcopy(request), "before": asdict(state),
        }
        turns.append(turn)
        try:
            raw = provider(request)
        except (TimeoutError, ConnectionError) as error:
            turn["transport_error"] = type(error).__name__
            status = "infrastructure_error"
            break
        turn["raw_response"] = raw
        try:
            response = json.loads(raw)
        except (TypeError, ValueError):
            response = None
        if (
            not isinstance(response, dict) or set(response) != {"speech", "action"}
            or not all(isinstance(value, str) for value in response.values())
        ):
            status = "malformed_response"
            break
        state, event = transition(state, actor, response["action"])
        turn.update(response=response, event=event)
        if not event["accepted"]:
            status = "illegal_action"
            break
        dialogue.append({"actor": actor, "speech": response["speech"], "engine_event": event})
        if state.escape.route.next_actor is None:
            status = "escaped"
            break
    return {
        "version": VERSION, "run_id": run_id, "evidence": evidence,
        "profiles": snapshot, "powered": powered, "status": status,
        "turns": turns, "final": asdict(state),
    }


def check():
    profiles = {"holder": "舞台技師。\n相手に説明する。  ",
                "partner": "교수에게도 질문하는 학생. 근거를 확인한다."}
    summaries = []
    for powered in (True, False):
        for index, path in enumerate(audit(powered)["paths"]):
            events = iter(path["events"])
            observed = []

            def scripted(request):
                payload = json.loads(request[1]["content"])
                observed.append(payload)
                event = next(events)
                assert payload["world"] == event["before"]
                return json.dumps({"speech": "배터리를 건넸다.", "action": event["action"]})

            run = run_episode(f"scripted-{powered}-{index}", powered, profiles, scripted,
                              evidence="synthetic")
            assert run["status"] == "escaped" and len(run["turns"]) == len(path["events"])
            assert run["final"] == path["events"][-1]["after"]
            for number, (turn, payload) in enumerate(zip(run["turns"], observed)):
                assert payload["persona_text"] == profiles[turn["actor"]]
                assert len(payload["dialogue"]) == number
                assert payload["dialogue"] == [
                    {"actor": prior["actor"], "speech": prior["response"]["speech"],
                     "engine_event": prior["event"]} for prior in run["turns"][:number]
                ]
                assert turn["event"] == path["events"][number]
            summaries.append({"powered": powered, "actions": len(run["turns"]),
                              "status": run["status"]})

    for raw, expected in (
        ("배터리를 건넸다.", "malformed_response"),
        ('{"speech":"배터리를 건넸다.","action":"invent_exit"}', "illegal_action"),
    ):
        run = run_episode("error-check", False, profiles, lambda _: raw, evidence="synthetic")
        assert run["status"] == expected and len(run["turns"]) == 1
        assert run["turns"][0]["raw_response"] == raw
        assert run["final"] == asdict(GateState(powered=False, gate_ready=False))

    def timeout(_):
        raise TimeoutError()

    run = run_episode("timeout-check", True, profiles, timeout, evidence="synthetic")
    assert run["status"] == "infrastructure_error" and len(run["turns"]) == 1
    run = run_episode(
        "budget-check", True, profiles,
        lambda _: '{"speech":"","action":"prepare_holder_exit"}',
        evidence="synthetic", max_attempts=1,
    )
    assert run["status"] == "budget_exhausted" and run["final"]["escape"]["route"]["actions"] == 1
    return {"evidence": "synthetic", "complete_runs": summaries,
            "error_checks": ["malformed_response", "illegal_action", "infrastructure_error",
                             "budget_exhausted"]}


if __name__ == "__main__":
    print(json.dumps(check(), ensure_ascii=False, indent=2))
