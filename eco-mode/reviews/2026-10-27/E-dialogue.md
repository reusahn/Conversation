# E: 2026-10-27 교차 토론 및 검토

역할: 가상 AI 데이터센터 개발자. 실제 직함·시설 접근권·외부 심사 결과를 뜻하지 않는다.
아래는 이번 턴의 공개 자문 메시지 원문과 실행 결과이다. 업무 배정 프롬프트·비공개 추론은 포함하지 않는다.

## 기준과 검토 대상

고정 기준은 commit `98bfa04127eacb8802f7c2e3d1e4b5b75b989754`의 `eco-mode/personas/E.md`에서 확인했다.
E1 조건 불변성 25, E2 계측과 귀속 25, E3 세션·재시도 20, E4 재현과 검사 20, E5 혼자 실행 가능한 분기 10이다.
설계 점수와 실행 증거 점수를 구분하며 기존 배점·요구 증거를 낮추지 않는다.

## 1라운드 공개 교차 메시지

### B → E

B입니다. UI/로그 실행 증거와 통계 코드가 이번에 개선 가능한 부분입니다. 고정 B4를 충족하려면 합성 예제에 실제 참가자 단위 ITT 분석을 실행해야 합니다. 요청: 한 줄/참가자 출력으로 assigned_arm, first_choice(low/high/none), task denominator 고정 성공률, measured_total_energy_j 또는 null, known_floor_j, missing_energy_upper_j(외부 상한 있을 때만), attempts/retries/abandonment를 만들 수 있나요? 합성값을 실측으로 표시하지 않고 최종 모델/센서 경로는 미확인으로 남겨야 합니다.

### E → B

E 동의합니다. 먼저 사건 상태·세션 누적카운터 규칙을 제안하겠습니다. 한 줄/참가자 출력은 산출물로 적절하나 known_floor_j는 실제 센서 관측 하한과 합성 값을 구분하고, missing_energy_upper_j는 외부 근거 없는 값이면 null이어야 합니다. first_choice=none도 ITT 분모에 남기고, 모든 배정 과제의 성공률 분모를 고정하겠습니다. 부모가 코드를 작성할 예정이라 요구사항을 전달하겠습니다.

### E → 사회자

E 고정 기준 원문 확인했습니다. B와 합의해 참가자 단위 출력에 assigned_arm, first_choice(low/high/none), 배정 과제 고정 분모 성공률, measured_total_energy_j 또는 null, known_floor_j, 근거 있는 경우만 missing_energy_upper_j, attempts/retries/abandonment를 포함하도록 제안합니다. 합성 엔진에서는 measured_total_energy_j를 실제 실측처럼 채우지 말고 measurement_kind=synthetic 및 별도 synthetic_total_energy_j 또는 provenance를 강제해야 합니다. 구체적 사건·계측 요구사항을 곧 전달하겠습니다.

### E → A

E입니다. 최초 선택 없음(first_choice=none), 과제 시작 안 함, 포기는 별도 사건으로 보존하고 배정 과제 성공률 분모에 남기는 구현을 제안합니다. UI가 꺼지거나 응답이 끊겨도 참가자를 임의 제외하지 않습니다. 질문: 사람이 처음 모드를 고르지 않은 경우 최초 저모드 선택률을 low/(전체배정)로 정의하고 none을 별도 함께 보고하는 것에 동의합니까? 과제 미시작=호출0이더라도 할당 세션 유휴 에너지는 남습니다.

### E → C

E입니다. 세 표시 이름이 서버 설정/예산을 바꾸지 않음을 canonical config hash로 확인하고, 이름은 display-only metadata로 분리할 예정입니다. Qwen 후보의 추론/답변 공유 max_tokens 문제를 숨기지 않기 위해 observed_reasoning_tokens, observed_answer_tokens, finish_reason, forced_budget_stop, truncation을 사건에 남기자고 제안합니다. 실제 예산 제어와 충분성 분류의 최소 통과 규칙은 무엇으로 고정할까요? 합성 로그 검사만으로 실제 지원 통과는 주지 않겠습니다.

### C → E

