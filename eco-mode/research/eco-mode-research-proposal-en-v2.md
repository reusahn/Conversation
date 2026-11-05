# Eco Mode Menu Design and Informed Choice in LLM Services

Research Proposal

Jonghoon Ahn | November 5, 2026 | English revision 2

## Research overview

I propose a study of how a large language model (LLM) service presents an Eco mode alongside fixed processing effort levels. The central question is whether users understand what Eco does and what they are agreeing to give up when they choose it. The study will compare the same six options in one flat list and in a menu that separates an adaptive conservation policy from fixed effort settings.

The first experiment will use a disclosed prototype and prepared responses. Its primary outcome will combine first-task Eco selection with demonstrated understanding of the proposed functionality. Additional outcomes will distinguish sufficient concise answers, acceptance despite a perceived shortcoming, personal editing, and requests for further work. The intended contribution is evidence for presenting environmental goals and processing controls so that users can make choices they understand.

## 1 Background and contribution

Environmental feedback and LLM choice already have a research history. GPTFootprint combined an Eco Score, environmental imagery, and estimated resource feedback in a ChatGPT extension, with nine users over one week [1]. EcoChat deployed a ChatGPT extension with 52 participants over four weeks; its published abstract reports increased awareness and reflection alongside no significant change in usage patterns [2].

Klesel and Messer studied energy disclosure and model choice with 365 participants [3]. Both displayed model options used GPT-4o mini, and the paper also examined subsequent quality judgments. Kim and colleagues examined latency and estimated carbon feedback with 89 university students [4]. Rabinovitch and colleagues report two preregistered text-editing experiments with 1,200 participants on environmental-cost information and ChatGPT use [6]. These studies make environmental awareness, mode choice, and usage reduction established research targets.

This proposal examines the semantic organization of the controls. Eco represents a proposed adaptive policy with a conservation goal; Light through Max represent fixed effort levels. Putting these different kinds of control in one list may encourage users to read them as a single ranking of capability. Context-dependent preference theory motivates attention to the surrounding choice set [5], while the proposed experiment holds its size constant. It will test whether explicit functional grouping changes understanding, choices, and perceived tradeoffs. The contribution is specific to this comparison; the proposal makes no claim to the first Eco interface.

## 2 Research questions

RQ1  How does flat versus function-grouped presentation affect first-task Eco selection accompanied by correct functional understanding?

RQ2  What response compromises do users accept, and how do sufficient brevity, acknowledged inadequacy, and personal editing differ across presentations?

RQ3  How do users continue, change modes, or finish in the prototype, and what reasons do they report for those actions?

## 3 Experimental comparison

Table 1  Main menu conditions

| Condition | Presentation |
| --- | --- |
| Flat | One list: Eco / Light / Medium / High / Extra High / Max |
| Grouped | Adaptive conservation policy: Eco
Fixed processing effort: Light / Medium / High / Extra High / Max |

Participants will be randomly assigned 1:1 to one presentation. Both conditions contain the same six selectable options, proposed functions, and item descriptions in the same order. Typography, width, selection controls, and initial state will be matched. The grouped condition adds nonselectable headings and visual separation. These changes form the presentation intervention; the study will not isolate the effects of a single word, heading, or spacing difference.

### Proposed function mapping

Eco is a proposed policy that would adjust processing effort to the task with a resource-conservation goal. Light is a fixed low effort setting selected directly by the user; Medium through Max are progressively higher fixed profiles. Eco could use more effort for a demanding task and is not necessarily the lowest setting. This first study will not implement an adaptive engine or measure resource savings.

A separate comprehension pilot will validate the distinction and fix the final descriptions and behavior mapping. No mode will be selected by default, and participants may defer. The menus are research concepts rather than specifications of a commercial product. The Eco / High / Max compact menu remains a follow-up comparison of a different choice set; it is not a third arm in this experiment.

## 4 Study design and procedure

### Participants and formative work

The initial study will recruit adult LLM users who can complete Korean-language tasks. English examples here are illustrative translations; an English-language replication would require linguistic validation. Approximately 6–10 formative participants will review both layouts in varied order, first describing the names without explanations and then explaining the functions after reading the shared descriptions.

