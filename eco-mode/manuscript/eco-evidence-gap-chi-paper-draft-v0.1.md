# The Eco–Evidence Gap: Sustainability Framing, Inference Effort, and Resource Beliefs in Commercial LLMs

**Working manuscript v0.1 — 28 October 2026**

**STATUS: PRE-EMPIRICAL DRAFT.** This manuscript is a proposed study, not a completed CHI paper. No participants have been recruited, no approval or exemption has been received from the UCSB Human Subjects Committee, no commercial API trials have been conducted for this study, and no provider-level electricity, carbon or water measurements have been collected. The Introduction and Related Work may be developed now; the empirical Methods must be revised to reflect an approved and actually implemented procedure. Results and empirical Conclusions cannot yet be written.

**Review-anonymization note:** This working document is kept in an attributable GitHub repository for project development. Do not submit an unmodified link as anonymous CHI supplementary material. University identity, location of the IRB, metadata, source repository and other identifying information must be anonymized before an anonymous review submission.

## Abstract (proposal; 137 words)

As conversational AI services introduce user-facing controls over model capabilities and reasoning effort, sustainability-oriented labels may shape choices without establishing the environmental consequences of those choices. Prior research has shown that energy disclosures influence model selection and subjective evaluations, but it remains unclear how such effects interact with operational inference-effort settings over the course of completing a task. We propose a preregistered, between-participants 2 × 2 experiment that independently varies an alternative mode’s label (Eco versus neutral) and its actual hosted-API reasoning-effort setting (lower versus standard). We examine initial choice, beliefs about computational and environmental savings, retries, mode switching, task completion, and provider-reported tokens accumulated across entire sessions. By separating experimentally verified interface and configuration effects from inaccessible data-center electricity measurements, the study aims to clarify the evidentiary boundaries of sustainability claims in commercial AI interfaces.

**Keywords:** Sustainable HCI; Human–AI Interaction; Generative AI; Sustainability Framing; Placebo Effects; Resource Transparency; Reasoning Effort.

## 1. Introduction

A person opening a conversational AI interface is rarely asked how much computation their question should consume. The interface is designed to make a remote and technically complicated service feel immediate: the user types a request, receives a response, and may try again until the outcome is satisfactory. The computational resources involved in generating each response are mostly concealed behind the interface. When services introduce options such as “fast,” “thinking,” or “eco,” however, the names of these options can become part of the user's understanding of what their interaction costs.

An Eco label presents an especially consequential promise, even when no quantitative promise is made explicitly. It suggests that choosing one option over another is a way to act responsibly toward the environment. A user who values environmental protection may be willing to accept lower performance, slower responses, or additional effort in order to make this choice. Yet the relation between this intention and its material consequences is not straightforward. The same goal can require one request or many. A less capable answer may cause a user to regenerate it, reformulate the problem, switch to a higher-effort mode, or abandon the task. A mode that appears economical at the level of one model invocation may therefore have a different pattern of resource demand at the level of a completed or abandoned user goal.

Existing sustainable-HCI research establishes that environmental information can change how people choose and evaluate AI systems. Klesel and Messer [1], in a CHI 2026 experiment involving 365 participants, found that energy-consumption disclosure increased selection of a purportedly more efficient model option. They did not observe a significant change in subsequent prompting behavior, but they did identify a perceptual effect in which users who selected the purportedly eco-friendly option rated its quality and satisfaction more negatively. Importantly, the compared options were implemented using the same GPT-4o mini backend. Their experimental design made it possible to isolate expectations, while leaving the consequences of genuinely different inference-effort settings beyond its scope. It would therefore be inaccurate to position the present work as the first study of environmentally motivated AI choice, green labels, or placebo effects in generative AI.

A second line of research examines the communication and accounting of AI's environmental costs. Ren and colleagues' EcoChat probe [2] placed estimated energy and emissions feedback in a ChatGPT browser experience and investigated how users interpreted this feedback in everyday use. Work on energy per successful goal [3] further challenges measurements based on an isolated invocation by accounting for the attempts, failures, and retries involved in achieving a goal. Together, these studies motivate a distinction between three objects that can be easily conflated: what the interface leads a user to believe, what computational setting the service applies, and what total resources an interaction actually demands.

We call the potential discrepancy among these objects the **Eco–Evidence Gap**. The term does not denote a finding already established by this project. It identifies a relationship to be tested: a sustainability-framed option may produce a belief that fewer resources were used even when no lower-effort setting is applied, while applying a lower-effort setting may have a more complicated relationship with full-session usage once users respond to incomplete or unsatisfactory outputs. We focus on the boundary conditions under which these two aspects of an Eco interface align or diverge.