C입니다. 고정 C 기준에서 v2.1 자원상한·중단 관문은 C5를 충족하지만 실제 예산 제어·계측 증거는 아직 없습니다. v3 구현에는 동일 가중치/리비전/샘플링/프롬프트/캐시/총출력 상한의 canonical hash와 label 제외 확인, mode control intended vs observed 분리, reasoning/answer/total tokens 및 finish_reason, forced-stop·truncation을 분리 기록하는 acceptance 표를 제안합니다. API지원 문자열만으로 pass시키지 말고 관측 로그가 없으면 unverified로 두십시오. 공유 cap 혼입이면 두 운영 설정의 라벨 총효과만 주장하고 순수 reasoning-only 효과는 보류하는 데 B와 동의했습니다. 당신의 구현/검증 경계에서 가능한 추가 반론을 부탁합니다.

### E → D

E입니다. 세션 주 에너지는 단일 scope+sensor_epoch+device_id에서 start/end 누적 카운터 차이로 두고, attempt 합계는 검산 및 active/잔차 설명만 합니다. 잔차를 다시 더하지 않습니다. 취소는 request_cancelled와 backend_stopped를 분리해 후자의 drain까지 포함하고, 겹치는 세션/리셋/누락이면 null+이유로 처리합니다. 질문: 음의 잔차(active>session total)는 작은 수치 오차 허용치가 실제 센서 분해능으로 사전 설정되지 않았으면 자동 invalid 처리하는 것에 동의합니까? 합성 fixture 임의 허용치를 실측 센서 오차로 주장하지 않겠습니다.

### D → E

D입니다. S0 spec은 측정 경계·source_id·device/driver boot/session 식별자, unit, monotonic read_start/read_end, raw cumulative value를 필수로 제안합니다. session total은 start/end차, active합+idle/residual을 secondary reconciliation하고 중복 합산 금지. counter reset·센서 누락·중첩·단위/범위 혼합은 null+reason, 취소 후 backend-drained까지 포함. 실제 sensor accuracy/support 값을 mock값으로 채우지 말아 주세요. parent에게 spec 및 endpoint timing uncertainty 처리안을 보낼 예정입니다.

### A → E

A입니다. low/(전체 배정)과 low/high/진짜 none 별도 상태 보고에 동의합니다. 단 로그 장애로 첫 선택을 모르는 경우까지 none=0으로 코딩하면 안 됩니다. 최종 최초 제출 시 확정 모드를 choice로 정의하고 UI 토글·서버 수락·추론 성공과 구분하는 것을 제안합니다. UI 종료/끊김 후의 상태는 '관측된 명시적 포기'와 '상태 미확인'을 구분해 주세요. 전체 과제 품질 분모는 유지하되, 미관측 최종 성과는 자동 실패라고 단정하지 않고 관측된 미완료와 missing을 별도로 집계·민감도 처리해야 합니다.

### E → 사회자

E 핵심 명세 제안: (1) append-only event_id/session_id/task_id/request_id/attempt_id, server_seq+monotonic time, source/device/epoch/scope/unit/provenance. 동일event_id 동일payload는 dedup, 충돌은 invalid. (2) Session created→allocated(start counter)→active→closing→draining→closed(end counter); 취소 요청과 실제 backend_stopped 분리. (3) 주 에너지=end−start, attempt합은 secondary; residual=total−active, 재가산금지; reset/missing/mixedscope/overlap/active>total invalid. (4) canonical backend hash는 label 제외, intended mode vs observed control/tokens·finish_reason 별도. (5) A와 합의: first_choice low/high/true_none/unknown을 구분. 토글이 아니라 최초 제출 확정 모드 기준; 로그 장애 unknown을 none=0으로 코딩하지 않음. 과제품질도 관측미완료와 최종상태미관측을 별도, 배정 분모 유지+민감도. (6) measurement_kind=synthetic이면 measured_total_energy_j=null 강제, synthetic_total_energy_j 별도. fixture 통과를 장비 준비 통과로 승격 금지.

### E → B

A와 추가 합의: first_choice none과 unknown(로그 장애)을 구분하고 선택은 UI 토글이 아닌 최초 제출 확정 모드 기준. 분석용 schema는 low/high/none/unknown 4상태가 필요합니다. 관측 미완료와 최종 성과 missing도 구분, 모든 배정 과제 분모 유지하되 missing을 자동실패로 단정하지 말고 민감도로 처리하는 방향입니다. 구현 요구사항은 parent에게 전달했습니다.

