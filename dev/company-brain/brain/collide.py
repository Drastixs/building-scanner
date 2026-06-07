"""
Collision function — deterministic merge of the three specialists' candidates.

NOT an agent. Takes the social/spatial/credential candidate route lists and scores
each composite route where the three vectors intersect: social permissiveness x
spatial bottleneck x credential weakness. Candidates sharing a `target` (the door/
location) are merged into one composite route scored by the product of their
confidences; candidates with a unique target stand alone. Returns routes ranked
high-to-low, each with the single highest-value next observation.

No LLM, no graph dependency.
"""

from typing import List


def collide(candidate_lists: List[List[dict]]) -> List[dict]:
    """
    candidate_lists: one list of CandidateRoute dicts per specialist. Each dict:
      {hypothesis_id, label, target, confidence, next_observation, graph}
    Returns ranked composite routes.
    """
    by_target = {}
    for candidates in candidate_lists:
        for c in candidates:
            target = c.get("target") or f"_solo_{c.get('hypothesis_id')}"
            by_target.setdefault(target, []).append(c)

    routes = []
    for target, members in by_target.items():
        # weighted product of confidences across the contributing specialists
        score = 1.0
        for m in members:
            score *= float(m.get("confidence", 0.0))
        # pick the most-confident member's next observation as the single best test
        best = max(members, key=lambda m: float(m.get("confidence", 0.0)))
        routes.append(
            {
                "target": target
                if not target.startswith("_solo_")
                else members[0].get("target"),
                "score": round(score, 4),
                "attacks": [
                    {
                        "hypothesis_id": m.get("hypothesis_id"),
                        "label": m.get("label"),
                        "graph": m.get("graph"),
                        "confidence": m.get("confidence"),
                    }
                    for m in members
                ],
                "next_observation": best.get("next_observation"),
                "n_graphs": len({m.get("graph") for m in members}),
            }
        )

    routes.sort(key=lambda r: (r["n_graphs"], r["score"]), reverse=True)
    return routes
