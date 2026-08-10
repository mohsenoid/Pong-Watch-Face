## Purpose

Defines the observable visual behavior of the watch face's retro-arcade theme: what is shown in active mode, what changes in ambient mode, and the constraints that keep the theme original rather than a copy of any specific copyrighted game.

## Requirements

### Requirement: Arcade time display
The watch face SHALL display the current time in `hh:mm` format in active (interactive) mode, rendered using a custom blocky pixel-art bitmap font (digits 0-9 and a colon glyph) in a single fixed color chosen for contrast against both halves of the two-color split background, centered over the watch face background.

#### Scenario: Time updates every minute
- **WHEN** the device time changes to a new minute while the watch face is in active mode
- **THEN** the displayed `hh:mm` text updates to match, using the pixel bitmap font glyphs

#### Scenario: Digits render in the arcade bitmap font
- **WHEN** the watch face is in active mode
- **THEN** every digit and the colon separator are rendered using the custom bitmap font glyphs, not the system default font

### Requirement: Static two-color split background
The watch face SHALL fill the entire background with two solid colors divided by a straight horizontal line, positioned so the time digit row visibly straddles the divide.

#### Scenario: Background fully covers the screen with two fixed colors
- **WHEN** the watch face is in active mode
- **THEN** the region above the dividing line is rendered in one solid color and the region below in the other, together fully covering the circular watch face with no gaps

### Requirement: Scanline background
The watch face SHALL render a faint horizontal scanline texture as a semi-transparent overlay on top of the two-color split background in active mode, evoking a CRT arcade-cabinet look without hiding the background colors.

#### Scenario: Background is visible behind the time display
- **WHEN** the watch face is in active mode
- **THEN** the two-color split background and its scanline overlay are visible in areas not covered by the time text or the arena group

### Requirement: Day-of-week and date display
The watch face SHALL display the current day of the week and date near the top of the screen, in the region above the split background's dividing line, in active mode.

#### Scenario: Date text updates when the day changes
- **WHEN** the device date changes to a new day
- **THEN** the displayed day-of-week and date text updates to match

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

### Requirement: Ambient mode content visibility
When the watch face transitions to ambient (always-on) mode, all content (background, time text, date text, and the arena group) SHALL remain visible and unchanged, relying on the system's own ambient dimming and the Wear OS "display offload" static-snapshot rendering to reduce power draw and naturally freeze any in-progress motion (such as the arena ball/paddles) at whatever state it was in when ambient mode was entered.

#### Scenario: Entering ambient mode keeps all content visible
- **WHEN** the watch face transitions from active to ambient mode
- **THEN** the background, time text, date text, and arena group all remain visible (no opacity changes applied by the watch face itself)

#### Scenario: Arena motion freezes in ambient mode
- **WHEN** the watch face transitions from active to ambient mode while the arena ball is in motion
- **THEN** the ball and paddles appear static for the duration of ambient mode, rather than continuing to animate

### Requirement: No third-party trademark or branding
The watch face SHALL NOT display any name, string, or asset referencing a specific third-party copyrighted or trademarked video game (for example, it SHALL NOT use the string "River Raid" or any equivalent third-party game title anywhere in the watch face name, on-screen text, or asset filenames intended as user-facing labels).

#### Scenario: Watch face name avoids third-party trademarks
- **WHEN** a user views the watch face's name (e.g., in the watch face picker)
- **THEN** the displayed name describes the original arcade theme generically and does not contain a third-party game's trademarked title
