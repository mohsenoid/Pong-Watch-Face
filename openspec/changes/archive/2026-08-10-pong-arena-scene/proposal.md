## Why

Seeing the divider-plus-bouncing-ball arena in action reminded the user of Pong more than Refraction specifically, and surfaced a real usability problem: the ball's position is driven directly by `[SECOND]` (an integer that only changes once a second) over a full 60-second cycle, so it reads as a slow, single-step-per-second jump rather than a lively bouncing ball. Leaning fully into the Pong idea — paddles instead of angular ship sprites, a faster cycle, and actually smooth motion — fixes both the aesthetic mismatch and the pacing complaint in one pass.

## What Changes

- Remove the two wedge/triangle "ship" sprites (`arena_ship_left.png`, `arena_ship_right.png`) and replace them with two simple paddle bars (plain vertical rectangles), the recognizable Pong look, near the left/right edges of the arena band.
- Restyle the existing central divider from a solid bar into a short-dashed vertical line — Pong's classic center court line — instead of introducing a new asset concept.
- Speed up the ball's bounce cycle substantially: instead of a `[SECOND]`-only formula that takes 60 seconds for a full back-and-forth, use `[SECOND] % <short period>` so the ball completes many bounces per minute.
- Smooth the motion using a WFF `<Animation>` child element inside the ball's `<Transform>` (interpolating between the per-second value updates), instead of the current abrupt per-second jump. This hasn't been used anywhere in the project yet, so it needs on-device verification during implementation, with a documented fallback (a shorter period alone, without interpolation) if `<Animation>` doesn't behave as the docs describe.
- Add a light vertical bounce component to the ball (a second, faster-period `[SECOND] % <period>` triangle wave on `target="y"`) so it moves diagonally within the band rather than sliding along a single horizontal line — closer to how a real Pong ball moves.
- Rename the "missile"/arena-track naming to Pong-appropriate names (`arena_ball`, `arena_paddle_left`/`arena_paddle_right`) for clarity going forward.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `watchface/arcade-theme`: the "Refraction-style bouncing arena" requirement is replaced with a Pong-style arena requirement (paddles instead of ships, faster/smoother/diagonal ball motion); the "Scanline background" and "Ambient mode simplification" requirements need no further wording changes (they already reference "the arena group" generically, from the prior change).

## Impact

- Affected files: `watchface/src/main/res/raw/watchface.xml` (arena `Group` contents), `watchface/scripts/generate_pixel_assets.py` (replace ship generation with paddle generation, restyle divider as dashed, rename ball asset), `watchface/src/main/res/drawable/` (remove ship PNGs, add paddle PNGs, regenerate divider/ball).
- No build, manifest, or dependency changes — module stays `hasCode = false`.
- No changes to previously-verified behavior: time display, hour-tens digit, ambient-mode time text, branding, scanline background.
