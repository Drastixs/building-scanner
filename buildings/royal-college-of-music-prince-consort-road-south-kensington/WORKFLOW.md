# Workflow — Royal College of Music, Prince Consort Road

## Date
2026-06-06

## Steps

1. Created output directory.
2. Searched RBKC planning register for "Prince Consort Road" and "Royal College of Music". All RBKC portal URLs (rbkc.gov.uk/planningsearch, atlas.rbkc.gov.uk, rbkc.gov.uk/Planning/searches/default.aspx) return a cybersecurity incident notice rather than planning data.
3. Attempted direct fetch of RBKC planning search pages — all redirect to cyber-attack incident page.
4. Identified the "More Music" planning application submitted June 2015 via news sources (thestrad.com, rcm.ac.uk, johnsimpsonarchitects.com). Permission granted 15 October 2015. Architect: John Simpson Architects.
5. Attempted to find planning reference number via Google cache, web.archive.org, and RBKC moderngov — no accessible cached copies found.
6. Searched for any direct PDF links to floor plan drawings on johnsimpsonarchitects.com, rcm.ac.uk — none publicly available.
7. Checked RBKC planningedm.rbkc.gov.uk (old document management URL) — also redirected to incident page.

## Outcomes

- **No floor plans downloaded.** RBKC planning system is completely offline.

## Failures / Issues

- **RBKC planning portal offline since November 2025 cyber-attack.** This is the primary failure. The council confirmed "a cyber-attack with criminal intent, with data copied and taken away" detected on 24 November 2025. The planning search, document viewer, and all historical document URLs are unavailable.
- No alternative public source for the RCM planning application drawings was found. The drawings would have been submitted in 2015 and approved same year; they are not hosted by the architect or the college publicly.

## Recovery path

When RBKC restores its planning portal:
1. Go to rbkc.gov.uk/planningsearch
2. Search address: Prince Consort Road SW7 2BS, application type: All, date range: 2015-01-01 to 2016-12-31
3. Expect two linked applications (full planning permission + listed building consent)
4. Download "existing floor plans" and "proposed floor plans" from the documents tab
