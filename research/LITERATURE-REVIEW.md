# The Web of Connections: Cognitive and Learning Mechanisms in Physical Red-Team Reasoning

*A PhD literature review on the epistemics of expert physical security assessment*

---

## Abstract

This review synthesises the cognition and learning-science literature relevant to how expert physical penetration testers ("red teamers") form, test, and reinforce a *web of connections* — the linked mental representation that fuses people, building spaces, and access-control credentials into an actionable model of a target during an authorised security assessment. The focus is deliberately epistemic and pedagogical: how theories about a target are generated, validated, and consolidated across an engagement and a career, **not** tooling and not intrusion procedure. No published study empirically examines the cognition of physical red teamers; the entire evidence base is drawn from adjacent high-stakes domains. I therefore assemble a theoretically motivated stack from four literatures: (1) Naturalistic Decision Making (NDM) and Recognition-Primed Decision making (RPD) for **theory formation**; (2) intelligence-analysis tradecraft — chiefly Heuer's Analysis of Competing Hypotheses (ACH) and his "spider web of memory" metaphor — for **theory testing**; (3) spatial-cognition theory and space-syntax graph theory for the **building sub-model**; and (4) Cognitive Task Analysis, specifically the Critical Decision Method (CDM), as the **elicitation** instrument for collecting the missing empirical data. Throughout I distinguish verified claims from inferences, flag two contested points (ACH's debiasing efficacy and the sequential spatial-stage model), and identify the boundary condition under which expert advantage collapses. The central claim of the review is that these frameworks are individually well-established but have never been validated against real practitioners; doing so is the PhD's contribution.

---

## 1. Introduction

A physical security assessment asks a single expert (or small team) to convert fragmentary, ambiguous information — an open-source footprint, an aerial photograph, a few hours of on-site observation — into a working theory of how an organisation can be physically compromised. That theory is not a list; it is a *web*. People are linked to roles, roles to access rights, access rights to credentials, credentials to readers, readers to doors, doors to spaces, spaces to paths, and paths back to the people who traverse them. The expert builds this web from incomplete cues, probes it with low-commitment tests, and revises it continuously. The construct of interest in this review is precisely that web of connections and the cognitive machinery that produces it.

Physical red-teaming is a revealing case of expert cognition for three reasons. First, it is a *high-consequence, time-pressured, low-information* task — the canonical conditions under which naturalistic (as opposed to classical-rational) decision making has been studied. Second, it is *adversarial and hypothesis-driven*: the practitioner is not merely perceiving an environment but actively theorising about a designed system that other professionals built to resist exactly this scrutiny. Third, the expertise is overwhelmingly *tacit* — practitioners can do far more than they can articulate, which makes the field a natural site for cognitive task analysis.

The scope of this review is the **epistemics and learning mechanisms** of that work: how a theory of the target is *formed*, *tested*, and *reinforced*. It is explicitly **not** about tools, hardware, software, or step-by-step intrusion methods. Where a mechanism could be read as procedural, I treat it strictly at the level of reasoning and learning.

A caveat governs the entire document and is stated once here, in full force: **every source below comes from an adjacent domain** — intelligence analysis, aviation, firefighting, emergency response, spatial navigation, architecture — and **none empirically studies physical red teamers**. The mapping onto red-team cognition is theoretically motivated and, in the judgement of the verification process behind this review, reasonable rather than overreaching; but it is an inference, not a measured fact about this population. Validating the stack against real practitioners is the proposed contribution (Section 11).

---

## 2. A Unifying Frame: Link Analysis and Attack-Graph Reasoning over Physical Space

Before mapping individual cognitive theories it helps to name the *form* of the artefact the red teamer is building. Across intelligence and security practice, the relevant representation is a **graph**: nodes and the links among them, reasoned over to find paths. The web of connections is usefully decomposed into three fused graphs that the practitioner maintains simultaneously:

- a **social graph** — people, their roles, trust relationships, and routines (entity resolution and relationship inference);
- a **spatial graph** — spaces, barriers, and paths through the building (Section 6);
- a **credential / access-control graph** — readers, the technologies they speak, the credentials that satisfy them, facility codes, privilege tiers, and the physical-to-logical bridges between them.

