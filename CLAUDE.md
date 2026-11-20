# CLAUDE.md - Counterfactual: The Jackson Trajectory

Portfolio project for Pranav (Sai Pranav Raj Kandula), MS Business Analytics & AI at UT Dallas. A Monte Carlo scenario model that changes one input in Michael Jackson's documented life (his father's parenting style: harsh/fear-based to firm but nurturing) and maps how the trajectory branches. Repo: `rajisworking16/jackson-counterfactual`, branch `main`.

**The full plan is `docs/BUILD_GUIDE.md`.** Its CURRENT STATUS section says what's done and what's next. Read it at the start of every session.

## Ground rules (the project's credibility; never break these)

1. **Not a prediction.** Outputs are probability bands over scenarios, each labeled with its assumptions. Rewrite any sentence (code comment, README, dashboard text) that claims certainty about an alternate life as a banded scenario.
2. **Source everything about Michael from his own words and the documented record:** *Moonwalk*, his interviews, court records, sibling accounts. Never invent trauma details or private facts.
3. **Joseph stays three-dimensional.** The harshness caused documented harm AND was entangled with the discipline that made the Jackson 5. No cartoon villain.
4. **The criminal allegations are out of scope.** The model covers the parenting variable and its documented downstream effects only. Don't add a 2005 row. State the scope wherever limits are described (README, dashboard page 3).
5. **No death gamification.** The 2009 death is a documented outcome, handled soberly: band probabilities only, never a score, countdown, slider or single predicted age.
6. **Every parameter carries a basis label:** RESEARCH / SIBLING CALIBRATION / ASSUMPTION. No silent numbers. A number without a basis label doesn't ship.

## How to work in this repo

Pranav is learning while he builds. Treat him as a capable collaborator, not a beginner.

- **One step per request.** Do the step named in CURRENT STATUS (or the one he asks for), then stop. Never start the next step or phase on your own.
- **Explain first.** Give the "why" in 2-3 lines before writing code, and end each step with a short "what you just learned" note.
- **Phase 3 is timed to his Python course.** For engine functions, offer to let him write it first and review his version. Draft it yourself only when he asks. Try each function in `notebooks/03_engine_sandbox.ipynb` (predict the output, then run it) before moving it into `model/simulate.py`.
- **Git:** stage and show the diff, then ask before committing. Use the commit message given in the guide for that step. **Never push** unless he says to. Never rewrite history or force-push.
- **Status:** after a step is committed, update CURRENT STATUS in `docs/BUILD_GUIDE.md` (phase table, commits, next actions) and include that edit in the same commit.

## Research rules (Phase 1 and the sibling table)

- Add a `source` only for a page you actually fetched in this session. Never fill a source from memory.
- Every new row goes in with `confidence` set as below and is listed in your reply as **unverified until Pranav checks it**. He verifies each row against its source before it stays.
- If an event can't be sourced, leave the row out. A Low-confidence row gets dropped, not kept.
- Confidence: High = his own words or court/official record; Medium = credible biography or sibling account; Low = widely repeated but thinly sourced (drop it). High on a self-report means "he said it," not "it happened."
- Siblings: documented public record only (careers, their own public statements). No speculation about anyone's private mental health.
- Keep `dial_links` honest: link only dials the event genuinely evidences.

## Parameters and calibration

- `data/parameters.csv` has 28 rows: P01-P14 (dial to mediator) and M01-M14 (mediator to outcome). The mechanism map in `docs/mechanism_map.md` must have the same 28 links.
- Don't change a range, a basis label, the longevity band mapping or the engine's baselines without telling him what and why, and getting a yes. The commit message records the reason.
- **Known issues, left for Step 3.6 on purpose:** Actual-preset Mental health and Longevity scores sit at the 0-10 floor, and 98.6% of Actual runs land in the `<45` longevity band, against the documented age of 50. Don't fix these early or quietly. They get fixed in the calibration pass, with the reasoning written up in `docs/calibration_notes.md`.
- Open gap for Phase 2: `mediators.csv` says Trauma / fear load feeds Relationships, but no parameter row links them. Raise it when Phase 2 starts and let him decide.

## Open decisions (raise these before adding Phase 1 rows)

1. Add a `self_report` column (yes/no) to `life_events.csv`.
2. Split `dial_links` into `dial_links` + `outcome_links` ("career peak", "health pathway" and "longevity outcome" aren't dials).
3. The age-check cell in `notebooks/01_research_dossier.ipynb` is his to write. Don't fill it in.

## Commands

```bash
source .venv/bin/activate              # every session
git status                             # check for uncommitted work first
python model/simulate.py               # Phase 3+: seeded, 10,000 runs
streamlit run app/streamlit_app.py     # Phase 4+
```

## Layout

- `data/`: CSV datasets; every file stays clean enough to show an interviewer. `data/outputs/`: only `outcome_bands.csv`, `branch_probabilities.csv` and `longevity_bands.csv` are committed.
- `notebooks/`: one per phase (00 setup check, 01 dossier, 02 data model, 03 engine sandbox). Commit notebooks with outputs cleared.
- `model/simulate.py`: the engine (03 notebook text says `engine.py`; the name is `simulate.py`).
- `app/streamlit_app.py`: the 3-page dashboard (Phase 4).
- `docs/`: BUILD_GUIDE.md, research_anchors.md, mechanism_map.md, calibration_notes.md.

## Writing style (README, docs, dashboard text, commit messages)

Direct, plain, human. No em-dashes. No buzzwords or hype. Contractions are fine. Quantify where the data allows. Never fabricate facts.
