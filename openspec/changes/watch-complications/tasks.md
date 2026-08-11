## 1. Verify ComplicationSlot works at all

- [ ] 1.1 Add one minimal `ComplicationSlot` (`supportedTypes="SHORT_TEXT"`, `DefaultProviderPolicy defaultSystemProvider="STEP_COUNT" defaultSystemProviderType="SHORT_TEXT"`) with a plain `PartText` rendering `[COMPLICATION.TEXT]`, positioned in a rough placeholder spot.
- [ ] 1.2 Build, install, check `adb logcat` for parse/evaluation failures, including any manifest-related complication registration errors.
- [ ] 1.3 Screenshot to confirm the step count actually renders (not blank/placeholder), and check whether `DefaultProviderPolicy` populated it immediately or requires the user to open the Edit flow first.
- [ ] 1.4 Confirm the slot is reachable/reassignable via the watch face's existing Edit flow (long-press → Edit → complication picker).

## 2. Build both complication slots

- [ ] 2.1 Add the second `ComplicationSlot` (`WATCH_BATTERY` default provider), matching the first slot's `SHORT_TEXT` rendering pattern.
- [ ] 2.2 Position both slots flanking the date text near `y≈55`, verifying against the circle's boundary math so neither clips the bezel or overlaps the date text; adjust coordinates as needed.
- [ ] 2.3 Style the complication text to fit the retro-arcade look (color, size) without over-scoping into a full pixel-font treatment.
- [ ] 2.4 Build, install, check logcat, screenshot both slots showing live data.

## 3. Final verification

- [ ] 3.1 Confirm all 15 color themes, ambient mode, and existing arena/date behavior are unaffected.
- [ ] 3.2 Confirm no build/dependency changes were introduced beyond `res/` resources and (if needed) manifest complication declarations — module stays `hasCode = false`.
- [ ] 3.3 Regenerate `res/drawable/preview.png` reflecting the new complications.
- [ ] 3.4 Update this file's checkboxes with outcomes and any deviations discovered during implementation.
