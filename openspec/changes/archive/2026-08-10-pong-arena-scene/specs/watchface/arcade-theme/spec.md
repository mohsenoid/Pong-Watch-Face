## REMOVED Requirements

### Requirement: Refraction-style bouncing arena
**Reason**: Replaced by a faster, smoother Pong-style arena (see proposal.md) — the ship sprites read more like Pong than the game that originally inspired them, and the ball's `[SECOND]`-only motion was too slow and too choppy (one visible jump per second, one full cycle per minute).
**Migration**: Visual-only watch face element; no data or API migration needed.

## ADDED Requirements

### Requirement: Pong-style bouncing arena
The watch face SHALL render, in the decorative band below the time display, a dashed vertical divider at horizontal center, two simple paddle bars near the left and right edges, and one small ball that moves back and forth across the band (with a lighter secondary vertical bounce, so its path is diagonal rather than a single horizontal line) at a pace that completes multiple full back-and-forth traversals per minute, with its on-screen motion appearing smooth rather than jumping once per second.

#### Scenario: Ball completes multiple bounces per minute
- **WHEN** the watch face is in active mode over the span of one minute
- **THEN** the ball completes more than one full back-and-forth traversal of the band (i.e., its horizontal bounce period is a fraction of 60 seconds, not the full 60 seconds)

#### Scenario: Ball motion appears smooth
- **WHEN** the current seconds value changes while the watch face is in active mode
- **THEN** the ball's on-screen position transitions smoothly toward its new target position rather than jumping there instantaneously

#### Scenario: Paddles and ball are original, unbranded art
- **WHEN** the divider, paddle, and ball assets are produced for this watch face
- **THEN** they SHALL be original pixel art generated for this project, and SHALL NOT reproduce the specific sprite art, level art, logo, or name of any existing copyrighted or trademarked video game
