## 1. Implement

- [x] 1.1 Add a `PartText` using `Localization`/`Text`/`Font family="SYNC_TO_DEVICE"`/`Template`/`Parameter expression="[SECOND_Z]"`, matching the date text's structure, placed small and near the main time row. **Outcome:** placed at `x=190,y=114,width=70,height=24`, size 16, centered in the free gap between the Classic date text (ends ~y=110) and the hh:mm digit row (starts y=148). Gated Classic-only (`[CONFIGURATION.layout]=="0"`) since Scoreboard's equivalent space is occupied by the large hour digit.
- [x] 1.2 Build, install, check `adb logcat` for parse/evaluation failures. **Outcome:** clean build, clean logcat, no errors.

## 2. Verify

- [x] 2.1 Screenshot to confirm the seconds value renders and updates every second. **Outcome:** confirmed via two screenshots ~2s apart ("17" → "20").
- [x] 2.2 Visually assess whether it competes with or looks inconsistent next to the `hh:mm` pixel-font display; adjust size/position/color if needed. **Outcome:** reads clearly as a small secondary element, doesn't compete with the large pixel-font digits below it. No adjustment needed.
- [x] 2.3 Confirm ambient mode and all other existing behavior are unaffected. **Outcome:** ambient dims correctly along with the rest of the scene (same `Variant` alpha applies), value freezes like other animated elements per the system's ambient snapshot behavior. Confirmed Scoreboard layout correctly hides the indicator (gated `[CONFIGURATION.layout]=="0"`). Repositioned during implementation per live feedback from `y=114` (gap between date and time) to `y=275` (gap between the digit row and the Classic Pong divider, which is actually at `y=322`, not the Scoreboard-only divider at `y=258`).

## 3. Final verification

- [x] 3.1 Confirm no build/dependency changes were introduced — module stays `hasCode = false`. **Outcome:** confirmed — only `watchface/src/main/res/raw/watchface.xml` changed; no build/manifest changes needed.
- [x] 3.2 Regenerate `res/drawable/preview.png` reflecting the new seconds indicator. **Outcome:** done, reflects Classic layout with the seconds readout in place.
- [x] 3.3 Update this file's checkboxes with outcomes. Done — see above.
- [x] 3.4 (added after initial implementation, per user request) Make the seconds indicator optional rather than always-on in Classic layout, so the user can decide whether to show it. **Outcome:** added a `BooleanConfiguration id="showSeconds" defaultValue="TRUE"` alongside the existing `Layout` `ListConfiguration`, gated as a separate on-device editor page ("Show Seconds" toggle). The seconds `PartText`'s alpha now requires both `[CONFIGURATION.layout]=="0"` and `[CONFIGURATION.showSeconds]=="TRUE"`. Verified in the on-device editor (now 3 pages: Color Theme, Layout, Show Seconds) — toggling off immediately hides the indicator on the live face, toggling on restores it, default is on.
- [x] 3.5 (added after 3.4, per user request) Also show seconds in Scoreboard layout, controlled by the same toggle. **Outcome:** added a second `PartText` at `x=203,y=221,width=44,height=20`, size 14, placed in the otherwise-empty gap between the two large scoreboard digits (x≈198–252, y≈207–255) — reads like a small period/timer indicator on a real scoreboard. Gated `([CONFIGURATION.layout]=="1")*([CONFIGURATION.showSeconds]=="TRUE")`. Verified: renders, updates every second, clears the divider (starts y=258) and both score digits with margin, dims correctly in ambient mode. One toggle now controls the indicator in both layouts.
