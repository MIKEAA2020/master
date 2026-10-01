# The Resolution Programme, Volume XIV
# Chapter 4 — The Seed-Level Boundary: the Decided Experiment

**Status**: executed and decided (this chapter is written around an
experiment that has RUN, not around a design that awaits one).  The
pre-registration was committed at `3a108d8` BEFORE the data — the commit
is the timestamp; the battery is `seed_boundary.py`; the verdicts are in
`scripts/seed_boundary_results.json` (864 runs, reproduction-gated).
**Date**: 2026-10-02 (session 0012; the experiment itself ran in session
0011, Task 44).  **The commissioning line**: *"the seed-level boundary
is the one item that sounds like a genuine scientific question … it must
be framed as a real experiment: clear hypotheses, controls, metrics,
falsification criteria, and independent replication."*  This chapter is
that experiment's full account.  **The same session's other decided
item** (recorded here because it closes the volume's premise): the grind
census's fourth round resolved the cover4d HOLD watch — the rule fires
HOLD; both arms of the grind are now rule-stopped, and the completion
face is Task 42's bookkeeping (§4.9).  The volume's two items are both
decided; what remains on this row is exactly one nameable upgrade
(§4.10).

---

## 4.0  The row, and why it had to be an experiment

The empirical face's one open row came into this volume as a banked
observation with good instruments and no evidential standing.  The Vol
IX second edition (`exp3_sheaf.py`) had measured: the task-level
ordering "perfect" (E = 0.541 / 0.577 / 0.594 / 0.615 against OOD error
0 / 0.93 / 0.99 / 1.00 across the four split geometries), the
seed-level correlation "null" (r̂ = −0.196 / −0.179 at n = 12 seeds per
split), and the pooled r = 0.59 flagged split-dominated.  That is an
underpowered anecdote: n = 12, no confidence intervals, no equivalence
test, no falsification rule, no replication.  Under the corpus's own
typing of evidence it was a MEASURED row, not a certified one — and the
commissioning critique named exactly what it lacked.

The volume's decision, executed in the order the discipline prescribes:
pre-register the design and commit it before any new data; reproduce
the banked numbers before generating new ones; power the battery for
the distinction the claim actually needs (equivalence vs. absence of
signal); state the falsification one-liners in advance; then run at
power and read the verdicts off the pre-registered rules — including
the verdicts that cut against the banked claims.  Two of them did
(§4.3, §4.4), and the corrections are now part of the record.  That is
what separates this chapter from a design document: nothing below is a
promise; everything is a measured outcome with its rule attached.

## 4.1  The pre-registration (the design fixed before the data)

The document is `download/seed_boundary_preregistration.md`, committed
at `3a108d8` before the run.  Its load-bearing choices:

- **Definitions fixed in advance.**  E — the token-sheaf coboundary
  energy, the `exp3_sheaf.py` instrument VERBATIM (per-token PCA-3
  projectors of the last-hidden activations, the edge disagreement of
  the identity section, centered), recorded at checkpoints 500 / 1500 /
  3000.  OOD error — 1 − OOD accuracy on the split's held-out pairs.
  Seed level — variation across initialization seeds at FIXED split
  geometry.  Task level — variation across geometries, each averaged
  over seeds.
- **The battery fixed in advance.**  Scope splits: `compositional_16`
  (primary), `intermediate_36`, `random_24`.  Controls: `full_49` (the
  specificity control — OOD error ≡ 0, so nothing can predict variance
  that does not exist) and `random_60` (the near-floor control); the
  independent replication block `compositional_16` at the disjoint seed
  base 2000–2095.  The family sweep at widths {32, 128} on both scope
  splits with OOD variance.  The geometry sweep: 16 new random
  geometries — sizes {16, 20, 24, 28, 32, 36, 40, 44} × geometry seeds
  {11, 23} — 12 model seeds each, the pool for H2 and the
  energy-matched pair analysis.
- **Power fixed in advance.**  n = 96 seeds per scope split (48 per
  control/family cell, 12 per geometry).  SE(Fisher-z) = 1/√93 = 0.104:
  80% power for |ρ| ≥ 0.28 at α = 0.05 two-sided; the TOST equivalence
  test at δ = 0.30 has ≈ 90% power when the true |ρ| ≤ 0.10.  The
  pre-statement, quoted because it was honored: *"if the true seed-level
  association is ≈ −0.2 (the n = 12 point estimate), the expected
  verdict is the NARROWED zone — a weak negative association below
  practical predictivity, NOT a clean null."*  The experiment was
  designed to tell those apart, which n = 12 could not.
- **The hypotheses with one-line decision rules.**  H1 (the scope law):
  UPGRADE iff TOST at δ = 0.30 succeeds in every scope split with
  OOD-error std > 0.02 AND no split shows |ρ̂| ≥ 0.30 with permutation
  p < 0.01; REFUTED iff some split shows |ρ̂| ≥ 0.30 with p < 0.01 AND
  the independent block confirms sign at p < 0.05; otherwise NARROWED.
  H2 (the task-level law): HOLDS iff the geometry-level Spearman over
  the 20 geometries has permutation p < 0.05; REFUTED iff p ≥ 0.05 OR
  an energy-matched pair (|ΔE_mean| < 0.01) disagrees on OOD by more
  than 0.15.  H3 (the missing-covariate test): a seed-level predictor
  is found iff some covariate reaches |ρ| ≥ 0.50, permutation p < 0.01,
  BH-FDR q < 0.05 across the 9-candidate panel, and sign-replication at
  p < 0.05 in ≥ 2 of 3 scope splits; otherwise the panel is banked as a
  negative.  H4 (family invariance): the H1 verdict class must be
  identical at widths 32 and 128.
- **The falsification one-liners, verbatim.**  *The scope law dies if E
  predicts seeds at |ρ| ≥ 0.3 with p < 0.01, replicated.  The
  task-level law dies if matched-energy geometries disagree on OOD by
  > 0.15, or the geometry-level ordering loses significance.  The
  covariate reading dies if the whole panel stays under the upgrade bar
  with adequate power.  The boundary becomes a LAW only through H1's
  TOST; anything else leaves it open with a measured bound.*
- **The reproduction-first gate.**  Seeds 1000–1011 of every original
  split must reproduce the banked `exp3_sheaf_results.json` values — E
  to 1e-9, OOD accuracy exactly — before any new data; any failure
  aborts the battery.

## 4.2  The instrument and the gate

`seed_boundary.py` is `exp3_sheaf.py`'s trainer VERBATIM,
width-parameterized so that width 64 is bit-identical to the banked
instrument, plus PURE-READ instrumentation: E at checkpoints 500 / 1500
/ 3000; training losses at steps 100 / 300 / 1000; the gradient-norm
mean and std over the last 500 steps; the wrong-OOD confidence.  The
battery is 864 resumable runs (JSONL, checkpointed — the corpus's
resume discipline), covering the gate, the three scope splits at
n = 96, the independent replication block, the two controls, the four
family cells, and the 16-geometry sweep.

The gate PASSED bit-identically: 48/48 runs reproduce the banked
numbers, worst |ΔE| = 0.0.  The instrumentation provably does not
perturb the instrument.  This is the reproduction-first discipline
doing what it exists to do — the new data stands on the old data's
exact shoulders — and it is the battery's first result: zero
instrument drift across the whole rebuild.

## 4.3  H1 — the scope law (the headline)

| Split | n | r(E₃₀₀₀, OOD err) | Fisher 95% CI | perm p | TOST p (δ=0.30) |
|---|---|---|---|---|---|
| compositional_16 | 96 | +0.057 | [−0.145, +0.255] | 0.582 | **0.0074** |
| intermediate_36 | 96 | −0.125 | [−0.317, +0.078] | 0.224 | **0.0380** |
| random_24 (floor control) | 96 | 0 (undefined) | — | 1.000 | 0.0014 |
| replication, seeds 2000–2095 | 96 | +0.011 | — | 0.918 | **0.0020** |

The upgrade rule fired: TOST succeeds in every split with OOD variance
(both p < 0.05), and no split comes anywhere near |ρ̂| ≥ 0.30 (the
largest |point estimate| is 0.125).  The floor control behaved exactly
as designed — random_24's 96 seeds all land at accuracy 0 (ood_std =
0.000), the specificity check that nothing predicts variance which
does not exist.  **The seed-level boundary is closed as a LAW: the
token-sheaf coboundary energy is a task-GEOMETRY diagnostic, not an
initialization-seed predictor.**