The expert's task is to find a traversal across all three: a person whose credential opens a reader on a door along a path to a target space. This is structurally an **attack-graph / link-analysis** problem, and it is why the intelligence-analysis literature on building and testing networks of inference (Section 5) transfers so naturally. The three subgraphs are not independent — a credential is meaningless without the person who carries it and the door it opens — and the cognitive challenge is precisely the *fusion*. The review now treats formation, testing, the spatial sub-model, and reinforcement in turn.

---

## 3. Theory Formation: NDM, Recognition-Primed Decisions, Sensemaking, and Schema

### 3.1 Recognition-Primed Decision making (RPD)

The best-supported account of how an expert *forms* an initial theory under time pressure is Klein's **Recognition-Primed Decision** model, the cornerstone of the Naturalistic Decision Making tradition [1]. In RPD the expert does not enumerate and compare options. Instead they pattern-match the present situation against a deep store of prior experience, *recognise* it as an instance of a familiar type, and thereby generate **a single plausible course of action**, which is then evaluated by **mental simulation** — imagining the action play out and proceeding if it works, modifying it if it does not. In Klein's canonical fireground-commander studies, a single recognised option was generated this way in the large majority of cases. This is a stable, textbook model; critiques target its scope of applicability, not the underlying pattern-matching-plus-mental-simulation characterisation [1].

Mapped to red-teaming, RPD predicts that an experienced practitioner, on seeing a particular reader bezel, lanyard colour, lobby layout, or smoker's door, does not run a decision tree but *recognises a pattern* ("this is a tailgate-friendly multi-tenant lobby") and immediately has a candidate plan, which they then run forward mentally before committing. This is a **verified framework but an inferred application** to red teamers.

### 3.2 Sensemaking and the Data-Frame theory

RPD describes choosing an action; **sensemaking** describes constructing the situation model that recognition operates on. The NDM literature treats sensemaking as the cognitive act of converting incomplete and ambiguous cues into a coherent, actionable interpretation under uncertainty and time pressure [1][2]. Klein, Phillips, Rall and Peluso's **Data-Frame theory** formalises this as a reciprocal process: incoming data are interpreted by being fitted into a **frame** (a structure that organises and gives meaning to the data), while the frame is itself revised by the data — together used to "build a coherent picture out of chaos" [2]. This connects to Endsley's situation-awareness construct and to Weick's organisational sensemaking. For the red teamer, sensemaking is the process of turning a scatter of OSINT fragments and on-site observations into a working picture of "how this place runs," and the frame is what tells them which incoming cue matters.

### 3.3 Intuition as accumulated pattern recognition

The NDM tradition defines expert **intuition** not as mysterious insight but as the *output of pattern recognition*: "large numbers of patterns gained through experience, resulting in different forms of tacit knowledge" [3]. Intuition is strengthened by "a broader experience base that lets people build better tacit knowledge, such as perceptual skills and richer mental models" [3]. This is the career-long inference engine: the more (relevant) situations an expert has encountered, the larger the pattern store that recognition draws on, and the more perceptually discriminating they become. It directly motivates the reinforcement question of Section 7.

### 3.4 Schema/frame-driven cognition

Underlying all three is **schema theory**. Kaste's analysis of the Data/Frame model states that experts use "cognitive frameworks, alternatively referred to as schemas, templates, scripts, frames and models, to effectively perceive, interpret, understand, recall, and anticipate information," and that these frameworks "capture past experience in ways that support rapid pattern recognition, adaptive responses and proactivity" [4]. Schemas are thus the *medium* in which the web of connections is stored and the mechanism that makes rapid recognition (3.1), coherent sensemaking (3.2), and intuition (3.3) possible. A red teamer's schema for "corporate campus access control" is what lets them anticipate where a loading dock, a server room, or a badge reader will be before they have seen it — anticipation being the operationally critical affordance schemas provide.

**Confidence note.** Sections 3.1–3.4 rest on verified, mutually corroborating sources [1][2][3][4]. Their *application to red teamers specifically* is an inference, well motivated but unvalidated.

---

## 4. (Reserved) — see Section 3

*Theory formation is treated as a single coherent block in Section 3; the testing apparatus follows.*

---

