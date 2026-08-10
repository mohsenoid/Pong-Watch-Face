## Why

**Revised twice during implementation** — see design.md's Context for the full story. The original plan (a two-color background split rotating like a clock hand, driven by `[MINUTE]`) hit a real WFF limitation: `Transform target="rotationDegrees"` was confirmed not to apply to a generic `PartImage` on this runtime. Around the same time, the user found a different reference they preferred anyway — a "Split"-style watch face with a **static** divide — and asked to build that instead. The color-swapping digits idea (rendering each digit twice, masked to the opposite background half) was then attempted and **abandoned**: `renderMode="MASK"` did not clip content in any safe, predictable way on this runtime (see design.md and tasks.md task group 3 for the full investigation) — it either did nothing or blanked the entire rest of the scene. Digits ended up a single fixed white color instead, which still reads well against both background halves. Final palette settled on purple/orange (the user's preference) rather than the intermediate dark-charcoal/orange attempt.

## What Changes

- Replace the black scanline background with a static two-color split: dark charcoal on top, orange (reusing the existing accent color) on the bottom, divided by a horizontal line positioned so the time digits visibly straddle it.
- Make the time digits swap color depending on which background half they're over: each digit position is rendered twice — once dark, once orange — with each copy clipped/masked to only the region matching the *opposite* background color, using WFF's `renderMode="MASK"` mechanism. **This masking approach on the existing `TimeText`-based digits is unverified on this runtime** (see design.md's risk/fallback) — this project has already found one case (`Transform` on `TimeText`) where a documented WFF feature silently didn't apply to `TimeText` specifically, so masking needs the same on-device verification discipline before committing to it, with a documented fallback (per-digit-value conditional `PartImage`s, the same pattern already used for the hour-tens digit) if it doesn't work.
- Add day-of-week and date text near the top of the face, in the dark region, using expression tokens (`[DAY_OF_WEEK_S]`, `[MONTH_S]`, `[DAY]`) that are sourced from documentation/search rather than this project's own prior verification, so they need the same on-device check as everything else before being trusted.
- Keep the Pong arena (paddles, dashed divider, ball) as-is on top of the new background, per explicit user choice — accepting the risk that its white/yellow palette wasn't designed against this new backdrop, to be checked visually.
- Turn the scanline texture from an opaque background fill into a faint semi-transparent overlay on top of the new split background, so some of the retro-CRT texture identity is preserved without hiding the new colors.
- No change to the digit font shapes themselves (still the transcribed Atari pixel-grid glyphs), the hour-tens digit logic, ambient-mode time text, or branding.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `watchface/arcade-theme`: adds a new background requirement (static two-color split) replacing the scanline-only background requirement, a new requirement for color-swapping digits, and a new requirement for date/day-of-week text; scanline requirement's wording changes from a background fill to an overlay.

## Impact

- Affected files: `watchface/src/main/res/raw/watchface.xml` (background layer, duplicated/masked digit layers, new date/day text), `watchface/scripts/generate_pixel_assets.py` (generate a second, dark-colored set of digit glyphs and mask shapes; generate the static split background; adjust scanline generation to be a semi-transparent overlay).
- No build, manifest, or dependency changes — module stays `hasCode = false`.
- Real risk of a masking-on-`TimeText` dead end requiring a fallback to a more XML-heavy `PartImage`-based digit approach — flagged explicitly in design.md rather than assumed away.
