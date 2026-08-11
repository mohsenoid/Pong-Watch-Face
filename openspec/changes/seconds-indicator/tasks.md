## 1. Implement

- [ ] 1.1 Add a `PartText` using `Localization`/`Text`/`Font family="SYNC_TO_DEVICE"`/`Template`/`Parameter expression="[SECOND_Z]"`, matching the date text's structure, placed small and near the main time row.
- [ ] 1.2 Build, install, check `adb logcat` for parse/evaluation failures.

## 2. Verify

- [ ] 2.1 Screenshot to confirm the seconds value renders and updates every second.
- [ ] 2.2 Visually assess whether it competes with or looks inconsistent next to the `hh:mm` pixel-font display; adjust size/position/color if needed.
- [ ] 2.3 Confirm ambient mode and all other existing behavior are unaffected.

## 3. Final verification

- [ ] 3.1 Confirm no build/dependency changes were introduced — module stays `hasCode = false`.
- [ ] 3.2 Regenerate `res/drawable/preview.png` reflecting the new seconds indicator.
- [ ] 3.3 Update this file's checkboxes with outcomes.
