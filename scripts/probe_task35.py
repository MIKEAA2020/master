#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_task35.py — Task 35's DESIGN PROBES for the 12-parameter
free-class wall (D_free >= sqrt(lambda*)).

The wall's statement (the corpus's corrected sandwich, Task 32 part A):
D_free <= sqrt(lambda*) (the line atom, the closure attainment) — the
wall is the REVERSE inequality over the full 2-state WFA class
(B, C, A_a, A_b — 12 parameters, the domain rho(K) < 1).

THE FOUR DECISIVE MEASUREMENTS:

P-A  THE OFF-BLOCK PENALTY at the known points (the symmetric shadow,
     the free escape point, the Vol IX optimizer, the line-atom
     approach x -> 0 with 2px = c*): the FULL exact 6x6 norm vs the
     BLOCK-CONSTANT COMPRESSION norm ||P(H_cell - H_g)P|| — the
     compression theorem's instrument: ||M|| >= ||Cat - K_g|| with
     K_g(alpha,gamma) = B S_alpha S_gamma C / sqrt(mu_a mu_g) (the
     power-sum kernel; S_alpha = the Parikh-class matrix sums).  If the
     compression infimum sits at sqrt(lambda*) too, the wall has an
     abelian-side reduction; if it dips below, the off-block mass is
     essential and the engine must certify the full 6x6.

P-B  THE COMPRESSION INFIMUM (multi-start over the 12 parameters, the
     dense truncated evaluator, the K-bracket): the power-sum family's
     floor measured.

P-C  THE TRANSVERSE CURVATURE at the diagonal family's grid points
     (the symmetric shadow, the Vol IX optimizer, the boundary-valley
     approach, the random stable 2-atom configs): the 4x4 second-
     difference matrix in the FOUR COUPLING directions (A_a12, A_a21,
     A_b12, A_b21) with B, C held fixed — the uniform-positivity
     question (the tube-lift composition's premise: if kappa_min > 0
     over the whole abelian region, the 6-D certified abelian cover
     lifts to a 12-D tube with the transverse Taylor certificates).

