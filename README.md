# building-scanner

Find and download public architectural drawings from UK planning registers (Idox). See `CONTEXT.md` for full background.

## Structure

```
buildings/          One directory per building — floor plans, sections, DAS PDFs + WORKFLOW.md per site.
dev/                Tools and development work: cve-research, ip-range, find-buildings, blueprint, arbor-graph, toolings, schematic-research.
events/             Event listings at scanned buildings (used to identify access opportunities).
research/           Written research notes — Arbor planning records, search methodology, literature review.
research_docs/      Reference PDFs and extracted text (Level39, One Canada Square, floor plan HTML).
CONTEXT.md          Full project brief: the idea, target building, method, obstacles, and open threads.
GRAPH-SEARCH-DESIGN.md  Design doc for the graph-based building search approach.
workflow-claude.md  Agent workflow notes and session instructions.
```
