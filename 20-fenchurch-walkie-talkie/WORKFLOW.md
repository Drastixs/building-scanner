# WORKFLOW — 20 Fenchurch Street (Walkie-Talkie)

## Source
Council: **City of London**
Portal: https://www.planning.cityoflondon.gov.uk/online-applications/
Application: `08/01061/FULMAJ` (confidence: high)

## What Worked
Primary reference 08/01061/FULMAJ confirmed from two authoritative sources: (1) City of London Court of Common Council report (democracy.cityoflondon.gov.uk/documents/s34044/20 Fenchurch Street.pdf, a scanned 2014 document) explicitly states 'planning permission was granted on 6th October 2009 ... (08/01061/FULMAJ)'; (2) GLA planning report PDU/0044b/01 (london.gov.uk, January 2009) confirms 'planning application no. 08/01061/FULMAJ'. Full planning history extracted from the scanned PDF: original application 06/00158/FULEIA was called-in by the Secretary of State and approved 9 July 2007 after public inquiry; amended annex building 07/01053/FULL approved 3 July 2008; main amended 38-storey scheme 08/01061/FULMAJ approved 6 October 2009; further amendments 11/00234/FULL approved 1 July 2011 (this is the scheme that was actually built); brise soleil addition 14/00110/FULL from 2014. The City of London IDOX planning portal (planning2.cityoflondon.gov.uk) is the correct portal but was inaccessible for document retrieval from this server — it returns HTTP 500 for all direct curl requests. WebFetch tool also encountered SSL certificate errors. No direct documents tab URL could be verified. The GLA reference for the strategic referral is PDU/0044b/01. The applicant is 'The City of London Real Property Company Ltd'; Land Securities and Canary Wharf Group formed the JV in September 2010 to implement the permission. Design and Access Statement and floor plan drawings will be in the 08/01061/FULMAJ application record on the IDOX portal — the keyVal for this application could not be determined as the portal rejects all server-side requests."

## Search Sequence Used
1. Web search: "20 Fenchurch Street Walkie-Talkie planning application floor plans"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `08/01061/FULMAJ` on https://www.planning.cityoflondon.gov.uk/online-applications/
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
