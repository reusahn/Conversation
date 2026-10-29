# The Illusion of Sustainable AI — Research Protocol v1.0

**Status (2026-10-28): study design only. Not preregistered, not approved by UCSB HSC, no recruited participants, no commercial-API measurements, no measured datacenter electricity, carbon or water.**
**Paper candidate:** *The Illusion of Sustainable AI: How Eco Labels and Actual Computational Effort Shape User Behavior, Environmental Beliefs, and Resource Demand in Commercial LLMs*
**Researchers:** Independent PhD-led proposal; faculty responsible investigator to be identified for UCSB ORahs.
**Relationship to earlier repo:** Refines `research/protocol-v4.md`, `research/hosted-llm-datacenter-study-v0.2.md`. The local GPU pilot is not the central experiment.

## 1. Central question and contribution limits

When a user is inclined to protect the environment, does an Eco-framed option on a commercial hosted LLM cause (a) different mode choices, (b) different full-session API-reported token demand and task outcomes, and (c) different beliefs about saving resources, even when an Eco-labeled alternative provides no lower-compute backend?

Crucial distinction: the behavioral label effect is *randomized* and can be estimated causally; baseline environmental intention is *measured*, so intention-to-behavior relationships are observational. Commercial API tokens are not a physical meter of data center power, carbon, water, or ecological damage. Low reasoning effort is a configuration, not a certified eco benefit.

### Closest prior work

Klesel & Messer, CHI 2026, https://arxiv.org/html/2603.23075v1, DOI 10.1145/3772318.3791015:
N=365; energy disclosure led to more pro-environmental model choice; follow-up prompt behavior showed no significant difference; subjective quality/satisfaction placebo effect; both purported model options used the same GPT-4o mini. Their paper *already* examined environmental attitude, choice, prompt number/length and expectation-induced perception. We cannot claim novelty merely from eco labels, placebo selection or attitudes.
Ren et al., EcoChat Probe, FAccT 2026, https://doi.org/10.1145/3805689.3812368: environmental feedback and usage, prior art.
Potential added contribution: a randomized **label × actual hosted reasoning configuration** test, with explicit sham condition, complete attempt-level provider usage and task outcomes, followed by approved disclosure and examination of belief calibration/trust. The 2×2 interaction and whole-session token measurement are novel *candidates* pending broader literature review and feasible model API.

## 2. Study design (preferred): 2×2 between-participant factorial

All participants see two selectable research assistant modes: **Standard** and an **alternative**. Standard always maps to a fixed high-effort policy, within a version-pinned *same commercial hosted model*.

Randomize participant to two hidden independent factors:
- **L (wording):** alternative appears as `Eco` (L=1), or an emotionally neutral `Mode B` (L=0).
- **B (actual backend):** alternative maps to lower-effort inference setting (B=1), or the same high-effort backend as Standard (B=0, sham).

| Arm | Visible modes | Alternative backend | Scientific role |
| A Neutral+Sham | Standard / Mode B | High (same as Standard) | Neutral/placebo control |
| B Eco+Sham | Standard / Eco | High (same as Standard) | Label-only 'Eco placebo' |
| C Neutral+Real-Lower | Standard / Mode B | Low | Real setting without eco framing |
| D Eco+Real-Lower | Standard / Eco | Low | Eco framing + genuine lower inference effort |

This is deliberately **not** 4 distinct provider models. A/B differ in words only. B/D differ in actual low/high setting, but cannot be asserted to differ in metered electricity without provider-side measurements.

Important first-choice detail: backend assignment cannot affect initial mode choice if it is invisible and no outputs have been observed. Therefore first-choice analysis tests LABEL, not actual backend. Backend can affect retries, subsequent switching, quality, duration, and tokens after interaction; report all assigned participants including those who never selected alternative (ITT). Among initial alternative choosers, backend comparison is randomized prior to first output, but selection after seeing label still complicates cross-label interpretation. Treat as a prespecified auxiliary contrast if justified.

### Ethical screen

This is a proposed **incomplete disclosure / potentially active deception** design. Do not give false quantitative eco guarantees; do not assert that alternative is physically energy-saving. Only use the names `Eco` or `Mode B` with identical truthful disclosure in all arms: *"Modes can differ in how they generate responses. Response quality and resource usage may vary; an environmental saving is not guaranteed."* Participants should not be told their backend arm before data collection if IRB authorizes the withholding. Wording including the upfront authorized-deception disclosure itself must be approved by UCSB HSC, not independently implemented as a trick. If not permitted, run a non-deceptive alternative with generic label framing and explicitly explain the randomization; assess this as a different estimand.

Keep icon, color, order, default selection, latency feedback, pricing, prompts, UI and factual disclosures identical except `Eco` vs `Mode B`. Neutral name chosen with pilot to avoid associations (e.g. Mode B).

