# Calibration notes (Step 3.6)

This file records how the model was checked against the Jackson siblings, what didn't match, which parameters changed and why. It's dated 2026-11-20. The engine is seeded at 42 and runs 10,000 times per profile.

The point of the check: nine children grew up in the same house with the same father, and their exposure varied. If the model gives a sibling-like exposure an outcome that no sibling resembles, the range is wrong, not the sibling. This is a sanity check, not a measurement. It's eight people (Jermaine is left out, see below), and the record covers public careers, public statements and lifespan to date, not private wellbeing.

## Sibling dial profiles (ASSUMPTION)

No source gives anyone's dial values, so each profile is a judgment built from that sibling's exposure record in `data/sibling_outcomes.csv`.

Order of the dials: discipline, warmth, autonomy, normalcy, body-image comments, financial control.

| Profile | Dials | Why |
|---|---|---|
| Michael | 9, 3, 2, 2, 8, 9 | The Actual preset. Lead singer from childhood; his own accounts of beatings and of being called ugly |
| Jackie / Tito / Marlon | 9, 3, 2, 2, 3, 9 | Same rehearsal regime and management (Joseph managed them until 1983). No documented body-image teasing |
| Randy | 6, 4, 4, 5, 3, 8 | Joined later (official member 1976); "my parents were a lot more lenient" with the youngest |
| Janet | 5, 3, 5, 6, 3, 7 | "He was very tough", "You call me Joseph"; managed by her father until 1985, at 19 |
| Rebbie | 6, 3, 5, 6, 2, 3 | Not in the group; solo career from 1974 |
| La Toya | 5, 4, 3, 5, 2, 6 | Not in the group; "a disciplinarian", "one spanking" (2011); her father pushed the family name onto her album |

Jermaine is excluded (`use_in_calibration = no (proxy)`), because his self-direction date is only a stand-in.

## What the starter model produced

| Profile | Longevity <45 / 45-55 / 55-65 / 65+ | Documented |
|---|---|---|
| Michael (Actual) | 98.7% / 1.3% / 0 / 0 | Died at 50 → 45-55 |
| Jackie / Tito / Marlon | 81.8% / 18.2% / 0 / 0 | Tito died in 2024 at 70; Jackie and Marlon still perform → 65+ |
| Randy | 1.2% / 79.4% / 19.3% / 0 | About 65 (birth year unverified) → 65+ |
| Janet | 0.1% / 69.2% / 30.8% / 0 | 60 → at least 55-65 so far |
| Rebbie | 1.0% / 82.1% / 16.9% / 0 | 76 → 65+ |
| La Toya | 0 / 34.0% / 66.0% / 0 | About 70 (birth year unverified) → 65+ |

Two problems showed up:
1. **Under the Actual preset, the model couldn't reproduce the documented life.** Only 1.3% of runs put Michael in the 45-55 band.
2. **The 65+ band was out of reach.** Outcome scores can't go above the 7.0 baseline, and the old top band started at exactly 7. A run only reached 65+ when every load was zero, so no sibling profile could get there, even though five of the six have a sibling who did.

## Changes applied (approved by Pranav, 2026-11-20)

| Change | Before | After | Basis | Reason |
|---|---|---|---|---|
| **A. M12** Trauma / fear load → Longevity | 0.35-0.65, RESEARCH | **0.15-0.35, SIBLING CALIBRATION** | The direction still comes from ACE dose-response; the size now comes from the siblings | Trauma reached longevity twice: directly through M12, and through mental health (M05 → M14). Brothers with exposure close to Actual lived past 65 |
| **B. Longevity bins** (score → band) | 0-3 / 3-5 / 5-7 / 7+ | **0-2 / 2-3.5 / 3.5-5 / 5+** | ASSUMPTION (still a convention) | The old top band could only be reached at zero load. The new bins cover the scores runs actually produce |
| **Display rule** | n/a | No model probability is ever shown as 0% or 100%; `format_prob` prints "<1%" / ">99%" | n/a | Under A and B, the Nurturing preset sits at the top of the score range in every run. "100%" would read as a certainty claim (Rule 1). The published CSVs keep the raw shares as data; every display goes through `format_prob` |

