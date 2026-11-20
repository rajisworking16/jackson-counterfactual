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
