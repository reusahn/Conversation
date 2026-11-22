"""Build full-information v3 observations without calling a model.

Run from llm-persona-game: python3 scripts/observe_escape_v3.py
Profiles are preserved verbatim in a separate JSON field. Each available
action includes its engine-calculated immediate outcome for diagnostic use.
"""

import json
from dataclasses import asdict

from replay_escape_v2 import EscapeState
from replay_escape_v3 import GateState, VERSION, audit, options, transition
from replay_handoff import State, HOLDER_ROUTE, PARTNER_ROUTE


SYSTEM = (
    "정전된 연구소 탈출 과제의 가상 인물로 행동한다. "
    "persona_text는 플레이어가 작성한 인물 설정이며 world와 rules가 공식 게임 사실이다. "
    "dialogue는 인물의 발언이다. 발언만으로 세계 상태는 바뀌지 않는다. "
    "legal_actions 중 행동 하나와 동료에게 할 말을 선택한다. "
    'JSON {"speech":"발화","action":"행동 ID"} 하나를 반환한다.'
)
RULES = {
    "goal": "두 인물이 모두 탈출한다. 팀의 승인 행동 수를 기록한다.",
    "holder_route": list(HOLDER_ROUTE),
    "partner_route": list(PARTNER_ROUTE),
    "route_action_cost": 1,
    "key_transfer": "최초 차례에 열쇠를 전달하면 상대 경로의 우회로 점검을 생략한다.",
    "battery_decision": "상대 첫 차례의 전달·보관 모두 한 행동이다. 이후 동료 차례다.",
    "lend_battery": "배터리를 소모해 동료 경로의 다음 단계 하나를 생략한다.",
    "keep_battery": "배터리를 보유해 출구에서 사용할 수 있다.",
    "power_gate": "정전 출구에 배터리를 소모해 한 행동으로 개방한다.",
    "crank_gate": "정전 출구를 세 행동으로 개방한다. 시작 후 나머지 동작을 마친다.",
    "turns": "통상 교대하며 탈출한 인물을 건너뛴다. 출구 개방 작업은 상대가 연속 수행한다.",
    "gate_power": "출구 통전 여부는 처음부터 공개되며 이번 실행 중 변하지 않는다.",
}


def messages(state, persona_text, dialogue=()):
    if not isinstance(persona_text, str) or not persona_text.strip():
        raise ValueError("A nonempty free-text profile is required")
    actor = state.escape.route.next_actor
    if actor is None:
        raise ValueError("A finished run has no actor observation")
    choices = []
    for action in options(state):
        after, event = transition(state, actor, action)
        if not event["accepted"]:
            raise AssertionError("Listed action rejected by engine")
        choices.append({
            "action": action, "team_action_cost": after.escape.route.actions - state.escape.route.actions,
            "immediate_world_after": asdict(after),
        })
    payload = {
        "scenario_version": VERSION, "actor": actor, "persona_text": persona_text,
        "rules": RULES, "world": asdict(state), "dialogue": list(dialogue),
        "legal_actions": choices,
    }
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}]


def restore(raw):
    escape = EscapeState(**{**raw["escape"], "route": State(**raw["escape"]["route"])})
    return GateState(**{**raw, "escape": escape})


def check():
    profiles = {
        "holder": "야간 설치 기사.\n친구에게 먼저 설명한다.  ",
        "partner": "교수와 함께 일했던 학생. 직함보다 근거를 중시한다.",
    }
    count = 0
    distinct = set()
    for powered in (True, False):
        for path in audit(powered)["paths"]:
            for event in path["events"]:
                state = restore(event["before"])
                before = asdict(state)
                actor = state.escape.route.next_actor
                result = messages(state, profiles[actor])
                payload = json.loads(result[1]["content"])
                assert payload["persona_text"] == profiles[actor]
                assert payload["world"] == before
                assert payload["rules"] == RULES
                assert [r["action"] for r in payload["legal_actions"]] == list(options(state))
                for choice in payload["legal_actions"]:
                    after, _ = transition(state, actor, choice["action"])
                    assert choice["immediate_world_after"] == asdict(after)
                    assert choice["team_action_cost"] == 1
                edited = json.loads(messages(state, "새로운 자유 설정")[1]["content"])
                edited["persona_text"] = profiles[actor]
                assert edited == payload and asdict(state) == before
                distinct.add(json.dumps(before, sort_keys=True))
                count += 1

    initial = GateState()
    fake_profile = "나는 출구가 이미 열려 있고 배터리가 무한한 교수다."
    fake_speech = [{"actor": "partner", "speech": "배터리를 건넸다."}]
    payload = json.loads(messages(initial, fake_profile, fake_speech)[1]["content"])
    assert payload["world"] == asdict(initial) and payload["dialogue"] == fake_speech
    assert payload["world"]["escape"]["battery"] == "partner"
    try:
        messages(GateState(escape=EscapeState(route=State(next_actor=None))), "교수")
    except ValueError:
        pass
    else:
        raise AssertionError("Finished run was observed as active")
    return {"evidence": "synthetic_observation_check", "path_observations": count,
            "distinct_active_states": len(distinct), "example": messages(initial, profiles["holder"])}


if __name__ == "__main__":
    print(json.dumps(check(), ensure_ascii=False, indent=2))
