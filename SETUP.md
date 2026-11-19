# MJ Counterfactual Project — Complete Setup Guide

**Project:** Jackson Counterfactual — a Monte Carlo scenario model of Michael Jackson's life trajectory under one changed input: a nurturing father instead of a harsh one.
**Owner:** Sai Pranav Raj Kandula · **Stack:** Python (pandas, NumPy), Streamlit, Plotly
**Companion doc:** `MJ_Counterfactual_Project_Prompt_and_Build_Guide.md` (the full project spec — model design, dials, branches, ethics guardrails). This guide is the SETUP: workspace, Git, GitHub, and the step-by-step working plan.

---

## 1. What "setup" means here

By the end of this guide you will have:
1. A project folder on your machine with the full structure already built.
2. A Git repository initialized with the first commit done.
3. A GitHub repo (`jackson-counterfactual`) under your account (rajisworking16) with the project pushed to it.
4. The starter datasets already in place (dials, life events spine, sibling table skeleton).
5. A phase-by-phase plan so every work session is just: open the folder, pick the next step, build.

Status on Muse's side: the scaffold is ALREADY BUILT and committed in Muse's workspace (`~/workspace/jackson-counterfactual/`). When you create your folder in Claude, you are recreating the same structure on your side — the automated script in §3 does it in one paste. Both copies start identical; GitHub becomes the shared home once you push.

---

## 2. Prerequisites (one-time, ~10 minutes)

You need three things on the machine where you'll work:

1. **Python 3.11 or newer** — check: `python3 --version`
2. **Git** — check: `git --version`
3. **GitHub CLI (gh)** — optional but recommended; it makes repo creation one command. Check: `gh --version`. Install from https://cli.github.com if missing.

If any check fails, install that one item and re-check. Nothing else is needed — pandas/NumPy/Streamlit/Plotly install into the project's own virtual environment in §3.

---

## 3. Automated workspace setup (one paste)

Open a terminal in the folder where you want the project to live, and paste this whole block. It creates the folder structure, a Python virtual environment, installs the libraries, writes the starter files, initializes Git, and makes the first commit.

```bash
# ---- Jackson Counterfactual: automated setup ----
PROJECT=jackson-counterfactual
mkdir -p $PROJECT/data $PROJECT/model $PROJECT/app $PROJECT/docs
cd $PROJECT

# Python environment + libraries
python3 -m venv .venv
source .venv/bin/activate
pip install --quiet --upgrade pip
printf "pandas\nnumpy\nstreamlit\nplotly\n" > requirements.txt
pip install --quiet -r requirements.txt

# Starter datasets (same content as Muse's scaffold)
cat > data/dials.csv << 'CSV'
dial,actual_documented,counterfactual_preset,what_it_captures
Physical discipline intensity,9,2,"Belt/switch at rehearsals, per Michael's own accounts"
Emotional warmth & affection,3,8,"Praise, comfort, being encouraged vs. fear"
Autonomy granted,2,7,"Choices about career, friends, rest, saying no"
Normalcy (school peers play),2,7,"Regular schooling, neighborhood friends, unstructured play"
Body-image comments (negative),8,1,"Teasing about his nose/appearance, per his accounts"
Parental financial control,9,4,"Father as manager controlling money/decisions into adulthood"
CSV

cat > data/life_events.csv << 'CSV'
year,age,event,dial_links,source,confidence
1958,0,"Born Aug 29, Gary, Indiana; father a steel-mill crane operator",,,
1964,6,"Jackson 5 formed; father's rigorous fear-based rehearsal regime begins","Discipline, Warmth",,
1968,10,"Motown audition; family relocates to Los Angeles","Autonomy, Normalcy",,
1969,11,"I Want You Back hits #1; childhood becomes full-time work","Normalcy, Financial control",,
1978,20,"The Wiz; meets Quincy Jones",Autonomy,,
1979,21,"Off the Wall - first real creative-control push",Autonomy,,
1982,24,Thriller - career peak,career peak,,
1984,25,"Pepsi commercial scalp burn - documented start of pain-medication exposure",health pathway,,
1988,29,"Moonwalk publishes his own account of the beatings and fear; buys Neverland","Warmth, Normalcy",,
1993,34,"Oprah interview: describes crying from loneliness, fear of his father, vomiting when he saw him","Discipline, Warmth",,
2009,50,"Dies June 25, 2009 (propofol; physician later convicted)",longevity outcome,,
CSV

cat > data/sibling_outcomes.csv << 'CSV'
sibling,birth_year,exposure_notes,career_path,public_wellbeing_markers,source
Rebbie,1950,"Left the family home earliest; most private life",,,
Jackie,1951,,,,
Tito,1953,,,,
Jermaine,1954,,,,
La Toya,1956,,,,
Marlon,1957,,,,
Michael,1958,"Highest exposure: lead singer, focal point of the rehearsal regime",,,
Randy,1961,,,,
Janet,1966,"Youngest; a somewhat different later-era Joe; steered her own career from age 18",,,
CSV

cat > data/outcome_dimensions.csv << 'CSV'
dimension,what_it_scores,scored_per
Career attainment,"Professional success reached under the scenario",life-stage
Creative output & risk-taking,"Volume and boldness of creative work",life-stage
Mental health,"Psychological wellbeing markers",life-stage
Physical health & appearance changes,"Health trajectory incl. appearance-related interventions",life-stage
Relationships & family closeness,"Trust, attachment, family bonds",life-stage
Longevity,"Lifespan outcome band",whole life
CSV

cat > data/mediators.csv << 'CSV'
mediator,driven_by_dials,feeds_outcomes
Practice hours & skill acquisition,"Discipline, Warmth, Autonomy","Career attainment, Creative output"
Trauma / fear load,"Discipline, Warmth, Body-image comments","Mental health, Relationships, Longevity"
Self-image & body perception,"Body-image comments, Warmth","Mental health, Physical health & appearance changes"
Attachment & trust in adults,"Warmth, Autonomy","Relationships & family closeness, Mental health"
Sleep & physical health,"Discipline, Normalcy","Physical health, Longevity"
Financial independence timing,"Financial control, Autonomy","Career attainment, Relationships"
CSV

cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.venv/
venv/
.env
.DS_Store
.streamlit/secrets.toml
EOF

touch model/.gitkeep app/.gitkeep

# Git: initialize + first commit
git init
git add -A
git commit -m "Phase 0: project scaffold - data schemas, starter datasets, structure"
echo "SETUP DONE - you are in: $(pwd)"
```

