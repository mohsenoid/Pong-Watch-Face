## 1. Verify CONFIGURATION expressions and tintColor (before building all themes)

- [x] 1.1 Added a minimal `UserConfigurations`/`ColorConfiguration` (2 options) plus a throwaway white `PartImage` with `tintColor="[CONFIGURATION.themeColor.0]"`.
- [x] 1.2 Built, installed, checked `adb logcat` — found and fixed a real crash (`IndexOutOfBoundsException`) caused by referencing an out-of-range color index.
- [x] 1.3 Confirmed via screenshot that the test square renders in the expected tinted color (red), after fixing the index bug.
- [x] 1.4 Repeated with `tintColor` on a `BitmapFont` inside a live `TimeText` — confirmed it's a silent no-op (digit stayed white, no logcat error).
- [x] 1.5 Recorded findings in design.md: `tintColor` works on `PartImage`, not on `BitmapFont`/`TimeText`; `Transform target="alpha"` also doesn't apply to `TimeText`. Digits were converted to conditional `PartImage`s regardless of theming (needed for reliable rendering either way).

## 2. Define the themes

- [x] 2.1 Defined 15 theme palettes directly in `watchface.xml`'s `UserConfigurations`/`ColorConfiguration` (`colors="<top> <bottom>"` per option): index 0 is "Classic Arcade" (the watch face's original purple/orange look, restored as default per user feedback), indices 1-14 are all 14 user-supplied Atari-inspired color pairs. `generate_pixel_assets.py`'s old `SPLIT_TOP_COLOR`/`ACCENT_COLOR`/`SPLIT_Y` constants were removed (background halves are now tinted at render time from a single reused `bg_solid.png`, not pre-colored per theme).
- [x] 2.2 Added 15 generic theme display-name strings (plus a config label) to `strings.xml`.
- [x] 2.3 (Follow-up) Lightened the "dark" color of all 14 imported palettes — the raw user-supplied dark colors read as near-black at the top of the split, which looked noticeably worse than the vivid default purple. Rewrote each dark color's HSL lightness to ~25% (with a saturation floor) while preserving hue, via a one-off script; kept the accent/bright color unchanged. Verified visually on 4 themes (Night Vision, Crimson Sky, Cosmic Cyan, Golden Marsh) plus the unaffected default.

## 3. Implement background theming

- [x] 3.1 `tintColor` confirmed working on `PartImage`/`Image` (task 1). Background is a two-color top/bottom split (matching the watch face's pre-existing look), not a single solid color — reuses one plain white `bg_solid.png` in two `PartImage`s (0–205, 205–450) tinted via `tintColor="[CONFIGURATION.themeColor.0]"` / `.1`.
- [x] 3.2 N/A — tintColor path was viable, no conditional-visibility fallback needed.
- [x] 3.3 Built, installed, checked logcat, screenshotted the default theme (index 0, Classic Arcade) — background renders identically to the pre-existing look.

## 4. Implement digit theming

- [x] 4.1 Converted all three `TimeText` digit positions (`hh_1`, `mm_10`, `mm_1`) to 26 total conditional `PartImage`s (`Transform target="alpha" value="([<digit token>]==N)*255"`), using `HOUR_UNITS_DIGIT`, `MINUTE_TENS_DIGIT`, `MINUTE_UNITS_DIGIT`. Removed the now-unused `DigitalClock`/`BitmapFonts` blocks. Removed test scaffolding (`test_white_square.png`, throwaway config, leftover `alpha=0` artifact).
- [x] 4.2 Built, installed, checked logcat. **Course correction**: digits were initially tinted per-theme (`tintColor` on each digit `PartImage`) with a single solid background — this worked and was verified on-device, but per direct user feedback ("I didn't want to change the digits colors! White was a great fit.") this was reverted: `tintColor` was stripped from all 28 digit/colon/hour-leading-one `PartImage`s so digits stay fixed white, and the theming moved to the split background instead (see task 3).

## 5. Verify all themes

- [x] 5.1 Verified via the real on-device Edit flow (see task 6.3) plus `defaultValue` swap-and-rebuild spot checks: Classic Arcade (default), Night Vision, Crimson Sky, Cosmic Cyan, Golden Marsh — screenshotted on the emulator. The remaining themes use the same code path (same two `tintColor` expressions, same `ColorOption` structure) so are not expected to behave differently, but were not all individually screenshotted.
- [x] 5.2 All spot-checked themes show good digit/background contrast, including after the task 2.3 lightening fix (previously the imported palettes' dark top color was "always very dark" per user feedback; now a rich, visible shade instead of near-black).
- [x] 5.3 Confirmed the arena (paddles, ball, divider) and date text stayed fixed white/yellow across all spot-checked themes.
- [x] 5.4 Confirmed ambient mode still works: content freezes and dims correctly under the default theme.

## 6. Final verification

- [x] 6.1 Confirmed no build/dependency/manifest changes — only `res/raw/watchface.xml`, `res/values/strings.xml`, `res/drawable/*`, `res/xml/watch_face_info.xml`, and `scripts/generate_pixel_assets.py` changed. Module stays `hasCode = false`.
- [x] 6.2 Regenerated `res/drawable/preview.png` from the default (Classic Arcade) theme at 10:10 (the traditional watch-marketing time), and added 4 more theme screenshots to `docs/` for the README gallery.
- [x] 6.3 **Found and fixed a real discoverability bug**: the on-device Edit (pencil) button never appeared for this watch face, on both the emulator and a real Pixel Watch 4 — confirmed it wasn't a general platform limitation by comparing against a built-in watch face, which did show the Edit button. Root cause: `res/xml/watch_face_info.xml` was missing `<Editable value="true" />` (undocumented on the main WFF XML reference pages, only found via `https://developer.android.com/training/wearables/wff/setup`). Fixed and confirmed the Edit flow now opens a real "Customize Watch Faces" > "Color Theme" picker on both the emulator and the real watch.
