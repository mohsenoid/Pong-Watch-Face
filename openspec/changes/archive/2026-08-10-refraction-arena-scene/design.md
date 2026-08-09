## Context

The watch face (`watchface/src/main/res/raw/watchface.xml`) currently has an `arcade_track` `Group` (river strip + drifting jet) occupying a band at `y="350"` to `y="414"` (height 64) below the time display, hidden in ambient mode via the existing `Variant` pattern. The prior change (`arcade-attract-watch-face`, now archived) established two load-bearing WFF facts worth restating since this design depends on them:

- Dynamic per-tick attribute values (position, alpha, etc.) only work via a `<Transform target="..." value="...">` **child element**, not as an inline expression string on the attribute itself. Confirmed via `adb logcat --pid=$(adb shell pidof -s com.google.wear.watchface.runtime)`, which surfaces `fail to parseInt: <expression>` when this is done wrong.
- A drawable referenced by both a `BitmapFont` Character map and a plain `PartImage` fails to render in the `PartImage` on this runtime — not relevant to this change (no shared resources planned) but worth keeping in mind if the ship/missile assets ever get reused elsewhere.

See proposal.md for why the river/jet scene is being replaced.

## Goals / Non-Goals

**Goals:**
- Replace the arena content (not its screen position or ambient-mode wiring, both of which already work) with a divider + two ships + one bouncing element.
- Get the bounce animation right using the already-proven `Transform` pattern from the start, instead of repeating last change's trial-and-error.
- Keep the asset count small: no separate arena background image — the divider/ships/missile render directly over the existing scanline background.

**Non-Goals:**
- No change to the digit font, hour-tens digit logic, colon, scanline background asset, branding, or ambient time text.
- No "refraction bend" physics simulation — the bounce is a straightforward back-and-forth (triangle wave), same mechanism as the prior jet drift, just correctly implemented this time. A visual flash/color-shift at the divider crossing is a nice-to-have, not required for this change's scenarios.
- No sound, haptics, or interactivity (tap-to-react) — WFF's tap-driven state changes weren't explored in the prior change and are out of scope here too.

## Decisions

**Transparent arena band, no dedicated background asset.** The prior river strip was its own opaque PNG layer. Since the new scene is just three small elements (divider, two ships, missile) rather than a full texture, letting the existing black scanline background show through directly behind them removes an asset and a potential z-order/alpha-blending pitfall, with no visible downside.

**Divider and ships are static `PartImage`s; only the missile gets a `Transform`.** Keeping the moving-parts surface area minimal (one element with dynamic behavior, matching the prior change's now-working example) reduces risk versus animating multiple pieces at once.

**Reuse the exact proven bounce formula and wiring.** `x="<min> + (clamp([SECOND],0,30) - clamp([SECOND]-30,0,30)) / 30 * <range>"` inside `<Transform target="x" value="...">`, nested inside the missile's `PartImage`, identical in structure to what was verified working (confirmed via logcat showing zero parse failures, and screenshots at different `[SECOND]` values showing different x positions) in the prior change. No new expression mechanism is being tried here.

**Color palette leans into Atari's multi-color capability rather than staying monochrome-orange.** The source article specifically highlights the Atari 2600's ability to show many colors on screen as a step up from the developer's earlier monochrome work. Giving the two ships and the missile distinct saturated colors (rather than reusing the time display's orange) visually nods to that without copying any specific in-game color values, since none were available from the article itself.

**Arena elements sit in the same `y="350"` height="64"` band as before**, preserving the vertical layout/spacing already tuned and verified against the circular clip bounds in the prior change.

## Risks / Trade-offs

- [Risk] Divider, ships, and missile could look cramped or overlap oddly within the existing 64px-tall band. → Mitigation: size assets with visible margin from the band edges; visually verify via emulator screenshot before calling it done (the concrete lesson from the prior change's river/jet redesign, which needed a redo after user feedback).
- [Risk] The missile crossing behind/in front of the divider or ships inconsistently. → Mitigation: XML document order controls paint order (later elements draw on top) — declare divider and ships first, missile last, within the arena `Group`.
- [Risk] Re-introducing the `x`-as-inline-attribute bug by copy-pasting the old (broken) river/jet snippet as a starting point instead of the fixed one. → Mitigation: start from the current (already-fixed) `Transform`-based sprite block in `watchface.xml` as the template, and check `adb logcat` for `fail to parseInt` immediately after the first build/install, before doing any further visual iteration.

## Migration Plan

Pure visual/resource change to a single decorative `Group` — no data, no persisted state, no build/manifest changes. Rollout: implement, verify on the Wear OS emulator (active mode bounce, ambient-mode hide, no logcat parse failures), done. Rollback is a plain revert of the `watchface.xml` `Group` and the drawable files.
