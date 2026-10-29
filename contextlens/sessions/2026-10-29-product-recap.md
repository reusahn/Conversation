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

### Assistant draft (prepared but not delivered before user steering)

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


## User steering: repeated exposure control

### User (verbatim)

그게 영상 바이얼의 사회적문제를 잡아주나?? 나같으면은 비슷한 영상이 사람에게 3번이상보여지면은 노출도를 줄이는걸 하겠다 이생각이 더 괜찮지않나? 누가 바이럴인지 아닌지 확인하는게 그렇게 중요한가

### Assistant commentary (verbatim)

네 제안은 사람들이 이미 본 콘텐츠에 계속 노출되는 문제를 직접 다루고 있어. 출처 확인보다 이 방향을 중심에 두고, 무엇을 ‘비슷한 영상’으로 묶을지 살펴볼게.

### Assistant response

**응. 네가 말한 문제에는 네 제안이 더 직접적으로 맞아.** 내가 출처 확인에 집중하면서, 네가 관심 있는 **‘비슷한 콘텐츠가 계속 밀려오는 경험’**을 놓쳤어. 바이럴인지 분류하는 것 자체는 사용자에게 큰 도움이 안 될 수 있어.

네 아이디어의 중심은 이거야.

**“이미 충분히 본 콘텐츠는 덜 보이게 하고, 얼마나 반복해서 볼지는 내가 정한다.”**

예를 들어 같은 장면을 계정 A에서 보고, B의 자막 버전으로 보고, C의 크롭 버전으로 또 보면:

> **You’ve seen this scene 3 times today.**  
> **Show less · Keep showing**

이렇게 세 번째부터 접어주고, 원하면 다시 볼 수 있게 하는 거지. 계정이 달라도 같은 장면이라는 걸 알아내는 기술이 여기서 의미를 가져.

다만 **‘비슷하다’의 기준이 핵심이야.**

- **같은 장면의 재업로드·자막·크롭 버전**부터 묶기.
- 같은 주제라도 새로운 설명이나 다른 관점이 있으면 별개로 두기.
- **3회는 시작 설정**으로 두고, 사용자가 횟수와 적용 기간을 바꾸거나 해제할 수 있게 하기.

이 방향의 사회적 목표는 **원치 않는 반복 노출을 줄이고, 피드를 조절할 선택권을 주는 것**이야. 허위정보나 중독까지 해결했다고 말할 수는 없어. 실제로 반복이 줄었는지, 보고 싶은 영상까지 가려지지는 않는지 확인해야 하고.

이미 Instagram에는 주제별로 더 보거나 덜 보도록 조절하는 **Your Algorithm**이 있어. 그래서 우리 차별점은 **‘같은 콘텐츠의 여러 변형을 묶어서, 개인이 정한 반복 횟수를 적용한다’**로 구체화해야 해. 이 기능의 최초성은 별도 조사가 필요해. genui{"citation":{"ref":"turn110search1"}}

해커톤에서는 **직접 만든 영어 영상 피드에서 필터를 켜기 전후를 보여주는 데모**가 명확해. Instagram 앱의 노출을 외부 도구로 직접 조절할 권한은 아직 확인되지 않았으니, 그 부분은 구현됐다고 약속하면 안 돼.

**나는 이 방향을 중심으로 다시 잡는 게 좋겠어. 기존의 영상 매칭 기술도 ‘반복 콘텐츠를 알아채는 기능’으로 이어서 쓸 수 있어.**

### Status

Proposal only. No feed filter was implemented or deployed, no Instagram exposure-control permission established, no novelty or impact result claimed. English UI remains requested. Same-scene variants proposed as initial scope, with configurable per-user repetition limit and reversible controls. Prior response draft above was not sent as a final response before this user message arrived.

Source: Meta, 12 May 2026, https://about.fb.com/news/2026/05/new-supervision-tools-parents-insights-teens-algorithm/ . Existing Your Algorithm topic controls differ from proposed same-scene repetition limit; this is not proof no competing feature exists.


## Development beyond a fixed repetition cap

### User (verbatim)

