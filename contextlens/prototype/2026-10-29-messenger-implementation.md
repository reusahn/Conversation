# ContextLens messenger experiment — 29 October 2026

The Site's English home page is now a messenger-style, browser-local repetition prototype. The earlier source workbench is preserved at `workbench.html`.

## Try it

- **Try the repeat demo:** starts a clean conversation, sends original / crop / caption variants of one scene, then an extended cut. At the default limit, appearance 3 folds; the longer cut remains visible with about 3 seconds of added footage.
- **Up arrow:** sends another randomly ordered test clip. Shuffle replenishes and shuffles the sample deck.
- **Repeat filter:** restores or folds existing appearances without changing their recorded counts.
- **Filter settings:** configure a 2–5 appearance limit, view local history or credits, reset.
- **Plus:** choose a local file or compatible direct-video URL, up to 40 MB. No external video-page extraction. Downloads require CORS. This was browser-tested with a same-origin MP4 URL and a local MP4 upload; universal remote URL support is not claimed.

## Five samples / twenty actual media files

Five excerpts from **Sintel's official trailer**, not five separate films. Each has original, 10% center-crop, caption-overlay and extended variants. Source media: `https://media.w3.org/2010/05/sintel/trailer.mp4`. Catalog: `dist/assets/chat/catalog.json`.

**Sintel © Blender Foundation | www.sintel.org — CC BY 3.0.**
Official project record: https://durian.blender.org/news/sintel-teaser/
Sharing: https://durian.blender.org/sharing/
License: https://creativecommons.org/licenses/by/3.0/
Modifications: excerpting, crop, resizing, caption overlay, generated thumbnails. The complete trailer including end credits remains available in the source/credits dialog. All people, messages and repost scenarios are fictional; no creator endorsement.

## Actual implementation

`messenger.js` decodes six frames from the arriving clip and applies the existing RGB block matching algorithm to the trailer reference index. Matched starts are assigned to the five predefined source-window families within 0.7 seconds. This is a small sample-window demonstration, not general semantic grouping or an arbitrary-content detector; source windows can overlap. Other matches remain visible as unmatched to the five samples. No Meta model is connected.

An appearance is counted once per message when 60% of the message remains in the conversation viewport for 800 ms. Counts describe this tab's observed appearances, not completed views, comprehension or global audience exposure. Reload and reset clear the session. No message/file/history upload to a server is performed by this implementation.

For each family, compare its matched source interval with the union of prior appearances' intervals. New spans under 0.4 seconds are ignored as alignment noise. Longer additions retain the clip and receive a green interval indicator. This means extra footage relative to earlier posts, not verified new information or automatic commentary understanding. Match failures remain visible. Folded video controls are disabled until reveal; reveal is reversible via Compare. Offscreen videos pause.

## Validation actually performed

- JavaScript syntax checks passed.
- All 20 generated files decoded with FFmpeg, and duration checks passed.
- All 20 generated variants matched within 0.7 seconds in the small fixture check (`scripts/check-chat-media.py`, `scripts/check-chat-matches.cjs`). This is not a held-out/general accuracy result.
- Chrome preview: guided sequence recorded 4 appearances and folded 1 at limit 3. Cropped/captioned variants recognized. Longer cut retained with about 3 added seconds; source match 00:23–00:32, frame distance 0.0320, 5 useful query frames.
- Clicking the addition played from about 6.29 seconds in the 9-second query.
- Filter off restored posts; filter on reapplied folding. Rule 2 folded the second local snow appearance. Show video restored it; local history retained both counts.
- A same-origin direct MP4 URL and local file chooser import succeeded and shared a scene counter. A YouTube page URL returned a clear unsupported-page error.
- Two initial truncated media files were detected and rebuilt. The final validation above was run after repair. A low-detail sample failed the existing matching rule; it was replaced with a visibly different source-window excerpt without lowering thresholds, and all final sample variants were checked again.
- Desktop visual QA completed, screenshot saved. Responsive CSS exists; no full mobile/device matrix was run.

Not connected: Messenger/Instagram accounts, native feed ranking, platform-wide statistics, real users or messages, AI semantic comparison, internet source search. No efficacy study or competition score.

Rebuild sample media: `python scripts/build-chat.py` (FFmpeg with libx264 / drawtext required). Then `python scripts/check-chat-media.py` and `node scripts/check-chat-matches.cjs`. The generated media/index ship with the buildless static site.


## Deployment provenance

{
  "project_id": "appgprj_6ae12b3d03a08191b644d841b8a542c7",
  "source_commit": "d81d9ad9ac8adad70e44658b54fd3e11d3490e1e",
  "version_id": "appgprj_6ae12b3d03a08191b644d841b8a542c7~appgver_63f6e7f9c9fc8191b98f8d49014cada0",
  "deployment_id": "appgdep_6ae3b5ffa1d48191bd16e9af899138a9",
  "status": "succeeded",
  "url": "https://contextlens-workbench.reusahn.chatgpt.site",
  "audience": "owner-private, preserved",
  "checkout": "/workspace/scratch/3dfc4989fa36/.sites-checkout"
}

Native deployment succeeded. Browser checks were conducted on the matching managed preview, not an authenticated production session.
