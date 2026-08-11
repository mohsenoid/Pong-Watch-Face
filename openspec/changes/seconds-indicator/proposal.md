## Why

The watch face currently displays no seconds anywhere, which some users expect to glance at.

## What Changes

- Add a small, unobtrusive seconds readout that updates every second, positioned so it doesn't compete visually with the primary `hh:mm` time display.
- Rendered with the existing system-font text pattern (already used for the date), not a new pixel-glyph set — keeps the change small and avoids roughly doubling the digit-element count.
- No changes to the color-theme system, digit font, date display, or Pong arena.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
(none — purely additive requirement)

## Impact

- Affected files: `watchface/src/main/res/raw/watchface.xml` (add one `PartText` using `[SECOND_Z]`).
- No build, dependency, or `hasCode` changes.
- Low risk — reuses an already-proven pattern (the date text) with a data source (`[SECOND_Z]`) from the same family already used elsewhere (`[SECOND]` drives the ball/paddle motion).
