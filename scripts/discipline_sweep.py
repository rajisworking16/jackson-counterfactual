"""Discipline trade-off sweep (README Finding 1).

Keeps every Actual-preset dial fixed and moves only Physical discipline intensity
through 9, 7, 5, 3, 2. Each level runs 10,000 times with seed 42, so every level
sees the same random draws (common random numbers) and the differences come from
the dial alone. Branch shares are the mean branch probabilities across runs, the
same way data/outputs/branch_probabilities.csv is built.

Run from the repo root:  python scripts/discipline_sweep.py
Writes data/outputs/discipline_sweep.csv. Scenario bands under the stated
assumptions, not a prediction.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "model"))

import pandas as pd  # noqa: E402
import simulate as sim  # noqa: E402

LEVELS = [9, 7, 5, 3, 2]
DIAL = "Physical discipline intensity"
OUT = ROOT / "data" / "outputs" / "discipline_sweep.csv"


def sweep(params, levels=LEVELS, n=sim.N_RUNS, seed=sim.SEED):
    rows = []
    for level in levels:
        dials = dict(sim.PRESETS["Actual (documented)"])
        dials[DIAL] = level
        _, bp = sim.run_preset(f"discipline {level}", dials, params, n=n, seed=seed)
        mean = bp.mean()
        rows.append({"discipline": level,
                     "branch_a_share": mean["A_no_career"],
                     "branch_b_share": mean["B_late_healthy"],
                     "branch_c_share": mean["C_same_timeline"]})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    params = sim.load_parameters(ROOT / "data" / "parameters.csv")
    df = sweep(params)
    os.makedirs(OUT.parent, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(df.round(3).to_string(index=False))
    print("Scenario bands under the stated assumptions, not a prediction.")
    print(f"Saved to {OUT.relative_to(ROOT)}")
