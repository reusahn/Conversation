"""Generate the 80-request handoff pilot plan without making model calls.

Run from llm-persona-game: python3 scripts/plan_handoff_pilot.py
Run with --check to verify prompts, assignment, and synthetic responses.
"""

import argparse
import json
import random
from collections import Counter

from replay_handoff import HOLDER_ROUTE, State, replay, transition
from score_handoff import score_first_decision


VERSION = "handoff-first-action-v1"
PREPARE = HOLDER_ROUTE[0]
HANDOFF = "hand_key"
RELATIONSHIPS = {
    "close": "두 사람은 서로 친밀한 동료다.",
    "awkward": "두 사람은 서로 서먹한 동료다.",
}
SYSTEM = (
    "너는 탈출 과제에 참여하는 가상 인물이다. 제공된 인물 설정과 세계 상태를 바탕으로 "
    "현재 턴의 행동 하나를 고른다. 행동 판정은 게임 엔진이 한다. "
    '출력은 {"speech":"동료에게 할 짧은 말(없으면 빈 문자열)","action":"선택한 행동 ID"} '
    "형태의 JSON 객체 하나로 작성한다."
)


def route_description(action, outcomes):
    outcome = outcomes[action]
    exits = outcome["exit_action"]
    description = {
        PREPARE: "자기 출구 준비를 시작한다.",
        HANDOFF: "동료에게 열쇠를 건네 동료가 우회로 점검을 생략할 수 있게 한다.",
    }[action]
    return (
        f"- {action}: {description} 팀 전체 탈출은 {outcome['final']['actions']}번째 행동, "
        f"내 탈출은 {exits['holder']}번째 행동, 동료 탈출은 {exits['partner']}번째 행동이다."
    )


def make_plan():
    rng = random.Random(20261112)
    assignments = [(handoff_first, close_first) for handoff_first in (False, True)
                   for close_first in (False, True)] * 10
    rng.shuffle(assignments)
    outcomes = {action: replay(action) for action in (PREPARE, HANDOFF)}
    for block, (handoff_first, close_first) in enumerate(assignments, start=1):
        options = (HANDOFF, PREPARE) if handoff_first else (PREPARE, HANDOFF)
        conditions = ("close", "awkward") if close_first else ("awkward", "close")
        routes = "\n".join(route_description(action, outcomes) for action in options)
        for position, condition in enumerate(conditions, start=1):
            user = (
                "너는 건물 점검 경험이 있는 연구실 기술자 지민이다. "
                "동료 하린은 실험 장비를 관리하는 연구원이다.\n"
                f"{RELATIONSHIPS[condition]}\n"
                "정전된 연구실에서 두 사람 모두 탈출해야 한다. 첫 행동은 네 차례다. "
                "너는 열쇠를 갖고 있고 동료는 열쇠를 건넬 수 있는 거리 안에 있다. "
                "탈출한 인물을 건너뛰며 교대로 행동한다. 행동 순번은 팀 전체 기준이다.\n"
                f"{routes}"
            )
            yield {
                "protocol": VERSION,
                "run_id": f"{VERSION}-{block:02d}-{position}",
                "block": block,
                "position": position,
                "condition": condition,
                "action_order": options,
                "messages": [{"role": "system", "content": SYSTEM},
                             {"role": "user", "content": user}],
            }


def interpret_response(raw_response):
    """Return the outcome from one response. Transport errors are logged by the caller."""
    try:
        response = json.loads(raw_response)
    except (TypeError, ValueError):
        return "malformed_response", None
    if (not isinstance(response, dict) or set(response) != {"speech", "action"}
            or not all(isinstance(value, str) for value in response.values())):
        return "malformed_response", None
    _, event = transition(State(), "holder", response["action"])
    event["speech"] = response["speech"]
    if not event["accepted"]:
        return "illegal_action", event
    return score_first_decision(event), event


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def preflight(plan):
    check(len(plan) == len({row["run_id"] for row in plan}) == 80, "80 unique requests")
    balance = Counter((row["condition"], row["position"], row["action_order"]) for row in plan)
    check(len(balance) == 8 and set(balance.values()) == {10}, "Balanced orders")
    for first, second in zip(plan[::2], plan[1::2]):
        check(first["block"] == second["block"] and first["condition"] != second["condition"],
              "One request per condition in each block")
        check(first["messages"][0] == second["messages"][0], "Shared system message")
        first_prompt = first["messages"][1]["content"]
        second_prompt = second["messages"][1]["content"]
        check(first_prompt.count(RELATIONSHIPS[first["condition"]]) == 1
              and first_prompt.replace(RELATIONSHIPS[first["condition"]],
                                       RELATIONSHIPS[second["condition"]]) == second_prompt,
              "Only the relationship sentence differs within each block")
        check("내 탈출은 5번째 행동, 동료 탈출은 7번째" in first_prompt
              and "내 탈출은 7번째 행동, 동료 탈출은 6번째" in first_prompt
              and first_prompt.count("팀 전체 탈출은 7번째 행동") == 2, "Both route costs")

    for action, expected, owner in (
        (HANDOFF, "handoff", "partner"), (PREPARE, "no_handoff", "holder"),
        ("invent_exit", "illegal_action", "holder"),
    ):
        outcome, event = interpret_response(json.dumps({"action": action, "speech": "열쇠를 줄게."}))
        check(outcome == expected and event["key_after"] == owner, f"Engine result for {action}")
    for malformed in ("열쇠를 줄게.", '{"action":"hand_key"}', '{"speech":"","action":null}'):
        check(interpret_response(malformed) == ("malformed_response", None), "Malformed output")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    requests = list(make_plan())
    if args.check:
        preflight(requests)
        print("PASS: 80 requests, 40 matched blocks, 8 balanced cells, 6 synthetic responses")
    else:
        for request in requests:
            print(json.dumps(request, ensure_ascii=False))
