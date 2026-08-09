## REMOVED Requirements

### Requirement: Drifting original sprite
**Reason**: Replaced by a Refraction-inspired bouncing arena scene (see proposal.md) — a static river-shooter decoration didn't read as distinctive or connected to a specific retro-game moment.
**Migration**: Visual-only watch face element; no data or API migration needed.

## ADDED Requirements

### Requirement: Refraction-style bouncing arena
The watch face SHALL render, in the decorative band below the time display, a vertical divider at horizontal center, two small originally-designed geometric ship sprites near the left and right edges (not traced from any specific published game's sprite art), and one small bouncing element whose horizontal position is derived from the current time's seconds value so it moves back and forth across the full band width, crossing the central divider each pass.

#### Scenario: Bouncing element position changes over time
- **WHEN** the current seconds value changes while the watch face is in active mode
- **THEN** the bouncing element's horizontal position on screen changes accordingly, moving back and forth between the left and right edges of the arena band and crossing the central divider on each pass

#### Scenario: Arena assets are original, unbranded art
- **WHEN** the divider, ship, and bouncing-element assets are produced for this watch face
- **THEN** they SHALL be original pixel art generated for this project, and SHALL NOT reproduce the specific sprite art, level art, logo, or name of any existing copyrighted or trademarked video game (including the homebrew game that inspired the mechanic)

## MODIFIED Requirements

### Requirement: Scanline background
The watch face SHALL render a black background with a faint horizontal scanline texture behind all other elements in active mode, evoking a CRT arcade-cabinet look.

#### Scenario: Background is visible behind the time display
- **WHEN** the watch face is in active mode
- **THEN** the scanline background is visible in areas not covered by the time text or the arena group

### Requirement: Ambient mode simplification
When the watch face transitions to ambient (always-on) mode, the arena group SHALL be hidden (rendered at zero opacity) and the time text SHALL switch to a simplified, thin/outline rendering, consistent with Wear OS ambient-mode power and burn-in guidance.

#### Scenario: Entering ambient mode hides the sprite and river
- **WHEN** the watch face transitions from active to ambient mode
- **THEN** the arena group's opacity becomes 0 (not rendered)

#### Scenario: Entering ambient mode simplifies the time text
- **WHEN** the watch face transitions from active to ambient mode
- **THEN** the time text is rendered using the simplified/thin ambient style instead of the full-color bitmap font
