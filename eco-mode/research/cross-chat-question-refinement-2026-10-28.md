# Eco Mode — cross-chat question refinement (2026-10-28)

**Status:** research-question critique and refinement only. Not an experiment, preregistration, ethical approval, external review, or evidence of environmental savings.

## Context and provenance

The user shared a separate ChatGPT conversation that summarized the Eco Mode project and gave six fictional persona scores for **the central research question only**: A HCI 88, B HCI writing 84, C AI 89, D environmental operations 86, E implementation 90, F fictional Ahn 87. These were *simulated perspectives* reported by that conversation, not independent scholars or journal reviewers. Do not treat these numbers as manuscript readiness or acceptance probabilities.

## Previous question (supplied)

> How does an Eco label change users' savings beliefs and mode choice, and how do whole-session token demand and task outcomes vary with actual inference configuration?

The main risk is presenting two juxtaposed questions without explaining how the psychological and technical factors interact. Related studies already investigate energy disclosure, eco-friendly choice and placebo-related subjective quality (Klesel & Messer, CHI 2026; https://arxiv.org/abs/2603.23075), as well as energy feedback (EcoChat Probe, FAccT 2026; https://doi.org/10.1145/3805689.3812368).

## Proposed focused overarching RQ

> **Does the effect of sustainability framing on users' beliefs and computational demand depend on whether an AI system actually reduces its inference effort?**

Korean: **AI의 친환경적 표시가 사용자의 절약 신념과 연산 자원 수요에 미치는 영향은 실제로 추론 연산량을 낮추는 설정이 적용되는지에 따라 달라지는가?**

This is a *testable proposal*, not a proven novel finding. It motivates testing moderation/interaction in a 2×2 randomized factorial (Eco vs neutral label) × (High vs Low backend), with same hosted provider/model and a fixed Standard option. Randomization must be independently verified; actual effort setting must be confirmed where possible.

## Operational refinement / important distinctions

1. **Initial mode choice** happens before any backend response: backend assignment cannot directly cause this first click when invisible. Analyze the *label main effect* on initial choice rather than claim a backend×label interaction at this point.
2. **Belief** has at least two constructs: belief that a *lower inference-effort configuration* was applied (benchmarked against actual backend setting), versus belief that *data-center electricity/carbon/water* were saved (not independently verifiable from API token logs). Do not conflate these or subtract unlike units.
3. **Whole-session service demand** is all provider-reported tokens across tasks, logical requests, actual backend attempts, retries, mode switches, failures, abandonments and accepted cancellations/drain; correct token field inclusion; participant is the independent randomized unit. Whether cancellation backend metering is available must be confirmed, and missing values must be preserved.
4. **Causal estimands:** randomized label and backend intention-to-treat effects, their interaction in total tokens and outcomes. Baseline environmental intention is measured observationally; interactions involving it are interpretation/moderation, not evidence intention was randomized.
5. **Mechanism ambiguity:** a lower-effort policy might decrease tokens per attempt yet increase session totals through additional requests, but a rising retry count alone cannot prove causal mediation; treat this as a mechanism candidate with caution and display task success/abandonment.
6. **Environmental claim ceiling:** API tokens and settings do not physically measure data-center power. Google/OpenAI published averages cannot be converted to a per-session low/high energy comparison without an applicable attribution model. Report energy as not observed absent validated source-specific provider measurements.
7. **Study ethics:** Withholding actual backend assignment or misrepresenting Eco performance needs UCSB HSC/IRB assessment, prospective authorization if appropriate, and approved debrief. No recruitment or deception before review.

## Proposed evaluable questions / outcome priority

- **Primary distinctive causal question (if adequately powered):** Is the Eco-label effect on **total provider-reported whole-session tokens** different when the alternative uses Low rather than High? Interaction: (D − C) − (B − A), where A neutral+High, B Eco+High, C neutral+Low, D Eco+Low. Requires powered sample, two-sided interval; an inconclusive interaction does not prove invariance.
- **Co-primary or key secondary, to finalize before collecting outcomes:** Eco label effect on **belief of lower compute** when backend is High (B vs A); initial choice label effect (combined Eco vs neutral) separately. Prespecify endpoint family and multiplicity based on feasibility; don't declare multiple primaries casually.
- **Mandatory contextual outcomes:** objectively scored task success, time, switching and retries, abandonment, provider usage completeness, confidence/quality; compare alternative selection beyond first click as post-response behavior.
- **Exploratory:** environmental intention associations and trust immediately before/after HSC-approved debrief; cannot imply long-term effects.

## What would genuinely extend CHI 2026 (if measured)

A factorial causal boundary condition: eco naming can lead to beliefs about lower compute even with identical backend, and the behavioral/resource-demand consequences of the name may differ depending on whether low effort actually exists. This **dissociation between perceived compute reduction, objectively applied configuration, and full-task tokens** is a candidate explanatory result, not just an eco-choice click effect. A narrow no-interaction finding could also be informative if precisely estimated, but a weak null is not a discovery.

## Readiness and next gates

- CHI-likeness/readiness is not measured by fictional scores. User-supplied scores were for question quality only.
- Freeze exact provider/model that can expose verifiable high/low reasoning setting and usage semantics.
- Validate tasks and logging, obtain allowable budget/credits and HSC review, pilot sample variance/interaction power. Four-arm interaction is potentially much more expensive than a two-arm label main effect. If insufficient resources, designate a two-arm sham label test as pilot and postpone the full factorial; do not claim interaction from such pilot.
- Manuscript Introduction/Related Work/Methods can be drafted now, empirical Results cannot.

## Relationship to other files

See `eco-placebo-factorial-protocol-v1.0.md` (four-arm design), `novel-contribution-eco-evidence-gap-v1.md` (contribution boundary), and `hosted-llm-datacenter-study-v0.2.md` (commercial data-center environmental measurement limits).
