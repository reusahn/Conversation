# 연구 준비 코드

## v3 사건·계측·분석 도구

Python3.12.14와 SciPy1.17.0에서 실행했다. requirements.txt에 실제 사용 버전을 보존했다.

- session_replay.py: append-only 사건 재현, 누적counter 총량, 취소→drain, 설정/계측경계·순서 감사, none/unknown 구분.
- analysis_prepare.py: participant_id·전체 할당manifest·전체K 품질·측정경계 확인, bounded 선택/품질 경계, 근사 Welch 에너지.
- synthetic_fixture.py: 모든 수치가 합성인 입력 생성.
- test_research_tools.py: 해시·중복·reset·누락·취소·scope·참가자·품질누락·통계 반례 검사.
- run_checks.py: 검사 실행, 합성 JSON 입출력과 소스 SHA256 보존.

실행 예:

    python run_checks.py
    python session_replay.py fixtures/synthetic-session.json
    python analysis_prepare.py fixtures/synthetic-dataset.json

[최신 결과](results/research-tools.json), [실행 로그](results/tests.txt), [합성 세션 입력](fixtures/synthetic-session.json), [합성 분석 결과](results/synthetic-analysis.json)

기존 v3는57/57 통과했고 A·C·D·E가 당시 소스를 독립 재실행했다. B도 후속 토론에서 같은57개와 동일 소스 해시를 독립 확인했다.
후속 지표 해석 수정의 최신 검사 수·소스 해시는 [최신 결과](results/research-tools.json)에 보존한다. 과거57검사의 독립 확인을 수정된 소스의 새 실행으로 세지 않는다.
2026-10-27 후속 수정에서 필수 반례5개를 추가한 뒤 `python run_checks.py`를 한 번 실행해62/62, 실패0·오류0·종료코드0을 확인했다. 이는 합성 코드 검증이며 실제 모델·센서·사람 실행과 별개다.
B는 수정 후 새5개와 기존 관련3개를 골라8/8 독립 실행하고 해시 불변을 확인했다. B가 수정 후62개 전체를 독립 재현했다고 표시하지 않는다. [독립 확인 범위](../reviews/2026-10-27-d-led/B-final.md)에 기록했다.
A–E가 최초40검사 버전에서 실제 반례를 찾아 수정하고 회귀검사를 추가했다.
합성 주 총량22J=활성17J+잔차5J이며 실제 센서값이 아니다. measured_total_energy_j는null이다.
결함 재현 전/후 검토 버전과 미완료 심사를 reviews/2026-10-27/에 구분해 보존했다.

## 해석과 미구현

이것은 offline JSON 재현·분석 준비 도구이다. UI·실제 모드 API·실제LLM·GPU/벽전력계·센서시각정렬·배정의 진위 인증·사용자 코드 격리는 미구현이다.
해시와 서로 다른 의도budget이 실제 백엔드 적용을 증명하지 않는다.
response_observation은 평탄한 fixture schema helper이며 실제vLLM adapter가 아니다.
provenance/epoch/manifest는 입력선언이며 독립 진위확인 대상이다.
confirmatory_allowed는항상false이다. 수치조건 점검을 실제 연구 효과 판정으로 쓰지 않는다.
전체 올바름을 보장하는 시험이 아니며 실제 사용자/모델/센서 통합 검증은 별도이다.

## 기존 개발 검사 기록

# 합성 엔지니어링 검사

실행: `node validation.js`

보존된 실행 결과는 [validation-result.json](validation-result.json)이다.
부모 실행환경의 JavaScript 런타임 및 Node.js v24.22.1에서 42/42 통과, Node 종료 코드 0을 확인했다.
페르소나들이 모두 파일을 열어 독립 재실행한 것은 아니다. 실행환경의 접근 실패와 사용량 제한은 각 자문 기록에 남겼다.

## 무엇을 검사했는가

- 네 개발 과제의 참조 함수: 각 6개 사례, 총 24개 검사.
- 의도적으로 잘못된 구현을 테스트가 검출하는지: 4개 검사.
- 합성 세션 집계·중복·누락·리셋·중첩·실패·포기·취소·추정 구분 등의 검사: 14개.
- 자료에 들어 있는 모든 에너지 수치는 합성 예시이다. 실제 GPU·외부 전력계 값이 아니다.

결과의 `measurement_valid` 및 `measured_fixture` 같은 내부 필드는 합성 자료 안에서 집계 규칙이 성립하는지를 뜻한다.
이 명칭을 실제 계측 수행 증거로 읽어서는 안 된다.
재시도 예제의 12 J 역시 가상 숫자이다.

## 구현하지 않은 것

