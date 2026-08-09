## Why

The project currently ships a placeholder "hello world" watch face (a plain digital clock with a static greeting) and no defined visual identity. The user explicitly wants a watch face that stands apart from the generic, forgettable faces common on the Play Store — a distinct, fun theme to actually build toward. We landed on a retro arcade / Atari 2600 "attract mode" concept: chunky pixel-font digits, a black CRT-scanline background, and a small original moving sprite, scoped as an MVP first pass before layering on a scoreboard-style complication HUD.

## What Changes

- Replace the placeholder digital clock layout in `watchface.xml` with an arcade-themed scene: black scanline background, large blocky pixel-font time display in an Atari-inspired accent color, and one small original pixel sprite (a jet-like shape drifting over a river strip, inspired by the general "river shooter" genre but not tracing any specific game's copyrighted art, name, or logo) whose position drifts based on the current seconds.
- Add a custom bitmap font (digits 0-9 and colon) built from generated pixel-art glyph images, registered via `BitmapFonts` in `watchface.xml`.
- Add new drawable assets: scanline background, river strip, jet sprite, and bitmap font glyphs — generated as original pixel art (via a local script), not sourced from or derived from any copyrighted game assets.
- Add an ambient-mode variant: sprite/river hidden (alpha 0) and digits rendered as a simple thin/outline style, consistent with Wear OS ambient battery and burn-in guidance.
- Update `strings.xml` watch face name to reflect the new theme (avoiding any third-party game trademark, e.g. not "River Raid").
- Out of scope for this MVP: the top scoreboard/complication HUD ("1UP"/step-count score row), multi-color per-digit palette, and animated (multi-frame) sprite — these are explicitly deferred to a follow-up change.

## Capabilities

### New Capabilities
- `watchface/arcade-theme`: Defines the visual behavior and content of the watch face's active and ambient scenes — the arcade-styled time display, background, and moving sprite, and how they respond to time and ambient-mode transitions.

### Modified Capabilities
(none — this is the first themed capability for this watch face; the current "hello world" scene has no existing spec to modify)

## Impact

- Affected files: `watchface/src/main/res/raw/watchface.xml`, `watchface/src/main/res/values/strings.xml`, new files under `watchface/src/main/res/drawable/` (background, river, jet sprite, bitmap font glyphs) and `watchface/src/main/res/font/` or `res/drawable/` for bitmap font characters.
- No build/dependency changes — the module remains `hasCode=false` (pure Watch Face Format XML + image resources), so no Kotlin/code is introduced.
- No breaking changes to app identity (`applicationId`, `minSdk`) or manifest structure.
- Follow-up change (not part of this proposal): scoreboard/complication HUD row, animated multi-frame sprite, preview.png regeneration to match the new theme.
