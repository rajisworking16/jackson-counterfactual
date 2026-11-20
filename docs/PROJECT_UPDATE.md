# Project Update: The Jackson Trajectory

**As of:** 2026-11-20 · **Branch:** `main`

A Monte Carlo scenario model that changes one input in Michael Jackson's documented life (his father's parenting style) and maps how the trajectory branches. It's a scenario model, not a prediction. The full plan is in [BUILD_GUIDE.md](BUILD_GUIDE.md).

## Where it stands

**15 of 22 build steps done.** Phases 0 to 3 are complete. Phase 3 closes with "Phase 3: center longevity baseline, freeze calibration": the longevity baseline is centered on 7.0 and **calibration is frozen**. Phase 4 (the dashboard) is next.

| Phase | Status | Progress |
|---|---|---|
| 0. Setup | ✅ Done | 2 of 2 steps |
| 1. Research dossier | ✅ Done | 4 of 4 steps |
| 2. Data model | ✅ Done | 3 of 3 steps + review fixes |
| 3. Simulation engine | ✅ Done | 6 of 6 steps; calibration frozen |
| 4. Dashboard | ⬜ Next | 0 of 4 steps |
| 5. Write-up + ship | ⬜ Not started | 0 of 3 steps |

## Phase 3: what was built

The engine is [model/simulate.py](../model/simulate.py). Each function was tried first in [notebooks/03_engine_sandbox.ipynb](../notebooks/03_engine_sandbox.ipynb): predict by hand, then run. The notebook is committed with outputs cleared.

| Step | Function | What it does |
|---|---|---|
| 3.1 | `PRESETS`, `load_parameters`, `sample_params` | 3 dial presets; one coefficient per link drawn uniformly from its range |
| 3.2 | `compute_mediators` | 6 dials → 6 mediators (0-10, clipped) |
| 3.3 | `branch_probabilities` | Practice and trauma → Branches A / B / C |
| 3.4 | `compute_outcomes`, `sample_baselines` | Mediators → 6 outcomes per life stage; M15 on Relationships; baselines drawn per run |
| 3.5 | `run_preset`, `summarize`, `longevity_bands`, `sensitivity` | Monte Carlo, seed 42, 10,000 runs; bands; sensitivity on every outcome |
| 3.6 | Sibling calibration, `format_prob` | Sibling profiles checked against the record; display rule |

Every hand prediction matched except one. Longevity at the range midpoints came out 0.96, not 0: an arithmetic slip, written up in the notebook.

## Step 3.6: calibration, in full

The write-up is [calibration_notes.md](calibration_notes.md). The sibling dial profiles are in [data/sibling_profiles.csv](../data/sibling_profiles.csv), all ASSUMPTION, with a basis note per row.

**Changes applied (each approved by Pranav)**

| Change | Before → After | Basis |
|---|---|---|
| A. M12 Trauma → Longevity | 0.35-0.65 → 0.15-0.35 | RESEARCH → SIBLING CALIBRATION (direction still from ACE) |
| B. Longevity bins | 0-3 / 3-5 / 5-7 / 7+ → 0-2 / 2-3.5 / 3.5-5 / 5+ | ASSUMPTION. Anchor: the 7.0 baseline is an ordinary lifespan for a US man born in 1958 (66.6 years, CDC/NCHS), so 65+ has to start below it. The exact cut points are still assumptions |
| Display rule | No probability shown as 0% or 100% | `format_prob` prints "<1%" / ">99%" |
| E. Outcome baselines | Fixed 7.0 → drawn per run: 6.0-8.0, Longevity **4.5-9.5 (centered on 7.0)** | ASSUMPTION. Non-parenting factors, acute events among them, move lifespan a lot. The narrowest centered range that keeps every preset at or under ~95% in any band |

Michael's 45-55 share is a side effect of the brother correction, not a target. It was 63% after A and B, and it's 30% in the final model.

