#!/usr/bin/env python3
"""quick_1d_check2.py — the corrected shell/corner reduction check.

CORRECTED CLAIM: the line-atom norm ||M_line(c,y)|| equals the norm of the
CORNER block (u_a=1 words) x (v_a=0 words) of the error — which is the
MULTIPLICITY-WEIGHTED 1-D Hankel problem:

    basis {col_0, col_1, v(r)}  (target columns + the weighted atom vector)
    G = [[2, 0, 2r], [0, 1, 1], [2r, 1, 1/(1-r^2)^2]]
    C = [[1, 0, -w], [0, 1, -wr], [-w, -wr, w^2/(1-r^2)]]
    ||M||^2 = lambda_max(C.G)

(the multiplicity: words b^i a b^j with i+j = n are (n+1) many — the row
weights of the shell; = the multinomial weight mu(1, n) = n+1 on the line
gamma = (1, n).)
"""
import math
import numpy as np

SRC = "/home/z/my-project/github_repos/master/scripts/free_cell.py"
src = open(SRC).read()
head = src[:src.index('# =====================================================================\n# PART A')]
ns = {}
exec(compile(head, 'fc_head', 'exec'), ns)
free_cell_exact_norm = ns['free_cell_exact_norm']


def line_atom_norm(c, y):
    B = np.array([0.0, c])
    C = np.array([1.0, 0.0])
    Aa = np.array([[0.0, 0.0], [1.0, 0.0]])
    Ab = y * np.eye(2)
    n, _ = free_cell_exact_norm(B, C, Aa, Ab)
    return n


def w1d_one_atom(w, r):
    """the multiplicity-weighted 1-D Hankel norm of delta_1 - w r^n
    (the 3x3 exact eigenproblem)."""
    t = 1.0 - r * r
    G = np.array([[2.0, 0.0, 2.0 * r],
                  [0.0, 1.0, 1.0],
                  [2.0 * r, 1.0, 1.0 / (t * t)]])
    C = np.array([[1.0, 0.0, -w],
                  [0.0, 1.0, -w * r],
                  [-w, -w * r, w * w / t]])
    ev = np.linalg.eigvals(C @ G)
    lam = max(float(np.real(e)) for e in ev)
    return math.sqrt(max(0.0, lam))


def w1d_two_atoms(w1, r1, w2, r2):
    """the multiplicity-weighted 1-D Hankel norm of delta_1 - w1 r1^n
    - w2 r2^n (the 4x4 exact eigenproblem)."""
    t1 = 1.0 - r1 * r1
    t2 = 1.0 - r2 * r2
    t12 = 1.0 - r1 * r2
    G = np.array([
        [2.0, 0.0, 2.0 * r1, 2.0 * r2],
        [0.0, 1.0, 1.0, 1.0],
        [2.0 * r1, 1.0, 1.0 / (t1 * t1), 1.0 / (t12 * t12)],
        [2.0 * r2, 1.0, 1.0 / (t12 * t12), 1.0 / (t2 * t2)]])
    C = np.array([
        [1.0, 0.0, -w1, -w2],
        [0.0, 1.0, -w1 * r1, -w2 * r2],
        [-w1, -w1 * r1, w1 * w1 / t1, w1 * w2 / t12],
        [-w2, -w2 * r2, w1 * w2 / t12, w2 * w2 / t2]])
    ev = np.linalg.eigvals(C @ G)
    lam = max(float(np.real(e)) for e in ev)
    return math.sqrt(max(0.0, lam))


print("=== consistency: line-atom 6x6 machinery vs the weighted-1-D 3x3 ===")
worst = 0.0
for (c, y) in [(0.397, 0.656), (0.3, 0.5), (-0.8, 0.7), (0.6, 0.4),
               (0.1, 0.9), (-0.5, -0.656), (1.5, 0.3)]:
    n_line = line_atom_norm(c, y)
    n_w1d = w1d_one_atom(c, y)
    worst = max(worst, abs(n_line - n_w1d))
    print("  (c,y)=(%+.3f,%+.3f): line 6x6 %.12f | weighted-1D %.12f | %.2e"
          % (c, y, n_line, n_w1d, abs(n_line - n_w1d)))
print("WORST: %.2e" % worst)
assert worst < 1e-10, "the corner reduction FAILED"
print(">>> CORNER REDUCTION VERIFIED: line atom = weighted-1-D single atom")

# independent referee for the 3x3: dense corner-block SVD
def corner_dense(w, r, K=60):
    """dense referee: the corner block over (i,j,k) <= K with the tail."""
    # rows: (i,j) with i+j <= K; cols: k <= K; entries 1[i+j+k=1] - w r^{i+j+k}
    rows = [(i, j) for i in range(K + 1) for j in range(K + 1 - i)]
    M = np.zeros((len(rows), K + 1))
    for a, (i, j) in enumerate(rows):
        for k in range(K + 1):
            e = (1.0 if i + j + k == 1 else 0.0) - w * (r ** (i + j + k))
            M[a, k] = e
    # the tail columns k > K: entries -w r^{i+j+k}: fold as rank-1 tail
    # (r^{i+j}) (w r^{k}) for k > K: norm = |w| * ||(r^{i+j})|| * ||(r^k)_{k>K}||
    # exact: ||(r^{i+j})_{rows}||^2 = sum_{n<=K} (n+1) r^{2n} (truncated rows)
    # plus the rows beyond i+j > K are absent -> this referee is a lower
    # bound approximation; use large K and rely on decay.
    return float(np.linalg.svd(M, compute_uv=False)[0])

for (c, y) in [(0.397, 0.656), (-0.8, 0.7)]:
    nd = corner_dense(c, y)
    print("  referee (dense corner, K=60): %.9f vs 3x3 %.9f"
          % (nd, w1d_one_atom(c, y)))

# === the 1-D TWO-ATOM scan: does the second atom beat sqrt(lambda*)? ===
from scipy.optimize import minimize

SQ = math.sqrt(1.6310919765642504)
print("\n=== the weighted-1-D TWO-ATOM scan (sqrt(lambda*) = %.10f) ===" % SQ)


def obj2(z):
    w1, r1, w2, r2 = z
    for r in (r1, r2):
        if abs(r) >= 0.999:
            return 1e6
    try:
        v = w1d_two_atoms(w1, r1, w2, r2)
    except Exception:
        return 1e6
    return v if math.isfinite(v) else 1e6


best, bz = None, None
rng = np.random.default_rng(20260929)
starts = [np.array([0.397, 0.656, 0.0, 0.5])]
for _ in range(400):
    starts.append(np.array([rng.uniform(-2.5, 2.5), rng.uniform(-0.9, 0.9),
                            rng.uniform(-2.5, 2.5), rng.uniform(-0.9, 0.9)]))
for z0 in starts:
    r = minimize(obj2, z0, method="Nelder-Mead",
                 options={"xatol": 1e-13, "fatol": 1e-15, "maxiter": 3000})
    if best is None or r.fun < best:
        best, bz = float(r.fun), np.array(r.x)
print("1-D TWO-ATOM infimum: %.10f at (w1,r1,w2,r2) = (%.6f, %.6f, %.6f, %.6f)"
      % (best, bz[0], bz[1], bz[2], bz[3]))
print("vs sqrt(lambda*) = %.10f  |  second atom improves by %.3e"
      % (SQ, SQ - best))
print("verdict:", "SECOND ATOM HELPS" if best < SQ - 1e-8 else
      "SECOND ATOM DOES NOT HELP (the 1-atom value is the 2-atom infimum)")
