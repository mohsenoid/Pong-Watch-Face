## Context

The current arena `Group` in `watchface/src/main/res/raw/watchface.xml` has a divider `PartImage`, two ship `PartImage`s, and a ball (`arena_missile`) `PartImage` with a `<Transform target="x" value="...">` child using `140 + (clamp([SECOND],0,30) - clamp([SECOND]-30,0,30)) / 30 * 160` — a triangle wave over the full 0-59 second range, so one full back-and-forth traversal takes 60 seconds. See proposal.md for why that reads as slow and choppy, and why the ship sprites are being dropped in favor of paddles.

WFF's expressions documentation (per the earlier `transform` training page fetch) shows `<Transform>` supporting a nested `<Animation duration="..." interpolation="...">` child to interpolate the rendered value between updates, rather than jump-cutting. This project hasn't used `<Animation>` yet — everything so far has been either a static value or a raw `Transform` expression without interpolation — so its exact on-device behavior needs verification, same as `Transform` itself did in the first change.

## Goals / Non-Goals

**Goals:**
- Ball completes noticeably more than one bounce per minute (target: a handful of seconds per traversal, not 60).
- Ball motion reads as continuous/smooth rather than a per-second jump.
- Paddles read as plain Pong paddles, not angular ships.
- Reuse the already-proven `clamp()`-based triangle-wave-in-a-`Transform` technique for the core motion; only the interpolation piece (`<Animation>`) is genuinely new.

**Non-Goals:**
- No collision detection or paddle-tracks-ball "AI" — paddles stay static bars, matching the existing fixed-position approach (this is a decorative animation, not a playable game).
- No sound/haptics on "hits".
- No change to the time display, hour-tens logic, ambient time text, scanline background, or branding.

## Decisions

**Shorten the bounce period via `[SECOND] % <period>` instead of raw `[SECOND]`.** Using modulo keeps the same proven `clamp()`-triangle-wave shape but compresses it into a period of a few seconds instead of 60. Picked a 4-second full cycle (2 seconds each direction) for the horizontal motion — fast enough to clearly read as "faster," not so fast it becomes a distracting flicker on a watch face that should stay glanceable. `value="140 + (clamp([SECOND] % 4, 0, 2) - clamp(([SECOND] % 4) - 2, 0, 2)) / 2 * 160"`.

**Add a lighter, out-of-phase vertical bounce for a diagonal path.** A second `<Transform target="y" value="...">` on the same ball `PartImage`, using a 5-second period (deliberately different from the horizontal 4-second period) over a small ~20px vertical range. Because 4 and 5 share no common factor smaller than their product, the combined horizontal+vertical pattern only fully repeats every 20 seconds (their LCM) instead of immediately, so the motion feels more like an actual bouncing ball than a metronome. This is a nice-to-have layered onto the already-working `Transform` mechanism, not a new risk in itself.

**Try `<Animation>` for smoothing; fall back to period-only if it doesn't behave as documented.** `<Transform>`'s value is re-evaluated once per second (driven by `[SECOND]`); without interpolation, the ball still jumps once/sec even at a 4-second period — better than 60s, but still a jump. Nesting `<Animation duration="1" interpolation="LINEAR">` inside each `Transform` should smoothly animate the rendered position across each 1-second interval toward the new target, reconstructing continuous motion from the piecewise-linear triangle wave (LINEAR chosen over an eased curve because the underlying function is already piecewise-linear — easing would visibly deviate from the intended straight-line bounce path). This hasn't been exercised anywhere in the project, so: verify via a build + logcat check (same discipline as the `Transform` bug from the first change) and a couple of screenshots close together in time. If `<Animation>` doesn't parse or doesn't visibly smooth the motion, fall back to the shortened period alone — still a large improvement over the current 60-second cycle even without interpolation.

**Paddles are plain rectangles, not tapered shapes.** A flat vertical bar (e.g. 10 wide x 40 tall) is the unambiguous, recognizable "Pong paddle" silhouette, and is simpler to generate correctly than the triangle math that needed a bugfix in the prior change (no risk of getting the orientation backwards, since a rectangle has no orientation).

**Divider becomes dashed instead of solid.** A short-dash vertical line (alternating filled/empty segments down the column) is Pong's actual center-court convention and is a purely cosmetic asset change — same generation approach as the existing solid divider, just with gaps.

**Keep paddle and ball colors from the prior change; keep the same safe horizontal zone.** The circular-clip-safe zone established last time (paddles/ball comfortably within roughly x=77 to x=373 at the band's most restrictive row) still applies — reuse it rather than re-deriving from scratch, changing only shapes and timing.

## Risks / Trade-offs

- [Risk] `<Animation>` may not work as the fetched docs describe (untested in this project, and this project's docs fetches have repeatedly needed on-device correction). → Mitigation: verify immediately via `adb logcat` (parse errors) and screenshots taken a fraction of a second apart; fall back to period-only (no `<Animation>`) if it doesn't visibly help — still ships the "faster" half of the fix even if "smoother" needs a different approach later.
- [Risk] A 4-second cycle might read as too fast/distracting once seen continuously on a real wrist, or too slow once the novelty wears off — pacing is subjective. → Mitigation: the period is a single easily-tunable number (`% 4`) in one `value` expression; treat the exact figure as adjustable during verification, not a hard requirement.
- [Risk] The added vertical bounce could make the ball clip a paddle or the divider at some phase combinations. → Mitigation: keep the vertical range small (~20px) and centered within the existing safe vertical band; visually verify across at least one full 20-second LCM cycle, not just a couple of screenshots, before calling it done.

## Migration Plan

Pure visual/resource change to the same decorative `Group` — no data, no persisted state, no build/manifest changes. Rollout: implement, verify on the Wear OS emulator (logcat clean, ball visibly faster and smoother across multiple screenshots, ambient mode still hides it and returns cleanly on wake), done. Rollback is a plain revert of the `watchface.xml` `Group` and the drawable files.
