# Anonymized Plan Analysis Report Template

Use this template for a study of 30 anonymized or synthetic plans. Duplicate
the per-plan section for Plan 01 through Plan 30, then complete the aggregate
section. Record neutral design observations only; do not infer real-world
security outcomes from layout data.

## Study Metadata

- Study title:
- Report version:
- Analysis date:
- Authors/reviewers:
- Number of plans included:
- Inclusion and exclusion criteria:
- Registered research questions:
- Metric definitions/configuration:
- Software and versions:
- Reviewer agreement method:

## Per-Plan Report

### Plan [01-30]: [Anonymous ID]

#### 1. Provenance

- Plan type: [synthetic / anonymized licensed source]
- Source collection or generator:
- Source release/version:
- License or permitted research use:
- Retrieval or generation date:
- Internal lineage record:
- De-identification method:
- Redistribution status: [permitted / derived outputs only / not permitted]
- Identity check: [confirm no address, coordinates, listing ID, source link, or
  identifying imagery appears in this report]

#### 2. Data Quality

- Input format:
- Scale/units: [known / estimated / unknown]
- Geometry completeness:
- Room-label completeness:
- Opening/adjacency completeness:
- Geometry validation results:
- Manual review status:
- Corrections or normalization applied:
- Material ambiguities:
- Fitness for topology analysis: [yes / qualified / no]
- Fitness for visibility analysis: [yes / qualified / no]
- Confidence in observations: [high / medium / low, with reason]

#### 3. Plan Summary

- Broad plan category:
- Approximate size band: [small / medium / large / unknown]
- Number of occupiable spaces:
- Number of circulation spaces:
- Relevant neutral features:
- Excluded or masked features:

Do not include an image or geometry that could be reverse-matched to a
real property. Prefer an abstract room graph or a substantially transformed
diagram when visualization is necessary and permitted.

#### 4. Topology

Report descriptive measurements without combining them into a security or
vulnerability score.

| Measure | Result | Interpretation | Confidence/caveat |
| --- | --- | --- | --- |
| Graph nodes and edges | | | |
| Entrance-to-room depth distribution | | | |
| Integration/closeness | | | |
| Choice/betweenness | | | |
| Connectivity | | | |
| Route-overlap summary | | | |
| Privacy-gradient continuity | | | |
| Dead-end ratio | | | |

Topology observations:

- Circulation structure:
- Public-to-private sequence:
- Spaces with high shared-route use:
- Wayfinding implications:
- Alternative interpretations:

#### 5. Visibility

State the analysis resolution, observer assumptions, omitted geometry, and
whether scale is reliable.

| Measure | Result | Interpretation | Confidence/caveat |
| --- | --- | --- | --- |
| Visual integration | | | |
| Isovist area/range | | | |
| Occlusivity | | | |
| Entrance-to-interior visibility | | | |
| Visibility from occupied to common space | | | |

Visibility observations:

- Broad visibility pattern:
- Areas supporting orientation or passive overlook:
- Areas with limited visual connection:
- Sensitivity to doors, furniture, or uncertain geometry:

Do not document surveillance placement, blind-spot exploitation, evasion
routes, or other operational access-control details.

#### 6. Privacy and Legibility

- Entrance transition: [direct / buffered / ambiguous]
- Public, shared, and private zones distinguishable:
- Private spaces visible from the entrance or shared circulation:
- Guest route legibility:
- Resident route legibility:
- Potential circulation conflicts:
- Accessibility and inclusive-wayfinding considerations:
- Overall privacy/legibility interpretation:

Discuss privacy and legibility separately where they conflict. A highly legible
layout may expose private areas; a strongly separated layout may make
orientation harder.

#### 7. CPTED Design Observations

Treat CPTED as a qualitative design framework, not evidence of crime
prevention. Describe only plan-level, non-operational observations.

| Principle | Observable design condition | Possible benefit | Qualification/tradeoff |
| --- | --- | --- | --- |
| Natural surveillance | | | |
| Natural access guidance | | | |
| Territorial reinforcement | | | |
| Maintenance/image support | | | |
| Activity support | | | |

- Reviewer 1 summary:
- Reviewer 2 summary:
- Agreement/disagreement:
- Adjudicated observation:

Do not analyze lock types, alarm systems, staff procedures, surveillance
coverage, restricted-area controls, or methods of defeating controls.

#### 8. Tradeoffs

| Design quality | Potential benefit | Potential cost/conflict | Evidence strength |
| --- | --- | --- | --- |
| Privacy | | | |
| Legibility/wayfinding | | | |
| Social visibility | | | |
| Circulation efficiency | | | |
| Accessibility | | | |
| Daylight/ventilation | | | |
| Usable area | | | |
| Egress considerations | | | |

Balanced interpretation:

#### 9. Limitations

- Missing or uncertain source data:
- Modeling assumptions:
- Metric sensitivity:
- Semantic-label uncertainty:
- Reviewer subjectivity:
- Domain or plan-type limitations:
- Factors not represented by the plan:
- Claims that cannot be supported:

#### 10. Safe Publication Check

