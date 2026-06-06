# Workflow: Populate Organizer Identity into event.md files

## What to do

Use Claude Code + Playwright to enrich each event.md with organizer identity fields.

For each `building-scanner/events/*/event.md`:
1. Read `event_url` from the frontmatter
2. Use Playwright to scrape the event page
3. Pass the HTML to Claude and extract: `organizer_name`, `organizer_email`, `organizer_company`, `organizer_linkedin` (if present)
4. Write those fields back into the event.md frontmatter

Once event.md files are enriched, the `organizer-enricher` reads from them directly:
```
event.md (has organizer_name + organizer_email)
  → enrich(name, email)
  → OrganizerProfile JSON
  → LLM agent
```

## Why

The 30+ event.md files already have `event_url` but no organizer fields.
The enricher needs a name/email to start. This step bridges the gap
without adding runtime complexity to the enricher itself.

## Script location

`toolings/organizer-enricher/populate-event-organizers.py`

## Run order

1. Run this script first (one-time, offline): `python populate-event-organizers.py`
2. Then run the enricher on any event: `python demo.py --event sxsw-london-2026-barbican-screen-festival`

## Fields to add to event.md frontmatter

```yaml
organizer_name: "string"
organizer_email: "string or null"
organizer_company: "string or null"
organizer_linkedin: "https://... or null"
organizer_twitter: "@handle or null"
organizer_website: "https://... or null"
```
