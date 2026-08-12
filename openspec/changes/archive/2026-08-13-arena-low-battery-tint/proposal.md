## Why

The watch face currently gives no visual indication of low battery anywhere. A small warning tint on the Pong arena elements gives the user a glanceable cue without adding any new UI chrome.

## What Changes

- The Pong ball switches to a warning color (red) when the device's battery level drops below a low-battery threshold, using the standalone `[BATTERY_PERCENT]` data source (independent of any complication). Applies in both Classic and Scoreboard layouts.
- It reverts to its normal yellow once the battery is no longer low.
- The paddles are intentionally left untinted (scoped down from the original "ball and both paddles" idea per live feedback during implementation) — the ball alone is enough of a cue without recoloring more of the arena.
- No changes to the color-theme system, paddle motion, ball motion, or any other arena behavior.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
(none — this adds new observable behavior via an additive requirement, not a change to existing requirement text)

## Impact

- Affected files: `watchface/src/main/res/raw/watchface.xml` (add `Transform target="tintColor"` expressions on the ball `PartImage`s in both layouts, driven by `[BATTERY_PERCENT]`).
- No build, dependency, or `hasCode` changes.
- First use of the standalone `[BATTERY_PERCENT]` data source in this project — gets verified on-device (build, install, `adb logcat`, screenshot) before being considered done, consistent with this project's established practice.
