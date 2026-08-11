## Context

The date text at `y=70` already uses `PartText` + `Localization` + `Text`/`Font`/`Template`/`Parameter` to render `[DAY_OF_WEEK_S]`, `[MONTH_S]`, `[DAY_Z]`. The same data-source family includes `[SECOND_Z]` (zero-padded seconds), already confirmed available per the WFF data-source reference used elsewhere this session. No new mechanism is needed.

## Goals / Non-Goals

**Goals:**
- A small, always-updating seconds readout that doesn't visually compete with the `hh:mm` display.

**Non-Goals:**
- A pixel-font seconds glyph set matching the main digits — plain system text is enough for a secondary, low-emphasis element (see Decisions).

## Decisions

**Plain system-font `PartText`, not new pixel-glyph `PartImage`s.** The main time digits use ~28 conditional `PartImage`s (one per possible digit value) purely because `TimeText`/`BitmapFont` was confirmed unable to support any dynamic `Transform`/`tintColor` in this project's earlier theming work. Seconds don't need per-theme tinting or the exact pixel font — reusing the date text's system-font pattern is far simpler and keeps this a small, low-risk change.

**Placement: small and near the existing colon/time row, not a separate prominent element.** Exact position to be confirmed visually during implementation so it reads as a secondary indicator, not a competing third time field.

## Risks / Trade-offs

- [Risk] A system-font seconds readout may look visually inconsistent next to the pixel-font `hh:mm` digits. → Mitigation: verify visually after implementation; if it looks out of place, this can be revisited later as its own follow-up (e.g. a smaller pixel-font treatment) without blocking this change.

## Migration Plan

Pure additive visual change, no persisted data. Rollback is a plain revert of the added `PartText` element.