To investigate this relationship, we propose a factorial experiment embedded in a research chat interface connected to a commercial hosted large language model (LLM). We independently randomize (1) whether an alternative mode is called **Eco** or assigned a neutral name and (2) whether that alternative invokes the same standard reasoning-effort policy as the baseline or a lower-effort policy of the same hosted model. This design separates the causal effect of the label from the causal effect of a change in the requested inference setting. It also makes it possible to examine whether labeling changes the usage consequences of introducing a lower-effort policy.

Our study deliberately avoids equating provider-reported token usage with measured data-center electricity. Commercial APIs can expose requests, response status, timing, and token counters, but generally do not expose a validated attribution of electricity, emissions, or water to individual requests. Google researchers have demonstrated that full-stack serving energy accounting requires information about accelerators, host machines, idle capacity, and data-center overhead [4]. Those measurements cannot be transferred to another provider or experimental setting by multiplying a generic energy-per-token constant. We therefore examine **observable service demand** and users' environmental beliefs, while explicitly marking physical electricity and emissions outcomes as unobserved unless suitable provider-specific evidence becomes available.

The proposed work seeks to establish a boundary condition for sustainable AI interface design: **does the influence of an Eco label on beliefs and whole-session computational demand depend on whether a lower-effort option actually exists?** The answer could reveal a gap, close one, or show that its magnitude depends on task characteristics. The contribution must ultimately be established through empirical results rather than inferred from the design alone.

## 2. Related Work

### 2.1 Sustainability disclosures and AI choice

Environmental information is increasingly presented as a possible intervention in the use of generative AI. In their controlled CHI study, Klesel and Messer [1] investigated energy-consumption disclosure and the associated model-choice and perceptual effects. Their findings established that a seemingly greener model choice can arise from an interface disclosure, and that performance-related expectations can affect subjective assessments even without a corresponding change in backend model. Their study also examined downstream prompting behavior. These results leave little justification for claiming that an Eco label's influence on initial choice or perceived quality is, in itself, an original discovery.

The present study therefore treats the label-only comparison as a necessary baseline and extends the experimental design to an independently manipulated hosted reasoning-effort policy. This operational distinction matters because it permits examination of both a **sham Eco** option, in which the alternative retains the standard policy, and a **lower-effort Eco** option, in which the API is instructed to use a different effort level. The scientific question is not simply whether one label attracts more clicks, but whether its consequences for subsequent interaction and total reported demand change when the underlying service policy changes.

### 2.2 Environmental feedback and user interpretation

Ren et al. [2] developed EcoChat, a browser-based technology probe for communicating estimated inference energy and emissions in a ChatGPT interface. Their four-week field deployment involved 52 participants and was supplemented by 18 interviews. This work demonstrates that resource information can become material for reflection even where changes to usage patterns are not evident. Importantly, users' interpretations of numerical environmental indicators depend on the framing and context in which those estimates are communicated.

Building on this work, we distinguish a belief that an AI mode used a **lower reasoning-effort setting**, which can be compared with an experimentally assigned API policy, from a belief that using the mode **saved data-center electricity or carbon**, which cannot be validated from API token records alone. This difference between the object of belief and the available evidence is central to our investigation.

### 2.3 From request-level to goal-level resource demand

A single request is not necessarily the right unit for understanding the practical cost of interaction. An inadequate answer may trigger another request, while an apparently successful answer may end the task. Panigrahy and Tyagi's goal-level accounting work [3] makes a related argument in the context of agentic systems, incorporating retries and failed attempts into energy accounting. We do not propose to invent the notion of task-level accounting. Instead, we apply this logic to **human-controlled mode choices**, comparing how labeling and actual effort settings jointly shape a participant's sequence of requests, retries, switches, and eventual task outcomes.

Unlike energy studies with access to physical hardware measurements, our initial commercial-API design measures provider-reported tokens across a defined session. Token counts are an observable measure of service usage, but they do not uniquely determine energy consumed by shared, possibly heterogeneous provider infrastructure.

### 2.4 The measurement boundary of hosted AI

Elsworth et al. [4] describe full-stack environmental accounting for Google's production AI serving infrastructure, incorporating active compute, host systems, idle capacity, and overhead. Such accounting is important for interpreting claims about AI's physical footprint. The availability of published median environmental figures does not imply that an external researcher can measure the marginal effect of a selected mode on an individual commercial API call.

