# ContextLens — official workshop preparation

Date: 29 October 2026 (California)

## User-provided announcement (verbatim)

**@Builders** [🔵](https://discord.com/assets/bd987f3558fe3c06.svg) Get ready for our first Live Session with Meta from 12:00 PM - 1:00 PM ET today!  **Agents 101: Build a Multimodal AI Agent Pt. 1** with Suraj Subramanian [Livestream](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/live "Livestream

(https://cerebralvalley.ai/e/meta-ai-developer-hackathon/live)")  **Prerequisites:** &#x20;

1. Download Muse Code
2. Sign in to Muse Code with your API Key
3. The repository for the workshop is here: [https://github.com/meta-models/legal-agent-workshop](https://github.com/meta-models/legal-agent-workshop "https://github.com/meta-models/legal-agent-workshop")
4. Run the following commands to setup

&#x20;git clone [https://github.com/meta-models/legal-agent-workshop.git](https://github.com/meta-models/legal-agent-workshop.git "https://github.com/meta-models/legal-agent-workshop.git") cd legal-agent-workshop/agent cp .env.example .env      # add MODEL_API_KEY here  Expect the workshop to use around $7 in tokens. Heads up, we recommend using a macOS or Linux machine (Windows probably needs WSL, untested), git, Python 3.9 or newer for this workshop.

## Assistant commentary

워크숍 저장소의 준비 과정을 확인하고, 우리 프로토타입에 활용할 수 있는 부분도 짚어볼게.

## Assistant response

이건 **Muse Code와 Meta 모델로 AI 에이전트를 만드는 실습 준비 공지**야. 법률 문서를 다루는 예제로 모델 연결과 도구 실행을 배우는 거고, 우리 프로젝트에도 참고할 수 있어.

중요한 내용은 다음이야.

- **시간:** 공지의 12–1 PM ET는 캘리포니아 오전 **9–10시**.
- **준비물:** Mac/Linux, Git, Python 3.9 이상, Muse Code, Meta API 키.
- **비용:** 공지 기준 토큰 사용료 **약 $7 예상**. 고정 요금이나 상한은 아니야.
- **API 키는 두 곳에 설정:** 실습 폴더의 `.env`와 Muse Code 로그인.

Mac 터미널에서 준비하는 명령어는 이렇게 나눠서 실행하면 돼.

```bash
git clone https://github.com/meta-models/legal-agent-workshop.git
cd legal-agent-workshop/agent
cp .env.example .env
```

생성된 `.env`를 편집기로 열어 **`MODEL_API_KEY=` 뒤에 본인의 키를 넣고 저장**해. 그다음:

```bash
./helper setup
muse
```

공식 저장소를 확인해보니, `./helper setup`이 필요한 Python 환경과 라이브러리를 준비하고 키 접근을 확인해줘. Muse Code 첫 실행에서는 **Paste an API key**를 선택하고, 실습 시작 프롬프트는 [핸드북의 1.7절](https://github.com/meta-models/legal-agent-workshop/blob/main/HANDBOOK.md)을 따르면 돼. Muse Code 설치도 그 핸드북에 연결돼 있어.

**우리에게 활용할 부분은 ‘같은 영상에 새로 붙은 자막·설명이 무엇인지 Meta 모델로 비교하는 기능’이야.** 현재 프로토타입은 영상 프레임과 구간만 비교하니까, 이 실습을 참고해서 내용 차이 분석을 붙일 수 있어. 그 분석이 잘 되는지는 따로 시험해야 해.

## Retrieval / action status

Read public meta-models/legal-agent-workshop README.md (blob f6743dd1fb506f39e874ce653275e06cf46145c7), agent/.env.example (8a757f43310abf6ce0fbb8837c16640f9bffe57b), HANDBOOK.md lines 1–145 (e48fcf8a9b67855a28e19e045f2e5ee78a802edf). Defaults mention muse-spark-1.3 and sam-3.1, Meta API base. Instructions summarized, not executed. No software installed, workshop agent run, token spend or API key access. Relative “today” in pasted announcement was not treated as a verified session date. Existing messenger prototype unchanged; model comparison is a proposed next capability, not an achieved integration.
