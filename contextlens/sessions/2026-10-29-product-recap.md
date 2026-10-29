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
