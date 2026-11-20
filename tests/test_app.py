"""Dashboard tests (Step 4.4). Run from the repo root: python -m pytest tests/"""
import re
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "app" / "streamlit_app.py")
PAGES = ["1. Documented timeline", "2. Dials and results", "3. Assumptions register"]
NOT_A_PREDICTION = "Scenario bands under the stated assumptions, not a prediction."
BAD_PERCENT = re.compile(r"(?<![\d.<>])(0|100)(\.0+)?\s?%")
DIALS = ["Physical discipline intensity", "Emotional warmth & affection", "Autonomy granted",
         "Normalcy (school peers play)", "Body-image comments (negative)", "Parental financial control"]


def open_page(page):
    at = AppTest.from_file(APP, default_timeout=120).run()
    at.sidebar.radio[0].set_value(page).run()
    return at


def rendered_text(at):
    """All visible text: prose elements, metric labels/values, and table cells."""
    out = []
    for kind in ("title", "header", "subheader", "markdown", "caption", "info", "warning", "success", "error"):
        out += [str(e.value) for e in getattr(at, kind)]
    out += [f"{m.label} {m.value}" for m in at.metric]
    for t in list(at.table) + list(at.dataframe):
        out += [str(v) for v in t.value.to_numpy().ravel()] + [str(c) for c in t.value.columns]
    return out


def branch_values(at):
    return [m.value for m in at.metric]


@pytest.mark.parametrize("page", PAGES)
def test_page_loads_without_exception(page):
    at = open_page(page)
    assert not at.exception, [e.value for e in at.exception]
    assert at.title, "every page has a title"


@pytest.mark.parametrize("page", [PAGES[0], PAGES[2]])
def test_scope_statement_on_pages_1_and_3(page):
    at = open_page(page)
    assert any("criminal allegations are out of scope" in i.value for i in at.info)


def test_slider_change_updates_branch_cards():
    at = open_page(PAGES[1])
    before = branch_values(at)
    assert len(before) == 3
    at.slider(key="dial::Physical discipline intensity").set_value(3).run()
    assert not at.exception
    after = branch_values(at)
    assert after != before, "moving the discipline dial should move the branch cards"
    assert at.selectbox(key="preset").value == "Custom"


def test_preset_change_resets_sliders_and_cards():
    at = open_page(PAGES[1])
    actual = branch_values(at)
    at.selectbox(key="preset").set_value("Firm but nurturing (counterfactual)").run()
    assert not at.exception
    assert at.slider(key="dial::Physical discipline intensity").value == 2
    assert branch_values(at) != actual


@pytest.mark.parametrize("page", PAGES)
def test_no_zero_or_hundred_percent_on_any_page(page):
    at = open_page(page)
    hits = [t for t in rendered_text(at) if BAD_PERCENT.search(t)]
    assert not hits, hits


@pytest.mark.parametrize("level", [0, 10])
def test_no_zero_or_hundred_percent_at_extreme_dials(level):
    at = open_page(PAGES[1])
    for d in DIALS:
        at.slider(key="dial::" + d).set_value(level)
    at.run()
    assert not at.exception
    hits = [t for t in rendered_text(at) if BAD_PERCENT.search(t)]
    assert not hits, hits


def test_saturation_note_shown_for_actual_mental_health():
    at = open_page(PAGES[1])
    assert any("Mental health: score saturated under these assumptions" in c.value for c in at.caption)


def test_every_chart_on_page_2_carries_the_not_a_prediction_line():
    at = open_page(PAGES[1])
    n = sum(c.value == NOT_A_PREDICTION for c in at.caption)
    assert n >= 3, f"branch cards, band chart and longevity table each need the line; found {n}"


def test_longevity_shown_only_as_band_probabilities():
    at = open_page(PAGES[1])
    table = at.table[0].value
    assert list(table.index) == ["<45", "45-55", "55-65", "65+"]
    assert all(re.fullmatch(r"<1%|>99%|\d{1,2}%", v) for v in table["Share of runs"])


def test_page_2_has_no_death_wording():
    at = open_page(PAGES[1])
    text = " ".join(rendered_text(at)).lower()
    for word in ("death", "died", " dies", " die ", "countdown", "lifespan prediction"):
        assert word not in text, word