UI·브라우저 실험, 실제 LLM 추론, 저/고 추론 예산 제어, GPU/외부 계측기, 실제 세션 누적 카운터,
프로덕션 설정 해시, 센서 시각 정렬, 최종 사건 상태 기계, 사용자 코드 격리 실행은 구현·검증하지 않았다.

현재 집계 함수 검사는 연구안의 주 지표인 실제 세션 시작/종료 누적 카운터를 완성한 구현이 아니다.
참조 과제는 실제 사람·모델의 쉬움/어려움을 검증한 과제집이 아니다.
검사 통과는 사람의 선택 효과, 실제 에너지 절감, 품질 유지 또는 환경 개선을 뜻하지 않는다.


## 제출·과제·실행 시도의 지표

`task_id`는 사전 배정된 과제이다. 기존 `request_id`가 서버가 수락한 한 번의 **논리 제출**을 식별한다. 사용자 재질문·재생성·모드 변경 후 재제출은 같은 과제여도 새 `request_id`를 사용한다.
`attempt_id`는 그 제출을 실행하는 개별 백엔드 시도이며 `attempt_start.request_id`로 연결한다. 같은 제출을 다시 실행하는 추가 attempt는 같은 `request_id`와 새 `attempt_id`를 쓰고 새 `request_submitted`를 만들지 않는다. 별도의 `logical_request_id` 필드는 도입하지 않았다.
ID의 유일성·참조·사건 순서를 검사하지만 실제 서버가 이 의미대로 ID를 발급했다는 진위는 입력 로그만으로 인증하지 않는다.

| 출력 필드 | 집계 단위와 의미 |
|---|---|
| `additional_requests` | 호환성을 위한 기존 감사 전 계수. 세션 첫 제출 이후의 추가 제출 수이며, 다른 과제의 최초 제출도 포함한다. 과제 재시도 수가 아니다. |
| `mode_switches` | 호환성을 위한 기존 감사 전 계수. 세션에서 인접한 제출 간 low/high 변경 수이며, 과제가 달라도 센다. 같은 과제의 상향 전환 수가 아니다. |
| `session_adjacent_mode_changes` | 의미 감사가 유효할 때의 세션 인접 제출 모드변경 수. 정상 로그에서 기존 `mode_switches`와 같다. |
| `within_task_mode_switches` | 각 과제의 제출만 시간순으로 모아 인접 모드변경을 세고 과제 전체에서 합한 수. 사이에 낀 다른 과제는 비교에서 건너뛴다. |
| `within_task_low_to_high` | 같은 과제의 인접 제출에서 low→high인 경우만 합한 수. 첫 제출이 high이면 상향 전환으로 세지 않는다. |
| `within_task_additional_submissions` | 각 과제에서 첫 제출 이후의 제출 수를 합한 값. 같은 모드의 재제출도 포함하며 실행 attempt 수와 다르다. |
| `within_request_additional_attempts` | 각 논리 제출에서 첫 실행 attempt 이후의 수를 합한 값. 추가 실행이라는 구조적 계수이며 실패 원인·재실행 이유·사용자 의도를 증명하지 않는다. |

예를 들어 T01-low→T02-high는 세션 모드변경1·같은 과제 상향전환0·과제 내 추가제출0이다. T01-low→T01-high는 같은 과제 모드변경1·상향전환1·추가제출1이다. T01-low→T01-low는 모드변경0·추가제출1이다. 하나의 `request_id`에 두 `attempt_id`가 있으면 과제 내 추가제출0·추가 attempt1이다.

새 유효 지표5개는 `protocol_observation_valid=false`이면 모두 `null`이다. 감사 전 파서가 보존한 request/attempt 기록의 계수는 `raw_event_metrics`에 남기고, 기존 `mode_switches`·`additional_requests` 값도 보존한다. 이 원시 계수는 잘못되거나 불완전한 사건으로도 계산될 수 있으므로 유효한 행동 결과로 쓰지 않는다. 이벤트 ID 중복 제거 뒤 request/attempt ID별로 보존한 기록을 세며, ID 충돌이 있으면 `issues`와 원본 사건을 함께 확인해야 한다.
`metric_definitions`에 출력 자체의 정의와 유효성 규칙을 포함했다. 기존 출력 필드를 삭제하거나 의미를 바꾸지 않는 추가 필드이며, 이 보완은 실제 사용자·모델·센서 검증이나 고정 심사점수 재평가가 아니다.
E의 설계97/실행50은 수정 전 v3 소스에 대한 마지막 완료 평가이다. 이 후속 수정 소스의 재평가 점수로 표시하지 않는다.
