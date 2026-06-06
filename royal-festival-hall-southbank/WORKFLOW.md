# Royal Festival Hall — Scan Workflow Notes

## Planning Authority
**London Borough of Lambeth** — planning.lambeth.gov.uk

## What Worked

- **Lambeth planning register** was the correct route. The Royal Festival Hall is Grade I listed and sits within the Southbank Centre estate in Lambeth. Searching by address (Belvedere Road SE1 8XX) or by the application reference (23/02466/LB) surfaces the listed-building-consent application and its attached drawing set.
- The application reference format `23/02466/LB` was identified successfully — "LB" denoting a listed-building application, year prefix 23 (2023). This application covers internal alterations including Level 2 spaces (general arrangement and specific rooms such as the prayer room).
- The Lambeth planning portal (Idox/Uniform system) lists documents by type; floor plan PDFs were identifiable from their filenames before attempting download.

## What Failed / Friction Points

- **Both PDF downloads failed — files are 0 bytes.** The Lambeth planning portal served the document links but the files themselves did not transfer correctly. This is a known issue with the Idox portal: some document links require an active browser session with cookies set, and direct programmatic download (wget/curl) results in an empty or error response.
- The Lambeth portal occasionally requires navigating through a CAPTCHA or session-gated document viewer before a PDF becomes downloadable, blocking automated retrieval.
- Southbank Centre Ltd (the venue operator) does not publish technical floor plans or stage plans for the Royal Festival Hall on its public website — only basic visitor maps are available.
- The GLA (Greater London Authority) has planning oversight of some Southbank Centre developments but does not separately hold the detailed drawing sets; those remain on the Lambeth register.

## Recovery Options

To obtain the files, either:
1. **Browser download** — navigate to planning.lambeth.gov.uk, search for application 23/02466/LB, open the Documents tab, and download the PDFs manually via the browser (session cookies resolve the auth issue).
2. **FOI request** — submit a request to Lambeth Planning citing application 23/02466/LB and requesting the drawing set; turnaround is typically 20 working days.
3. **Southbank Centre Estates** — contact the Southbank Centre directly; as a publicly funded arts organisation they are often willing to share floor plans for legitimate research/event purposes.

## Best Information Found

No usable spatial data was retrieved for this building in the current scan. The application reference 23/02466/LB is confirmed valid and the Level 2 GA plan and prayer room plan are known to exist on the Lambeth register — they just require a browser session to download.

## Source Summary

| File | Source | Status |
|------|--------|--------|
| 23_02466_LB-existing-level2-general-arrangement.pdf | London Borough of Lambeth planning register (app 23/02466/LB) | FAILED — 0 bytes |
| 23_02466_LB-existing-level2-prayer-room.pdf | London Borough of Lambeth planning register (app 23/02466/LB) | FAILED — 0 bytes |