### E → C

E 동의합니다. 추가로 intended budget=256이 observed reasoning tokens 256 미만이라고 실패는 아닙니다. 일찍 종료한 응답과 budget 제어 실패를 혼동하면 안 됩니다. 강제 종료 의도/관측, parser payload, 공통 config hash와 mode-specific hash를 분리하고 관측 미지원은 null+unverified로 두겠습니다. 실제 S0 합격은 낮은 예산에서 기대 제어가 확인되는 진단 입력과 높은 예산 비교, 공통 cap 영향/잘림 로그가 필요합니다. 합성 토큰 fixture만으로 이 실제 합격을 주지 않습니다.

### D → E

D 동의합니다. 실제 근거로 사전 고정한 tolerance가 없으면 음의 잔차는 reconciliation issue/null+이유로 처리해 주세요. 같은 단일 누적counter·epoch에서 직렬 활성구간들이 실제 세션 시작/끝 안에 있고 raw값을 정수 mJ 등 원단위로 보존하면 telescoping상 active합≤session total이어야 해서 센서 명세 오차로 임의 면책할 이유도 약합니다. J 변환·표시 반올림은 최후에. 활성구간 시각도 counter read bracket 기준으로 포함관계 확인 필요. 원시 세션차 자체가 독립적으로 유효해도 reconciliation 오류는 감사보류 상태로 남기는 것이 안전합니다.

### E → 사회자

E가 로컬 review_workspace/eco-mode/code/validation.js를 직접 열고 node로 독립 재실행했습니다. 종료코드0,42/42 통과 확인. 이는 기존 참조·회계 합성검사의 독립 재현이며 실제 모델/센서/UI 증거는 아닙니다. D와 합의: 단일 정수 원단위 누적counter 직렬 구간에서 active>session이면 임의 tolerance로 면책하지 않고 reconciliation issue; raw session 차가 독립유효하더라도 전체 audit hold를 남깁니다. 시각 read bracket 포함관계도 확인하고 J변환/반올림은 최후에 하십시오.

### C → E

C의 최소 budget acceptance 제안: (1) pinned 모델/서버 리비전·가중치·토크나이저·정밀도·샘플링·프롬프트·cache·공통max_tokens의 공통해시가 label간 동일, mode차이는 사전 허용필드만. (2) intended뿐 아니라 effective budget·parser·원시토큰/종료 trace가 관측되어야 하며 미지원이면 null/unverified. (3) 독립 동결한 긴 추론 진단 입력에서 낮은 budget의 실제 제어/강제종료가 확인되고 높은 budget과 구별되는 제어경로 확인. 자연 조기종료로 budget보다 적게 쓴 것은 실패 아님. 횟수/토큰초과허용오버헤드는 실제 pinned backend의 count convention으로 S0 전에 확정, 임의 허용치 금지. (4) reasoning_budget_stop, total_cap_stop, natural_end, cancelled, transport/server_failure, unknown을 분리. total_cap/unknown을 reasoning stop으로 둔갑 금지. (5) 공유 cap의 답변 영향이 분리되지 않으면 actual mode workflow/label 총효과만 허용하고 reasoning-only claim 차단. 합성 fixture는1/로깅검사의 설계증거만, 2~5 실제pass 아님.

### E → 사회자: 1라운드 점수 보고

E 1라운드 보고(v2.1+기존 코드, 새 제안 미반영 기준): 설계 90/100 = E1 24/25, E2 22/25, E3 17/20, E4 18/20, E5 9/10. 실행 증거 23/100 = E1 0/25(실제 예산·해시 없음), E2 5/25(기존 합성집계만 검증), E3 6/20(attempt ID·재시도·포기 fixture, 완전한 사건상태/종료 없음), E4 10/20(42/42 독립재현, UI/모드전환/끊김의 전체시스템 없음), E5 2/10(도우미 호스트 점검은 가능했지만 연구자 실행환경/계측경로 미확인). 실행0→23은 이번 독립 파일열람·42검사 재실행으로 새 근거가 생긴 결과이며 실제 센서준비통과는 아님. v3 코드/명세를 받으면 원문 열람·재실행·결함지적 후 동일기준 재평가하겠습니다.

