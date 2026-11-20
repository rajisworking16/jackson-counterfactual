"""Counterfactual: The Jackson Trajectory - simulation engine.
Dials -> mediators -> branch probabilities -> outcome bands.
Monte Carlo over basis-labeled parameter ranges. NOT a prediction:
every output is a band over scenarios under stated assumptions.
"""
import numpy as np
import pandas as pd

SEED = 42
N_RUNS = 10_000


PRESETS = {
    "Actual (documented)": {
        "Physical discipline intensity": 9, "Emotional warmth & affection": 3,
        "Autonomy granted": 2, "Normalcy (school peers play)": 2,
        "Body-image comments (negative)": 8, "Parental financial control": 9},
    "Strict coach, warm father": {
        "Physical discipline intensity": 5, "Emotional warmth & affection": 6,
        "Autonomy granted": 4, "Normalcy (school peers play)": 4,
        "Body-image comments (negative)": 4, "Parental financial control": 6},
    "Firm but nurturing (counterfactual)": {
        "Physical discipline intensity": 2, "Emotional warmth & affection": 8,
        "Autonomy granted": 7, "Normalcy (school peers play)": 7,
        "Body-image comments (negative)": 1, "Parental financial control": 4},
}


def load_parameters(path="data/parameters.csv"):
    return pd.read_csv(path)


def sample_params(params, rng):
    """One draw: a coefficient per link, uniform in [low, high]."""
    return dict(zip(params.link_id, rng.uniform(params.low, params.high)))


def compute_mediators(dials, c):
    """Dials (0-10) -> six mediators (0-10, clipped). Practice is a LEVEL;
    the other five are LOADS (higher = heavier). Intercepts 0.25 (practice)
    and 0.55 (attachment) are ASSUMPTION baselines."""
    d = {k: v / 10 for k, v in dials.items()}
    trauma = 10 * (c["P01"] * d["Physical discipline intensity"]
                   + c["P02"] * d["Emotional warmth & affection"]
                   + c["P03"] * d["Body-image comments (negative)"])
    practice = 10 * (0.25
                     + c["P04"] * d["Physical discipline intensity"]
                     + c["P05"] * d["Emotional warmth & affection"]
                     + c["P06"] * d["Autonomy granted"])
    self_image = 10 * (c["P07"] * d["Body-image comments (negative)"]
                       + c["P08"] * d["Emotional warmth & affection"])
    attachment = 10 * (0.55
                       + c["P09"] * d["Emotional warmth & affection"]
                       + c["P10"] * d["Autonomy granted"])
    sleep = 10 * (c["P11"] * d["Physical discipline intensity"]
                  + c["P12"] * d["Normalcy (school peers play)"])
    fin_delay = 10 * (c["P13"] * d["Parental financial control"]
                      + c["P14"] * d["Autonomy granted"])
    clip = lambda x: float(np.clip(x, 0, 10))
    return {"Practice hours & skill acquisition": clip(practice),
            "Trauma / fear load": clip(trauma),
            "Self-image & body perception": clip(self_image),
            "Attachment & trust in adults": clip(attachment),
            "Sleep & physical health": clip(sleep),
            "Financial independence timing": clip(fin_delay)}


def branch_probabilities(med):
    """Career branches from practice (P) and trauma (T). Logistic midpoint 5.5,
    scale 1.2 and the 0.15-0.9 clip on C's share are ASSUMPTION."""
    P, T = med["Practice hours & skill acquisition"], med["Trauma / fear load"]
    fame = 1 / (1 + np.exp(-(P - 5.5) / 1.2))
    a = 1 - fame
    c_share = float(np.clip(T / 10, 0.15, 0.9))
    return {"A_no_career": a, "B_late_healthy": fame * (1 - c_share),
            "C_same_timeline": fame * c_share}


STAGE_DECAY = {"Childhood": 0.0, "Teen": 0.1, "Young adult": 0.2, "Peak": 0.35, "Later": 0.5}

