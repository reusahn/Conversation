"""Enumerate every legal-action path in the existing escape fixture.

Run from llm-persona-game: python3 scripts/audit_escape_choices.py
The report measures task structure. It makes no model calls.
"""

import json
from collections import Counter, deque
from dataclasses import asdict

from replay_handoff import State, options, replay, transition


def audit_choices():
    initial = State()
    frontier = deque([initial])
    visited = set()
    decisions = []
    forced = 0
    terminals = []
    edges = 0
    while frontier:
        state = frontier.popleft()
        if state in visited:
            continue
        visited.add(state)
        actions = options(state)
        if state.next_actor is None:
            assert not actions
            terminals.append(asdict(state))
            continue
        if not actions:
            raise AssertionError("An active state has no legal continuation")
        if len(actions) > 1:
            decisions.append({"state": asdict(state), "choices": list(actions)})
        else:
            forced += 1
        for action in actions:
            after, event = transition(state, state.next_actor, action)
            assert event["accepted"] and after.actions == state.actions + 1
            assert after.actions <= 7, "Fixture should finish within seven legal actions"
            edges += 1
            frontier.append(after)

    paths = []

    def visit(state, actions, widths):
        if state.next_actor is None:
            paths.append({"actions": actions, "choice_counts": widths, "final": asdict(state)})
            return
        legal = options(state)
        for action in legal:
            after, _ = transition(state, state.next_actor, action)
            visit(after, actions + [action], widths + [len(legal)])

    visit(initial, [], [])
    for path in paths:
        expected = replay(path["actions"][0])
        assert path["actions"] == [event["action"] for event in expected["events"]]
        assert path["final"] == expected["final"]

    assert len(visited) == 15 and edges == 14
    assert len(decisions) == 1 and decisions[0]["state"] == asdict(initial)
    assert forced == 12 and len(terminals) == len(paths) == 2
    assert all(path["choice_counts"] == [2, 1, 1, 1, 1, 1, 1] for path in paths)
    assert all(path["final"]["holder_step"] == 3 and path["final"]["partner_step"] == 4
               for path in paths)
    return {
        "evidence": "exhaustive_legal_transition_audit",
        "reachable_states": len(visited),
        "legal_edges": edges,
        "branching_states": decisions,
        "forced_nonterminal_states": forced,
        "terminal_states": terminals,
        "terminal_action_counts": dict(sorted(Counter(s["actions"] for s in terminals).items())),
        "paths": paths,
        "scope": "All legal actions from State(). Invalid actions and model errors are excluded.",
    }


if __name__ == "__main__":
    print(json.dumps(audit_choices(), ensure_ascii=False, indent=2))
