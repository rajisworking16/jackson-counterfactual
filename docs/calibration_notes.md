# Calibration notes (Step 3.6)

This file records how the model was checked against the Jackson siblings, what didn't match, which parameters changed and why. It's dated 2026-11-20. The engine is seeded at 42 and runs 10,000 times per profile or preset.

The point of the check: nine children grew up in the same house with the same father, and their exposure varied. If the model gives a sibling-like exposure an outcome that the documented record rules out, the range is the suspect, not the sibling. This is a sanity check, not a measurement. It covers eight people (Jermaine is left out, see below), and the record holds public careers, public statements and lifespan to date. It says nothing about private wellbeing.

## Sibling dial profiles (ASSUMPTION)

The profiles are in [`data/sibling_profiles.csv`](../data/sibling_profiles.csv): one row per profile, the six dial values, and a basis note. No source gives anyone's dial values, so every row is ASSUMPTION, a judgment built from that sibling's exposure record in `data/sibling_outcomes.csv`.

| Profile | Discipline, Warmth, Autonomy, Normalcy, Body-image, Financial control |
|---|---|
| Michael | 9, 3, 2, 2, 8, 9 (= the Actual preset) |
| Jackie / Tito / Marlon | 9, 3, 2, 2, 3, 9 |
| Randy | 6, 4, 4, 5, 3, 8 |
| Janet | 5, 3, 5, 6, 3, 7 |
| Rebbie | 6, 3, 5, 6, 2, 3 |
| La Toya | 5, 4, 3, 5, 2, 6 |

Jermaine is excluded (`use_in_calibration = no (proxy)`), because his self-direction date is only a stand-in.

**Birth dates** were checked against a fetched source on 2026-11-20 (HELLO!, Nov 2026; AOL/Parade, Jul 2024 for years):
- Rebbie May 29, 1950; Jackie May 4, 1951; Tito Oct 15, 1953 (died Sept 15, 2024, at 70).
- La Toya May 29, 1956; Marlon Mar 12, 1957; Randy Oct 29, 1961; Janet May 16, 1966.

Randy's (1961) and La Toya's (1956) years in `sibling_outcomes.csv` were already correct, so nothing changed.

## How siblings are compared: censoring

Michael (died at 50) and Tito (died at 70) have a documented lifespan band, so for them the check is the share of runs in that band.

The other six are living, so their final band isn't known yet. Matching them to a band would treat "alive today" as "died in this band". For each living sibling, the check is instead the share of runs whose longevity band ends at or before their current age (as of 2026-11-20). The record has already ruled those runs out. **Lower is better.** The bands are read as half-open: "55-65" means died before 65.

## Changes applied

Each change was approved by Pranav (2026-11-20).

| Change | Before | After | Basis |
|---|---|---|---|
| **A. M12** Trauma / fear load → Longevity | 0.35-0.65, RESEARCH | 0.15-0.35, SIBLING CALIBRATION | Direction from ACE dose-response; size from siblings |
| **B. Longevity bins** (score → band) | 0-3 / 3-5 / 5-7 / 7+ | 0-2 / 2-3.5 / 3.5-5 / 5+ | ASSUMPTION |
| **Display rule** | n/a | No probability is ever shown as 0% or 100%; `format_prob` prints "<1%" / ">99%" | n/a |
| **E. Outcome baselines** drawn per run | Fixed 7.0 | Each outcome's baseline drawn independently per run: **6.0-8.0**; Longevity **4.5-8.5** | ASSUMPTION |

**Why A.** Trauma reached longevity twice: directly through M12, and through mental health (M05, then M14). Brothers with exposure close to the Actual preset are documented living past 65 (Tito died at 70; Jackie and Marlon are 75 and 69).

**Why B (the anchor, not a fit).** The 7.0 outcome baseline stands for an ordinary lifespan for a US man of Michael's generation. Its anchor is US male life expectancy at birth in 1958: **66.6 years** ([CDC/NCHS, Death rates and life expectancy at birth](https://data.cdc.gov/api/views/w9j2-ggv5/rows.csv)). Since 65 is just under an ordinary lifespan, the 65+ band has to start below the baseline score. The old bins started it at exactly 7, so a run only reached 65+ with zero load. The anchor fixes the direction: 65+ starts below 7. It doesn't fix the exact cut points (2 / 3.5 / 5), which stay ASSUMPTION.

**Michael's 45-55 share is a side effect, not a target.** After A and B, the Actual preset put 63% of runs in 45-55. That followed from correcting the brothers' lifespans, which the old model ruled out. The model wasn't tuned to make Michael land at 50. Under E it drops to 34% (see below), and that is accepted.

**Why E.** The fixed 7.0 baseline meant a preset with near-zero load got the same score in every run. That produced bands with no spread: Nurturing at 100% in 65+, and mental health capped at exactly 7.00. Drawing the baseline per run puts back the variation that has nothing to do with parenting. Longevity gets the widest range, because non-parenting factors such as acute events move lifespan a lot; his own death, acute propofol intoxication ruled a homicide, is one of them. The brief was to start at 4.5-8.5 and widen until no preset was above about 95% in any band. At 4.5-8.5 the highest preset band share is 86%, so no widening was needed. **Range used: 4.5-8.5.** M14 now uses each run's own mental-health baseline: `M14 × (mental baseline − mental)`.