The pilot will check whether Eco and Light are distinguishable, whether the grouped display remains usable, and whether the wording supports prediction on a new task. Response pairs will be evaluated without mode labels for factual accuracy, task coverage, and usefulness. Revisions will address ambiguity and burden, without selecting materials for a preferred treatment effect. Final materials, scoring rules, and logging will be fixed before the main study.

### Main experiment

Writing, information organization, and ideation tasks will be used, with all six task orders balanced within each condition. The first task supplies the primary outcome before repeated exposure. Longer environmental-attitude questions will follow behavioral choices.

Table 2  Main study sequence

| Stage | Procedure |
| --- | --- |
| Initial choice | Read the task and assigned menu; choose a mode or explicitly defer. |
| Functional check | On the first task only, answer three comprehension items without corrective feedback. |
| Common comparison | Review X and initial sufficiency; then review Y and make final comparative judgments. |
| Recorded action | Choose a response, edit, open further response Z, request another mode, or decline to use the examples. |
| Follow-up | Report reasons, acceptable compromises, environmental expectations, and choice burden. |

Before response evaluation, the interface will state that the chosen mode has not run. All participants will receive the same X and Y examples for a given task, independently of mode choice. Their first action after this common comparison will be recorded before any optional branch. Opening Z will reveal one further authored response; editing will open an editable copy; requesting another mode will reopen the assigned menu and record the target. No branch will generate a live model response.

The functional questions may prompt reflection, so later actions estimate effects within this shared study sequence. Prototype actions will not be described as natural service use or actual completion of a participant’s outside task.

## 5 Measures and analysis

### Primary outcome

The primary outcome is the joint event of selecting Eco on the first task and answering all three functional-comprehension items correctly immediately afterward. The items test adaptive versus fixed effort, the possibility that Eco uses higher effort on a demanding task, and the distinction between Eco and fixed low Light. Appendix A specifies the items and proposed scoring. They measure demonstrated understanding after choice, rather than proving what a participant knew before choosing.

The main estimate will be the difference in joint-event proportions, grouped minus flat, with a two-sided 95% confidence interval. Raw Eco selection, the complete choice distribution, and the three-item comprehension score will also be reported so that an increase in the joint outcome can be interpreted. Comprehension is an outcome: people who misunderstand or do not choose Eco will remain in their assigned groups.

### Response compromises and subsequent actions

Initial and post-comparison sufficiency judgments will be recorded separately. After seeing X and Y, participants will report comparative usefulness and whether X is sufficient. The post-comparison judgment will define the perceived-sacrifice indicator. Choosing X unchanged will be separated from using Y, editing either answer, seeking further information, changing modes, or using neither. A limited exploratory indicator of perceived sacrifice requires an explicit judgment that Y is more useful, X is insufficient, and a choice to use X unchanged. A sufficient concise answer will remain a separate case; length and idea count will not establish objective quality loss.

The first action after common X/Y exposure will support comparisons under the same information. Later branches, including opening Z and any subsequent choice, will be exploratory. Editing will retain the source response and revised text separately from unchanged use. Stopping without adopting a response, deferring, and finishing with a selected response will be distinct events. Reasons may overlap and will be elicited after actions; stopping alone will not establish conservation, adequacy, or abandonment.

### Interpretation and missing data

The assigned sample defines the analysis population. Incorrect and explicit do-not-know comprehension responses are observed responses; missing records, withdrawal, and unjudgeable cases will be reported separately. Undetermined joint outcomes will not be silently coded as failures. Missing-data procedures and sensitivity analyses will be preregistered, with randomized and observed denominators shown.

Repeated secondary judgments will account for participant and task differences. Secondary contrasts, multiplicity handling, and model fallbacks will be set before collection. Post-choice comprehension, motives, and environmental ratings will not establish causal mediation. Environmental expectations will use a seven-point scale with a separate cannot-judge option after the tasks; they describe post-experience reports.

## 6 Feasibility and research ethics

Preparation requires two menu layouts, shared descriptions, a behavior mapping, three X/Y response pairs, one optional Z response per task, an editable-response view, and a logging instrument. The prototype will record display condition, task order, first mode choice, comprehension responses, common-stage action, optional branches, and reported reasons. The optional Z texts and branch instructions must be authored and piloted before collection.

