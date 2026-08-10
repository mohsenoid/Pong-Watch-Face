## Context

Colors currently live in two places: `watchface/scripts/generate_pixel_assets.py` (Python constants baked into generated PNGs — `ACCENT_COLOR`, `SPLIT_TOP_COLOR`, `DIGIT_COLOR`) and their references in `watchface.xml` (`bg_split`, `digit_0`..`digit_9`, `digit_colon`, `hour_leading_one`). Three of the five digit positions (`hh_1`, `mm_10`, `mm_1`) are `TimeText` elements using a `BitmapFont` (`family="arcade_digits"`); the other two (hour-tens conditional digit, colon) are plain `PartImage`s.

**Palette source changed mid-implementation.** The user provided a well-researched list of 14 classic-Atari/arcade-inspired color pairs, all structured as a single dark background plus a single bright accent color (the classic vector-monitor CRT look — green-on-black, amber-on-olive, etc.), not a two-tone top/bottom split. This is a better fit for the retro-arcade aesthetic than the originally-drafted two-tone split palettes, so the background model changes from "two colors split by a horizontal line" to "one solid background color plus one accent color used for the digits" — simpler visually and, as it turns out, simpler to implement too (only one background region to color instead of two). This also means the existing `Static two-color split background` requirement (added by the prior `duo-color-hand-background` change, already synced to the main spec) is being removed/replaced by this change — see the delta spec.

**Confirmed via on-device testing (task group 1):**
- `[CONFIGURATION.<configId>.<colorIndex>]` expressions work, but the indexing was initially misunderstood and caused a real crash (`IndexOutOfBoundsException`) during testing: the index selects **which color within the currently-selected option's `colors` list**, not which option. A `ColorOption` with `colors="#FFFFFF"` (one color) only has valid index `0` — referencing `.1` on it crashes the renderer (`java.lang.IndexOutOfBoundsException: Index 1 out of bounds for length 1`, visible in `adb logcat`). Fixed by giving each option multiple colors and referencing them correctly.
- `tintColor="[CONFIGURATION...]"` **works on `PartImage`** — confirmed by tinting a white test square to a `ColorOption`'s second color and seeing it render red as expected.
- `tintColor` **does not work on `BitmapFont` inside `TimeText`** — same test pattern applied to a live digit's `BitmapFont` left it unchanged (still white), no logcat error either (a silent no-op, consistent with this project's established pattern of `TimeText` not supporting things `PartImage` does).
- A separate, harmless `DWF:ResourceManager: Failed to read from inputStream error: Path is empty or null` warning appears repeatedly once `UserConfigurations` is present, independent of whether `tintColor` succeeds or fails — most likely related to the `ColorOption`/`ColorConfiguration` elements not having an optional preview-icon resource, which this project doesn't set. Does not appear to affect actual watch face rendering; not treated as a blocker.

Given `tintColor` doesn't reach `TimeText`, the digit-coloring mechanism still needs to be resolved (in progress — see Decisions).

## Goals / Non-Goals

**Goals:**
- 7 selectable color themes (solid background + one accent color for the digits), sourced from the user's Atari-inspired palette list, with generic (non-trademarked) display names.
- Selection happens through the watch face's own native configuration UI (`UserConfigurations`/`ColorConfiguration`) — no custom in-app picker.
- Resolve digit theming using only mechanisms confirmed to actually work on this runtime, not assumed from docs/samples.

**Non-Goals:**
- The Pong arena (paddles, ball, divider) and the date/day text keep their current fixed colors — not themed in this change.
- No new game mechanics, layout changes, or digit font changes.
- Theme option labels reference colors/moods, never specific game titles (extends the existing no-trademark requirement) — e.g. Battlezone's green-on-black becomes "Night Vision", not "Battlezone".

## Decisions

**Fifteen palettes (top/bottom split background): the original look plus all 14 user-supplied pairs, generically named:**

| # | Name | Top | Bottom | Inspired by (not shown in UI) |
|---|------|-----|--------|-------------------------------|
| 0 | Classic Arcade (default) | `#5A3CC8` | `#FF6A00` | the watch face's original, pre-theme-system look |
| 1 | Night Vision | `#081C08` | `#00FF66` | Battlezone |
| 2 | War Room | `#3A422D` | `#FFC000` | Combat |
| 3 | Radar Yellow | `#0A0E29` | `#FFFF00` | Missile Command |
| 4 | Crimson Sky | `#2A0505` | `#FF2222` | Red Baron |
| 5 | Neon Magenta | `#1A0F24` | `#FF00FF` | Yar's Revenge |
| 6 | Copper Cyan | `#5C1D0C` | `#00E5FF` | Dig Dug |
| 7 | Jungle Vine | `#261A0A` | `#D4FF00` | Pitfall! |
| 8 | Emerald Grid | `#0D1F1D` | `#70FF30` | Adventure |
| 9 | Molten Amber | `#111827` | `#FF8000` | Breakout |
| 10 | Venom Pink | `#062419` | `#FF007F` | Centipede |
| 11 | Golden Marsh | `#0C1B40` | `#FFD700` | Frogger |
| 12 | Cosmic Cyan | `#120626` | `#00FFFF` | Asteroids |
| 13 | Desert Amber | `#2E1B05` | `#FFC700` | Defender |
| 14 | Signal Green | `#0A1128` | `#00FF33` | Space Invaders |