**Open choice on E (not changed).** 4.5-8.5 is centered on 6.5, not 7.0, so besides widening it also lowers every profile's longevity by 0.5 on average. A range centered on 7.0 (5.0-9.0) improves the living-sibling check (for example Randy 59% → 47%, La Toya 46% → 34%). But it puts Nurturing at 98.7% in 65+, which breaks the ~95% rule, so it would need widening to around 4.0-10.0. That's a decision for Pranav.

## Before and after

**Before** = committed after A + B (fixed 7.0 baseline). **After** = with E applied.

**Siblings**

| Sibling | Status (2026-11-20) | Check | Before | After |
|---|---|---|---|---|
| Michael | died at 50 | P(45-55) | 62.9% | 33.8% |
| Tito | died at 70 | P(65+) | 0.2% | 5.7% |
| Jackie | living, 75 | P(band ends by 75), lower is better | 99.8% | 94.3% |
| Marlon | living, 69 | P(band ends by 69) | 99.8% | 94.3% |
| Randy | living, 65 | P(band ends by 65) | 36.3% | 59.3% |
| Rebbie | living, 76 | P(band ends by 76) | 34.6% | 59.0% |
| La Toya | living, 70 | P(band ends by 70) | 4.9% | 46.4% |
| Janet | living, 60 | P(band ends by 60) | 0.0% | 16.6% |

**Presets (longevity bands; Childhood mental health)**

| Preset | <45 / 45-55 / 55-65 / 65+ before | after | Mental at exactly 0, before → after | Mental p90, before → after |
|---|---|---|---|---|
| Actual (documented) | 26% / 63% / 11% / <1% | 50% / 34% / 16% / 1% | 21.5% → 24.9% | 1.89 → 2.16 |
| Strict coach, warm father | <1% / <1% / 4% / 96% | <1% / 7% / 36% / 57% | 0% → 0% | 5.90 → 6.25 |
| Firm but nurturing | <1% / <1% / <1% / >99% | <1% / <1% / 14% / 86% | 0% → 0% | 7.00 → 7.67 |

**What E fixed:** no preset is near-certain in any band anymore (the top share is 86%, down from 100%), and mental health is no longer capped at 7.00.

**What it cost:** spreading the outcomes also spreads them downward, so more runs for every living sibling end before their current age. The brothers stay the worst miss: 94% of runs for a brother's profile are ruled out by Jackie and Marlon being alive.

## Test F (not applied): reference-level loads

Loads enter the outcome formulas relative to a reference level of 3, `(load − 3)`, so a load below 3 adds to the outcome. Tested in memory, on top of E:

| Measure | Without F (E applied) | With F |
|---|---|---|
| Actual: share of Childhood runs at exactly 0 mental health | 24.9% | 0.0% |
| Nurturing: Childhood mental health p90 | 7.67 | 10.00 (at the cap) |
| Nurturing: longevity 65+ share | 86% | 100% |
| Strict coach: longevity 65+ share | 57% | 100% |

F removes the floor but moves the problem to the top. The low-load presets pile up at the 10.0 cap, and both are back to 100% in one band. Not recommended as it stands. A version with a cap well above 7 (or no fixed cap) would need its own design.

## Other options documented but not applied

- **C.** Narrow M14 to 0.10-0.30. It helps the brothers and hurts the match for Michael. That's a trade-off, not a fix.
- **D.** Branch logistic midpoint 5.5 → 4.5. All eight siblings had careers, but this would also change the counterfactual presets' headline results.

## What the model still can't do

- **Tell Michael from his brothers.** In these profiles the only dial difference is body-image comments, so the model predicts nearly the same lifespan for very different documented lives. The brothers' profile is the single largest miss. Lowering their discipline from 9 to 7 helped about as much as any parameter change did, so the gap is as sensitive to the profile guess as to the model.
- **Model an acute cause of death.** Michael's death on June 25, 2009 was ruled a homicide, from acute propofol intoxication, and his physician was convicted of involuntary manslaughter. The longevity path is a chronic dose-response curve with a wide non-parenting spread (E). None of it is a claim that the parenting variable explains how or when he died.
- **Rank careers the way the record does.** Career is scored from practice volume. Group role, opportunity and talent aren't parenting dials.
- **Check mental health against the siblings.** No permitted evidence exists: the rules allow no inference about anyone's private mental health. The Actual preset's mental-health floor (24.9% of Childhood runs at exactly 0) remains an ASSUMPTION-driven result.

## Sanity checks (after E)

| Check | Result |
|---|---|
| 1. Actual: Branch C dominates, Branch A near zero | Partly (C 0.546 is the largest; A 0.119) |
| 2. Nurturing: Branch A rises but doesn't swallow everything | Passes (A 0.287; B 0.606 is the largest) |
| 3. Actual mental health clearly below Nurturing | Passes (median 0.77 vs 6.85) |
| No preset above ~95% in any longevity band | Passes (max 86%) |
