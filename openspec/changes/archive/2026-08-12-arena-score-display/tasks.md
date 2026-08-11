## 1. Verify rand()-driven PartText renders and re-rolls correctly

- [x] 1.1 Add one `PartText` (left score) using `Localization`/`Text`/`Font family="SYNC_TO_DEVICE"`/`Template`/`Parameter expression="round(rand(0,9) + [MINUTE] * 0)"`, grey color, in a rough placeholder position. **Outcome:** `Localization` turned out unnecessary (only needed for calendar-based tokens, not for arithmetic-only expressions) - omitted.
- [x] 1.2 Build, install, check `adb logcat` for parse/evaluation failures. **Outcome:** clean build, no errors.
- [x] 1.3 Screenshot to confirm a single digit 0-9 renders (not a float, not blank, not multiple digits). **Outcome:** confirmed - rendered "8" cleanly.
- [x] 1.4 Wait for (or force, if practical) a minute rollover and confirm the digit re-rolls to a new (possibly different) value, rather than changing every second or never changing. **Outcome:** confirmed - stayed "8" across 3 checks within the same minute (08:47:xx), then changed to "7" exactly at the 08:47→08:48 rollover.

## 2. Add the second score and finalize position

- [x] 2.1 Add the right score `PartText`, mirroring the left one with its own independent `rand(0,9) + [MINUTE] * 0` expression.
- [x] 2.2 Position both above their respective paddles (`x≈70-120` left, `x≈320-370` right, `y≈270`), verifying against the circle boundary so neither clips the bezel or collides with the main clock digits or the arena divider/paddles. **Outcome:** final positions `x=55` (left) / `x=315` (right), both `y=260`, `width=80`, `height=40` — exactly mirrored (`450 - 55 - 80 = 315`), well within the circle boundary at that y, no collisions.
- [x] 2.3 Build, install, check logcat, screenshot both scores rendering together. **Outcome:** clean build, no errors, both scores rendered independently ("8" and "6" in one screenshot), confirming separate `rand()` draws.

## 3. Live feedback pivot (post-implementation)

- [x] 3.1 Real-device feedback: `SYNC_TO_DEVICE` rendered the score as a 7-segment digital-clock style font; kept that look but changed color from grey (`#ff888888`) to white (`#ffffffff`) to match the main clock, per feedback. Verified on-device.
- [x] 3.2 Further feedback: move the scores closer to the middle divider instead of above the paddles. Repositioned from `x=55`/`x=315` to `x=140`/`x=230` (`PartText` era). Verified on-device.
- [x] 3.3 Further feedback: replace the system font entirely with the same pixel digit font used by the main clock. Rebuilt as 20 conditional `PartImage`s (10 per side, reusing `digit_0.png`...`digit_9.png`), replacing the two `PartText` elements. Since `rand()` can't safely drive 10 independently-evaluated conditional blocks (each would re-roll separately - see design.md), switched the value source to a deterministic scramble of `[MINUTE]` (`([MINUTE]*7+3)%10` left, `([MINUTE]*13+5)%10` right) instead of `rand()`. Final position: `x=165`/`x=255`, `width=30`, `height=40`, `y=260`. Verified on-device: math cross-checked against rendered digits at `MINUTE=59` (6, 2) and `MINUTE=0` (3, 5) - both matched exactly.

## 4. Final verification

- [x] 4.1 Confirm ball motion, paddle motion, and all other arena/theme behavior are unaffected. **Outcome:** confirmed via screenshots throughout - divider, paddles, and ball all render and animate normally.
- [x] 4.2 Confirm all 15 color themes and ambient mode are unaffected. **Outcome:** spot-checked theme index 1 (Night Vision) and ambient mode - both render the scores correctly (ambient dims them along with everything else via the existing scene-wide `Variant`).
- [x] 4.3 Confirm no build/dependency changes were introduced — module stays `hasCode = false`. **Outcome:** confirmed - only `watchface/src/main/res/raw/watchface.xml` changed.
- [x] 4.4 Regenerate `res/drawable/preview.png` reflecting the new score display. **Outcome:** done, reflects the final pixel-font white scores.
- [x] 4.5 Update this file's checkboxes with outcomes.

## 5. Phase 2: evolved into a "Layout" configuration (post-completion, direct-chat iteration)

This work happened after task group 4 closed the original scope, in response to further live feedback. Summarized here rather than itemized per-task; see design.md's "Phase 2" section for the full technical narrative.

- [x] 5.1 Reference footage of real Pong showed genuine incrementing scoreboards; the reverted `arena-hit-flash` change's paddle-flash effect was replaced with this scoreboard concept (already the premise of this whole change).
- [x] 5.2 Pivoted the scoreboard digits from a decorative `[MINUTE]`-scramble value to the **real** `[MINUTE_TENS_DIGIT]`/`[MINUTE_UNITS_DIGIT]` tokens, once it was clear a fake stat next to the real clock read as confusing live.
- [x] 5.3 Added a new `ListConfiguration` (`layout`: Classic / Scoreboard) so this alternate look is opt-in, not a change to the default watch face appearance. Verified Classic renders identically to its pre-this-change appearance after every subsequent edit.
- [x] 5.4 Built the Scoreboard layout: hour large and centered at top (fixed a two-digit-hour centering bug along the way), minute digits as the real-data scoreboard, curved date (`TextCircular`, first use in this project - required correcting a geometry misunderstanding), larger Pong arena.
- [x] 5.5 Iterated the arena size/position several times in response to feedback ("more space", "move up", "move to middle", "shrink paddles"), discovering and fixing a real paddle-ball vertical-sync bug along the way (paddle's random range must stay narrow relative to the ball's own vertical swing, or they visibly stop overlapping). Final tuning prioritizes sync reliability over using the full available arena space - left as an explicitly acknowledged, deferred trade-off.
- [x] 5.6 Verified on-device throughout: no logcat errors at any step, Classic layout re-confirmed unaffected after each Scoreboard-only change, ambient mode confirmed working in both layouts.
- [x] 5.7 Updated proposal.md, design.md, and this change's delta spec to describe the final shipped behavior (Layout configuration, Scoreboard mode) rather than the original decorative-score design, before archiving.