## 5. Theory Testing: Competing Hypotheses, Diagnosticity, Disconfirmation, and the Spider Web of Memory

If RPD and sensemaking describe how a theory is *born*, the intelligence-analysis tradecraft of Richards Heuer describes how it should be *interrogated* — and supplies the single most on-point metaphor for the construct this PhD studies.

### 5.1 Analysis of Competing Hypotheses (ACH)

Heuer's **Analysis of Competing Hypotheses**, set out in *Psychology of Intelligence Analysis* (CIA) [5], is an eight-step procedure built to counter the natural human tendency to fixate on a single favoured explanation. The analyst (1) enumerates **all reasonable alternative hypotheses**, (2) lists the relevant evidence and arguments, (3) builds a **matrix with hypotheses as columns and evidence as rows**, and assesses, for each cell, whether the evidence is consistent or inconsistent with that hypothesis. The decisive moves are two. First, the analyst proceeds **by trying to disprove hypotheses rather than to prove them** [5] — a hypothesis survives by resisting refutation, not by accumulating supportive points. Second, evidence is weighted by **diagnosticity** — its power to *discriminate among* the competing hypotheses — **not by quantity** [5]; a single highly diagnostic item outweighs a pile of evidence consistent with everything. The matrix structure (rows = evidence, columns = hypotheses) and the explicit-enumeration prescription are independently confirmed by the National Academies' treatment and the US Government's *Tradecraft Primer* [6][7]. The method is codified, alongside 65 other structured techniques, in Heuer and Pherson's *Structured Analytic Techniques for Intelligence Analysis* [8].

For the red teamer, ACH is the disciplined version of "what are all the ways into this building, which evidence would distinguish them, and which one survives my attempts to rule it out?" It externalises the web's competing path-hypotheses into a matrix and forces attention onto discriminating evidence.

> **Contested point — state plainly.** ACH's *descriptive* procedure is solid and well-attested. Its *efficacy as a debiasing tool* is empirically disputed: controlled studies (Dhami et al. 2019; van Gelder and colleagues; Maegherman et al. 2021) have failed to show that ACH reliably reduces confirmation bias relative to unstructured analysis [5–8, caveat]. This review therefore presents ACH as a **descriptive model of disciplined hypothesis testing**, not as a proven cognitive corrective. Whether structured disconfirmation actually improves red-team accuracy is itself an open empirical question (Section 11).

### 5.2 Hypothesis-driven observation and absence-as-evidence

A corollary of ACH reframes reconnaissance itself. Effective observation is **not passive**: discriminating signal from noise requires a prior set of hypotheses that direct attention. Heuer instructs the analyst, for each hypothesis, to ask "If this hypothesis is true, what should I expect to be seeing or *not* seeing?" and to "note the absence of evidence as well as its presence" — invoking Conan Doyle's dog that "did not bark in the night" as the paradigm of diagnostic absence [5]. Wohlstetter's classic formulation, cited by the National Academies, is that effective observation needs "not only an ear, but a variety of hypotheses that guide observation" [7].

This is the concrete inference heuristic behind on-site recon: OSINT-derived priors generate expectations, and on-site observation tests them, with the **non-appearance of an expected indicator** (no visible cameras where policy would demand them; no badge check at a door that should be controlled) treated as genuinely diagnostic. It also dissolves the apparent gap between desk research and field work — the field observations are *structured by the priors* rather than gathered blind.

### 5.3 The spider web of memory

Heuer supplies the review's most on-point citation for the very construct under study. Describing creativity, openness, and the breaking of established mind-sets, he writes (Ch. 3, verbatim): all of these "involve **spinning new links in the spider web of memory — links among facts, concepts, and schemata that previously were not connected or only weakly connected**" [5]. This is, almost literally, a cognitive description of *building and revising a web of connections*: new analytic insight is the forging of previously absent or weak links, and mind-set-breaking is the deliberate re-wiring of that web. For a thesis named after the web of connections, this is the keystone citation — it grounds both the building of new links (formation) and the breaking of entrenched ones (revision) in a single, authoritative source.

---

## 6. The Spatial Sub-Model: Landmark/Route/Survey Knowledge and Space-Syntax Depth

The spatial graph deserves its own treatment because it has its own mature literature.

### 6.1 Landmark, route, and survey knowledge

