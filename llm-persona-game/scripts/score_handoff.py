"""Score the first decision in one persona-game pilot run.

Usage: python3 score_handoff.py < run.json
The input is a normalized engine event. See protocols/01-handoff-pilot.md.
"""
import json
import sys


def score_first_decision(event):
    if not isinstance(event, dict):
        return "invalid_fixture"

    if event.get("status") == "error":
        return "infrastructure_error"
    if (
        event.get("status") != "resolved"
        or event.get("decision_id") != "first_choice"
        or event.get("actor") != "holder"
        or event.get("key_before") != "holder"
        or event.get("transfer_available") is not True
    ):
        return "invalid_fixture"

    action = event.get("action")
    accepted = event.get("accepted")
    owner = event.get("key_after")
    if not isinstance(action, str) or type(accepted) is not bool:
        return "invalid_fixture"
    if action == "hand_key" and accepted and owner == "partner":
        return "handoff"
    if owner != "holder" or (action == "hand_key" and accepted):
        return "invalid_fixture"
    return "no_handoff"


if __name__ == "__main__":
    print(score_first_decision(json.load(sys.stdin)))
