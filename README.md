# Aureon — design preview

A clickable mock-up of the proposed Aureon design, published so the discussion in
[retrohog/Aureon#1](https://github.com/retrohog/Aureon/issues/1) can point at something real.

**Live:** https://retrohog.github.io/aureon-design/

## What this is

A single self-contained `index.html`. No build step, no dependencies except the Google Fonts
stylesheet. Open it in any browser — every control works: theme, density, typeface, screens,
the Home recommendation preview, the mini player settings and the menu bar player.

It is a design artefact, not the app. Nothing here ships; the app is
[retrohog/Aureon](https://github.com/retrohog/Aureon).

## Publishing a new version

Double-click **Publish Design.command** on the Desktop (or inside this folder). It takes the
newest `Aureon Pulse.html` from the Desktop, restores the share metadata in `<head>`, commits
and pushes it here. GitHub Pages then serves it at the same URL, usually within a minute.

Run from a terminal instead:

```sh
python3 publish.py            # uses ~/Desktop/Aureon Pulse.html
python3 publish.py path/to/file.html
```
