# Calibration notes (Step 3.6)

This file records how the model was checked against the Jackson siblings, what didn't match, which parameters changed and why. It's dated 2026-11-20. The engine is seeded at 42 and runs 10,000 times per profile or preset. **Calibration is frozen** (see the end of this file).

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

**Birth dates**, checked against a fetched source on 2026-11-20 (HELLO!, Nov 2026; AOL/Parade, Jul 2024 for years):
- Rebbie May 29, 1950; Jackie May 4, 1951; Tito Oct 15, 1953 (died Sept 15, 2024, at 70).
- La Toya May 29, 1956; Marlon Mar 12, 1957; Randy Oct 29, 1961; Janet May 16, 1966.

Randy's and La Toya's years were already correct.

## How siblings are compared: censoring

Michael (died at 50) and Tito (died at 70) have a documented lifespan band, so for them the check is the share of runs in that band.

The other six are living, so their final band isn't known yet. For each of them, the check is the share of runs whose band ends at or before their current age (as of 2026-11-20). The record has already ruled those runs out. **Lower is better.** The bands are read as half-open: "55-65" means died before 65.

## Changes applied

Each change was approved by Pranav (2026-11-20).

| Change | Before | After | Basis |
|---|---|---|---|
| **A. M12** Trauma / fear load → Longevity | 0.35-0.65, RESEARCH | 0.15-0.35, SIBLING CALIBRATION | Direction from ACE dose-response; size from siblings |
| **B. Longevity bins** (score → band) | 0-3 / 3-5 / 5-7 / 7+ | 0-2 / 2-3.5 / 3.5-5 / 5+ | ASSUMPTION, anchored (below) |
| **Display rule** | n/a | No probability shown as 0% or 100%; `format_prob` prints "<1%" / ">99%" | n/a |
| **E. Outcome baselines** drawn per run | Fixed 7.0 | Each outcome drawn independently per run: **6.0-8.0**; Longevity **4.5-9.5** (centered on 7.0) | ASSUMPTION |

**Why A.** Trauma reached longevity twice: directly through M12, and through mental health (M05, then M14). Brothers with exposure close to the Actual preset are documented living past 65 (Tito died at 70; Jackie and Marlon are 75 and 69).

**Why B (an anchor, not a fit).** The 7.0 outcome baseline stands for an ordinary lifespan for a US man of Michael's generation. Its anchor is US male life expectancy at birth in 1958: **66.6 years** ([CDC/NCHS, Death rates and life expectancy at birth](https://data.cdc.gov/api/views/w9j2-ggv5/rows.csv)). Since 65 is just under an ordinary lifespan, the 65+ band has to start below the baseline score. The old bins started it at exactly 7, so a run only reached 65+ with zero load. The anchor fixes the direction: 65+ starts below 7. It doesn't fix the exact cut points (2 / 3.5 / 5), which stay ASSUMPTION.

**Michael's 45-55 share is a side effect, not a target.** After A and B it was 63%. That followed from correcting the brothers' lifespans, which the old model ruled out. It was never tuned to put Michael at 50. Under the final E it's 30%, and that is accepted.

**Why E.** With a fixed 7.0 baseline, a preset with near-zero load got the same score in every run. That produced bands with no spread: Nurturing at 100% in 65+, and mental health capped at exactly 7.00. Drawing the baseline per run puts back the variation that has nothing to do with parenting. Longevity gets the widest range, because non-parenting factors such as acute events move lifespan a lot; his own death, acute propofol intoxication ruled a homicide, is one of them. The range is centered on 7.0, matching B's anchor. **4.5-9.5 is the narrowest centered range that keeps every preset at or under ~95% in any band.** M14 uses each run's own mental-health baseline: `M14 × (mental baseline − mental)`.

### Choosing E's longevity range

