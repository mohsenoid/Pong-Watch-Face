## Why

The watch face currently gives no visual indication of low battery anywhere. A small warning tint on the Pong arena elements gives the user a glanceable cue without adding any new UI chrome.

## What Changes

- The Pong ball and both paddles switch to a warning color (e.g. red) when the device's battery level drops below a low-battery threshold, using the standalone `[BATTERY_PERCENT]` data source (independent of any complication).
- They revert to their normal color once the battery is no longer low.
- No changes to the color-theme system, paddle motion, ball motion, or any other arena behavior.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
(none — this adds new observable behavior via an additive requirement, not a change to existing requirement text)

## Impact

- Affected files: `watchface/src/main/res/raw/watchface.xml` (add `Transform target="tintColor"` expressions on the ball and paddle `PartImage`s, driven by `[BATTERY_PERCENT]`).
- No build, dependency, or `hasCode` changes.
- First use of the standalone `[BATTERY_PERCENT]` data source in this project — gets verified on-device (build, install, `adb logcat`, screenshot) before being considered done, consistent with this project's established practice.
