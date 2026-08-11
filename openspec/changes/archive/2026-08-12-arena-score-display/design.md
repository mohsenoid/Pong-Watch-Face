## Context

The canvas has a mostly-empty band between the main clock (`y=148`, height `104`, ending at `y≈252`) and the arena divider/paddles (`y≈322` onward) — roughly `y≈260-310` is free. The paddles sit at `x=95` (left) and `x=345` (right), matching the reference Pong screenshot's layout where each score sits above its corresponding paddle.

The paddles already use `rand(342, 362) + [SECOND] * 0` to get a fresh random value each second, re-rolling only because the expression references `[SECOND]` (confirmed on-device this session: without a referenced data source, an expression isn't guaranteed to re-evaluate on a useful cadence).

## Goals / Non-Goals

**Goals:**
- Two "score" numbers that look like a Pong scoreboard and change periodically, without claiming to track real events. (Superseded in Phase 2 - the digits ended up showing the real minute instead, as part of a full second "Scoreboard" layout mode.)

**Non-Goals:**
- A real incrementing score tied to actual ball-paddle events — not achievable statelessly (see Decisions), and explicitly not attempted here.

## Decisions

**Course correction during implementation:** the first working version used a plain system-font `PartText` (`family="SYNC_TO_DEVICE"`) with `Parameter expression="round(rand(0,9) + [MINUTE] * 0)"`, muted grey, positioned above each paddle. This was built and verified on-device (confirmed a single clean digit renders, stays constant within a minute, and changes at the minute rollover). After seeing it live, feedback was: keep the "7-segment" look `SYNC_TO_DEVICE` happened to render as, but white instead of grey, and moved closer to the middle divider instead of above the paddles — implemented and reverified. A further look then asked for the pixel font (matching the main clock) instead of the system font entirely.

**Final approach: pixel-digit-font `PartImage`-per-value pattern, driven by a deterministic scramble of `[MINUTE]`, not `rand()`.** The main clock digits work by rendering all 10 possible `digit_N.png` `PartImage`s for a position and using `Transform target="alpha" value="([TOKEN]==N)*255"` on each to show only the matching one — this works because `[HOUR_UNITS_DIGIT]` etc. are stable data-source values that all 10 sibling elements read identically. `rand()` does not have this property: it produces a fresh independent draw on every evaluation, so if each of the 10 conditional `PartImage`s independently called `round(rand(0,9))==N`, each would re-roll separately and the visibility checks would desync (showing zero, multiple, or flickering digits rather than exactly one consistent value) — this is why the first version used `PartText` instead. To get the pixel font working correctly, the value source was changed from `rand()` to a deterministic arithmetic scramble of `[MINUTE]` (`([MINUTE] * 7 + 3) % 10` for the left score, `([MINUTE] * 13 + 5) % 10` for the right) - both stable and read identically by all 10 sibling `PartImage`s (same property as `[HOUR_UNITS_DIGIT]`), while still looking arbitrary rather than obviously derived from the visible clock. Verified on-device: at `MINUTE=59`, left evaluates to `6` and right to `2`, matching what rendered.

**Re-roll cadence: once per minute**, via `[MINUTE]` in the scramble formula — verified changing at the minute rollover, not every second.

**Different scramble constants per side** (`*7+3` vs `*13+5`) so the two sides diverge from each other on most minutes, without being independent random draws (which the pixel-font approach can't safely support - see above).

**Color: white, matching the main clock digits** (reusing the existing white `digit_0.png`...`digit_9.png` assets as-is, no `tintColor` needed) - direct feedback after seeing the grey/system-font version live.

**Position: `y=260`, flanking the vertical divider (`x=165` left / `x=255` right, digit width `30`, centered at `x=180`/`x=270` either side of the divider at `x≈225`)** - moved inward from the original above-the-paddles placement after live feedback that it read better closer to the middle line.

## Risks / Trade-offs (original scope)

- [Risk] A once-per-minute re-roll might look arbitrary/disconnected from any visible "event" in the arena, since there is no real hit detection. → Superseded, see Phase 2 below.
- [Risk] The deterministic scramble is not truly random (a keen observer could work out the pattern), unlike the paddles' genuine `rand()`. → Superseded, see Phase 2 below.

## Phase 2: Evolved into a full "Layout" configuration

After the deterministic-scramble version shipped and was reviewed live, the direction changed substantially:

**Decision: show the real minute, not a decorative value.** A fake "score" sitting next to the real `hh:mm` clock read as confusing/pointless once seen live - simplest fix was to show the actual minute value as the scoreboard-styled digits instead of inventing a fake one. This meant reusing the exact same `PartImage`-per-digit-value pattern, just swapping the driving expression from the `[MINUTE]` scramble to the real `[MINUTE_TENS_DIGIT]`/`[MINUTE_UNITS_DIGIT]` tokens (same tokens the Classic layout's minute digits already used).

**Decision: make this a full alternate layout, not a permanent change to the one layout.** Once the minute moved down to double as the "score," the hour no longer needed to share the top row with it - the hour could go large and centered on its own. This is different enough from the original layout that changing it unconditionally would have altered the watch face's default appearance, which the user did not want. Resolved by adding a second `UserConfigurations` entry - a `ListConfiguration` named `layout` with two `ListOption`s (`Classic`, `Scoreboard`) - and gating every affected element (date, hour position, minute/score digits, arena size and position) with `[CONFIGURATION.layout]=="0"` / `=="1"` `Transform`s, duplicating elements where the two layouts needed structurally different content (e.g., straight `PartText` date for Classic vs. `TextCircular` date for Scoreboard - `PartText` can contain one or the other, not both conditionally).

**`TextCircular` geometry (new to this project):** initial attempt set `centerX`/`centerY` to the canvas center with a small `height` (e.g. `70`) expecting a "band" positioned near the top - this instead rendered the text near the canvas's vertical center, overlapping the clock. Correct model: `width`/`height` define a full ellipse's axes around `centerX`/`centerY`, and `startAngle`/`endAngle` carve out the visible arc - setting `height` equal to `width` (both ≈ the desired radius × 2) produces a proper circular arc; a small `height` produces a squashed, low-radius ellipse near the center instead of a ring near the edge. Confirmed on-device before finalizing.

**Two-digit hour centering bug (found and fixed):** the hour's x-position ternary initially centered the *single-digit* case correctly but did not account for the hour-tens digit (`hour_leading_one`) also being visible for hours ≥10 - the combined two-glyph group was centered incorrectly (visibly shifted left) for hours like 10, 11, 12. Fixed by making the hour-units digit's x-position formula shift further right when the two-digit condition is true, so the *pair* centers correctly, not just the units digit alone.

**Arena sizing went through several iterations, converging on prioritizing paddle-ball sync over using the full available space.** The arena was progressively enlarged (in response to "more space now, scale up the game") and repositioned upward (in response to "move hour/minute lower is bad" and related feedback), then the paddle was shrunk to 2/3 height ("more like the original game"). Each size/range change to the paddle or ball risked breaking their vertical overlap, since paddle motion is genuine `rand()` (no relationship to the ball's position - see the reverted `arena-hit-flash` change for why true collision detection isn't achievable declaratively). Empirically (screenshot comparison across multiple seconds), the reliable formula is: **keep the paddle's random range narrow relative to the ball's own vertical swing** - widening either one independently reintroduces frequent visible misses. The final tuning (paddle height 40, random range 30px, ball swing 40px) prioritizes sync reliability; this leaves visible unused vertical space between the paddles/ball and the bottom of the divider/arena band, which was explicitly left unresolved per user direction (see Risks).

## Risks / Trade-offs (current)

- [Risk] The Scoreboard arena's paddles and ball occupy a smaller vertical band than the divider visually implies, leaving unused space near the bottom of the arena. → Explicitly deferred: widening the motion range (tested twice) reintroduces frequent visible paddle/ball misses, which was judged worse than the unused space. Revisit only with a fundamentally different approach (e.g., a taller paddle, or accepting a lower sync-reliability bar) - not a quick tuning fix.
- [Risk] The Scoreboard minute digits are real data (not decorative), so - unlike the original scramble-based design - there's no remaining "fake stat" concern, but the digits do duplicate information already visible if a user mentally reads "large hour + scoreboard minute" as two separate facts rather than one time. → Accepted: this was the explicit, live-reviewed design direction.

## Migration Plan

Additive visual + configuration change (new `ListConfiguration`), no persisted data beyond the system's own configuration-selection storage (same mechanism already used for the color theme). Classic layout (the default) is unaffected. Rollback is a revert of the `ListConfiguration` and all `[CONFIGURATION.layout]`-gated elements in `watchface.xml`.
