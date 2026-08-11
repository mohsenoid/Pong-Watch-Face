## MODIFIED Requirements

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

## ADDED Requirements

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
