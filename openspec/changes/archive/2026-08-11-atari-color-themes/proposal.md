## Why

The watch face currently ships with a single fixed color scheme (purple/orange split background, white digits). The user wants a choice of color themes inspired by well-known Atari-era palettes, selectable from the watch face's own configuration UI (the standard long-press-to-edit flow), rather than being locked into one look.

## What Changes

- Add a native Watch Face Format `UserConfigurations`/`ColorConfiguration` with 15 selectable color themes. This is a built-in WFF mechanism (confirmed in the official `SimpleAnalog` sample, and re-confirmed by this project's own on-device testing: `ColorConfiguration`/`ColorOption` elements, referenced via `[CONFIGURATION.<id>.<index>]` expressions) — the watch face editor's system UI handles the picker itself, no custom UI is built here.
- Theme 0 (the default) restores the watch face's **original purple/orange split look** ("Classic Arcade") per user feedback that it was missed after the palette-based themes replaced it as default. Themes 1-14 each define two colors from the user-supplied list of 14 classic-Atari/arcade-inspired color pairs — all 14 are included, not just a subset. **These two colors theme the top/bottom split background** (the pre-existing two-tone split look), not the digits.
- **Digits stay fixed white across all themes** — confirmed via direct user feedback during implementation that white digits are "a great fit" and should not be tinted per-theme. (An earlier iteration of this change tinted the digits to the theme's accent color and used a single solid background color; that was reverted per this feedback.)
- Theme palettes are named generically by color/mood, not by any specific game title (e.g. Battlezone's green-on-black becomes "Night Vision") — consistent with the watch face's existing "no third-party trademark or branding" requirement, which this change extends to explicitly cover configuration/theme option labels too.
- Only the split background switches with the selected theme. The digits, the scanline overlay, the date/day text, and the Pong arena (paddles, ball, divider) are explicitly **out of scope** for per-theme coloring — they keep their current fixed colors (white/yellow).
- **The default theme is unchanged** — "Classic Arcade" (purple/orange) is index 0 and the default, matching the watch face's pre-existing out-of-the-box appearance. (An earlier iteration of this change made a palette-based theme the new default; that was reverted after user feedback that the original look was missed.)
- No change to layout, digit shapes/font, the hour-tens conditional logic, ambient-mode behavior, or the Pong game mechanics.
- Also fixed a real on-watch discoverability bug found during implementation: the watch face's `res/xml/watch_face_info.xml` was missing `<Editable value="true" />`, so the system's Edit (pencil) button never appeared for this watch face in the favorites carousel, even though `UserConfigurations` was present and functioning. This was silent — no logcat error, no XML validation failure — and would have made the theme picker unreachable in practice.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `watchface/arcade-theme`: adds a color-theme-selection requirement (7 selectable themes affecting background and digit colors) and extends the existing no-trademark requirement to cover theme option labels.

## Impact

- Affected files: `watchface/src/main/res/raw/watchface.xml` (add `UserConfigurations`, switch background/digit color references to `[CONFIGURATION...]` expressions), `watchface/src/main/res/values/strings.xml` (theme display-name strings), `watchface/scripts/generate_pixel_assets.py` (the digit-color generation approach needs to produce a full glyph set per theme's digit color, or a different rendering strategy — resolved in design.md).
- No build, manifest, or dependency changes — module stays `hasCode = false`.
- This is the first use of `UserConfigurations`/`ColorConfiguration` in this project. It's a well-established, core WFF mechanism (unlike the recently-discovered-broken `Transform target="rotationDegrees"` and `renderMode="MASK"`), but per this project's established discipline it still gets verified on-device early rather than assumed to work from the sample alone.
