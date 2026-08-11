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

### Requirement: Selectable color themes
The watch face SHALL offer 15 selectable color themes through its native configuration UI (with the on-device Edit affordance enabled so the picker is reachable), each defining a two-color top/bottom split background. The theme selected by the user SHALL persist across watch face sessions (standard system configuration behavior) and SHALL apply immediately when changed. The time digits SHALL remain a fixed white color across all themes.

#### Scenario: Selecting a theme changes the background colors
- **WHEN** a user selects a different color theme from the watch face's configuration UI
- **THEN** the top and bottom background colors update to match the selected theme, and the time digits remain white

#### Scenario: Default theme renders correctly
- **WHEN** the watch face is installed and no theme has been explicitly selected yet
- **THEN** it renders using the default theme (theme index 0)

#### Scenario: Arena and date text are unaffected by theme selection
- **WHEN** a user selects any color theme
- **THEN** the Pong arena (paddles, ball, divider) and the date/day-of-week text continue to render in their existing fixed colors, unaffected by the theme selection

#### Scenario: Watch face is editable from the device
- **WHEN** a user long-presses the watch face (or opens it from the favorites carousel) on the watch
- **THEN** an Edit option is available and leads to the color theme picker

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
The watch face SHALL NOT display any name, string, or asset referencing a specific third-party copyrighted or trademarked video game (for example, it SHALL NOT use the string "River Raid" or any equivalent third-party game title anywhere in the watch face name, on-screen text, asset filenames intended as user-facing labels, color-theme configuration option names, or layout configuration option names).

#### Scenario: Watch face name avoids third-party trademarks
- **WHEN** a user views the watch face's name (e.g., in the watch face picker)
- **THEN** the displayed name describes the original arcade theme generically and does not contain a third-party game's trademarked title

#### Scenario: Color theme names avoid third-party trademarks
- **WHEN** a user views the list of selectable color themes in the watch face's configuration UI
- **THEN** each theme's display name describes its color palette generically (e.g., by color or mood) and does not contain any third-party game's trademarked title

#### Scenario: Layout option names avoid third-party trademarks
- **WHEN** a user views the list of selectable layout modes in the watch face's configuration UI
- **THEN** each layout's display name describes it generically (e.g., "Classic", "Scoreboard") and does not contain any third-party game's trademarked title

### Requirement: Selectable layout mode
The watch face SHALL offer two selectable layout modes through its native configuration UI, alongside the existing color theme picker: "Classic" (the original `hh:mm` layout, unchanged from the base arcade theme) and "Scoreboard" (an alternate layout described by the requirements below). The layout selected by the user SHALL persist across sessions and SHALL apply immediately when changed. Classic SHALL remain the default layout.

#### Scenario: Selecting Scoreboard changes the layout
- **WHEN** a user selects the Scoreboard layout from the watch face's configuration UI
- **THEN** the hour/minute display, date display, and arena all switch to the Scoreboard variants described below

#### Scenario: Default layout renders correctly
- **WHEN** the watch face is installed and no layout has been explicitly selected yet
- **THEN** it renders using the Classic layout

#### Scenario: Classic layout is unaffected by the Scoreboard layout's existence
- **WHEN** the Classic layout is selected
- **THEN** the watch face renders identically to its appearance before the Scoreboard layout was introduced (full `hh:mm` display, straight date text, original arena size and position)

### Requirement: Scoreboard hour and minute display
In Scoreboard layout, the watch face SHALL display only the current hour, large and centered near the top of the screen (using the same pixel bitmap font as Classic layout, correctly centered whether the hour is one or two digits). The current minute SHALL be displayed as two separate pixel-font digits (tens and units), styled to resemble a Pong scoreboard, positioned below the hour and reflecting the real current minute value.

#### Scenario: Hour display stays centered for one- and two-digit hours
- **WHEN** the watch face is in Scoreboard layout and the hour changes between a one-digit and a two-digit value
- **THEN** the hour digit(s) remain visually centered as a group, rather than shifting off-center

#### Scenario: Minute digits reflect the real time
- **WHEN** the device's minute value changes while the watch face is in Scoreboard layout
- **THEN** the two scoreboard-style minute digits update to match the new minute value exactly

### Requirement: Curved date text in Scoreboard layout
In Scoreboard layout, the date/day-of-week text SHALL be rendered as curved text following the top of the circular bezel, in place of the straight horizontal date text used in Classic layout.

#### Scenario: Date text curves along the top bezel in Scoreboard layout
- **WHEN** the watch face is in Scoreboard layout
- **THEN** the date/day-of-week text is rendered as curved text near the top edge of the circular face

### Requirement: Larger Pong arena in Scoreboard layout
In Scoreboard layout, the Pong arena (divider, paddles, ball) SHALL render larger than in Classic layout, using the additional vertical space freed by the curved date and compact hour display, while the paddles and ball SHALL remain visibly reachable by each other's motion (not scattered so widely that they rarely appear to interact).

#### Scenario: Arena is larger in Scoreboard layout
- **WHEN** comparing the Classic and Scoreboard layouts
- **THEN** the Scoreboard layout's divider, paddles, and ball are visibly larger than their Classic-layout counterparts

#### Scenario: Paddles remain within the visible circular face
- **WHEN** a paddle moves to any position within its motion range in Scoreboard layout
- **THEN** the paddle remains fully within the circular display area, not clipped by the bezel
