# Session Summary 0008 — the feasibility-ordered sweep: the split
corollary refuted, the critical locus closed (the Vol XIII gate
cleared), the grind steady

**Date**: 2026-10-01
**Order**: "proceed in order of feasibility with dependency awareness
(topological order is the constraint, feasibility is the priority)"

## The state at entry

The prior session had closed Task 38 (the tail's structural law —
the five-part law, the race law predictive to 1 level) and pushed
three drain increments (the remote at 9c36f2c).  The remaining
queue: the gradient-split corollary (Task 38's banked "actionable"
~2x drain), the critical-locus continuation (the other FW-4 residue
item — the Vol XIII gate), the drain grind (the standing order),
and the carried items (the Vol XIII write-up, the escape
quantification, the far-field laws, the seed-level boundary).

## The dependency graph (read off the state, feasibility-ranked)

1. **The A/B probe of the split corollary** — the highest
   feasibility (a 20-minute controlled experiment on the live
   stack) AND the gate on all further grinding (why grind at 1x if
   a 2x edit is one validation away?).
2. **The critical-locus continuation** — the Vol XIII gate; the
   machinery existed (probe_task35's kernel + the line-atom
   family); the design pre-check was cheap.
3. **The drain** — the standing order, wall-clock-bound, the
   engine validated optimal either way.
4. **The records** — the README rows, the Corrigendum addendum,
   the session summary (this file).

## Task 39 — the gradient-split corollary REFUTED (the A/B before
the edit)

`gradient_split_ab.py`: the engine's own machinery (the AST-filter
exec), the LIVE 39-entry stack copied per arm, the F_* counters
snapshotted/restored — no checkpoint mutation.  **AB-0**: the
TL-3b carrier profile has FLATTENED on the live stack (the top
carrier 18% vs ~30% at the census-width boxes — the peaked profile
was a TRANSIENT of the measurement-time stack).  **AB-A/AB-B**: the
stock width-first split 0.4998 e45/call (0 stalls) vs the gradient
arm 0.4185/call — **0.84x with 324 cap-hit stalls**.  The dynamic
variant priced out (24 evals = 17 calls of overhead vs a ≤1.05x
headroom): at the flat live profile the measured 0.135 bits/level
is ALREADY the informed-split optimum.  **The width-first rule
stays — the engine validated near-optimal.**  A banked assumption
killed before it touched the engine.

## Task 40 — the critical locus CLOSED (the line-atom valley's
deep refinement)

The design pre-check found the SATURATION PLATEAU (the family does
not converge to √λ* — it converges to √λ* + 2.149e-9).  The full
instrument (`critical_locus.py`):

- **The closed form** (new, exact): the diagonal commuting family
  gives S_(i,j) = μ_(i,j)·diag(xⁱyʲ, (−x)ⁱyʲ) EXACTLY — the kernel
  E(α,γ) = √(μ_αμ_γ)[1_{α+γ=(1,1)} − p·y^J·x^I·(1−(−1)^I)], E
  symmetric; validated against the general machinery to 0.0.  The
  STRUCTURED O(n)-per-apply matvec (the Φ-polynomial operator)
  validated to 4.4e-16 — the deep-K and the prec-120 engine.
- **THE PLATEAU LAW**: the family saturates at √λ* + 2.1491e-09
  (CERTIFIED at mpmath prec 120, K=64: 1.2771421150615995710039) —
  the valley is unbounded in B (B = c*/2x) but FLAT in value: the
  I=1 stripe (2px = c*) is the x⁰ leading structure, the
  B-magnitude cancels identically.
- **THE APPROACH LAW**: E(x) − plateau ~ x^4.00 (R² 1.0000).
- **THE K-TAIL LAW**: |E_K − E_∞| ~ exp(−0.805·K) (the y*^K
  geometric); the K ≥ 36 floor < 1e-12.
- **THE OFF-FAMILY FLOOR**: the descent at K=64 lands **+1.132e-11
  above √λ*** — 60x deeper than the Task-35 winner (+6.4e-10), the
  SVD backward error ±6.3e-13 — driven by tiny displacements (the
  B's ~4e-6, the couplings ~1e-7): the thinness quantified.  The
  x=1e-2 start stalls at +2.46e-9 — the deep path is delicate.
- **THE TIGHTNESS STATEMENT**: every measured point ABOVE √λ* and
  the floor within 1.1e-11 — **the compression infimum is
  consistent with √λ* EXACTLY (TIGHT): the power-sum class does
  not dip below √λ* at any measured level; the shadow-equivalence
  theorem's √λ* target CONFIRMED SHARP on the free side.**
- **THE B-EXIT**: the wall's ROOT caps B at 120; the x < 1.65e-3
  segment lies outside the box, covered analytically by the
  parameter-space-global compression bound.

**The Vol XIII gate is cleared** — the record content is complete
through Task 40 (the Corrigendum's Addendum 6: Tasks 38/39/40).

## The drain (the standing order)

One driver round post-closure: cover4d 54M → 54.5M calls
(27,186,871 leaves, all BDC: 9,847,477 e0 + 7,749,145 e4 +
9,590,249 e5; the frontier 32; ZERO stalls); the wall 680k → 700k
calls (306,401 certified: 135,406 window + 170,995 e4/e5; ZERO
stalls; 41 stack).  The flow law steady.

## The commits

- `d95152a` — Task 39: the gradient-split corollary refuted (the
  A/B, 0.84x, 324 stalls; the tail_law README row added).
- `6873cc6` — Task 40: the critical locus closed (the plateau law,
  the x^4 approach, the K-tail, the off-family floor +1.132e-11,
  the tightness; Addendum 6).
- `cac3d8e` — the drain increment (cover4d 54.5M / 27.19M leaves;
  wall 700k / 306,401 certified; zero stalls).

## The honest residue (next in queue)

- **The Vol XIII PDF regeneration** (the record content complete;
  the write-up the carried item).
- **The drain grind** (the standing order — the cover4d frontier
  32, the wall stack 41).
- **The unbounded far-field laws** (the third FW-4 item — the
  window's polynomial growth formalized).
- **The escape quantification** (the honest ℋ₂ residual — the
  curved-valley path beyond the quadratic model's reach, filed at
  HX-6).
- **The seed-level boundary** (carried).