- [ ] Anonymous ID only; no address or property identity.
- [ ] No coordinates, listing IDs, identifying source links, or metadata.
- [ ] No reverse-matchable image or unmodified real plan.
- [ ] License and redistribution terms permit every included artifact.
- [ ] No vulnerability score, ranking, or “most/least secure” claim.
- [ ] No attack path, bypass advice, evasion guidance, or exploitable detail.
- [ ] No detailed access-control, surveillance, or restricted-area analysis.
- [ ] Observations are framed as design research with uncertainty.
- [ ] Any plan-specific result is sufficiently abstracted for publication.
- [ ] A second reviewer completed disclosure review.

Publication decision: [publish / publish after abstraction / aggregate only /
do not publish]

Reviewer and date:

---

## Aggregate Report: 30 Plans

### 1. Scope and Cohort

- Plans analyzed:
- Synthetic versus anonymized counts:
- Source collections/generators:
- Plan categories and size bands:
- Inclusion/exclusion summary:
- Missing-data summary:
- Analysis configuration shared across plans:
- Deviations from the registered protocol:

Describe the cohort in broad groups. Do not provide a lookup table that links
anonymous IDs to real sources or properties.

### 2. Provenance and Data Quality Summary

| Source/generator group | Plan count | Usage rights | Key quality issues | Analyses permitted |
| --- | ---: | --- | --- | --- |
| | | | | |

- Geometry validation pass rate:
- Label/adjacency completeness:
- Manual audit coverage:
- Scale-known proportion:
- Exclusions and reasons:
- Potential source or generator bias:

### 3. Aggregate Topology

Report distributions, ranges, medians, confidence intervals, and broad groups.
Do not publish a ranked table of individual plans.

| Measure | Valid N | Median/IQR | Range or CI | Group-level interpretation |
| --- | ---: | --- | --- | --- |
| Entrance-to-room depth | | | | |
| Integration/closeness | | | | |
| Choice/betweenness | | | | |
| Connectivity | | | | |
| Route overlap | | | | |
| Privacy gradient | | | | |
| Dead-end ratio | | | | |

- Recurring topology patterns:
- Differences by broad plan category:
- Robustness/sensitivity results:

### 4. Aggregate Visibility

| Measure | Valid N | Median/IQR | Range or CI | Group-level interpretation |
| --- | ---: | --- | --- | --- |
| Visual integration | | | | |
| Isovist area/range | | | | |
| Occlusivity | | | | |
| Entrance-to-interior visibility | | | | |
| Occupied-to-common-space visibility | | | | |

- Recurring visibility patterns:
- Effects of geometry or scale uncertainty:
- Results omitted from publication and why:

### 5. Privacy and Legibility Themes

- Frequency of direct versus buffered entrances:
- Public-to-private zoning patterns:
- Common wayfinding strengths:
- Common privacy tensions:
- Circulation conflicts:
- Accessibility and inclusive-design themes:
- Cases that contradicted the registered expectations:

Use counts or broad proportions where disclosure risk permits. Avoid presenting
unusual plan characteristics that could enable re-identification.

### 6. CPTED Design Themes

| Principle | Recurring observation | Plans reviewed (N) | Reviewer agreement | Important qualification |
| --- | --- | ---: | --- | --- |
| Natural surveillance | | | | |
| Natural access guidance | | | | |
| Territorial reinforcement | | | | |
| Maintenance/image support | | | | |
| Activity support | | | | |

- Cross-cutting design observations:
- Conflicting interpretations:
- Evidence limits:

Do not convert these observations into crime predictions, security grades, or
comparative vulnerability rankings.

### 7. Cross-Cohort Tradeoffs

| Recurring design pattern | Benefits observed | Costs/conflicts observed | Applicable cohort | Evidence strength |
| --- | --- | --- | --- | --- |
| | | | | |

- Privacy versus legibility:
- Integration versus separation:
- Passive overlook versus personal privacy:
- Efficiency versus transition space:
- Other accessibility, egress, daylight, ventilation, or usable-area effects:

### 8. Aggregate Limitations

- Dataset representativeness:
- Source/generator artifacts:
- De-identification effects:
- Geometry and semantic uncertainty:
- Visibility-model assumptions:
- Reviewer reliability:
- Lack of operational or outcome data:
- Generalizability:
- Ethical and publication constraints:
- Appropriate and inappropriate conclusions:

### 9. Conclusions

- Findings supported by the data:
- Findings requiring replication:
- Null or contradictory findings:
- Design questions for future research:

Keep conclusions at cohort level. Do not identify individual plans as better,
worse, safer, less safe, vulnerable, or secure.

### 10. Aggregate Safe Publication Review

- [ ] Only aggregate distributions or sufficiently abstract synthetic examples
  are included.
- [ ] Small cells, outliers, and distinctive combinations have been suppressed
  or generalized.
- [ ] No source-to-plan linkage or re-identification aid is present.
- [ ] No addresses, coordinates, property names, or identifying metadata appear.
- [ ] No individual vulnerability ranking or security score appears.
- [ ] No bypass, evasion, attack-path, or access-control guidance appears.
- [ ] Licensing permits all published text, tables, diagrams, and derived data.
- [ ] Uncertainty, bias, and limits are stated beside relevant findings.
- [ ] Independent disclosure review is complete.

Release contents:

- Public:
- Aggregate only:
- Withheld:
- Reason for withholding:
- Disclosure reviewer and date:
