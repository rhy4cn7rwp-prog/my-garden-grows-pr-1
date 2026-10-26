# My Garden Grows — PR #1 iPhone playtest

Separate playable review build for
https://github.com/rhy4cn7rwp-prog/my-garden-grows-preview/pull/1

Source revision: `c40273c9cec9987190a4a493ff60ca9fc6d6a91f`.

Preview: https://rhy4cn7rwp-prog.github.io/my-garden-grows-pr-1/

This repository exists only to host this PR review build. It does not deploy to,
modify, or merge into either existing game repository/site. Artwork and game
source match the PR revision except for the documented hosting-only changes.

## Saved progress

GitHub Pages project sites for one account share a browser origin. The review
build therefore uses independent `mgg-pr-1:mgg10` and `mgg-pr-1:mgg10-backup`
save keys. Before starting for the first time, `preview-storage.js` copies any
existing `mgg10` / `mgg10-backup` records **without writing or removing them**.
It preserves the copied wallet, purchases, treasure placement and active market
through the game's normal recovery process. Further playtest progress stays in
this review save; it never replaces progress on either existing site.

Use the same Safari profile and regular browsing mode to copy an existing farm.
A different browser/profile or Private Browsing may not have that save available.
No site data needs to be cleared. Existing PR saves are never overwritten by the
copy step. Reading/turning the guide remains optional and does not change progress.

## Updating

This is a pinned review build, not automatic deployment from the PR branch.
`preview-manifest.json` records the exact source revision and hosting-only changes.
Update this repository only when a new PR revision is ready for playtesting; keep
the same namespaced keys to preserve this playtest's progress. Do not merge or
publish it to the existing public game as part of a review deployment.
