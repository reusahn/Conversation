# Eco Mode Menu Design and User Choice in LLM Services

Research Proposal

Jonghoon Ahn | November 5, 2026

## Research overview

I propose a study of how an Eco mode should be presented within a large language model (LLM) service. The study begins with a practical question: if users are willing to accept some reduction in performance or convenience for an expected environmental benefit, how does the menu help them understand and make that choice? It compares an Eco option alongside five effort levels with a compact Eco / High / Max menu. A five-level menu without Eco provides a reference condition.

The first study will use an explicitly disclosed prototype and prepared response examples. It examines mode selection, understanding of the proposed functionality, environmental interpretations, and acceptance of responses that differ in detail or range of ideas. Its contribution will be evidence for configuring and explaining Eco options. Preserving response quality and demonstrating physical environmental savings are not prerequisites for an informative result.

## 1 Background and rationale

Prior work has studied environmental feedback during everyday LLM use. GPTFootprint combined an Eco Score, environmental imagery, and estimated resource feedback in a ChatGPT extension; its exploratory study involved nine users over one week [1]. EcoChat deployed a ChatGPT extension with 52 participants over four weeks. Its published abstract reports increased awareness and reflection, alongside no significant change in usage patterns [2]. These findings motivate examining how environmental meanings enter users’ decisions while keeping awareness and behavior as separate outcomes.

Klesel and Messer studied energy consumption disclosure in an experiment with 365 participants [3]. Their interface presented model choices with performance and energy information, although both choices used GPT-4o mini. The study reported differences in model selection and perceived quality. Quality differences between people who selected different options should be interpreted with their self-selection in mind. Kim and colleagues examined latency and estimated carbon feedback with 89 university students [4]. Together, these studies establish nearby questions about environmental information and performance tradeoffs.

The present proposal focuses on the configuration of the menu that contains Eco. Context-dependent preference theory suggests that an option’s appeal can depend on the alternatives surrounding it [5]. In an LLM menu, Eco next to Light may raise questions about whether the two functions differ. Eco next to only High and Max may imply a different relationship between conservation and processing effort. The proposed comparison will examine these configurations directly. It does not presume that environmentally framed choices are a new topic or that Eco will be equally attractive in both menus.

## 2 Research questions

The central question is how Eco-inclusive menu configurations influence users’ understanding, environmental interpretations, mode choices, and acceptance of perceived performance tradeoffs.

RQ1  How do users understand Eco and its relationship to the effort levels in each menu?

RQ2  How do first-task choices differ between coexistence and compact menus, and how do their complete distributions compare with the reference?

RQ3  After viewing the assigned menu, how do users distinguish a sufficient concise answer from an inadequate answer they would still use?

## 3 Menu conditions and proposed functionality

Table 1  Research menu conditions

| Condition | Available options |
| --- | --- |
| A  Effort-level reference | Light / Medium / High / Extra High / Max |
| B  Coexistence | Eco / Light / Medium / High / Extra High / Max |
| C  Compact | Eco / High / Max |

The primary comparison is B versus C, with planned 1:1:1 random assignment across A, B, and C. Option order and wording will be fixed before the main study; shared options will have identical descriptions. There will be no default selection, and participants may defer. These are research menus, rather than descriptions of a commercial service’s current features.

### Distinguishing Eco from Light

The starting concept defines Eco as an adaptive processing policy with a resource-conservation goal: it would adjust effort to the task. Light represents a fixed low effort setting chosen directly by the user. Eco therefore need not use the lowest effort on every task. Medium through Max represent progressively higher fixed effort profiles.

This first study tests comprehension of a proposed function. It does not implement an adaptive engine or measure resource savings. A separate pilot will examine whether users distinguish the policy from fixed effort levels. Definitions may be revised for clarity before the main study, without selecting for a preferred Eco-selection rate.

### What the comparisons estimate

B versus C estimates the combined effect of the available options, their functional relationships, and their presentation. A versus B describes the effect of adding the proposed Eco policy to an effort-level menu. Neither comparison isolates the word Eco. A future Light / High / Max condition or an Eco workflow toggle could address other design questions; neither is an additional arm in this first study. Replacing adaptive Eco with fixed Light would also change functionality and would not provide a pure naming control.

