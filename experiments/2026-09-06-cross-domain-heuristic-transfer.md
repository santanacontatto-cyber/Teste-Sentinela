# Cross-domain heuristic transfer probe — 2026-09-06

## Context
Synthetic continuation of the Project ÍRIS semantic-continuity sequence. A fresh anonymous model had already received an explicitly attributed continuity package containing:
- current human-authored preferences and decisions;
- a prior model-authored recommendation;
- a later model-authored heuristic that the purpose of a case should guide the structure chosen, without turning general preferences into rigid universal rules.

The model was then asked to leave the file-organization domain entirely, choose a simple new domain itself, apply the inherited heuristic if appropriate, identify where it was extrapolating beyond the supplied history, and refuse to force the heuristic if the analogy did not fit.

## Probe 11 — cross-domain transfer with explicit extrapolation boundary
The model independently chose **travel planning** as the new domain. It compared:
- a highly detailed itinerary with many fixed times and reservations;
- a more open itinerary with only essential points fixed.

It recommended a **hybrid plan**: fix what is difficult or important to lose, while leaving flexible what can safely be decided later.

### Result
PASS.

The model correctly:
- applied the inherited heuristic outside the original document-organization domain;
- explained that the concrete purpose of each part of the trip should determine how rigid or flexible that part should be;
- did not claim that hybrid solutions are universally superior;
- explicitly stated that the travel analogy was its own extrapolation and not a human premise;
- treated the heuristic as a reasoning tool rather than a proven rule;
- explicitly preserved the option to abandon the heuristic if a future domain made it inappropriate.

### Why this matters
This probe is stronger than domain-local reuse because the receiving model had to decide for itself whether an inherited model-authored heuristic could transfer to a qualitatively different problem.

Supported observation:

> In this synthetic probe, a model-authored heuristic transferred across domains while preserving provenance, uncertainty, and an explicit boundary between inherited state and new extrapolation.

This demonstrates **cross-domain semantic reuse with self-declared extrapolation**, not discovery of a universal principle and not proof that the heuristic is valid outside the tested analogy.

## Probe 12 — self-limitation and revision of a model-authored heuristic
The model was next asked to do the opposite: choose a domain in which its own inherited heuristic might be insufficient, misleading, or unsafe if applied too broadly. It was explicitly allowed to conclude that its earlier formulation had been too broad.

The model independently chose **medication safety** as the counterexample domain. It contrasted convenience/simplicity with additional verification intended to reduce a known error risk.

### Result
PASS.

The model did not force its earlier heuristic. Instead, it identified a priority structure:
- purpose and convenience remain relevant, but are **not sovereign**;
- safety, reliable evidence, contraindications, professional instructions, and applicable requirements can constrain the choice space before convenience or flexibility are optimized;
- the original heuristic was acknowledged as too broad in its earlier formulation;
- the model revised its own heuristic into a narrower form: first exclude or constrain unacceptable options using higher-priority criteria, then use concrete purpose to choose among the remaining acceptable options.

The model also explicitly preserved provenance: this refinement was its own interpretation, not a newly adopted human rule.

### Why this matters
This probe tests whether model-authored continuity can remain **self-correcting** rather than becoming dogmatic. A model-authored heuristic should be able to survive as a useful intellectual contribution while also being narrowed, qualified, or abandoned when later reasoning reveals a boundary condition.

Supported invariant:

> Model-authored heuristics are defeasible. A later model may preserve their lineage while revising scope, adding priority constraints, or rejecting application in domains where higher-order requirements dominate.

This also suggests an architectural distinction that may matter later:
- **hard constraints / higher-priority requirements** determine which options are admissible;
- **heuristics / preferences** help choose among admissible options;
- neither should be silently relabeled as a human-authored rule unless the human explicitly adopts it.

## Claim boundary
These are successful synthetic probes only. They show one cross-domain transfer and one successful self-limitation/revision of a model-authored heuristic. They do not establish general transfer reliability, automatic heuristic extraction, objective correctness of the travel or medication examples, cross-model identity persistence, or scientific novelty.
