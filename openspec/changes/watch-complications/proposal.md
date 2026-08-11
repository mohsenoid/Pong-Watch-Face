## Why

The watch face is currently purely decorative — it shows no live system data. Adding step count and battery complications makes it feel like a genuine daily-driver face, using the system's own complication data rather than any custom logic.

## What Changes

- Add two native Watch Face Format complication slots (`ComplicationSlot`), defaulting to step count and battery level via `DefaultProviderPolicy`.
- Both slots remain user-reassignable to any compatible system-provided complication through the standard Wear OS complication picker, reached via the watch face's existing on-device Edit flow.
- Slots are placed in the currently-empty space flanking the date text near the top of the watch face.
- No changes to the color-theme system, digit font, date display, or Pong arena.

## Capabilities

### New Capabilities
- `watchface/complications`: native system-data complications (steps, battery) surfaced on the watch face via `ComplicationSlot`.

### Modified Capabilities
(none)

## Impact

- Affected files: `watchface/src/main/res/raw/watchface.xml` (add two `ComplicationSlot` elements with `DefaultProviderPolicy` and `PartText` rendering), `watchface/src/main/AndroidManifest.xml` (verify whether complications require additional manifest declarations).
- No build, dependency, or `hasCode` changes — module stays declarative XML only.
- First use of `ComplicationSlot`/`DefaultProviderPolicy` in this project — per this project's established discipline, gets verified on-device early (build, install, check `adb logcat`, screenshot) rather than assumed to work from documentation alone.