Human navigation knowledge is classically organised into three types [9][10]. **Landmark knowledge** is recognition of salient features. **Route knowledge** is sequential, egocentric path-following between decision points ("at the lobby turn left, the lifts are past the desk"). **Survey knowledge** is an allocentric, map-like, metric representation that supports novel inference such as shortcuts and bearings. Werner et al. proposed this taxonomy for human and robot navigation [10]; Brunyé et al. confirm the three types and, importantly, document **large individual differences** — some people acquire survey knowledge almost immediately, others never do [9].

> **Contested point — state plainly.** The strict *sequential stage* hypothesis — that knowledge obligatorily progresses landmark → route → survey — is **contested**. Route and survey knowledge can develop in parallel, and the "hierarchical" framing reflects the older Siegel & White school rather than settled consensus (Montello 1998) [9, caveat]. This review therefore treats landmark/route/survey as **distinct knowledge types that can develop in parallel**, not an obligatory progression. The *taxonomy* is robust; the *staging* is not.

For red-teaming, this predicts that a practitioner's building model is heterogeneous: parts known only as landmarks, parts as memorised routes, and (for the strongest practitioners or best-reconned buildings) parts as true survey knowledge supporting novel-path inference — exactly the capability needed to reason about an entry the defender did not anticipate.

### 6.2 Space-syntax depth as a reachability metric

Spatial cognition describes the *form* of the mental map; **space syntax** (the Hillier & Hanson lineage) supplies a **quantitative, falsifiable** metric for the property the red teamer most cares about: how reachable a target space is. In space syntax, **depth** between two spaces is "the least number of syntactic steps in a graph that are needed to reach one from the other," and **accessibility is inversely related to depth** — "access is easy in structures with a low depth value and difficult in structures with a high depth value" [11].

This gives the spatial graph a measurable observable. A target space's depth from the public entrance is a concrete proxy for how hard it is to reach, and the practitioner's *estimate* of that depth (versus its true value) becomes a measurable quantity in a learning study — a way to ask whether experts build more accurate reachability models than novices. Known critiques of space syntax target axial/visibility analysis at *urban* scale, not the depth–accessibility relationship at *building* scale, which is what is relevant here [11].

---

## 7. Theory Reinforcement Across a Career

How does the web of memory get *built and consolidated* over years? The NDM account (Section 3.3) is that intuition grows with the experience base [3]. But the literature attaches a sharp qualification.

### 7.1 The right experience, not mere tenure

Klein frames expertise as improved by *broadening the experience base* so practitioners build better tacit knowledge, perceptual skills, and richer mental models — an experiential, situated-learning claim rather than a rule-teaching one [3][4]. The verified caveat is decisive for a learning study: **raw tenure does not reliably improve accuracy.** Drawing on Ericsson's deliberate-practice tradition and Kahneman & Klein's (2009) joint paper, skilled intuition forms only in **high-validity environments** (regular, learnable structure) with **structured practice and timely, accurate feedback** [3, caveat]. Where those conditions are absent, years of experience can breed confidence without competence. This reframes the central learning question from "how long have they done it?" to "what is the *feedback structure* of their practice?"

### 7.2 The under-sourced apprenticeship angle — a flagged gap

The research questions behind this review named two further frameworks for career-long learning: **Lave and Wenger's** communities of practice / legitimate peripheral participation, and **Schön's** reflective practitioner. The mentorship-debrief-apprenticeship structure of red-team learning — shadowing senior operators, post-engagement debriefs, war stories as a knowledge-transfer medium — maps naturally onto both. **However, neither framework was directly sourced in the verified evidence set.** I therefore flag the social-learning and reflective-practice account of red-team enculturation as **named but unsourced** — a genuine theoretical gap and a clear research opportunity (Section 11), not an established result.

---

## 8. Failure Modes and the Boundary Condition

A learning study needs a *contrast baseline*: the characteristic errors that distinguish poor reasoning from expert reasoning. The intelligence-analysis literature supplies a well-attested catalogue [5][6].

