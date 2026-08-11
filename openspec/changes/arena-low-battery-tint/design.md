## Context

The ball and paddles are plain `PartImage`s with white/yellow fill baked into their generated PNGs (`arena_ball.png`, `arena_paddle_left.png`, `arena_paddle_right.png`), currently with no `tintColor` at all. This project has confirmed `tintColor` works on `PartImage` (used extensively for the color-theme background). The standalone `[BATTERY_PERCENT]` data source (confirmed available via the WFF arithmetic-expression reference, alongside `[BATTERY_IS_LOW]` and `[BATTERY_CHARGING_STATUS]`) has not been used in this project before.

## Goals / Non-Goals

**Goals:**
- A clear, glanceable low-battery cue on the arena elements using only standalone battery data sources (not the complication from the separate `watch-complications` change, so this works regardless of what's assigned to any complication slot).

**Non-Goals:**
- Any complication-based battery display (that's `watch-complications`).
- A numeric battery readout — this is a color cue only.

## Decisions

**Use `[BATTERY_PERCENT] < 20` via a ternary expression on `Transform target="tintColor"`, not `[BATTERY_IS_LOW]`.** `BATTERY_PERCENT < 20` gives an explicit, tunable threshold matching common "low battery" conventions (20% is Android's own default low-battery warning threshold), whereas `BATTERY_IS_LOW`'s exact system-defined threshold is undocumented in what was found this session — using the numeric comparison keeps the behavior predictable and adjustable.

**Warning color: reuse the existing `#FF2222`-family red already used for the "Crimson Sky" theme's accent, applied via `tintColor="[BATTERY_PERCENT] < 20 ? #FF2222 : #FFFFFF]"`-style ternary (exact syntax to confirm on-device) rather than a new color.** Keeps the palette internally consistent; the ball/paddles' normal color (white/yellow) is preserved as the non-warning branch.

## Risks / Trade-offs

- [Risk] Whether `tintColor` accepts a full ternary expression (as opposed to only a flat `[CONFIGURATION...]` reference, which is the only pattern proven so far in this project) is unverified. → Mitigation: test on a single element (the ball) in isolation before wiring up both paddles.
- [Risk] Testing low-battery visually on a real device requires an actually-low battery, or a temporarily-hardcoded threshold. → Mitigation: verify with a temporarily-loosened threshold (e.g. `< 100`) to force the warning state on-screen, then revert to the real `< 20` threshold before finishing.

## Migration Plan

Pure additive visual change, no persisted data. Rollback is a plain revert of the added `Transform target="tintColor"` elements.
