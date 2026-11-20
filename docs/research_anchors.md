# Research anchors

Which published research backs which links in the model, and how strong that backing is. Every source below was fetched and read on 2026-11-19. Where a source couldn't be read, this doc says so instead of citing it from memory.

Link IDs refer to `data/parameters.csv` (built in Phase 2) and `docs/mechanism_map.md`.

## 1. Corporal punishment meta-analyses (Gershoff)

**Gershoff & Grogan-Kaylor (2016), "Spanking and child outcomes: Old controversies and new meta-analyses."** *Journal of Family Psychology* 30(4), 453-469. DOI 10.1037/fam0000191, PMID 27055181.

- Five decades of research, about 160,000 children (PubMed lists 111 effect sizes and 160,927 children).
- Spanking was "significantly linked with 13 of the 17 outcomes they examined, all in the direction of detrimental outcomes."
- It "was not associated with more immediate or long-term compliance."
- Adults spanked more as children were more likely to show antisocial behavior and mental health problems.
- "Both spanking and physical abuse were associated with the same detrimental child outcomes," in the same direction and at nearly the same strength.

The study looked at open-handed spanking, not abuse. What Michael and Joseph each described (a switch, a stick, a belt) sits at the harsher end, so this anchor is conservative for the Actual preset.

Sources read: [UT News, Apr 25, 2016](https://news.utexas.edu/2016/04/25/risks-of-harm-from-spanking-confirmed-by-researchers); [PubMed search listing](https://pubmed.ncbi.nlm.nih.gov/?term=Gershoff+Grogan-Kaylor+2016+spanking+child+outcomes+meta-analyses) (journal, volume, pages, DOI, PMID, effect-size count).

**Gershoff (2002), *Psychological Bulletin*.** Not read this session. The APA press release and Monitor pages came back empty, and PsycNet returned a loading stub. It isn't cited for any number until someone reads it.

*Used for: P01 (Physical discipline → Trauma / fear load). Also supports the direction of M05 (Trauma → Mental health), alongside anchor 2.*

## 2. Adverse Childhood Experiences (ACE) study

**Felitti et al. (1998), "Relationship of childhood abuse and household dysfunction to many of the leading causes of death in adults."** *American Journal of Preventive Medicine* 14(4), 245-258. (Citation as listed in the reference list of Felitti 2002, below. The AJPM page itself only returned a redirect stub.)

- Over 17,000 Kaiser Permanente members in Southern California, 1995 to 1997, two waves. All questions cover the respondent's first 18 years.
- "Study findings show a graded dose-response relationship between ACEs and negative health and well-being outcomes." 12.5% of the sample reported four or more ACEs.
- The 1998 CDC release: the more adverse experiences, the more likely heart disease, cancer, stroke, diabetes and skeletal fractures.
- Felitti (2002): "This graded, dose-response effect is present for all the associations we found." A person with an ACE score of 4 was 390% more likely to have COPD and 460% more likely to be depressed than someone with a score of 0.

Two limits: the sample is mostly middle-class HMO members, and ACEs are counted as yes/no categories, not intensities. Using them on a 0-10 trauma load is a modelling choice, and it's listed in the assumptions register.

Sources read: [CDC, About the CDC-Kaiser ACE Study](https://www.cdc.gov/violenceprevention/aces/about.html); [CDC press release, May 14, 1998](https://archive.cdc.gov/www_cdc_gov/media/pressrel/r980514.htm); [Felitti (2002), *Permanente Journal* 6(1), "Turning Gold into Lead"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6220625).

*Used for: P11 (Discipline → Sleep & physical health), M05 (Trauma → Mental health), M09 (Sleep & physical health → Physical health), M12 (Trauma → Longevity), M13 (Sleep & physical health → Longevity), M14 (Mental health → Longevity).*

## 3. Child-performer outcomes

Thin, and the doc says so. The only peer-reviewed item found is a narrative review, Anderson (2011), *Medical Problems of Performing Artists* 26(3), 146-149, PMID 21987069. Only its PubMed listing could be read. The listing says "child actors appear to have unique psychological needs" and that the paper "makes a case for future research." A 2025 BPS article by a chartered psychologist ([The psychology of child actors](https://bps.org.uk/psychologist/psychology-child-actors)) describes long hours leading to "exhaustion, irritability, and even burnout," but it cites no studies.

Nothing here is strong enough to put a number on a link. The career branch logic (Step 3.3) stays ASSUMPTION, checked against the siblings.

*Used for: context only. No parameter takes the RESEARCH label from this anchor.*

## 4. Sibling calibration method

Nine children grew up in the same house with the same father, but their exposure varied. Michael was lead singer from childhood. Rebbie and La Toya weren't in the group. Randy joined later. Janet was the youngest, and in her own words her father was still her manager. Their documented outcomes are in `data/sibling_outcomes.csv`.

The check: run the model on dial settings that match each sibling's documented exposure. If it produces an outcome band that no sibling at similar exposure resembles, the range is wrong, not the sibling. This is a sanity check, not a measurement: nine people is a tiny sample, and the record is public careers and public statements, not private wellbeing. The comparison is written up in `docs/calibration_notes.md` (Step 3.6).

*Used for: every range, as a check. It's the basis for the links labeled SIBLING CALIBRATION (P04, P13, P14, M01).*

## Relabeled to ASSUMPTION (2026-11-20)

The starter parameter table labeled these links RESEARCH, but none of the anchors above backs them. Pranav decided to relabel all six ASSUMPTION in `data/parameters.csv`. Each note now ends "(was RESEARCH)". If a source is read later, a link can move back to RESEARCH, with the source added to this doc.

| Link | Claimed basis | Status |
|---|---|---|
| P02 Warmth → Trauma | "ACE successors" (warmth as a buffer) | No buffering source read |
| P07 Body-image comments → Self-image | Appearance teasing literature | No source read |
| P09 Warmth → Attachment | Attachment literature | No source read |
| M06 Self-image → Mental health | Body-image literature | No source read |
| M07 Attachment → Mental health | Attachment literature | No source read |
| M10 Attachment → Relationships | Attachment literature | No source read |

The remaining RESEARCH links are P01, P11, M05, M09, M12, M13 and M14, all backed by anchors 1 and 2.