- **Satisficing** — accepting the first "good enough" hypothesis instead of testing alternatives. Heuer identifies three weaknesses flowing from it [5].
- **Selective perception** — once a working hypothesis is held, it acts as a *perceptual filter*: "a hypothesis functions as a perceptual filter," so the analyst sees what they are looking for and misses the rest [5].
- **Failure to generate the full hypothesis set** — the true explanation is never tested because it was never listed [5].
- **Confirmation bias** — weighting confirming over disconfirming evidence (the exact tendency ACH is built to counter) [5].
- **Premature convergence / mindset / groupthink** — a team "prematurely converges on one hypothesis... then confirms that hypothesis by seeking out supportive data... rather than seeking data that might disprove it" [6].

These define what *novice* or *undisciplined* red-team reasoning should look like, and give a learning study its dependent variables: does training or experience move practitioners *away* from satisficing and selective perception and *toward* full-set generation and disconfirmation?

### The boundary condition: expertise collapse on ambiguous cues

The single most important caveat against over-claiming expert superiority is this: **expertise advantage collapses under ill-structured, ambiguous cues.** The National Academies, citing Devine & Kozlowski (1995), report that experts outperform novices with *well-structured* cues but perform **no better than novices** on ill-structured tasks of the kind typical of intelligence analysis [6]. This converges with Kahneman & Klein (2009) on high- versus low-validity environments and with Shanteau (1992). The implication for this PhD is twofold: it explains *why* structured techniques and disconfirmation discipline are prescribed (they are scaffolding for exactly the conditions where intuition fails), and it warns against assuming experienced red teamers are reliably better than novices in the most ambiguous recon judgements. Whether physical security assessment is a high-validity domain (where genuine skilled intuition can form) or a low-validity one (where experience breeds overconfidence) is itself unresolved (Section 11). *(This claim carried one dissenting vote in verification; the dissent concerned framing, and the claim self-scopes the collapse to low-validity domains.)*

---

## 9. How To Apply Each Technique in This Research

This section is operational: for each framework, what it looks like *when studying or training a red teamer*, how to instrument it, and what artefacts it yields.

**Recognition-Primed Decision making (RPD).** *Use it as a coding scheme for decision episodes.* When analysing a recorded or recalled engagement, segment the reasoning into recognition events and mark, for each, whether the practitioner generated a single recognised option (RPD-consistent) or compared several (analytical). Instrument it by prompting, at each decision point, "What did you see that told you what to do?" and "Did you consider other options, or did one just seem right?" *Artefact:* an annotated decision timeline tagging each choice as recognition-driven vs. deliberative, with the cues that triggered recognition — a direct test of whether red-team formation is RPD-shaped.

**Sensemaking / Data-Frame.** *Use it to trace frame evolution.* Track which **frame** the practitioner holds at each phase ("this is a lax single-tenant office") and the data that shifted it. Instrument by asking what picture they had at OSINT stage, what surprised them on site, and what they re-interpreted. *Artefact:* a frame-revision log — a sequence of (frame, triggering datum, revised frame) tuples — showing how chaos was resolved into a coherent picture and where it was resisted.

**Analysis of Competing Hypotheses (ACH).** *Use it as both a probe and an intervention.* As a probe: reconstruct, post hoc, the set of entry hypotheses the practitioner actually held and build the evidence-by-hypothesis matrix to see whether they reasoned diagnostically or confirmatorily. As an intervention (a training study): teach ACH and measure whether full-set generation and disconfirmation increase. *Artefact:* the populated ACH matrix (hypotheses × evidence, scored for consistency and diagnosticity). **Caveat:** because ACH's debiasing efficacy is contested, treat any improvement as a finding to be demonstrated, not assumed.

**Hypothesis-driven observation (absence-as-evidence).** *Use it to score recon discipline.* For each on-site observation, capture whether the practitioner had a *prior expectation* ("I expected a guard here") and whether **absences** were treated as informative. Instrument with "Before you looked, what did you expect to see — or not see?" *Artefact:* an expectation-vs-observation ledger, with diagnostic absences flagged ("no badge check at the side door"), measuring how much observation was theory-laden versus passive.

**Critical Decision Method (CDM).** *Use it as the primary data-collection instrument* (Section 10). It is how the study obtains the raw decision episodes that the schemes above annotate. *Artefact:* Situation Assessment Records, an incident timeline, and a decision-requirements table — the externalised tacit reasoning of one real engagement.

