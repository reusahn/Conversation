# ContextLens
**Less repetition. More control.**

**Problem**
The same short video can reappear through different accounts, crops, captions, and edits. Viewers may repeatedly encounter familiar footage while having little control over that repetition. Simply hiding similar videos can also remove useful commentary or follow-up scenes.

**Our proposal**
ContextLens is a viewer-controlled filter that recognizes repeated footage, shows personal appearance counts, and folds repetitive posts after a configurable limit—three appearances by default. A blurred preview explains the decision, and viewers can reopen any video.

The key feature is preserving what changes: extended footage remains visible, while a planned Meta-model component will compare captions and commentary to help identify substantive additions. Uncertain cases remain visible.

**Hackathon prototype**
An English messenger-style web app simulates a conversation using five openly licensed sample clips and their edited variants. The current prototype supports visual matching, repetition counts, adjustable blur controls, added-footage playback, local uploads, and compatible direct-video links. It is not connected to Instagram or Messenger.

**Planned Meta integration**
We will test Muse Spark for comparing accompanying text and commentary, grounding its explanations in the supplied material. This integration is not yet implemented.

**Validation**
We will test unseen edits and unrelated clips, measure incorrect grouping, and check whether useful additions remain accessible. Short usability sessions will assess whether people understand and can override the filter.

**Goal**
Give viewers practical control over repeated exposure while preserving access to new material.