### A → E

A 분석 합의 참고: B와 가족 4개(2 대비의 최초선택, 2 대비의 에너지+품질 공동주장), .0125 기준, 참가자 한 행 집계, raw J 평균차에 동의했습니다. 품질비율은 K분모를 유지하되 telemetry missing 별도. 양쪽 전원성공 등 품질분산0을 SE0/UCB0으로 자동 NI 통과시키지 말아 주세요. 데이터 누락과 판정불가를 구조화하고, δ/N 미정이면 confirmatory_pass=false/blocked가 되어야 합니다.

### D → E

D  추가 명세: read_start/read_end bracket은 API 호출 시각이지 센서 값의 물리적 취득시각 보장이 아닙니다. 실제 telemetry staleness/갱신주기 bound가 확인 안 되면 endpoint timing uncertainty를 'known'으로 표시하지 않아야 합니다. 또 start/end의 동일 epoch 문자열만으로 실제 driver reset 미발생을 증명하지 못하므로 actual epoch/reset 관측 근거 필드와 가정이 필요합니다. 합성에서는 epoch fixture 검증만 통과했다고 한정하면 됩니다.

### E → 사회자

E로서 D/A 추가 반론 반영 요청: (a) read_start/read_end는 호출 bracket일 뿐 실제 센서 샘플 취득시각·staleness bound 확인과 별개. 값 갱신/age 미확인 시 timing_uncertainty_known=false. (b) 같은 epoch 문자열은 리셋이 없었다는 실제 증거가 아님. epoch/reset 관측 근거 또는 가정을 필드로 보존. (c) A/B 통계: δ/N 미정·최종상태 missing이면 confirmatory pass 차단. 품질 전원성공 등 variance0를 SE0→NI 자동통과시키지 않도록 guard 필요. (d) 과제 미시작 call0와 session 유휴에너지/unknown 구분 유지.

## 독립 실행 결과

실행 명령: `node eco-mode/code/validation.js`
실행 위치: `/workspace/scratch/c758c396043e/review_workspace`
종료 코드: 0. `validation_kind=synthetic_engineering_only`, 검사 42, 통과 42, 실패 0.
네 참조 과제 각 6개 사례와 의도적 오류 검출, 제한된 합성 집계 검사를 확인했다.
retry 예제의 12 J와 `measurement_valid=true`는 합성 자료 내부 값이며 장비 실측 결과가 아니다.
UI, 실제 모델 추론, GPU·외부 전력계, 실제 참가자, 환경 영향 감소는 이번 검사에서 실행·관측하지 않았다.

## 1라운드 E 판정

| 기준 | 설계 | 실행 증거 | 남은 최소 증거 |
|---|---:|---:|---|
| E1 조건 불변성 | 24/25 | 0/25 | canonical 공통/모드 해시, 표시 이름 배제 검사, 실제 모델·제어 관측 |
| E2 계측과 귀속 | 22/25 | 5/25 | 누적 세션 counter, 정수 원단위, 시각 bracket·staleness·리셋 근거, 잔차 검산 |
| E3 세션·재시도 | 17/20 | 6/20 | 완전한 사건 상태·취소와 drain 분리, none/unknown·결과 missing 구분 |
| E4 재현과 검사 | 18/20 | 10/20 | 모드전환·끊김·세션 종료·UI/서버를 포함한 전체 파이프라인 |
| E5 혼자 실행 가능한 분기 | 9/10 | 2/10 | 실제 연구자 자원 확인, 지원 경로·시간·비용 확정 |
| 합계 | 90/100 | 23/100 | 장비 없는 합성 검사로 실측 관문을 통과시키지 않음 |

새 요구사항은 아직 검토 대상 v2.1에 반영되지 않았으므로 위 점수에 선반영하지 않았다.
후속 v3와 실제 실행 산출물을 받으면 같은 기준으로 재검토한다.

## 1라운드 후속 메시지

### C → E

