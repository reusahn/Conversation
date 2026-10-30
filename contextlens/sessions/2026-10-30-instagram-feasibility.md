# Instagram deployment feasibility

30 October 2026 (California)

User: 실제로 인스타에 쓰면안되나

Assistant commentary: 실제 Instagram에서 쓸 수 있는 형태를 확인해볼게. PC 웹 확장 프로그램으로 내 화면의 게시물을 가리는 방법과, 모바일 앱 자체에 적용하는 방법을 구분해서 볼 필요가 있어.

Assistant response:

**응. PC에서 Instagram 웹을 볼 때 작동하는 브라우저 확장 프로그램 형태로 시도할 수 있어.** 실제 인스타 화면에 적용하는 쪽이 사용 목적도 더 분명해져.

Chrome 확장 프로그램은 웹페이지의 내용을 읽고 화면을 바꿀 수 있어. 그래서 **게시물 위에 반복 횟수를 표시하거나, 영상을 블러 처리하고 다시 보기 버튼을 붙이는 UI**는 기술적으로 구현 가능한 방식이야. genui{"citation":{"ref":"turn114search2"}}

예상 사용 흐름은 이래.

1. 사용자가 PC Chrome에서 Instagram을 평소처럼 봐.
2. 확장 프로그램이 화면에 나타난 영상과 노출 기록을 비교해.
3. 같은 장면이 세 번째 나타나면 블러와 **“This scene appeared 3 times”**를 표시해.
4. 사용자가 열어보거나 기준을 바꿔.

여기서 조절하는 건 **사용자 브라우저에 표시되는 화면**이야. Instagram 서버의 추천 순위가 바뀌는 것은 아니야. 공식 API 문서는 주로 프로 계정의 게시물·댓글 관리 등을 지원하며, 개인 추천 피드를 재정렬하는 기능은 확인되지 않았어. genui{"citation":{"ref":"turn114search0"}}

**아직 확인해야 하는 핵심은 실제 Instagram 영상에서 비교용 프레임을 안정적으로 얻을 수 있는지야.** 지금 프로토타입에서는 우리가 제공한 파일을 비교했어. Instagram에서는 영상 제공 방식과 브라우저 보안 제한 때문에 그대로 옮겨지지 않을 수 있어. 특히 다른 계정의 크롭·재편집 영상까지 묶으려면 이 부분을 시험해야 해.

**나는 다음 개발을 ‘실제 Instagram 웹용 확장 프로그램’으로 잡는 게 좋겠어.** 먼저 실제 게시물에서 영상 비교가 되는지 검증하고, 되면 현재 만든 블러·횟수·다시 보기 기능을 붙이자. 모바일 Instagram 앱 내부에 적용하는 것은 별도 문제이고, 현재는 구현하지 않았어.

Status: Feasibility proposal only; no extension installed/built, no Instagram account accessed or video extraction tested. DOM modification capability does not prove access to Instagram video frames or platform permission. Official Chrome content-script documentation and Meta's official Instagram API Postman documentation were consulted. No native recommendation-control claim.
