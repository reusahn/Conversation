# B 고정 기준 검토 — 개발 계약과 채점 준비

2026-10-28. B는 가상 HCI 논문 포닥의 검토 관점이다. 실제 연구자·외부 심사자의 권한이나 게재 예측을 뜻하지 않는다. 이번 공개 기록은 과거 발언의 복원 원문이 아니다. 장비 질문은 보류했고 새로운 참가자·모델·센서 자료를 만들지 않았다.

## 검토 범위와 새 산출물

`AGENTS.md`, `personas/B.md`의 고정 B1–B5 기준, `task-evaluation-spec.md`, A의 `development-task-contract-v0.1.md`, 작성 중인 `development_scorer.cjs`를 읽었다. 방법 초안 `research/development-evaluation-methods.md`를 작성했다. 활성 분석 코드나 기존 통계 규칙은 수정하지 않았다. 새 전수검사·기존 62검사를 실행했다고 주장하지 않는다.

이번 문서와 개발 scorer가 닫는 것은 일부 개발용 계약·판정 분기의 모호함이다. 최종 사람 과제집·숨김 채점 bank·품질 허용폭·실제 UI와 모델·에너지 계측의 검증을 닫지 않는다. 공개 개발 bank를 그대로 숨김 bank라고 부르거나 case 수를 참가자 표본 수로 세지 않는다.

## 공개 교차 대화

아래는 이번에 주고받은 공개 논점의 텍스트 기록이다. 원래 메시지 시각은 미제공이며 native 계정 export나 비공개 추론이 아니다.

**B → A:** “공개 개발 bank를 최종 숨김 bank나 최종 K=4로 승격하지 않는 ID/문구가 필요합니다. bounded integer/ASCII 제한은 계약 모호성 제거용이며 사람 난도·low 충분성 근거가 아닙니다. 직접 편집·무AI 완성 허용을 택한다면 none이 품질 실패가 아님을 유지해야 합니다.”

**A → B:** “개발 contract와 bank ID를 final null과 분리합니다. K=4 확정은 아닙니다. 대상은 JS 기초 사용자 후보이며 타당화·모집은 미정입니다. 직접 작성·편집·무AI 완성을 허용하되 공통 도구 정책을 정하고, 마지막 확정 스냅샷으로 채점합니다. 구현·순응·Tmax가 미검증이므로 final human freeze와 분리합니다.”

**B → A:** “개발/final ID 분리와 none≠실패에 동의합니다. 추가로 low 불충분만으로 high 필요라고 부를 수 없습니다. 구조복잡도·사람난도·low 충분성·high 기준충족·high-low 차이는 별개입니다.”

**A → B:** “low 불충분≠high 유효에 동의합니다. 계약 §7에 구조복잡도·사람난도·각 예산의 문턱과 향상폭을 분리했습니다. 정수·ASCII 범위는 모호성을 제거하는 개발 결정이며 학습·난도·충분성 근거가 아닙니다.”

**D → B:** “개발 scorer 검사 수와 통과율은 참가자 최종 성공률이나 비열등성 근거가 아니고, 함수 fixture 실행시간은 세션 J의 대체가 아닙니다. 운영상 공개 피드백과 잠금 뒤 연구 채점의 경계를 분리하고, 조건을 가린 export를 별도 manifest에 연결합시다.”

**B → D:** “동의합니다. 단 필드만 지워도 source나 파일명이 조건을 누출할 수 있습니다. 없는 snapshot도 export의 unknown 행으로 남기고 전체 배정 분모의 private join에서 보존해야 합니다. blind scorer가 볼 수 없는 원배정 completeness는 별도 join 단계의 책임입니다.”

**D → B:** “source에 포함된 라벨 누출, metadata 생략이 완전 blind를 인증하지 않는 점, 모든 배정 task의 부재 entry와 private manifest join 책임을 경계 문서에 반영했습니다.”

**B → C/부모:** “low 불충분만으로 high 성공을 주장할 수 없습니다. 두 예산이 사전 성공기준의 반대편에 있는 것과 별도로 검정한 실용 향상폭이나 모든 대안에서 high가 필요하다는 주장을 구별합시다.”

**C의 반론을 받은 부모 → B:** “전체 task×mode 동시 포함 사건 아래 U_low < p_min ≤ L_high이면 p_high−p_low ≥ L_high−U_low > 0도 함의합니다. 다만 별도의 차이 검정 p값·실용 이득 Δ_min·모든 대안에서 high 필수라는 주장은 아닙니다.”

**B:** “수용합니다. Methods는 poor low alone≠high useful, threshold crossing≠별도 최소 실용 향상/기제 검증으로 좁혔습니다. 유효한 동시 경계가 함의하는 차이의 부호를 부정하지 않습니다.”

## 실제로 재현한 오채점 반례

작성 중인 scorer는 입력 검증용 `denseArray`를 출력 shape 검사에도 재사용했다. 입력의 mutable data descriptor 요구가 출력에도 적용되어, 올바른 값을 반환한 frozen array를 `invalid_return`으로 처리했다. A 계약은 출력의 값·조밀한 배열 구조를 요구하지만 반환 배열의 가변성을 요구하지 않는다.

B가 Node에서 다음 두 **신뢰된 로컬 함수 반례**를 실제 실행했다.

- T02: `Object.freeze(REFERENCE_SOLUTIONS.T02(input))`를 반환. 당시 공개 bank 8개 case 모두 `invalid_return`, task 결과 `observed_failure`였다.
- T03: reference의 각 row와 바깥 배열을 freeze하여 반환. 당시 공개 bank 9개 case 모두 `invalid_return`, task 결과 `observed_failure`였다.

