# ContextLens — product proposal v3

Status: design proposal after three discussion rounds, 27 October 2026. No application implementation, Meta API execution, matching measurements, recipient tests or organizer approval has been achieved in this session.

## Product commitment

**Share the clip with the evidence that explains this specific claim.**

The initial pilot serves viewers exchanging material represented in the permitted reference collection. The upload page shows the collection searched. An unknown result says no match was found in this collection, not that no original exists. A viewer supplies an allowed clip and the caption accompanying it, then taps one concrete question. ContextLens searches a disclosed, rights-cleared source collection and returns an account-free page connecting that exact caption/question to playable source moments and available production/date records. The recipient can inspect the evidence, expand its surrounding context and share the same result snapshot.

The proposed contribution is the executed connection between the supplied claim, a matching source interval, question-relevant evidence and the recipient's replayable result. Source search, provenance, messaging bots and fact-checking are established fields; historical novelty and universal truth detection are not claimed.

## What changed after the actual team discussion

1. Original-link discovery alone is insufficient: show which source moment or record addresses the actual question.
2. Preserve the exact supplied caption separately from the viewer's question, including whether a question came from supplied comments. A comment cannot silently become a post assertion.
3. Bind each shared page to this clip/caption/question analysis snapshot. Re-captioned footage requires its own finding; a general verification badge cannot travel with it.
4. Use question buttons rather than requiring a written prompt: when the footage was already available, production origin, surrounding action. Keep unanswerable questions visible.
5. Validate references mechanically but audit meaning independently. Valid IDs do not prove semantic support.

## First version and architecture

- Input: local MP4 clip up to 30 seconds plus supplied post text; no account. Clearly identify the reference collection searched.
- Ingest: timestamped visual fingerprints and available aligned transcripts/scene chunks, plus typed reference records. Existing matchers are attributed dependencies.
- Match: retrieve candidate frames and confirm temporal correspondence; output source ID and source interval or unknown. Freeze matching thresholds before evaluation.
- Initial supported transformations: contiguous trimming, re-encoding, resizing, and center crops removing at most 20% of the original total width or height. Speed changes, mirrored footage, mixed-source composites and arbitrary shot reordering are exploratory, outside initial support.
- Evidence: store evidence ID, source ID, media/content hash, corpus version, evidence type, source interval when applicable, record URL and retrieval time. Distinguish event date, filming date, original publication date and repost date, including unknowns.
- Spark: extract explicit claims/questions, choose which available source records or scene/transcript chunks to inspect, and select evidence relevant to the chosen question. Limit the proposed investigation to three evidence-tool operations. This is useful only if it outperforms or improves access/cost relative to the defined simpler baselines.
- Output: exact caption, question origin, matching interval, one supported typed finding, playable source evidence, expand-context control, model-suggested relevance note clearly distinguished from records, and explicit unknowns. Restricted templates render typed dates/production records. No universal fake/real or AI-probability score.
- Validation: enforce existing evidence IDs, accessible media, interval bounds, required types and valid result schema. Semantic relevance/support remains model-proposed and independently evaluated, never certified by the schema checker.
- Fallback: if matching is unknown or evidence selection fails, show searched coverage and unresolved fields; if a source is matched but the question cannot be resolved, show the actual match and available records without inventing an answer.
- Sharing: an immutable analysis snapshot with a stable link; account-free phone playback. Sharing is manual.
- Trace: redacted tool input/output, configurations, model ID, usage, timings and structured result; no credentials or private model reasoning.

## Optional comments

Use only supplied/authorized comments. They may prioritize a question, never establish truth, private belief or the post author's claim. Show bounded sample counts and ambiguity; questions, explicit statements, doubts and unclear/ironic expressions stay distinct. No “percentage fooled.” Inaccessible comments are not zero comments. The product works without this panel.

## Model and access constraints

Use Spark where question/evidence selection requires multimodal or semantic reasoning. Deterministic dates and matching should not be delegated to narrative intuition. Meta's current video guide documents visual understanding, but warns that Spark 1.3 audio understanding is not fully supported. Test the selected transcription path separately; never invent word timestamps. SAM and Muse Image are not required unless a proven task needs them. Instagram integration is not a first-version dependency; a shared URL does not grant arbitrary media/comment access.

## Frozen evaluation plan, to run after implementation

These are prospective acceptance targets, not results. Freeze the manifest, hashes, transformations, thresholds and labels before testing. Development-source and final-test-source families are disjoint for threshold tuning. Test originals may be indexed; final query edits and labels are held out. Use at least five test-source families.

