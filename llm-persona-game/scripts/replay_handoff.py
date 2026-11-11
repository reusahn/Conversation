"""Replay scripted actions in the two-person escape pilot.

Run from llm-persona-game: python3 scripts/replay_handoff.py
The JSON output contains synthetic engine events. No model is called.
"""

import json
from dataclasses import asdict, dataclass, replace
from functools import lru_cache

from score_handoff import score_first_decision


HOLDER_ROUTE = ("prepare_holder_exit", "cross_holder_exit", "leave_holder_exit")
PARTNER_ROUTE = (
    "inspect_backup_route",
    "prepare_partner_exit",
    "cross_partner_exit",
    "leave_partner_exit",
)


@dataclass(frozen=True)
class State:
    holder_step: int = 0
    partner_step: int = 0
    key_owner: str = "holder"
    next_actor: str = "holder"
    actions: int = 0


def options(state):
    if state.next_actor == "holder":
        if state.actions == 0:
            return (HOLDER_ROUTE[0], "hand_key")
        return (HOLDER_ROUTE[state.holder_step],)
    if state.next_actor == "partner":
        return (PARTNER_ROUTE[state.partner_step],)
    return ()


def transition(state, actor, action):
    legal_actions = options(state)
    accepted = actor == state.next_actor and action in legal_actions
    after = state
    if accepted:
        after = replace(state, actions=state.actions + 1)
        if action == "hand_key":
            # The key opens the shortcut, skipping the backup-route inspection.
            after = replace(after, key_owner="partner", partner_step=1)
        elif actor == "holder":
            after = replace(after, holder_step=state.holder_step + 1)
        else:
            after = replace(after, partner_step=state.partner_step + 1)

        holder_done = after.holder_step == len(HOLDER_ROUTE)
        partner_done = after.partner_step == len(PARTNER_ROUTE)
        if holder_done and partner_done:
            next_actor = None
        elif partner_done or (actor == "partner" and not holder_done):
            next_actor = "holder"
        else:
            next_actor = "partner"
        after = replace(after, next_actor=next_actor)

    event = {
        "status": "resolved",
        "decision_id": "first_choice" if state.actions == 0 else "progress",
        "actor": actor,
        "key_before": state.key_owner,
        "key_after": after.key_owner,
        "transfer_available": "hand_key" in legal_actions and actor == state.next_actor,
        "action": action,
        "accepted": accepted,
        "before": asdict(state),
        "after": asdict(after),
    }
    return after, event


@lru_cache(maxsize=None)
def terminal_action_counts(state):
    if state.next_actor is None:
        return frozenset({state.actions})
    return frozenset(
        count
        for action in options(state)
        for count in terminal_action_counts(transition(state, state.next_actor, action)[0])
    )


def replay(first_action):
    state = State()
    events = []
    while state.next_actor is not None:
        action = first_action if not events else options(state)[0]
        state, event = transition(state, state.next_actor, action)
        if not event["accepted"]:
            raise ValueError(f"Illegal scripted action: {action}")
        events.append(event)
    exits = {
        "holder": next(e["after"]["actions"] for e in events if e["action"] == HOLDER_ROUTE[-1]),
        "partner": next(e["after"]["actions"] for e in events if e["action"] == PARTNER_ROUTE[-1]),
    }
    return {
        "classification": score_first_decision(events[0]),
        "terminal_action_counts": sorted(terminal_action_counts(State(**events[0]["after"]))),
        "exit_action": exits,
        "final": asdict(state),
        "events": events,
    }


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    independent = replay("prepare_holder_exit")
    handoff = replay("hand_key")
    check(independent["events"][0]["before"] == handoff["events"][0]["before"], "Initial state")
    for result, label, owner, first_progress, exits in (
        (independent, "no_handoff", "holder", (1, 0), {"holder": 5, "partner": 7}),
        (handoff, "handoff", "partner", (0, 1), {"holder": 7, "partner": 6}),
    ):
        first = result["events"][0]
        check((first["after"]["holder_step"], first["after"]["partner_step"]) == first_progress,
              "First action changes only the expected route progress")
        check(result["classification"] == label and result["final"]["key_owner"] == owner,
              "Scorer and final key ownership")
        check(result["terminal_action_counts"] == [7] and result["final"]["actions"] == 7,
              "Terminal cost across legal continuations")
        check(result["exit_action"] == exits, "Individual exit order and timing")

    initial = State()
    after, wrong_actor = transition(initial, "partner", "hand_key")
    check(after == initial and not wrong_actor["accepted"]
          and score_first_decision(wrong_actor) == "invalid_fixture", "Wrong actor cannot transfer")
    after, speech = transition(initial, "holder", "I give the key to my partner.")
    check(after == initial and not speech["accepted"]
          and score_first_decision(speech) == "no_handoff", "Speech cannot change ownership")
    progressed, _ = transition(initial, "holder", "prepare_holder_exit")
    progressed, _ = transition(progressed, "partner", "inspect_backup_route")
    check(progressed.next_actor == "holder", "Late-transfer test uses the rightful actor")
    after, late = transition(progressed, "holder", "hand_key")
    check(after == progressed and not late["accepted"] and not late["transfer_available"],
          "Transfer is restricted to the initial decision")
    print(json.dumps({"independent": independent, "handoff": handoff,
                      "rejected": [wrong_actor, speech, late]}, indent=2))


if __name__ == "__main__":
    main()
