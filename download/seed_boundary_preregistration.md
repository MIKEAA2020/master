# The Seed-Level Boundary — Pre-Registered Experiment Design

**Instrument**: `seed_boundary.py` (the Vol XIV, Chapter 4 battery — this
document is committed BEFORE the experiment runs; the commit is the
timestamp).
**Commissioning critique (this session)**: *"the seed-level boundary is
the one item that sounds like a genuine scientific question ... it must
be framed as a real experiment: clear hypotheses, controls, metrics,
falsification criteria, and independent replication."*
**The claim under test**: the banked reading *"task-level ordering
perfect, seed-level correlation null"* (Vol IX second edition /
`exp3_sheaf.py`), currently an **underpowered observation** — n = 12
seeds per split, r̂ = −0.196 / −0.179, no CI, no equivalence test, no
falsification rule. It cannot be called science until it is powered,
pre-registered, and decisive.

---

## 1. Definitions (fixed before data)

- **E** — the token-sheaf coboundary energy (the `exp3_sheaf.py`
  instrument VERBATIM: per-token PCA-3 projectors of last-hidden
  activations, edge disagreement of the identity section, centered).
  Recorded at three checkpoints: E_500, E_1500, E_3000.
- **OOD error** — 1 − OOD accuracy on the split's held-out pairs.
- **Seed level** — variation across initialization seeds at FIXED split
  geometry (the only thing that varies is the MLP init seed).
- **Task level** — variation across split geometries (each geometry
  averaged over seeds).
- **Scope splits** (fixed): `compositional_16` (train a,b ∈ 0..3),
  `intermediate_36` (a,b ∈ 0..5), `random_24` (24 scattered pairs,
  geometry seed 7). Primary: `compositional_16`.
- **Controls**: `full_49` (OOD error ≡ 0 — E's seed-variance can say
  nothing where there is no OOD variance: the specificity control);
  `random_60` (near-floor OOD failure); the **independent replication
  block** `compositional_16` at a disjoint seed base (2000–2095).
- **Family sweep** (fixed): width ∈ {32, 128} at `compositional_16` and
  `intermediate_36` (H4's invariance test).
- **Geometry sweep** (fixed): 16 new random geometries — sizes
  {16, 20, 24, 28, 32, 36, 40, 44} × geometry seeds {11, 23}, 12 model
  seeds each. The pool for H2 and the energy-matched pair analysis.

## 2. Sample size and power (fixed before data)

n = 96 seeds per scope split; 48 per control/family cell; 12 per
geometry. SE(Fisher-z) = 1/√93 = 0.104 at n = 96: 80% power for
|ρ| ≥ 0.28 at α = 0.05 (two-sided); the TOST equivalence test at
δ = 0.30 has ≈ 90% power when the true |ρ| ≤ 0.10. **Stated before the
run**: if the true seed-level association is ≈ −0.2 (the n = 12 point
estimate), the expected verdict is the NARROWED zone — a weak negative
association below practical predictivity, NOT a clean null. The
experiment is designed to tell these apart, which n = 12 could not.

## 3. Hypotheses and decision rules (fixed before data)

**H1 — THE SCOPE LAW** (E is a task-geometry diagnostic, not a
seed-level predictor). Primary endpoint: seed-level Pearson ρ(E_3000,
OOD error) within each scope split.
- **UPGRADE TO LAW** iff: TOST at δ = 0.30 succeeds (both one-sided
  p < 0.05) in EVERY scope split with OOD-error std > 0.02, AND no
  scope split shows |ρ̂| ≥ 0.30 with permutation p < 0.01.
- **REFUTATION** (E IS a seed-level signal) iff: some scope split has
  |ρ̂| ≥ 0.30 AND permutation p < 0.01 AND the independent replication
  block confirms sign and p < 0.05.
- **NARROWED** (the honest middle): otherwise — report the CIs; the
  boundary stands as measured-but-not-closed, with the CI as the bound.

**H2 — THE TASK-LEVEL LAW** (E orders geometries as their OOD errors).
Endpoint: geometry-level Spearman ρ(E_mean, OOD-err_mean) over the 20
geometries (16 new + 4 original), permutation p (10⁴).
- **HOLDS** iff p < 0.05. **REFUTED** iff p ≥ 0.05 OR an
  energy-matched pair exists (|ΔE_mean| < 0.01) with |ΔOOD| > 0.15.

**H3 — THE MISSING-COVARIATE TEST** (some training-dynamics covariate
carries the seed-level signal E does not). Panel (fixed): E_500,
E_1500, log-loss at steps 100/300/1000, final train NLL, the
gradient-norm mean and std over the last 500 steps, and
wrong-OOD-confidence. Within each scope split vs OOD error.
- **UPGRADE** (a seed-level predictor is found) iff: some covariate has
  |ρ| ≥ 0.50, permutation p < 0.01, BH-FDR q < 0.05 across the panel,
  replicated (same sign, p < 0.05) in ≥ 2 of the 3 scope splits.
- Otherwise the panel is banked as a **negative** — the scope reading
  strengthens (H1 + H3 jointly: no measured covariate of this family
  predicts seed-level OOD luck either).

**H4 — FAMILY INVARIANCE**: the H1 verdict (whatever it is) replicates
at width 32 and 128 at fixed geometry. Report per-width CIs; invariance
holds iff the verdict class is identical at all widths.

**Secondary endpoint** (same rules as H1): E vs wrong-OOD confidence
(the hallucination measure — the chat's original prediction).

## 4. Reproduction-first gate (before any new data)

The first 12 seeds (1000–1011) of every original split must reproduce
the banked `exp3_sheaf_results.json` values — E to 1e-9, OOD accuracy
exactly. Any failure ABORTS the battery (instrument drift; diagnose
before repairing). The pooled "split-dominated" correlation is
recomputed at the new n as the confound quantification.

## 5. Statistics

Pearson + Spearman; Fisher-z 95% CIs; 10⁴-permutation p-values;
10⁴-resample bootstrap CIs; TOST at δ = 0.30; BH-FDR across the H3
panel. All hand-rolled on numpy (no scipy dependency). Two-sided
unless stated. The verdict rules above are the ONLY upgrade paths —
no post-hoc criterion may promote a result.

## 6. The falsification one-liners

- The scope law dies if E predicts seeds at |ρ| ≥ 0.3 with p < 0.01,
  replicated.
- The task-level law dies if matched-energy geometries disagree on OOD
  by > 0.15, or the geometry-level ordering loses significance.
- The covariate reading dies if the whole panel stays under the
  upgrade bar with adequate power.
- The boundary becomes a LAW only through H1's TOST; anything else
  leaves it open with a measured bound.
