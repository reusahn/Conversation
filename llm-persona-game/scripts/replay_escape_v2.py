"""Executable second-decision specification for the same escape scenario.

The initial key transfer uses v1 rules. On the partner's first turn, they can
lend a single-use battery to power the holder's route preparation, or retain
it as an unused reserve. Lending skips one holder route step. Both choices
consume one action. No later battery use is implemented.
Run: python3 scripts/replay_escape_v2.py
"""

import json
from dataclasses import asdict, dataclass, replace

from replay_handoff import State, options as base_options, transition as base_transition


VERSION = "escape-two-decisions-v2"


@dataclass(frozen=True)
class EscapeState:
    route: State = State()
    battery: str = "partner"
    battery_decision: str | None = None


def options(state):
    if state.route.next_actor == "partner" and state.battery_decision is None:
        return ("lend_battery", "keep_battery")
    return base_options(state.route)


def transition(state, actor, action):
    before = state.route
    accepted = actor == before.next_actor and action in options(state)
    after = state
    decision = "progress"
    if before.actions == 0:
        decision = "first_choice"
    elif actor == "partner" and state.battery_decision is None:
        decision = "battery_choice"
    if accepted:
        if decision == "battery_choice":
            route = replace(before, actions=before.actions + 1, next_actor="holder")
            if action == "lend_battery":
                route = replace(route, holder_step=before.holder_step + 1)
                after = replace(state, route=route, battery="consumed", battery_decision=action)
            else:
                after = replace(state, route=route, battery_decision=action)
        else:
            route, event = base_transition(before, actor, action)
            assert event["accepted"]
            after = replace(state, route=route)
    return after, {
        "version": VERSION, "actor": actor, "action": action,
        "decision_id": decision, "accepted": accepted,
        "before": asdict(state), "after": asdict(after),
    }


def audit():
    paths = []
    branching = []
    visited = set()

    def visit(state, events):
        assert state.route.actions <= 8
        if state not in visited:
            visited.add(state)
            if len(options(state)) > 1:
                branching.append({"state": asdict(state), "actions": list(options(state))})
        if state.route.next_actor is None:
            paths.append(events)
            return
        assert options(state)
        for action in options(state):
            after, event = transition(state, state.route.next_actor, action)
            assert event["accepted"] and after.route.actions == state.route.actions + 1
            visit(after, events + [event])

    visit(EscapeState(), [])
    assert len(paths) == 4 and len(branching) == 3
    assert {b["state"]["route"]["next_actor"] for b in branching} == {"holder", "partner"}
    results = []
    for events in paths:
        final = events[-1]["after"]
        choice = events[1]["action"]
        assert events[1]["decision_id"] == "battery_choice"
        assert final["route"]["holder_step"] == 3 and final["route"]["partner_step"] == 4
        assert len(events) == (7 if choice == "lend_battery" else 8)
        assert final["battery"] == ("consumed" if choice == "lend_battery" else "partner")
        results.append({
            "first_action": events[0]["action"], "second_action": choice,
            "actions": len(events), "battery": final["battery"], "events": events,
        })
    initial = EscapeState()
    assert transition(initial, "partner", "lend_battery")[0] == initial
    for first in options(initial):
        second, _ = transition(initial, "holder", first)
        assert transition(second, "holder", "lend_battery")[0] == second
        third, _ = transition(second, "partner", "lend_battery")
        assert transition(third, "partner", "lend_battery")[0] == third
        assert transition(second, "partner", "I lend the battery")[0] == second
    return {"version": VERSION, "evidence": "synthetic_legal_path_enumeration",
            "branching": branching, "paths": results}


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