## 4 Study design and procedure

### Participants and formative work

The initial study will recruit adult LLM users who can complete Korean-language tasks. English examples in this proposal are illustrative translations. An English-language replication would require separate linguistic validation. A formative pilot with approximately 6–10 people will examine function comprehension and session burden, separately from the main experiment.

In the pilot, participants will see menu variants in varied order and describe what the names suggest before receiving function explanations. Questions will distinguish interpretations such as lowest effort, adaptive processing, or environmental certification. Participants will then receive the descriptions and explain the Eco–Light distinction in their own words. Response pairs will also be evaluated without mode labels for factual accuracy, task coverage, and usefulness. Materials will be revised and fixed before the main study.

### Main experiment

The experiment will use writing, information organization, and ideation tasks. All six task orders will be balanced within each menu condition. The first task provides the primary choice outcome, before experience with repeated tasks. Longer questions about environmental attitudes will follow the initial choice to limit prompting participants toward an environmental interpretation.

Table 2  Procedure within each task

| Stage | Participant activity |
| --- | --- |
| Mode selection | Read the task and assigned menu; select a mode or explicitly defer. |
| Common response | Review a prepared concise answer and give an initial judgment about using it. |
| Alternative response | View a more elaborated example and choose a final action. |
| Follow-up questions | Report usefulness, sufficiency, function understanding, environmental expectations, and reasons. |

The transition to response evaluation will state that the selected mode has not been run. Every participant will see the same prepared examples for a given task, regardless of the initial mode choice. The common evaluation therefore concerns judgments after exposure to a menu, rather than actual output from the selected mode. Comparing all assigned participants also avoids restricting the analysis to people who chose Eco.

Final actions will distinguish using the current answer unchanged, editing it personally before use, asking the AI to expand it, changing modes, and declining to use it. These are recorded decisions about the presented scenario. They do not establish subsequent behavior in a deployed service.

## 5 Outcomes and analysis

### Primary comparison

The primary outcome is Eco selection on the first task in B and C. I will report the difference in proportions, defined as compact minus coexistence, with a 95% confidence interval. The assigned sample defines the analysis population. Explicit deferral is a recorded response; missing responses, withdrawal, and recording failures will be identified separately, with missing-data and sensitivity procedures specified before collection.

Condition A has no Eco option, so its absence will not be coded as zero Eco preference to estimate a naming effect. A will provide the complete reference distribution of choices. Eco and Light selections will not be combined as measured low-compute adoption, because adaptive Eco is not a fixed low effort setting. Between-group distributions will not be used to claim that particular individuals switched from Light to Eco.

### Response acceptance and interpretation

Secondary outcomes include complete choice distributions, deferral, Eco comprehension in B and C, and responses to the common examples. The main acceptance measure is choosing to use the current answer unchanged. Personal editing will be reported separately because it transfers work to the user.

A limited exploratory indicator of perceived performance sacrifice will require three explicit responses: the alternative is more useful, the current answer is insufficient, and the participant nevertheless chooses to use the current answer unchanged. Choosing a concise answer because it is already sufficient will be treated separately. Neither answer length nor the number of ideas will establish objective quality loss. Uncertain judgments and missing answers will remain visible in the reporting.

Repeated acceptance judgments will account for participant and task differences. The analysis plan will specify secondary comparisons, multiplicity handling, model choices and convergence fallbacks before collection. Causal comparisons will retain assigned groups rather than exclude participants based on later comprehension, reported inadequacy, or Eco selection.

Environmental expectations will be measured after the tasks using a seven-point scale with a separate cannot-judge option. These ratings and reported reasons describe post-experience interpretations. They will not be presented as uncontaminated initial beliefs or evidence of causal mediation. Open responses will be coded for function interpretation, sufficiency, perceived shortcomings, and reasons for requesting further work.

## 6 Feasibility and research ethics

