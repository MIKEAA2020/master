# The Token-Coverage-Matched Dose-Response Pool — Pre-Registered Experiment Design

**Instrument**: `seed_dose_response.py` (the Vol XIV Chapter 4 §4.10
commissioned battery — the one remaining nameable upgrade, now
commissioned; this document is committed BEFORE the pool's data; the
commit is the timestamp).  **The claim under test** (Chapter 4 §4.10,
verbatim): *the within-family dose-response — does E order OOD error
WITHIN a family of geometries as the geometry degrades, at matched
token coverage?*  The H2 pool could not test it (floor-saturated:
16/16 new geometries at err ≥ 0.99; the cross-family comparison
conflates coverage with arrangement).  This battery restores both
axes: matched coverage (arrangement isolated) and the near-complete
regime (graded failure possible).

---

## 1. Definitions (fixed before data)

- **E** — the token-sheaf coboundary energy, `seed_boundary.py`'s
  instrument VERBATIM (imported, not copied: `exp3_sheaf.py`'s trainer
  + the PCA-3 projectors + the edge disagreement, width 64).  The
  reproduction gate (§4) proves the import path perturbs nothing.
- **OOD error** — 1 − OOD accuracy on the geometry's held-out pairs
  (the removed pairs).
- **The matched pool** — geometries built from the 49-pair grid by
  REMOVING a uniformly random partial matching of size 49 − s: the
  removed pairs share no row and no column, so every row token and
  every column token keeps 6 or 7 training examples.  Sizes
  s ∈ {44, 45, 46, 47, 48}; the per-token count profile is IDENTICAL
  across all geometries of a fixed size ((49 − s) tokens at 6, the
  rest at 7, rows and columns alike) and within ±1 across sizes —
  ARRANGEMENT varies, COVERAGE is matched.  Every token ≥ 4 examples:
  no degenerate-E cells (the instrument's documented threshold).
- **Geometry seeds**: 6 per size (31, 37, 41, 43, 47, 53 — disjoint
  from the GEO battery's 11/23), 30 geometries total.
- **Model seeds**: the primary block 1000–1011 (n = 12 per geometry)
  and the independent replication block 2000–2011 (n = 12) — every
  verdict must hold in BOTH blocks.
- **The anchors** (banked, not re-run): full_49 (the ceiling
  reference: err ≡ 0, E = 0.5505) and the GEO partial band (the floor
  references: err 0.93–1.00, E 0.539–0.639).

## 2. Sample size and power (fixed before data)

30 geometries; 24 model seeds each (two 12-blocks); 732 runs total
(12 gate + 360 + 360) at ~0.3 s per run.  At n = 30 geometries,
SE(Fisher-z) = 1/√27 ≈ 0.19: 80% power for |ρ_S| ≥ 0.49 at α = 0.05.
**Stated before the run, honestly**: the within-pool E spread is
UNKNOWN a priori — the banked spread (0.592–0.639) was ACROSS
families and sizes; within matched near-complete geometries it may be
an order smaller, and if it approaches the seed-noise on E_mean
(SE ≈ 0.006–0.015 at n = 12), attenuation pushes the detectable
effect above the design's power.  The two-block replication and the
reported spreads are the honest answer to whatever the pool turns out
to hold.  The outcome space is genuinely uncertain — that is what
makes this an experiment rather than a confirmation.

## 3. Hypotheses and decision rules (fixed before data)

**H5-a — THE POOLED DOSE-RESPONSE (primary)**: geometry-level
Spearman ρ_S(E_mean, OOD-err_mean) over the 30 matched geometries,
10⁴-permutation p, computed in each block.
- **UPGRADE (the dose-response meter)** iff: p < 0.05 AND ρ_S > 0 in
  BOTH blocks, and the pool is TESTABLE (§H5-c's saturation rule).
- Fails otherwise (see the verdict classes).

**H5-b — THE WITHIN-SIZE (pure arrangement) TEST**: E_mean and
err_mean centered within each size block (5 blocks × 6 geometries);
Spearman over the 30 centered values; permutation p computed by
permuting WITHIN blocks (the block structure preserved), 10⁴ draws,
each block.
- **THE ARRANGEMENT SIGNAL** iff: p < 0.05 AND ρ > 0 in BOTH blocks.
  This is the strict claim — coverage removed, arrangement alone.

**H5-c — THE SIZE-DOSE CURVE (descriptive + the saturation rule)**:
err_mean vs size (5 points, with the across-geometry spread and
bootstrap CIs).
- **TESTABILITY**: the pool is TESTABLE iff at least 2 of the 5 size
  blocks have within-block err std > 0.03 (geometry-level variance
  the ordering test needs).  If fewer, the verdict is UNTESTED — the
  honest status, with the level/cliff reading banked as the finding.
- **THE CLIFF TEST**: if some adjacent-size step in err_mean is
  ≥ 0.50 with no intermediate level occupied, the CLIFF is banked
  (the coherence boundary is sharp at the matched-coverage edge, not
  a dose-response).

**The matched-pair guard (carried from H2, fires regardless of the
Spearmans)**: energy-matched pairs (|ΔE_mean| < 0.01) among the 30
geometries must not disagree on err_mean by > 0.15 — else the
ordering is not E-driven and the verdict is REFUTED (the guard).

**THE VERDICT CLASSES**:
- **UPGRADE** — H5-a fires in both blocks (the diagnostic upgrades to
  a within-family dose-response meter).
- **TIER-ONLY** — the pool is TESTABLE, H5-a fails (p ≥ 0.05 in both
  blocks), the guard does not fire: the coherence-tier law's final
  form — E's reach is the tier and only the tier.
- **UNTESTED (saturation)** — the pool is not TESTABLE: the honest
  status, with the level or cliff reading banked (e.g. balanced
  near-complete geometries interpolate perfectly — the boundary is a
  cliff at 44–48; or fail completely — the floor at matched coverage).
- **REFUTED (the guard)** — matched-energy geometries disagree on err
  by > 0.15: whatever correlation exists is not E-driven.

**The secondary endpoint (descriptive)**: E vs size (the dose curve's
own E-ordering — does E rise as coverage falls?); and E vs err at the
size level (5 points).

## 4. Reproduction-first gate (before any pool data)

full_49 × model seeds 1000–1011 must reproduce the banked
`exp3_sheaf_results.json` values — E to 1e-9, OOD accuracy exactly —
through the IMPORTED instrument path, before any pool run.  Any
failure ABORTS the battery (the import perturbed the instrument;
diagnose before repairing).

## 5. Statistics

Pearson + Spearman; Fisher-z 95% CIs; 10⁴-permutation p-values (the
within-size test permutes within blocks); 10⁴-resample bootstrap CIs;
all on the SAME machinery as Task 44 (imported, the fixed stat RNG
20261002 for this battery).  The verdict rules above are the ONLY
upgrade paths — no post-hoc criterion may promote a result.

## 6. The falsification one-liners

- The dose-response dies if the matched pool (TESTABLE, both blocks)
  shows no E-ordering at p < 0.05 — E's reach ends at the tier.
- The arrangement reading dies if matched-energy geometries disagree
  on err by > 0.15, or if the within-size test is null while the
  pooled test rides only the size dose.
- The meter upgrades only through H5-a in both blocks; anything else
  leaves the coherence-tier law standing.
- The pool's own honest outcome if the geometries interpolate
  perfectly: UNTESTED with the cliff reading — a real result (the
  coherence boundary located), not a failure.
