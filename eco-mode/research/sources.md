# 근거와 선행연구

확인 기준일: 2026-10-26. 아래 자료는 연구 질문과 계획을 검토할 때 사용한 원문·공식 문서이다.
문헌의 실험 결과를 이 프로젝트의 결과로 옮기지 않는다. 사전논문은 출판·심사 완료 논문과 구분한다.
문서의 기능 지원과 실제 연구 장비에서의 작동은 별도 검증 대상이다.

| 자료 | 연결 | 이번 연구에서 확인할 점 |
|---|---|---|
| Good for the Planet, Bad for Me? (CHI 2026) | https://arxiv.org/html/2603.23075v1 | 환경 표시와 성능 기대·선택을 다룬 가까운 선행연구. 실제 두 예산의 전체 세션 에너지·품질을 검증하는 설계와 대조할 필요가 있음 |
| EcoChat (FAccT 2026) | https://kclpure.kcl.ac.uk/portal/en/publications/ecochat-probe-how-energy-feedback-shapes-end-users-interpretation/ | 환경·에너지 피드백과 사용 경험에 관한 선행연구. 인식 변화와 사용량 변화는 같은 결과가 아님 |
| When LLMs Slow Down (ICT4S 2026 원문) | https://arxiv.org/html/2608.23968v1 | 지연시간·탄소·Eco 선택의 관계. 명명 효과와 지연의 효과를 구분 |
| A-LEMS / Energy per Successful Goal (사전논문) | https://arxiv.org/html/2605.22883v1 | 성공 과제까지의 재시도·실패 비용 집계가 이미 논의됨. 전체 과제 집계 자체를 최초 기여로 주장하지 않음 |
| When Is Smaller Greener? (사전논문) | https://arxiv.org/abs/2610.19345 | 신뢰도와 길이를 포함한 자원 비교. 작은 모델과 같은 모델의 추론 예산 조절을 구분 |
| EcoLogits (JOSS 2025) | https://joss.theoj.org/papers/10.21105/joss.07471 | 모델·가정에 근거한 환경 추정 도구. 직접 계측과 추정을 구분 |
| Qwen3-4B 공식 모델 카드 | https://huggingface.co/Qwen/Qwen3-4B | 공개 모델 후보, thinking 제어와 실행 설정 확인 |
| vLLM 공식 Reasoning Outputs | https://docs.vllm.ai/en/stable/features/reasoning_outputs/ | reasoning parser, thinking token budget, 출력 제한과 강제 종료 동작 확인 |
| NVIDIA NVML 공식 Device Queries | https://docs.nvidia.com/deploy/nvml-api/latest/api/group__nvmlDeviceQueries.html | 누적 에너지 API의 단위·범위·장치 지원을 확인. 실제 센서 지원을 별도로 검사 |
| Energy Use of AI Inference: Efficiency Pathways and Test-Time Scaling | https://www.microsoft.com/en-us/research/publication/energy-use-of-ai-inference-efficiency-pathways-and-test-time-scaling/ | 추론 시 계산량과 에너지의 관계를 해석할 근거 |
| Making AI Less “Thirsty” | https://arxiv.org/abs/2304.03271 | 물 사용은 전력만으로 직접 확정할 수 없으며 위치·운영 가정과 범위가 필요 |
| UCSB Human Subjects | https://www.research.ucsb.edu/index.php/human-subjects/about | 사람 대상 활동이 생길 때 소속 절차·심의/면제 해당 여부 확인. 이 계획은 기관의 판정을 대신하지 않음 |

## 현재의 차별점 후보

기존의 환경 라벨, 피드백, 지연, 자원 추정 연구와 대조하여 다음 조합을 검증할 계획이다.

1. 저예산 실행 설정은 동일하게 유지하고 Low/Fast/Eco라는 이름을 무작위로 바꾼다.
2. 이름의 총효과를 선택뿐 아니라 실패·재시도·전환·포기를 포함한 세션 에너지로 평가한다.
3. 품질 허용폭을 미리 정하고 에너지 감소와 품질 유지를 함께 판단한다.

이는 기여 후보이다. 모든 선행연구를 망라한 체계적 문헌고찰이나 최초성 보장은 아직 아니다.
