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
