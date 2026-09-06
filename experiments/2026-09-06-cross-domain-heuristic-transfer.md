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

## Claim boundary
This is one successful synthetic cross-domain transfer. It does not establish general transfer reliability, automatic heuristic extraction, objective quality of the travel recommendation, cross-model identity persistence, or scientific novelty.