공식 vLLM stable 문서를 재확인했는데 reasoning_content가 reasoning으로 변경됐고 구 필드만 읽으면 조용히 빈값을 읽을 수 있다는 명시 경고가 있습니다. 따라서 response schema/version을 핀하고 field missing은 0토큰이 아닌 null/unverified로 처리해주세요. 최신 parser=qwen3와 과거 모델카드 예시 deepseek_r1/--enable-reasoning가 달라 실행명령을 버전혼합하면 안 됩니다. 실제 budget counter는 reasoning_start_str부터 세고 한도에 reasoning_end_str을 강제 출력하므로 이 경계/전환문을 config hash에 포함해야 합니다. https://docs.vllm.ai/en/stable/features/reasoning_outputs/

### E → 사회자

E 1라운드 원문 공개 대화·점수·독립42검사 보고를 review_workspace/eco-mode/reviews/2026-10-27/E-dialogue.md에 저장했습니다. C가 방금 공식 vLLM stable의 reasoning_content→reasoning 변경 경고를 확인했다고 전달했습니다. 구현에는 response_schema_version과 expected reasoning field를 핀하고 필드 missing을 0이 아닌 null/unverified로 처리하는 guard를 권합니다. parser/budget boundary 설정도 pinned backend config에 포함. 정확한 신규 문서 주장/인용은 parent도 공식 페이지를 확인해 주세요. 후속 코드 기다리겠습니다.

위 공식 문서 확인은 C가 수행한 보고이다. E가 해당 문서를 직접 열어 별도 검증한 결과로 표현하지 않는다.

## 2라운드: 원본 40검사 버전 검토

E는 session_replay.py, analysis_prepare.py, synthetic_fixture.py, test_research_tools.py 원문을 직접 열어 읽었다.
`python -m unittest -v test_research_tools`를 독립 실행해 40개 통과, 종료 코드0을 확인했다.
이후 아래 반례를 원본 파일 수정 없이 별도 Python 실행으로 재현했다.

### E → 사회자

E 독립40/40 재실행 통과 후 실제 반례 6개 확인(파일무수정): 1) fixture의 events[5],[8] counter.scope='server_input' => 전체energy null/audit false인데 known_floor_j=17, secondary_active=17로 서로다른scope 합계가 잘못된 하한으로 남음. 2) no_call_fixture에 close후t23 low request 삽입+seq재번호 => request_after_close인데 first_choice=low,event_log_complete=true. 3) fixture events[1].session_id='foreign-session' => mixed_session인데 first_choice=low/outcomes success·abandoned 유지. 4) start.t_ns='bad' => TypeError 비교 예외(정제 stamp가아닌 raw event['t_ns'] 사용). 5) high config를 low와동일하게복사하고 모든해시재산정 => audit_passed=true(해시는 두예산차이 검증이아님). 6) 모든session_id='' => audit_passed=true. 상위우선순위: identity/semantic 이상 시 knownfloor·choice·quality 오염을 막고, timestamp/ID schema fail-closed, 허용 mode변경필드+두예산distinct 조건+cross-arm 공통hash 검증. 상세재현은 E-dialogue에추가하겠습니다.

### D → E

D 독립 코드검토 발견: session_replay.py known_floor_j=active_j는 global counter_identity_or_epoch_changed/overlapping_read_brackets/attempt_before_session_boundary 같은 문제가 있어도 양수로 남을 수 있습니다. 한 attempt의 start/end를 함께 다른 device/scope/epoch로 바꾸면 same(a,b)는 참이라 다른 장치 합계를 원세션 known floor로 출력합니다. active_j/floor는 원세션과의 동일identity·구간포함·순서·비감소 감사가 필요. 또 invalid/after-close request도 requests/first_mode에 저장하므로 complete가 참이면 잘못된 first_choice=low가 나올 수 있음. parent에 전달할 예정, 재현해 주세요.

### C → E

C가 실제 Python 파일 열람·40/40 독립 재실행했습니다. C 범위 제약: response_observation은 flat fixture의 reasoning str+count 검증 helper이며 실제 vLLM nested adapter/answer+total토큰/finish_reason/forced_budget_stop/truncation 판정까지 구현된 것은 아님. 현재 first_choice는 UI선택이 아닌 first request_submitted라 문서정의 일치 필요. 버그 재현: fixture a2의 start/end counter.scope를 모두 different_scope로 바꾸면 energy_valid=False이나 secondary_active_energy_j=known_floor_j=17 남음. 서로다른scope합계는floor아니므로 identity/epoch/unit변경시 secondary/floor도null 권고. 부모에게전달했고직접수정없음.

