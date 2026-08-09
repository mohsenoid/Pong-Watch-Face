## Context

`watchface/src/main/res/raw/watchface.xml` is a Watch Face Format (WFF) declarative XML file (450x450, `DIGITAL` clock type). The module has `hasCode = false` / `enableKotlin = false` — there is no Kotlin/Java code path, so everything must be expressed as static XML + drawable resources. The existing file already demonstrates the two relevant WFF mechanisms we'll reuse: `Variant` (`mode="AMBIENT" target="alpha"`) to swap opacity/appearance between active and ambient rendering, and `Parameter`/`Template` for dynamic text. See proposal.md for why we're replacing the placeholder scene.

WFF expressions use square-bracket data-source tokens (e.g. `[SECOND]`, `[HOUR_0_23]`) inside `x`/`y`/`rotationDegrees`/`alpha`-type attributes and inside `Condition`/`Template` content. Custom pixel-art digits are supported via a `BitmapFonts`/`BitmapFont`/`Character` block that maps each glyph to a `res/drawable` PNG.

## Goals / Non-Goals

**Goals:**
- Ship a working, on-device-verifiable arcade-themed watch face: scanline background, pixel bitmap-font time in Atari orange/red, one drifting original sprite over a river strip, and a battery/burn-in-conscious ambient variant.
- Keep every visual asset originally generated for this project (no downloaded fonts/art, no copyrighted game assets), per the copyright discussion in proposal.md.
- Keep the change entirely within `res/` (XML + drawables) — no build config, dependency, or manifest changes.

**Non-Goals:**
- No scoreboard/complication HUD ("1UP" / step-count "SCORE" row) — deferred to a follow-up change.
- No multi-frame sprite animation (wing flap, engine blink) or multi-color per-digit palette — MVP uses a static sprite image with a position transform only.
- No regeneration of `res/drawable/preview.png` in this change (the Play-Store-style preview thumbnail) — can follow once the on-device look is confirmed.

## Decisions

**Bitmap font via generated pixel-art glyphs, not a bundled TTF.**
A licensed pixel/arcade TTF (e.g. "Press Start 2P") would need to be downloaded and its license reviewed before bundling — extra friction and an external dependency. Instead we generate each digit (0-9) and a colon glyph as PNGs from a hand-authored 5x7 dot-matrix pattern, scaled up with nearest-neighbor resampling for crisp blocky pixels, using a small local Python (Pillow) script (Pillow 11.3.0 confirmed available locally). This keeps every asset original and license-free, and matches the WFF `BitmapFont`/`Character` mechanism already discovered. Ambient mode does not use this bitmap font at all (see below), so we don't need a second glyph set.

**Sprite motion via a position expression, not `PartAnimatedImage`.**
WFF supports frame-sequence/AGIF animation through `PartAnimatedImage`, but that requires an `AnimationController`, a `Thumbnail`, and multiple frame assets — more asset and XML surface than an MVP needs. Instead, the sprite is a single static `PartImage` inside a `Group`/`Transform` whose `translationX` (or `x`) is driven by a `[SECOND]`-based expression (e.g. a triangle-wave built from `clamp()`/`abs()` over `[SECONDS_IN_DAY]` or `[SECOND]`) so it drifts back and forth across the river strip. This gets "the watch face feels alive" for near-zero asset cost; multi-frame animation is an easy follow-up once `PartAnimatedImage` is validated on-device.

**Ambient mode reuses the existing `Variant` pattern, with a separate plain-font time text.**
Following the pattern already present in the skeleton file (two `TimeText` elements, one active one ambient, toggled via `Variant mode="AMBIENT" target="alpha"`), ambient mode gets its own `TimeText` using a plain thin system `Font` (not the bitmap font) in a single flat color — cheaper to render, avoids bitmap-font glow/color on OLED always-on, and matches Wear OS ambient guidance. The river/sprite `Group` gets `alpha` flipped to 0 in ambient via the same `Variant` mechanism used for the current `hello_world` group.

**Scanline texture as a single static background PNG, not per-line `PartDraw` elements.**
WFF has no loop construct; drawing N scanlines would mean N explicit `Line`/`Rectangle` elements in `PartDraw`. A single generated 450x450 PNG (black with faint horizontal darker/lighter bands at low alpha) is one `PartImage` and is simpler and cheaper to render.

**Watch face name: generic arcade description, not "River Raid" or any game title.**
Per proposal.md's copyright discussion, `strings.xml`'s `watch_face_name` is updated to something like "Retro Arcade" / "8-Bit Arcade" — descriptive of the genre/style, not a specific trademarked title.

## Risks / Trade-offs

- **[Risk]** Hand-authored 5x7 dot-matrix digits may look cramped or uneven at the chosen render size on a real 450x450 round display. → **Mitigation**: generate glyphs at a generous scale factor (e.g. 16x-20x the base grid) so we can size down in XML without blurring (bitmap fonts in WFF are raster, so oversampling is the only lever), and do an on-device visual check before considering the MVP done.
- **[Risk]** A `[SECOND]`-derived triangle-wave expression could be malformed (WFF expression syntax is easy to get subtly wrong) and silently fail to update or render statically. → **Mitigation**: start with the simplest possible expression (linear mapping, no `clamp`/`abs` combinators) and verify visually that the sprite actually moves before adding easing.
- **[Risk]** Frequent expression re-evaluation (e.g. keyed off `[SECOND]`) has a battery cost the WFF docs specifically call out. → **Mitigation**: this element is hidden entirely in ambient mode, and active-mode power cost is a known, accepted trade-off for a screen-on interactive face; revisit only if on-device testing shows a problem.
- **[Risk]** No emulator/simulator tooling is confirmed set up for WFF preview in this repo yet. → **Mitigation**: tasks.md will include a step to build and visually verify via `adb`/Wear OS emulator (or Android Studio's watch face preview) before calling the change done; if no device/emulator is available, this becomes a documented limitation rather than a silent skip.

## Migration Plan

No data migration — this is a pure visual/resource change to a single-scene watch face with no user data or persisted state. Rollout is: implement on this branch, visually verify on-device/emulator, then merge. Rollback is a plain revert of the XML/drawable changes (no schema or compatibility concerns).
