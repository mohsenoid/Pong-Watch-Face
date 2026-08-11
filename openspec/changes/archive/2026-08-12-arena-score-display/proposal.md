## Why

Real Pong games display a scoreboard above the paddles (large muted-grey digits), which is a much more authentic, recognizable Pong element than the paddle-flash effect it replaces (see `arena-hit-flash`, reverted after comparing against real Pong footage).

**This change evolved substantially beyond its original scope during implementation.** What started as a small decorative-score addition to the existing layout became a full second layout mode ("Scoreboard"), selectable alongside the existing color theme, once it became clear that a fake/decorative score sat awkwardly next to the real clock. The final shipped feature is documented below; see design.md and tasks.md for the iteration history.

## What Changes

- Add a new "Layout" configuration (a `ListConfiguration`, alongside the existing color theme `ColorConfiguration`) with two options: **Classic** (the original layout, unchanged - default) and **Scoreboard** (described below).
- **Scoreboard layout**: the hour is shown large and centered at the top (correctly centered for both one- and two-digit hours); the current minute is shown as two real pixel-font digits styled like a Pong scoreboard, positioned near the arena; the date is rendered as curved text along the top bezel instead of straight text; the Pong arena (divider, paddles, ball) renders larger than in Classic layout.
- The original idea of a decorative, non-real "score" (via `rand()` or a deterministic scramble of `[MINUTE]`) was abandoned in favor of showing the **real current minute** as the scoreboard digits - simpler, and avoids the "fake stat next to a real clock" awkwardness.
- Classic layout is fully unaffected - it renders identically to the watch face's appearance before this change.
- Along the way, a real paddle/ball vertical-sync issue was discovered and fixed: shrinking the paddle or widening its random motion range independently of the ball's own motion range made the paddle "miss" the ball much more often. The final tuning favors reliable sync over using the full available arena space - see design.md's Risks section for the trade-off that remains unresolved.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `watchface/arcade-theme`: extends the no-trademark requirement to layout option names, and adds the Scoreboard layout mode with its hour/minute display, curved date, and larger arena.

## Impact

- Affected files: `watchface/src/main/res/raw/watchface.xml` (new `ListConfiguration`; dual Classic/Scoreboard element sets for the date, hour position, and arena, each gated by `[CONFIGURATION.layout]`; minute digits driven by real `[MINUTE_TENS_DIGIT]`/`[MINUTE_UNITS_DIGIT]` tokens), `watchface/scripts/generate_pixel_assets.py` (paddle/ball/divider dimensions retuned several times), `watchface/src/main/res/values/strings.xml` (layout option labels).
- No build, dependency, or `hasCode` changes.
- First use of `TextCircular` and `ListConfiguration` in this project - both verified on-device.
