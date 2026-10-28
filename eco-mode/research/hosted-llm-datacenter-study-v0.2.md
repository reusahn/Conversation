# Hosted LLM Eco Mode — environmental intention, backend computation, and data-center impact (v0.2)

Date: 2026-10-28
Status: revised DESIGN after user clarified that the study target is **ChatGPT/Gemini/Claude-like commercial hosted LLM services and large-company data centers**, not a personal desktop GPU. No empirical measurements, no API expenditure, no participant research. This supersedes the **priority** of the prior local-first proposal in `stage0-zero-cost-plan-v0.1.md`. Local GPU benchmarking is at most a separate validation exercise and cannot establish a hosted provider's per-request electricity or environmental effects.

## Research question

**When people choose an Eco option on a commercially hosted LLM service for environmental reasons, how do their decisions change service use and provider-reported computational demand, and what can — and cannot — be inferred about data-center electricity, carbon, and water?**

This encompasses three separate causal/measurement layers:
1. **Human/interaction:** baseline environmental intention, randomized Eco-vs-neutral framing, low/high mode selection, retries, switching, abandonment, and task completion.
2. **Provider API telemetry:** total input/output/reasoning tokens (with correct inclusion semantics), response timing, model/version, effort controls if supported, all requests within full task sessions.
3. **Environmental accounting:** real physical request-level energy/cooling/carbon require privileged provider telemetry not generally available in commercial APIs. Public provider/third-party estimates are *scenario inputs*, not observed treatment-level energy savings. Annual corporate facility figures do not isolate a single API prompt or mode. A decrease in reported token demand does not prove a decrease in actual facility electricity, emissions, water, or ecological harm.

## What public sources can show (not interchangeable)

- Google, Elsworth et al. (2025), *Measuring the environmental impact of delivering AI at Google Scale*, https://arxiv.org/abs/2508.15734 . Reported Gemini Apps median text prompt (at the measured time/service): 0.24 Wh, 0.03 gCO2e, 0.26 mL water under Google's full-stack attribution. That is *not* a universal constant, an OpenAI rate, an API low-vs-high marginal measurement, or a valid factor to multiply by token savings.
- OpenAI Academy, `Environmental Impact of AI` (updated 2026-06-09), https://academy.openai.com/en/public/clubs/higher-education-05x4z/resources/environmental-impact-of-ai . References Epoch AI's independent estimate of roughly 0.3 Wh for a *typical GPT-4o query*. This is a model-based external estimate, NOT an experimentally measured value for current ChatGPT modes or per-token energy.
- OpenAI Responses API reasoning guide, https://developers.openai.com/api/docs/guides/reasoning ; can set model-dependent `reasoning.effort`; usage includes input/output and (where available) reasoning token counts. `reasoning_tokens` may be part of output tokens, not additive. Model/version and exact usage semantics must be frozen and verified. API provides no general per-response verified data-center joules.
- Google Cloud carbon-footprint dashboard, https://docs.cloud.google.com/carbon-footprint/docs/view-carbon-data ; estimates account-based monthly cloud emissions, not per-prompt electricity in Gemini Apps. Microsoft Azure emissions impact dashboard likewise pertains to customer cloud use/accounting, not a direct meter of a particular proprietary AI service response.
- Klesel & Messer (CHI 2026), *Good for the Planet, Bad for Me?*, https://arxiv.org/abs/2603.23075 ; green information and model-choice effects already studied. Novelty cannot be merely labeling a green choice.
- Ren et al. (FAccT 2026), *EcoChat Probe*, https://doi.org/10.1145/3805689.3812368 ; environmental feedback and actual behavior already studied.

## Correct, feasible zero-purchase start

**Stage 0: No API usage or new hardware.**
- Review available hosted API models and mode/effort controls, official token usage definitions, published provider energy/environment methodologies, access/pricing/academic credits, and what remains unmeasurable.
- Make a source-quality table: **direct observable provider usage** / **public provider-side attributed average** / **externally modeled estimate** / **unavailable**.
- Write data schema and treatment conditions; design fixed tasks in at least one user context; lock consent/privacy plan in coordination with UCSB review.
- Do NOT use the user's 4070 SUPER or USC/UCSB GPU infrastructure as a required starting step.

**Stage 1: Small, spend-capped commercial API technical pilot.**
- On one provider/model (if access/credits exist), hold prompts/model constant and vary controllable reasoning/computation setting (e.g., low/high) when supported; record original response usage, wall time, success/failure, cancellations, retry counts, service conditions.
- Report **token difference** as observed. Report energy as `NOT_OBSERVED` unless there is validated provider direct energy telemetry for this exact measurement scope. Do not call output cap or shorter visible answer a confirmed lower compute budget.
- Avoid large, repeated calls without a budget cap.

**Stage 2: Hosted-service HCI experiment after approvals.**
- Same API backend, randomized label Eco vs neutral Low; identical choices and information other than label; baseline AI-specific environmental intention measured independently.
- Every session includes all calls/retries/changes/task completion. Analyze ITT label effect on full-session provider token demand, with behavioral outcomes and performance costs. Intention-to-behavior/resource associations are *not* causal; experimentally manipulated label effects are.
- Environmental consequences are secondary sensitivity analyses with transparent, provider-specific bounds where data permit; otherwise explicitly **undetermined**.

**Stage 3: Optional industry partnership.**
- A provider collaboration with raw datacenter serving-energy telemetry and allocation method can enable physically grounded low-vs-high session-energy results. Without it, the paper should NOT claim actual physical datacenter electricity saved by users choosing Eco, and should target a clear empirical HCI/measurement-consequence contribution within available evidence.

## Desired paper contribution and limits

The strongest feasible paper without company cooperation is a study of **sustainability intention vs observed commercial LLM usage and task outcomes** and a methodologically transparent account of **why token-based eco claims cannot automatically be equated with measured datacenter benefit**. A stronger physical-energy paper is conditional on provider-side instrumentation or a rigorously justified provider-specific estimation framework. Do not market it as a directly measured commercial-datacenter energy trial.

### Original local pilot reinterpretation

The local Ollama + consumer GPU plan may help test software logging mechanics, but it is optional and cannot calibrate Gemini/ChatGPT/Claude proprietary infrastructure energy. It is not the next required step.
