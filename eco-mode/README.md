# Eco 모드와 LLM 자원 사용 연구

**같은 낮은 추론 설정을 ‘Eco’라고 부르는 것이 사용자의 선택을 바꾸고, 품질을 유지하면서 실패·재시도까지 포함한 총에너지를 줄이는가?**

혼자 준비하는 연구이다. 지금은 기술·설계 단계이며, 참가자는 사람의 선택 효과를 실제로 검증할 단계에서 검토한다.
해커톤은 범위에 포함하지 않는다.

## 기록

- [우리 대화 기록](conversation/chat.md)
- [수집 범위와 복원 여부](conversation/manifest.json)
- [초기 세 역할 검토의 보존 요약](personas/prior-three-role-reviews.md)
- [A: HCI 교수](personas/A.md)
- [B: HCI 논문 포닥](personas/B.md)
- [C: AI 교수](personas/C.md)
- [D: AI 데이터센터 CEO](personas/D.md)
- [E: AI 데이터센터 개발자](personas/E.md)
- [마지막 교차 검토 정리와 다음 의제](reviews/cross-review-and-next-round.md)

## 연구와 구현

- [연구 주제·질문·계획 v2.1](research/protocol-v2.1.md)
- [선행연구와 공식 문서](research/sources.md)
- [표본 민감도 시나리오](research/power-sensitivity.json)
- [합성 검사 코드](code/validation.js)
- [합성 검사 결과 42/42](code/validation-result.json)
- [검사 실행과 범위 설명](code/README.md)
- [이어가기 상태](state/continuation.md)

## 마지막 완료된 가상 심사

| 역할 | 검토한 안 | 점수 |
|---|---|---:|
| A HCI 교수 | v2 | 90/100 |
| B HCI 논문 포닥 | v2 | 62.5/100 |
| C AI 교수 | v2 | 95/100 |
| D 데이터센터 CEO | v2 | 70/100 |
| E 데이터센터 개발자 | v1 | 설계 86/100, 실행 증거 0/100 |

[기계 판독용 검토 상태](reviews/status.json)

전원 만점에 도달하지 않았다. E의 v2 및 C의 v2.1 재심사는 사용량 제한으로 완료되지 않았다.
E의 v1 실행 점수를 v2 재심사 점수로 표현하지 않는다.
문서 개선, 합성 검사, 실제 장비 계측, 사람의 행동 변화와 환경 개선은 서로 다른 증거이다.

## 보존 범위

현재 접근 가능한 대화와 자문 기록을 모았으며 원문 전사·복원 요약·상태 보고를 구분했다.
일부 이전 자문과 교차 메시지는 전문 원문을 복구하지 못해 요약으로 보존했다.
이 기록은 ChatGPT 계정 전체의 원본 내보내기가 아니다.
이 대화의 이후 턴은 접근 권한과 내용이 제공되는 환경에서 계속 갱신한다. 다른 채팅의 새 메시지를 자동으로 감지하는 연결은 설정되지 않았다.
