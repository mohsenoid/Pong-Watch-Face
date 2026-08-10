## MODIFIED Requirements

### Requirement: No third-party trademark or branding
The watch face SHALL NOT display any name, string, or asset referencing a specific third-party copyrighted or trademarked video game (for example, it SHALL NOT use the string "River Raid" or any equivalent third-party game title anywhere in the watch face name, on-screen text, asset filenames intended as user-facing labels, or color-theme configuration option names).

#### Scenario: Watch face name avoids third-party trademarks
- **WHEN** a user views the watch face's name (e.g., in the watch face picker)
- **THEN** the displayed name describes the original arcade theme generically and does not contain a third-party game's trademarked title

#### Scenario: Color theme names avoid third-party trademarks
- **WHEN** a user views the list of selectable color themes in the watch face's configuration UI
- **THEN** each theme's display name describes its color palette generically (e.g., by color or mood) and does not contain any third-party game's trademarked title

## REMOVED Requirements

### Requirement: Static two-color split background
**Reason**: Superseded by "Selectable color themes" (see ADDED Requirements) — the palette model changed from a two-tone top/bottom split to a solid background plus a single accent color, per a user-supplied set of classic-arcade-inspired color pairs that are all structured that way.
**Migration**: Visual-only watch face element; no data or API migration needed.

## ADDED Requirements

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
