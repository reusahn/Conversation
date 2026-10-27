# ContextLens Collaboration Plan

Two person build plan for the Meta Global AI Developer Hackathon

27 October 2026 | Target submission 4 November 2026

We will build a working prototype that helps someone share a viral clip with the source evidence needed to understand its accompanying claim. The first version will search a clearly disclosed collection of footage we are allowed to use. The deliverable is a playable, shareable evidence page, supported by reproducible code and an honest three minute demonstration.

## The product

A viewer uploads an allowed clip and supplies its caption. They choose a question such as **When was this footage already available**, **What production is this from**, or **What happens around this moment**. The system finds the matching source interval, selects relevant evidence and produces a page the viewer can send to a friend. The recipient can replay that evidence without an account.

The shared page preserves the exact caption and question. Changing a caption creates a new analysis; an explanation about one claim cannot become a general verification badge for the footage. Unavailable evidence stays unresolved.

## The demonstration

The following scenarios are proposed demonstration fixtures, not findings about actual posts.

| Input | Expected behavior |
| --- | --- |
| A permitted film clip with an accurate film caption | Find its source interval and show the credited production evidence without an accusation. |
| The same clip described as first filmed today | Keep the same source match; show earlier publication evidence when it exists. Do not infer the event or filming date. |
| A clip outside the reference collection | Say no match was found in this collection. Do not invent a source or an AI verdict. |

## First release scope

Build file upload, source interval matching, question buttons, evidence playback, typed date and production records, unknown states and a shareable result link. Optional comment samples may prioritize questions after the core flow works. Instagram integration, internet wide source search, home feed filtering, AI probability scores and copyright judgments are outside the first release.

<!-- PAGE BREAK -->

## Proposed responsibilities

This split uses Jonghoon's filmmaking and interface experience and the collaborator's stated interest in problem framing. It is a proposal for the two collaborators to agree, not a claim that the collaborator has already accepted these tasks. Coding ownership can be reassigned at kickoff without changing completion criteria.

| Work package | Lead | Review and completion |
| --- | --- | --- |
| Viewer task and social problem | Collaborator | Jonghoon reviews the scenario and wording. Both can explain one user and one sharing task. |
| Allowed footage and source records | Jonghoon | Collaborator checks permission notes, source intervals, dates and production records. |
| Upload and visual matching | Jonghoon | Collaborator supplies held out queries and unknown controls after thresholds are frozen. |
| Spark evidence workflow | Jonghoon | Collaborator defines claim and evidence labels, reviews outputs and logs failures. |
| Mobile evidence and sharing page | Jonghoon | Collaborator tests the recipient flow on a separate phone without coaching. |
| Baselines and evaluation report | Collaborator | Jonghoon reproduces the runs. Two reviewers label support independently where feasible. |
| Demo and submission | Jonghoon | Collaborator checks actual operation, exact claims, results and public link access. |

## Component handoffs

The corpus manifest gives each allowed source a stable ID, media hash, permission note and typed records. The matcher returns a source ID with start and end offsets, or an unknown result. Spark receives retrieved records and source chunks, selects evidence for the chosen question and returns evidence IDs with unresolved fields. The page resolves those IDs into actual playback and records.

Software can check IDs, types and time bounds. It cannot prove that every model sentence follows from its citation. Treat the model's relevance explanation as a proposal; audit its support independently. Earlier publication shows that footage existed by a date. It does not establish when an event occurred. A documented production record is separate from a visual guess about AI creation.

## How we will collaborate

Use one shared task list with one owner and one reviewer per task. Hold a short daily check in: show the working increment, name the blocker, and agree on the next test. Exchange sample JSON records and a playable example before integrating components. Put runnable code in a dedicated project repository; use **Conversation/contextlens** for planning and public dialogue records. Never commit credentials or footage that cannot be redistributed.

<!-- PAGE BREAK -->

## Delivery schedule

All dates below are in California time. These are proposed milestones.

