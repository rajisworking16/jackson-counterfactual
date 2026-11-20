# Project Update: The Jackson Trajectory

**As of:** 2026-11-20 · **Branch:** `main`

A Monte Carlo scenario model that changes one input in Michael Jackson's documented life (his father's parenting style) and maps how the trajectory branches. It's a scenario model, not a prediction. The full plan is in [BUILD_GUIDE.md](BUILD_GUIDE.md).

## Where it stands

**15 of 22 build steps done.** Phases 0 to 3 are complete. Phase 3 finished with the Step 3.6 calibration follow-up, in the commit "Phase 3: calibration follow-up - baseline uncertainty, censored sibling check". Phase 4 (the dashboard) is next.

| Phase | Status | Progress |
|---|---|---|
| 0. Setup | ✅ Done | 2 of 2 steps |
| 1. Research dossier | ✅ Done | 4 of 4 steps |
| 2. Data model | ✅ Done | 3 of 3 steps + review fixes |
| 3. Simulation engine | ✅ Done | 6 of 6 steps + calibration follow-up |
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
| E. Outcome baselines | Fixed 7.0 → drawn per run: 6.0-8.0, Longevity **4.5-8.5** | ASSUMPTION. Non-parenting factors, acute events among them, move lifespan a lot |

Michael's 45-55 share is a side effect of the brother correction, not a target. It was 63% after A and B, and it's 34% after E.

**Censored sibling check.** For the living siblings, the check is the share of runs whose band ends by their current age, which the record has already ruled out. Lower is better. Michael and Tito keep a band match.

| Sibling | Status | Check | After A+B | After E |
|---|---|---|---|---|
| Michael | died at 50 | P(45-55) | 62.9% | 33.8% |
| Tito | died at 70 | P(65+) | 0.2% | 5.7% |
| Jackie | living, 75 | P(ends by 75) ↓ | 99.8% | 94.3% |
| Marlon | living, 69 | P(ends by 69) ↓ | 99.8% | 94.3% |
| Randy | living, 65 | P(ends by 65) ↓ | 36.3% | 59.3% |
| Rebbie | living, 76 | P(ends by 76) ↓ | 34.6% | 59.0% |
| La Toya | living, 70 | P(ends by 70) ↓ | 4.9% | 46.4% |
| Janet | living, 60 | P(ends by 60) ↓ | 0.0% | 16.6% |

E removed the near-certain bands, but it spreads every outcome both ways, so the living-sibling check got worse. The brothers' profile is still the biggest miss.

**Test F (not applied): loads measured from a reference level of 3.** Actual's zero-mental-health share drops from 24.9% to 0%. But Nurturing's p90 goes from 7.67 to 10.00 (at the cap), and two presets go back to 100% in 65+. It moves the problem rather than fixing it.

**Open choice.** 4.5-8.5 is centered on 6.5, not 7.0. A range centered on 7.0 (5.0-9.0) helps the living siblings, but it puts Nurturing at 98.7% in 65+, so it would need widening to around 4.0-10.0. That's Pranav's decision.

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
| Actual (documented) | 50% | 34% | 16% | 1% |
| Strict coach, warm father | <1% | 7% | 36% | 57% |
| Firm but nurturing | <1% | <1% | 14% | 86% |

**Mental health, Childhood** (median, with p10-p90): Actual 0.77 (0.0-2.2), Strict coach 5.21 (4.2-6.2), Nurturing 6.85 (6.0-7.7).

**Sensitivity** (Actual preset: each dial moved 2 → 8. Medians for the scores; longevity as percentage-point shifts in band share)

| Dial | Career | Creative | Mental | Physical | Relationships | Longevity <45 | Longevity 65+ |
|---|---|---|---|---|---|---|---|
| Warmth | +0.86 | +0.79 | +2.93 | +0.99 | +2.05 | −37.0 pp | +11.7 pp |
| Discipline | +4.77 | +2.88 | −2.41 | −1.05 | −0.82 | +40.8 pp | −42.5 pp |
| Body-image comments | 0.00 | −0.11 | −2.23 | −1.73 | −0.35 | +27.1 pp | −6.5 pp |
| Autonomy | +0.82 | +0.39 | +0.39 | 0.00 | +1.00 | −2.6 pp | +0.3 pp |
| Normalcy | 0.00 | 0.00 | 0.00 | +0.62 | 0.00 | −13.3 pp | +2.2 pp |
| Financial control | −0.46 | 0.00 | 0.00 | 0.00 | −0.74 | 0.0 pp | 0.0 pp |

## Sanity checks

| Check | Result |
|---|---|
| 1. Actual: Branch C dominates, Branch A near zero | 🟡 Partly (C 0.546; A 0.119) |
| 2. Nurturing: Branch A rises but doesn't swallow everything | ✅ |
| 3. Actual mental health clearly below Nurturing | ✅ (0.77 vs 6.85) |
| No preset above ~95% in any longevity band | ✅ (max 86%) |

## Basis labels

The 29 links break down as:
- **6 RESEARCH:** P01, P11, M05, M09, M13, M14
- **5 SIBLING CALIBRATION:** P04, P13, P14, M01, M12
- **18 ASSUMPTION**

The fixed numbers (baselines, intercepts, branch logistic, stage decay, bins) are all ASSUMPTION and listed in [mechanism_map.md](mechanism_map.md).

## Open items

- The centering of the longevity baseline range (above).
- Janet's split date: WDET says 1985, while ET (2022) places it before her second album.
- Jermaine's 2011 memoir hasn't been read.
- The age-check cell in `notebooks/01_research_dossier.ipynb` is Pranav's.

## Next: Phase 4, the Streamlit dashboard

1. **Page 1:** the documented timeline.
2. **Page 2:** dials, branch cards and outcome bands. Longevity appears only as band probabilities through `format_prob`, with "not a prediction" under every chart.
3. **Page 3:** the assumptions register: 29 links, the fixed numbers, a calibration summary, limitations and the scope statement.
4. **Run, screenshot, polish.**

## Scope

The model covers the parenting variable and its documented downstream effects only. The criminal allegations are out of scope.