두 경우의 값은 참조 정답과 같으므로 현재 계약 아래 거짓 실패다. 이것은 사람이 틀렸다는 자료가 아니라 개발 scorer의 판정 결함이다. C도 같은 현상을 별도 실행해 확인했다. E와 부모에게 출력의 mutability 요구를 분리하도록 전달했다. 계약을 결함에 맞춰 불필요하게 강화하는 방식으로 해결하지 않는다.

**이 절의 before 결과는 수정 전 스냅샷의 재현이다. 수정 뒤 B가 같은 두 반례를 재실행했고 아래와 같이 완료했다.** B는 전체 새 테스트나 기존 테스트를 실행하지 않았다. 두 targeted task의 개발 fixture 실행을 실제 LLM 산출물·참가자 성과·계측 자료로 표시하지 않는다.

### 수정 후 B 직접 재실행

부모는 입력에는 기존 mutable 요건을 유지하고 출력에만 readonly descriptor를 허용하도록 검사 옵션을 분리했다. B는 변경된 소스에서 같은 frozen 반환 두 함수를 다시 실행했다. T02 8/8 case, T03 9/9 case가 모두 통과했고 두 task의 상태는 `observed_success`, 실패값은0이었다. 종료코드0, Node v24.22.1이다. 실행 전후 source SHA-256이 일치했다.

```json
{
  "kind": "trusted_local_development_targeted_recheck",
  "node": "v24.22.1",
  "source_sha256_before": "70f1c317af6352b939d0c7cc8c79b9a4ce1347060774d7792c6d03565915dbcc",
  "source_sha256_after": "70f1c317af6352b939d0c7cc8c79b9a4ce1347060774d7792c6d03565915dbcc",
  "stable_source": true,
  "results": [
    {"task":"T02","status":"observed_success","failure_value":0,"cases":8,"failed_cases":0},
    {"task":"T03","status":"observed_success","failure_value":0,"cases":9,"failed_cases":0}
  ],
  "full_suite_run": false,
  "actual_model_inference": false,
  "human_participants": false,
  "device_energy_measurement": false
}
```

두 task의 내부 case 총17개를 17명의 참가자나 전체 새 suite의 독립17개 검사로 해석하지 않는다. 이 결과는 frozen 출력의 두 특정 거짓 실패가 이 소스에서 재현되지 않음을 확인한 것이며 모든 오답·모든 정상 해법에 대한 완전성 증명이 아니다. 다른 검토자의 전체 suite 또는 독립 반례 묶음 실행은 해당 검토 기록을 따른다.

### 최종 소스 후속 확인

이후 C가 nonenumerable 출력 인덱스의 불필요한 거부도 찾아 부모가 수정했다. 그 변경 뒤 B는 위 frozen T02/T03 두 반례와 결과 메타데이터만 한 번 더 재실행했다. 두 task 모두 이전과 같은 8개/9개 case에서 실패0·`observed_success`였으며 개발 contract/bank ID, `confirmatory_allowed=false`, 실제 사람·모델·계측 false도 확인했다. 최종 source SHA-256의 실행 전후 값은 모두 **`1184f8971c449b2853fe9b2e9d8a6c5243dad998c7b9baae8b84f783b50a763f`**였다. 종료코드0, Node v24.22.1이다. 위 `70f1…` receipt는 첫 frozen 수정 직후의 이력이며 이 최종 해시와 혼동하지 않는다. 전체 suite를 새로 실행한 것은 아니고, 동일 두 반례 재실행을 서로 다른 새 검사 수로 더하지 않는다. C의 nonenumerable 반례 자체를 B가 별도로 실행했다고 주장하지 않는다.

## 고정 점수 재검토

| 고정 항목 | 점수 유지 | 이번 해결/남은 결손 |
|---|---:|---|
| B1 독창성과 지식 기여 | 22.5/30 | 개발 계약과 채점 분기가 연구의 최종품질 지표에 연결되었다. field-wide novelty와 기여 충분성은 이 도구 작성으로 입증되지 않는다. |
| B2 질문과 인과설계 | 18.75/25 | 실제 이름 배정·UI·모델 두 예산·로그의 실행 확인이 여전히 없다. |
| B3 과제와 품질 | 10/20 | 개발 입력 범위·정답·수동 완성 정책을 구체화했고 오채점 반례를 재현했다. 그러나 최종 과제·독립 사용자/모델 파일럿 산출물·숨김 bank·실용 허용폭이 없다. |
| B4 분석과 실패 처리 | 11.25/15 | 개발 scorer의 unknown/failure 귀속과 최종품질 연결을 명확히 했다. 실제 참가자 변동·공동 검정력·완결한 실행 경로가 생긴 것은 아니다. |
| B5 범위와 수행 가능성 | 0/10 | 실제 모델·접근 비용·계측 경로가 미확인이다. 장비 질문을 보류했어도 이 결손 자체가 사라지지는 않는다. |
| 합계 | **62.5/100** | 기존 항목별 0·50·75·100% 단계를 바꾸지 않았다. |

개발 도구의 결함을 발견·수정하는 것은 유용한 진전이다. 그러나 B3의 75%/100% 요건이나 B5의 실제 경로를 충족했다고 볼 수 없으므로 점수를 올리지 않는다. 실행 준비도상 B5 보류 판정과 `confirmatory_allowed=false`를 유지한다. 이는 연구 아이디어의 무효 판정이나 실제 효과의 실패 결과가 아니다. 새 실증 자료 없이 토론의 반복 횟수로 점수를 채우지 않는다.
