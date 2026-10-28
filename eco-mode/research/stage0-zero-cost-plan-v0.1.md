> **Scope correction (2026-10-28):** The intended research targets commercially hosted LLM services (ChatGPT/Gemini/Claude) and their data-center resource/environmental impacts. This local GPU plan is OPTIONAL tooling validation, not the primary study or required first step. Consult [hosted-llm-datacenter-study-v0.2.md](hosted-llm-datacenter-study-v0.2.md). No local GPU measurement may be represented as hosted-provider energy or emissions evidence.

# Stage 0 — zero-API-cost local feasibility plan (2026-10-28)

Status: method/instrumentation only; no empirical energy or human-subject results.

## Decision

Do **not** purchase GPU time, subscribe to an inference API or recruit people yet. First use local Ollama + Qwen3 0.6B with `think=false` versus `think=true` as a minimal **on/off thinking instrumentation smoke test**. It is not a validated low/high compute-budget intervention, and a successful smoke test does not certify energy savings.

Official model: https://ollama.com/library/qwen3:0.6b (523 MB model download). Ollama docs: https://docs.ollama.com/quickstart and https://github.com/ollama/ollama/blob/main/docs/capabilities/thinking.mdx.

1. Install and launch Ollama locally. Run `ollama pull qwen3:0.6b`.
2. Use a Python standard-library-only script to send identical prompts to the local `/api/chat` endpoint, `stream=false`, `think=false/true`, identical generation parameters and randomized/balanced order. Verify the model's support via `/api/show`. Start with 2 simple objectively checkable smoke tasks (arithmetic and JavaScript output), repeated twice per condition. These are NOT the final participant task bank.
3. Record model tag/digest, machine OS, timestamp, experiment config, task ID, condition, prompt, answer, requested control, provider-reported prompt_eval_count/eval_count, durations, termination status, exact-match score, error and missingness. Do not add cache/reasoning components to counts if they are already included in the provider field. Do not treat output text length as internal thinking token count.
4. Report `energy_j=null` and `energy_status=NOT_MEASURED`. CPU-only execution does not mean energy was measured. Report completion failures and output caps rather than silently excluding them. Do not publish the smoke data as an ecological outcome.
5. If the local computer cannot run the model, stop without purchases and investigate **UCSB CSC Pod/Knot** campus-available resources (reported free; access still must be confirmed) and whether a suitable GPU energy interface is supported. Sources: https://csc.cnsi.ucsb.edu/get-started and https://rcd.ucsb.edu/resources/computing-resources/compute-centers.

## Gate for Stage 1 energy metering

Choose a stable, dedicated and authorized machine and a documented sensor boundary (e.g. GPU NVML total energy if supported on the device; otherwise measured sampled power with explicitly stated limitations). Verify actual applied model controls, complete attempts/drain, idle energy, timestamps, sampling lag, baseline, repeated trials and uncertainties. Never call a token count or duration a measured joule. On shared Colab/GPU infrastructure, metering attribution can be unreliable. Cloud free tiers can vary and do not guarantee accelerators.

## Gate for human study

Only after backend, scoring and metering work, obtain UCSB human-subjects determination/review and conduct an independent usability pilot. Randomize Eco vs Low *labels* on an otherwise identical low-compute backend; measure environmental intention separately and before treatment. Distinguish randomized label total effect from observational intention associations and never claim causality from self-reported motives alone.

## Current evidence/status

No actual model run by the assistant, no physically measured joules, no validated low/high computation budgets, no human data, no preregistration. The local smoke script has been syntax-tested and exercised against a mock Ollama API, not a running model. Existing v4 analysis/synthetic fixture results are not empirical evidence.
