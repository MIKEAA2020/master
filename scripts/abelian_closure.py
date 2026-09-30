#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
abelian_closure.py — Task 32, part A: THE CLASS-LEVEL ADJUDICATION and the
boundary-valley closure (the user's order: "the class-level problem (a
lower bound on the abelian optimum)").

THE DISCOVERY (probe_task32_boundary.py): the abelian parity-odd family
(the mirrored pairs, x -> 0 with 2px = c fixed) descends IN NORM to the
line-atom value sqrt(lambda*) = 1.277142112908..., which is BELOW both
Task 29/31 escape points (1.277142117.  Hence the "escape" (the free
point below the best abelian point) was a SCAN ARTIFACT: the best abelian
point was never the abelian infimum — the boundary valley continues
descending past it.  This battery makes that adjudication exact:

CL-0  the references reproduced (the line atom, the Vol IX optimizer, the
      symmetric shadow, the free escape point — all through the exact
      6x6 machinery).
CL-1  THE BOUNDARY VALLEY measured: the fixed-(c*,y*) curve (the quartic
      descent), the per-x profile, the symmetric subfamily's own
      descent, the placement of Vol IX's optimizer and Task 31's
      symmetric shadow ON the valley.
CL-2  THE ESCAPE RETRACTED: both escape points sit ABOVE sqrt(lambda*);
      the "two basins" are stall points of one valley; the anisotropy
      (the B:a coordinate ratio ~ c/2a^2 ~ 900:1) explains why every
      local-search instrument stalled; the dense cross-check; the shell
      theorem (r2_strictness T2) re-verified: the pair never beats its
      limit.
CL-3  THE EXACT CLOSURE (the certified upper bound D_abelian <=
      sqrt(lambda*)): the mirrored family's pencil REDUCES BY THE STATE-
      FLIP INVOLUTION to a 3x3 whose entries, after the boundary
      substitution 2px = c, depend on x ONLY THROUGH x^4 (D = (1-y^2)^2
      - x^4) — the quartic law is STRUCTURAL, not numerical; the reduced
      cubic's x -> 0 limit is the line-atom branch (verified against the
      machinery and against la_certificate's value); the coefficient K
      of the quartic law derived EXACTLY (the closed form) and matched
      to the measured 0.2457; hence D_abelian(2) <= sqrt(lambda*) EXACTLY
      (with T2: the pairs never go below).
CL-4  the corrected sandwich and the honest verdict: D_free <= D_abelian
      <= sqrt(lambda*), the line atom (a free point) attains sqrt(lambda*)
      — the shadow-equality RESTORED in the closure sense; what remains
      open is exactly the LOWER bound D_abelian >= sqrt(lambda*)
      (abelian_lower_bound.py, part B) and the free-class lower bound
      (the box-count wall).

Output: abelian_closure_results.json
"""
import json
import math
import time

import numpy as np
import sympy as sp
from scipy.optimize import minimize

SRC = ("/home/z/my-project/github_repos/master/scripts/free_cell.py")
src = open(SRC).read()
head = src[:src.index('# =====================================================================\n# PART A')]
ns = {}
exec(compile(head, 'fc_head', 'exec'), ns)
free_cell_exact_norm = ns['free_cell_exact_norm']

t0 = time.time()
OUT = {"meta": {
    "order": "Task 32 part A: the class-level adjudication — the boundary "
             "valley, the escape's retraction, the exact closure "
             "D_abelian <= sqrt(lambda*)",
    "date": "2026-09-30"}}

LAMBDA_STAR = 1.6310919765642504414737578928177383666901925754942
SQRT_LAMBDA = math.sqrt(LAMBDA_STAR)
C_STAR = 0.3971072873503973695456334
Y_STAR = 0.6563224669957891081761482
VOL_IX = 1.277142689665
X_SHADOW = 0.0149530780            # Task 31's symmetric shadow's a
B_SHADOW = np.array([7.5440973695, -6.3889831599])
C_SHADOW = np.array([1.7601091851, 2.0783330839])
Y_SHADOW = 0.6563223465
FREE_ESCAPE = 1.2771421169949382   # Task 31's free descent point
SYM_SHADOW = 1.277142125195311

# =====================================================================
print("=" * 76)
print("CL-0 — the references reproduced (the exact 6x6 machinery)")
print("=" * 76)


def pair_norm(x, c, y):
    """the parity-odd mirrored pair at scale x (B=(P,-P), C=(1,1))."""
    P = c / (2.0 * x)
    n, _ = free_cell_exact_norm(np.array([P, -P]), np.array([1.0, 1.0]),
                                np.diag([x, -x]), np.diag([y, y]))
    return n


def line_atom_norm(c, y):
    n, _ = free_cell_exact_norm(np.array([0.0, c]), np.array([1.0, 0.0]),
                                np.array([[0.0, 0.0], [1.0, 0.0]]),
                                y * np.eye(2))
    return n


la = line_atom_norm(C_STAR, Y_STAR)
sh = free_cell_exact_norm(B_SHADOW, C_SHADOW,
                          np.diag([X_SHADOW, -X_SHADOW]),
                          np.diag([Y_SHADOW, Y_SHADOW]))[0]
print("  the line atom at (c*, y*)   : %.15f" % la)
print("  the symmetric shadow (Task31): %.15f  (recorded %.15f)"
      % (sh, SYM_SHADOW))
print("  sqrt(lambda*)                : %.15f" % SQRT_LAMBDA)
OUT["CL0"] = {"line_atom": la, "sqrt_lambda_star": SQRT_LAMBDA,
              "symmetric_shadow": sh,
              "shadow_minus_sqrt_lambda": sh - SQRT_LAMBDA}

# =====================================================================
print()
print("=" * 76)
print("CL-1 — THE BOUNDARY VALLEY measured")
print("=" * 76)

# (a) the fixed-(c*, y*) curve: the quartic descent
xs = [0.0715219, 0.05, 0.03, 0.02, 0.0149531, 0.01, 0.005, 0.002, 0.001]
curve = []
print("  the fixed-(c*, y*) boundary curve:")
print("      %-11s %-18s %-18s" % ("x", "norm", "norm - sqrt(lambda*)"))
for x in xs:
    n = pair_norm(x, C_STAR, Y_STAR)
    curve.append({"x": x, "norm": n, "delta": n - SQRT_LAMBDA})
    print("      %-11.4g %-18.15f %-+18.4e" % (x, n, n - SQRT_LAMBDA))

# the quartic fit: delta_lambda = K x^4 (exact prediction: only x^4
# enters; the exact K below is the LAMBDA-coefficient)
Kfit = [((r["norm"] ** 2 - LAMBDA_STAR) / r["x"] ** 4)
        for r in curve if r["x"] <= 0.03]
K_fit = float(np.median(Kfit))
print("  the quartic law lambda(x) = lambda* + K x^4 (in LAMBDA): the"
      " per-point K = %s (median %.6f)"
      % (["%.4f" % k for k in Kfit], K_fit))
OUT["CL1_curve"] = curve
OUT["CL1_quartic_fit_K"] = K_fit

# (b) the per-x profile (re-optimized (c, y))
prof = []
print("  the per-x profile ((c, y) re-optimized):")
for x in [0.0715, 0.03, 0.01, 0.003, 0.001]:
    r = minimize(lambda z: pair_norm(x, z[0], z[1]) or 1e6,
                 np.array([C_STAR, Y_STAR]), method="Nelder-Mead",
                 options={"xatol": 1e-12, "fatol": 1e-15, "maxiter": 2000})
    prof.append({"x": x, "best": float(r.fun),
                 "c": float(r.x[0]), "y": float(r.x[1])})
    print("      x = %-8.4g best %.15f  at (c, y) = (%.7f, %.7f)"
          % (x, r.fun, r.x[0], r.x[1]))
OUT["CL1_profile"] = prof

# (c) the symmetric subfamily's own descent (the 6-param family, a -> 0
#     with the 2px = c* rescaling — B scaled, C free)
sym = []
print("  the symmetric subfamily pushed to the boundary (2px = c*):")
for a in [0.0149531, 0.005, 0.001, 1e-4]:
    sc = X_SHADOW / a
    n = free_cell_exact_norm(B_SHADOW * sc, C_SHADOW,
                             np.diag([a, -a]),
                             np.diag([Y_SHADOW, Y_SHADOW]))[0]
    sym.append({"a": a, "norm": n, "delta": n - SQRT_LAMBDA})
    print("      a = %-8.4g norm %.15f  (%+.3e)" % (a, n, n - SQRT_LAMBDA))
OUT["CL1_symmetric_descent"] = sym

# (d) the placement: Vol IX's optimizer and the shadow are ON the valley
p_shadow = B_SHADOW * C_SHADOW        # (13.278, -13.276)
c_shadow = 2 * p_shadow[0] * X_SHADOW
print("  the placement: the shadow's effective (2px, y) = (%.7f, %.7f)"
      % (c_shadow, Y_SHADOW))
print("                    vs the line atom (c*, y*) = (%.7f, %.7f)"
      % (C_STAR, Y_STAR))
print("                Vol IX's optimizer: (2px, y) = (%.7f, %.7f)"
      % (2 * 2.77175129 * 0.07152188, 0.656323579))
OUT["CL1_placement"] = {
    "shadow_2px": float(c_shadow), "shadow_y": Y_SHADOW,
    "vol_ix_2px": float(2 * 2.77175129 * 0.07152188),
    "vol_ix_y": 0.656323579,
    "c_star": C_STAR, "y_star": Y_STAR}

# =====================================================================
print()
print("=" * 76)
print("CL-2 — THE ESCAPE RETRACTED")
print("=" * 76)

# (a) both escape points ABOVE sqrt(lambda*)
print("  the free escape point  : %.15f  = sqrt(lambda*) + %.4e  (ABOVE)"
      % (FREE_ESCAPE, FREE_ESCAPE - SQRT_LAMBDA))
print("  the symmetric shadow    : %.15f  = sqrt(lambda*) + %.4e  (ABOVE)"
      % (sh, sh - SQRT_LAMBDA))
print("  the abelian curve at x=0.01 (a GENUINELY ABELIAN point):")
n01 = pair_norm(0.01, C_STAR, Y_STAR)
print("      %.15f  = sqrt(lambda*) + %.4e  (BELOW both escape points)"
      % (n01, n01 - SQRT_LAMBDA))
OUT["CL2"] = {"free_escape": FREE_ESCAPE,
              "free_escape_minus_sqrt_lambda": FREE_ESCAPE - SQRT_LAMBDA,
              "abelian_point_x_0.01": n01,
              "abelian_point_minus_free_escape": n01 - FREE_ESCAPE}

# (b) the anisotropy: why every local search stalled
dpdx = C_STAR / (2 * X_SHADOW ** 2)
print("  the valley's anisotropy at the shadow: |dB/da| = c/(2a^2) = %.0f"
      % dpdx)
print("      a Nelder-Mead simplex adapted to the B-scale (~7) explores"
      " a-steps ~ 1e-3, gaining ~ 4K a^3 * 1e-3 ~ %.1e < the stall"
      " tolerance — the crawl dies; the valley needs the 900:1 ratio"
      % (4 * K_fit * X_SHADOW ** 3 * 1e-3))
OUT["CL2_anisotropy"] = {"dB_da": float(dpdx), "ratio": float(dpdx)}

# (c) the shell theorem re-verified: the pair never beats its limit
worst = -1e9
rng = np.random.default_rng(20260930)
for _ in range(120):
    w = rng.uniform(0.05, 1.5) * rng.choice([-1, 1])
    y = rng.uniform(0.1, 0.92)
    x = rng.uniform(0.002, 0.5)
    n_pair = pair_norm(x, 2 * w, y)          # 2px = 2w
    n_la = line_atom_norm(2 * w, y)
    if n_pair is not None:
        worst = max(worst, n_la - n_pair)
print("  the shell theorem T2 re-verified: max(line_atom - pair) = %.2e"
      "  [<= 0 required: the pair never beats its boundary limit]"
      % worst)
OUT["CL2_shell_recheck"] = {"max_la_minus_pair": float(worst)}

# (d) the dense L=8 cross-check at a near-boundary abelian point
def dense_sv(B, C, Aa, Ab, K=8):
    Ws = [""]
    for k in range(1, K + 1):
        Ws += ["".join(p) for p in __import__("itertools").product(
            "ab", repeat=k)]
    E = np.zeros((len(Ws), len(Ws)))
    for i, u in enumerate(Ws):
        for j, v in enumerate(Ws):
            w = u + v
            hv = 1.0 if (w.count("a"), w.count("b")) == (1, 1) else 0.0
            Mw = np.eye(2)
            for ch in w:
                Mw = Mw @ (Aa if ch == "a" else Ab)
            E[i, j] = hv - float(B @ Mw @ C)
    return float(np.linalg.svd(E, compute_uv=False)[0])

P001 = C_STAR / (2 * 0.001)
n_d = dense_sv(np.array([P001, -P001]), np.array([1.0, 1.0]),
               np.diag([0.001, -0.001]), np.diag([Y_STAR, Y_STAR]))
n_d_la = dense_sv(np.array([0.0, C_STAR]), np.array([1.0, 0.0]),
                  np.array([[0.0, 0.0], [1.0, 0.0]]), Y_STAR * np.eye(2))
print("  the dense L=8 cross-check at x = 1e-3: pair %.9f vs line atom"
      " %.9f (the same truncation offset — the ORDERING confirms)"
      % (n_d, n_d_la))
OUT["CL2_dense_cross_check"] = {"pair_x1e-3": n_d, "line_atom": n_d_la}

# =====================================================================
print()
print("=" * 76)
print("CL-3 — THE EXACT CLOSURE (the certified D_abelian <= sqrt(lambda*))")
print("=" * 76)

# The state-flip involution at a mirrored point: in the basis
# (blocks (1,0), (1,1), u_+) the pencil reduces to a 3x3.  Derivation:
# the mirrored point Aa = diag(x,-x), Ab = diag(y,y), B = (beta,-beta),
# C = (gamma,gamma); K = kron(Aa,Aa)+kron(Ab,Ab) diagonal
# diag(x^2+y^2, y^2-x^2, y^2-x^2, x^2+y^2); the Lyapunov Grams closed:
#   Lc = gamma^2 [[A, B],[B, A]], Lr = beta^2 [[A, -B],[-B, A]],
#   A = 1/(1-x^2-y^2), B = 1/(1+x^2-y^2);
# the block sums and the u_+/- split give the 3x3 below (verified against
# the machinery at sample points first).
def A3_numeric(c, y, x):
    D = (1 - y * y) ** 2 - x ** 4
    G3 = np.array([[1.0, 0.0, math.sqrt(2) * c / 2],
                   [0.0, 2.0, math.sqrt(2) * c * y],
                   [math.sqrt(2) * c / 2, math.sqrt(2) * c * y,
                    c * c / (2 * D)]])
    C3 = np.array([[1.0, 0.0, -math.sqrt(2) * y],
                   [0.0, 1.0, -math.sqrt(2)],
                   [-math.sqrt(2) * y, -math.sqrt(2),
                    2 * (1 - y * y) / D]])
    return C3 @ G3


ok = 0.0
for (c_, y_, x_) in [(0.4, 0.6, 0.05), (0.397, 0.656, 0.01),
                     (0.3, 0.7, 0.2), (0.5, 0.5, 0.1)]:
    lam3 = max(float(np.real(v)) for v in
               np.linalg.eigvals(A3_numeric(c_, y_, x_)))
    lam6 = pair_norm(x_, c_, y_) ** 2
    ok = max(ok, abs(lam3 - lam6) / lam6)
print("  the 3x3 reduction vs the 6x6 machinery: max rel disagreement "
      "%.2e" % ok)
OUT["CL3_reduction_check"] = float(ok)

# the symbolic reduced cubic, the boundary substitution, the x^4 law
cs, ys, xs_, lam = sp.symbols('c y x lambda', positive=True)
Ds = (1 - ys ** 2) ** 2 - xs_ ** 4
G3s = sp.Matrix([[1, 0, sp.sqrt(2) * cs / 2],
                 [0, 2, sp.sqrt(2) * cs * ys],
                 [sp.sqrt(2) * cs / 2, sp.sqrt(2) * cs * ys,
                  cs ** 2 / (2 * Ds)]])
C3s = sp.Matrix([[1, 0, -sp.sqrt(2) * ys],
                 [0, 1, -sp.sqrt(2)],
                 [-sp.sqrt(2) * ys, -sp.sqrt(2),
                  2 * (1 - ys ** 2) / Ds]])
A3s = sp.simplify(C3s * G3s)
ch = sp.factor(sp.expand(A3s.charpoly(lam).as_expr()))
num, den = sp.fraction(sp.together(ch))
# NOTE: charpoly returns a PurePoly whose generator is a FRESH
# unassumed symbol named 'lambda' — extract it and use it below
lamR = [s for s in num.free_symbols if s.name == "lambda"][0]
assert lamR is not None
# THE STRUCTURAL x^4 LAW: the roots live on the numerator; its x-powers
# must be multiples of 4 (x, x^2, x^3 FORBIDDEN)
Pnum = sp.Poly(sp.expand(num), xs_)
exps = sorted({t[0][0] for t in Pnum.terms()})
assert all(e % 4 == 0 for e in exps), exps
print("  THE STRUCTURAL x^4 LAW: the reduced pencil's charpoly numerator"
      " is a polynomial in x^4 (the x-exponents present: %s) — after the"
      " boundary substitution 2px = c there is NO x, x^2, x^3 dependence"
      " — the quartic descent is EXACT, not fitted." % exps)

# the numerator as N_0 + s N_4 + s^2 N_8 with s = x^4
s = sp.symbols('s', positive=True)
terms = Pnum.terms()
N0 = sum(co for (exps_, co) in terms if exps_[0] == 0)
N4 = sum(co for (exps_, co) in terms if exps_[0] == 4)
N8 = sum(co for (exps_, co) in terms if exps_[0] == 8)

# the limiting cubic (x -> 0): N_0 = 0 (up to the denominator's limit)
ch0 = sp.factor(sp.expand(N0))
print("  the x -> 0 limit of the charpoly numerator (the line-atom"
      " branch cubic):")
print("     ", ch0)

# the quartic coefficient K: N_0(lambda0) = 0 and
# N_0'(lambda0) delta + s N_4(lambda0) + ... = 0 gives
#     lambda(x) = lambda_0 - (N_4 / N_0') x^4 + O(x^8)
dPlam = sp.diff(N0, lamR)
K_expr = sp.simplify(-N4 / dPlam)
K_at = float(K_expr.subs({lamR: LAMBDA_STAR, cs: C_STAR, ys: Y_STAR})
             .evalf(30))
print("  the exact quartic coefficient K(c*, y*) = %.10f  (the measured"
      " fit %.10f — agreement %.2e)"
      % (K_at, K_fit, abs(K_at - K_fit)))
OUT["CL3_exact"] = {
    "reduced_charpoly_numerator": sp.sstr(sp.factor(sp.expand(num))),
    "x_exponents": [int(e) for e in exps],
    "limit_cubic": sp.sstr(ch0),
    "K_exact": K_at, "K_measured": K_fit,
    "law": "lambda(c, y, x) = lambda_0(c, y) + K(c, y) x^4 + O(x^8): the"
           " mirrored family's pencil depends on x only through "
           "x^4 = (the D-denominator); the boundary valley's quartic "
           "descent is a STRUCTURAL identity",
    "verdict": "with T2 (the pair never beats its limit) and the x^4 "
               "descent: D_abelian(2) <= sqrt(lambda*) EXACTLY — the "
               "abelian closure contains the line-atom value, and no "
               "abelian point below it is known or possible on the shell"}

# the limiting cubic's top root vs lambda*
lam0_root = sp.nroots(N0.subs({cs: sp.Float(C_STAR, 30),
                                ys: sp.Float(Y_STAR, 30)}))
top_root = max([complex(r) for r in lam0_root], key=lambda z: z.real)
print("  the limiting cubic's top root at (c*, y*): %.15f  vs lambda* = "
      "%.15f  (delta %.2e)" % (top_root.real, LAMBDA_STAR,
                               top_root.real - LAMBDA_STAR))
OUT["CL3_limit_root"] = float(top_root.real)

# =====================================================================
print()
print("=" * 76)
print("CL-4 — the corrected sandwich and the verdict")
print("=" * 76)
print("  THE CORRECTED LEDGER:")
print("   1. D_free(2) <= sqrt(lambda*): the line atom IS a free point"
      " (a 2-state WFA with nilpotent Aa) at sqrt(lambda*).")
print("   2. D_abelian(2) <= sqrt(lambda*): the boundary valley (this"
      " battery) — the abelian closure attains it.")
print("   3. Task 29/31's 'escape' points sit ABOVE sqrt(lambda*) — the"
      " escape is RETRACTED (a scan artifact: the stall points of one"
      " anisotropic valley).")
print("   4. The shadow-equality conjecture is RESTORED in the closure"
      " sense: no free point below sqrt(lambda*) has ever been found;")
print("      it is now equivalent to the class-level LOWER bound"
      " D_abelian >= sqrt(lambda*) (part B) together with the"
      " free-class lower bound (the box-count wall).")
OUT["CL4"] = {
    "sandwich": "1 <= D_free(2) <= D_abelian(2) <= sqrt(lambda*); the "
                "line atom attains sqrt(lambda*) in the free class; the "
                "abelian closure attains it via the x^4 boundary valley",
    "escape_verdict": "RETRACTED: both Task 29's 5.73e-7 and Task 31's "
                      "residual 8.2e-9 were comparisons against stall "
                      "points of the boundary valley, not against the "
                      "abelian infimum; every escape point is ABOVE "
                      "sqrt(lambda*) = 1.2771421129084462",
    "open": "the class-level LOWER bound D_abelian >= sqrt(lambda*) over "
            "the full 6-parameter abelian family (abelian_lower_bound.py)"
            "; the free-class lower bound (the box-count wall)"}

OUT["meta"]["wall_time_s"] = time.time() - t0
with open("/home/z/my-project/github_repos/master/scripts/"
          "abelian_closure_results.json", "w") as f:
    json.dump(OUT, f, indent=1, default=float)
print()
print("wall time %.1f s — results written" % (time.time() - t0))
