"""Engine unit tests for model/simulate.py. Run from the repo root: python -m pytest tests/"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("simulate", ROOT / "model" / "simulate.py")
sim = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sim)

PRACTICE = "Practice hours & skill acquisition"
TRAUMA = "Trauma / fear load"
DIALS = list(sim.PRESETS["Actual (documented)"])


@pytest.fixture(scope="module")
def params():
    return sim.load_parameters(ROOT / "data" / "parameters.csv")


def mediators(practice, trauma):
    base = {k: 5.0 for k in ("Self-image & body perception", "Attachment & trust in adults",
                             "Sleep & physical health", "Financial independence timing")}
    return {PRACTICE: practice, TRAUMA: trauma, **base}


# branch_probabilities

@pytest.mark.parametrize("practice", [0, 2.5, 5.5, 8, 10])
@pytest.mark.parametrize("trauma", [0, 3, 7, 10])
def test_branch_probabilities_sum_to_one(practice, trauma):
    bp = sim.branch_probabilities(mediators(practice, trauma))
    assert set(bp) == {"A_no_career", "B_late_healthy", "C_same_timeline"}
    assert sum(bp.values()) == pytest.approx(1.0, abs=1e-12)
    assert all(0 <= v <= 1 for v in bp.values())


@pytest.mark.parametrize("trauma, share", [(0, 0.15), (1, 0.15), (10, 0.90), (9.5, 0.90), (5, 0.50)])
def test_c_share_clipped_to_015_090(trauma, share):
    bp = sim.branch_probabilities(mediators(6.0, trauma))
    fame = bp["B_late_healthy"] + bp["C_same_timeline"]
    assert bp["C_same_timeline"] / fame == pytest.approx(share)


# sample_params

def test_sample_params_draws_inside_ranges(params):
    rng = np.random.default_rng(sim.SEED)
    lo = dict(zip(params.link_id, params.low))
    hi = dict(zip(params.link_id, params.high))
    for _ in range(2000):
        c = sim.sample_params(params, rng)
        assert set(c) == set(params.link_id)
        for k, v in c.items():
            assert lo[k] <= v <= hi[k], (k, v, lo[k], hi[k])


# reproducibility

def test_run_preset_is_reproducible_with_seed_42(params):
    dials = sim.PRESETS["Actual (documented)"]
    df1, bp1 = sim.run_preset("Actual", dials, params, n=1000, seed=42)
    df2, bp2 = sim.run_preset("Actual", dials, params, n=1000, seed=42)
    pd.testing.assert_frame_equal(bp1, bp2)
    pd.testing.assert_frame_equal(df1, df2)


def test_run_preset_differs_with_another_seed(params):
    dials = sim.PRESETS["Actual (documented)"]
    _, bp42 = sim.run_preset("Actual", dials, params, n=200, seed=42)
    _, bp7 = sim.run_preset("Actual", dials, params, n=200, seed=7)
    assert not bp42.equals(bp7)


# compute_mediators

@pytest.mark.parametrize("level", [0, 10])
@pytest.mark.parametrize("draw", ["low", "high", "random"])
def test_compute_mediators_clipped_at_extreme_dials(params, level, draw):
    dials = {d: level for d in DIALS}
    if draw == "random":
        rng = np.random.default_rng(sim.SEED)
        draws = [sim.sample_params(params, rng) for _ in range(500)]
    else:
        draws = [dict(zip(params.link_id, params[draw]))]
    for c in draws:
        med = sim.compute_mediators(dials, c)
        assert len(med) == 6
        assert all(0 <= v <= 10 for v in med.values()), med


# compute_outcomes

def test_branch_a_caps_career_and_creative(params):
    c = dict(zip(params.link_id, params.high))
    c.update({"BASE::" + d: 8.0 for d in sim.OUTCOMES})
    med = mediators(practice=10, trauma=0)
    med["Financial independence timing"] = 0.0
    capped = sim.compute_outcomes(med, c, "A_no_career")
    uncapped = sim.compute_outcomes(med, c, "B_late_healthy")
    for stage in sim.STAGE_DECAY:
        assert capped[stage]["Career attainment"] == pytest.approx(3.0)
        assert capped[stage]["Creative output & risk-taking"] == pytest.approx(4.5)
        # the caps only bite because the same inputs score higher off branch A
        assert uncapped[stage]["Career attainment"] > 3.0
        assert uncapped[stage]["Creative output & risk-taking"] > 4.5


def test_branch_a_caps_hold_across_random_draws(params):
    rng = np.random.default_rng(sim.SEED)
    dials = sim.PRESETS["Firm but nurturing (counterfactual)"]
    for _ in range(500):
        c = {**sim.sample_params(params, rng), **sim.sample_baselines(rng)}
        staged = sim.compute_outcomes(sim.compute_mediators(dials, c), c, "A_no_career")
        for row in staged.values():
            assert row["Career attainment"] <= 3.0
            assert row["Creative output & risk-taking"] <= 4.5


# format_prob

@pytest.mark.parametrize("p, expected", [
    (0.0, "<1%"), (0.004, "<1%"), (0.0099, "<1%"),
    (1.0, ">99%"), (0.996, ">99%"), (0.9901, ">99%"),
    (0.01, "1%"), (0.119, "12%"), (0.5, "50%"), (0.99, "99%"),
])
def test_format_prob_known_values(p, expected):
    assert sim.format_prob(p) == expected


def test_format_prob_never_zero_or_hundred():
    for p in np.linspace(0, 1, 100_001):
        assert sim.format_prob(p) not in ("0%", "100%"), p


# saturation

def test_saturation_flags_more_than_20_percent_pinned():
    scores = pd.Series([0.0] * 15 + [10.0] * 10 + [5.0] * 75)  # 25% pinned
    share, flagged = sim.saturation(scores)
    assert share == pytest.approx(0.25)
    assert flagged


def test_saturation_not_flagged_at_or_below_20_percent():
    at_threshold = pd.Series([0.0] * 20 + [5.0] * 80)
    assert sim.saturation(at_threshold) == (pytest.approx(0.20), False)
    near_edges = pd.Series([0.001, 9.999] * 50)  # close to the edges, not on them
    assert sim.saturation(near_edges) == (0.0, False)