The main sample will be determined for the joint primary outcome using a justified baseline rate, minimum difference of interest or precision target, and missingness allowance. Allocation is 1:1. The pilot will establish session burden; 20–30 minutes is a planning target. Recruitment limits, stopping rules, compensation, fees, and the analysis plan will be fixed before collection. If the required sample is infeasible, the work will be reported as an exploratory pilot.

Before a human pilot or recruitment, I will complete applicable institutional review, consent, and data-management procedures. Participants will be told that functions are proposed concepts, answers are authored examples, and environmental savings have not been measured. They may defer or withdraw. Identifiers will be separated from study records, with retention, compensation, and sharing arrangements specified. No live LLM backend, dedicated GPU, or energy sensor is required for this first study.

## 7 Expected contribution and scope

The study will test a design principle for LLM controls: whether distinguishing a conservation policy from fixed effort levels helps users understand what they select. Joint reporting of choice and comprehension will show whether apparently similar Eco-selection rates conceal different interpretations. Response judgments and recorded follow-up choices will describe the compromises users accept and the work they prefer to continue themselves or request from the interface.

The IEA report provides the wider energy-system motivation [7]. Physical resource savings, sustained use, retries in live services, and ecological effects require subsequent evaluation. Quality preservation and demonstrated environmental savings are not success conditions for this first experiment. A null menu effect, persistent misunderstanding, or reluctance to accept a perceived compromise would also answer the research questions.

## References

[1] Graves, N., Larrieu, V., Zhang, Y. T., Peng, J., Nagaraj Rao, V., Liu, Y., & Monroy-Hernández, A. (2025). GPTFootprint: Increasing Consumer Awareness of the Environmental Impacts of LLMs. In CHI EA 2025 — Extended Abstracts of the 2025 CHI Conference on Human Factors in Computing Systems, Article 296. ACM. https://doi.org/10.1145/3706599.3719708

[2] Ren, Y., Morais, L. A., Calegario, F., Krupa, F., Simões, F. P. M., Ferreira, N., & Panagiotidou, G. (2026). EcoChat Probe: How Energy Feedback Shapes End Users’ Interpretations of Everyday Generative AI Use. In Proceedings of the 9th ACM Conference on Fairness, Accountability, and Transparency (FAccT 2026), 5194–5218. ACM. https://doi.org/10.1145/3805689.3812368

[3] Klesel, M., & Messer, U. (2026). Good for the Planet, Bad for Me? Intended and Unintended Consequences of AI Energy Consumption Disclosure. In Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems, 1–14. ACM. https://doi.org/10.1145/3772318.3791015

[4] Kim, H., Chen, X., Cabral, A., Lin, C. K., Gupta, U., & Hester, J. (2026). When LLMs Slow Down: How Environmental Impacts Mediate University Students’ LLM Usage. In 2026 12th International Conference on ICT for Sustainability, 322–334. IEEE. https://doi.org/10.23919/ICT4SCPS00102.2026.00038

[5] Tversky, A., & Simonson, I. (1993). Context-Dependent Preferences. Management Science, 39(10), 1179–1189. https://doi.org/10.1287/mnsc.39.10.1179

[6] Rabinovitch, H., Kashi, I., & Shalvi, S. (2027). Informing users about LLMs’ environmental costs encourages ethical consumption. Computers in Human Behavior, 187, Article 109214. https://doi.org/10.1016/j.chb.2026.109214

[7] International Energy Agency. (2026). Key Questions on Energy and AI. IEA. Institutional report. https://www.iea.org/reports/key-questions-on-energy-and-ai

GPTFootprint is a CHI extended abstract; references 2–4 are conference papers. References 5 and 6 are journal articles, and reference 7 is an institutional report. The publisher assigns reference 6 to its February 2027 issue; the online article was available when this proposal was prepared.

## Appendix A Function descriptions and measurement

The descriptions and items below will be validated in Korean during the formative pilot. The same option descriptions will appear in both menu conditions.

Table 3  Shared proposed function descriptions

| Option | Description |
| --- | --- |
| Eco | A proposed policy that adjusts processing effort to the task with a resource-conservation goal. |
| Light | A fixed low processing effort setting selected by the user. |
| Medium | A fixed medium processing effort setting. |
| High | A fixed high processing effort setting. |
| Extra High | A fixed effort setting above High. |
| Max | The highest fixed processing effort setting in this research menu. |

