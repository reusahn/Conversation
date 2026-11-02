# Candidate technical contribution beyond feature integration

1 November 2026 (California)

User: Meta의 vPDQ 같은 기존 기술이나 에이피아이나 모델을 쓰는게 더 좋아서 더 특별화 특별한점은뭘까 블러나 횟수느 ㄴ기능이고 더필요한건 기술적 특허받을정도의 새로움

Assistant commentary:

맞아. vPDQ나 Meta 모델을 기반으로 쓰면서도, 그 위에 새 알고리즘을 만들 수 있어. 블러 같은 기능과 구분해서, 기존 연구가 이미 해결한 부분을 확인하고 우리가 기술적으로 도전할 지점을 찾아볼게. 특허를 받을 수 있다는 판단과 해커톤에서 보여줄 수 있는 새로움도 구분해서 설명할게.

조사해보니, 편집된 영상의 출처를 찾는 것 자체는 Adobe의 VPN 같은 기존 연구에서도 다루고 있어. 그래서 새로움의 후보를 더 좁혀야 해. 나는 자막·반응 얼굴·교체된 음성 때문에 매칭이 애매할 때, 영상의 어느 부분을 추가 검증할지 선택하는 알고리즘을 검토할 만하다고 봐.

Assistant response:

**맞아. 네가 원하는 건 ‘기존 모델을 활용한 기능’에서 더 나아가, 우리가 만든 새로운 기술적 방법이 있는 프로젝트야.** vPDQ나 Meta API를 기반으로 쓰는 건 좋아. 그 위에서 **어떤 계산·탐색·검증 방법을 새로 만들었는지**가 있어야 해.

다만 조사해보니, **‘편집된 영상에서도 원본을 찾는다’만으로는 새로움이 충분하지 않아.** Adobe의 VPN은 이미 잘린 영상, 크기·품질 변경, 자막·이모지 추가 등에 견디는 출처 검색과 영상·음성 특징 결합을 연구했어. 앞서 제안한 기능들을 더 구체적인 기술 문제로 좁혀야 해. genui{"citation":{"ref":"turn119view0"}}

**내가 지금 가장 검토하고 싶은 기술 후보는 이거야.**

> **원본 후보들이 헷갈릴 때, 후보를 구별하는 데 필요한 프레임과 화면 영역을 골라 추가로 검증하는 검색 알고리즘.**

예를 들어 쇼츠 화면의 절반은 반응하는 사람의 얼굴이고, 아래에는 큰 자막이 있으며, 실제 출처 영상은 작은 영역에만 남아 있다고 해보자. 음악도 교체됐고.

이 상황에서 개발할 방법은 다음과 같아.

1. **vPDQ 등으로 출처 후보를 빠르게 찾는다.**
2. **후보별로 실제 일치하는 영역과 불일치하는 영역을 계산한다.** 화면 전체 점수에만 의존하지 않고, 시간에 따라 일치가 이어지는지도 본다.
3. **남은 후보를 가장 잘 구별할 프레임·영역을 선택한다.** 그 부분에만 정밀 매칭이나 SAM을 이용한 영역 분리 등을 추가 적용한다.
4. **근거가 충분하면 결과를 내고, 부족하면 후보를 남긴다.** 같은 장면을 담은 재업로드끼리 구별할 근거가 없으면 최초 원본을 임의로 고르지 않는다.

**우리가 새로 설계할 핵심은 3번의 선택 규칙과 4번의 종료 조건이야.** 단순히 “점수가 낮으면 Spark를 호출한다”는 연결보다 구체적인 알고리즘이 필요해. 어떤 불일치를 보고, 다음에 어디를 검사하며, 언제 멈출지를 정의하는 거지.

역할도 분명해져.

| 구성 요소 | 역할 |
|---|---|
| vPDQ 등 기존 검색 기술 | 빠르게 후보를 좁히는 기반 |
| SAM·Meta 모델 | 필요한 영역 분리나 보조 분석 |
| **우리가 개발할 부분** | **추가 검증할 위치·순서·종료 조건을 정하는 방법** |
| 블러·횟수·비교 화면 | 기술의 결과를 보여주는 사용자 기능 |

**그리고 이 방법도 아직 ‘새로운 발명’으로 확인된 건 아니야.** 선택적 검증이나 중요한 프레임을 고르는 접근에도 선행연구가 있을 수 있어. 지금은 **기술적 기여를 만들기 위한 구체적인 연구 가설**이야.

검증은 같은 후보 목록과 비용 조건에서 다음 세 가지를 비교하면 돼.

- vPDQ 기반 매칭
- 정해진 프레임을 추가로 검사하는 방식
- **우리가 선택한 프레임·영역만 추가 검사하는 방식**

여기서 **같은 오검출 수준에서 더 많은 출처를 찾거나, 같은 정확도를 더 적은 비용으로 달성하는지** 보여줘야 해. 판단을 보류한 비율도 함께 공개해야 하고.

특허 가능성은 별도 판단이야. 미국 기준으로는 신규성·비자명성뿐 아니라 특허 대상 적격성과 충분한 설명 등도 요구돼. 지금 조사만으로 ‘특허받을 기술’이라고 말할 수는 없어. genui{"citation":{"refs":["turn119search0","turn119search2"]}}

**내 추천은 ‘원본 찾기 앱’에서 한 단계 들어가, ‘편집으로 가려진 영상에서 적은 검증으로 출처를 식별하는 방법’을 개발하는 거야.** 이 정도로 문제와 알고리즘을 좁혀야, 네가 원하는 기술적 새로움을 실제로 따져볼 수 있어.

Status: Proposed research hypothesis only; adaptive verification/sampling and stopping rules are NOT established as novel or patentable. No new algorithm, experiment, model call, patent search of specific claims or legal opinion. Prior art reviewed includes VPN (Adobe/CVMP 2021), vPDQ, TransVCL abstract, VCSL and audiovisual copy-alignment work. A rigorous paper-and-patent prior-art comparison remains pending. Baseline comparisons and evaluation conditions above are proposed, not executed. Identical available evidence cannot establish direct copying direction or first origin.

Primary sources: https://research.adobe.com/publication/vpn-video-provenance-network-for-robust-content-attribution/ ; https://www.uspto.gov/patents/basics/essentials ; https://www.uspto.gov/web/offices/pac/mpep/s2106.html .
