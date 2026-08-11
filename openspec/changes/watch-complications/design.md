## Context

The current `watchface.xml` has a fixed layout on a 450x450 circular canvas: two-tone split background, a date/day `PartText` at `y=70`, three digit groups at `y=148`, and an `arcade_track` `Group` at `y≈320-440`. The band around the date text (`y≈40-110`) is the only space not already occupied. `ComplicationSlot` and `DefaultProviderPolicy` have not been used in this project before.

Research this session found the concrete mechanism:
- `ComplicationSlot` requires `x`, `y`, `width`, `height`, `slotId`, `supportedTypes`, one `Bounding` child, and one `<Complication type="...">` block per supported type.
- `DefaultProviderPolicy defaultSystemProvider="STEP_COUNT|WATCH_BATTERY" defaultSystemProviderType="SHORT_TEXT"` pre-assigns a system provider; the user can still reassign via the system's complication picker.
- `SHORT_TEXT` complications expose `[COMPLICATION.TEXT]`, `[COMPLICATION.TITLE]`, `[COMPLICATION.MONOCHROMATIC_IMAGE]` for use inside `PartText`/`PartImage` with the existing `Template`/`Parameter` pattern already used for the date text.
- A watch face cannot force a complication to always show one specific data source and hide reassignment — that's standard, unavoidable Wear OS UX.

## Goals / Non-Goals

**Goals:**
- Two complication slots showing live step count and battery level by default, reachable and reassignable via the existing Edit flow.
- Fits the retro-arcade visual language without changing the color-theme system or layout proportions.

**Non-Goals:**
- Custom complication data sources (weather, custom app data).
- Letting the user reposition/resize complications beyond the system's own reassignment flow.
- `RANGED_VALUE` or image-heavy complication types — `SHORT_TEXT` only, for simplicity and to match existing text-rendering patterns.

## Decisions

**`SHORT_TEXT` complications rendered via the existing `PartText`/`Template`/`Parameter` pattern.** Simplest type to integrate with code already in the file (the date text uses this exact pattern), reads clearly at small watch-face scale, and avoids the extra visual work `RANGED_VALUE` (progress arc/bar) would need.

**Placement: flanking the date text, roughly `x≈70,y≈55` and `x≈340,y≈55`, ~50x50 each.** This is the only band of the canvas not already occupied. Exact coordinates need on-device verification against the circle's boundary (`half_width = sqrt(225² - (y-225)²)`) before finalizing, consistent with prior bezel-adjacent work in this project.

**One slot each for `STEP_COUNT` and `WATCH_BATTERY` via `DefaultProviderPolicy`.** Guarantees both slots are populated immediately on install without requiring the user to open the Edit flow first (assuming `DefaultProviderPolicy` behaves as documented — to be confirmed on-device, since this could plausibly need the user to visit Edit at least once, per Risks below).

## Risks / Trade-offs

- [Risk] `ComplicationSlot`/`DefaultProviderPolicy` are new mechanisms for this project; whether `DefaultProviderPolicy` truly pre-populates data before the user ever opens Edit is unverified, and `SHORT_TEXT`'s `[COMPLICATION.TEXT]` may truncate awkwardly at small sizes. → Mitigation: build/install/screenshot/logcat-check with one minimal slot before building both out fully.
- [Risk] Complication slot placement could clip the circular bezel or crowd the date text. → Mitigation: screenshot-verify placement on-device before finalizing coordinates.
- [Risk] Complications may require additional `AndroidManifest.xml` declarations not obvious from the WFF XML reference alone. → Mitigation: watch `adb logcat` closely on first build for complication-related registration errors.

## Migration Plan

Pure additive change — no persisted data beyond the system's own complication-provider assignment (standard Wear OS behavior). Rollback is a plain revert of the added `ComplicationSlot` elements and any manifest changes.