| Longevity baseline | Center | Highest preset band | Michael P(45-55) | Tito P(65+) | Jackie / Marlon ↓ | Randy ↓ | Rebbie ↓ | La Toya ↓ | Janet ↓ | Living avg ↓ |
|---|---|---|---|---|---|---|---|---|---|---|
| 4.5-8.5 (superseded) | 6.5 | 86% | 33.8% | 5.7% | 94.3% | 59.3% | 59.0% | 46.4% | 16.6% | 61.7% |
| 5.0-9.0 | 7.0 | **98.7%** (fails ~95%) | 36.2% | 13.6% | 86.4% | 46.7% | 46.3% | 33.5% | 6.4% | 51.0% |
| **4.5-9.5 (applied)** | 7.0 | 89% | 29.7% | 19.3% | 80.7% | 47.6% | 47.2% | 37.0% | 13.2% | 51.1% |
| 4.0-10.0 | 7.0 | 82% | 24.9% | 23.4% | 76.6% | 48.0% | 47.6% | 39.2% | 19.3% | 51.2% |

↓ = P(band ends by current age), lower is better. "Living avg" averages the six living siblings, counting Jackie and Marlon separately.

**Superseded step: 4.5-8.5.** This was the first E run. It was centered on 6.5, not 7.0, so as well as widening the spread it lowered every profile's longevity by 0.5 on average. That broke B's anchor (7.0 = an ordinary lifespan), and it made the check worse for every living sibling. It was replaced by 4.5-9.5, which is better on every living sibling: the average falls from 61.7% to 51.1%.

## Before and after (whole Step 3.6)

**Siblings**

| Sibling | Status (2026-11-20) | Check | Starter model | After A + B | Final (A + B + E 4.5-9.5) |
|---|---|---|---|---|---|
| Michael | died at 50 | P(45-55) | 1.3% | 62.9% | 29.7% |
| Tito | died at 70 | P(65+) | 0.0% | 0.2% | 19.3% |
| Jackie | living, 75 | P(ends by 75) ↓ | 100% | 99.8% | 80.7% |
| Marlon | living, 69 | P(ends by 69) ↓ | 100% | 99.8% | 80.7% |
| Randy | living, 65 | P(ends by 65) ↓ | 99.9% | 36.3% | 47.6% |
| Rebbie | living, 76 | P(ends by 76) ↓ | 100% | 34.6% | 47.2% |
| La Toya | living, 70 | P(ends by 70) ↓ | 100% | 4.9% | 37.0% |
| Janet | living, 60 | P(ends by 60) ↓ | 69.3% | 0.0% | 13.2% |

The starter model had a 0% 65+ share for every profile, so every living sibling past 65 was fully ruled out.

**Presets**

| Preset | Longevity <45 / 45-55 / 55-65 / 65+: starter | after A + B | final | Childhood mental health: share at 0, p90 (final) |
|---|---|---|---|---|
| Actual (documented) | 99% / 1% / 0 / 0 | 26% / 63% / 11% / <1% | 40% / 30% / 23% / 7% | 24.9%, 2.16 |
| Strict coach, warm father | 0 / 25% / 75% / 0 | <1% / <1% / 4% / 96% | <1% / 6% / 29% / 65% | 0%, 6.25 |
| Firm but nurturing | 0 / 0 / 64% / 36% | <1% / <1% / <1% / >99% | <1% / <1% / 11% / 89% | 0%, 7.67 |

## Test F: tested and rejected

Loads entered the outcome formulas relative to a reference level of 3, `(load − 3)`, so a load below 3 would add to the outcome. It was tested in memory, on top of E:

| Measure | Without F | With F |
|---|---|---|
| Actual: share of Childhood runs at exactly 0 mental health | 24.9% | 0.0% |
| Nurturing: Childhood mental health p90 | 7.67 | 10.00 (at the cap) |
| Nurturing and Strict coach: longevity 65+ share | 86% and 57% | 100% and 100% |

**Rejected.** It moves the floor problem to a ceiling problem: the low-load presets pile up at the 10.0 cap, and two presets go back to a single band. The floor is handled on the dashboard instead (see the saturation rule below).

## Other options documented, not applied

