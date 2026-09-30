# Session 0006 — Task 36: the free e4/e5 unstable-mode divergence certificates

- **Date**: 2026-10-01
- **HEAD at end**: (this session's Task 36 commit; the push PENDING —
  the PAT secrets wiped by the reset, the same pattern as 48c88a5:
  re-supply the fine-grained PAT, run `scripts/restore_pat.sh`).
- **Last Task ID**: 36
- **Ledger (open)**: (1) the cover4d abelian drain's frontier (the
  continuation: re-run `scripts/abelian_cover4d.py`; 39.5M → 43M+
  calls this session, the cap at 100M, ZERO stalls); (2) the wall's
  far-out refinement + the boundary grind (re-run
  `scripts/free_class_wall.py` — the Task-36 chain active: the e45
  passes +10k/slice, the far-out census replaced by the bounded
  refinement); (3) the critical-locus continuation (the line-atom
  valley, B ~ c*/2x unbounded); (4) the unbounded far-field laws;
  (5) the seed-level boundary; (6) the third-order remainder.
- **Closed this session**: (i) THE STATE RESTORED from the remote
  (Tasks 32-35 pulled after the reset; the venv rebuilt; flint
  reinstalled); (ii) THE FREE e4/e5 PARTIAL-SUM UNSTABLE-MODE
  DIVERGENCE CERTIFICATES BUILT AND DEPLOYED — the Task-34 BDC
  mirror on the free side: the word-power recursion T_{n+1} =
  A_a T_n A_a^T + A_b T_n A_b^T (PSD-monotone toward Lc), the class
  vectors v = (z, 0) with the CONSTANT denominator, the partial-sum
  sandwiches (polynomial, degree 2N+4, NO convergence needed — sound
  at every in-class point including the ρ ≥ 1 X-cancellation
  strata; the excited out-of-class points vacuous); the N-ladder +
  the fixed/adaptive z-menu; the far-out census replaced by the
  bounded refinement; (iii) THE IN-SESSION BUGFIX (the honest
  record): the interval word-power recursion missed the right
  multiplication (decaying at ‖A‖ not the spectral rate) + the
  Q_plain cross-term typo — the float probe exposed it, both fixed,
  the cross-validation added (the word-power sums vs the corpus's
  Lyapunov 9.34e-06), the engine honestly reset from the git
  checkpoint; (iv) the probes: the anchor EXACT, the soundness
  validated, the divergence law ρ^{2N}, the coverage 87.8% of the
  recorded stalls at N=2, the X-cancellation conic construction.
- **Open orders / next steps**: keep re-running both scripts (the
  drain + the far-out refinement); the critical-locus continuation;
  the PAT re-supply + the push.
- **Recovery pointers**: worklog Task 36;
  `scripts/probe_task36.py` + `probe_task36b.py` (the design probes
  + the coverage); `scripts/free_class_wall.py` (the integrated
  chain) + `free_class_wall_results.json` + `free_class_wall_ckpt.json`;
  `scripts/abelian_cover4d.py` + `_ckpt.json` (the drain);
  `scripts/fg_driver.sh` (the foreground drain driver — the sandbox
  reaps the background processes).
- **The English rule**: maintained (the fifth session running).
