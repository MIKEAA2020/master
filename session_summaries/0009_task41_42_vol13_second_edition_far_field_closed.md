# Session Summary 0009 — the queue cleared: the second edition, the grind, and the far field closed

**Session**: 2026-10-01 (web-e79ae75e). **The user's order**: "do all
items in queue: your call — the Vol XIII PDF regeneration (record
content now complete through Task 40 — the carried write-up), more
drain rounds (standing order), and the unbounded far-field laws — the
last FW-4 item."

## What was done (feasibility-ordered)

1. **THE DRAIN (2 fg-driver rounds, zero stalls)**: cover4d
   54.5M -> 56M calls (27,936,871 leaves certified, all BDC; the
   frontier 28-32 branches); the wall 700k -> 740k calls (326,402
   certified: 135,406 window + 190,996 e4/e5 partial-sum; the stack
   41 -> 39).  Both checkpoints committed and pushed with each
   increment.
2. **THE VOL XIII SECOND EDITION REGENERATED** (the carried
   write-up): `vol13_content.py` extended with four new chapters
   (the corrigendum — the escape retracted, the valley adjudicated;
   the two walls, certified symmetric; the tail's law, the split
   refuted, the critical locus closed; the regenerated ledger) and
   five new tables; the cover re-titled (the second edition,
   October 2026) and re-rendered (poster_validate + cover_validate
   PASS, html2poster at 794px); the body regenerated via the proven
   Vol XI engine clone (with the no_dash_breaks fix extended to the
   stats labels, table captions and figure captions); **27 pages,
   10 tables, 8 chapters; pdf_qa PASS, font.check 0 issues, TOC
   clean**.  The README's volume list gains its missing Vol XIII row
   (item 13, the second edition).  Delivered to the mirror's and the
   local `download/`.
3. **THE UNBOUNDED FAR-FIELD LAWS CLOSED** (the last FW-4 item —
   `far_field_laws.py` + Addendum 7 + the README row):
   - **THE WINDOW'S QUARTIC LAW**: sigma2 ~ s^3.977 (the per-doubling
     exponents 4.00 exactly — the pencil M_cell - s^2 M_BC); the
     sound one-shots growing exactly s^4.
   - **THE e0-POLY'S DEGRADATION** (the honest negative result):
     ~ -s^2 exactly — the form z-quadratic, sign-invariant; the e0
     is NOT a far-field carrier.
   - **THE e45 EXCITED GROWTH**: rho^3.666 at N=2 (the 2N = 4
     asymptote), crossing lambda* between rho 1 and 2.
   - **THE ROW-SOUND WINDOW BOUND** (the battery's new instrument —
     the dependence-corrected square): the same-sign annulus
     quadrants certify ONE SHOT 6/6 strict-sound (2.07e8 / 3.32e9 /
     5.31e10 at s = 1/2/4), A-blind.
   - **THE MIXED QUADRANTS**: the center path censors (the
     A-straddle, the domain gate closed) — the root's OWN grind
     structure, scale-invariant, NO new obstruction (the race law's
     guarantee).
   - **THE VALLEY TAIL CROSS-VALIDATED**: the full Rayleigh resolves
     the plateau margin at every x to 1e-6 (B = 2e5): 5.49e-9 =
     2·sqrt(lambda*)·2.1491e-9 exactly — Task 40's plateau law at
     the wall's own instrument (the interval form more robust than
     the float).
   - The honest in-session record: three instrument errors in the
     first pass, all caught by the reproduction-first gates; the
     flint gate semantics confirmed sound en route.

## The state at close

- The remote at the far-field closure commit; the worklog at Task 42.
- **The wall's named FW-4 residue items are ALL closed or measured**
  (the e4/e5 forms — Task 36; the critical locus — Task 40; the
  tail's law — Task 38; the unbounded far-field laws — Task 41).
- The remaining honest residue: the continuation grind itself (the
  cover4d frontier 32 branches; the wall's 39-stack far-out
  refinement; the near-boundary layer) + the seed-level boundary
  (unchanged, the empirical face's one open row).
- The recovery protocol unchanged: `restore_pat.sh` +
  `restore_env.sh`, then the fg driver.
