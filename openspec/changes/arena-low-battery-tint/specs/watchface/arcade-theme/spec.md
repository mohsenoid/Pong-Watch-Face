## ADDED Requirements

### Requirement: Low-battery arena tint
The Pong ball and paddles SHALL switch to a warning tint when the device's battery level drops below a low-battery threshold, and SHALL revert to their normal color once the battery is no longer low, independent of any complication configuration.

#### Scenario: Ball and paddles show a low-battery warning tint
- **WHEN** the device's battery level drops below the low-battery threshold
- **THEN** the ball and paddles render in a warning color instead of their normal color

#### Scenario: Warning tint clears when battery is no longer low
- **WHEN** the device's battery level rises back above the low-battery threshold (e.g., after charging)
- **THEN** the ball and paddles return to their normal color
