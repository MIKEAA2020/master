# session_summaries/ — the persistent home for session-reset summaries

## Purpose

Every time the conversation context is exhausted or the environment resets,
a compact summary of the session's state is written here BEFORE the reset
(or immediately after recovery).  This directory is the durable,
version-controlled answer to the recurring question "where do the reset
summaries live?" — so that a fresh session can bootstrap from the REPO
instead of re-deriving state from chat history (the token-saving protocol).

## The protocol

1. **At the end of every session** (or at the start of the next one, if the
   reset hit first), append a file `NNNN_<short-slug>.md` where `NNNN` is
   the zero-padded sequence number and the slug identifies the session's
   dominant task(s).
2. Each file follows the house template (below): the state of the ledger,
   the last task ID, the HEAD commit, the open orders, the recovery
   pointers (which worklog entries / results JSONs carry the detail).
3. The file stays SHORT (one screen): the detail lives in the worklog and
   the results JSONs — this directory is an INDEX, not an archive of
   transcripts.
4. Never edit older entries except to append a one-line correction marker
   (`> CORRECTION (NNNN): ...`) — the history must stay append-only, the
   same discipline as the worklog.

## The house template

```markdown
# Session NNNN — <one-line description>

- **Date**: YYYY-MM-DD
- **HEAD at end**: <commit> (<one-line subject>)
- **Last Task ID**: <n>
- **Ledger (open)**: <the open items, one line each>
- **Closed this session**: <one line each>
- **Open orders / next steps**: <the standing instructions>
- **Recovery pointers**: worklog Task <n>; scripts/<file>.py +
  <file>_results.json; download/<volume>.pdf
- **Hygiene notes**: PAT persisted at .secrets (root, gitignored) +
  scripts/restore_pat.sh; venv = `pip install --break-system-packages
  python-flint` + numpy/scipy/matplotlib after a reset.
```

## Index

- `0001_pre_task32_recovery.md` — the backfilled pre-Task-32 state
  (reconstructed after the context loss that followed Task 31/Volume XIII;
  written at Task 32 recovery time from the repo + the transferred
  summary; carries the 0002 correction marker).
- `0002_task32_class_level.md` — Task 32: the class-level adjudication
  (the escape retracted; the structural x^4 law; the kappa sign
  resolved; the p-convexity; the V-cone).
- `0003_task33_covering.md` — Task 33: the 4-D covering engine (the
  6x6 true-norm ball instrument, hole-free; the layered run — 511,679
  certified leaves; the box-count wall replaced by the measured
  structural residue; the checkpoint/resume protocol).
- `0004_task34_residue_closed.md` — Task 34: the residue closed (the
  boundary-divergence formalization deployed — the BDC corner
  identities and the CS ratio bound; the derivative-penalty patch
  mode; the orbit reduction).
- `0005_task35_drain_and_free_wall.md` — Task 35: the drain and the
  free wall (the FW-4 residue named; the free-class engine's first
  certified arc).
- `0006_task36_e45_divergence.md` — Task 36: the e45 divergence
  certificates (the word-power recursion; the partial-sum sandwich;
  the far-out refinement replacing the census).
- `0007_task37_pat_durability_drain_vol13.md` — Task 37: the PAT
  durability layer + the drain + the Vol XIII first edition.
- `0008_task39_40_split_refuted_critical_locus.md` — Tasks 39/40: the
  gradient-split corollary refuted by controlled A/B; the critical
  locus closed (the plateau law, the quartic, the off-family floor).
- `0009_task41_42_vol13_second_edition_far_field_closed.md` — Tasks
  41/42: the Vol XIII second edition; the unbounded far-field laws
  (the last FW-4 item) closed.
- `0010_task43_third_printing_vol14_outline.md` — Task 43: the Vol
  XIII third printing (Addendum 7 folded in); the Vol XIV outline
  committed (the post-far-field state).
- `0011_task44_seed_boundary_law_stopping_rule.md` — Task 44: the
  commissioning critique answered with executed science — the
  programme's first PRE-REGISTERED experiment (the gate bit-identical
  48/48; H1 the seed-level boundary CLOSED AS A LAW: TOST
  equivalence to |rho|<0.30, independent-seed replication, the banked
  n=12 null exposed as small-sample noise; H3 the covariate panel's
  negative; H2 the "perfect ordering" honestly corrected to the
  coherence-tier law with the floor-saturated pool documented) + the
  grind's STOPPING RULE measured (grind_census.py: the wall arm
  STOPPED by the rule, the cover4d arm on its 3-window HOLD watch
  after catching its own projection error).
