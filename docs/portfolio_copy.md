# Portfolio copy (drafts)

Drafts for the portfolio card, resume, LinkedIn and interviews. None of this goes public until the sensitivity read (Step 5.2) is done and its fixes are in.

## Portfolio card

**Title:** Counterfactual Scenario Modeling: "The Jackson Trajectory"

**Blurb:** A Monte Carlo scenario model that changes one input in a documented life, parenting style, and maps how the trajectory branches. Nine siblings serve as a control group, every one of the 29 parameters carries a basis label, and every assumption is published, including where the model fails. Python, NumPy, Streamlit.

## Resume bullet (add only once live)

> Designed and validated a Monte Carlo scenario model (Python, NumPy, Streamlit) of how one changed input, parenting style, branches a documented life: 33 sourced events, a 9-sibling control group, 29 basis-labeled parameters, 10,000 seeded runs. Directed AI-assisted implementation and made every calibration call, including freezing it to avoid overfitting.

## LinkedIn post

Attach the real dashboard screenshots, untouched: `docs/screenshots/page2_dials_results_desktop.png` first, then `page3_assumptions_register_desktop.png`.

> What happens to a life if you change one input?
>
> I built a scenario model to practice the kind of what-if analysis companies use for pricing, policy and risk. I picked a case with an unusually rich record: Michael Jackson's childhood, documented in his own words, and nine siblings who grew up in the same house with the same father.
>
> The model changes one thing, his father's parenting style, and runs 10,000 simulations. Each run draws every effect size from a range. Each range is labeled: backed by published research, checked against the siblings, or a stated assumption. Most are assumptions, and the dashboard says so.
>
> What it shows, as ranges under those assumptions:
> - In the model, lowering discipline alone raises the share of runs with no music career from 12% to 68%, because the model assumes fear-driven practice built much of his skill. Add warmth and autonomy, and it's 29%.
> - No single dial matters most. Discipline drives career and longevity; warmth drives mental health and relationships.
>
> Where it falls short, and I think that's the more useful part:
> - It fails a basic check: Michael's actual lifespan band isn't the model's most likely one.
> - It can't tell him apart from his brothers.
> - I stopped calibrating after one pass, because more tuning would have meant fitting six lifespans to my own guesses.
>
> It's a scenario model, not a prediction. The assumptions register lists every number.
>
> Python · NumPy · Monte Carlo simulation · sensitivity analysis · Streamlit. Implementation was AI-assisted; the design and every calibration call were mine.
>
> [link to the repo]

## 60-second interview answer

> I wanted to practice what-if modeling on a case where the evidence was rich enough to check against. Michael Jackson's childhood is documented in his own words, and his eight siblings grew up under the same father with different exposure, so they work as a rough control group.
>
> The model turns six parenting dials into mediators like practice hours and fear load, then into career branches and outcome bands, across 10,000 seeded runs. Every one of the 29 links has a range and a label: research, sibling calibration or assumption.
>
> The main finding is a trade-off. Lowering discipline cuts the fear load but also cuts practice, so the no-career share rises, unless warmth and autonomy hold practice up.
>
> Where it fails: under the actual dials, his documented lifespan band isn't the most likely one, and the model can't tell him apart from his brothers, who lived much longer. I calibrated once against the siblings and then froze it. Six lifespans run through profiles I'd guessed isn't enough data to keep tuning on. More tuning would have looked better and meant less.
>
> The part I'd point to is the assumptions register: every number, where it comes from, and what I'd never claim from it.
