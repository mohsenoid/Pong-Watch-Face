## 1. Pong pixel-art assets

- [x] 1.1 Removed `generate_ships()`, `_render_grid()`, `_mirror_rows()`, and the `SHIP_ROWS_FACING_RIGHT`/`SHIP_GRID_*` constants from `watchface/scripts/generate_pixel_assets.py` (nothing else referenced them), and deleted `arena_ship_left.png`/`arena_ship_right.png`.
- [x] 1.2 Added `generate_paddles()` producing plain 10x40 rectangle bars as `arena_paddle_left.png`/`arena_paddle_right.png`, reusing the prior cyan/magenta colors (renamed to `PADDLE_LEFT_COLOR`/`PADDLE_RIGHT_COLOR`).
- [x] 1.3 Changed `generate_divider()` to draw short dashes (6px on, 4px gap) down the column instead of a solid fill.
- [x] 1.4 Renamed `generate_missile()` to `generate_ball()`, output renamed to `arena_ball.png` (old `arena_missile.png` removed).
- [x] 1.5 Ran the script and visually spot-checked a composited mock layout (paddles + dashed divider + ball) before wiring into XML — confirmed correct on the first attempt this time (no repeat of the prior change's direction bug, since rectangles have no orientation to get wrong).

## 2. Pong arena scene in watchface.xml

- [x] 2.1 Replaced the two ship `PartImage`s with two paddle `PartImage`s (`arena_paddle_left`/`arena_paddle_right`), positioned at x=95/x=345 (narrower than the old ships, comfortably inside the circular-clip-safe zone with margin to spare).
- [x] 2.2 Divider `PartImage` now references the dashed `arena_divider` asset (position/size unchanged).
- [x] 2.3 Ball `PartImage` now references `arena_ball`, with `target="x"` using `[SECOND] % 4` (4-second horizontal cycle) and a second `target="y"` `Transform` using `[SECOND] % 5` (5-second, ~20px vertical bounce) for a diagonal path.
- [x] 2.4 Added `<Animation duration="1" interpolation="LINEAR">` inside both `Transform` elements.
- [x] 2.5 Ambient `Variant` on the arena `Group` left untouched — confirmed still correct in verification (3.6).

## 3. Verification

- [x] 3.1 Build succeeded with no XML/resource validation errors — including the two new `Transform`/`Animation` combinations and the `%` modulo operator in expressions.
- [x] 3.2 Installed and checked `adb logcat` immediately — zero `fail`/`error` matches from the WFF runtime (only unrelated `HWUI`/EGL emulator warnings). `<Animation>` parsed cleanly; no regression to the inline-attribute bug.
- [x] 3.3 Verified both speed and smoothness directly: two screenshots taken ~0.14s apart, both within the *same* clock second, showed the ball at visibly different x/y positions — proof the `<Animation>` interpolation is genuinely running between per-second updates, not just a faster jump-cut. `<Animation>` worked as documented; no fallback needed.
- [x] 3.4 Paddles read clearly as plain bars, fully within the circular boundary with visible margin; divider shows clear dashes.
- [x] 3.5 Captured 6 screenshots spaced 3s apart (~18s span, close to the 20s LCM cycle): ball visibly traced a diagonal bouncing path crossing the divider multiple times, never overlapping a paddle or clipping at the screen edge in any frame.
- [x] 3.6 Ambient mode hides the whole arena (confirmed via `KEYCODE_SLEEP`) and returns cleanly to the faster/smoother active-mode animation on wake (`KEYCODE_WAKEUP`).
- [x] 3.7 Confirmed via `git status`/`git diff` — only `res/` resources and `generate_pixel_assets.py` changed; no `AndroidManifest.xml`/`build.gradle.kts`/`settings.gradle.kts` changes.
- [x] 3.8 Regenerated `res/drawable/preview.png` from a fresh emulator screenshot of the Pong scene; confirmed the watch face picker shows the updated thumbnail.
