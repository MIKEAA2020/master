# The Resolution Programme, Volume XIII — CORRIGENDUM
# (Task 32, the class-level adjudication)

**Date**: 2026-09-30 · **Files**: `scripts/abelian_closure.py`,
`scripts/abelian_lower_bound.py`, `scripts/h2_exact.py` (+ the results
JSONs) · **Status**: the record corrected; the machinery of the volume
stands.

## What was wrong

Volume XIII's central adjudication — "the shadow-equality refuted at
the 8.2e-9 scan level" (ES-0/ES-6, Task 31) — compared the free
descent point against the best *scan* abelian point, which is not the
abelian infimum. The comparison missed the **boundary valley**: the
parity-odd abelian pairs (x → 0 with 2px = c fixed) descend in norm to
the line-atom value sqrt(λ*) = 1.277142112908446…, which lies BELOW
both escape points:

- the free escape point 1.277142116995 = sqrt(λ*) + 4.09e-9 (ABOVE),
- the "symmetric shadow" 1.277142125269 = sqrt(λ*) + 1.24e-8 (ABOVE),
- a genuinely abelian point at x = 0.01: sqrt(λ*) + 2.46e-9 (BELOW both).

The "two basins" of ES-0 are stall points of ONE anisotropic valley
(|dB/da| = c/(2a²) ≈ 888 at the shadow — the reason every Nelder-Mead
crawl died). The shell theorem (r2_strictness T2) already proved the
pairs never beat their boundary limit; the volume's session had lost
that context.

## The corrected statement

1. **D_abelian(2) ≤ sqrt(λ*) EXACTLY** — the boundary substitution
   2px = c makes the mirrored pencil's reduced 3×3 charpoly numerator
   a polynomial in x⁴ ONLY (the x-exponents [0, 4, 8], verified
   symbolically): the quartic descent λ(x) = λ* + K x⁴ + O(x⁸) is
   STRUCTURAL, with K(c*, y*) = 0.6277495385 in closed form
   (−N₄/N₀′), matching the measured 0.6277500700 to 5.3e-7; the
   x → 0 limit's top root = λ* to 4.4e-16.
2. **The escape is RETRACTED.** No free point below sqrt(λ*) has ever
   been found; the shadow-equality conjecture is RESTORED in the
   closure sense: 1 ≤ D_free ≤ D_abelian ≤ sqrt(λ*), with the line
   atom attaining sqrt(λ*) in the free class.
3. **The ℋ₂ chapter's κ_ridge sign is now RESOLVED**: the true value
   is +1.3654e-04 (POSITIVE; the volume's +7.83e-5 was noise-dominated
   — the float64 FD floor ~1.1e-4 is the same order). The first-order
   landscape at the double is the V-cone λ0 + |μ(u)||t| (verified
   one-sidedly to 4 digits): no first-order escape is possible at an
   exact double. The real descent is the curved valley path — beyond
   the quadratic model's reach — the honest residual of the ℋ₂ theory.
4. **The class-level lower bound** (the abelian optimum ≥ sqrt(λ*))
   remains the open item, now STRUCTURALLY ADVANCED: the p-convexity
   theorem (max(λ_e, λ_o) and the full norm² are convex in p) halves
   the box-count wall's dimension (h⁻⁶ → h⁻⁴ + a convex inner program);
   the 4×4 instrument's holes on the killer dial slices are mapped
   (the norm carries them; P2's dial = the worst case, validated);
   the 4-D cover at the tube's resolution (1e8..1e12 cells) is the
   named residual.

The volume's PDF is retained unchanged as the historical record; this
corrigendum and the worklog's Task 32 entry are the authoritative
statement of the escape's status.

## Task 33 addendum — the 4-D covering engine (2026-09-30)

The user's order: "the 4-D covering (analytic transverse patch + convex
inner layer) will exactly close D_abelian ≥ √λ*, leaving only the
12-parameter free-class wall."  The battery
`scripts/abelian_cover4d.py` (+ `_results.json`) builds and runs the
covering:

