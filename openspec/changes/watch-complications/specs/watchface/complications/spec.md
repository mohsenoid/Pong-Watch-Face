## Purpose

Defines the watch face's use of native Wear OS complications to surface live system data (such as step count and battery level) without the watch face implementing any custom data-fetching logic itself.

## ADDED Requirements

### Requirement: Step count and battery complications
The watch face SHALL provide two complication slots, defaulting to step count and battery level respectively, populated via the system's own complication data sources rather than any custom data source.

#### Scenario: Complications show live system data
- **WHEN** the watch face is installed and in active mode
- **THEN** one slot displays the current step count and the other displays the current battery level, both sourced from the system

#### Scenario: Complication values update as system data changes
- **WHEN** the underlying system data for a complication changes (e.g., step count increases, battery level drops)
- **THEN** the displayed complication value updates to match

### Requirement: Complications are user-reassignable
The watch face SHALL allow the user to reassign either complication slot to a different compatible data source through the system's standard complication picker, reached via the watch face's on-device Edit flow.

#### Scenario: User reassigns a complication slot
- **WHEN** a user opens the watch face's Edit flow and changes a complication slot's assigned data source
- **THEN** the slot displays data from the newly assigned source instead of the default