## 3. Preregisterable research questions / hypotheses

RQ1 (Choice): Does Eco labeling increase initial selection of the alternative, as compared with neutral Mode B?
**H1 (directional):** randomly assigned Eco label increases initial alternative-choice probability. Main intention-to-treat (ITT) mean proportion difference by label.

RQ2 (Behavior/resources): How do label and actual inference effort affect the **total provider-reported tokens per randomized session**, requests, retries, switching, abandonment, task completion and latency? 
**H2a (technical hypothesis):** low-effort backend changes provider-reported token demand compared with high under the same prompts; likely lower per attempt but may not reduce whole-session demand. Prespecify token inclusion semantics and two-sided ITT estimation of backend effect rather than promising decreases.
**H2b (exploratory interaction):** does eco label change the effect of lower effort on whole-session token demand due to retries, switches or abandonment? A label×backend interaction is causal if randomization/implementation succeeds.

RQ3 (Belief/placebo): With an identical high backend, does labeling the alternative Eco increase *belief that energy was saved* and willingness to accept worse performance? 
**H3 (directional secondary):** among the SHAM-backend arms, Eco label increases claimed environmental benefit despite no verified lower compute. It does not prove per-session physical energy equality.

RQ4 (Disclosure & trust): How do participants update perceived environmental benefit and trust after learning the truth about the labels and hidden backend assignment? 
Exploratory pre/post debrief trust change; interpret carefully as immediate reactions, not long-term trust or as an automatically identified causal effect of deception itself. Need approved scripted debrief and data-removal procedure.

RQ5 (Intention–action gap): Do pre-treatment AI-specific environmental intention and acceptance of a performance tradeoff predict choice, retries, and measured token demand, and does randomized label moderate these associations? 
Correlational associations for intention; no claim environmental intention causally reduces electricity.

## 4. Outcomes, measurement validity, analysis

**Proposed confirmatory endpoints** (final choice before data):
1. Initial choice of alternative, analyzed by randomly assigned label (Eco vs Mode B).
2. Whole-session **provider-reported total token usage**, analyzed as label and backend ITT (and if sample permits the interaction) with preregistered model and multiplicity strategy.

Additional planned outcomes: alternative use share; logical requests vs backend attempts; within-task retry/switch; objectively scored outcomes per task; final completion/abandonment/unknown; duration; satisfaction; perceived environmental benefit; acceptability of performance tradeoff; trust just before and after debrief. No 'energy saved' label on an API token result.

Data keys: participant_pseudonym, assignment_label, assignment_backend, task_id, request_id, attempt_id, mode_selected, model_snapshot, reasoning_effort_requested/actual when verifiable, response_status, input_tokens, cached_input_tokens_subset, output_tokens, reasoning_tokens_subset, provider_total_tokens, latency, task_success/unknown, cancellation/drain. Use authoritative final usage once per attempt; never add subset fields to parent fields twice. Unreported fields are null.

Participant = independent unit; repeated prompts are clustered within participant. Include all randomized participants in primary ITT; report missingness and censoring separately (technical failure != zero energy or zero tokens). For binary choice use risk difference with confidence interval, with randomization-aware standard errors; for skewed tokens use prespecified robust uncertainty method, with participant-level randomization/block assignment; never choose tests after observing an attractive result. Predefine family-wise error handling (e.g. Holm for two confirmatory comparisons); interactions and moderation exploratory unless separately powered/preregistered. The sample size is **TBD after external pilot variance and minimum effect of interest**, not invented.

The task bank must be independently tested and objective (e.g. pre-authored functional JS tasks, not code submitted by subjects to unsafe execution; or fixed factual QA). Predetermine task time cap and optional retries. Do not convert poorer task success into 'efficiency improvement'. No external private prompts; avoid personal data sent to provider APIs.

## 5. Distinct evidence tiers for environment

Tier 1 **observed in our hosted experiment**: commercial API requests, model/mode settings, provider usage counters, latency, task behavior/quality. Token metrics do not directly quantify FLOPs or facility energy.
Tier 2 **published conditional references**: Google 2025 Gemini Apps fleet-attributed 0.24 Wh median prompt, etc., https://arxiv.org/abs/2508.15734. This is a different measured population/time/stack. Never multiply by our token reduction to infer ChatGPT energy or participant CO2. Public company-wide totals cannot establish per-mode counterfactual effects.
Tier 3 **physically attributable provider energy**: requires cooperation/privileged provider telemetry with actual attributable serving energy, idle, CPU, cooling and time/location energy mix as relevant. Without it, result is `energy_not_observed`, not 'no savings' or 'no environmental impact'.

## 6. UCSB HSC/IRB and participant protections

- Discuss protocol with UCSB Human Subjects Office *before any recruitment/actual subjects*: https://www.research.ucsb.edu/human-subjects/for-researchers and hsc@research.ucsb.edu.
- UCSB distinguishes **active deception** from **incomplete disclosure**: https://www.research.ucsb.edu/human-subjects/orahs-definitions. Avoid claiming this study is exempt on one's own authority.
- 45 CFR 46.104(d)(3)(iii) allows a particular benign behavioral interventions exemption involving deception only when subjects give prospective authorization to participate in circumstances where they may be unaware of or misled about the study's nature/purposes; HSC determines applicability. https://www.law.cornell.edu/cfr/text/45/46.104
- Prepare: scientific necessity of withheld implementation; lowest-risk alternative considered; prospective information/authorized deception; age 18+ adults; voluntary participation/withdrawal, appropriate compensation; no false carbon savings promises; exact debrief that explains hidden sham/real backend and that real lower reasoning effort **does not prove lower facility power**; privacy, retention and withdrawal/deletion policy per HSC, with practical pseudonym linkage.
- All online survey questions should allow skipping in accordance with UCSB FAQ. No covert collection from real ChatGPT users.
- Student investigators are ORahs **Associate** users and cannot directly submit a protocol without an eligible faculty researcher account: https://www.research.ucsb.edu/human-subjects/orahs-definitions.
- Required human-subjects research training for all researchers: https://www.research.ucsb.edu/human-subjects-faqs.
- Submit final scripts, mock UI, randomization details, task bank, surveys, backend model endpoints, storage plan, recruitment, risk mitigation, and debrief for committee determination.

## 7. Approved-only example debrief content

'In this study, the name shown for one AI mode and its technical setting were independently assigned. Some participants saw a mode named Eco even though it used the same inference setting as Standard. Other participants used a lower-reasoning setting; that setting has not been independently verified to save data-center electricity or carbon. We withheld the exact mapping until now to examine how labels shape decisions and perceptions. We are studying AI usage and beliefs, not measuring your personal environmental impact. [HSC-approved data withdrawal contact and procedure].'

Do not use until approved by HSC.

## 8. Work packages / gates

G0: literature matrix, research claims, task bank/score, factorial randomization and outcome definitions.
G1: commercial API model/effort support, usage correctness, version pinning, authorization, capped provider credits/cost. Technical dry-run with NO subjects, including low vs high quality/usage comparison.
G2: design/faculty review + UCSB Human Subjects Committee determination/approval before any human-facing test, recruitment or personal data collection.
G3: independent comprehension/usability pilot as approved; revise and preregister final analysis, minimum effect/precision/sample/stopping.
G4: run main experiment and produce frozen analysis; disclose all positive/null/contrary outcomes and interpretation constraints.
G5: write actual Findings/Discussion; submit to CHI or other appropriate HCI venue. Current empirical results are zero.

## Paper outline

1. Introduction: sustainability intentions, eco naming, provider-side opacity
2. Related Work: CHI 2026 (Klesel & Messer), FAccT EcoChat, placebo effects, AI effort metering / sustainability claims
3. Research questions and factorial design
4. System / hosted API behavior and logging contract
5. UCSB-approved participant procedure and debrief
6. Pre-registered statistical methods
7. Results (pending)
8. Discussion: beliefs vs observable resource demand; limitations of energy inference
9. Conclusion (pending)

## References

- https://arxiv.org/html/2603.23075v1
- https://doi.org/10.1145/3805689.3812368
- https://developers.openai.com/api/docs/guides/reasoning
- https://developers.openai.com/api/docs/guides/token-counting
- https://arxiv.org/abs/2508.15734
- https://www.research.ucsb.edu/human-subjects/orahs-definitions
- https://www.research.ucsb.edu/human-subjects/for-researchers
- https://www.research.ucsb.edu/human-subjects-faqs
- https://www.law.cornell.edu/cfr/text/45/46.104

## 9. Research readiness review rubric (100-point planning aid; not a CHI prediction)

| Criterion | Points | Evidence needed |
|---|---:|---|
| Distinct contribution beyond CHI 2026 | 20 | comparison matrix, grounded new question and outcomes, broadened literature review |
| Causal identification and treatment fidelity | 20 | independently randomized 2×2 cells, untouched label-only contrast, verified backend configuration, preregistered comparisons |
| Measurement and task quality | 20 | full-session attempt-level actual provider usage, subset semantics, objective outcomes, missingness/retry rules, NO conflation with joules |
| Human-subject protection | 20 | faculty researcher/HSC determination, prospective authorization as required, exact consent/debrief, privacy/withdrawal protections |
| Statistics and reproducibility | 20 | feasible sample/power from independent pilot, fixed analysis family, uncertainty intervals, releaseable scripts and nonidentifying outputs |

A high design-review score never certifies actual conservation or publication. **No numerical score is assigned yet**; readiness requires real evidence of the relevant gate. This is a project self-audit, not a claim of independent reviewer evaluation.
