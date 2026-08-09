## 1. Arena pixel-art assets

- [x] 1.1 In `watchface/scripts/generate_pixel_assets.py`, remove `generate_river_strip()` and `generate_sprite_jet()` (and their call sites in `main()`), and delete `river_strip.png`/`sprite_jet.png` from `watchface/src/main/res/drawable/`.
- [x] 1.2 Add a `generate_divider()` function producing a thin, bright vertical bar PNG sized for the arena band. Sized 6x48 (not 64) — matches the ship sprite height rather than the old river band height, since the ships needed a narrower vertical slot to stay clear of the circular clip (see 3.3).
- [x] 1.3 Add ship sprite generation (`generate_ships()`, driven by a `SHIP_ROWS_FACING_RIGHT` column-range grid mirrored via `_mirror_rows()`) producing two small original geometric wedge/triangle ships in distinct saturated colors (cyan, magenta) — not the time display's orange. First attempt had the triangle math backwards (apex/base inverted), producing ships pointing away from center instead of toward each other; fixed by reworking the row-range-to-column-range logic and re-checking a rendered mockup before wiring into XML.
- [x] 1.4 Add a `generate_missile()` function producing one small bright yellow bouncing-element square.
- [x] 1.5 Ran the script and visually spot-checked a composited mock layout (divider + both ships + missile) before wiring into XML — caught and fixed the ship-direction bug at this stage, before it reached the emulator.

## 2. Arena scene in watchface.xml

- [x] 2.1 Replaced the `arcade_track` `Group`'s two `PartImage` children (river strip, jet) with divider, left ship, right ship, then missile last (so it paints on top), per design.md's document-order decision.
- [x] 2.2 Added `<Transform target="x" value="...">` to the missile `PartImage` using the proven clamp-based triangle-wave formula. Confirmed via `adb logcat` (zero parse failures) and two screenshots at different `[SECOND]` values (26 and 55) showing the missile clearly on opposite sides of the divider.
- [x] 2.3 Left the `arcade_track` `Group`'s ambient `Variant` untouched — confirmed still correct in verification.

## 3. Verification

- [x] 3.1 Build succeeded with no XML/resource validation errors.
- [x] 3.2 Installed on the Wear OS emulator and checked `adb logcat` immediately — zero `fail`/`error` matches from the WFF runtime (only unrelated emulator `HWUI`/EGL graphics warnings). No regression to the inline-attribute bug.
- [x] 3.3 Visual verification found a real layout bug on the first pass: the ships (placed at x=30/x=380, in the old 64-tall/y=350 band) were almost entirely clipped by the circular watch face boundary, which narrows significantly near the bottom of the screen — only tiny slivers of each ship were visible. Recomputed the visible x-range at the band's most restrictive y-coordinate (circle equation `half_width = sqrt(225^2 - (y-225)^2)`) and moved the whole arena to a narrower, higher band (`y=346`, ships/missile at `x=90`/`x=320`/bounce range `140-300`) that stays well within the circle at every row. Re-verified: divider, both ships, and missile all fully visible with margin; missile confirmed crossing the divider at different `[SECOND]` values; ambient mode hides the whole arena and returns cleanly on wake (`KEYCODE_SLEEP`/`KEYCODE_WAKEUP` round trip confirmed via screenshots).
- [x] 3.4 Confirmed via `git status`/`git diff` — only `res/` resources and `watchface/scripts/generate_pixel_assets.py` changed; no `AndroidManifest.xml`, `build.gradle.kts`, or `settings.gradle.kts` changes. Module stays `hasCode = false`.
- [x] 3.5 (Not in the original task list, added for consistency with the prior change.) Regenerated `res/drawable/preview.png` from a fresh emulator screenshot of the working arena scene, replacing the now-stale river/jet thumbnail.
