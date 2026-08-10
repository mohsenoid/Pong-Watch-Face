## 1. Rotation investigation (superseded, kept for record)

- [x] 1.1 Generate a throwaway two-tone test image and wire it into `watchface.xml` with `<Transform target="rotationDegrees" value="[MINUTE]*6">`, positioned so its center coincides with canvas center.
- [x] 1.2 Build, install, and check logcat — no parse failures.
- [x] 1.3 Screenshot at different `[MINUTE]` values and measure the dividing line's pixel position precisely — found it stayed perfectly vertical (unchanging) regardless of minute, contradicting the expected rotation. Confirmed with a follow-up isolated test using a hardcoded `value="90"` instead of an expression: still no rotation. **Conclusion: `Transform target="rotationDegrees"` does not apply to a generic `PartImage` on this runtime.** Direction changed away from rotation entirely (see design.md's Context) before pursuing an `AnalogClock`/`MinuteHand`-based workaround — no further action needed on this front.

## 2. Static split background assets

- [x] 2.1 In `watchface/scripts/generate_pixel_assets.py`, added `generate_split_background()` producing `bg_split.png` (450x450, split at `y=205`). Color later revised from dark charcoal to purple `(90,60,200)` per user preference (task 3's masking abandonment made this a plain color swap, no other impact).
- [x] 2.2 Added `generate_split_masks()` producing `mask_dark_half.png`/`mask_orange_half.png` — later removed in task group 3 once masking was abandoned (dead code with nothing referencing it).
- [x] 2.3 Changed `generate_scanline_background()` to produce a semi-transparent overlay (alpha 20/55 alternating instead of opaque).
- [x] 2.4 Wired `bg_split` and the scanline overlay into `watchface.xml` in place of the old opaque scanline background.
- [x] 2.5 Built, installed, checked logcat (clean), and screenshotted: static split renders correctly, digit row straddles the divide, scanline overlay visible without hiding colors, arena still reads clearly against both halves.

## 3. Verify mask rendering (before duplicating all the digits)

- [x] 3.1 Built an isolated test: a full-canvas orange `PartImage` paired with a `renderMode="MASK"` sibling (`mask_dark_half.png`) in a `Group`. First attempt (mask-then-source order, default group render mode) did nothing — orange covered the whole circle, ignoring the mask entirely.
- [x] 3.2 Tried source-then-mask order with `renderMode="ALL"` on the parent `Group`: this genuinely clipped the orange fill to just the top half — proof masking *can* work — but it also blacked out every other element in the scene (digits, arena, everything), including breaking the circular clip shape (square corners appeared). Shrinking the `Group`'s own bounding box to a digit-sized area contained the visible "orange" patch to that box, but the "black out everything else in the entire scene" side effect persisted regardless of the group's size or position, and the mask boundary wasn't even visibly respected within that small view.
- [x] 3.3 **Conclusion: masking is not safe to build on with the tested approaches** — it either does nothing or destructively blanks the rest of the scene. Invoked design.md's fallback tier 2: dropped the per-digit color-swap effect entirely, switched to a single fixed digit color (white) with good contrast against both background halves. Removed the now-unused `generate_split_masks()` function and its two mask PNGs. Updated proposal.md/design.md/spec accordingly (see below).

## 4. Color-swapping digits — DROPPED

- [x] 4.1-4.3 Superseded by task 3.3's fallback decision. Digits use a single fixed white color (`DIGIT_COLOR` in `generate_pixel_assets.py`) instead of two masked color copies. Spec's "Color-swapping time digits" requirement removed from this change's scope (see updated delta spec — the "Arcade time display" and new background requirements no longer reference per-digit color swapping).

## 5. Date/day text

- [x] 5.1 First attempt (bracket tokens embedded directly in `<Template>` text, e.g. `[DAY_OF_WEEK_S], [MONTH_S] [DAY]`) failed silently — rendered as literal text, no logcat error. Found the real, confirmed-working pattern by searching `android/wear-os-samples` directly (`WatchFaceFormat/Weather/watchface.xml`): data-source tokens go in `<Parameter expression="[TOKEN]"/>` elements referenced via `%s` placeholders inside `<Template><![CDATA[...]]></Template>`, alongside a `<Localization calendar="GREGORIAN" timeZone="SYNC_TO_DEVICE"/>` sibling. Also found the real day-of-month token is `[DAY_Z]`, not `[DAY]`. Rebuilt with `[DAY_OF_WEEK_S]`, `[MONTH_S]`, `[DAY_Z]` in that pattern — confirmed via logcat (clean) and screenshot: renders as "Mon, Aug 10" correctly.
- [x] 5.2 Positioned at `x=45, y=70, width=360, height=40`; visible circle x-range at that y-position comfortably exceeds the text's bounds (verified both by the circle-equation margin check and the rendered screenshot showing no clipping).
- [x] 5.3 Format reads cleanly as-is ("Mon, Aug 10") — no further adjustment needed.

## 6. Arena contrast and full verification

- [x] 6.1 Visually verified the Pong arena (white paddles/divider, yellow ball) reads clearly against both the purple and orange background halves, across many screenshots throughout this change.
- [x] 6.2 **Ambient-mode design changed mid-implementation** per user request: instead of hiding the arena/date text and swapping to a plain thin font (the original plan, and every prior change's pattern), everything now stays visible in ambient mode — all the `Variant mode="AMBIENT" target="alpha" value="0"` elements were removed, and the redundant ambient-only thin `TimeText` was deleted. This relies on Wear OS's "display offload" ambient rendering (confirmed in `adb logcat`: `enter ambient, set display offloading`) to freeze the Pong ball/paddles at whatever position they were in when ambient engaged, giving a natural "paused game" effect without any explicit pause logic. Verified via multiple sleep/wake cycles - initially saw the emulator flap between active/ambient states rapidly (an `onDisplayOffloadStateFailure` loop, an emulator quirk unrelated to the XML), but it settles into a stable, correctly-dimmed ambient frame within ~8 seconds, and returns cleanly to full active rendering on wake every time.
- [x] 6.3 Confirmed via `git status`/`git diff` — only `res/` resources and the generator script changed; no `AndroidManifest.xml`/`build.gradle.kts`/`settings.gradle.kts` changes.
- [x] 6.4 Regenerated `res/drawable/preview.png` from a fresh emulator screenshot multiple times as the design evolved; final version reflects the fully-settled state.

## 7. Post-verification refinements (user feedback during this session)

- [x] 7.1 Switched `SPLIT_TOP_COLOR` back from dark charcoal to purple `(90,60,200)` per user preference (a plain color-constant change, no other impact).
- [x] 7.2 Pong center divider: tried doubling thickness first (width 6->12) - user clarified they meant *height*, not thickness. Reverted to width=6, doubled height instead (`ARENA_BAND_HEIGHT * 2` = 96), recentered vertically (`y=322`).
- [x] 7.3 Extended the ball's horizontal bounce range (was `x=140..300`, stopping ~30px short of each paddle) to `x=105..329`, so it now visibly touches each paddle's near edge at the extremes of its cycle - confirmed via multi-frame screenshots showing direct overlap with both paddles.
- [x] 7.4 Added a short, thin horizontal `section_separator` image between the time display and the arena, per user request. Iterated on size twice based on feedback (160x3 called "too thick"; 280x1 after a second round) before the user decided the whole idea "was wrong" and asked for it to be removed entirely - reverted: removed the `PartImage` from `watchface.xml`, the `generate_section_separator()` function and its call in `main()`, and the generated PNG. Net no change from the pre-task-7.4 baseline.
- [x] 7.5 Sped up the ball/paddle bounce periods (X: 4s->2s, Y: 5s->3s) for "more action" per user request, then **reverted to the original 4s/5s periods** per a follow-up request - net no change to speed from the pong-arena-scene baseline.
- [x] 7.6 Made the two paddles move independently: they previously shared the exact same Y-position formula (mirroring the ball 1:1, moving in perfect lockstep). Gave each its own distinct period (left: 4s, right: 6s, both different from the ball's own 5s Y-period) so they're no longer synchronized - confirmed via precise pixel measurement showing the two paddles' Y positions diverging (and even moving in opposite directions) across sampled frames.
