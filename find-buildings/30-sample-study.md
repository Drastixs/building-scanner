# Reproducible 30-Sample Residential Floor-Plan Study

## Scope

This protocol defines a pilot study of exactly 30 residential floor-plan
samples. Samples must come from licensed research datasets and must be synthetic
or stripped of identifiers by the dataset provider and the study pipeline. The
study does not use scraped listings, planning records, addresses, coordinates,
or identifiable real buildings.

The study evaluates plan-level spatial properties such as circulation depth,
room adjacency, privacy gradients, and visibility. It does not produce
site-specific security assessments or a single security score.

This document is a sampling plan only. It does not claim that any dataset or
sample has been downloaded, accepted, or processed.

## Reproducibility controls

Before selection, create a frozen study manifest containing:

- protocol version: `30-sample-v1`;
- random seed: `20260606`;
- official dataset name, release/version, and source URL;
- retrieved license and terms checksum;
- source-file checksum and provider-issued sample identifier;
- eligibility fields and exclusion reason;
- assigned study ID, stratum, and split.

Keep provider identifiers in an access-controlled manifest. Analysis tables and
reports use only IDs `S01` through `S30`. Do not retain or construct mappings to
addresses, coordinates, listings, or occupants.

## Source allocation

Use three sources, with exactly 10 eligible samples from each:

| Study IDs | Source | Data character | Allocation |
| --- | --- | --- | ---: |
| `S01-S10` | CubiCasa5K | Research floor-plan images and annotations; use only records passing de-identification checks | 10 |
| `S11-S20` | Swiss Dwellings | Structured dwelling geometry/features; use only records without identifying fields | 10 |
| `S21-S30` | Structured3D | Synthetic residential scenes | 10 |
| **Total** |  |  | **30** |

Use only an official release whose terms permit the intended research. If a
source fails license, access, privacy, or format review, pause the protocol and
issue a versioned amendment naming another licensed synthetic or anonymized
research dataset. Do not silently alter the allocation.

## Balanced sampling

Balance each source across two size strata, using a source-relative measure so
that scale and annotation differences do not force incomparable thresholds:

- `compact`: eligible plans at or below the source's median normalized internal
  floor area;
- `large`: eligible plans above the source's median normalized internal floor
  area.

If reliable metric area is unavailable, use room count as the preregistered
fallback: at or below the source median is `compact`, and above it is `large`.
Record which measure was used and do not mix measures within one source.

Assign exactly five compact and five large samples per source:

| IDs | Stratum |
| --- | --- |
| `S01-S05`, `S11-S15`, `S21-S25` | Compact |
| `S06-S10`, `S16-S20`, `S26-S30` | Large |

Within each source and stratum:

1. Sort eligible records by a stable provider-issued identifier.
2. Detect duplicate or near-duplicate plans before randomization.
3. Shuffle with a deterministic pseudorandom generator seeded from
   `SHA-256("30-sample-v1|20260606|<source>|<stratum>")`.
4. Select the first five eligible records.
5. Assign study IDs in shuffled order according to the table above.

Do not choose samples based on metric outcomes, visual appeal, or expected
findings.

## Inclusion rules

A sample is eligible only when all of the following are true:

1. It is a residential dwelling or synthetic residential scene.
2. Dataset access and intended analysis are permitted by documented terms.
3. It contains no address, coordinates, resident identity, listing link, or
   identifying exterior imagery in the analysis record.
4. It represents one complete dwelling plan, or a clearly separable dwelling
   unit within a larger source record.
5. Room boundaries and traversable connections can be derived from documented
   annotations or reproducible preprocessing.
6. It has at least three occupiable rooms and at least one legitimate entrance.
7. Geometry is sufficiently complete to construct a connected room-access graph,
   allowing explicitly documented non-occupiable exterior nodes.
8. Scale or room count is available for deterministic size stratification.

## Exclusion rules

Exclude a candidate before sampling when any of the following applies:

- commercial, institutional, hotel, dormitory, or other non-dwelling use;
- identifiable or re-identifiable location or occupant information;
- uncertain or incompatible license or terms;
- duplicate or near-duplicate of another eligible plan;
- incomplete crop, missing dwelling boundary, or irreparable geometry;
- no defensible entrance or door connectivity;
- mixed units that cannot be separated without subjective reconstruction;
- corrupt files or undocumented transformations;
- a source record linked across train/test partitions to the same underlying
  dwelling or synthetic scene.

Log every exclusion under a controlled vocabulary without storing identifying
content. Do not replace a post-selection failure opportunistically: take the
next record in the same deterministic shuffled stratum and preserve the failed
ID assignment in the audit log.

## Split strategy

Use a fixed 18/6/6 exploratory split, balanced by source and size:

| Split | Compact IDs | Large IDs | Total |
| --- | --- | --- | ---: |
| Train | `S01-S03`, `S11-S13`, `S21-S23` | `S06-S08`, `S16-S18`, `S26-S28` | 18 |
| Validation | `S04`, `S14`, `S24` | `S09`, `S19`, `S29` | 6 |
| Test | `S05`, `S15`, `S25` | `S10`, `S20`, `S30` | 6 |

The split supports pipeline development, not reliable model-performance claims;
30 samples are too few for that. Freeze the split before feature computation.
Group all floors, augmentations, renderings, and derived graphs from the same
source dwelling or synthetic scene into one split. Fit label mappings,
imputation, normalization, thresholds, and any learned parameters using the
training split only. Use validation for pipeline choices and open the test split
once for the preregistered final run.

Report descriptive results by source and size stratum. Treat source comparisons
as domain-shift checks, not estimates of geographic populations.

## Run checklist

- [ ] Freeze `30-sample-v1`, seed `20260606`, research questions, and metrics.
- [ ] Verify current official access terms and permitted uses for all sources.
- [ ] Record release identifiers, retrieval dates, and license/terms checksums.
- [ ] Confirm raw data storage and outputs comply with source restrictions.
- [ ] Scan metadata and imagery for prohibited identifying information.
- [ ] Build the eligible pool independently for each source.
- [ ] Normalize dwelling boundaries, room labels, units, openings, and entrances.
- [ ] Run geometry, connectivity, completeness, and plausibility validation.
- [ ] Detect duplicate and near-duplicate plans before sampling.
- [ ] Calculate source medians and assign five compact/five large samples.
- [ ] Apply deterministic shuffling and assign IDs `S01-S30`.
- [ ] Record exclusions and deterministic same-stratum replacements.
- [ ] Apply the fixed 18/6/6 split with source groups kept intact.
- [ ] Freeze and checksum the non-identifying study manifest.
- [ ] Manually audit all 30 plans for labels, geometry, entrances, and privacy.
- [ ] Compute only preregistered plan-level spatial metrics.
- [ ] Keep test samples hidden until the pipeline is frozen.
- [ ] Report aggregate distributions, uncertainty, exclusions, and limitations.
- [ ] Publish no source plans unless redistribution is expressly permitted.
- [ ] Publish no addresses, identifying links, or site-specific security details.
