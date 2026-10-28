# Eco Mode — Environmental intention and measured resource consumption (focused pilot v0.1)

Date: 2026-10-28
Status: DESIGN ONLY / NOT PREREGISTERED / NO HUMAN DATA / NO ENERGY MEASUREMENT
Repository context: research/protocol-v4.md; research/v4-analysis-contract.md; research/S0-metering-spec.md. This document narrows the initial scientific question and does not replace or retroactively freeze those protocols.

## Central scientific question

**Does the intention to use AI sustainably translate into measurable reductions in computational resource consumption?**

We study the relationship between (a) intention to reduce environmental harm, (b) lower-compute mode selection, (c) subsequent retries/switching/abandonment, and (d) metered whole-session resources. An individual choosing a mode labelled Eco is not proof of environmental intent, and token savings are not proof of energy or ecological savings.

### Target estimands (do not conflate)

1. **Randomized label effect on use (causal ITT):** Eco vs Low neutral label, identical underlying low-compute option and identical High alternative. Outcomes: initial low-option choice and subsequent mode selection/switching.
2. **Randomized label effect on total consumption (causal ITT):** Eco vs Low on per-assigned-participant total session joules, and separately total provider-reported tokens. Include all requests, retries, failures, interruptions, switching, cancellations/drain and allocated idle within a fixed measurement boundary. Retain all assignments and missingness. This is *not* the causal effect of the participant's unrandomized choice of low compute.
3. **Intention–action/resource associations (NOT causal):** whether pre-measured AI-specific environmental conservation intention predicts lower-compute choice and total measured session joules/tokens, conditional on prespecified baseline task familiarity and prior AI experience. Estimate baseline-intention-by-randomized-label interactions only if sample and analysis support them.
4. **Perceived vs observed benefit (interpretive, not subtracting unlike units):** compare distributions of participants' post-task beliefs about having saved energy with aggregate randomized energy comparisons and separately measured low-vs-high technical benchmarks. Do not claim any participant's unchosen counterfactual was observed.
5. **Performance cost:** final objective task outcome, completion/abandonment, time and subjective acceptance, reported alongside every resource result. Quality non-inferiority is not a resource-result gate.

## Rationale and close precedent

Klesel & Messer, CHI 2026, DOI:10.1145/3772318.3791015, tested energy consumption disclosure, pro-environmental attitude, initial model choice, subsequent prompt use and perceptions in 365 participants. Crucially, both displayed models used GPT-4o mini; the design isolated expectation/perception, rather than differences in physically metered actual low/high compute configurations. Thus neither pro-environmental attitude moderation nor a green choice label alone is our novelty. It is a prior that must be cited and directly contrasted.
Ren et al., EcoChat Probe, FAccT 2026, DOI:10.1145/3805689.3812368, deployed energy feedback to 52 participants for four weeks, reporting reflections and no significant change in usage patterns. Our distinct candidate is end-to-end metering with an operational compute trade-off and task outcomes.

## Pilot design: two-stage, sequential

### Stage A — technical calibration (no participants)

- Select *one* accessible open model and a single serving stack, with reproducible version/seed/temperature and verified low/high inference-compute controls. Do not use mere output-length truncation as evidence of different inference budgets.
- Fix short, assessable tasks (initial candidate: beginner JavaScript function edits, evaluated by independent functional tests); do not call these representative of all AI uses.
- Repeat identical inputs under randomized/balanced low/high execution order; capture request ID, backend applied settings, response usage field semantics, wall time, output and scoring, and physically metered energy with sensor scope/lag/idle/caches documented.
- Predefine boundaries. On an allocated session, energy includes idle, all attempts and cancellation drain. If isolated per-task energy attribution is invalid, report session-only energy.
- Feasibility gates: both settings actually distinct; token schema tested against provider traces; sensor support/precision verified; task scorer/ground truth verified; runtime stable. No requirement that low must reduce energy.

### Stage B — human study (requires UCSB human-subjects review/determination before recruitment)

- Randomize at participant level to **Eco label vs Low label**. Other option High is identical across arms. Both arms have the *same factual disclosure*: low-compute may sometimes yield worse results; energy reduction is not guaranteed. No default, color/icon, location, pricing or feedback differences; counterbalance option position equally if needed.
- Collect AI-specific conservation intention ahead of treatment (ideally as a separate neutral-appearing baseline session several days before, with precautions against priming), and pre-existing AI/task familiarity. Environmental intention is measured, never inferred merely from Eco choice. Scale reliability and comprehension are piloted; do not invent validated scale status.
- Participants complete the same fixed task set under the same rules, with freedom to retry and switch mode. Log all task/request/attempt IDs, assignment, selections and switches, final success/failure/abandonment/unknown, allocation start/stop/drain and token/energy scope.
- After tasks, measure recalled performance trade-off, perceived environmental benefit, experienced satisfaction, and self-reported motive. These are post-treatment descriptions; do not condition primary ITT inclusion on them.
- Start with an IRB-cleared *usability/instrumentation pilot*, not a powered efficacy trial. Sample size for the main study must depend on independent variance/power/precision estimates and a prespecified minimum effect of interest. Do not select N from desired significance.
- No user-generated code execution without process isolation and resource controls.

## Initial question wording (draft, not validated instrument)

Baseline Likert 1–7:
- "When using AI, I would consider using a less computationally demanding option to reduce environmental impact."
- "I would accept a slower or less capable AI response when a lower-compute option could reduce environmental impact."
- "Reducing environmental impact matters to me when I choose how to use AI."
Prefer separate general environmental attitude and AI-specific intentions; avoid promising any real measured environmental benefit.

After session (distinct constructs):
- "Which factor most influenced your initial mode choice?" (environment / expected accuracy / speed / familiarity / other; multiple motives allowed)
- "I believed my mode choice reduced the energy used for this session." (1–7)
- "I was willing to accept lower answer quality in exchange for a possible reduction in resource use." (1–7)
- "How certain are you that your choice saved energy?" (1–7)
- "Did you switch modes or retry because the response was insufficient?" (confirm with behavioral logs, not self-report only)

## Analysis plan to specify BEFORE main outcomes

Primary randomized contrast: Eco minus Low in session energy (J) as a *difference of means across all randomly assigned participants*, with a two-sided interval; separately tokens. Selection rate is an additional prespecified behavioral outcome. Specify multiplicity/confirmatory-family choices explicitly before execution (existing v4 proposal: energy and tokens; selection secondary). Consider randomization/permutation or robust methods if skew/point mass dictates, with a prespecified choice rule. Cluster by participant for repeated tasks, not request count. Keep missing/invalid values as unknown; report attrition and sensitivity bounds, never silently recode energy to 0.

Baseline intention–choice and intention–energy relationships are associative, including the role of previous task skill and AI experience. Do not interpret the post-treatment selection of low as a valid mediator without further identification assumptions. Avoid a causal 'intention saves energy' claim.

Predeclare a matrix of outcomes: choice increases / energy decreases; choice increases / energy unchanged; choice increases / energy increases due to retries; no clear effects; low has lower objective quality; missing energy. Negative or inconclusive results can be valuable with sufficient precision, transparency and a distinctive contribution, not automatically publishable.

## Next evidence gates

1. Select exact tasks/population and draft a reproducible task scoring bank.
2. Secure permission for one server/GPU and identify direct metering path; record limits on time/spend; no purchases assumed.
3. Run stage A with actual raw backend/sensor traces and audit anomalies.
4. Build UI and minimal event logging, test comprehension/selection flow.
5. Obtain UCSB Human Subjects Committee determination/review before human recruitment; run independent pilot.
6. Freeze primary estimands, valid analysis, precision/power, exclusions/missing handling and stopping rule before main data.

## References

- Klesel, M. & Messer, U. (2026), *Good for the Planet, Bad for Me?* CHI. https://doi.org/10.1145/3772318.3791015
- Ren, Y. et al. (2026), *EcoChat Probe*. FAccT. https://doi.org/10.1145/3805689.3812368
- UCSB Office of Research: https://www.research.ucsb.edu/human-subjects/for-researchers

No actual empirical results are claimed in this document.