**Verify it worked** (run these; all should succeed):
```bash
ls data/            # dials.csv life_events.csv mediators.csv outcome_dimensions.csv sibling_outcomes.csv
git log --oneline   # shows the Phase 0 commit
python -c "import pandas, numpy, streamlit, plotly; print('libraries OK')"
```

Every future session starts with two commands:
```bash
cd jackson-counterfactual
source .venv/bin/activate
```

---

## 4. GitHub repo creation + first push

### Option A — GitHub CLI (fastest, one-time sign-in)

```bash
gh auth login          # choose GitHub.com, HTTPS, sign in as rajisworking16
gh repo create jackson-counterfactual --public --source=. --remote=origin --push
```
That single second command creates the repo under your account, links it as `origin`, and pushes the Phase 0 commit. Done.

### Option B — Website (if gh is not installed)

1. Go to https://github.com/new — sign in as rajisworking16.
2. Repository name: `jackson-counterfactual`. Description: "Monte Carlo counterfactual scenario model — one changed input (parenting style) in a documented life." Public. Do NOT check "Add a README" (we already have files).
3. Create repository, then in your project terminal:
```bash
git remote add origin https://github.com/rajisworking16/jackson-counterfactual.git
git branch -M main
git push -u origin main
```

### After the first push — the daily Git habit

Every work session ends with:
```bash
git add -A
git commit -m "Phase N: <what you built, in plain words>"
git push
```
Small, frequent commits. The commit history is itself portfolio evidence — an interviewer can watch the project being built properly.

---

## 5. Folder map — what lives where

| Path | What it's for | Phase |
|---|---|---|
| `data/dials.csv` | The 6 parenting dials: documented actual vs counterfactual preset | Done (Phase 0) |
| `data/life_events.csv` | The documented life spine; grows to 30–40 verified events | Phase 1 |
| `data/sibling_outcomes.csv` | The control group: 9 siblings, exposure + outcomes | Phase 2 |
| `data/mediators.csv` | The 6 mediating variables (dials act through these) | Phase 2 |
| `data/outcome_dimensions.csv` | The 6 scored outcomes | Phase 2 |
| `model/` | The Monte Carlo simulation engine | Phase 3 |
| `app/` | The Streamlit dashboard | Phase 4 |
| `docs/` | Research dossier, mechanism map, assumptions register | Phases 1–4 |
| `SETUP.md` | This guide (keep a copy in the repo root) | — |
| `README.md` | The public project write-up | Phase 5 |

---

## 6. The build plan — step by step