**Space-syntax depth.** *Use it to quantify the spatial mental model.* Have the practitioner sketch or describe the building's connectivity, derive the **depth** of target spaces from their model, and compare against ground-truth depth from floor plans. *Artefact:* a justified-graph of the practitioner's spatial model with depth values, and an accuracy score (estimated vs. true depth) — a falsifiable measure of how good their reachability model is and how it improves with expertise.

**Schema elicitation.** *Use it to surface the templates behind recognition.* Through contrast cases (novice vs. expert on the same site) and "what would you expect here?" anticipation probes, draw out the schemas a practitioner brings to a building *type*. *Artefact:* a catalogue of named schemas ("multi-tenant lobby," "campus loading dock") with their associated expectations and affordances — the content of the pattern store that RPD draws on.

---

## 10. Elicitation Methodology: The Critical Decision Method

Because no empirical data on red-team cognition exists, the study must generate it, and the verified method of choice is **Cognitive Task Analysis** via the **Critical Decision Method (CDM)** [12][1]. CDM is a structured, retrospective interview technique for eliciting the tacit decision-making of experts around a **single, specific, challenging past incident** (here: one real engagement). Its defining features are:

- **Multiple-pass retrospection.** The practitioner recounts the incident several times, each pass at a different level of detail — first an unstructured account, then a structured timeline, then probe-driven deepening, then a "what if" / expert-novice contrast pass [12].
- **Probe questions.** A set of cognitive probes (about cues, goals, expectations, options considered, situation assessment, and what an inexperienced person would have missed) guides the deepening. The probes are best described as **semi-structured and tailorable**, not a strictly fixed script [12, caveat].
- **Concrete artefacts.** CDM yields **Situation Assessment Records, timelines, and decision-requirements tables** [12] — externalised representations of the expert's reasoning that feed directly into the coding schemes of Section 9.

CDM is a current, validated CTA method applied across aviation, medicine, and emergency response [12][13], which is precisely the adjacent-domain pedigree the present study seeks to extend to physical red teaming. A multi-pass CDM protocol over a corpus of authorised engagements, augmented with novice-vs-expert contrast and spatial-sketch tasks, is the natural empirical core of the thesis.

---

## 11. Gaps and Contribution

**The domain-transfer gap (the master caveat).** Every framework above is verified in an adjacent domain and *none* has been tested on physical red teamers. This is not a weakness of the review but the **statement of the contribution**: the thesis validates (or refutes, or refines) this stack against real practitioners via CDM. The frameworks are the hypotheses; the red teamers are the test.

**The credential-reasoning gap (RQ3).** The cognition literature has **nothing** to say about how a practitioner builds the credential/access-control sub-model — reader model → RF technology → clonability → facility code → privilege tier → physical-to-logical bridge. No verified source covers it. This leaves a sharp open question: is credential reasoning the *same* RPD/schema pattern-matching as the rest of the web, or is it a more **deliberate, analytic, fault-tree style** of reasoning distinct from sensemaking? Determining which is a self-contained, publishable contribution.

**The social-learning gap (Lave & Wenger / Schön).** As flagged in Section 7.2, communities of practice, legitimate peripheral participation, and reflective practice were named but never sourced. The apprenticeship/mentorship/debrief structure through which red-team expertise is transmitted is **under-theorised**, and characterising it empirically is a clean research opportunity.

**The high- vs low-validity open question.** Given that expertise collapses on ambiguous cues (Section 8), the field's status is unresolved: is physical security assessment a **high-validity** domain in which genuine skilled intuition forms, or a **low-validity** one in which experienced operators are systematically overconfident relative to their accuracy? The answer determines whether the field should lean on intuition or on structured disconfirmation — a question with both theoretical and practitioner-training stakes.

Taken together, the contribution is to take a coherent, well-attested but *untested-here* cognitive stack and subject it to its first empirical confrontation with the population it purports to describe — closing the domain-transfer gap, resolving the credential-reasoning question, and theorising the apprenticeship structure that current sources leave dark.

---

## 12. References

Sources marked *(paywall/mirror)* returned restricted access during verification and were corroborated via secondary sources or mirrors; their content is confirmed but was not all read in full directly.

