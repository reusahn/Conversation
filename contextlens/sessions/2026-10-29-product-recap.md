# ContextLens — simplified product recap

Date: 29 October 2026 (California)

## Visible user messages (verbatim)

> 비디오소스를 직접업로드하거나 링크로 들고오면좋겠어

> 그리고영어여야해

> 흠 다시 생각해보자 우리 이내용 정리 쉽게

## Visible assistant commentary (verbatim)

> 영상 파일 업로드와 링크 가져오기를 눈에 잘 보이게 추가할게. 비교할 원본 영상도 직접 넣을 수 있게 하고, 링크를 가져오지 못하면 이유를 표시하도록 만들겠어.

> 구현은 잠깐 멈추고, 우리가 누구를 위해 무엇을 만드는지부터 쉽게 정리해볼게.

## Assistant response

응. **우리가 만들려는 건 ‘바이럴 영상의 출처와 맥락을 확인하는 웹도구’야.** 이름은 ContextLens.

짧은 영상을 보면 **실제 사건인지, 영화 장면인지, 오래된 영상인지** 설명만으로는 구분하기 어려울 때가 있어. 그때 확인할 근거를 옆에 붙여주는 거야.

사용 방법은 세 단계면 돼.

1. **영상 넣기** — 파일을 업로드하거나 링크 붙여넣기.
2. **맥락 확인하기** — 찾을 수 있는 원본, 해당 장면의 앞뒤, 공개 기록을 보여주기. 못 찾으면 ‘확인되지 않음’으로 표시.
3. **맥락과 함께 공유하기** — 출처 링크와 짧은 설명을 붙여 친구에게 보내기.

예를 들어, **‘오늘 실제로 일어난 일’이라는 설명으로 퍼지는 영화 장면**을 넣으면, 원본 작품과 일치하는 장면·공개 기록을 보여주는 식이야. 이건 우리가 시연할 수 있는 예시야.

**와우 포인트는 같은 장면이 서로 다른 설명으로 퍼졌다는 걸 한 화면에서 보여주고, 원본을 바로 재생하는 것.** 댓글 분석은 사람들이 무엇을 궁금해하는지 정리하는 보조 기능으로 두면 돼.

우선 **영상 입력 → 원본과 비교 → 근거와 함께 공유**, 이 세 가지에 집중하자. 화면은 전부 영어로 만들고.

현재 프로토타입은 **파일 업로드와 샘플 원본 1개 비교**까지 돼. 링크 가져오기·사용자 원본 추가·영어 화면은 아직 반영 전이고, 인터넷 전체에서 원본을 자동으로 찾는 기능도 아직 없어.

## Implementation status

This turn paused implementation to clarify the product at the user's latest request. The earlier upload/link and English-only interface requests remain pending. No Site source change, new deployment, Meta model run, persona score or user study occurred. The supplied misleading-caption example is a proposed demonstration, not an observed platform post. Continue the existing Site and preserve its audience.


## Follow-up: social problem and intervention

### User (verbatim)

그게 영상 바이얼의 사회적문제를 잡아주나??

### Assistant commentary (verbatim)

출처를 찾는 기능이 실제로 어떤 문제를 줄이는지, 해결하지 못하는 건 무엇인지 나눠서 볼게.

### Assistant response

**일부는 다룰 수 있어. 하지만 지금의 ‘원본 찾아주기’만으로는 네가 말한 사회문제를 해결한다고 하기엔 부족해.** 내가 기능을 정리하면서 사회적 목표를 너무 좁혔어.

네가 관심 있는 문제는 이런 것들이잖아.

| 사회문제 | 우리가 도울 수 있는 범위 |
|---|---|
| 영화·연출 장면을 실제 사건처럼 받아들임 | 확인된 작품·제작 기록과 장면을 연결 |
| 오래된 영상을 최근 사건으로 받아들임 | 이전 공개 기록을 제시. 실제 촬영일은 별도로 확인 |
| 일부만 잘린 장면으로 사람을 오해함 | 확보된 원본의 앞뒤를 재생해 비교 |
| AI 영상을 실제 촬영으로 받아들임 | 제작자 공개·출처 기록이 있을 때 제시. 기록이 없으면 미확인 |
| 무단 재사용, 양산형 콘텐츠, 과도한 시청 | 현재 기능으로 직접 해결하기 어려움 |

**우리가 집중할 사회문제는 ‘맥락이 사라진 영상이 오해를 동반한 채 다시 공유되는 것’으로 잡는 게 논리적이야.** 바이럴 자체가 해로운 건 아니니까.

그러려면 결과도 원본 링크 하나에서 끝나면 약해. 예를 들어 이런 흐름이어야 해.

1. 사람이 ‘오늘 실제로 벌어진 일’이라는 설명의 영상을 가져와.
2. 도구가 확인 가능한 원본과 이전 공개 기록을 보여줘.
3. 사람이 설명을 고치거나 공유를 보류할 수 있어.
4. 다시 공유한다면 **출처와 확인된 맥락도 함께 전달**돼.

공유할 때 정확성에 주의를 돌리는 개입이 이후 공유하는 뉴스의 질을 개선했다는 실험 연구는 있어. 다만 그 연구가 **우리 영상 도구의 효과까지 입증한 건 아니야.** genui{"citation":{"ref":"turn108view0"}}

**가장 큰 약점은 사용자가 굳이 별도 웹사이트에 영상을 가져와야 한다는 점이야.** 이미 의심하는 사람만 쓰면, 무심코 믿고 넘기는 사람에게는 닿지 않을 수 있어. 그래서 ‘얼마나 잘 찾는가’와 함께 **사람들이 실제로 쓰는가, 잘못된 설명을 수정하는가**를 확인해야 해.

내 판단은 이거야. **사회문제와 연결은 돼. 아직 해결 효과는 검증되지 않았고, 현재 프로토타입은 그중 ‘원본과 비교하기’만 구현한 단계야.** 다음 설계의 중심을 ‘영상을 분석하기’에서 **‘오해가 담긴 재공유를 줄이기’**로 잡으면 목적과 기능이 더 잘 맞아.

### Evidence and status

Research consulted: Pennycook et al., Nature (2021), DOI 10.1038/s41586-021-03344-2; abstract https://pubmed.ncbi.nlm.nih.gov/33731933/ . News accuracy-attention experiments do not validate ContextLens video intervention. This response proposes a narrower social objective; no implementation change, user test, causal effect or new persona score was produced.
