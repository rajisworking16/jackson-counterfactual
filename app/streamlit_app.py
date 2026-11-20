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


# ---------------------------------------------------------------- page 3
@st.cache_data
def md_table(doc, heading):
    """Read the first markdown table under a '## heading' in docs/<doc> into a DataFrame."""
    lines = (ROOT / "docs" / doc).read_text().splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.strip() == "## " + heading)
    rows = []
    for ln in lines[start + 1:]:
        if ln.startswith("## "):
            break
        if ln.startswith("|"):
            rows.append([c.strip() for c in ln.strip().strip("|").split("|")])
        elif rows:
            break
    header, body = rows[0], [r for r in rows[2:]]
    return pd.DataFrame(body, columns=header)


def page_register():
    st.title("Assumptions register")
    st.info(SCOPE)
    st.markdown("Every number the model uses is listed here, with where it comes from. "
                "**RESEARCH** = a published study backs the direction and size. **SIBLING CALIBRATION** = the size "
                "was checked against the nine siblings' documented outcomes. **ASSUMPTION** = a stated judgment "
                "with a wide range. Most links are ASSUMPTION, and that's stated plainly.")

    st.header("The 29 links")
    params = load_params()
    bases = sorted(params["basis"].unique())
    pick = st.multiselect("Filter by basis", bases, default=bases, key="basis_filter")
    shown = params[params["basis"].isin(pick)]
    st.caption(f"Showing {len(shown)} of {len(params)} links. "
               + ", ".join(f"{b}: {int((params.basis == b).sum())}" for b in bases) + ".")
    st.dataframe(shown.rename(columns={"link_id": "link", "from_node": "from", "to_node": "to"}),
                 hide_index=True, width="stretch", height=38 + 35 * len(shown))

    st.header("Fixed numbers that aren't links")
    st.dataframe(md_table("mechanism_map.md", "Fixed numbers that aren't links"), hide_index=True, width="stretch")

    st.header("Calibration against the siblings (frozen)")
    st.markdown(
        "Sibling-like dial profiles (ASSUMPTION, in `data/sibling_profiles.csv`) were run through the engine and "
        "compared with the documented record: public careers, public statements and lifespan to date.\n\n"
        "**Applied (approved):**\n"
        "- **A.** M12 (trauma → longevity) narrowed from 0.35-0.65 to 0.15-0.35, now SIBLING CALIBRATION. "
        "Trauma reached longevity twice, directly and through mental health.\n"
        "- **B.** Longevity bins re-spanned to 0-2 / 2-3.5 / 3.5-5 / 5+. Anchor: the 7.0 baseline stands for an "
        "ordinary lifespan for a US man born in 1958 (66.6 years, CDC/NCHS), so 65+ starts below it.\n"
        "- **E.** Outcome baselines drawn per run (6.0-8.0; longevity 4.5-9.5, centered on 7.0) for everything "
        "outside the parenting variable.\n"
        "- **Display rule.** No probability is shown at either extreme: below 1% reads \"<1%\" and above 99% reads "
        "\">99%\". Bands with more than 20% of runs at a limit are marked as saturated.\n\n"
        "**Tested and rejected:** C (narrow M14: trades one sibling's match for another's), D (lower the branch "
        "midpoint: would move the counterfactual headline results), F (reference-level loads: moves the floor "
        "problem to a ceiling problem).\n\n"
        "**Frozen.** Longevity calibration stopped here, to avoid fitting six lifespans run through assumed profiles.")

    st.header("Limitations")
    st.markdown(
        "1. **The documented age-50 check fails.** Under the Actual preset, the most likely band is <45 (40% of runs); "
        "45-55, where the documented age sits, holds 30%. It passed before baseline uncertainty was added and was "
        "never a calibration target, so it isn't tuned back.\n"
        "2. **About half the runs are ruled out for each living sibling.** On average 51% of runs end before a living "
        "sibling's current age (Jackie and Marlon 81%, Randy 48%, Rebbie 47%, La Toya 37%, Janet 13%). The model "
        "leans toward shorter lives than this family has had.\n"
        "3. **The brothers' profile is the largest miss.** Same rehearsal regime as Michael; the model can't tell "
        "their documented lives apart from his.\n"
        "4. **Longevity is a conventional score-to-age mapping**, anchored in direction only. The bands are a way to "
        "read a score, not a lifespan estimate.\n"
        "5. **No counterfactual data exists.** The bands are structured judgment anchored to research and to nine "
        "siblings' public record, not measurement. One life, one family, one era.\n"
        "6. **Career is scored from practice volume.** Group role, opportunity and talent aren't parenting dials.\n"
        "7. **Mental health has no sibling check.** The project draws no inference about anyone's private mental "
        "health, so the Actual preset's floor (about a quarter of runs at 0) can't be tested against anyone.")
    st.markdown("**The 2009 outcome.** Michael Jackson died on June 25, 2009, of acute propofol intoxication; the "
                "coroner ruled it a homicide and his physician was convicted of involuntary manslaughter, an acute "
                "cause that sits outside what the model's chronic longevity pathway represents.")

    st.header("Sources")
    st.markdown(
        "**Research anchors** (details in `docs/research_anchors.md`):\n"
        "- Gershoff & Grogan-Kaylor (2016), *Journal of Family Psychology*: spanking linked with 13 of 17 detrimental "
        "outcomes across about 160,000 children, and not with better compliance "
        "([UT News](https://news.utexas.edu/2016/04/25/risks-of-harm-from-spanking-confirmed-by-researchers)).\n"
        "- The CDC-Kaiser ACE study (Felitti et al., 1998): a graded dose-response between childhood adversity and adult "
        "health ([CDC](https://www.cdc.gov/violenceprevention/aces/about.html)).\n"
        "- US male life expectancy at birth, 1958: 66.6 years "
        "([CDC/NCHS](https://data.cdc.gov/api/views/w9j2-ggv5/rows.csv)).\n\n"
        "**Primary sources on Michael and the family:**\n"
        "- *Moonwalk* (1988), as quoted by [CBS News/AP](https://www.cbsnews.com/news/joe-jackson-complicated-relationship-with-his-children/) "
        "and [Yahoo Entertainment](https://www.yahoo.com/lifestyle/not-easy-firing-father-michael-jacksons-complicated-relationship-late-father-joe-222713803.html).\n"
        "- The Oprah interview (February 10, 1993), via [TIME](https://time.com/archive/6722459/peter-pan-speaks) and "
        "[NPR](https://www.tpr.org/2018-06-27/joe-jackson-strict-manager-and-father-to-pop-royalty-dead-at-89).\n"
        "- The Oxford Union speech (2001), via [Salon](https://salon.com/2011/03/08/10_year_time_capsule_michael_jackson_oxford_invincible).\n"
        "- Coroner's ruling (August 28, 2009), via [ABC News](https://abcnews.com/Entertainment/MichaelJackson/story?id=8433380); "
        "the physician's conviction (November 7, 2011), via [ABA Journal](https://abajournal.com/news/article/conrad_murray_guilty_involuntary_manslaughter_death_michael_jackson).\n"
        "- Sibling accounts: La Toya on [CNN](https://transcripts.cnn.com/TRANSCRIPTS/1106/21/pmt.01.html) (2011); Janet and Randy "
        "via [Entertainment Tonight](https://www.etonline.com/node/178497) (2022); Jackie via "
        "[The Irish Times / Guardian](https://www.irishtimes.com/culture/music/the-jacksons-it-was-michael-s-body-and-he-did-what-he-wanted-to-look-how-he-wanted-to-look-1.4530020) (2021).\n\n"
        "Every row of `data/life_events.csv` and `data/sibling_outcomes.csv` carries its own source and URL.")
    st.caption(NOT_A_PREDICTION)


PAGES = {"1. Documented timeline": page_timeline, "2. Dials and results": page_dials,
         "3. Assumptions register": page_register}


def main():
    st.set_page_config(page_title="The Jackson Trajectory", layout="wide")
    names = list(PAGES)
    try:  # ?page=1|2|3 opens a page directly (shareable links, screenshots)
        start = min(max(int(st.query_params.get("page", 1)) - 1, 0), len(names) - 1)
    except ValueError:
        start = 0
    choice = st.sidebar.radio("Page", names, index=start)
    st.sidebar.caption(SCOPE)
    PAGES[choice]()


main()
