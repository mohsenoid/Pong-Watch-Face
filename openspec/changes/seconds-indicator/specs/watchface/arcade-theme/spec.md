## ADDED Requirements

### Requirement: Seconds indicator
The watch face SHALL display the current seconds value in both Classic and Scoreboard layouts when the "Show Seconds" setting is enabled (default: on), updating at least once per second, positioned in each layout so it does not compete visually with the primary time display. It SHALL be hidden entirely, in both layouts, when the setting is disabled.

#### Scenario: Seconds value updates every second
- **WHEN** the device's seconds value changes while the watch face is in active mode and "Show Seconds" is enabled
- **THEN** the displayed seconds indicator updates to match, regardless of which layout is selected

#### Scenario: User disables the seconds indicator
- **WHEN** the user turns off "Show Seconds" in the watch face editor
- **THEN** the seconds indicator is hidden immediately in both layouts, with no other visual change
