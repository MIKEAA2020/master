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
