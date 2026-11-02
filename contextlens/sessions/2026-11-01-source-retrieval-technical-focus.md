# Technical focus: source retrieval

1 November 2026 (California)

User: 최초 원본을 찾는게 더 좋은 해커톤의 에이아이나 그런거아닐까?? 기술

Assistant commentary: 응. 출처 영상을 실제로 찾아내고 일치 구간까지 검증할 수 있다면, 블러 기능보다 기술 중심의 해커톤 주제로 더 강하다고 봐. 기존 영상 매칭 기술과 비교해서 우리가 새로 기여할 부분도 확인해볼게.

Assistant response:

**응. 기술 중심의 해커톤 주제로는 그쪽이 더 강하다고 봐.** 블러는 이용자가 결과를 경험하는 방식이고, **편집된 영상에서 출처를 찾아내는 기술이 프로젝트의 핵심**이 되는 거야.

우리가 도전할 문제를 이렇게 잡으면 돼.

> **“짧게 잘리고, 크롭되고, 자막이나 음악이 바뀐 영상에서도 출처 영상과 해당 구간을 찾아낼 수 있을까?”**

예를 들어 **20초짜리 쇼츠를 넣었더니, 출처 후보인 긴 영상의 08:12–08:32 구간을 찾아 나란히 재생하는 시연**이야. 이건 만들려는 시연 예시이고, 현재 구현됐다는 뜻은 아니야.

여기에 기술적으로 필요한 작업이 생겨.

- **후보 탐색:** 영상 프레임·음성·자막의 단서로 관련 영상을 찾기.
- **장면 검증:** 실제 같은 장면인지 비교하고 일치 구간을 정렬하기.
- **출처 근거:** 게시 기록과 확인 가능한 제작 정보를 연결하기.

그 결과를 이용해서 원본 앞뒤 장면을 보여주거나, 같은 출처에서 나온 반복 게시물을 묶고 블러 처리할 수 있어. **출처 탐색 기술 하나가 여러 사용자 기능의 기반이 되는 구조**지.

다만 영상 매칭 자체에는 Meta의 vPDQ 같은 기존 기술이 있어. 따라서 경쟁력은 **어떤 편집까지 견디는지, 출처 후보를 얼마나 정확히 찾는지, 결과를 얼마나 쉽게 검증할 수 있는지**로 보여줘야 해. genui{"citation":{"ref":"turn117search0"}}

**‘최초 원본 추적’을 목표로 삼는 건 좋아.** 다만 결과에서는 최초 제작·게시가 확인된 경우와, 우리가 찾은 자료 중 가장 이른 영상인 경우를 구분하면 돼.

내 추천은 명확해. **출처 영상 탐색·구간 매칭을 핵심 기술로, 맥락 비교를 대표 시연으로, 반복 횟수·블러를 부가 기능으로 두자.**

Status: Recommendation and hypothetical demo only. No new implementation or verified original-source discovery. Existing vPDQ precedent checked against official facebook/ThreatExchange documentation via web retrieval after the connector file read returned no usable content. No novelty or award guarantee.
