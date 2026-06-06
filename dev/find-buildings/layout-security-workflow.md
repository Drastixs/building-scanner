# Privacy-Preserving Layout Analysis Workflow

Last checked: 2026-06-06

## Objective

Study how residential layouts support legibility, privacy, circulation and
defensible-space principles using licensed research datasets. The workflow is
for comparative design research. It must not identify occupied buildings,
produce site-specific vulnerability reports or recommend ways to bypass access
controls.

## 1. Define the research question

Use a falsifiable, design-level question, for example:

- Does a transitional space between entrance and living area improve visual
  privacy?
- How does circulation depth differ between compact and large apartments?
- Which plan features reduce conflict between resident, guest and service paths?

Pre-register the population, metrics, exclusions and expected direction of each
hypothesis. Treat CPTED as a design framework, not as proof that a plan prevents
crime.

## 2. Acquire and govern data

1. Select sources from [datasets.md](datasets.md).
2. Save the terms, release identifier, checksum and retrieval date.
3. Keep raw files outside the public repository.
4. Strip addresses, coordinates, listing IDs and identifying imagery.
5. Assign random internal IDs and prohibit reverse lookup.
6. Split by source building before augmentation to prevent leakage.

Create a dataset card and model card. Document excluded samples and why they
were excluded.

## 3. Normalize plans

Convert each plan into:

- closed room polygons;
- door and opening segments;
- normalized room labels;
- one graph node per occupiable or circulation space;
- one graph edge per traversable opening;
- an exterior/root node connected only to legitimate entrances.

Validate geometry automatically:

- no self-intersecting polygons;
- doors touch the spaces they connect;
- room areas and opening widths are plausible;
- disconnected components are flagged;
- units and scale are known or marked unknown.

Manually audit a stratified sample from every source. Report parser accuracy
separately from downstream model accuracy.

## 4. Compute spatial features

Use a room-access graph for topology and
[depthmapX](https://github.com/SpaceGroupUCL/depthmapX) for visibility or
space-syntax analysis. Its official repository describes it as GPLv3,
multi-platform spatial network analysis software. The
[depthmapX introductory tutorial](https://www.spacesyntax.online/software-and-manuals/depthmap/tutorial/)
includes a building-analysis path.

Useful plan-level features:

| Feature | Interpretation |
| --- | --- |
| Entrance-to-room depth | Number or weighted cost of transitions from exterior |
| Integration/closeness | How centrally accessible a space is in the graph |
| Choice/betweenness | How often a space lies on shortest routes |
| Connectivity | Directly connected neighboring spaces |
| Visual integration | Visibility-based centrality from a VGA grid |
| Isovist area/occlusivity | Visible extent and boundary complexity from a point |
| Route overlap | Shared edges among resident, guest and service route classes |
| Privacy gradient | Change from public to private room labels along paths |
| Dead-end ratio | Share of circulation nodes with only one onward connection |

Do not turn these metrics into a universal “security score.” Keep individual
measures visible because high integration can aid wayfinding while reducing
privacy, and low integration can create isolation.

## 5. Add a CPTED design rubric

Use a published CPTED guide, such as the
[Virginia DCJS CPTED handbook](https://www.dcjs.virginia.gov/sites/dcjs.virginia.gov/files/training-events/8139/cpted-handbook-v4-20170627.pdf),
to define reviewer questions around:

- natural surveillance;
- natural access control;
- territorial reinforcement;
- maintenance/image;
- activity support.

Translate principles into observable, non-site-specific labels. Examples include
whether an entrance has a transition zone, whether common circulation has
overlook from occupied spaces, and whether public-to-private transitions are
legible. Use at least two trained reviewers, measure agreement and adjudicate
disagreements.

## 6. Train and evaluate

Recommended sequence:

1. Establish simple graph-statistic and linear-model baselines.
2. Train a room-graph model only if it materially improves the registered task.
3. Balance or weight plan types, source datasets and size bands.
4. Evaluate on a held-out dataset to expose geographic domain shift.
5. Report confidence intervals, calibration and performance by subgroup.
6. Perform ablations for geometry, semantic labels and visibility features.

Avoid using “crime risk” as a target unless a qualified research team has lawful,
ethically reviewed outcome data and a defensible causal design. Layout alone is
not a reliable proxy for security outcomes.

## 7. Human design review

For each proposed layout modification, have architects assess:

- fire egress and accessibility implications;
- daylight, ventilation and usable area;
- resident privacy and dignity;
- wayfinding and visitor experience;
- operational and maintenance impact;
- whether the recommendation merely moves risk elsewhere.

AI output should be a comparison with stated tradeoffs, not an autonomous
approval or compliance decision.

## 8. Publish safely

Publish:

- aggregate distributions and confidence intervals;
- synthetic or heavily abstracted examples;
- normalized room graphs without source identifiers;
- code, schemas, tests and reproducible metric definitions;
- limitations, failed hypotheses and dataset biases.

Do not publish:

- addresses or links between records and occupied properties;
- detailed access-control, staff-only or surveillance layouts;
- ranked lists of vulnerable buildings;
- per-building attack paths or bypass recommendations;
- source files where redistribution is not expressly permitted.

## Reproducible project layout

```text
project/
  configs/             dataset and experiment configuration
  data_cards/          provenance, terms and bias records
  schemas/             normalized geometry/graph contracts
  src/ingest/          source-specific parsers
  src/geometry/        validation and normalization
  src/features/        graph and visibility metrics
  src/models/          baselines and learned models
  tests/               parser, geometry and metric tests
  reports/             aggregate, non-identifying outputs
```

## First experiment

Start with a small, auditable experiment:

1. Sample 500 licensed apartment plans from one dataset.
2. Normalize room polygons, doors and adjacency.
3. Hand-check 50 plans.
4. Compare entrance-to-bedroom depth, entrance visibility and route overlap.
5. Test whether a vestibule or hall is associated with reduced direct visibility
   into private rooms, controlling for plan area and room count.
6. Replicate on a second dataset before drawing a design conclusion.

This validates the data and metrics before investing in a generative model.