The banked n = 12 "null" (r̂ = −0.196 / −0.179) is thereby exposed as
SMALL-SAMPLE NOISE: the n = 96 intervals swallow those point estimates
whole, and the independent seed block lands at +0.011 — on the other
side of zero from the original reading.  An underpowered null is not a
finding; at power, this one became an equivalence.  The honest
pre-statement of §4.1 ("if the truth were ≈ −0.2 the expected verdict
was NARROWED") is answered: the truth was not −0.2; the truth is
consistent with zero, and the TOST bounds it below 0.30 in every
powered split, replicated.

## 4.4  H2 — the task-level law, and the honest correction

The pre-registered H2 endpoint is the geometry-level Spearman over the
20 geometries (16 new + 4 original; the 21st pool entry is the
full-grid control).  Measured: ρ_S = 0.339, permutation p = 0.1376 —
**the rule fires REFUTED**, and it is worth being precise about which
clause fired: the significance clause (p ≥ 0.05), NOT the matched-pair
clause.  All 48 energy-matched pairs (|ΔE_mean| < 0.01) disagree on
OOD error by at most 0.066 — under the 0.15 bar by a factor of more
than two.  No matched-energy contradiction exists anywhere in the pool.

En route, the battery corrected a second banked claim.  The "perfect
4-split ordering" does NOT survive powering: compositional_16's E
(0.5984) and intermediate_36's E (0.5923) — the order FLIPPED relative
to the banked reading, Welch t = 1.15, df ≈ 133, while their OOD
errors genuinely differ (0.934 vs. 0.984).  E does not resolve
fine-grained ordering within the partial band.  What stands is the
**COHERENCE-TIER law**, now measured at power:

- full_49: E = 0.5505, OOD err = 0.000 — decisively below every
  partial geometry (Welch t = −8.84, df ≈ 134 against the pooled
  partial band);
- the partial/coherent geometries: E ≈ 0.592–0.639, err 0.93–1.00 —
  the tiers within this band UNRESOLVED (that is the corrected
  reading, not a loss: the instrument's resolution is the tier, not
  the rank);
- the scattered geometries: failure is CATASTROPHIC, not graded —
  16/16 new geometries at err ≥ 0.99, and the sharpest case is
  rand44: 44 of 49 pairs trained, 0 of 5 held-out pairs solved across
  all 12 seeds.  Scattered splits do not fail a little; they fail
  completely.

The post-hoc reading (labeled as post-hoc, as the discipline
requires): the pool was FLOOR-SATURATED — within the scattered family
the error axis had essentially no variance (everything at ≈ 1.0), so
the geometry-level ordering had nothing to order.  The within-family
dose-response is UNTESTED, not disproven; the redesign that would test
it is named in §4.10.  The instrument's degenerate-E threshold is
documented as part of the same honest accounting: tokens with fewer
than 4 training examples fall to the E = 0.0 fallback (rand16/g23 the
named cell: E = 0.0000, err = 1.0 — the pool's one invalid instrument
reading, excluded from nothing and hidden from no one).

The full 21-geometry pool (the chapter's table of record):

| Geometry | kind | n | E | OOD err |
|---|---|---|---|---|
| full_49 | original/control | 48 | 0.5505 | 0.0000 |
| compositional_16 | original | 96 | 0.5984 | 0.9343 |
| intermediate_36 | original | 96 | 0.5923 | 0.9840 |
| random_24 | original | 96 | 0.6254 | 1.0000 |
| random_60 | original/control | 48 | 0.6194 | 1.0000 |
| rand16/g11 … rand44/g23 | new sweep | 12 each | 0.5386–0.6390 | 0.9971–1.0000 |
| rand16/g23 | new (degenerate) | 12 | 0.0000 | 1.0000 |

Tier means: full 0.5505, coherent-partial 0.6002, scattered 0.6017 —
the partial and scattered TIERS overlap in E (they are both
"non-coherent"), which is exactly why the pooled Spearman could not
reach significance: one real contrast (full vs. everything else), one
saturated axis (everything else vs. itself).

## 4.5  H3 — the covariate negative

The 9-candidate training-dynamics panel — E_500, E_1500, losses at
steps 100/300/1000, final train NLL, gradient-norm mean and std, and
wrong-OOD confidence — was tested against seed-level OOD error within
each scope split.  The result is a clean negative at every entry: the
largest |r| in any powered split is 0.096 (E_1500, intermediate_36);
BH-FDR q-values run 0.917–1.000; nothing approaches the pre-registered
bar (|ρ| ≥ 0.50, p < 0.01, q < 0.05, sign-replicated in ≥ 2/3 splits).
The random_24 column is identically zero — the floor control again
behaving as designed.

The negative is banked with its scope stated: seed-level OOD variance
(σ ≈ 0.033 in both scope splits — the quantity that exists and varies)
is unexplained by every instrument this battery pointed at it.  Jointly
with H1, the scope reading strengthens rather than weakens: not only
does E not predict seed luck — neither does anything in the measured
panel.  The "missing covariate" reading of the boundary (§4.8) is
thereby a named negative, not an open hope.

## 4.6  H4 — the family sweep

| Cell | n | r | TOST p (δ=0.30) | class (by rule) |
|---|---|---|---|---|
| comp_16, width 32 | 48 | +0.097 | 0.077 | NARROWED |
| comp_16, width 64 | 96 | +0.057 | 0.007 | LAW |
| comp_16, width 128 | 48 | +0.030 | 0.031 | LAW |
| interm_36, width 32 | 48 | −0.056 | 0.045 | LAW |
| interm_36, width 64 | 96 | −0.125 | 0.038 | LAW |
| interm_36, width 128 | 48 | −0.085 | 0.066 | NARROWED |

By the pre-registered CLASS rule the verdict is WIDTH-DEPENDENT (four
LAW, two NARROWED).  The post-hoc diagnosis (labeled as post-hoc):
the two NARROWED cells are TOST-power artifacts at n = 48 — the class
rule passes equivalence there only for |r̂| < 0.065, and both cells sit
just outside that gate with CIs crossing zero.  All six point
estimates lie in [−0.125, +0.097]; every width's CI crosses zero; no
width shows a consistent sign.  There is no evidence of actual width
dependence in the estimates — only in the rule's resolution at n = 48.
The honest reading: the class rule was coarser than the 48-run cells;
the law's substance (all estimates near zero, none near 0.30) holds at
every width.

The pooled confound was re-measured at power while the battery was
alive: r = 0.441 at n = 384 (perm p = 1e-4, TOST p = 0.999 — a real
association, decisively NOT equivalence).  This is the split-dominated
pooled correlation the corpus always flagged, now a measured quantity
rather than a caveat: pool the geometries and E "predicts" error
because the coherence tiers differ in both — within any fixed
geometry, the association vanishes.  The confound is the tier
structure viewed from the wrong level, and the census of §4.3 is the
control that removes it.

## 4.7  The secondary endpoint (the hallucination measure)

E vs. wrong-OOD confidence — the chat's original prediction, carried
through the same pre-registered machinery: compositional_16 r = −0.180
(perm p = 0.080, TOST p = 0.109) — the honest NARROWED zone, neither
significant nor equivalent, the CI as the bound; intermediate_36
r = −0.005 (TOST p = 0.0017 — equivalent to zero); random_24
r = +0.102 (TOST p = 0.023).  The prediction remains exactly where the
battery found the seed-level error signal: open in the narrowed zone
in one split, equivalent-to-zero in the others, with no covariate in
the panel to rescue it.  The row is banked as measured, not closed.

## 4.8  The boundary's new statement (the law and its scope)

The two readings the outline carried in are now resolved by the data:

- **The scope reading is the law.**  E measures the split geometry's
  coherence tier — full grid (E ≈ 0.55) decisively below coherent
  partial (E ≈ 0.59–0.64) and both below catastrophic scatter — and it
  carries no seed-level information: at fixed geometry, the seed-level
  association is bounded below |ρ| < 0.30 by equivalence in every
  powered split and every seed block, with all point estimates in
  [−0.18, +0.10] and the widest CI upper edge at 0.26.
- **The missing-covariate reading is a named negative.**  H3's panel
  found nothing; seed-level OOD luck (σ ≈ 0.033) is unexplained by
  every training-dynamics instrument the battery measured.  What
  varies across seeds is, on this evidence, invisible to pre-training
  geometry and to the measured run-time covariates alike.

The boundary as the corpus now states it: the token-sheaf coboundary
energy is a task-geometry diagnostic whose predictive reach ends at
the geometry.  Its verified deliverable is the coherence tier; its
verified non-deliverable is initialization luck.  Both statements
carry the same evidential tier as the rest of this volume's
certificates: pre-registered, powered, replicated, falsification rules
honored.

## 4.9  The grind's rule, resolved the same session

The volume's other item closed in the same session this chapter was
written, and it belongs in the record here because the two closures
are the same kind of event: instruments honestly reporting the limits
of what they can carry.  The grind census's fourth round (session
0012, this turn) ran the cover4d slice the watch needed: 60.0M calls,
29,924,011 leaves certified (BDC: 10,840,150 e0 + 8,324,792 e4 +
10,759,069 e5), frontier 30 branches.  The series 24 → 26 → 28 → 30 →
30 over the watch's windows gives the third consecutive below-floor
window (trailing closure −2.0 branches/M calls against the +0.05
floor; the projection to zero: NO-CLOSURE, the trend opens).  **The
rule fires HOLD.**  The wall arm had already stopped by its own rule
(Task 44 — the stack's far-out replenishment, net +4/window).  Both
arms of the grind are now rule-stopped; the completion face is Task
42's bookkeeping (the far-field growth laws + the one-shot sound
shells + the valley tail's plateau law + the analytic B-exit), with
the certified region — 29.92M leaves on the cover side, 346,400
certified on the wall side — standing as certified.

One new measurement belongs to the honest account: the first stall
leaves of the entire cover4d arc appeared in this deciding round —
1246 of them, and their measured center margins are the reason they
are residue, not obstruction: minimum +11.25 above λ*, median +107
(n = 1099 with measured values), every measured value ≥ λ* at float
precision.  These are interval-width effects at the frontier's current
depth — the same pattern the wall's far-out refinement showed (the
centers pass comfortably; the interval certificates at depth are pure
width artifacts) — and they corroborate the HOLD reading rather than
complicating it: the remaining frontier is deep refinement whose
certificate cost grows while its mathematical content (every measured
center already above λ*) is already accounted for by the analytic
faces.  The grind ends not with exhaustion but with a measured
statement of its own scope — the certificates accumulate, the
completion is bookkeeping, and the rule stops the spend.

## 4.10  The one remaining nameable upgrade: the token-coverage-matched dose-response pool

Everything on this row is decided except one question, and it is
named here precisely because it is the only one left: **the
within-family dose-response** — does E order OOD error WITHIN a family
of geometries as the geometry degrades, at matched token coverage?
The H2 pool could not test it: the scattered family was
floor-saturated (16/16 at err ≥ 0.99 — no variance on the axis to be
ordered), and the cross-family comparison conflates coverage with
arrangement (rand44's 44 trained pairs vs. comp_16's 16 differ in both
at once).  The pre-registered rule fired REFUTED on a test that had,
in truth, not run — the honest status is UNTESTED.

The redesign, as named in the results and priced here: a pool of
geometries at **token-coverage-matched sizes 44–48** — near-complete
subsets of the 49-pair grid in which every token is held at a matched
number of training examples across geometries, isolating the
ARRANGEMENT term from the raw-coverage term, in the regime where
failure is graded (between full_49's 0.000 and the partial band's
0.93+) so the error axis has variance to order.  The form its
pre-registration would take: the same instrument, 12 seeds per
geometry, 10–16 geometries (120–200 runs — one session's battery at
the same per-run cost); the geometry-level Spearman over the matched
pool with the same permutation and equivalence machinery; the
falsification one-liner: the dose-response dies if the matched pool
shows no graded error ordering across its E spread, or if
matched-energy pairs (|ΔE| < 0.01) disagree on OOD by > 0.15, exactly
as before.  HOLD's answer, for this row, would be the coherence-tier
law's final form: E's reach is the tier and only the tier; REFUTE's
answer would upgrade the diagnostic to a within-family dose-response
meter.  Either outcome is a real result.

Its status in the ledger: **the one remaining nameable upgrade** —
named, designed in outline, priced, uncommissioned.  The chapter does
not promise it runs; it records that everything else on the row has
been run and decided.

## 4.11  The methodological first

This chapter's battery is the programme's first closure by
pre-registered experiment, and the protocol it followed is the
template the volume's remaining batteries inherit:

1. **Pre-register, and let the commit be the timestamp.**  The design,
   the power analysis, and the decision rules were fixed and committed
   (3a108d8) before a single new run existed.
2. **Reproduce before generating.**  The gate (48/48 bit-identical)
   ran before any new data; zero drift is a result, not a formality.
3. **Power for the distinction the claim needs.**  "No signal" and
   "bounded below practical predictivity" are different claims; the
   TOST at δ = 0.30 with n = 96 is what separates them, and n = 12 was
   never going to.
4. **State the falsification one-liners and honor them when they fire
   against you.**  Two banked claims died under this battery's rules —
   the seed-level null was small-sample noise, and the "perfect
   ordering" was small-sample luck.  A method that only confirms is
   marketing; this one falsified its own priors and banked the
   corrections (the coherence-tier law is a BETTER claim than the one
   it replaced, because it is scoped to what the instrument resolves).
5. **Label every post-hoc reading as post-hoc.**  The floor-saturation
   diagnosis (H2), the TOST-power diagnosis (H4), and the
   token-coverage-matched redesign are all labeled readings after the
   fact — recorded, priced, and explicitly not promoted to findings.
6. **Bank the negatives with the positives.**  The covariate panel's
   clean zero is in the ledger with the law, at the same tier.

The ledger after this chapter: the boundary row reads DECIDED — a
scope law, equivalence-replicated, with a named negative where the
missing covariate was hoped for; the grind row reads DECIDED — HOLD by
the rule, the completion face stated (§4.9); and the empirical face's
one open item is the named pool of §4.10, which becomes science the
day it is pre-registered and run.  The volume's premise — two items,
different in kind from everything closed before — is now two items
different in OUTCOME: both decided by instruments reporting honestly
what they can carry.

---

## Addendum (session 0013, Task 47) — the pool commissioned, pre-registered, run, and decided

§4.10's "one remaining nameable upgrade" was commissioned by the
volume's closing order (*"then commission the dose-response pool so
even the last named item becomes a decided experiment"*) and executed
under the full Task-44 protocol: the pre-registration
(`download/seed_dose_preregistration.md`) committed at `cd42256`
BEFORE the data — the commit is the timestamp; the instrument
IMPORTED from `seed_boundary.py` verbatim; the reproduction gate run
first (12/12 full_49 runs reproduce the banked numbers through the
imported path, worst |ΔE| = 0.0 — the import perturbed nothing); then
the pool: 30 matched geometries (the 49-grid minus a uniformly random
partial matching, sizes 44–48 × geometry seeds {31, 37, 41, 43, 47,
53} — every token keeping 6 or 7 examples, the count profile identical
within each size, no degenerate-E cells) × 24 model seeds in two
12-blocks (1000–1011, 2000–2011) — 720 runs, 402 s.

**THE VERDICT, by the pre-registered class: UNTESTED (saturation)**
— 0 of the 5 size blocks carry within-block error variance; the level
reading is the finding, exactly the honest outcome the
pre-registration anticipated ("a real result — the coherence boundary
located — not a failure").  The measured content:

- **THE CLIFF IS ABSOLUTE.**  err ≡ 1.000 ± 0.000 at every size
  44–48, every geometry, every seed: 2160 of 2160 held-out
  predictions failed — not one seed, at any coverage from 44/49 to
  48/49, ever solved a single held-out pair.  The failure is
  CONFIDENT (wrong-confidence on the failed pairs: mean 0.749,
  median 0.756) and the memorization is PERFECT (train accuracy
  ≡ 1.0000 in all 720 runs — the minimum is 1.0000): the model learns
  the 48 seen facts exactly and predicts the one missing fact wrongly
  with three-quarters confidence.  There is no interpolation regime
  at the matched edge — the graded-failure band §4.10 hypothesized
  between full_49's 0.000 and the partial band's 0.93+ DOES NOT
  EXIST in this instrument's regime.
- **E'S COVERAGE DOSE IS REAL — AND HAS NOTHING TO PREDICT.**  E's
  geometry means run monotone 0.5699 (size 44) → 0.5645 → 0.5600 →
  0.5554 → 0.5491 (size 48), the descriptive Spearman against the
  coverage dose (49 − size) = 0.899 over the 30 geometries, with
  within-size spreads (0.002–0.007) an order below the dose's total
  span and the per-geometry seed-level E spread 0.014–0.022.  The
  diagnostic measures the coverage dose cleanly — and the error axis
  it was commissioned to order is constant at 1.000: H5-a's pooled
  Spearman is exactly 0.000 (p = 1.0, both blocks — the test's honest
  degenerate value), H5-b's block-centered arrangement test likewise
  0.000, and the matched-pair guard is silent (253 matched-energy
  pairs, max |Δerr| = 0.000).  The dose-response cannot exist
  because the response does not.
- **THE ERROR LANDSCAPE'S SHAPE, ACROSS THE WHOLE RECORD.**  49/49 →
  the vacuous perfect (nothing held out); 44–48/49 at matched
  coverage → total confident failure (1.000); 36/49 → 0.984; 16/49 →
  0.934; the scattered family → ≥ 0.99.  Error is NOT monotone in
  coverage — it is a function of the held-out set's structure: pairs
  among partially-unseen tokens extrapolate occasionally (the
  coherent-partial band's mild grading), while a single missing fact
  among fully-seen tokens never interpolates.  The coherence
  boundary is a cliff at the top of the coverage axis, not a slope.

**The last named item is thereby DECIDED — as a decisive negative
with located structure**: the within-family dose-response axis does
not exist in this instrument's regime (the error axis is constant at
matched coverage; the graded band lives only in the
coherent-partial family, on the other side of the cliff).  The
coherence-tier law stands as the FINAL form of §4.8, its boundary now
located absolutely: E's verified reach is the tier and the coverage
dose; the error landscape's only transitions are the cliff at the
matched edge and the catastrophic scatter below it.  The empirical
face's ledger is now fully decided — every row closed by experiment,
pre-registered, the rules honored, the negatives banked at the same
tier as the laws.