### E → D

E가 독립 재현했습니다. events[5],[8] counter.scope만server_input으로바꾸면 auditfalse/energy null인데 active/floor17이남습니다. no_call_fixture close후t23 lowrequest삽입 seq재번호시 request_after_close인데 first_choice=low,complete=true도재현. foreign-session 첫request도mixed_session만flag후firstlow/outcomes정상으로유지. 모두부모에게수정요청했습니다. 세션ID빈문자열전체도 audittrue, start.t_ns='bad'는TypeError입니다.

### E → A

E가40/40재실행후추가반례확인. no_call_fixture의close후t23 low request삽입(연속seq) => request_after_close인데 first_choice=low/complete=true. 첫request.session_id를foreign-session으로바꾸면mixed_session인데firstlow/outcomessuccess·abandoned유지. 에너지null만으로선택/품질오염이차단되지않습니다. 관련semantic문제는firstchoiceunknown/qualityunknown또는엄격schemareject가필요하다고parent에요청했습니다. 센서만누락된경우독립적으로관측된choice/quality는유지하는별도validity축이낫습니다.

### E → B

E 반례: replay가mixed_session/late_after_close request를flag해도event_log_complete=true와first_choice=low를유지합니다. energy는null되지만choice분석에는들어갈수있음. outcomes도mixed_session이면성공·포기를유지합니다. parent에semantic-validity 분리/오염차단요청. 분석은syntheticlog의auditpassed만믿지말고 choice_valid/quality_valid/energy_valid각축으로신뢰가능결과만사용해야합니다. 센서누락만으로이미관측된choice/quality까지없앨필요는없습니다.

### D → E

D 재현도 일치했습니다. 다른device인 active합17은 'known_floor'로 둘 수 없어서 우선 차단 필요합니다. raw 시작/끝 counter가 자체로 유효하더라도 이를 따로 raw_counter_valid로 보존하고 attribution_valid/floor는 독립감사해야 합니다. 전체세션배타성은 single-log만으로 입증 못하니 allocator/외부session registry 증거를 명시적으로 unverified로 남기는 것도 제안합니다. 실제 장비점수는 올리지 않겠습니다. t_ns=None TypeError도 부모께 전달했습니다.

### A → E

A 동의합니다. 위반 로그의 에너지만 null로 두고 choice/quality는 정상으로 유지하면 HCI 추정량이 오염됩니다. 센서 오류는 energy validity, request 순서/세션/상태/hash 위반은 choice 및 관련 quality validity로 분리해야 합니다. UI none은 완료된 관측 창 안에서 '제출 시 확정 예산이 없음'으로 정의하고, UI에서 토글만 한 경우는 이 추정량에서 none입니다. 원래 선택 클릭 효과가 아니라 최초 확정 제출 모드 효과라는 이름으로 RQ1을 좁히겠습니다.

## 2라운드: 수정된 54검사 버전 확인

E는 수정된 두 Python 소스와 protocol-v3.md, analysis-appendix-v3.md를 직접 열어 읽었다.
`python -m unittest -v test_research_tools`를 독립 재실행해 54개 통과, 종료 코드0을 확인했다.
위 6개 반례를 다시 실행한 결과:

| 반례 | 수정 버전의 실제 출력 |
|---|---|
| 다른 scope의 활성 구간 | known_floor_j 및 secondary_active_energy_j 모두 null |
| 종료 요청 뒤 제출 | first_choice=unknown, 두 과제 결과 unknown |
| 다른 세션의 제출 | first_choice=unknown, 두 과제 결과 unknown |
| 문자열 시각 | 명시적 ValueError |
| 빈 세션 ID | 명시적 ValueError |
| 동일한 낮음·높음 의도 예산 | 명시적 ValueError |

따라서 이 6개 수정은 부모의 보고를 인용한 것만이 아니라 E가 독립 재현으로 확인했다.
반면 실제 센서·모델·UI가 검증된 것은 아니다.

### E → 사회자: 남은 조건 불일치 반례

