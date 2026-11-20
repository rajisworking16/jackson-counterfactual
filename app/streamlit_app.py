"""Counterfactual: The Jackson Trajectory - dashboard.

Page 1: the documented timeline (no model output).
Scenario bands under stated assumptions, never a prediction.
"""
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "model"))
import simulate as sim  # noqa: E402

PITCH = ("Counterfactual scenario modeling, applied to the most documented childhood in pop history: "
         "change one input (his father's parenting style) and see how the trajectory branches.")
SCOPE = ("Scope: this model covers the parenting variable and its documented downstream effects only. "
         "The criminal allegations are out of scope.")
NOT_A_PREDICTION = "Scenario bands under the stated assumptions, not a prediction."


@st.cache_data
def load_csv(name):
    return pd.read_csv(DATA / name)


# ---------------------------------------------------------------- page 1
def page_timeline():
    st.title("The documented timeline")
    st.markdown(PITCH)
    st.info(SCOPE)
    st.markdown("**Documented events only, no model output.**")

    ev = load_csv("life_events.csv").copy()
    ev["dial_links"] = ev["dial_links"].fillna("").replace("", "none (career or outcome event)")
    self_r, approx = ev["self_report"].eq("yes"), ev["year_approx"].eq("yes")
    ev["record_type"] = "Documented record"
    ev.loc[self_r, "record_type"] = "His own account (self-report)"
    ev.loc[approx, "record_type"] = "Approximate year"
    ev.loc[self_r & approx, "record_type"] = "Self-report, approximate year"

    fig = px.scatter(
        ev, x="year", y="age", color="dial_links", symbol="record_type",
        symbol_map={"Documented record": "circle", "His own account (self-report)": "diamond",
                    "Approximate year": "x", "Self-report, approximate year": "diamond-open"},
        hover_data={"event": True, "source": True, "confidence": True, "year": True, "age": True,
                    "dial_links": True, "record_type": False},
        labels={"year": "Year", "age": "Age", "dial_links": "Parenting dial(s) evidenced",
                "record_type": "Record type"},
        height=520)
    fig.update_traces(marker=dict(size=11))
    fig.update_layout(legend=dict(title=None), margin=dict(t=20))
    st.plotly_chart(fig, width="stretch")
    st.caption("Diamonds mark rows that rest on Michael's own account: high confidence there means he said it, "
               "not that it happened. Crosses mark an approximate year. Hover a point for the event, source and confidence.")

    with st.expander(f"All {len(ev)} events, with sources"):
        st.dataframe(ev[["year", "age", "event", "dial_links", "outcome_links", "self_report",
                         "year_approx", "source", "confidence"]], hide_index=True, width="stretch")


# ---------------------------------------------------------------- page 2
LIVE_RUNS = 2_000
SCORE_DIMS = [d for d in sim.DIMS if d != "Longevity"]  # Longevity is shown as bands only (Rule 5)
BRANCHES = [("A_no_career", "A. No professional music career", "Music stays a gift, not a profession."),
            ("B_late_healthy", "B. Fame with a lighter load", "A career arrives, often later, with less of the fear load."),
            ("C_same_timeline", "C. Same timeline as documented", "Fame on the documented schedule, with the heavier load.")]


@st.cache_data
def load_params():
    return sim.load_parameters(DATA / "parameters.csv")


@st.cache_data(show_spinner="Running 2,000 scenarios...")
def run_engine(dial_values, n=LIVE_RUNS):
    """Cached by dial values. Returns branch means, per-stage bands with saturation, longevity bands."""
    dials = dict(zip(sim.PRESETS["Actual (documented)"], dial_values))
    df, bp = sim.run_preset("Custom", dials, load_params(), n=n)
    rows = []
    for (stage, dim), s in df.melt(id_vars=["stage"], value_vars=SCORE_DIMS, var_name="dim").groupby(["stage", "dim"])["value"]:
        share, flagged = sim.saturation(s)
        rows.append({"stage": stage, "dimension": dim, "median": s.median(), "p10": s.quantile(.1),
                     "p90": s.quantile(.9), "saturated_share": share, "saturated": flagged})
    return bp.mean().to_dict(), pd.DataFrame(rows), sim.longevity_bands(df).iloc[0].to_dict()


def dial_evidence():
    """How many timeline rows evidence each dial (dial_links uses short_name)."""
    links = load_csv("life_events.csv")["dial_links"].fillna("").str.split(", ").explode()
    return links[links != ""].value_counts().to_dict()


