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

현재57/57 통과. A·C·D·E가 최종본을 독립 재실행했다. A–E가 최초40검사 버전에서 실제 반례를 찾아 수정하고 회귀검사를 추가했다.
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


additional_requests는 세션 첫 요청 이후의 추가 제출 수이다. 다른 과제의 최초 제출도 포함하므로 과제별 재시도 수와 동일 지표로 보고하지 않는다.