응응 이미있던 그 알고리즘에 뭔가 더 발전시키거나 더 와우포인트를 만들어야해 그런게 와우포인트인거야

### Assistant commentary (verbatim)

그럼 ‘세 번 보면 접기’에서 한 단계 더 가보자. 이미 본 내용과 새로 추가된 내용을 구분해서, 반복은 줄이면서 새로운 정보는 놓치지 않게 하는 방향을 생각해볼게.

### Assistant response

**응. 그러면 ‘세 번 보면 숨기기’를 발전시켜서, ‘이미 본 부분과 새로 추가된 부분을 구분하는 피드’로 가보자.**

예를 들어 같은 장면을 여러 계정이 재사용해도, 어떤 영상은 자막만 바뀌고 어떤 영상은 새로운 설명이나 다른 시점을 추가하잖아. **그 차이를 보여주면서 반복 노출을 조절하는 것**이 핵심이야.

| 다음에 등장한 영상 | 제안하는 동작 |
|---|---|
| 이미 본 장면에 음악·크롭만 변경 | 같은 묶음으로 세고, 설정한 횟수부터 접기 |
| 같은 장면에 새로운 해설 추가 | ‘새 해설 있음’ 표시하고 유지 |
| 이전 영상에 없던 후속 장면 추가 | 새 구간을 표시하고, 눌러서 바로 보기 |
| 새로운 내용인지 판단이 불확실 | 유지하고 사용자가 묶음을 수정하도록 하기 |

화면에는 이렇게 나오는 거야.

> **You’ve seen this scene 3 times.**  
> **This version adds a different viewpoint.**  
> **Watch the addition · Watch full video**

**와우 포인트는 반복을 없애면서도, 놓칠 만한 차이를 찾아준다는 거야.** 사용자가 좋아하는 주제는 계속 보되 같은 장면을 계속 소비할 필요는 줄이는 방향이지. ‘새 해설’이 정확하거나 유익하다는 뜻은 아니고, 무엇이 달라졌는지를 보여주는 거야.

기존 기능과의 차이는 분명해야 해. Meta는 이미 동일 콘텐츠 대신 원본을 추천하는 정책을 발표했어. 그래서 단순 중복 탐지만으로 차별화하기는 어려워. **우리의 발전 방향은 ‘앱에 기록된 개인의 시청 이력을 기준으로, 이번 버전에서 달라진 부분까지 비교한다’는 것**이야. 이 조합의 최초성은 아직 확인하지 않았어. genui{"citation":{"ref":"turn111search1"}}

해커톤 데모는 **직접 구성한 피드에서** 이렇게 보여주면 돼.

1. 같은 장면의 재업로드·크롭·해설·후속 장면 버전이 차례로 등장해.
2. 필터를 켜면 반복 버전이 접히고, 추가된 해설과 장면은 남아.
3. 접힌 이유와 새 구간을 클릭해서 직접 확인하고, 잘못 묶였으면 풀어.

영상 매칭은 반복 구간을 찾고, Meta 모델은 자막·해설의 차이를 설명하도록 설계할 수 있어. **현재 프로토타입에는 이 피드 기능이 아직 없어.**

사회적 효과도 구체적으로 검증할 수 있어. **반복 시청 시간은 줄었는가, 새로운 관점까지 잘못 가리지는 않았는가.** 이 두 가지를 함께 확인하면, 네가 말한 ‘알고리즘을 더 발전시키는 프로젝트’가 돼.

### Status and source

Product proposal only: per-user viewed-history comparison, repeated footage folding, added commentary/segments highlighted, uncertain cases retained, reversible user grouping. Novelty and social impact unverified; no Site code change, API call, new persona evaluation or deployment. Demo sequence is proposed and team-curated, not a live Instagram feed or observed result.

Primary source: Meta, 2 May 2024, https://about.fb.com/ltam/news/2024/05/ayudando-a-los-creadores-a-encontrar-nuevas-audiencias/ . Identical-content replacement already announced; source also distinguishes materially transformed works. This is background, not an exhaustive 2026 competition review.