Index 0 (Classic Arcade) stays the default, matching the watch face's original purple/orange appearance — per direct user feedback ("I am missing the original yellow and purple, let's have it as the first option") after an earlier iteration made a palette-based theme ("Night Vision") the default. Themes 1-7 were the initial hue-variety subset of the user's 14-pair list; themes 8-14 (Adventure, Breakout, Centipede, Frogger, Asteroids, Defender, Space Invaders) were added afterward per a follow-up request to include the remaining pairs rather than only a subset ("can we add more, I shared 14 colors").

**Course correction during implementation:** the first working version of this change tinted the *digits* to each theme's accent color and used a single solid *background* color (`tintColor="[CONFIGURATION.themeColor.N]"` on the digit `PartImage`s and on one full-canvas background `PartImage`). This was built, verified on-device, and worked correctly — but after seeing it live, the user's feedback was explicit: digits should stay white ("White was a great fit"), and instead the *background* should be the themed element, split into two colors like the watch face's original look. The two colors already defined per theme (previously "background" + "accent") were repurposed as "top" + "bottom" split-background colors, and all `tintColor` attributes were removed from the digit/colon/hour-leading-one `PartImage`s. No new drawables were needed for the split — the existing single white `bg_solid.png` is reused for both halves via two `PartImage`s with different `height`/`y` (0–205 and 205–450) and `tintColor` referencing index 0 and index 1 respectively.

**Background: two `PartImage`s covering the top and bottom halves, each `tintColor="[CONFIGURATION.themeColor.0]"` / `.1`.** Confirmed working — same `bg_solid.png` white source reused for both, scaled into each half's bounds.

**Digits: fixed white, no `tintColor`.** `TimeText` was confirmed to support no dynamic mechanism at all (see below), so digits were already converted to the `PartImage`-per-conditional-value pattern regardless of theming — that conversion stayed, but the `tintColor` attribute was removed from all 28 of those `PartImage`s per the correction above.

`TimeText` limitation (why the `PartImage` conversion happened at all): tested `Transform target="alpha" value="0"` (hardcoded, cheapest possible test) directly on a live `TimeText`: the digit stayed fully visible, no logcat error. Combined with the earlier `Transform target="x"` (previous change) and `tintColor` (this change) findings, `TimeText` does not respond to any `Transform`-driven attribute change on this runtime - only `<Variant mode="AMBIENT">` (a different, system-mode-tied mechanism) reliably changes its alpha.

Final approach: convert all three live digit `TimeText` positions (`hh_1`, `mm_10`, `mm_1`) to the `PartImage`-per-conditional-value pattern already proven for the hour-tens digit - one `PartImage` per possible digit value, `Transform target="alpha" value="([<data source>]==N)*255"` to show only the matching one. Value counts: `hh_1` and `mm_1` need all 10 digits (0-9); `mm_10` (minutes tens digit) only ever takes values 0-5, so needs 6. Total 26 conditional `PartImage`s replacing 3 `TimeText`s. The digit-value data sources are the same ones already connected under the hood by the current `TimeText format` tokens (confirmed via `adb logcat` in the very first version of this watch face: `HOUR_UNITS_DIGIT`, `MINUTE_TENS_DIGIT`, `MINUTE_UNITS_DIGIT`), used directly instead of going through a `TimeText format` string.

Digit glyphs stay a single neutral white set (`DIGIT_COLOR` in the generator script), fixed across all themes.

**Arena and date text stay fixed-color** — per the Non-Goals, keeps the change scoped.

**Edit button discoverability bug found and fixed:** after implementing the `ColorConfiguration` and confirming it worked (by forcing `defaultValue` and rebuilding), the watch face's on-device Edit (pencil) button was still missing from the favorites/long-press carousel — confirmed on both the emulator and a real Pixel Watch 4, and confirmed it wasn't a general platform limitation by comparing against a built-in watch face (`MD284`), which *did* show the Edit button in the same carousel. Root cause: `res/xml/watch_face_info.xml`'s `<WatchFaceInfo>` has an `Editable` field that defaults to `false` and controls the Edit button's visibility — this project's `watch_face_info.xml` only declared `<Preview>`, never `<Editable value="true" />`. This is undocumented in the main WFF XML reference pages and only surfaced via `https://developer.android.com/training/wearables/wff/setup`. Fixed by adding `<Editable value="true" />`; confirmed the Edit flow now opens a real on-watch "Customize Watch Faces" > "Color Theme" editor on both the emulator and the real watch.

## Risks / Trade-offs

- [Risk] Changing the default theme (index 0) changes the watch face's out-of-the-box appearance from the current purple/orange/white to green-on-near-black. → Mitigation: called out explicitly here and in the proposal; this is an intentional choice per the user's direction, not an oversight.
- [Risk] If `Transform`-alpha doesn't work on `TimeText`, the fallback (full `PartImage` conversion for 3 digit positions x 7 themes) is a substantial `watchface.xml` rewrite. → Mitigation: build and verify one theme end-to-end before replicating the pattern; generate all glyph sets programmatically.
- [Risk] The benign `ResourceManager: Path is empty or null` warning could theoretically indicate a real (if currently invisible) problem. → Mitigation: watch for it growing into an actual rendering issue as more `ColorOption`s are added; if so, investigate adding preview-icon resources to `ColorOption`/`ColorConfiguration`.

## Migration Plan

Pure visual/resource + configuration change — no persisted user data beyond the watch face editor's own standard configuration storage. Rollout: finish the digit-theming verification, wire up all 7 themes, verify each visually and via `adb logcat`, confirm ambient mode and the Pong arena/date text remain unaffected. Rollback is a plain revert of the `watchface.xml` `UserConfigurations` block and any new drawable/script changes.