- **C.** Narrow M14 to 0.10-0.30. It helps the brothers and hurts the match for Michael: a trade-off, not a fix.
- **D.** Branch logistic midpoint 5.5 → 4.5. All eight siblings had careers, but this would also change the counterfactual presets' headline results.

## Calibration frozen

**Longevity calibration stops here.** There are six documented lifespans (two completed, four censored at current age), and they are run through dial profiles that are themselves assumptions. Every further tweak would mostly be fitting the model to my own guesses about those profiles. From here, a change to any range, baseline, bin or profile needs a new reason (a fetched source, or a found error), not a better fit. If one comes, it gets recorded here as a new step.

### Remaining misses, stated plainly

1. **The brothers' profile.** 80.7% of runs for the Jackie / Tito / Marlon profile end before Jackie's and Marlon's current ages, and only 19.3% reach Tito's 65+. In these profiles the only dial difference from Michael is body-image comments, so the model predicts nearly the same lifespan for very different documented lives. Lowering the brothers' discipline from 9 to 7 helped about as much as any parameter change did, so the miss is as much about the profile guess as about the model.
2. **The living-sibling check overall.** About half the runs (51% on average) end before each living sibling's current age. Randy, Rebbie and La Toya sit near 37-48%; Janet is lowest at 13%. The model leans toward shorter lives than this family has had.
3. **Longevity is a conventional score-to-age mapping.** The bins (0-2 / 2-3.5 / 3.5-5 / 5+ → <45 / 45-55 / 55-65 / 65+) are anchored in direction only: 7.0 is an ordinary lifespan for a US man born in 1958. No study gives this mapping. The bands are a way to read the score, not a lifespan estimate.
4. **Acute causes of death aren't modeled.** Michael's death on June 25, 2009 was ruled a homicide (acute propofol intoxication), and his physician was convicted of involuntary manslaughter. The longevity path is a chronic dose-response curve with a wide non-parenting spread. None of it is a claim that the parenting variable explains how or when he died.
5. **Careers can't be ranked the way the record does.** Career is scored from practice volume. Group role, opportunity and talent aren't parenting dials.
6. **Mental health has no sibling check.** The rules allow no inference about anyone's private mental health, so there is nothing to compare against. Actual's mental health stays on the floor: 24.9% of Childhood runs at exactly 0, and 55.1% by the Later stage.

### Note for Phase 4: saturation rule

Wherever a band on page 2 has **more than 20% of runs at exactly 0 or 10**, the page shows "score saturated under these assumptions" next to it. `saturation()` in `model/simulate.py` returns the share and the flag. With the frozen calibration, this applies to the Actual preset's Mental health in every stage: 24.9% in Childhood, rising to 55.1% by Later. No other dimension or preset passes 20%; the next highest is Actual's longevity score, at 6.6% of runs at 0.

## Sanity checks (final)

| Check | Result |
|---|---|
| 1. Actual: Branch C dominates, Branch A near zero | Partly (C 0.546 is the largest; A 0.119) |
| 2. Nurturing: Branch A rises but doesn't swallow everything | Passes (A 0.287; B 0.606 is the largest) |
| 3. Actual mental health clearly below Nurturing | Passes (median 0.77 vs 6.85) |
| No preset above ~95% in any longevity band | Passes (max 89%) |
| Actual puts age 50 in its most likely band (45-55) | **Fails** (<45 is 40%, 45-55 is 30%) |

**Why the age-50 failure is accepted.** This check passed after A and B (63% in 45-55). It failed once E spread the longevity baseline, which moved part of Actual's mass into <45. It's accepted, and not tuned back, for four reasons:
1. Michael's band was never a calibration target. The 45-55 match after A and B was a side effect of the brother correction.
2. His death was an acute event (acute propofol intoxication, ruled a homicide) that the model's chronic longevity pathway doesn't represent. A chronic dose-response curve shouldn't be expected to land on an acute outcome.
3. The 45-55 band still holds 30% of runs, so the documented band isn't ruled out.
4. Calibration is frozen: pulling Actual back toward 45-55 would mean fitting one lifespan through an assumed profile.
