# Project Update: The Jackson Trajectory

**As of:** 2026-11-20 · **Branch:** `main` · **Latest commit on GitHub:** see `git log` ("Phase 5: pre-read copy fixes")

A Monte Carlo scenario model that changes one input in Michael Jackson's documented life (his father's parenting style) and maps how the trajectory branches. It's a scenario model, not a prediction. The full plan is in [BUILD_GUIDE.md](BUILD_GUIDE.md).

## Where it stands

**21 of 22 build steps done.**
- Phases 0 to 4 are complete: the engine is calibrated and frozen, and the three-page Streamlit dashboard is built, tested and screenshotted.
- In Phase 5, the README and the portfolio drafts are done.
- The one step left is **5.2, the sensitivity read**, which needs 2-3 real readers.

| Phase | Status | Progress |
|---|---|---|
| 0. Setup | ✅ Done | 2 of 2 steps |
| 1. Research dossier | ✅ Done | 4 of 4 steps |
| 2. Data model | ✅ Done | 3 of 3 steps + review fixes |
| 3. Simulation engine | ✅ Done | 6 of 6 steps; calibration frozen |
| 4. Dashboard | ✅ Done | 4 of 4 steps, 16 tests passing |
| 5. Write-up + ship | 🟡 Waiting on readers | 2 of 3 steps (5.1, 5.3); 5.2 needs real readers |

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

## Phase 4: the dashboard

[app/streamlit_app.py](../app/streamlit_app.py) has three pages, all text and charts, with no photos or logos, in the default Streamlit theme. Run it with `streamlit run app/streamlit_app.py`; `?page=2` opens a page directly.

| Page | What it shows |
|---|---|
| 1. Documented timeline | Plotly scatter of all 33 events (year × age), colored by the dial each evidences. Distinct symbols mark self-report and approximate-year rows. Hover shows the event, source and confidence. Pitch, scope statement and "Documented events only, no model output." at the top. The 2009 row is plain |
| 2. Dials and results | A preset selector and 6 sliders. Under each slider, how many timeline rows evidence it; Body-image comments is flagged as the least-supported input with a large effect (1 row). Branch cards, outcome bands (median with p10-p90 whiskers, by stage), and longevity as a band table, all through `format_prob`. The saturation note where more than 20% of runs sit at 0 or 10 (today: Actual's mental health). "Not a prediction" under every chart. Live at 2,000 runs, cached by dial values; published results use 10,000 |
| 3. Assumptions register | Scope first; all 29 links, filterable by basis; the fixed numbers (read from mechanism_map.md); the calibration summary; limitations, with the failed age-50 check and the living-sibling check first; the 2009 outcome in one sober sentence; sources |

**Tests** ([tests/test_app.py](../tests/test_app.py), `python -m pytest tests/`): **16 passing**. They cover:
- every page loading without an exception, and the scope statement on pages 1 and 3
- slider and preset changes moving the branch cards
- no "0%" or "100%" anywhere in rendered text, including with every dial at 0 and every dial at 10
- the saturation note, the not-a-prediction line under every page 2 chart, longevity as bands only, and no death wording on page 2

**Speed:** in a real browser, a slider change updates the cards in about **0.25 s**.

**Screenshots:** [docs/screenshots/](screenshots/) has all three pages on desktop, and pages 1 and 2 at phone width (390 px, no horizontal scroll).

## Phase 4 fixes (commit `46fd9f2`)

- Branch B is now labeled "B. Later fame, lighter load".
- The body-image warning's 2.2-point figure is labeled "(published 10,000-run analysis)". It's true now: `simulate.py` publishes `data/outputs/sensitivity_actual.csv` at 10,000 runs per side, and the figure holds there (−2.23).
- `.streamlit/config.toml` turns off Streamlit's usage statistics.

## Phase 5 so far

- **[README.md](../README.md)** (Step 5.1, about 4 minutes to read). Method first. Findings as bands only:
  - the discipline trade-off (no career goes from 12% to 68% as discipline drops 9 → 2 under Actual's other dials), with the assumptions that drive it
  - the interaction (29% in Nurturing)
  - sensitivity by outcome, with no single "most important dial"

  Then plain limitations (the failed age-50 check first), the 2009 outcome in one sober sentence, scope, how to run it with tests, sources and screenshots. A "How it was built" section notes the AI-assisted implementation and that every design, scope and calibration decision was Pranav's.
- **[docs/portfolio_copy.md](portfolio_copy.md)** (Step 5.3, drafts):
  - portfolio card blurb
  - resume bullet, labeled "add only once live"
  - LinkedIn post, which attaches the real screenshots
  - 60-second interview answer covering where the model fails and why calibration stopped
- **[docs/sensitivity_read.md](sensitivity_read.md)**: a one-page brief for the 2-3 readers, with the one question, links, how to run the app, and a notes table.

## Pre-read copy fixes (committed: "Phase 5: pre-read copy fixes")

| Fix | Status |
|---|---|
| LinkedIn bullet in `portfolio_copy.md` now says "In the model…" and names the assumption behind the 12% → 68% figure (fear-driven practice built much of his skill) | ✅ Done |
| README "The control group" gains one sentence showing the siblings' public views of Joseph vary. It quotes Jackie ("My father was the one who cracked the whip"), Janet ("drove me to be the best that I can") and Michael at Oxford, 2001 ("He pushed me because he loved me"), each checked against its source row | ✅ Done |
| Resume bullet replaced with Pranav's two-sentence version (Monte Carlo model; 33 events, 9-sibling control group, 29 basis-labeled parameters, 10,000 seeded runs; directed AI-assisted implementation, made every calibration call), keeping "add only once live" | ✅ Done |

## Next

1. **Step 5.2, the sensitivity read (hard stop).** Send `docs/sensitivity_read.md` to 2-3 readers, including someone who knows the culture and the fanbase. Fix what they flag, then commit "Phase 5: sensitivity-read fixes".
2. **After that, Pranav's own steps:** the v1.0 tag, repo visibility, the portfolio card going live, and the resume bullet.

## Scope

The model covers the parenting variable and its documented downstream effects only. The criminal allegations are out of scope.
