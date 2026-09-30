#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_task35b.py — the two follow-up measurements the design probe
flagged:

P-B'  THE 1.3e-9 QUESTION: the P-B best point (the descent from the
      line-atom seed) re-checked on the K-chain (24, 28, 32, 36) and
      IDENTIFIED (its coordinates vs the line-atom family): does the
      power-sum compression floor sit at sqrt(lambda*) or below?

P-C'  THE TRUE TRANSVERSE CURVATURE: the SYMMETRIC stencil (the +--
      cancellation killing the gradient contamination — the probe's
      forward stencil f(2t)-2f(t)+f(0) = 2gt + kappa t^2 was measuring
      the GRADIENT, not the curvature): the 4x4 Hessian in the four
      coupling directions with the diagonal entries
      [V(+te_i)+V(-te_i)-2V(0)]/t^2 and the mixed entries the
      standard four-point mixed difference.
"""
import numpy as np
from scipy.optimize import minimize

SRC = ("/home/z/my-project/github_repos/master/scripts/"
       "probe_task35.py")
src = open(SRC).read()
head = src[:src.index('print("=" * 72)\nprint("P-A')]
ns = {'__name__': 'p35'}
exec(compile(head, 'p35head', 'exec'), ns)
x12_to_mats = ns['x12_to_mats']
compression_dense = ns['compression_dense']
line_atom_point = ns['line_atom_point']
norm12 = ns['norm12']
X_SYM, X_FREE, X_AB8 = ns['X_SYM'], ns['X_FREE'], ns["X_AB8"]
SQRT_L = ns["SQRT_L"]

rng = np.random.default_rng(35)


def compr_obj(x):
    B, C, Aa, Ab = x12_to_mats(x)
    rho = max(abs(np.linalg.eigvals(
        np.kron(Aa, Aa) + np.kron(Ab, Ab))))
    if rho >= 0.999 or not np.all(np.isfinite(x)):
        return 10.0
    v, _ = compression_dense(B, C, Aa, Ab, K=14)
    return v if np.isfinite(v) else 10.0


print("=" * 72)
print("P-B' — the 1.3e-9 question: the K-chain and the identification")
print("=" * 72)
# reproduce the P-B winner: the descent from the line-atom seed
x0 = line_atom_point(2e-3)
r = minimize(compr_obj, x0, method="Nelder-Mead",
             options={"maxiter": 600, "xatol": 1e-10,
                      "fatol": 1e-12})
xb = r.x.copy()
print("  the descent from the line-atom seed: K14 %.10f" % r.fun)
for K in (24, 28, 32, 36):
    v, n = compression_dense(*x12_to_mats(xb), K=K)
    print("    K=%d (n=%d): %.13f   [%+.3e vs sqrt(lambda*)]"
          % (K, n, v, v - SQRT_L))
print("  the winner's coordinates (B, C, diag, couplings):")
print("   ", np.array2string(xb, precision=8, max_line_width=90))
p1 = xb[0] * xb[2]
p2 = xb[1] * xb[3]
print("  the effective atoms: p1=%.6f p2=%.6f  2*p1*x1=%.8f  "
      "2*p2*x2=%.8f  y1=%.6f y2=%.6f" %
      (p1, p2, 2 * p1 * xb[4], 2 * p2 * xb[5], xb[6], xb[7]))
print("  the full 6x6 norm at the winner: %.13f  [%+.3e]"
      % (norm12(xb), norm12(xb) - SQRT_L))

print()
print("=" * 72)
print("P-C' — the true transverse curvature (the symmetric stencil)")
print("=" * 72)


def curv_true(x, t=1e-3):
    V0 = norm12(x) ** 2
    Vp = []
    Vm = []
    for d in range(4):
        xp = x.copy()
        xp[8 + d] += t
        xm = x.copy()
        xm[8 + d] -= t
        Vp.append(norm12(xp) ** 2)
        Vm.append(norm12(xm) ** 2)
    K = np.zeros((4, 4))
    for i in range(4):
        K[i, i] = (Vp[i] + Vm[i] - 2 * V0) / (t * t)
    for i in range(4):
        for j in range(i + 1, 4):
            xpp = x.copy()
            xpp[8 + i] += t
            xpp[8 + j] += t
            xpm = x.copy()
            xpm[8 + i] += t
            xpm[8 + j] -= t
            xmp = x.copy()
            xmp[8 + i] -= t
            xmp[8 + j] += t
            xmm = x.copy()
            xmm[8 + i] -= t
            xmm[8 + j] -= t
            K[i, j] = K[j, i] = (
                norm12(xpp) ** 2 - norm12(xpm) ** 2
                - norm12(xmp) ** 2 + norm12(xmm) ** 2) / (4 * t * t)
    return K


def rand_diag_point():
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
       ("the line atom x=2e-3", line_atom_point(2e-3)),
       ("the line atom x=1e-2", line_atom_point(1e-2))]
for i in range(6):
    pts.append(("rand diag #%d" % i, rand_diag_point()))
allmin = []
for tag, x in pts:
    K = curv_true(x)
    ev = np.linalg.eigvalsh(K)
    allmin.append(ev[0])
    print("  %-22s V=%.9f  kappa: %s" %
          (tag, norm12(x),
           " ".join("%+.2e" % e for e in ev)))
print("  the gauge-flat directions appear as the ~0 eigenvalues;")
print("  the MODULI transverse curvature: the nonzero spectrum.")
print("  min eigenvalue over the grid: %+.3e" % min(allmin))
pos = sum(1 for e in allmin if e > 0)
print("  (%d/%d points with fully positive spectrum)" % (pos,
                                                         len(allmin)))