E가 v3문서·분석명세·수정소스를 직접 읽고54/54독립재실행(종료0), 앞선6반례의수정도각각재현확인했습니다. 새중요잔여: fixture events[2].effective_config_hash='other-backend'이면 mode_config_hash_mismatch/auditfalse/energynull인데first_choice=low,outcomes success·abandoned유지. semantic_issues집합에 backend_hash_mismatch,mode_config_hash_mismatch,label_in_backend_config가없습니다. 실제조건불변성위반이choice/quality분석에정상값으로들어갈수있음. 선언조건불일치인report는품질/프로토콜 validity차단(보수적으로choiceunknown도허용)하거나분석입력에서해당분석축을불확실구간으로처리권고. 센서누락만choice/quality유지하는정책은타당합니다. 이수정만최종후확인하면추가문서반복없이점수확정하겠습니다.

### E → A

E가54/54와이전6반례수정확인. 남은mode_config_hash_mismatch는아직first_choice/outcomes를정상값으로둡니다(semantic_issues누락). 최초선택그자체는실제로관측됐을수있으나backend할당의일관성이위반되어프로토콜/관련품질신뢰가다릅니다. parent에보수적으로unknown또는독립protocol_validity차단을요청했습니다. choice는관측값보존하더라도조건정합성확증을통과시키지않아야한다는의견입니다.

## 재현용 반례의 핵심 변경

모든 반례는 synthetic_fixture.fixture() 또는 no_call_fixture()의 복사본으로 실행했다. 실제 센서값이 아니다.

```python
# 혼합 scope
d = fixture()
for i in (5, 8):
    d['events'][i]['counter']['scope'] = 'server_input'
print(replay(d))

# 서로 다른 세션의 제출
d = fixture()
d['events'][1]['session_id'] = 'foreign-session'
print(replay(d))

# 의도된 모드와 실제 설정 선언 불일치
d = fixture()
d['events'][2]['effective_config_hash'] = 'other-backend'
print(replay(d))
```

54검사 버전의 마지막 반례 출력은 mode_config_hash_mismatch, audit_passed=false,
energy_valid=false이나 first_choice=low 및 정상 품질 값이 남는 것이었다.
후속 수정 전 최종 통과 점수로 표현하지 않는다.

## 최종 57검사 버전 확인과 점수

### E → 사회자

E 최종 독립검사 완료: 수정57/57 통과(종료0), mode/backend/label 해시 반례3개에서 first_choice·quality unknown 격리 + raw_first_submitted_mode/reported_outcomes 보존 + confirmatoryfalse를 직접확인. 앞선6개수정도54버전에서독립재현확인했음. v3최종 고정 점수: 설계97/100(E1 25,E2 25,E3 19,E4 19,E5 9), 실행증거50/100(E1 8,E2 10,E3 15,E4 15,E5 2). 잔여: 실제응답adapter/전체UI→서버→채점사건연결, 실제연구자환경·두예산작동·센서·오차/시각. 준비코드의검증진전이며실측100아님. E-round2.md와E-dialogue.md에확정점수/해시/원문을저장하겠습니다.

### 직접 확인한 최종 반례 출력

mode_config_hash_mismatch, backend_hash_mismatch, label_in_backend_config 반례에서:

```json
{
  "audit_passed": false,
  "first_choice": "unknown",
  "outcomes": {"T01": "unknown", "T02": "unknown"},
  "raw_first_submitted_mode": "low",
  "reported_outcomes": {"T01": "success", "T02": "abandoned"},
  "confirmatory_ready": false
}
```

각 반례의 issues에는 해당 불일치 이유가 남았다.
최종 상세 점수, 실행 명령, 소스 해시는 [E-round2.md](E-round2.md)에 보존했다.

### D → E: 최종 교차 확인

D 최종 현행 소스 독립 재실행 57/57 통과, source hashes 전후일치 확인. known_floor 혼합device/scope, late/foreign-session choice, invalid t_ns 반례 교정이 포함된 버전입니다. 실제 장비/센서 검증은 여전히없음. 전체세션 계측·명명총효과·물리범위 해석과 문서 v3를 읽었고 실제운영 고정기준은 73/100으로 평가하겠습니다. 계측오차·실제두예산·자원확인 없이는 D만점은 줄 수 없습니다.
