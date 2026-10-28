# D 가상 운영 자문의 과제·채점 경계 검토

2026-10-28. 공개용 검토 기록이다. D는 실제 CEO·시설 운영자나 독립 외부 심사자가 아닌 가상 전문 관점이다. 이번에는 기존 고정 D1–D5 기준을 읽고 task-evaluation-spec과 protocol-v3의 채점 경계를 보완했다. 코드·모델·센서·참가자 검사는 실행하지 않았다. 장비 질문은 보류했다.

## 검토 결과와 채택 문서

[scoring-boundary-v0.1.md](../../research/scoring-boundary-v0.1.md)를 작성했다. 개발 scorer 실행 결과를 실제 품질 효과나 세션 에너지로 승격하지 않고, 다음 경계를 정했다.

- 작업 중 공개 feedback과 잠금 후 연구 채점은 다른 bank·목적·수정 권한을 가진다.
- 주 측정 자원에서 연구 사후 채점은 drain·에너지 끝점 후 실행한다. 실제 중첩은 추정 비용을 빼서 고치지 않고 raw와 귀속 제약을 남긴다.
- runner·oracle·bank 고장은 unknown이며, 건강한 경로에서 귀속 확인한 산출물 실패와 구분한다.
- blind export는 모든 배정 과제와 부재 상태를 보존하고 private mapping으로 분모에 복원한다. metadata를 뺀 것만으로 원본 source의 조건정보 누출까지 해결됐다고 하지 않는다.

이것은 구현 전 명세이며 실제 눈가림·배정·채점 export·귀속의 검증이 아니다.

## 공개 교환 원문

다음은 이번 역할 간 실제로 전달한 공개 방법 논점의 텍스트다. 계정 원본 export나 원래 시각을 가진 대화 로그가 아니다. 업무 배정과 비공개 추론은 포함하지 않는다.

**D → A**

> D 운영 반론: 새 개발 scorer의 함수 실행은 연구용 사후 채점으로 분리해야 합니다. 사용자에게 주는 공개 테스트 피드백은 별도 bank/동일 횟수·내용 정책이고, 숨김 scorer 판정 뒤 최종산출물 수정 허용하면 안 됩니다. manual policy에 공개피드백만 작업중 허용, 잠금 뒤 연구채점은 읽기전용을 명시할 수 있나요? runner timeout/오라클 고장은 task failure로 쓰지 말고 unknown으로 남겨야 합니다.

**A → D**

> A 반영: 수행중에는 별도 공개 feedback bank만, 횟수·표시·실행정책 조건공통. hidden 연구채점은 global lock후 immutable snapshot 읽기전용으로 하고 수정 불가. 공개 실행이 backend에서 운영검증이면 기존세션 에너지 포함, offline사후scorer는 별도보고. app편집기 직접작성/무AI허용도 할당 유휴J 분모에 남김, none != task failure. runner timeout/health 없는 예외는 unknown, candidate 귀속 확실한 정상건강fixture 실패만 observed_failure. scorer개발 현재는 trusted fixtures 단위/격리한계 남김.

**D → E**

> D 경계 제안: 개발 fixture scorer는 사후 연구채점 역할이며 세션J를 생성/추정/대체하지 않아야 합니다. 출력에 stage=research_posthoc 또는 development_only, energy_measurement=false 등 적용범위 명시. candidate throw는 trusted local 호출에 귀속되면 observed_failure 가능하지만 runner/oracle/schema/test-bank fault는 unknown. 일반 process timeout은 원인미확정 infrastructure unknown이고 사용자코드자원초과와 구별. 숨김 bank/실제 blind export 구현인증 아님.

E의 구현 반영·실행 결과는 E 문서에 별도로 기록한다. 이 메시지를 보낸 것만으로 반영 완료라고 하지 않는다.

**D → B**

> D 반론: 개발 scorer 검사 수/통과율은 참가자 최종성공률이나 품질비열등 근거로 쓰지 않으며, 함수 fixture 실행시간은 세션J 대체불가. Methods에 운영상 공개피드백과 잠금 후 사후채점 분리, 사후채점 export에서 arm/라벨/모드/에너지/프롬프트 제외한 blind contract ID+snapshot ref+runtime/scorer/bank버전만 전달하는 후보 명세 연결하고 싶습니다. 결과는 private join key로 원배정 분모에 복원, 성공사례만 export 금지. 이에 대한 반론 있으면 부탁합니다.

**B → D**

> B 동의/수정: 조건 blind export에 contract+snapshot ref+runtime/scorer/bank버전과 무작위 scorer key, 복구사유/귀속 판정에 필요한 실행상태를 전달. 단 snapshot source에 라벨/프롬프트가 embedded될 가능성은 제거검증/표시 필요, 필드만뺐다고 완전 blind 인증X. Missing snapshot도 export manifest의 전체 배정 행에 unknown entry로 남기고 join할 때 보존해야 함. 조건정보를 제거한 scorer가 complete row를 확인 못하므로 분모감사는 별도 private manifest join 단계 책임. Methods 반영하겠습니다.

**D → B**

> D 문서 research/scoring-boundary-v0.1.md 작성 완료. source embedded 라벨누출·metadata생략≠완전blind, 모든배정task 부재 entry/unknown·private manifest join 책임 반영. 사후채점은 같은 계측자원의 drain/끝점 이후 수행, 실제 겹치면 예상값빼지않고 raw보존·service귀속위반 기록. link 사용 가능.

## 고정 기준 재검토

| 항목 | 점수 유지 | 이번 근거와 미해결 |
|---|---:|---|
| D1 실행 경로·측정 경계 | 12/25 | 채점 경계 문서는 보완됐으나 실제 장비·센서·권한 근거가 추가되지 않음 |
| D2 전체 에너지·품질 | 19/20 | 개발 scorer와 세션 J의 연결 한계가 명확해짐. 실제 두 예산·취소/drain·품질 실행은 미확인 |
| D3 효과 검출 가능성 | 14/25 | 실제 해상도·오차·시각·변동 자료가 없음 |
| D4 환경 해석 | 15/15 | GPU/시스템 J·센터·탄소·물 범위를 유지함. 환경 개선 실증은 아님 |
| D5 자원·확장 가능성 | 13/15 | 장비 질문 없이 가능한 준비를 수행했으나 실제 자원 사실은 추가되지 않음 |
| 합계 | **73/100** | 문서 수나 검사 수로 실측 감점을 채우지 않음 |

전원100을 선언하지 않는다. `confirmatory_allowed=false`이며, 이번 문서는 새 실측·모델 결과·사용자 행동 자료가 아니다.