Work the phases in order. Each phase lists its steps and the prompt to paste to Claude at its start (from the spec's starter prompts). Your rule in every phase: **you drive and write; Claude drafts in parallel; Muse reviews.**

### Phase 0 — Setup ✅ (this guide)
- [ ] Run the §3 script (or confirm Muse's scaffold)
- [ ] Verify the three checks
- [ ] Create the GitHub repo (§4) and push

### Phase 1 — Research dossier (no code)
*Starter prompt:* "Help me build the research dossier: a table of Michael's documented life events (year, age, event, which parenting dial it connects to, source). Start with the 15 most load-bearing events. I will verify each one against a source before we keep it."
- [ ] Fill `source` + `confidence` for the 11 starter rows in `life_events.csv`
- [ ] Extend to 30–40 events
- [ ] Write `docs/research_anchors.md`: Gershoff meta-analyses (2002; 2016), ACE study (Felitti 1998), child-performer literature — one short paragraph each, in your own words
- [ ] Commit + push: "Phase 1: research dossier"

### Phase 2 — Data model (spreadsheet-level thinking, no engine yet)
*Starter prompt:* "Help me design the CSV schemas for this model: life_events, sibling_outcomes, dials, outcome_dimensions. Show me the columns and 3 example rows each, then I will fill them."
- [ ] Fill `sibling_outcomes.csv` — exposure notes, career path, wellbeing markers per sibling
- [ ] Draw the mechanism map (dials → mediators → outcomes) as a one-page diagram in `docs/`
- [ ] For each dial→mediator and mediator→outcome link, write the range and its basis: RESEARCH / SIBLING CALIBRATION / ASSUMPTION
- [ ] Commit + push: "Phase 2: data model + mechanism map"

### Phase 3 — Simulation engine (Python — timed to your Python lessons)
*Starter prompt:* "Help me build the simulation engine: dials -> mediating variables -> outcome dimensions, with each link as a range, sampled by Monte Carlo (10,000 runs). Write it one function at a time and explain each."
- [ ] `model/engine.py`: one function per link, predict-first, tiny pieces
- [ ] Branch node: A (no professional career) / B (fame later, healthier) / C (same timeline, different interior) — probabilities driven by the mediators
- [ ] Presets: Actual / Strict-coach-warm-father / Fully nurturing / free sliders
- [ ] Sensitivity output: which dial moves outcomes most
- [ ] Seeded runs (fixed random seed) so results are reproducible
- [ ] Commit + push after each working function

### Phase 4 — Streamlit dashboard
*Starter prompt:* "Help me build the Streamlit dashboard: page 1 the real timeline, page 2 the dials and branch results, page 3 the assumptions register. One page at a time."
- [ ] Page 1: the real timeline (Plotly)
- [ ] Page 2: dial sliders, branch cards, outcome bands
- [ ] Page 3: assumptions register + sources (this page is what makes it serious)
- [ ] Run it: `streamlit run app/app.py`
- [ ] Commit + push: "Phase 4: dashboard"

### Phase 5 — Write-up & portfolio
*Starter prompt:* "Help me write the project README and portfolio blurb: method first, findings second, limitations stated plainly, no certainty claims about an alternate life."
- [ ] README: method → findings → limitations
- [ ] Portfolio card + resume bullet (from the spec §7 — add the bullet only once it's live)
- [ ] Sensitivity read by 2–3 trusted people before publishing anything public

---

## 7. How we work together (the standing rhythm)

- **You** create the folder in Claude and drive every step — you write the code and fill the data. That's where the learning is.
- **Claude** drafts in parallel: dossier rows, sibling-table research, README drafts, one function at a time in Phase 3.
- **Muse (me)** owns: architecture decisions, model-design review, code review of what you wrote, keeping the phases in order, and the portfolio/resume framing at the end. Bring each phase's output back here before moving to the next.
- **Pace:** Phases 1–2 fit train-ride-sized chunks. Phase 3 waits until your Python lessons are a few steps further (loops, functions) — we time it to the lessons, not ahead of them. Sunday anchor slots for the bigger pieces. No deadline; applications and interview prep stay ahead of this project.
- **Git rule:** commit + push at the end of every session, even a small one.

## 8. Guardrails (from the spec — they travel with the project)

- This is a scenario model, not a prediction and not a claim about a real alternate life. The write-up says exactly what the model does and does not show.
- Documented facts only in the dossier; every event carries a source and a confidence level. Folklore stays out.
- Every parameter range cites its basis (RESEARCH / SIBLING CALIBRATION / ASSUMPTION). No silent numbers.
- The 2009 death is handled as a longevity data point, factually and without spectacle.
- Allegations outside the parenting question are out of scope for this project.

---

## 9. Your first session (30–45 minutes)

1. Create the project folder in Claude; run the §3 setup script there (or copy Muse's scaffold).
2. Run the three verification checks.
3. Create the GitHub repo (§4, Option A if you can) and push.
4. Open `data/life_events.csv`, look at the 11 starter rows, and pick the first 3 you'll source in Phase 1.
5. End the session the right way: `git add -A && git commit -m "Phase 0 complete" && git push`.
6. Tell Muse "Phase 0 done" — and we start Phase 1 together, step by step.