We therefore distinguish three measurement tiers: (i) intervention assignment and verifiable request/usage records, (ii) conditional environment-impact estimates with disclosed provenance and assumptions, and (iii) direct, provider-attributable energy measurement. Only the first is assumed feasible in the present study; the second would be explicitly exploratory, and the third requires additional provider-side access.

## 3. Research Questions

The overarching question is:

**RQ: Does the effect of sustainability framing on users' beliefs and full-session computational demand depend on whether a hosted AI service actually applies a lower inference-effort policy?**

We operationalize this question in three parts.

**RQ1 — Label and belief.** When the alternative uses the same reasoning-effort policy as the Standard option, does calling it Eco increase users' belief that a lower-effort setting was used? We hypothesize that Eco labeling will increase this belief compared with a neutral name. This is a directional, experimentally testable prediction about the **setting**, not a verified reduction in electricity.

**RQ2 — Label × backend and session demand.** Does the effect of an Eco label on total provider-reported session tokens differ when the alternative uses a lower rather than standard reasoning-effort policy? We test this factorial interaction without prescribing its sign. Retries, mode switches, response failures, completion, and abandonment are recorded as complementary behavioral and performance outcomes.

**RQ3 — Choice and interpretation.** How are pre-existing environmental intentions associated with initial option choice, subsequent behavior, and beliefs about having saved resources? We treat environmental intention as a measured covariate rather than a randomized cause. Immediate belief correction and trust following approved disclosure of experimental conditions are considered exploratory outcomes.

## 4. Proposed Study Design

### 4.1 Factorial conditions

We propose a between-participants 2 × 2 factorial design. Every participant sees the same baseline option, **Standard**, which requests a prespecified higher reasoning-effort policy from one version-pinned commercially hosted model. The alternative option differs along two independently randomized dimensions:

1. **Label:** “Eco” versus a pilot-tested neutral name (“Mode B”).
2. **Applied API policy:** the same higher-effort policy as Standard (**sham**) versus an API-supported lower-effort policy (**lower**).

| Condition | Alternative's visible name | Alternative's requested backend policy |
|---|---|---|
| A: Neutral / Sham | Mode B | Standard-effort policy |
| B: Eco / Sham | Eco | Standard-effort policy |
| C: Neutral / Lower | Mode B | Lower-effort policy |
| D: Eco / Lower | Eco | Lower-effort policy |

These are experimental terms, not commercial product claims. The lower policy must be verified as supported and correctly requested on the selected model. A lower API effort setting is not itself evidence of a particular change in physical FLOPs or data-center joules.

Color, iconography, display position, price, model identity, explanations, and task content must be identical across groups other than the assigned label. Participants must not be told that Eco **guarantees** electricity or carbon savings. Information withheld about the alternative's actual mapping, if any, must be permitted under the approved human-subjects protocol.

### 4.2 Free choice followed by task interaction

Participants first select which mode they would like to use for a task, before seeing generated content. Because the hidden backend setting has not yet affected the interface at this point, the initial choice primarily identifies the randomized **label effect**. It would be inappropriate to interpret an effect of the hidden backend on this first click absent leakage or other design failure.

Participants then attempt a fixed set of tasks, with optional retries and switches. Each task has a predefined objective success criterion and a time limit determined in an independent pilot. The sequence of requests and switches is logged rather than restricted to one model invocation per task. A separate, later **assigned-mode calibration block** may be added to ensure exposure to the lower policy, but must be clearly distinguished from the freely chosen interaction block: forcing exposure would change the behavioral estimand and could contaminate later preferences.

The first task-domain candidate is short, objectively assessable JavaScript repair, supported by existing experimental scoring tools in the project repository. This limits generalization to participants with relevant programming knowledge. Summarization or broader conversational use would require a separate validated evaluation instrument and could be studied as replication rather than mixed into the first confirmatory design.

### 4.3 Measures and operational definitions

**Baseline intentions.** Before exposure to assigned labels, collect a brief, independently tested measure of AI-specific willingness to reduce environmental costs, alongside AI familiarity and relevant task skill. Administering these questions well ahead of the mode-choice task, if feasible, can reduce immediate priming. Statements about users' motives must not be inferred solely from their mode choice.

**Initial behavior.** Record the first mode chosen as a binary choice of alternative versus Standard. A participant can select Eco for reasons unrelated to the environment; this interpretation is assessed separately.