### Primary comprehension items

- Eco uses the same fixed effort on every task / can adjust effort to the task / do not know. Correct: can adjust.

- For a demanding task, Eco could use more effort than Light / must always use less / do not know. Correct: could use more.

- Light is a fixed low setting / adjusts effort automatically like Eco / do not know. Correct: fixed low.

One point is assigned per correct response, for a score of 0–3. Incorrect and do-not-know answers remain distinguishable in the data. All three correct answers satisfy the functional criterion for the joint outcome; the rubric will be fixed before the main study. Missing items remain recorded as missing. Environmental-benefit beliefs are assessed separately.

### Prototype disclosure

> This screen is a research prototype. Its functions are proposed concepts, and its answers are prepared examples. It is not connected to a live model or adaptive engine. Computation, electricity use, and environmental savings have not been measured. Choose the mode you would use for the task.

> We will now evaluate common response examples, independently of your mode choice. They are not output from your selected mode. After comparing them, your action may open another prepared example, an editor, or the mode menu.

### Action recording and follow-up

The action view will distinguish using X unchanged, using Y unchanged, editing an answer, opening Z, requesting another mode, using neither, and explicit deferral. It will record the first action after X/Y exposure and later branch events separately. Afterward, participants will explain their decision, identify any perceived shortcoming, and report which forms of compromise they would accept. These reports will not be treated as proof of an environmental motive.

## Appendix B Illustrative common response pairs

Responses X and Y will be shown to all participants for each task. These authored examples will be piloted without mode labels. A further response Z for optional continuation will be finalized before collection. The more elaborated example is not necessarily more useful.

### Writing a workshop invitation

**Prompt**  Write an invitation for students who will be meeting one another for the first time. The drawing workshop is on Saturday from 2 to 4 p.m. in Studio B and is free. The online registration form is due Friday at 6 p.m. Make it welcoming to people with no drawing experience.

**Response X**  Join our free drawing workshop on Saturday from 2 to 4 p.m. in Studio B. No drawing experience is required. Please submit the online registration form by Friday at 6 p.m.

**Response Y**  You are invited to a drawing workshop, even if you have never drawn before. Everyone is welcome, regardless of experience.

The workshop takes place on Saturday from 2 to 4 p.m. in Studio B. Participation is free. To join, submit the online registration form by Friday at 6 p.m.
Come meet other students and try drawing without pressure to be an expert.

### Organizing information about a shared space

**Prompt**  Organize these notes clearly for a first-time visitor. The space has 48 seats and is free. It is open from 9 a.m. to 6 p.m. and closed on Sundays. An online reservation is required. Each visit can last up to two hours, and bookings open two days before the visit.

**Response X**  This free, 48-seat space is open from 9 a.m. to 6 p.m. and closed on Sundays. Online reservations are required and open two days before your visit. Each visit can last up to two hours.

**Response Y**  Access and opening hours: The space has 48 seats and is free to use. Opening hours are 9 a.m. to 6 p.m.; it is closed on Sundays.
Reservations: An online reservation is required. Bookings open two days before your visit, and each visit can last up to two hours.

### Proposing a participatory installation

**Prompt**  Suggest a small installation that visitors can participate in, using 50 sheets of black paper and tape. The indoor space is 3 m by 3 m, the budget is at most KRW 100,000, and no electrical equipment will be used.

**Response X**  Create a collective landscape on a wall. Visitors tear pieces of black paper and tape them beside earlier visitors’ pieces, gradually extending a shared scene. Provide the paper and tape and invite each person to continue what is already there.

**Response Y**  Collective landscape: Visitors add torn paper beside existing pieces to reshape a shared wall scene.
Folded surface: Visitors add folded paper pieces that create a varied surface of light and shadow using the room’s existing ambient light.
Map of empty spaces: Visitors arrange paper with gaps between the pieces, marking a place they would like to occupy.
All three ideas use paper and tape without electrical equipment, within the stated space and material constraints.

The pairs vary tone and organization, information structure, and the range of ideas. Pilot checks will separate task coverage from perceived sufficiency. Greater length or variety will not establish better quality. No pair will deliberately introduce factual errors or dangerous advice to demonstrate a tradeoff.