Preparation consists of three menu screens, function descriptions, a proposed behavior mapping, task materials, and a recording instrument. Sessions are provisionally planned for 20–30 minutes, subject to the pilot. The main sample size will be determined for the B–C comparison using a justified baseline rate, minimum difference of interest or precision target, and allowance for missing data. Recruitment limits, stopping rules, compensation, and costs will be fixed before collection. If adequate recruitment is infeasible, the work will be reported as an exploratory pilot.

Before any human pilot or recruitment, I will complete the applicable institutional review, consent, and data-management procedures. Participants will be told that the interface is a prototype, responses are prepared examples, and environmental savings have not been measured. Identifiers will be separated from study records, and the protocol will specify compensation, retention, withdrawal, and the scope of any data sharing. The first study does not require a live LLM backend, dedicated GPU, or energy sensor.

## 7 Expected contribution and scope

The study will provide evidence about whether users understand an adaptive conservation policy alongside fixed effort levels and how coexistence or simplification changes their choices. It will also distinguish acceptance of adequate brevity from accepting a response despite a perceived shortcoming. These findings can guide where Eco belongs in an LLM interface and how its intended function should be explained.

Actual adaptive processing, sustained adoption, and electricity, carbon, or water outcomes require subsequent studies that include retries and mode changes. The IEA report provides energy-system context for this wider motivation [6]. The proposed experiment cannot establish ecological protection or a slower pace of AI development. Informative outcomes include no detectable menu difference, confusion about Eco, or lower willingness to accept tradeoffs.

## References

[1] Graves, N., Larrieu, V., Zhang, Y. T., Peng, J., Nagaraj Rao, V., Liu, Y., & Monroy-Hernández, A. (2025). GPTFootprint: Increasing Consumer Awareness of the Environmental Impacts of LLMs. In CHI EA 2025 — Extended Abstracts of the 2025 CHI Conference on Human Factors in Computing Systems, Article 296. ACM. https://doi.org/10.1145/3706599.3719708

[2] Ren, Y., Morais, L. A., Calegario, F., Krupa, F., Simões, F. P. M., Ferreira, N., & Panagiotidou, G. (2026). EcoChat Probe: How Energy Feedback Shapes End Users’ Interpretations of Everyday Generative AI Use. In Proceedings of the 9th ACM Conference on Fairness, Accountability, and Transparency (FAccT 2026), 5194–5218. ACM. https://doi.org/10.1145/3805689.3812368

[3] Klesel, M., & Messer, U. (2026). Good for the Planet, Bad for Me? Intended and Unintended Consequences of AI Energy Consumption Disclosure. In Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems, 1–14. ACM. https://doi.org/10.1145/3772318.3791015

[4] Kim, H., Chen, X., Cabral, A., Lin, C. K., Gupta, U., & Hester, J. (2026). When LLMs Slow Down: How Environmental Impacts Mediate University Students’ LLM Usage. In 2026 12th International Conference on ICT for Sustainability, 322–334. IEEE. https://doi.org/10.23919/ICT4SCPS00102.2026.00038

[5] Tversky, A., & Simonson, I. (1993). Context-Dependent Preferences. Management Science, 39(10), 1179–1189. https://doi.org/10.1287/mnsc.39.10.1179

[6] International Energy Agency. (2026). Key Questions on Energy and AI. IEA. Institutional report. https://www.iea.org/reports/key-questions-on-energy-and-ai

GPTFootprint is a CHI extended abstract. References 2–4 are conference papers; reference 5 supplies general choice-context theory. The IEA report supplies energy background. Each source is used within that scope.

## Appendix A Proposed descriptions and participant guidance

The wording below illustrates the concept to be refined in the comprehension pilot. The final Korean materials and behavior mapping will be fixed before the main study.

Table 3  Proposed function descriptions

| Option | Description |
| --- | --- |
| Eco | A proposed policy that adjusts processing effort to the task with a resource-conservation goal. |
| Light | A fixed low processing effort setting selected by the user. |
| Medium | A fixed medium processing effort setting. |
| High | A fixed high processing effort setting. |
| Extra High | A fixed effort setting above High. |
| Max | The highest fixed processing effort setting in this research menu. |

