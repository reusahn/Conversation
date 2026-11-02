# Distinguishing source-retrieval core from repetition UI

1 November 2026 (California)

User (verbatim): 오리지널 영상이 어디였는 어디서나왔는지 알아내는 에이아이 기술보다 더 좋으거같아 그게??

Assistant commentary: 해커톤의 핵심 기술로는 출처 영상을 찾아내는 쪽이 더 강하다고 봐. 내가 앞선 설명에서 블러 기능의 직관성과 출처 탐색의 기술적 가치를 섞어서 설명했어. 그 둘을 구분해서 정리할게.

Assistant response:

**아니. 블러·횟수 표시가 ‘원래 영상이 어디서 나왔는지 찾아내는 AI 기술’보다 더 좋은 핵심이라는 뜻은 아니야.** 해커톤의 기술적 중심으로는 **출처 영상 탐색과 정확한 장면 매칭**이 더 강하다고 봐. 내가 앞에서 화면의 직관성과 기술적 가치를 섞어서 설명했어.

네가 말한 기술의 결과는 이런 거지.

> **짧게 잘리고, 크롭되고, 자막이 붙은 영상을 넣어도 → 출처 영상 후보를 찾고 → 어느 구간에서 가져왔는지 보여준다.**

여기에 출처의 앞뒤 장면과 공개 기록을 연결하면, 사람들이 영상의 맥락을 직접 확인할 수 있어.

역할을 이렇게 잡으면 명확해져.

| 역할 | 기능 |
|---|---|
| **핵심 기술** | 편집된 클립에서 출처 영상 후보와 일치 구간 찾기 |
| **핵심 경험** | 현재 클립과 출처를 나란히 재생하고 차이 확인하기 |
| **선택 기능** | 같은 장면의 반복 횟수 표시·블러 처리 |

**블러는 그 기술을 활용하는 기능 중 하나로 두면 돼.** 중요한 성과는 “세 번째라서 가렸다”보다 **“겉모습이 바뀌었는데도 같은 영상의 출처와 해당 구간을 찾아냈다”**가 되는 거야.

다만 **찾아낸 가장 오래된 게시물과 최초 원본은 구분해야 해.** 확보한 자료만으로 최초 업로더나 촬영자를 확정할 수 없다면 ‘출처 후보’ 또는 ‘확인된 이전 게시 영상’으로 보여주는 게 맞아.

**네가 중심에 두고 싶은 게 이 기술이라면, 제안서도 ‘출처 영상 탐색’을 앞에 놓고 다시 정리하는 게 맞아.** 현재 구현은 작은 샘플 컬렉션 안의 매칭까지이고, 인터넷에서 출처를 찾아오는 기능은 아직 없어.

Status: Comparative product judgment, not a new implementation or independent evaluation. Re-centering source retrieval is recommended in response to the user's challenge, not claimed as a silently adopted scope change. Current prototype remains limited-reference matching; internet-wide retrieval and earliest-origin identification unimplemented. No new score, model call or test.