# ASSUMPTION (Step 3.6, option E): each outcome's baseline is drawn per run instead of
# fixed at 7.0. The spread stands for everything outside the parenting variable.
# Longevity gets a wider range: non-parenting factors such as acute events (his own
# death among them) move lifespan a lot. Centered on 7.0, the B anchor (an ordinary
# lifespan for a US man born in 1958). 4.5-9.5 is the narrowest centered range that
# keeps every preset at or under ~95% in any band. Calibration is frozen here.
BASELINE_RANGE = (6.0, 8.0)
LONGEVITY_BASELINE_RANGE = (4.5, 9.5)
OUTCOMES = ["Career attainment", "Creative output & risk-taking", "Mental health",
            "Physical health & appearance changes", "Relationships & family closeness", "Longevity"]


def sample_baselines(rng):
    """One baseline per outcome for this run, drawn independently."""
    out = {}
    for dim in OUTCOMES:
        lo, hi = LONGEVITY_BASELINE_RANGE if dim == "Longevity" else BASELINE_RANGE
        out["BASE::" + dim] = rng.uniform(lo, hi)
    return out


def compute_outcomes(med, c, branch):
    """Mediators -> six outcomes (0-10, higher = better), per life stage.
    7.0 baseline (ASSUMPTION). Load -> outcome coefficients are positive and
    subtracted; practice is added around a midpoint of 5. Baselines come from
    sample_baselines() in c; a missing one falls back to 7.0 (the midpoint tests)."""
    m = med
    b = lambda dim: c.get("BASE::" + dim, 7.0)
    career = b("Career attainment") + c["M01"] * (m["Practice hours & skill acquisition"] - 5) \
                 - c["M02"] * m["Financial independence timing"]
    if branch == "A_no_career":
        career = min(career, 3.0)          # normal-life ceiling on this dimension
    creative = b("Creative output & risk-taking") + c["M03"] * (m["Practice hours & skill acquisition"] - 5) \
                   - c["M04"] * m["Trauma / fear load"]
    if branch == "A_no_career":
        creative = min(creative, 4.5)      # music as a gift, not a profession
    mental = b("Mental health") - c["M05"] * m["Trauma / fear load"] \
                 - c["M06"] * m["Self-image & body perception"] \
                 - c["M07"] * m["Attachment & trust in adults"]
    physical = b("Physical health & appearance changes") - c["M08"] * m["Self-image & body perception"] \
                   - c["M09"] * m["Sleep & physical health"]
    relations = b("Relationships & family closeness") - c["M10"] * m["Attachment & trust in adults"] \
                    - c["M11"] * m["Financial independence timing"] \
                    - c["M15"] * m["Trauma / fear load"]
    longevity = b("Longevity") - c["M12"] * m["Trauma / fear load"] \
                    - c["M13"] * m["Sleep & physical health"] \
                    - c["M14"] * (b("Mental health") - mental)
    clip = lambda x: float(np.clip(x, 0, 10))
    base = {"Career attainment": clip(career), "Creative output & risk-taking": clip(creative),
            "Mental health": clip(mental), "Physical health & appearance changes": clip(physical),
            "Relationships & family closeness": clip(relations), "Longevity": clip(longevity)}
    staged = {}
    for stage, decay in STAGE_DECAY.items():
        row = dict(base)
        for dim in ("Mental health", "Physical health & appearance changes"):
            row[dim] = clip(row[dim] - decay * m["Trauma / fear load"] * 0.3)
        staged[stage] = row
    return staged  # Longevity is whole-life: the same value at every stage


def run_preset(name, dials, params, n=N_RUNS, seed=SEED):
    rng = np.random.default_rng(seed)
    rows, branches = [], []
    for _ in range(n):
        c = {**sample_params(params, rng), **sample_baselines(rng)}
        med = compute_mediators(dials, c)
        bp = branch_probabilities(med)
        branches.append(bp)
        branch = rng.choice(list(bp), p=list(bp.values()))
        staged = compute_outcomes(med, c, branch)
        for stage, outs in staged.items():
            rows.append({"preset": name, "branch": branch, "stage": stage, **outs})
    return pd.DataFrame(rows), pd.DataFrame(branches)


def p10(s):
    return s.quantile(0.10)


def p90(s):
    return s.quantile(0.90)


DIMS = ["Career attainment", "Creative output & risk-taking", "Mental health",
        "Physical health & appearance changes", "Relationships & family closeness", "Longevity"]


def summarize(df):
    return df.groupby(["preset", "stage"])[DIMS].agg(["median", p10, p90])


