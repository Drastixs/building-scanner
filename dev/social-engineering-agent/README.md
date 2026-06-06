# social-engineering-agent

Agent for pattern cognition and hypothesis matching in physical security assessment.

## Goal

Build a context-brain agent that models how expert physical penetration testers reason — fusing social, spatial, and credential graphs to surface likely attack paths and test hypotheses.

## Stack

- **Memory brain:** [Mubit](https://mubit.ai/) — persistent execution memory for agents. Writes lessons at end of each run, recalls relevant context before the next. Sub-80ms retrieval, cross-agent/multi-session, Anthropic-native via `mubit.init()`.
- **Pattern cognition:** see `methodology/phys-sec-engineer-patterns.md`
- **Hypothesis engine:** ACH (Analysis of Competing Hypotheses) + RPD loop — `methodology/hypothesis-engine.md`
- **LLM:** Claude (Anthropic) via Mubit gateway — provider-agnostic
- **Data sources:** `../../dev/toolings/`, `../../research/LITERATURE-REVIEW.md`, `../../events/`

## Structure

```
social-engineering-agent/
├── README.md                 ← this file
├── methodology/
│   ├── phys-sec-engineer-patterns.md   ← practitioner pattern breakdown
│   └── hypothesis-engine.md            ← ACH + RPD loop design
└── agent/                              ← code (next phase)
```

## Status

- [x] Methodology breakdown written
- [ ] Mubit confirmed + wired
- [ ] Agent scaffold
- [ ] Context brain populated
