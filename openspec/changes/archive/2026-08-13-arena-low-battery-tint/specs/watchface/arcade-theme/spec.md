## ADDED Requirements

### Requirement: Low-battery arena tint
The Pong ball SHALL switch to a warning tint when the device's battery level drops below a low-battery threshold, in both Classic and Scoreboard layouts, and SHALL revert to its normal color once the battery is no longer low, independent of any complication configuration. The paddles are unaffected and always render in their normal color.

#### Scenario: Ball shows a low-battery warning tint
- **WHEN** the device's battery level drops below the low-battery threshold
- **THEN** the ball renders in a warning color instead of its normal color, in whichever layout is currently selected

#### Scenario: Warning tint clears when battery is no longer low
- **WHEN** the device's battery level rises back above the low-battery threshold (e.g., after charging)
- **THEN** the ball returns to its normal color

#### Scenario: Paddles are unaffected by battery level
- **WHEN** the device's battery level drops below the low-battery threshold
- **THEN** the paddles continue to render in their normal color, unaffected by the ball's warning tint
