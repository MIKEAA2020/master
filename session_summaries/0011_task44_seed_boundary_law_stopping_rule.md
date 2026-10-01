# Session Summary 0011 — Task 44

## The commissioning critique and the answer

The user's critique: the log shows disciplined research *operations*
(resync, drain, build, QA, version, push) — necessary conditions for
science, not sufficient ones. The far-field laws are treated as items
being closed, not as validated claims. The drain rounds are counters,
not discoveries. The one genuine scientific question on the books —
the seed-level boundary ("task-level ordering perfect, seed-level
correlation null") — was listed as still open. Priority order given:
**seed-boundary evidence design > finishing the grind if genuinely
near closure > more versioning**, with the grind bound to a stopping
rule and an expected endpoint.

This session answered with executed science, in the correct order.

## The pre-registration (committed before the data)

`download/seed_boundary_preregistration.md` (commit `3a108d8`, pushed
before the experiment ran): hypotheses H1–H4, the power analysis
(n=96/split; SE(Fisher-z)=0.104; TOST δ=0.30; the honest pre-statement
that a true ρ≈−0.2 would land in the NARROWED zone), the controls, the
primary/secondary endpoints, the falsification one-liners, and the
reproduction-first gate. The instrument (`seed_boundary.py`) is
exp3's trainer VERBATIM plus pure-read instrumentation — 864
resumable runs.

## The results (verdicts by the pre-registered rules only)

- **THE GATE: bit-identical reproduction** — 48/48 runs, worst |ΔE| = 0.0.
- **H1 — THE LAW**: the token-sheaf coboundary energy is a
  task-geometry diagnostic, **not** a seed-level predictor. Seed-level
  r(E, OOD error) = +0.057 [−0.145, +0.255] (comp_16) and −0.125
  [−0.317, +0.078] (interm_36), TOST-equivalence to |ρ|<0.30 at
  p=0.007/0.038, replicated with an independent seed block
  (r=+0.011, p=0.92). **The banked n=12 "r=−0.19/−0.18" was
  small-sample noise. The seed-level boundary is CLOSED as a law.**
- **H3 — the covariate negative**: the 9-candidate
  training-dynamics panel all fail the bar — seed-level OOD variance
  (σ≈0.033) is unexplained by every instrument pointed at it.
- **H2 — the honest correction**: the banked "perfect 4-split
  ordering" does not survive powering (comp/interm E-means tie,
  order flipped, Welch t=1.15). What stands: the coherence-tier law
  (full-grid ≪ every partial geometry, decisively) + the observation
  that scattered splits fail catastrophically (rand44: 44/49 pairs
  trained, 0/5 OOD; 16/16 new geometries at err ≥ 0.99). The
  pre-registered rule fires REFUTED on the pooled Spearman
  (p=0.1376); the labeled post-hoc reading: the pool was
  floor-saturated — the within-family dose-response is untested, not
  disproven.
- **H4**: width-class differences are TOST-power artifacts at n=48
  (labeled post-hoc; all estimates in [−0.125, +0.097], CIs crossing
  zero).
- The pooled confound re-measured: r=0.441 at n=384 (split-dominated,
  as always flagged).

## The stopping rule, measured (`grind_census.py`)

The rule was stated first, then evaluated from the parsed round
series: **the wall arm STOPPED** (stack oscillates 39–45 with the
far-out replenishment; its completion face is Task 42's far-field
bookkeeping); **the cover4d arm caught its own projection error**
(the "3M-calls-to-zero" reading was a windowing artifact — the next
three slices reversed the trend to 24→26→28→30): HOLD-CANDIDATE,
2 of 3 consecutive below-floor windows, the next rounds decide. The
drain protocol is amended: cover4d-only slices, the census re-run per
round. Grind this turn: 58M→59.5M calls, 29,678,999 leaves, zero
stalls, frontier 30.

## The state carried forward

- The drain protocol: census-driven, cover4d-only, 1–2 slices decide
  CONTINUE vs HOLD.
- Vol XIV Chapter 4's battery is EXECUTED (the outline's status note
  records it); the volume's write-up now has a decisive experiment to
  carry, not just a design.
- The honest open items: the within-family dose-response (the
  token-coverage-matched pool, sizes 44–48 — named, priced, not
  promised); the cover4d HOLD watch; the Vol XIV build itself.
