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


PAGES = {"1. Documented timeline": page_timeline}


def main():
    st.set_page_config(page_title="The Jackson Trajectory", layout="wide")
    choice = st.sidebar.radio("Page", list(PAGES))
    st.sidebar.caption(SCOPE)
    PAGES[choice]()


main()