def set_preset_dials():
    preset = st.session_state["preset"]
    if preset in sim.PRESETS:
        for dial, v in sim.PRESETS[preset].items():
            st.session_state["dial::" + dial] = v


def mark_custom():
    st.session_state["preset"] = "Custom"


def page_dials():
    st.title("Dials, branches and outcome bands")
    st.markdown("Change the parenting inputs and see how the scenario bands move. Every number on this page is "
                "a band over simulated runs under stated assumptions (page 3), not a prediction about a real life.")
    st.caption(f"Live results use {LIVE_RUNS:,} runs per setting, cached by dial values. "
               "The published results in `data/outputs/` use 10,000 runs.")

    dials_df = load_csv("dials.csv")
    evidence = dial_evidence()
    if "preset" not in st.session_state:
        st.session_state["preset"] = "Actual (documented)"
        set_preset_dials()

    left, right = st.columns([1, 2], gap="large")
    with left:
        st.selectbox("Preset", list(sim.PRESETS) + ["Custom"], key="preset", on_change=set_preset_dials)
        for r in dials_df.itertuples():
            st.slider(r.dial, 0, 10, key="dial::" + r.dial, on_change=mark_custom, help=r.what_it_captures)
            n_rows = evidence.get(r.short_name, 0)
            st.caption(f"Evidenced by {n_rows} timeline row{'s' if n_rows != 1 else ''}.")
            if r.short_name == "Body-image comments":
                st.warning(f"Least-supported input with a large effect: {n_rows} timeline "
                           f"row{'s' if n_rows != 1 else ''} (TIME's paraphrase of the 1993 Oprah interview), yet moving "
                           "it from 2 to 8 shifts median mental health by about 2.2 points in the sensitivity analysis.")

    values = tuple(st.session_state["dial::" + d] for d in sim.PRESETS["Actual (documented)"])
    branches, bands, longevity = run_engine(values)

    with right:
        st.subheader("Career branches")
        cols = st.columns(3)
        for col, (key, label, desc) in zip(cols, BRANCHES):
            col.metric(label, sim.format_prob(branches[key]))
            col.caption(desc)
        st.caption(NOT_A_PREDICTION)

        st.subheader("Outcome bands")
        stage = st.selectbox("Life stage", list(sim.STAGE_DECAY), key="stage")
        b = bands[bands.stage == stage].set_index("dimension").loc[SCORE_DIMS[::-1]].reset_index()
        fig = px.scatter(b, x="median", y="dimension", range_x=[0, 10], height=360,
                         labels={"median": "Score (0-10, higher is better)", "dimension": ""},
                         error_x=b["p90"] - b["median"], error_x_minus=b["median"] - b["p10"])
        fig.update_traces(marker=dict(size=12), hovertemplate="%{y}: median %{x:.1f}<extra></extra>")
        for row in b[b.saturated].itertuples():
            fig.add_annotation(x=10, y=row.dimension, xanchor="right", showarrow=False,
                               text=sim.SATURATION_NOTE, font=dict(size=12))
        fig.update_layout(margin=dict(t=10, l=10))
        st.plotly_chart(fig, width="stretch")
        st.caption("Dot = median; whiskers = p10 to p90 of the runs.")
        for row in b[b.saturated].itertuples():
            st.caption(f"{row.dimension}: {sim.SATURATION_NOTE} "
                       f"({sim.format_prob(row.saturated_share)} of runs at the 0 or 10 limit).")
        st.caption(NOT_A_PREDICTION)

        st.subheader("Longevity (whole life, band probabilities)")
        st.table(pd.DataFrame({"Band": sim.LONGEVITY_LABELS,
                               "Share of runs": [sim.format_prob(longevity[k]) for k in sim.LONGEVITY_LABELS]})
                 .set_index("Band"))
        st.caption("Bands read a 0-10 score through a conventional mapping (page 3); they aren't an age estimate.")
        st.caption(NOT_A_PREDICTION)


PAGES = {"1. Documented timeline": page_timeline, "2. Dials and results": page_dials}


def main():
    st.set_page_config(page_title="The Jackson Trajectory", layout="wide")
    choice = st.sidebar.radio("Page", list(PAGES))
    st.sidebar.caption(SCOPE)
    PAGES[choice]()


main()
