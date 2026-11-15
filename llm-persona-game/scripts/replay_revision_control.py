"""Rehearse the unchanged-profile control with scripted actions, no model.

Run from llm-persona-game: python3 scripts/replay_revision_control.py
"""

import json

from replay_handoff import HOLDER_ROUTE
from replay_persona_revision import run_attempt
from score_handoff import score_first_decision


def comparison(block_id, profiles, actor, revised_text, selectors, *, edited_first):
    if actor not in profiles or profiles[actor] == revised_text:
        raise ValueError("One existing profile must change")
    revised = {**profiles, actor: revised_text}
    baseline = run_attempt(f"{block_id}-baseline", None, profiles, selectors["baseline"])
    profiles_by_arm = {"unchanged": profiles, "edited": revised}
    order = ("edited", "unchanged") if edited_first else ("unchanged", "edited")
    retries = {}
    for arm in order:
        retries[arm] = run_attempt(
            f"{block_id}-{arm}", baseline["run_id"], profiles_by_arm[arm], selectors[arm]
        )
    return baseline, retries


def first_transfer(attempt):
    event = attempt["turns"][0]["event"]
    if not event["accepted"]:
        return None
    label = score_first_decision(event)
    return {"handoff": 1, "no_handoff": 0}.get(label)


def metrics(baseline, retries):
    original = first_transfer(baseline)
    unchanged = first_transfer(retries["unchanged"])
    edited = first_transfer(retries["edited"])
    return {
        "unchanged_flip": unchanged != original if None not in (original, unchanged) else None,
        "edited_flip": edited != original if None not in (original, edited) else None,
        "edited_minus_unchanged": edited - unchanged if None not in (edited, unchanged) else None,
    }


def demo():
    original = {
        "holder": "무대 조명 기사. 상황을 각자 판단한 뒤 의견을 나눈다.",
        "partner": "동료 무대감독. 다른 사람의 계획을 듣고 장비를 확인한다.",
    }
    edited = "무대 조명 기사. 판단하기 전에 동료에게 먼저 의견을 묻는다."
    prepare = HOLDER_ROUTE[0]
    outputs = []
    patterns = [
        ((prepare, "hand_key", "hand_key"), (True, True, 0)),
        ((prepare, prepare, "hand_key"), (False, True, 1)),
        (("hand_key", "hand_key", prepare), (False, True, -1)),
        ((prepare, "invent_exit", "hand_key"), (None, True, None)),
    ]
    for number, (actions, expected) in enumerate(patterns, start=1):
        first_inputs = []

        def provider(arm, first_action):
            def select(observation):
                if observation["state"]["actions"] == 0:
                    first_inputs.append((arm, observation))
                    return "열쇠를 줄게.", first_action
                return "", observation["legal_actions"][0]

            return select

        arms = ("baseline", "unchanged", "edited")
        providers = {arm: provider(arm, action) for arm, action in zip(arms, actions)}
        baseline, retries = comparison(
            f"block-{number}", original, "holder", edited, providers, edited_first=number % 2 == 0
        )
        assert [arm for arm, _ in first_inputs] == ["baseline", *retries]
        assert all(not input_["dialogue"] for _, input_ in first_inputs)
        inputs = dict(first_inputs)
        assert inputs["baseline"] == inputs["unchanged"]
        assert dict(inputs["unchanged"], profile=edited) == inputs["edited"]
        assert all(retry["parent_id"] == baseline["run_id"] for retry in retries.values())
        assert retries["edited"]["profiles"]["partner"] == original["partner"]
        result = metrics(baseline, retries)
        assert tuple(result.values()) == expected
        outputs.append({"baseline": baseline, "retries": retries, "metrics": result})

    return {"evidence": "scripted_input", "blocks": outputs}


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