1. Cambridge Handbook of Expertise and Expert Performance — *Expert Professional Judgments and Naturalistic Decision Making* (RPD, sensemaking, CDM). https://www.cambridge.org/core/books/abs/cambridge-handbook-of-expertise-and-expert-performance/expert-professional-judgments-and-naturalistic-decision-making/2B5113B9D384CFFE9B2F9265A0A71EE2

2. Klein, Phillips, Rall & Peluso — Data-Frame Theory of sensemaking (and Klein 2015, *JARMAC*, on intuition). https://www.sciencedirect.com/science/article/pii/S2211368115000364

3. Klein (2015), *Journal of Applied Research in Memory and Cognition* — intuition as experience-built pattern recognition; experiential vs. rule-based learning. https://www.sciencedirect.com/science/article/pii/S2211368115000364

4. Kaste (2012), Embry-Riddle Aeronautical University dissertation — Data/Frame model; schema/template/script/frame cognition. https://commons.erau.edu/cgi/viewcontent.cgi?article=1086&context=edt

5. Heuer, R. J. — *Psychology of Intelligence Analysis* (CIA): ACH (8 steps, disprove-not-confirm, diagnosticity), absence-as-evidence, the spider-web-of-memory metaphor, satisficing/selective-perception failure modes. *(paywall/mirror)* https://www.cia.gov/resources/csi/books-monographs/psychology-of-intelligence-analysis-2/

6. National Academies (2011), *Intelligence Analysis for Tomorrow* — ACH matrix structure; mindset/groupthink/premature convergence; expertise collapse on ill-structured cues (citing Devine & Kozlowski 1995). https://nap.nationalacademies.org/read/13040/chapter/5

7. National Academies / US Government *Tradecraft Primer* (2009) — explicit hypothesis enumeration; Wohlstetter on hypothesis-guided observation. https://www.nationalacademies.org/read/13062/chapter/8

8. Heuer, R. J. & Pherson, R. H. (2019), *Structured Analytic Techniques for Intelligence Analysis*, 3rd ed., CQ Press/SAGE — 66 techniques including ACH and Multiple Hypothesis Generation. *(paywall/mirror)* https://us.sagepub.com/en-us/nam/structured-analytic-techniques-for-intelligence-analysis/book255432

9. Brunyé et al. (2020), *Cognitive Research: Principles and Implications* — landmark/route/survey types; large individual differences; critique of obligatory sequential staging. https://link.springer.com/article/10.1186/s41235-020-00213-w

10. Werner et al. (1997) — *Spatial Cognition: The Role of Landmark, Route and Survey Knowledge in Human and Robot Navigation*. https://www.researchgate.net/publication/37931583_Spatial_Cognition_The_Role_of_Landmark_Route_and_Survey_Knowledge_in_Human_and_Robot_Navigation

11. Space-syntax paper (Hillier & Hanson lineage), *Journal of Asian Architecture and Building Engineering* (2023) — depth defined as least syntactic steps; accessibility inversely related to depth. *(paywall/mirror)* https://www.tandfonline.com/doi/full/10.1080/13467581.2023.2292083

12. Hoffman, Crandall & Shadbolt (1998), *Human Factors* 40(2) — CDM: multiple-pass retrospection, probe questions, Situation Assessment Records / timelines / decision requirements. https://journals.sagepub.com/doi/10.1518/001872098779480442

13. Gary Klein — Critical Decision Method overview (Klein, Calderwood & MacGregor 1989 lineage). https://www.gary-klein.com/cdm

14. Lave, J. & Wenger, E. — communities of practice / legitimate peripheral participation *(named in research questions; not directly sourced in the verified evidence set — flagged as a gap)*. https://infed.org/dir/welcome/jean-lave-etienne-wenger-and-communities-of-practice/

**Contested-efficacy references (cited in-text, Section 5.1, via the verification caveat; not in the primary verified set):** Dhami et al. (2019); van Gelder and colleagues; Maegherman et al. (2021) on the disputed bias-reduction efficacy of ACH. **Reinforcement-caveat references (Section 7.1):** Kahneman & Klein (2009) on high- vs low-validity environments; Ericsson on deliberate practice; Shanteau (1992). These are named in the verified caveats but were not themselves the subject of independent verification.
