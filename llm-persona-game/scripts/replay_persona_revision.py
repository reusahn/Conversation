"""Replay a free-text profile revision in the existing escape fixture.

Run: python3 scripts/replay_persona_revision.py
All dialogue and action inputs are scripted. This module calls no model.
"""

import json
from dataclasses import asdict

from replay_handoff import State, options, transition


def run_attempt(run_id, parent_id, profiles, select):
    state = State()
    snapshot = dict(profiles)
    if snapshot.keys() != {"holder", "partner"} or any(
        not isinstance(text, str) or not text.strip() for text in snapshot.values()
    ):
        raise ValueError("The escape fixture needs two nonempty free-text profiles")

    turns = []
    while state.next_actor is not None:
        actor = state.next_actor
        observation = {
            "actor": actor,
            "profile": snapshot[actor],
            "state": asdict(state),
            "legal_actions": options(state),
            "dialogue": tuple((turn["event"]["actor"], turn["speech"]) for turn in turns),
        }
        speech, action = select(observation)
        state, event = transition(state, actor, action)
        turns.append({"id": f"{run_id}:{len(turns) + 1}", "speech": speech, "event": event})
        if not event["accepted"]:
            break

    return {
        "evidence": "scripted_input",
        "run_id": run_id,
        "parent_id": parent_id,
        "profiles": snapshot,
        "initial": asdict(State()),
        "turns": turns,
        "escaped": state.next_actor is None,
    }


def demo():
    profiles = {
        "holder": "야간 전시 설치 기사. 하린과 오래 일했고 판단하기 전에 상황을 설명한다.",
        "partner": "하린은 장비 기록 담당자다. 낯선 장치 앞에서 확인 질문을 한다.",
    }
    observations = []

    def scripted(first_action):
        def select(observation):
            observations.append(observation)
            if observation["state"]["actions"] == 0:
                return "열쇠를 줄게.", first_action
            return "", observation["legal_actions"][0]

        return select

    original = run_attempt("attempt-1", None, profiles, scripted("prepare_holder_exit"))
    revised_profile = "야간 전시 설치 기사. 하린과 오래 일했고 판단하기 전에 하린에게 먼저 묻는다."
    profiles["holder"] = revised_profile
    retry = run_attempt("attempt-2", original["run_id"], profiles, scripted("hand_key"))
    rejected = run_attempt("rejected", None, profiles, scripted("invent_exit"))

    assert original["initial"] == retry["initial"]
    assert original["profiles"]["holder"] != retry["profiles"]["holder"]
    assert original["profiles"]["partner"] == retry["profiles"]["partner"]
    assert retry["profiles"]["holder"] == revised_profile
    assert observations[0]["profile"] == original["profiles"]["holder"]
    assert observations[7]["profile"] == revised_profile and not observations[7]["dialogue"]
    assert observations[1]["profile"] == original["profiles"]["partner"]
    assert observations[1]["dialogue"] == (("holder", "열쇠를 줄게."),)
    assert original["escaped"] and retry["escaped"]
    assert len(original["turns"]) == len(retry["turns"]) == 7
    assert original["turns"][0]["speech"] == retry["turns"][0]["speech"]
    assert original["turns"][0]["event"]["key_after"] == "holder"
    assert retry["turns"][0]["event"]["key_after"] == "partner"
    assert retry["parent_id"] == original["run_id"]
    event = rejected["turns"][0]["event"]
    assert not event["accepted"] and event["before"] == event["after"] and not rejected["escaped"]
    return {
        "attempts": [original, retry],
        "revision": {
            "actor": "holder",
            "observed_turn": original["turns"][0]["id"],
            "reason": "합성 예시: 발화와 소유권 상태의 불일치를 본 뒤 질문 습관을 수정",
        },
        "rejected_attempt": rejected,
    }


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