1. **Matching:** at least 18 of 20 held-out supported edits match the correct source and interval with both start and end offsets within two seconds. Test 10 out-of-collection clips, including similar distractors; target zero authoritative wrong source assignments. Report numerator/denominator and every error. These small counts do not estimate internet-wide reliability.
2. **Claim grounding:** reuse a subset of query footage under supported, contradicted and unresolved captions. Count retrieval once per clip; evaluate caption grounding separately. Dates must be typed. Earlier publication establishes that footage existed by then, not when the depicted event occurred. Creation records establish documented/declared production origin; visual appearance is not AI proof.
3. **Evidence support:** two independent reviewers label atomic assertions as supported, contradicted or unresolved against the cited evidence, blinded to system condition where feasible. Preserve disagreements; report unsupported correction clauses / all correction clauses, cases with any unsupported correction, and answerable-case coverage. Do not let universal abstention pass.
4. **Primary comparison:** freeze twelve prelabelled answerable caption/question cases. A successful case requires a supported finding, evidence relevant to that exact question, a functioning citation, and preserved unknowns. Compare question-directed Spark to Spark given full available source transcript/records, holding candidate retrieval, model version, generation settings, output contract and predeclared run counts constant. Prospective gate: at least 10/12 full-system successes and at least two additional successes versus full-source Spark. Add six predeclared unresolved cases; no unsupported factual correction across all eighteen. Report coverage and abstentions. Record the fixed-window/source-metadata baseline separately. Cost, latency and evidence-access time are secondary endpoints; a failed primary comparison cannot become a win by selecting a favorable secondary result. Publish paired outputs and all failures. The small suite is an engineering gate, not a statistical significance or broad impact claim.
5. **Usability:** five non-team volunteers receive results on phones; target at least four independently identify what is supported, what remains unknown, and replay the cited evidence. Record assistance and failure counts. This is a narrow usability check, not a belief-change or misinformation-impact study.
6. **Operations:** measure end-to-end processing and evidence-access time, p50/p95 where sample size permits, per-request usage/cost and playback failures. A suggested 60-second first-use budget is to be tested, not promised.

## Demo plan: 180 seconds, contingent on a working build

- 0–20: a viewer preparing to share an exciting clip; state the exact question.
- 20–90: process a newly transformed authorized query against a frozen index; show the match and click its evidence.
- 90–120: same footage, accurate production caption versus a claim that it was first filmed today. Same match, evidence-specific answers; filming/event dates stay unknown unless recorded.
- 120–145: out-of-collection footage or no production record; show justified unknown rather than an AI accusation.
- 145–180: open the actual shared result on another phone; show measured baseline/error/cost results and disclosed coverage.

All footage and records must be authorized. Team-created demonstration captions/comments must be labelled demonstration fixtures. The source-match and evidence selection must execute, not resolve a URL to a prewritten correct answer. Do not edit latency out of an alleged live run.

## Fixed excellence checklist: 100 possible points

Official category weights are 30/25/20/25. The following subchecks are the team's own operational interpretation, not official organizer subweights.

| Dimension | Full-credit evidence required |
| --- | --- |
| Impact /30 | Specific sharing task (10), consequential evidence answering it (10), observed recipient understanding (10) |
| Meta tooling /25 | Substantive structured model work (10), measured value over simpler presentation (10), supported outputs and failure handling (5) |
| Technical depth/execution /20 | Held-out source/interval matching (8), unknown/citation handling (6), reproducible deployed path with measured latency/cost (6) |
| Demo /25 | Real unseen-query run (10), accurate/unknown controls (5), independently usable shared result (10) |

Do not award these as achieved execution points for a written plan. Final persona scores, if given, are explicitly speculative concept-readiness judgments; they are not predictions of actual judging. Full credit requires implementation evidence. No number of dialogue rounds can create missing observations.

## Build priorities through submission

- Oct 27–28: audit usable source assets and records; prove upload, real source/interval matching, evidence playback and an unknown case. Test actual Meta video/tool API capabilities.
- Oct 29–30: evidence schema, question selection, caption-bound shared page, account-free phone playback; record baseline outputs.
- Oct 31–Nov 1: freeze final suite and perform the held-out tests; independent semantic audit; fix on development data and disclose any new test version.
- Nov 2: recipient usability checks; revise wording/interaction while preserving test history. Optional comment priorities only if the core passes.
- Nov 3: public reproducibility check, measured demo rehearsal and source/asset review.
- Nov 4: final submission buffer; deadline 6 PM California / 9 PM Eastern. Public submission code must identify work built during the event.

## Open gates

Actual API call, rights-cleared source coverage, robust matching, comparative Meta value, semantically supported outputs, recipient understanding and final organizer eligibility remain unverified. The guide's “Simple Image Analyzers” wording is not a blanket vision ban or a project approval.

Review outcome: all five written review artifacts support building this direction, with amendments incorporated for pilot coverage, typed recency wording, both interval boundaries and a frozen primary endpoint. Ivan preferred relevant-evidence access as the primary outcome; the facilitator selected Sinan's independently adjudicated evidence-answer success rule and retained access time as a secondary endpoint. This is a documented design decision, not a further unanimous review of v3. The same fixed excellence checklist remains. Missing execution observations have not been awarded as achieved points.