P-D  THE WINDOW INSTRUMENT (O-2's cut-web window, |u|,|v| <= 2): the
     window residual at the known points (the corner-payment split)
     and the far-field explosion measurement (the window entries are
     POLYNOMIAL in the 12 parameters — the cheap root-box killer).
"""
import numpy as np
from math import factorial
from scipy.optimize import minimize

# the machinery (the corpus's exec-head pattern — probe_shadow2.py's
# exact 6x6 machinery, everything before its VOL_IX line)
SRC = ("/home/z/my-project/github_repos/master/scripts/"
       "probe_shadow2.py")
ns = {}
exec(compile(open(SRC).read().split("VOL_IX = ")[0], "ps2_head", "exec"),
     ns)
norm_of = ns["norm_of"]
build_GC = ns["build_GC"]
BLOCKS = ns["BLOCKS"]
MU = ns["MU"]
word_matrix = ns["word_matrix"]

LAMBDA_F = 1.6310919765642504
SQRT_L = LAMBDA_F ** 0.5
C_STAR = 0.3971672569443035
Y_STAR = 0.6563248795193563

rng = np.random.default_rng(35)


def x12_to_mats(x):
    Aa = np.array([[x[4], x[8]], [x[9], x[5]]])
    Ab = np.array([[x[6], x[10]], [x[11], x[7]]])
    return x[0:2], x[2:4], Aa, Ab


def norm12(x):
    return norm_of(*x12_to_mats(x))


X_SYM8 = np.load("/home/z/my-project/github_repos/master/scripts/"
                 "shadow_refined.npy")
X_SYM = np.concatenate([X_SYM8, np.zeros(4)])
X_FREE = np.load("/home/z/my-project/github_repos/master/scripts/"
                 "escape_refined.npy")
X_AB8 = np.array([2.77175129, -2.771744134, 1.0, 1.0,
                  0.07152188, -0.071722572, 0.656323579, 0.656321527])


# ------------------------------------------------------------------
# the power-sum class machinery (the compression kernel's basis)
# ------------------------------------------------------------------
def class_sums(Aa, Ab, K):
    """S_alpha for all alpha with |alpha|_1 <= K (the Parikh-class
    matrix sums): S_(i,j) = Aa S_(i-1,j) + Ab S_(i,j-1)."""
    S = {(0, 0): np.eye(2)}
    for n in range(1, K + 1):
        for i in range(n + 1):
            j = n - i
            M = np.zeros((2, 2))
            if i >= 1:
                M = M + Aa @ S[(i - 1, j)]
            if j >= 1:
                M = M + Ab @ S[(i, j - 1)]
            S[(i, j)] = M
    return S


def mu_of(a):
    return float(factorial(a[0] + a[1])
                 // (factorial(a[0]) * factorial(a[1])))


def compression_dense(B, C, Aa, Ab, K=24):
    """||P(H_cell - H_g)P|| — the block-constant compression of the
    free error: the kernel E(a,g) = sqrt(mu_a mu_g) 1_{a+g=(1,1)}
    - B S_a S_g C / sqrt(mu_a mu_g), dense SVD over |a|_1 <= K
    (the truncation bracket: the tail decays with the S_alpha)."""
    S = class_sums(Aa, Ab, K)
    grid = [(i, j) for n in range(K + 1)
            for i in range(n + 1) for j in [n - i]]
    n = len(grid)
    BS = [B @ S[a] for a in grid]
    SC = [S[g] @ C for g in grid]
    sm = [mu_of(a) ** 0.5 for a in grid]
    E = np.empty((n, n))
    for ai, a in enumerate(grid):
        row = np.empty(n)
        for gi in range(n):
            g = grid[gi]
            cell = (sm[ai] * sm[gi]
                    if (a[0] + g[0], a[1] + g[1]) == (1, 1) else 0.0)
            row[gi] = cell - (BS[ai] @ SC[gi]) / (sm[ai] * sm[gi])
        E[ai] = row
    sv = np.linalg.svd(E, compute_uv=False)
    return float(sv[0]), n


def line_atom_point(x):
    """the mirrored parity-odd family's approach to the line atom:
    A_a = diag(x,-x), A_b = diag(y*,y*), B = (c*/2x, -c*/2x), C=(1,1)
    — the 2px = c* boundary substitution (Task 32's CL-1 valley)."""
    p = C_STAR / (2.0 * x)
    return np.array([p, -p, 1.0, 1.0, x, -x, Y_STAR, Y_STAR,
                     0.0, 0.0, 0.0, 0.0])


# =====================================================================
print("=" * 72)
print("P-A — the off-block penalty at the known points")
print("=" * 72)
print("  the references: sqrt(lambda*) = %.13f" % SQRT_L)
rows = []
for tag, x in [("the symmetric shadow", X_SYM),
               ("the free escape point", X_FREE),
               ("the Vol IX optimizer", np.concatenate([X_AB8,
                                                        np.zeros(4)]))] \
        + [("the line atom x=%.0e" % xx, line_atom_point(xx))
           for xx in (5e-2, 1e-2, 2e-3, 5e-4)]:
    v_full = norm12(x)
    v_c, ngrid = compression_dense(*x12_to_mats(x), K=24)
    v_c16, _ = compression_dense(*x12_to_mats(x), K=16)
    rows.append((tag, v_full, v_c, v_c - v_c16))
    print("  %-24s full %.13f  compr %.10f (K24-K16: %+.1e)"
          % (tag, v_full, v_c, v_c - v_c16))
pen = [r[2] - SQRT_L for r in rows]
print("  the compression values sit %+.3e .. %+.3e above sqrt(lambda*)"
      % (min(pen), max(pen)))

# =====================================================================
print()
print("=" * 72)
print("P-B — the compression infimum (the power-sum family's floor)")
print("=" * 72)


def compr_obj(x):
    # the stability guard: the domain rho(K) < 1 (the bounded Hankels);
    # the exploding class sums would poison the dense evaluator
    B, C, Aa, Ab = x12_to_mats(x)
    rho = max(abs(np.linalg.eigvals(
        np.kron(Aa, Aa) + np.kron(Ab, Ab))))
    if rho >= 0.999 or not np.all(np.isfinite(x)):
        return 10.0
    v, _ = compression_dense(B, C, Aa, Ab, K=14)
    return v if np.isfinite(v) else 10.0


best_c, x_best_c = compr_obj(X_SYM), X_SYM.copy()
seeds = [X_SYM, X_FREE, np.concatenate([X_AB8, np.zeros(4)]),
         line_atom_point(2e-3)]
for i in range(8):
    if i < 4:
        s = seeds[i]
    else:
        s = X_SYM + rng.normal(size=12) * np.array(
            [0.3, 0.3, 0.3, 0.3, 0.02, 0.02, 0.02, 0.02,
             0.02, 0.02, 0.02, 0.02])
    r = minimize(compr_obj, s, method="Nelder-Mead",
                 options={"maxiter": 600, "xatol": 1e-10,
                          "fatol": 1e-12})
    if r.fun < best_c:
        best_c, x_best_c = float(r.fun), r.x.copy()
    print("    start %d: %.10f (best %.10f)" % (i, r.fun, best_c), flush=True)
v_hi, _ = compression_dense(*x12_to_mats(x_best_c), K=24)
print("  the compression infimum (multi-start, K=14): %.10f"
      "  -> the K=24 check: %.10f" % (best_c, v_hi))
print("  vs sqrt(lambda*) = %.10f : the power-sum floor sits %+.3e "
      "above" % (SQRT_L, v_hi - SQRT_L))

# =====================================================================
print()
print("=" * 72)
print("P-C — the transverse curvature at the diagonal family's grid")
print("=" * 72)


def curv_spectrum(x, t=1e-3):
    """the 4x4 second-difference matrix in the coupling directions
    (8..11) with B, C and the diagonals held fixed: K_ij = [V(t(e_i
    + e_j)) - V(t e_i) - V(t e_j) + V(0)] / t^2."""
    V0 = norm12(x) ** 2
    K = np.zeros((4, 4))
    Vd = []
    for d in range(4):
        xp = x.copy()
        xp[8 + d] += t
        Vd.append(norm12(xp) ** 2)
    for i in range(4):
        for j in range(i, 4):
            xp = x.copy()
            xp[8 + i] += t
            xp[8 + j] += t
            K[i, j] = K[j, i] = (norm12(xp) ** 2 - Vd[i]
                                 - Vd[j] + V0) / (t * t)
    return K


def rand_diag_point():
    """a random stable 2-atom diagonal config (in the abelian
    cover's regime): the mirrored pair + the generic pair."""
    while True:
        x1, y1 = rng.uniform(-0.9, 0.9), rng.uniform(-0.9, 0.9)
        x2, y2 = rng.uniform(-0.9, 0.9), rng.uniform(-0.9, 0.9)
        if x1 ** 2 + y1 ** 2 < 0.81 and x2 ** 2 + y2 ** 2 < 0.81:
            break
    p1, p2 = rng.uniform(-8, 8), rng.uniform(-8, 8)
    B = np.array([p1, p2]) / np.sqrt(abs(p1 * p2) + 1e-9) * 1.5
    C = np.array([p1, p2]) / B
    return np.array([B[0], B[1], C[0], C[1], x1, x2, y1, y2,
                     0.0, 0.0, 0.0, 0.0])


pts = [("the symmetric shadow", X_SYM),
       ("the Vol IX optimizer", np.concatenate([X_AB8, np.zeros(4)])),
       ("the line atom x=2e-3", line_atom_point(2e-3))]
for i in range(7):
    pts.append(("rand diag #%d" % i, rand_diag_point()))

kmins = []
for tag, x in pts:
    K = curv_spectrum(x)
    ev = np.linalg.eigvalsh(K)
    kmins.append((tag, ev[0], norm12(x)))
    print("  %-22s V=%.9f  kappa eig: %s" %
          (tag, norm12(x),
           " ".join("%+.2e" % e for e in ev)))
gpos = [e for (t, e, v) in kmins if e > 0]
print("  the gauge-flat note: the GL(2) orbit's tangent directions")
print("  carry ~0 curvature (the value's exact invariance); the")
print("  MODULI curvatures are the nonzero spectrum.")
print("  min eigenvalue over the grid: %+.3e (%d/%d positive)"
      % (min(e for _, e, _ in kmins), len(gpos), len(kmins)))

# =====================================================================
print()
print("=" * 72)
print("P-D — the window instrument (the cut-web window |u|,|v| <= 2)")
print("=" * 72)
WIN_WORDS = ["", "a", "b", "aa", "ab", "ba", "bb"]


def window_residual(x):
    B, C, Aa, Ab = x12_to_mats(x)
    n = len(WIN_WORDS)
    M = np.zeros((n, n))
    for i, u in enumerate(WIN_WORDS):
        for j, v in enumerate(WIN_WORDS):
            w = u + v
            cell = 1.0 if (w.count("a"), w.count("b")) == (1, 1) \
                else 0.0
            M[i, j] = cell - (B @ word_matrix(Aa, Ab, w) @ C)
    return float(np.linalg.svd(M, compute_uv=False)[0]), M


for tag, x in [("the symmetric shadow", X_SYM),
               ("the free escape point", X_FREE),
               ("the Vol IX optimizer", np.concatenate([X_AB8,
                                                        np.zeros(4)]))]:
    w, _ = window_residual(x)
    print("  %-24s window residual %.9f (full %.9f): the tail "
          "payment %.3e" % (tag, w, norm12(x), norm12(x) - w))
# the far-field explosion: scale B, C up
for s in (1.0, 2.0, 4.0, 8.0):
    x = X_SYM.copy()
    x[0:4] = x[0:4] * s
    w, _ = window_residual(x)
    print("  the B/C scale x%.0f: the window residual %.4f" % (s, w))
print()
print("probe done — the design verdicts feed free_class_wall.py")