| Dates | Working deliverable | Completion check |
| --- | --- | --- |
| 27 to 28 October | Allowed source collection and upload to matching to playback spike | A new query finds its actual source interval; an unknown clip remains unknown; one real Meta API call works. |
| 29 to 30 October | Question selection and caption specific evidence page | Every displayed record opens; another phone can replay and share the result without an account. |
| 31 October to 1 November | Frozen test suite and baseline runs | Save configurations, manifests, outputs, timings, usage and all failures. |
| 2 November | Recipient checks and wording revisions | Record task completion, assistance and unknown state understanding. Add comments only if the core is stable. |
| 3 November | Reproducibility and timed demo rehearsal | A fresh setup runs the documented flow. The actual demonstration fits three minutes. |
| 4 November | Submission and buffer | Verify code, product and video links. Submit before **6 PM California time or 9 PM Eastern time**. |

## The first 48 hours

Agree on a small set of permitted originals and a concrete caption question. Record the available dates and production facts before writing explanations. Build a plain visual matching baseline and actual source playback. Make one real Meta API call with an allowed input. Save a newly trimmed or resized query that is not mapped to a prewritten answer. Test an out of collection clip. Open the result on a phone.

If this path fails, repair or narrow the declared transformation support before adding features. Do not replace missing implementation with a scripted successful output. The first version supports trimming, reencoding, resizing and a limited center crop; speed changes, mirrored footage, composites and arbitrary shot reordering remain exploratory.

## Source coverage and access

The first pilot serves people exchanging clips represented in the permitted collection. The upload page states what collection is searched. A share URL does not automatically provide permission to download arbitrary social media video or comments. File input is the reliable first entry point. Publish coverage and unresolved results alongside successful examples.

<!-- PAGE BREAK -->

## Acceptance tests

All numbers here are prospective engineering targets. No application performance or user result has been measured yet.

| Area | Target and reporting rule |
| --- | --- |
| Source matching | At least 18 of 20 held out supported edits identify the correct source with both start and end offsets within two seconds. |
| Unknown sources | Zero authoritative wrong source assignments on 10 out of collection clips, including similar distractors. This small test does not establish internet wide reliability. |
| Evidence selection | On 12 prelabelled answerable cases, at least 10 supported and playable answers, with at least two more successes than full source Spark under the same retrieval and settings. |
| Unresolved claims | Add six unresolved cases. Across all 18 cases, no unsupported factual correction. Report answer coverage so universal abstention cannot pass. |
| Recipient usability | At least four of five nonteam volunteers identify what is supported, state what remains unknown and replay the evidence without coaching. Report counts and assistance. |
| Operation | Record processing time, source access time, model usage, cost and playback failures. Cost and latency are secondary outcomes, not a substitute for an evidence selection failure. |

Freeze development and final test source families, query edits, labels, thresholds and run counts before final evaluation. Test originals may be indexed; final query edits cannot be used for tuning. Two reviewers should judge evidence support independently and be blinded to condition where feasible. If only team members review, disclose that limitation. Preserve disagreements and failed cases.

## Submission quality

The official category weights are impact 30, Meta tooling 25, technical execution 20 and demo 25. Our goal is full credit through a working build, useful baseline comparisons, recipient understanding and a reproducible demonstration. Persona scores are planning feedback, not actual judges' scores or a promise of first place.

The participant guide lists **Simple Image Analyzers** among projects to avoid. Our proposed distinction is an actual source matching and evidence sharing workflow; the wording does not itself confirm eligibility. Use only authorized assets and clearly identify event built code.

## Working references

Participant guide: cerebralvalley.ai/e/meta-ai-developer-hackathon/details

Meta video and audio documentation: dev.meta.ai/docs/video-understanding

The Meta documentation warns that Spark 1.3 audio understanding is not fully supported. Test the chosen transcription path separately; do not promise exact word timestamps. Existing tools such as Meedan Check and InVID are prior art. Our claim is the specific working interaction we demonstrate, not the invention of verification.