**Whole-session service demand.** Record participant ID, task ID, request ID, backend attempt ID, intended and verified setting, submitted content, response status, provider-reported input and output token counts, any available reasoning-token subsets, timing, retries, and transitions. Use the authoritative usage event once, without adding a subset such as reasoning tokens to its already inclusive parent count. A session begins at the prespecified trial start and ends only after the relevant backend executions have completed or been canceled according to the logging policy. Unreported provider usage is missing, not zero.

**Task outcomes.** Record final objective success, task completion, failure, abandonment, unknown outcome, elapsed time, and performance-related dissatisfaction. Keep unsuccessful and abandoned tasks in the assigned-participant denominator. Lower token demand accompanied by fewer completed goals must not be called greater efficiency at equal task performance.

**Beliefs.** Distinguish (a) whether the participant believes a lower inference-effort setting was applied and (b) whether the participant believes actual data-center energy or emissions were reduced. The first can be compared with assigned technical settings. The second cannot be established as true or false using API token information alone. Also assess confidence, experienced quality, and willingness to accept possible performance costs.

**Disclosure response.** If approved by the ethics committee, explain the true label and backend assignment after the primary measurements. Measure immediate updating of setting beliefs and trust before and after disclosure; do not describe these as long-run trust outcomes or a causal effect of “deception” without an appropriate comparison.

### 4.4 Hosted model feasibility and privacy

Before any human study, the selected commercial API, model snapshot, effort policy, rate limits, and token usage schema must be tested with fixed nonparticipant prompts. Technical dry runs must verify supported effort settings, request/response semantics, incomplete responses, and whether a model change or caching policy would invalidate comparisons. Prompt and response logs must avoid unnecessary personal data. User-generated executable code, if included, requires sandbox isolation and resource limits. Expenditure must be capped before API trials.

### 4.5 Research ethics

This protocol may involve incomplete disclosure and could qualify as active deception depending on how the Eco label and hidden mappings are presented. Such procedures cannot be initiated merely because investigators intend to explain them in the eventual paper. A qualified faculty investigator and the university's Human Subjects Committee must determine applicable review, prospective consent or authorization, approved wording, debriefing, retention, and withdrawal procedures before recruitment or use of participant data. An alternative fully disclosed condition must be considered if the sham manipulation is not approved. Participants must not be given knowingly false quantitative environmental-saving guarantees.

## 5. Planned Analysis

The **participant** is the randomization and independent analysis unit; multiple prompts are not treated as multiple participants. Analyses should preserve all randomized participants and report missingness and technical failures. A pilot will establish feasible sample size and precision, including the additional power needed to estimate an interaction. Neither the minimum effect of interest nor final sample size is specified at this stage.

Let Y_A, Y_B, Y_C, and Y_D denote group means of full-session provider-reported tokens. The proposed primary factorial contrast is:

**Interaction = (Y_D − Y_C) − (Y_B − Y_A).**

This tests whether the Eco-label effect on total reported tokens differs when the alternative is configured with lower versus standard reasoning effort. The contrast is interpretable as a randomized intention-to-treat effect when assignment and logging are valid, even for participants who never select the alternative; limited take-up may reduce the estimable effect. We will preregister the confidence-interval procedure, treatment contrasts, and multiplicity control before the main study. Initial choice and sham-condition setting beliefs will be prespecified key outcomes, with hierarchy determined after an independent feasibility pilot.

The distribution of tokens may be skewed, and some sessions may generate no usable response. Therefore, an appropriate robust or randomization-based analysis and missing-data sensitivity checks must be selected prospectively. Observed retries and mode switches may help interpret an interaction but cannot, without additional causal assumptions, establish that retries are the unique mediator of any resource effect. Task success, latency, and abandonment must be reported next to all token outcomes.

Analyses linking baseline environmental intention with choice or usage are associative. No inference about a causal effect of intention is warranted merely because the label and backend were randomized.

## 6. Possible Findings and Interpretation (NOT RESULTS)

The design allows multiple substantively different findings, none of which is presupposed.

First, Eco labeling could increase belief in lower computation in the sham condition, even though both options request the same standard-effort policy. This would demonstrate a measurable miscalibration concerning the *technical setting*. It would not prove that the same exact number of tokens or joules was used in every stochastic request.

Second, a lower-effort option could reduce provider-reported tokens per attempt but have a smaller effect on whole-session token demand if people retry, switch modes, or continue longer. Conversely, it might reduce whole-session demand without material performance loss. Either result would help characterize the circumstances in which a lower-effort control has practical consequences.