## After the changes

| Profile | Longevity <45 / 45-55 / 55-65 / 65+ | Matches the record? |
|---|---|---|
| Michael (Actual) | 26.1% / **62.9%** / 11.0% / <1% | ✅ The documented band is the most likely one |
| Jackie / Tito / Marlon | 2.3% / 50.9% / 46.6% / 0.2% | ✗ Still short: all three lived past 65 |
| Randy | <1% / <1% / 36.3% / **63.7%** | ✅ |
| Janet | <1% / <1% / 19.3% / **80.7%** | ✅ Consistent so far (she's 60) |
| Rebbie | <1% / <1% / 34.6% / **65.4%** | ✅ |
| La Toya | <1% / <1% / 4.8% / **95.2%** | ✅ |

The preset results that go on the dashboard:

| Preset | <45 | 45-55 | 55-65 | 65+ |
|---|---|---|---|---|
| Actual (documented) | 26% | 63% | 11% | <1% |
| Strict coach, warm father | <1% | <1% | 4% | 96% |
| Firm but nurturing | <1% | <1% | <1% | >99% |

**Under these assumptions.** The Nurturing preset's ">99%" is a property of the model, not a finding. Its loads are near zero, so every run lands near the top score. Read it as "this preset removes the load the model counts", not as a statement about a real life.

The branch probabilities, mental health, career and relationships results are unchanged by A and B, because both touch longevity only. Sanity checks 2 and 3 still pass. Check 1 still only partly passes: Branch A is 0.119 for Actual.

## Options documented but not applied

- **C. Narrow M14 (mental health → longevity) to 0.10-0.30.** It moves the brothers' 65+ share from 0.2% to 2.7%, but drops Michael's 45-55 share from 63% to 55%. That's a trade-off, not a fix.
- **D. Branch logistic midpoint from 5.5 to 4.5.** All eight siblings had professional careers, and this halves the "no career" probability everywhere. Not applied: it would also change the counterfactual presets' headline results, and the family's careers may say more about the family business than about practice volume.
- **E. Baseline drawn per run (6.0-8.0) instead of a fixed 7.0.** This would stand for everything outside the parenting variable. It removes the flat 7.00 ceiling on mental health (Nurturing's p90 becomes 7.7) and would need its own approval.

## What the model still can't do

- **Tell Michael from his brothers.** In these profiles the only dial difference is body-image comments, so the model predicts nearly the same lives for very different documented lives. Pushing the brothers toward 65+ would mean fitting the model to profiles that are themselves guesses. Lowering the brothers' discipline from 9 to 7 moves their 65+ share from 0.2% to 5.4%, so the gap is as sensitive to that guess as to any parameter.
- **Model an acute cause of death.** Michael's death on June 25, 2009 was ruled a homicide: acute propofol intoxication, with his physician later convicted of involuntary manslaughter. The model's longevity path is a chronic dose-response curve. The 45-55 band now being the most likely is a check that the model isn't wildly off. It isn't a claim that the parenting variable explains how or when he died.
- **Rank careers the way the record does.** Career is scored from practice volume. Group role, opportunity and talent aren't parenting dials. So the model gives Rebbie (8.06) nearly the same median career score as Michael (8.07), and Janet (7.40) one of the lowest. The record says otherwise.
- **Check mental health.** No permitted evidence exists: the rules allow no inference about anyone's private mental health. The Actual preset's mental-health floor stays as an ASSUMPTION-driven result: 21.5% of Childhood runs score exactly 0.

## Sanity checks after calibration

| Check | Result |
|---|---|
| 1. Actual: Branch C dominates, Branch A near zero | Partly (C 0.546 is the largest; A 0.119) |
| 2. Nurturing: Branch A rises but doesn't swallow everything | Passes (A 0.284; B 0.608 is the largest) |
| 3. Actual mental health clearly below Nurturing | Passes (median 0.79 vs 6.91) |
| Calibration: Actual puts age 50 in its most likely band (45-55) | Passes (62.9%) |
