# Graph Search & Link-Discovery Design

**A tool for exploring connections between cognition/learning techniques and physical red-team tradecraft.**

> Scope note: this is a research instrument for a PhD studying *learning mechanisms* and *expert cognition*. It models techniques, frameworks, and the conceptual links between them. It is not intrusion tooling and contains no operational attack procedures — the "red-team" nodes are cognition constructs (entity resolution as a *reasoning pattern*, mental-mapping as a *spatial-cognition process*), not exploits.

---

## 1. Problem framing: retrieval vs. discovery are two different jobs

The researcher's stated goal — "dynamically search the body of techniques and **make links between them**" — actually conceals two distinct computational tasks that demand different methods. Conflating them is the most common way these tools fail.

**Task A — Retrieval (find the right node).** Given a query in natural language or domain jargon ("what's the disprove-not-confirm method?", "diagnosticity", "the spider-web-of-memory idea"), return the technique node(s) the user meant. This is an *information-retrieval* problem: match a query string against a corpus of node descriptions. Keyword and semantic search live here.

**Task B — Discovery (find links that aren't written down yet).** Given two techniques, *explain how they connect* (the path through intermediate concepts); or, given one technique, *propose techniques it should plausibly connect to but currently doesn't*. This is **link prediction / pathfinding** over a graph. It is structurally different from retrieval: you are not matching text against a query, you are reasoning over the *topology* of relationships. Neither keyword nor vector search can do this — they have no notion of a typed, multi-hop relationship.

The whole design hangs on keeping these separate. Retrieval gets you *to* a node; discovery happens *between* nodes. A concrete example from this domain:

- *Retrieval*: "find the node about reasoning from missing evidence" → returns **Absence-as-Evidence (dog-that-did-not-bark)**.
- *Discovery*: "what connects **Recognition-Primed Decision making** to **Analysis of Competing Hypotheses**?" → the system should traverse `RPD —forms→ Working-Hypothesis —tested-by→ ACH` and surface that ACH's *diagnosticity* discipline is precisely the corrective for RPD's single-option satisficing. That answer is a *path*, not a document.

The corpus itself reinforces this framing. Heuer's own metaphor for expert insight is "spinning new links in the spider web of memory — links among facts, concepts, and schemata that previously were not connected or only weakly connected." The tool is, almost literally, an instrument for spinning and testing those links. That is a graph operation.

---

## 2. The data model: one property graph for both worlds

We model everything as a **typed, directed property graph**. Two families of nodes coexist in a single graph: (1) the **cognition/learning frameworks** (RPD, Sensemaking/Data-Frame, ACH, CDM, space-syntax depth, communities of practice, deliberate practice, high/low-validity environments) and (2) the **~100-item taxonomy of connectable cues** the researcher developed (people↔photos, reader-model↔RF-tech↔clonability, bin-day↔rear-access, facility codes, privilege tiers). They are *not* separate graphs — the entire value of the tool is that a low-level cue node (`facility-code`) connects, through typed edges, up to a high-level cognition node (`Credential-Reasoning` → `Schema-Driven-Pattern-Matching` → `RPD`). The graph is the bridge.

### 2.1 Node types

| Label | Meaning | Example instances |
|---|---|---|
| `Framework` | A named cognition/learning theory | RPD, Data-Frame Sensemaking, Schema Theory, ACH, CDM, Space-Syntax |
| `Construct` | A finer mechanism inside a framework | Diagnosticity, Mental Simulation, Topological Depth, Landmark/Route/Survey knowledge |
| `Tradecraft` | A red-team *reasoning* pattern | Entity Resolution, Social-Graph Building, Trust-Transitivity, Mental-Mapping, Credential Reasoning |
| `Cue` | A connectable observable (the ~100-item taxonomy) | photo, bin-day, reader-model, RF-tech, facility-code, badge-photo, rear-access |
| `FailureMode` | A documented cognitive failure | Satisficing, Confirmation Bias, Selective Perception, Groupthink |
| `Artifact` | An elicitation output | Situation Assessment Record, Timeline, Decision Requirement |
| `LearningProcess` | How expertise is acquired | Deliberate Practice, Communities of Practice, Reflective Practice |
| `Environment` | A validity context | High-Validity Env, Low-Validity Env |
| `Source` | A citation | Heuer 1999, Klein 2015, Hillier & Hanson, Hoffman et al. 1998 |

### 2.2 Edge types (typed, directed, weighted)

Every edge carries a `weight` (0–1 strength) and a `confidence` (0–1, how well-sourced the assertion is — directly reflecting the corpus's own 3-0 / 2-1 verification votes).

| Edge | Direction / meaning | Example |
|---|---|---|
| `MAPS_TO` | tradecraft → framework | `Mental-Mapping —MAPS_TO→ Space-Syntax` |
| `TESTS` | method → hypothesis/construct | `ACH —TESTS→ Working-Hypothesis` |
| `FORMS` | process → output | `RPD —FORMS→ Working-Hypothesis` |
| `REINFORCES` | process → expertise | `Deliberate-Practice —REINFORCES→ Schema-Library` |
| `FAILS_VIA` | method → failure mode | `Single-Hypothesis-Focus —FAILS_VIA→ Selective-Perception` |
| `ELICITED_BY` | construct → method | `Decision-Requirement —ELICITED_BY→ CDM` |
| `MEASURES` | construct → property | `Topological-Depth —MEASURES→ Accessibility` |
| `ENABLES` | construct → capability | `Diagnosticity —ENABLES→ Hypothesis-Discrimination` |
| `DEPENDS_ON` | construct → precondition | `Skilled-Intuition —DEPENDS_ON→ High-Validity-Env` |
| `CROSS_GRAPH_PIVOT` | cue → cue (the taxonomy links) | `reader-model —CROSS_GRAPH_PIVOT→ RF-tech —CROSS_GRAPH_PIVOT→ clonability` |
| `CITES` | node → source | `ACH —CITES→ Heuer-1999` |
| `CONTRADICTS` | claim ↔ claim | `Sequential-Stage-Model —CONTRADICTS→ Parallel-Spatial-Learning` |

`CROSS_GRAPH_PIVOT` is the workhorse for the cue taxonomy: it encodes the researcher's "connectable things" (photo→person, bin-day→rear-access, reader-model→RF→clonability) as first-class graph edges, so they become traversable and link-predictable rather than just notes.

### 2.3 Node properties

Every node stores its retrieval surfaces *on the node itself* — this is what lets one store serve all three search modalities:

```json
{
  "id": "ach",
  "label": "Framework",
  "name": "Analysis of Competing Hypotheses",
  "aliases": ["ACH", "competing hypotheses matrix"],
  "description": "Eight-step disprove-not-confirm procedure; enumerates all reasonable hypotheses as a data-by-hypothesis matrix and weights evidence by diagnosticity rather than quantity.",
  "embedding": [0.013, -0.221, ...],        // dense vector for semantic search
  "text_tsv": "...",                          // full-text index column for keyword search
  "confidence": 0.9,                          // 3-0 verified
  "source_ids": ["heuer-1999", "nas-13040"]
}
```

### 2.4 Worked example (Cypher)

```cypher
// --- Frameworks & constructs ---
CREATE (rpd:Framework {name:'Recognition-Primed Decision making', conf:0.95})
CREATE (sense:Framework {name:'Data-Frame Sensemaking', conf:0.9})
CREATE (ach:Framework {name:'Analysis of Competing Hypotheses', conf:0.9})
CREATE (diag:Construct {name:'Diagnosticity', conf:0.9})
CREATE (wh:Construct {name:'Working Hypothesis'})
CREATE (depth:Construct {name:'Topological Depth', conf:0.95})

// --- Tradecraft & cues ---
CREATE (mm:Tradecraft {name:'Mental-Mapping'})
CREATE (cred:Tradecraft {name:'Credential Reasoning'})
CREATE (reader:Cue {name:'reader-model'})
CREATE (rf:Cue {name:'RF-tech'})
CREATE (clone:Cue {name:'clonability'})

// --- Failure & sources ---
CREATE (sel:FailureMode {name:'Selective Perception'})
CREATE (heuer:Source {name:'Heuer 1999'})

// --- Typed edges with weight/confidence ---
CREATE (rpd)-[:FORMS {w:0.8}]->(wh)
CREATE (ach)-[:TESTS {w:0.9}]->(wh)
CREATE (diag)-[:ENABLES {w:0.85}]->(ach)
CREATE (rpd)-[:FAILS_VIA {w:0.7}]->(sel)
CREATE (mm)-[:MAPS_TO {w:0.9, conf:0.95}]->(depth)
CREATE (cred)-[:MAPS_TO {w:0.6}]->(rpd)
CREATE (reader)-[:CROSS_GRAPH_PIVOT {w:0.9}]->(rf)
CREATE (rf)-[:CROSS_GRAPH_PIVOT {w:0.85}]->(clone)
CREATE (clone)-[:MAPS_TO {w:0.5}]->(cred)
CREATE (ach)-[:CITES]->(heuer)
```

Note how the cue chain `reader-model → RF-tech → clonability` plugs directly into `Credential-Reasoning` and from there toward `RPD`. Low-level observables and high-level cognition theory live in one connected component — exactly what makes cross-level discovery possible.

---

## 3. The three search modalities

### 3.1 Keyword / lexical (BM25, full-text)

**How it works.** Tokenize the corpus, build an inverted index, rank documents by term-frequency / inverse-document-frequency (BM25). Implementations: PostgreSQL FTS (`tsvector`/`tsquery`), SQLite FTS5, Elasticsearch/OpenSearch.

**Good at.** Exact terms and rare jargon. This domain is *dense* with precise, low-frequency vocabulary — "diagnosticity", "facility code", "allocentric survey knowledge", "Situation Assessment Record". For these, BM25 is near-perfect and cheap: the researcher who types "diagnosticity" wants the diagnosticity node, full stop. Boolean operators (`AND`/`OR`/`NOT`) give precise recall control.

**Misses.** Synonymy and paraphrase. "Cheap low-commitment probe" and "low-cost hypothesis test" share almost no tokens but mean the same thing; BM25 scores them near zero against each other. It also can't relate "spider web of memory" to "link prediction" without a literal shared word.

**Query against this graph:**
```sql
-- Postgres FTS: find nodes mentioning diagnosticity or disconfirmation
SELECT name, ts_rank(text_tsv, q) AS rank
FROM nodes, to_tsquery('diagnosticity | disconfirm:*') q
WHERE text_tsv @@ q
ORDER BY rank DESC LIMIT 10;
```

### 3.2 Semantic / dense vector (embeddings + ANN)

**How it works.** Embed each node's `name + description` into a dense vector with a sentence-embedding model (e.g. OpenAI `text-embedding-3-large`, Cohere `embed-v3`, or open models like `bge-large` / `e5-large` / `nomic-embed-text`). Store vectors, query by embedding the user's text and retrieving nearest neighbours via approximate-nearest-neighbour search (pgvector HNSW, FAISS, Qdrant).

**Good at.** Conceptual / paraphrase similarity. "A cheap, low-commitment probe to test a guess" lands next to **Absence-as-Evidence** and **Hypothesis-Driven Observation** even with zero shared keywords. This is the right tool when the researcher describes a *concept* they can't name — common in early exploratory research.

**Misses.** Three things, all relevant here. (1) **Exact IDs and rare tokens** — embeddings smear "facility code" toward generic "access code" and lose precision. (2) **Negation and fine distinctions** — "disprove not confirm" can embed close to "confirm", inverting the intended meaning. (3) **Relational / multi-hop reasoning** — a vector says *RPD is similar to ACH*; it cannot say *RPD forms a hypothesis that ACH then tests*. Similarity is not relationship.

**Query against this graph:**
```python
qv = embed("a cheap low-commitment way to test a hunch during recon")
# pgvector cosine ANN
SELECT name, 1 - (embedding <=> :qv) AS score
FROM nodes ORDER BY embedding <=> :qv LIMIT 10;
# → Absence-as-Evidence, Hypothesis-Driven Observation, Mental Simulation
```

### 3.3 Graph search (traversal, algorithms, link prediction)

**How it works.** Query the *structure*. Three sub-capabilities:

1. **Pattern matching & traversal** — Cypher/openCypher (Neo4j), or SPARQL (RDF). "Find all `FailureMode`s reachable from `RPD` in ≤2 hops."
2. **Graph algorithms** — shortest path (how do A and B connect?), centrality/PageRank (which technique is pivotal?), community detection (Louvain/Leiden — which techniques cluster into a "testing" vs "spatial" vs "credential" theme?).
3. **Link prediction** — the discovery engine. Heuristics (common-neighbours, **Adamic-Adar**, Jaccard, preferential attachment) score *missing* edges by local structure; learned methods (**node2vec**, **GraphSAGE** node embeddings) score candidate links by learned structural/feature similarity.

**Good at.** Everything relational and everything in Task B. Multi-hop "how are these connected" questions, finding pivotal/central techniques, clustering the field, and — uniquely — *proposing connections that no one has written down*. If `Mental-Mapping` and `ACH` share many common neighbours (both touch hypothesis-driven observation, both touch sensemaking) but have no direct edge, Adamic-Adar flags that gap as a likely-real-but-missing link for the researcher to investigate.

**Misses.** It is a poor *fuzzy-text entry point*. You cannot hand Cypher "the disprove-not-confirm thing" and expect it to find ACH — graph queries need you to already be *at* a node (by id or exact name). Graph search assumes you've solved Task A; it owns Task B.

**Queries against this graph:**
```cypher
// Shortest path: HOW do two techniques connect?
MATCH p = shortestPath(
  (a:Framework {name:'Recognition-Primed Decision making'})
  -[*..5]-(b:Framework {name:'Analysis of Competing Hypotheses'}))
RETURN p;

// Centrality: which technique is most pivotal in the testing cluster?
CALL gds.pageRank.stream('techGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC LIMIT 5;

// Link prediction (Adamic-Adar) for a node with no direct edge to ACH
MATCH (a:Construct {name:'Topological Depth'}), (b)
WHERE NOT (a)--(b) AND b:Tradecraft
RETURN b.name,
       gds.alpha.linkprediction.adamicAdar(a, b) AS score
ORDER BY score DESC LIMIT 10;
```

---

## 4. Why none alone is sufficient — the case for hybrid

Each modality fails exactly where another is strong:

- Keyword nails jargon, **dies on paraphrase**.
- Semantic nails paraphrase, **smears rare IDs and can't reason over relationships**.
- Graph owns relationships and discovery, **can't take you to a node from fuzzy text**.

The researcher's workflow needs all three in sequence, not in competition. The canonical pattern (often called **GraphRAG**) is:

> **Anchor → Expand → Rank.**
> (1) Use **hybrid keyword+semantic retrieval** to turn fuzzy human input into one or more *anchor nodes* (Task A). (2) Use **graph traversal / link-prediction** to expand from anchors and discover connections (Task B). (3) Rank the combined result by a blend of retrieval score, edge weight/confidence, and structural score.

For the anchor step, fuse keyword and semantic results with **Reciprocal Rank Fusion (RRF)** — a parameter-light fusion that needs no score normalization and consistently beats either retriever alone:

```
RRF_score(node) = Σ_retrievers  1 / (k + rank_in_that_retriever)     (k ≈ 60)
```

A query like "the cheap probe idea Heuer talks about" then works: *semantic* catches "cheap probe" (→ Absence-as-Evidence, Hypothesis-Driven Observation), *keyword* catches "Heuer" (→ nodes citing Heuer-1999), RRF fuses them, and the top anchor becomes the launch point for graph expansion.

---

## 5. Recommendation: graph-first for discovery, hybrid-retrieval for entry

**The opinionated call: build a hybrid system whose *discovery layer is graph-native*, fed by a *hybrid keyword+vector entry layer*.**

The reasoning is simple and decisive. The researcher's *core* goal is to "make links between techniques." That sentence describes **link prediction and pathfinding** — operations that are graph-native and that *neither keyword nor semantic search can perform at all*. Vector similarity can tell you two techniques are *similar*; only the graph can tell you they are *connected*, *how*, through *what intermediate constructs*, and which connections are *plausibly missing*. So the graph is not one option among three — it is the only modality that addresses Task B, and Task B is the point of the tool.

But you cannot make the graph the entry point, because researchers type fuzzy natural language and half-remembered jargon, and Cypher can't fuzzy-match. So:

- **Entry / lookup layer → hybrid keyword+vector with RRF.** Keyword handles the dense jargon ("diagnosticity", "facility code", "Situation Assessment Record"); vector handles paraphrase and concept-without-a-name; RRF fuses them into anchor nodes.
- **Discovery layer → graph traversal + algorithms.** Shortest-path to *explain how* two techniques connect; PageRank/centrality to find *pivotal* techniques; Louvain/Leiden community detection to *cluster* the field (testing cluster, spatial cluster, credential cluster); Adamic-Adar + node2vec **link prediction** to *propose new connections*.

### Decision matrix (task × modality)

| Task | Keyword | Semantic | Graph | Best |
|---|:--:|:--:|:--:|:--:|
| Look up a known jargon term ("diagnosticity") | ★★★ | ★★ | ✗ | **Keyword** |
| Find a concept by description (no name) | ★ | ★★★ | ✗ | **Semantic** |
| Match an exact ID ("facility code") | ★★★ | ★ | ✗ | **Keyword** |
| Robust NL entry (mixed jargon + paraphrase) | ★★ | ★★ | ✗ | **Hybrid (RRF)** |
| Explain *how* A connects to B | ✗ | ✗ | ★★★ | **Graph (path)** |
| Find the most pivotal technique | ✗ | ✗ | ★★★ | **Graph (centrality)** |
| Cluster the techniques into themes | ✗ | ★ | ★★★ | **Graph (community)** |
| **Propose new/latent links** | ✗ | ★ | ★★★ | **Graph (link pred.)** |

Semantic gets a half-star on "propose new links" only as a *feature signal* feeding the graph link-predictor (text similarity is a useful node feature for GraphSAGE) — not as a standalone capability. The pattern is unambiguous: hybrid owns entry, graph owns discovery.

---

## 6. Reference architecture & stack

Two viable stacks; pick by appetite for operational complexity.

**Option A — single store (recommended to start): PostgreSQL + Apache AGE + pgvector.**
One database holds everything: AGE provides openCypher graph queries, pgvector provides ANN vector search, native FTS provides BM25. No cross-system sync, trivial to back up, ideal for a single-researcher tool with a graph in the hundreds-to-low-thousands of nodes.

**Option B — best-in-class graph: Neo4j + the Graph Data Science (GDS) library.**
Choose this if link prediction and graph algorithms are heavily used — GDS ships production PageRank, Louvain/Leiden, node2vec, GraphSAGE, and link-prediction pipelines out of the box. Pair with an external vector index (Qdrant/FAISS) or Neo4j's native vector index, plus a full-text index for keyword.

```
                ┌─────────────────────────────────────────────┐
   user query → │  ORCHESTRATION LAYER                         │
                │                                              │
                │  1. ANCHOR                                   │
                │     ├─ keyword (FTS / BM25)  ─┐              │
                │     └─ vector (ANN, embeds)  ─┼─ RRF fuse →  │ → anchor nodes
                │  2. EXPAND                    ┘              │
                │     graph traversal (Cypher) +              │
                │     algorithms (path / PageRank / Louvain)  │
                │  3. DISCOVER                                 │
                │     link prediction (Adamic-Adar, node2vec)  │
                │  4. RANK (retrieval × edge-conf × struct)   │
                └─────────────────────────────────────────────┘
                                   │
                ┌──────────────────┴───────────────────┐
                │  STORE: Postgres+AGE+pgvector  (or)   │
                │         Neo4j+GDS + vector index      │
                │  nodes carry: description, embedding, │
                │  tsv, confidence, source_ids          │
                └───────────────────────────────────────┘
```

Embeddings are computed once at ingest and stored *on the node* (re-embed only when a description changes). The FTS index and the ANN index both point at the same node rows, so the anchor step queries one store twice and fuses.

### Three end-to-end queries the researcher would actually run

**Q1 — "What tests the hypotheses formed by RPD?"** (entry by name → 2-hop traversal)
```cypher
MATCH (rpd:Framework {name:'Recognition-Primed Decision making'})
      -[:FORMS]->(h)<-[:TESTS]-(m)
RETURN m.name AS tests_via, h.name AS hypothesis;
// → ACH tests the Working Hypothesis that RPD forms.
```

**Q2 — "Find latent links between space-syntax depth and credential reasoning."** (link prediction)
```cypher
MATCH (a:Construct {name:'Topological Depth'}),
      (b:Tradecraft {name:'Credential Reasoning'})
WHERE NOT (a)-[*..2]-(b)
RETURN gds.alpha.linkprediction.adamicAdar(a,b) AS aa_score,
       gds.alpha.linkprediction.commonNeighbors(a,b) AS shared;
// High score = "these should plausibly connect" → flag for researcher review.
```
Plus a path probe to see *via what* a weak link might run:
```cypher
MATCH p = allShortestPaths(
  (:Construct {name:'Topological Depth'})-[*..4]-(:Tradecraft {name:'Credential Reasoning'}))
RETURN p;   // surfaces e.g. depth → accessibility → access-control cue → credential reasoning
```

**Q3 — "Which technique is most central to the testing cluster?"** (community + centrality)
```cypher
CALL gds.louvain.stream('techGraph') YIELD nodeId, communityId   // detect clusters
// then PageRank within the cluster containing ACH:
CALL gds.pageRank.stream('techGraph') YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name, score ORDER BY score DESC LIMIT 5;
// → expect ACH / Diagnosticity high; identifies the pivotal hub of the testing theme.
```

---

## 7. Evaluation: is the search / discovery any good?

Evaluate the two tasks **separately**, because they fail differently.

**Retrieval (Task A).** Build a small gold set: ~30–50 queries (mix of jargon and paraphrase) each labelled with the node(s) the researcher considers correct. Report **precision@k** and **recall@k** (k = 5, 10) and **MRR**. Run keyword-only, vector-only, and RRF-hybrid on the same gold set — you expect hybrid to dominate, and you'll *see* the jargon-vs-paraphrase split (keyword wins the "diagnosticity" rows, vector wins the "cheap probe" rows).

**Link prediction (Task B).** Standard hold-out protocol: randomly **mask 10–20% of existing edges**, train the predictor on the rest, and test whether it ranks the masked (true) edges above random non-edges. Report **AUC-ROC** and **precision@k** on the held-out edges. AUC well above 0.5 means the structure is genuinely informative.

**Human-in-the-loop validation of *novel* proposals.** The held-out test only checks edges you *already had*. The actual product — *proposing links no one wrote down* — can only be judged by the researcher. Surface each proposed link with its score, the common neighbours that justify it, and the supporting path, then let the researcher rate it **confirmed / plausible-investigate / refuted**. Track the **confirmation rate over time** as the headline quality metric, and feed confirmed links back as new edges (closing the loop and improving future prediction).

There is a pleasing reflexivity here, and it's worth building in deliberately: the domain's *own* gold-standard method, Heuer's Analysis of Competing Hypotheses, prescribes that you test by trying to **disprove**, weighting evidence by **diagnosticity**, not by piling up confirmations. The validation UI should mirror that discipline — present each proposed link as a *hypothesis to be refuted*, prompt "what would we expect to see if this link were real, and is it absent?", and reward the researcher for killing weak links rather than rubber-stamping them. The tool for studying disconfirmation discipline should itself be governed by disconfirmation discipline.

---

## 8. Limitations (honest)

- **Embedding quality caps semantic recall.** General-purpose embedding models under-represent this domain's narrow vocabulary; "diagnosticity" or "allocentric survey knowledge" may embed poorly. This is *why* the hybrid keeps keyword in the loop, and why a future fine-tuned/domain-adapted embedding would help. Watch especially for **negation failures** ("disprove not confirm" embedding near "confirm").
- **Small-graph cold-start for link prediction.** With only ~150–300 nodes initially, structural link predictors (node2vec, Adamic-Adar) are data-starved — there simply aren't enough edges to learn from, so early proposals will be noisy. Mitigate by leaning on **text/feature similarity as a node feature** (GraphSAGE) until the hand-curated edge set grows, and by treating early proposals as conversation-starters, not findings.
- **Spurious semantic links.** Vector similarity readily connects things that are *topically* near but *conceptually* unrelated (e.g. two unrelated techniques that both mention "experience"). Any semantically-suggested link must clear the graph-structure check (shared *typed* neighbours), and ultimately the human gate, before it's accepted.
- **The corpus carries real uncertainty.** The underlying research flagged genuinely contested claims (ACH's debiasing *efficacy* is disputed; the strict sequential landmark→route→survey stage model is contested; several claims passed only 2-1). These belong in the graph as `confidence` weights and explicit `CONTRADICTS` edges — the tool should *expose* disagreement, not launder it into false certainty. RQ3 (credential-reasoning cognition) had **no** verified cognition-science source, so those nodes are researcher-hypothesized and should be marked as such.
- **Human confirmation stays in the loop — permanently.** None of the above is a defect to be engineered away. The system is a *discovery aid for a researcher*, not an oracle. Its job is to propose well-justified, structurally-grounded candidate links cheaply and at scale; the researcher's job — exactly as ACH prescribes — is to try to disprove them. That division of labour is the design, not a workaround.

---

## Final recommendation (one line)

**Single-store property graph (Postgres + AGE + pgvector to start, Neo4j + GDS if link prediction becomes central), with a hybrid keyword+vector RRF *entry* layer and a graph-traversal + link-prediction *discovery* layer — because finding the right technique is retrieval, but making links between techniques is link prediction, and only the graph can do the second.**
