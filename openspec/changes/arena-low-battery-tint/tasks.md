## 1. Verify tintColor responds to a conditional battery expression

- [ ] 1.1 On the ball `PartImage` only, add `Transform target="tintColor" value="[BATTERY_PERCENT] < 100 ? '#FF2222' : '#FFE600'"` (loosened threshold to force the warning state visibly for testing; exact string/color-literal syntax to confirm against the arithmetic-expression reference).
- [ ] 1.2 Build, install, check `adb logcat` for parse/evaluation failures.
- [ ] 1.3 Screenshot to confirm the ball renders red (forced warning state).
- [ ] 1.4 Change the threshold back toward a real value (`< 20`) and confirm the ball returns to its normal yellow color at the current (presumably higher) battery level.

## 2. Apply to both paddles

- [ ] 2.1 Apply the same pattern (with the real `< 20` threshold) to both paddle `PartImage`s.
- [ ] 2.2 Build, install, check logcat, screenshot to confirm all three elements (ball + 2 paddles) tint together.

## 3. Final verification

- [ ] 3.1 Confirm normal (non-low-battery) rendering is unaffected across a couple of the 15 color themes.
- [ ] 3.2 Confirm ambient mode still works correctly with the new expression in place.
- [ ] 3.3 Confirm no build/dependency changes were introduced — module stays `hasCode = false`.
- [ ] 3.4 Update this file's checkboxes with outcomes, including the confirmed expression syntax.