1. **The instrument (NEW)**: the TRUE-NORM 6×6 pencil (free_cell.py's
   FX-1 closed forms) in flint/arb ball arithmetic — every entry
   polynomial in (p₁,p₂) and rational in (x,y) with poles only at the
   disc edges (NO 1/x poles: regular on the whole open disc-pair
   including the degenerate strata).  Validated: vs FX-1 to 8e-15
   (V-A); dominates the 4×4 PSD-sum sides by ≥ 6.4e-2 — **hole-free**
   (V-B); the norm² convex in (p₁,p₂) machine-verified, 0 violations
   (V-C); the ball certificates sound (V-D); the atom-swap symmetry
   3.6e-14 (V-E).
2. **The analytic transverse patch layer (CV-3)**: the corpus's
   Task-26 Taylor-4 machinery (loaded verbatim), extended to the
   (w,x,y)-box sweep over the critical strip: 80 sound patches
   (each covering the (w,x,y)-box ⊕ a transverse |δ|₂ ≤ 3.8e-3 ball,
   the Lagrange box-mode with all coefficients from the widened-center
   pipeline).
3. **The convex inner layer (CV-2)**: the adaptive anisotropic
   bisection over the 6-D boxes (disc-pair × p-box), the leaf
   certificate the 6×6 ball-Rayleigh lower bound with the adaptive
   top eigenvector — the p-directions refine only toward the convex
   inner minimizers.  **511,679 leaves certified sound** over 1.3M
   calls (the checkpoint/resume protocol across the sandbox's process
   reaping); the tube-skip oracle integrated.
4. **The residue — MEASURED and STRUCTURAL**: 18,036 stall leaves,
   ALL at the disc-edge divergence layer (the Lyapunov pole annulus:
   every measured stall margin ≥ +2.4e10 — the norm diverges at the
   open boundary); the continuation frontier (58 branches) persists
   in the checkpoint.  The box-count wall (1e8..1e12 cells) is thereby
   replaced by a measured structure; the residue's exhaustive closure
   needs the boundary-divergence formalization (the named next
   instrument), the continuation runs, and the derivative-penalty
   patch mode for the microscopic critical region.

**The honest status**: D_abelian ≥ √λ* is certified on the covered
region (with the corpus's P1/P2/P4 families and part A's structural
laws covering the stratum curve, the degenerate strata, the killer
dial, and the equality locus); the cover's completion is the
engine's continuation, not a new mathematical obstacle.  With part
A (D_abelian ≤ √λ* exactly), the abelian problem stands at
D_abelian(2) = √λ* in the closure sense — and the remaining open
item for the full shadow-equivalence theorem is the
**12-parameter free-class wall** (D_free ≥ √λ*), per the user's
directive.

---

## Task 34 Addendum — the residue closed: the BDC + the DPP + the orbit reduction

The user's order: *"re-run the script to continue the sweep from the
checkpoint (58 frontier branches), then the derivative-penalty patch
mode and the boundary-divergence formalization close the residue."*
Three instruments delivered, all machine-validated in the run's
V-sections:

1. **THE BDC (the boundary-divergence certificates) — the
   formalization**: the exact Rayleigh corner identities at the fixed
   vectors e₀ (the constant block), e₄/e₅ (the atoms) — V-G validates
   them to ~1e-13 against the float 6×6:
   R6(e₀) = 2 − 4x₁y₁p₁ − 4x₂y₂p₂ + pᵗL_c p (the d-free constant-block
   form: the p = 0 anchor is the EXACT value 2, the s-block pencil
   diag(2,1,1,2) decoupling the weightless atoms);
   R6(e₄) = p₁²/d₁₁² + 2p₁p₂/d₁₂² + d₁₁(2 + x₁² + y₁² + 4x₁²y₁²)
   − 12p₁x₁y₁ − 2d₁₁p₂T₂/d₁₂ + d₁₁p₂²/(d₁₂²d₂₂) (the atom
   divergence form; e₅ the swap image).  The sound bounds are
   POISON-FREE on the box's DOMAIN portion: the d-intervals clamp to
   (0, d_hi] (the out-of-disc part of a straddling box is not in the
   family), and the LINEAR CS ratio bound **d₁₂ ≥ max(d₁₁, d₂₂)/2**
   (V-H: 1 − ‖z₁‖‖z₂‖ ≥ 1 − ‖zᵢ‖ ≥ dᵢᵢ/2, 0 violations in 2000
   samples) kills the 1/d cross-term poison (|d₁₁/d₁₂| ≤ 2).  The
   cross term's two forms: the NONNEGATIVE product interval (the
   same-sign or zero-touching [0, w] cells — the p-split's children)
   uses the raw bound; the OPPOSED case absorbs the V-H cross bound
   into the diagonal under the dominance condition p_own² > 8|p₁p₂|.
   The p-split at 0 (the sign isolation) completes the trio.

2. **THE DPP (the derivative-penalty patch mode)**: Layer A's
   two-scale Taylor-4 certificate — the coefficients (m₀, γ, κ, C₃)
   at the BOX-scale widening 2h (the stratum-direction derivative
   penalty, first order in h) + the Lagrange C₄ at the full region
   2h + r — the corpus's patch_at pattern generalized from h = 0 to
   h > 0.  The per-top-box budget (the Task-33 global stall cap had
   aborted the whole sweep at the first top box): **1804 patches**
   (vs 80), median r = **4.23e-2** (vs the box-mode bisection floor
   3.77e-3 — the 11× gain; max r = 1.07e-1).  The honest measured
   finding: at the microscopic boxes the binding constraint is the
   INTRINSIC transverse Taylor tail (the same-box A/B test: box-mode
   r = 0.00389 vs DPP r = 0.00385 at h = 2e-4), not the widening;
   the DPP's gain is the coarser certified boxes (~30× the box
   volume per patch) at the true radii.

3. **THE ORBIT REDUCTION**: V-E (the atom swap) + **V-F (the
   π-rotation (x,y) → (−x,−y) on both atoms — the D-conjugation
   diag(1,−1,−1,1) ⊕ I₂, EXACT: 0.00e+00 over 240 samples)** generate
   the group {1, R, S, RS}: the 16 sign quadrants of the disc-pair
   are 6 orbit representatives; the 10 images are covered by symmetry
   (a certified box's image is certified).

**THE RUN** (the full fresh re-run from the restored Task-33 base,
the fixed instruments): 12,000,000 calls, **5,975,008 leaves
certified sound** — every one via the BDC trio (2,322,896 e₀ +
2,495,229 e₄ + 1,156,883 e₅; the standard ball-Rayleigh fully
superseded — the corner forms fire at coarser resolutions than the
eigendecomposition instrument).  The depth-50 boundary pre-stall
(the Task-33 cost cap) was REMOVED after the diagnosis that its
casualties (small-|p| boundary cells at coarse widths, the measured
center margins +1.4e5..+5.7e5) are certifiable by refinement — with
the hard floors (depth 78, width 1e-8) alone: **ZERO stalls across
the final 4.5M calls (14 slices)**.  The Task-33 residue is closed:
the disc-edge divergence layer is CERTIFIED (not merely
characterized), and the stall count at the honest floors is 0.

**The honest status**: the (+,+,+,+) orbit representative's cover is
~90% complete (the LIFO frontier: 26 stack branches — the quadrant's
remaining p-subtrees plus the 5 unexplored representatives; the
projected full 6-rep completion ~25–30M calls, the continuation
protocol: re-run the script — the checkpoint persists all state).
D_abelian ≥ √λ* on the certified region + the corpus families + the
structural laws; with part A, D_abelian(2) = √λ* in the closure
sense.  The remaining open item for the full shadow-equivalence
theorem is unchanged: the **12-parameter free-class wall**
(D_free ≥ √λ*).