Third, the label × backend interaction may be small or absent. A precisely estimated interaction close to zero could bound how much eco framing changes the token-demand consequences of a genuine lower-effort option. An imprecise nonsignificant result would not establish equivalence.

Finally, users may report that they protected the environment despite a lack of physical energy evidence. This result should be framed as confidence in an **unverified environmental benefit**, not proof that their belief was false. Only externally validated, configuration-specific electricity attribution could adjudicate the physical claim.

## 7. Discussion Agenda: What Would This Contribute?

A completed study could contribute empirical evidence about **when environmental branding aligns or diverges with observable technical controls and user behavior**. The HCI insight would be a boundary condition on the design of resource-oriented mode choices, not a universal claim that Eco labels constitute greenwashing or that low reasoning effort always saves energy.

If supported, the results may motivate three design principles: explain what a mode actually controls; show users the uncertainty and limits of environmental claims; and account for a whole goal, including corrective interaction, rather than presenting invocation-level claims as task-level benefits. These remain provisional implications to be revised or removed in light of the findings.

The principal limitation is the opaqueness of commercial AI infrastructure. Our API instrumentation measures reported usage, not physical energy. The experiment also concerns one model, set of tasks, participant population, and interface. It cannot support broad ecological or industry-wide claims without further evidence and replication.

## 8. Conclusion (TO BE WRITTEN AFTER THE STUDY)

No empirical conclusion can currently be given. The completed paper should state what was actually observed, how certain the estimates were, where the manipulation worked or failed, and which environmental consequences remain unmeasured.

## References (working bibliography; verify full ACM metadata before submission)

[1] Michael Klesel and Uwe Messer. 2026. *Good for the Planet, Bad for Me? Intended and Unintended Consequences of AI Energy Consumption Disclosure.* Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems. DOI: https://doi.org/10.1145/3772318.3791015 . Open text: https://arxiv.org/html/2603.23075v1

[2] Yuheng Ren, Luiz Augusto Morais, Filipe Calegario, Frédérique Krupa, Francisco Paulo Magalhães Simões, Nivan Ferreira, and Georgia Panagiotidou. 2026. *EcoChat Probe: How Energy Feedback Shapes End Users’ Interpretations of Everyday Generative AI Use.* Proceedings of FAccT 2026, 5194–5218. DOI: https://doi.org/10.1145/3805689.3812368

[3] Deepak Panigrahy and Aakash Tyagi. 2026. *Energy per Successful Goal: Goal-Level Energy Accounting for Agentic AI Systems.* arXiv preprint. https://arxiv.org/abs/2605.22883

[4] Cooper Elsworth et al. 2025. *Measuring the environmental impact of delivering AI at Google Scale.* arXiv preprint. https://arxiv.org/abs/2508.15734

[5] OpenAI. *Reasoning models: API documentation.* https://developers.openai.com/api/docs/guides/reasoning (accessed 2026-10-28).

[6] University of California, Santa Barbara Office of Research. *ORahs 2.0 Definitions: Active Deception, Incomplete Disclosure, Associate roles.* https://www.research.ucsb.edu/human-subjects/orahs-definitions (accessed 2026-10-28).

[7] ACM CHI 2027. *Guide to a Successful Submission* and *Papers*. https://chi2027.acm.org/guide-to-a-successful-submission/ and https://chi2027.acm.org/authors/papers/ (accessed 2026-10-28).

## Revision checkpoints before a serious CHI manuscript

- [ ] Confirm model and API settings genuinely distinct, and usage-count semantics.
- [ ] Expand HCI theory beyond the immediately adjacent 2026 papers, checking placebo, eco-label framing, greenwashing perceptions, effort/performance expectations, and ethical deception.
- [ ] Decide whether the interaction is the single primary endpoint or whether choice/setting belief is co-primary; plan multiplicity control.
- [ ] Develop trustworthy objective task bank, independently validate scoring and task suitability.
- [ ] Estimate detectable interaction effects and sample using independent pilot data; four arms require substantially more people than a two-arm main effect.
- [ ] Obtain the requisite faculty sponsorship and UCSB human-subjects review/decision, consent/debrief scripts and privacy plan.
- [ ] Run technical API pilot within explicit credit/cost cap and then approved usability pilot.
- [ ] Preregister hypotheses, endpoints, missingness/switching policy, sample/stopping and analysis.
- [ ] Collect and analyze actual data; write Results, figure captions, Discussion and Conclusion based on evidence.
- [ ] For anonymous CHI review, unlink or anonymize public identifiable project repository and supplement links in accordance with venue policy.