# ASSUMPTION: how the 0-10 longevity score maps to lifespan bands. No study gives
# this mapping; it is a stated convention, listed in the assumptions register.
# Step 3.6: was [0, 3, 5, 7, 10]. The score can't exceed the 7.0 baseline, so the
# old top band (7+) was only reachable with zero load; bins now span reachable scores.
LONGEVITY_BINS = [0, 2, 3.5, 5, 10.0001]
LONGEVITY_LABELS = ["<45", "45-55", "55-65", "65+"]


def longevity_bands(df):
    """Share of runs in each lifespan band, per preset. Longevity is whole-life,
    so one stage is enough. Reported as band probabilities, never a single age."""
    whole = df[df["stage"] == "Later"].reset_index(drop=True)
    band = pd.cut(whole["Longevity"], bins=LONGEVITY_BINS, labels=LONGEVITY_LABELS,
                  right=False, include_lowest=True)
    return pd.crosstab(whole["preset"], band, normalize="index").reindex(columns=LONGEVITY_LABELS, fill_value=0.0)


SCORE_SHIFTS = {"career_shift": "Career attainment", "creative_shift": "Creative output & risk-taking",
                "mental_health_shift": "Mental health", "physical_health_shift": "Physical health & appearance changes",
                "relationships_shift": "Relationships & family closeness"}


def sensitivity(dials, params, n=2000, seed=SEED):
    """One-at-a-time: move each dial 2 -> 8 and measure the shift in every outcome dimension.
    Score dimensions: shift in the median (0-10). Longevity (Rule 5: band probabilities only,
    never a score): shift in the share of runs in the <45 and 65+ bands, in percentage points."""
    out = {}
    for dial in dials:
        lo, hi = dict(dials), dict(dials)
        lo[dial], hi[dial] = 2, 8
        d_lo, _ = run_preset("lo", lo, params, n=n, seed=seed)
        d_hi, _ = run_preset("hi", hi, params, n=n, seed=seed)
        row = {k: d_hi[dim].median() - d_lo[dim].median() for k, dim in SCORE_SHIFTS.items()}
        b_lo, b_hi = longevity_bands(d_lo).iloc[0], longevity_bands(d_hi).iloc[0]
        row["longevity_under45_pp"] = 100 * (b_hi["<45"] - b_lo["<45"])
        row["longevity_65plus_pp"] = 100 * (b_hi["65+"] - b_lo["65+"])
        out[dial] = row
    return pd.DataFrame(out).T.sort_values("mental_health_shift", key=abs, ascending=False)


SATURATION_THRESHOLD = 0.20
SATURATION_NOTE = "score saturated under these assumptions"


def saturation(scores, threshold=SATURATION_THRESHOLD):
    """Phase 4 display rule: share of runs pinned at 0 or 10, and whether page 2
    must show SATURATION_NOTE next to that band (more than 20% of runs pinned)."""
    share = float(((scores == 0) | (scores == 10)).mean())
    return share, share > threshold


def format_prob(p):
    """Display rule (Step 3.6): never show a band as 0% or 100%. Model shares are
    scenario bands under stated assumptions, not certainties."""
    if p < 0.01:
        return "<1%"
    if p > 0.99:
        return ">99%"
    return f"{p:.0%}"


if __name__ == "__main__":
    import os
    os.makedirs("data/outputs", exist_ok=True)
    params = load_parameters()
    all_df, branch_rows = [], []
    for name, dials in PRESETS.items():
        df, bp = run_preset(name, dials, params)
        all_df.append(df)
        branch_rows.append({"preset": name, **bp.mean().to_dict()})
    results = pd.concat(all_df, ignore_index=True)
    results.to_csv("data/outputs/simulation_results.csv", index=False)
    pd.DataFrame(branch_rows).to_csv("data/outputs/branch_probabilities.csv", index=False)
    summarize(results).to_csv("data/outputs/outcome_bands.csv")
    longevity_bands(results).to_csv("data/outputs/longevity_bands.csv")
    print(pd.DataFrame(branch_rows).round(3).to_string(index=False))
    print(longevity_bands(results).map(format_prob).to_string())
    print("Scenario bands under the stated assumptions, not a prediction.")
    print("Saved to data/outputs/")