**Choosing the longevity baseline (centered on 7.0, B's anchor)**

| Range | Highest preset band | Michael P(45-55) | Tito P(65+) | Living-sibling avg ↓ |
|---|---|---|---|---|
| 4.5-8.5 (superseded: centered on 6.5) | 86% | 33.8% | 5.7% | 61.7% |
| 5.0-9.0 | 98.7% (fails ~95%) | 36.2% | 13.6% | 51.0% |
| **4.5-9.5 (applied)** | 89% | 29.7% | 19.3% | 51.1% |
| 4.0-10.0 | 82% | 24.9% | 23.4% | 51.2% |

4.5-9.5 is better than the superseded 4.5-8.5 for every living sibling, so it was applied.

**Censored sibling check (final).** For living siblings, the check is the share of runs whose band ends by their current age, which the record has already ruled out. Lower is better.

| Sibling | Status | Check | Final |
|---|---|---|---|
| Michael | died at 50 | P(45-55) | 29.7% |
| Tito | died at 70 | P(65+) | 19.3% |
| Jackie / Marlon | living, 75 / 69 | P(ends by current age) ↓ | 80.7% |
| Randy | living, 65 | ↓ | 47.6% |
| Rebbie | living, 76 | ↓ | 47.2% |
| La Toya | living, 70 | ↓ | 37.0% |
| Janet | living, 60 | ↓ | 13.2% |

**Test F: tested and rejected.** Measuring loads from a reference level of 3 removes Actual's zero floor, but it pushes the low-load presets to the 10.0 cap, and two presets go back to 100% in one band. It moves the floor problem to a ceiling problem.

**Calibration frozen.** Longevity calibration stops here, to avoid fitting six lifespans run through assumed profiles. Remaining misses:
- The brothers' profile (80.7% of runs ruled out).
- About half of the runs end before each living sibling's current age.
- Longevity is a conventional score-to-age mapping, anchored in direction only.

Details are in [calibration_notes.md](calibration_notes.md).

**Birth dates verified** (HELLO!, AOL/Parade): Randy Oct 29, 1961; La Toya May 29, 1956; both already correct in the data.

## Current results (seed 42, 10,000 runs per preset)

**Branch probabilities**

| Preset | A: no career | B: later, healthier | C: same timeline |
|---|---|---|---|
| Actual (documented) | 0.119 | 0.335 | 0.546 |
| Strict coach, warm father | 0.211 | 0.643 | 0.145 |
| Firm but nurturing | 0.287 | 0.606 | 0.107 |

**Longevity bands** (band probabilities only, under these assumptions)

| Preset | <45 | 45-55 | 55-65 | 65+ |
|---|---|---|---|---|
| Actual (documented) | 40% | 30% | 23% | 7% |
| Strict coach, warm father | <1% | 6% | 29% | 65% |
| Firm but nurturing | <1% | <1% | 11% | 89% |

**Mental health, Childhood** (median, with p10-p90): Actual 0.77 (0.0-2.2), Strict coach 5.21 (4.2-6.2), Nurturing 6.85 (6.0-7.7).

**Sensitivity** (Actual preset: each dial moved 2 → 8. Medians for the scores; longevity as percentage-point shifts in band share)

| Dial | Career | Creative | Mental | Physical | Relationships | Longevity <45 | Longevity 65+ |
|---|---|---|---|---|---|---|---|
| Warmth | +0.86 | +0.79 | +2.93 | +0.99 | +2.05 | −30.1 pp | +22.7 pp |
| Discipline | +4.77 | +2.88 | −2.41 | −1.05 | −0.82 | +31.5 pp | −43.8 pp |
| Body-image comments | 0.00 | −0.11 | −2.23 | −1.73 | −0.35 | +21.9 pp | −16.0 pp |
| Autonomy | +0.82 | +0.39 | +0.39 | 0.00 | +1.00 | −2.7 pp | +1.5 pp |
| Normalcy | 0.00 | 0.00 | 0.00 | +0.62 | 0.00 | −12.1 pp | +7.5 pp |
| Financial control | −0.46 | 0.00 | 0.00 | 0.00 | −0.74 | 0.0 pp | 0.0 pp |

## Sanity checks

| Check | Result |
|---|---|
| 1. Actual: Branch C dominates, Branch A near zero | 🟡 Partly (C 0.546; A 0.119) |
| 2. Nurturing: Branch A rises but doesn't swallow everything | ✅ |
| 3. Actual mental health clearly below Nurturing | ✅ (0.77 vs 6.85) |
| No preset above ~95% in any longevity band | ✅ (max 89%) |
| Actual puts age 50 in its most likely band | ❌ Fails (<45 is 40%, 45-55 is 30%). Accepted: the documented band was never a calibration target, and the death was acute, outside the chronic pathway. See calibration_notes.md |

## Basis labels

The 29 links break down as:
- **6 RESEARCH:** P01, P11, M05, M09, M13, M14
- **5 SIBLING CALIBRATION:** P04, P13, P14, M01, M12
- **18 ASSUMPTION**

The fixed numbers (baselines, intercepts, branch logistic, stage decay, bins) are all ASSUMPTION and listed in [mechanism_map.md](mechanism_map.md).

## Open items

- Janet's split date: WDET says 1985, while ET (2022) places it before her second album.
- Jermaine's 2011 memoir hasn't been read.
- The age-check cell in `notebooks/01_research_dossier.ipynb` is Pranav's.

## Next: Phase 4, the Streamlit dashboard

1. **Page 1:** the documented timeline.
2. **Page 2:** dials, branch cards and outcome bands.
   - Longevity appears only as band probabilities, through `format_prob`.
   - "Not a prediction" goes under every chart.
   - **Saturation rule:** wherever a band has more than 20% of runs at exactly 0 or 10, it shows "score saturated under these assumptions" (`saturation()`). Today that applies to Actual's mental health: 24.9% of runs at 0 in Childhood, 55.1% by Later.
3. **Page 3:** the assumptions register: 29 links, the fixed numbers, a calibration summary, limitations and the scope statement.
4. **Run, screenshot, polish.**

## Scope

The model covers the parenting variable and its documented downstream effects only. The criminal allegations are out of scope.
