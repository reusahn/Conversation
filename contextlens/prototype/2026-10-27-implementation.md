# ContextLens browser prototype implementation

27 October 2026. This records actual work and limitations.

## Live prototype

https://contextlens-workbench.reusahn.chatgpt.site

Owner-private, with ChatGPT sign-in. No audience expansion was requested or performed.

## Implemented

- Actual local frame-descriptor matching of three transformed demo clips and local uploads against one reference.
- Source interval playback, surrounding context, original audio and synchronized comparison.
- Three variant clips converge on the same source through actual comparison, not a prewritten answer mapping.
- Supplied captions and questions are kept separate from source records. Comment expressions use bounded keyword/question rules; private belief is not inferred.
- Demo share URLs rerun and restore the comparison. An explicit URL dialog supports manual copying when clipboard access is unavailable. Local video bytes remain on the current device and must be exported for cross-device sharing.
- Evidence video recording actually exports a browser-supported MP4 or WebM file. Tested output: MP4 container, 960 x 600, 8.12 seconds, VP9 video plus Opus audio, 194378 bytes. A decoded frame was visually checked.

## Checks performed

All three sample variants matched. A fresh clip absent from the demo selectors, cut at 28.5 seconds in the reference, matched around 28.38 seconds in Chrome. An unrelated moving pattern clip returned unknown. Source record and AI-uncertainty questions, surrounding context, share URL restoration and MP4 download were checked through the browser UI. JavaScript syntax and fixture/package checks passed.

The reference index was increased from 4 fps to 8 fps after a crop exhibited temporal sampling error. Similarity thresholds were not relaxed to force a pass. These are development checks, not the earlier frozen final benchmark. No claim of internet-wide accuracy follows.

## Deliberately unconnected

Spark / Meta Model API, internet video search and Instagram integration are not connected. Date/production wording comes from explicitly authored records and rules. This is not a trained AI-generation detector. The earlier 20-query acceptance suite, model comparisons, external user study and impact claims remain unrun. No new persona scores were assigned.

## Footage and credits

Sintel © copyright Blender Foundation | www.sintel.org. CC BY 3.0. Full trailer with credits retained; excerpts/crop/resize and demonstration captions were added.

- https://durian.blender.org/news/sintel-teaser/
- https://durian.blender.org/sharing/
- https://media.w3.org/2010/05/sintel/trailer.mp4
- https://creativecommons.org/licenses/by/3.0/

Sample descriptions and comments are created fixtures, not actual posts or audience evidence. The creators do not endorse ContextLens.

## Deployment provenance

Project: appgprj_6ae12b3d03a08191b644d841b8a542c7

Source commit: f42cf58a16b7f552415f756b83e3985ae06ab7fb

Saved version: appgprj_6ae12b3d03a08191b644d841b8a542c7~appgver_cb73e9842cec8191abd5ed8ebdc8974f

Deployment: appgdep_6ae13115087c8191a8924aa5b0f85d8e

Native deployment status: succeeded. Browser tested the matching local source preview. A production visit showed ChatGPT sign-in; the agent did not complete a separate authenticated production UI session. Source is preserved in the Site's configured Git repository. Local checkout: /workspace/sites/contextlens-workbench-20261027.
