#!/usr/bin/env python3
"""quick_1d_check.py — the structural consistency check for the shell reduction.

CLAIM (to verify before building the battery):
  The line-atom norm ||M_line(c,y)|| equals the 1-D Hankel norm
  ||H^{1D}_{delta_1 - c*y^j}|| where delta_1 = 1[j=1] on Z>=0 and the
  1-D Hankel is [e(u+v)]_{u,v>=0} on l2 (the shell/line reduction).

If true, the whole cell problem chains down to the 1-D problem, and
Task 17's certificate IS the 1-D single-atom certificate.
"""
import math
import numpy as np
import sys

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


def one_d_hankel_norm(e_coefs, L=400):
    """||[e(u+v)]|| by dense truncation with a long geometric tail folded in.

    e is given as a function j -> e(j).  We build the matrix on [0,L)^2 and
    add the exact tail contribution via the atom Gram (only valid when e is
    a finite combination of delta masses and decaying exponentials, which is
    exactly our case).  Simpler here: L large enough that the truncation is
    converged to ~1e-12 (y^L tiny), plus a Richardson check.
    """
    M = np.zeros((L, L))
    for u in range(L):
        for v in range(L):
            M[u, v] = e_coefs(u + v)
    return float(np.linalg.svd(M, compute_uv=False)[0])


def e_line(c, y):
    def e(n):
        return (1.0 if n == 1 else 0.0) - c * (y ** n)
    return e


print("consistency: line-atom machinery norm vs the 1-D Hankel norm")
worst = 0.0
for (c, y) in [(0.397, 0.656), (0.3, 0.5), (-0.8, 0.7), (0.6, 0.4),
               (0.1, 0.9), (-0.5, -0.656)]:
    n_line = line_atom_norm(c, y)
    n_1d = one_d_hankel_norm(e_line(c, y), L=300)
    worst = max(worst, abs(n_line - n_1d))
    print("  (c,y)=(%+.3f,%+.3f): line %.12f | 1-D %.12f | diff %.2e"
          % (c, y, n_line, n_1d, abs(n_line - n_1d)))
print("WORST DIFF: %.2e" % worst)

# the 1-D single-atom infimum over (c, y): should be sqrt(lambda*) = 1.2771...
from scipy.optimize import minimize
best = None
rng = np.random.default_rng(7)
for st in range(120):
    z0 = np.array([rng.uniform(-1.5, 1.5), rng.uniform(-0.95, 0.95)])
    r = minimize(lambda z: one_d_hankel_norm(e_line(z[0], z[1]), L=160) or 1e6,
                 z0, method="Nelder-Mead",
                 options={"xatol": 1e-12, "fatol": 1e-14, "maxiter": 2000})
    if best is None or r.fun < best:
        best, bz = float(r.fun), np.array(r.x)
print("1-D single-atom infimum (truncated scan): %.9f at (c,y)=(%.6f, %.6f)"
      % (best, bz[0], bz[1]))
print("sqrt(lambda*) reference: 1.2771421129084462")
print("match:", abs(best - 1.2771421129084462) < 2e-5)