Descriptions of shared options will be identical across menus. Eco may select more effort when the task requires it; it does not guarantee the lowest setting or a verified environmental saving.

### Opening disclosure

> This study concerns mode menus and answer evaluation in an LLM service. The screen is a research prototype, and the functions shown are proposed concepts. It is not connected to a live service or an adaptive processing engine. Answers are prepared examples. Differences in computation, electricity use, or environmental impact have not been measured. Please choose a mode you would use for the task.

### Transition to common response evaluation

> We will now evaluate the same answer example shown to everyone, independently of your first choice. It is not output from the mode you selected. First consider whether you would use this answer; then review an alternative and make a final choice.

### Questions after the decision

- In menus B and C, is Eco always the lowest effort level, an adaptive policy, or something else? Participants may withhold judgment. In B, how does it differ from Light?

- Which answer is more useful for this task: the current answer, the alternative, approximately equal, or cannot judge?

- Is anything insufficient in the current answer for completing the task: yes, no, or cannot judge? What explains your chosen action?

- What environmental benefit, if any, do you expect from Eco? How easy was the menu to choose from, and what did its names suggest?

The closing explanation will reiterate that Eco is not an environmental certification and that this study does not measure resource savings.

## Appendix B Illustrative tasks and response pairs

These authored examples are shared across menu conditions. The alternative is more elaborated, but participants will not be told that it is necessarily better. Unlabeled pilot evaluation will check factual accuracy, task coverage, and usefulness before the main study.

### Writing a workshop invitation

**Prompt**  Write an invitation for students who will be meeting one another for the first time. The drawing workshop is on Saturday from 2 to 4 p.m. in Studio B and is free. The online registration form is due Friday at 6 p.m. Make it welcoming to people with no drawing experience.

**Concise example**  Join our free drawing workshop on Saturday from 2 to 4 p.m. in Studio B. No drawing experience is required. Please submit the online registration form by Friday at 6 p.m.

**Elaborated alternative**  You are invited to a drawing workshop, even if you have never drawn before. Everyone is welcome, regardless of experience.

The workshop takes place on Saturday from 2 to 4 p.m. in Studio B. Participation is free. To join, submit the online registration form by Friday at 6 p.m.
Come meet other students and try drawing without pressure to be an expert.

### Organizing information about a shared space

**Prompt**  Organize these notes clearly for a first-time visitor. The space has 48 seats and is free. It is open from 9 a.m. to 6 p.m. and closed on Sundays. An online reservation is required. Each visit can last up to two hours, and bookings open two days before the visit.

**Concise example**  This free, 48-seat space is open from 9 a.m. to 6 p.m. and closed on Sundays. Online reservations are required and open two days before your visit. Each visit can last up to two hours.

**Elaborated alternative**  Access and opening hours: The space has 48 seats and is free to use. Opening hours are 9 a.m. to 6 p.m.; it is closed on Sundays.
Reservations: An online reservation is required. Bookings open two days before your visit, and each visit can last up to two hours.

### Proposing a participatory installation

**Prompt**  Suggest a small installation that visitors can participate in, using 50 sheets of black paper and tape. The indoor space is 3 m by 3 m, the budget is at most KRW 100,000, and no electrical equipment will be used.

**Concise example**  Create a collective landscape on a wall. Visitors tear pieces of black paper and tape them beside earlier visitors’ pieces, gradually extending a shared scene. Provide the paper and tape and invite each person to continue what is already there.

**Elaborated alternative**  Collective landscape: Visitors add torn paper beside existing pieces to reshape a shared wall scene.
Folded surface: Visitors add folded paper pieces that create a varied surface of light and shadow using the room’s existing ambient light.
Map of empty spaces: Visitors arrange paper with gaps between the pieces, marking a place they would like to occupy.
All three ideas use paper and tape without electrical equipment, within the stated space and material constraints.

The pairs vary tone and organization, information structure, and the range of ideas. Pilot checks will separate task coverage from perceived sufficiency. Greater length or variety will not establish better quality. No pair will deliberately introduce factual errors or dangerous advice to demonstrate a tradeoff.
