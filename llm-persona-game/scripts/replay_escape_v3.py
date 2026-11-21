"""Same escape scenario with a powered/unpowered partner exit gate.

An unpowered gate uses one battery action or three manual-crank actions.
Gate power is public at the start and never randomized during a run.
Run from llm-persona-game: python3 scripts/replay_escape_v3.py
"""

import json
from dataclasses import asdict, dataclass, replace

from replay_escape_v2 import EscapeState, options as v2_options, transition as v2_transition
from replay_handoff import State


VERSION = "escape-gate-resource-v3"


@dataclass(frozen=True)
class GateState:
    escape: EscapeState = EscapeState()
    powered: bool = True
    gate_ready: bool = True
    manual_steps: int = 0


def at_gate(state):
    route = state.escape.route
    return route.next_actor == "partner" and route.partner_step == 3 and not state.gate_ready


def options(state):
    if at_gate(state):
        if state.manual_steps == 0 and state.escape.battery == "partner":
            return ("power_gate", "crank_gate")
        return ("crank_gate",)
    return v2_options(state.escape)


def transition(state, actor, action):
    before = state.escape.route
    accepted = actor == before.next_actor and action in options(state)
    after = state
    if accepted:
        if at_gate(state):
            battery = state.escape.battery
            manual_steps = state.manual_steps
            if action == "power_gate":
                battery = "consumed"
                ready = True
            else:
                manual_steps += 1
                ready = manual_steps == 3
            route = replace(before, actions=before.actions + 1)
            after = replace(
                state, escape=replace(state.escape, route=route, battery=battery),
                gate_ready=ready, manual_steps=manual_steps,
            )
        else:
            escape, event = v2_transition(state.escape, actor, action)
            assert event["accepted"]
            after = replace(state, escape=escape)
    return after, {
        "version": VERSION, "actor": actor, "action": action, "accepted": accepted,
        "before": asdict(state), "after": asdict(after),
    }


def audit(powered):
    paths = []

    def visit(state, events):
        assert state.escape.route.actions <= 11
        if state.escape.route.next_actor is None:
            assert state.gate_ready
            paths.append(events)
            return
        for action in options(state):
            after, event = transition(state, state.escape.route.next_actor, action)
            assert event["accepted"]
            assert after.escape.route.actions == state.escape.route.actions + 1
            visit(after, events + [event])

    initial = GateState(powered=powered, gate_ready=powered)
    visit(initial, [])
    assert len(paths) == (4 if powered else 6)
    results = []
    for events in paths:
        battery_choice = events[1]["action"]
        gate_actions = [e["action"] for e in events if e["action"] in ("power_gate", "crank_gate")]
        final = events[-1]["after"]["escape"]
        assert final["route"]["holder_step"] == 3 and final["route"]["partner_step"] == 4
        assert events[1]["before"]["powered"] == powered
        if powered:
            assert not gate_actions
            expected = 7 if battery_choice == "lend_battery" else 8
        elif battery_choice == "lend_battery":
            assert gate_actions == ["crank_gate"] * 3
            expected = 10
        elif gate_actions == ["power_gate"]:
            expected = 9
        else:
            assert gate_actions == ["crank_gate"] * 3
            expected = 11
        assert len(events) == expected
        results.append({
            "first_action": events[0]["action"], "battery_choice": battery_choice,
            "gate_actions": gate_actions, "team_actions": len(events),
            "battery_final": final["battery"], "events": events,
        })
    minimum = {
        choice: min(r["team_actions"] for r in results if r["battery_choice"] == choice)
        for choice in ("lend_battery", "keep_battery")
    }
    assert minimum == (
        {"lend_battery": 7, "keep_battery": 8} if powered
        else {"lend_battery": 10, "keep_battery": 9}
    )
    assert transition(initial, "partner", "power_gate")[0] == initial
    for events in paths:
        for event in events:
            before = event["before"]
            escape = EscapeState(**{
                **before["escape"],
                "route": State(**before["escape"]["route"]),
            })
            state = GateState(**{**before, "escape": escape})
            if at_gate(state):
                assert transition(state, "holder", "crank_gate")[0] == state
                assert transition(state, "partner", "I power the gate")[0] == state
                if state.escape.battery != "partner":
                    assert transition(state, "partner", "power_gate")[0] == state
    return {"gate_powered": powered, "minimum_by_battery_choice": minimum, "paths": results}


if __name__ == "__main__":
    print(json.dumps({"version": VERSION, "evidence": "synthetic_legal_path_enumeration",
                      "variants": [audit(True), audit(False)]}, ensure_ascii=False, indent=2))
