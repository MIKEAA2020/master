# Session 0004 — Task 34: the residue closed (the BDC + the DPP + the orbit reduction)

- **Date**: 2026-09-30
- **HEAD at end**: f5339de — Task 34: the residue closed
  (the BDC + the DPP + the orbit reduction).
- **Last Task ID**: 34
- **Ledger (open)**: the class-level lower bound's status ADVANCED TO
  CLOSED-ON-THE-CERTIFIED-REGION — the disc-edge divergence layer is
  now CERTIFIED (the BDC), the honest stall count 0 at the hard
  floors (depth 78 / width 1e-8).  The remaining items: (1) the
  5 unexplored orbit representatives + the (+,+,+,+)'s ~21 frontier
  branches (the continuation protocol: re-run
  `scripts/abelian_cover4d.py`; the projected full 6-rep completion
  ~25–30M calls); (2) the 12-parameter free-class wall
  (D_free ≥ √λ*) — the user's named remaining gap to the full
  shadow equivalence; (3) the seed-level boundary; (4) the
  third-order remainder along the valley.
- **Closed this session**: (i) THE BDC — the exact e0/e4/e5 Rayleigh
  corner identities (V-G, ~1e-13) as poison-free clamped interval
  bounds on the box's DOMAIN portion, the linear CS ratio bound
  d12 ≥ max(d11,d22)/2 (V-H, 0 violations), the nonneg-product and
  V-H-dominance cross forms, the p-split at 0; (ii) THE DPP — the
  two-scale Taylor-4 patch certificate (the coefficients at the
  box-scale widening 2h + the Lagrange C4 at 2h + r), the per-top-box
  budget: 1804 patches, median r = 4.23e-2 (11× the box-mode floor);
  (iii) THE ORBIT REDUCTION — V-F the π-rotation EXACT (0.00e+00):
  16 quadrants = 6 orbit representatives of {1, R, S, RS}, the 10
  images symmetry-covered; (iv) THE RUN — the full fresh re-run from
  the restored Task-33 base: 12,000,000 calls, 5,975,008 leaves
  certified sound (ALL via the BDC trio: 2.32M e0 + 2.50M e4 +
  1.16M e5), ZERO stalls across the final 4.5M calls (the depth-50
  pre-stall removed after diagnosing its casualties as certifiable:
  small-|p| boundary cells, center margins +1.4e5..+5.7e5).
- **Open orders / next steps**: the continuation runs (the
  checkpoint; ~17–18M more calls to the full 6-rep completion);
  then the 12-parameter free-class wall (the user's named last gap).
- **Recovery pointers**: worklog Task 34;
  scripts/abelian_cover4d.py + abelian_cover4d_results.json +
  abelian_cover4d_ckpt.json (the continuation state: the stack of 26
  branches + all counters); scripts/probe_task34.py (the design
  probes); download/The_Resolution_Programme_XIII_Corrigendum.md
  (the Task-34 addendum).
- **Key numbers**: λ* = 1.6310919765642504…; V-F the π-rotation
  0.00e+00 (240 samples); V-G the corner identities 1.1e-13/1.4e-12/
  2.3e-13; V-H 0 violations (2000 samples); the DPP patches 1804
  (median r 4.23e-2, max 1.07e-1); the run 12M calls / 5,975,008
  certified leaves / 0 stalls at the hard floors; the same-box A/B
  (the intrinsic-tail finding): box-mode r 0.00389 vs DPP 0.00385
  at h = 2e-4.
- **Hygiene notes**: the per-top-box budget + the per-top-box
  checkpoint are MANDATORY for the A-sweep (the global stall cap
  aborted the whole sweep at the first top box — the Task-33 design
  flaw found and fixed this session); the BDC trio fires BEFORE the
  eigendecomposition (the standard cert is fully superseded — 0
  standard passes is the expected accounting, not a breakage); the
  depth-50 boundary pre-stall is REMOVED (its casualties are
  certifiable by refinement); the checkpoint version flags ("dpp" =
  3, "b_sv" = 2) gate the one-time re-measurements.
