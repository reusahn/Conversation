# Precise novel contribution — The Eco–Evidence Gap

Date: 2026-10-28
Status: testable proposed contribution, **NOT** an empirical finding. This document refines, but does not replace, `eco-placebo-factorial-protocol-v1.0.md`.

## 1. A deliberately narrow scientific claim

> **Sustainability framing may increase users' confidence that their AI use saves resources even when the interface makes no computational-effort reduction, while a genuinely lower-effort option need not reduce full-task service demand once retries, task failure and switching are included.**

We provisionally call this dissociation the **Eco–Evidence Gap** rather than implying that any specific amount of data-center energy has been measured. We must not treat this as a discovered effect, nor as the first placebo/green-label study.

The added HCI knowledge, if supported, is a **causally isolated boundary condition on the environmental meaning of an Eco mode**: when perceived savings, real backend configuration, and entire-session provider-reported demand agree or diverge.

## 2. Exactly what prior work already covers

- Klesel & Messer, CHI 2026, https://arxiv.org/html/2603.23075v1: N=365, sustainable AI disclosure affects choice; subjective quality/satisfaction placebo effect; no significant differences in follow-up number/average tokens per prompt; pro-environmental attitude and moral licensing already tested; two displayed options were run on the same GPT-4o mini. Their work cannot be described as merely measuring clicks.
- Ren et al., EcoChat Probe, FAccT 2026, https://doi.org/10.1145/3805689.3812368: field awareness/feedback and use patterns; no significant usage pattern change.
- Panigrahy et al., Energy per Successful Goal, arXiv v2 Oct 2026, https://arxiv.org/abs/2605.22883: attempts/failures/retries as goal-level costs already developed. Do not claim invention of task-level accounting.
- Kim et al., When LLMs Slow Down, Aug 2026, https://arxiv.org/abs/2608.23968: latency/carbon tradeoff willingness, eco-mindedness already studied.
- Consequently, novelty candidate is the **factorial, real commercial hosted LLM test separating framing, actual inference-setting manipulation, and holistic interaction demand with explicit belief calibration** — and not any individual ingredient by itself. Broader literature review still required.

## 3. Identification: randomized 2×2 label × actual backend

In every group Standard always means the verified High effort setting on the *same* provider/model. The alternative is randomly framed `Eco` or `Mode B`, independently of whether it uses High or Low.

| Group | Alternative label | Alternative actual effort |
|---|---|---|
| A | Mode B | High (sham) |
| B | Eco | High (sham) |
| C | Mode B | Low |
| D | Eco | Low |

All 4 groups have factual shared disclosure, no fabricated numerical carbon/energy guarantees, consistent color/icons/ordering/defaults. Only HSC-approved withholding or authorized deception before use.

### Primary discriminating contrasts

- **False effort belief in sham condition:** among randomly assigned A vs B, does the name Eco increase belief that alternative was set to use less inference computation? This *is objectively checkable*: both actually ran the same High policy. Crucially, do **not** assert each completed session used exactly equal energy or tokens merely because settings were identical.
- **End-to-end demand:** label causal ITT and backend causal ITT on *whole-session provider-reported total token usage*, with attempts, retries, switches, tasks, abandonments and unknowns kept in the assigned sample. Relevant interaction `[mean(D)-mean(C)] - [mean(B)-mean(A)]` tests whether label effect changes when a genuinely low-effort setting exists. A rigorous analysis should also display objective task success/completion and latency; successful-only ratios cannot replace all-assigned totals.
- **Belief vs evidence:** measure separately (i) belief that the alternative used reduced inference effort (testable against actual configuration); (ii) belief that data-center electricity/carbon/water were saved (not validated by API tokens). These are different constructs and must not be subtracted from token or electricity units.
- **Correction/debrief:** immediately pre/post revelation of hidden setting, report accuracy of compute-setting beliefs and participant trust. This measures immediate belief update only, and is not evidence of long-term trust or causal harm caused by lying. Additional independent disclosure randomization would be needed for distinct disclosure causal inference.

### Outcome evidence tiers
1. Verified setting applied (e.g. API low/high reasoning effort, not merely short visible answers).
2. Provider usage counters and task outcomes = **observable API demand**, not data-center joules.
3. Data-center kWh, carbon and water: `not observed` without direct validated provider energy/impact telemetry or a defensible scope-specific attribution method. Public Google Gemini estimates or OpenAI environmental materials cannot be used as an unvalidated per-token conversion factor.

## 4. What counts as a publishable finding, if shown with sufficient evidence

- **Strong positive pattern:** B vs A increases false belief of lower inference effort despite equal backend setting; D vs C changes net session token demand less than per-attempt benchmarks predict due to observable retries/switching. These constitute distinct psychological and operational divergences, not verified electricity savings.
- **Contrast pattern:** belief changes but no reliably detectable total-demand difference (with CI narrow enough to exclude the prespecified meaningful effect); shows limits of labels on observable demand.
- **Inverse pattern:** real Low backend increases total token demand or failure/abandonment; reports performance costs, does not automatically label 'rebound energy'.
- **Null/uncertain:** no narrow discrimination => no claimed gap; a publishable contribution cannot be guaranteed.

## 5. Single-sentence contribution for Introduction

> *We experimentally disentangle sustainability labels from actual inference-effort controls in a commercially hosted LLM, revealing whether—and under what task and interaction conditions—users' beliefs about resource savings track the backend configuration and full-session API demand.*

This sentence expresses **what the paper tests**; replace 'revealing whether' with specific findings only after data collection.

## 6. Minimal study requirements / risks

- Secure commercial model API effort control and version/prompt logging, verify usage field inclusion semantics and meaningful low/high backend variation; prohibit unbounded costs.
- Pretest factual task bank and goal-completion metrics, and separate initial choice from post-response behavior. Set participant as randomization/analysis unit.
- Pilot environmental expectation manipulation without exposing to unapproved deceptive procedures. Establish effect/variance for sample size and correct multiplicity before confirmatory main study.
- Receive UCSB HSC determination with faculty researcher, consent/authorized deception and approved debrief. Never recruit before approval. Do not imply later publication alone legitimates deception.
- If company energy data is inaccessible, bound the scientific contribution to behavior, setting, tokens, task performance and misperceptions — do NOT use 'real data-center savings' in a result claim.

## 7. Reviewer decision test

A strong CHI contribution must answer: **What causal contrast about environmentally framed hosted AI can we establish that CHI 2026, EcoChat and agentic goal accounting did not already establish?**

Answer: the **independent causal contrast of label vs *actually changed* hosted model effort and its *whole-session* demand, linked to verifiably mistaken beliefs about the backend**. It remains a novel-contribution *candidate*, contingent on broader literature search and empirical evidence.

