#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_shadow2.py — refine the abelian optimum: (a) the symmetric
subfamily probe (Aa = diag(alpha,-alpha), Ab = diag(beta,beta) — the
structure the multi-start exhibited); (b) heavier multi-start on the full
8-dim; (c) the flat-ridge (Aa block) W1 residuals at the best point."""
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize
import importlib.util

spec = importlib.util.spec_from_file_location(
    "ps1", "/home/z/my-project/github_repos/master/scripts/probe_shadow.py")
# reuse only the machinery: re-declare to avoid re-running the probe

rng = np.random.default_rng(11)

BLOCKS = [((0, 0), [""]), ((1, 0), ["a"]), ((0, 1), ["b"]),
          ((1, 1), ["ab", "ba"])]
MU = {(0, 0): 1.0, (1, 0): 1.0, (0, 1): 1.0, (1, 1): 2.0}


def kron4(Aa, Ab):
    return np.kron(Aa, Aa) + np.kron(Ab, Ab)


def lyap(Aa, Ab, X):
    K = kron4(Aa, Ab)
    rho = max(abs(np.linalg.eigvals(K)))
    if np.max(np.abs(X)) < 1e-15:
        return np.zeros((2, 2)), rho
    if rho >= 1.0 - 1e-12:
        return None, rho
    v = np.linalg.solve(np.eye(4) - K, X.reshape(4, order="F"))
    return v.reshape(2, 2, order="F"), rho


def lyap_T(Aa, Ab, X):
    K = np.kron(Aa.T, Aa.T) + np.kron(Ab.T, Ab.T)
    rho = max(abs(np.linalg.eigvals(K)))
    if np.max(np.abs(X)) < 1e-15:
        return np.zeros((2, 2)), rho
    if rho >= 1.0 - 1e-12:
        return None, rho
    v = np.linalg.solve(np.eye(4) - K, X.reshape(4, order="F"))
    return v.reshape(2, 2, order="F"), rho


def word_matrix(Aa, Ab, w):
    M = np.eye(2)
    for ch in w:
        M = M @ (Aa if ch == "a" else Ab)
    return M


def build_GC(B, C, Aa, Ab):
    Lc, rho = lyap(Aa, Ab, np.outer(C, C))
    if Lc is None:
        return None, None, rho
    Lr, _ = lyap_T(Aa, Ab, np.outer(B, B))
    if Lr is None:
        return None, None, rho
    FBu, FBv = {}, {}
    for (beta, words) in BLOCKS:
        Su = np.zeros(2)
        Sv = np.zeros(2)
        for w in words:
            Mw = word_matrix(Aa, Ab, w)
            Su = Su + B @ Mw
            Sv = Sv + Mw @ C
        FBu[beta] = Su
        FBv[beta] = Sv
    G = np.zeros((6, 6))
    Cmat = np.zeros((6, 6))
    betas = [b for (b, _) in BLOCKS]
    for i, b in enumerate(betas):
        G[i, i] = MU[b]
        Cmat[i, i] = MU[(1 - b[0], 1 - b[1])]
        for k in range(2):
            G[i, 4 + k] = FBu[b][k]
            G[4 + k, i] = FBu[b][k]
            Cmat[i, 4 + k] = -FBv[(1 - b[0], 1 - b[1])][k]
            Cmat[4 + k, i] = -FBv[(1 - b[0], 1 - b[1])][k]
    G[4:6, 4:6] = Lr
    Cmat[4:6, 4:6] = Lc
    return G, Cmat, rho


def norm_of(B, C, Aa, Ab):
    G, Cmat, rho = build_GC(B, C, Aa, Ab)
    if G is None:
        return 1e6
    A = Cmat @ G
    ev = np.linalg.eigvals(A)
    return np.sqrt(max(max(float(np.real(e)) for e in ev), 0.0))


VOL_IX = 1.277142689665
X0 = np.load("/home/z/my-project/github_repos/master/scripts/shadow_best.npy")
print("probe-1 best: %.15f (gap %.2e)" %
      (norm_of(X0[0:2], X0[2:4], np.diag(X0[4:6]), np.diag(X0[6:8])),
       norm_of(X0[0:2], X0[2:4], np.diag(X0[4:6]), np.diag(X0[6:8])) - VOL_IX))

# (a) the symmetric subfamily: (b1, b2, c1, c2, alpha, beta)
def obj_sym(z):
    Aa = np.diag([z[4], -z[4]])
    Ab = np.diag([z[5], z[5]])
    return norm_of(z[0:2], z[2:4], Aa, Ab)


z0 = np.array([X0[0], X0[1], X0[2], X0[3],
               0.5 * (X0[4] - X0[5]), 0.5 * (X0[6] + X0[7])])
best_sym = obj_sym(z0)
z_best = z0.copy()
for i in range(8):
    zz = z0 if i == 0 else z0 + rng.normal(size=6) * 0.1
    r = minimize(obj_sym, zz, method="Nelder-Mead",
                 options={"maxiter": 2500, "xatol": 1e-14, "fatol": 1e-16})
    if r.fun < best_sym:
        best_sym, z_best = float(r.fun), r.x.copy()
print("the symmetric subfamily optimum: %.15f (gap to Vol IX %.2e)"
      % (best_sym, best_sym - VOL_IX), flush=True)
print("  (b1,b2,c1,c2,alpha,beta) = %s" % ["%.9f" % v for v in z_best])

# (b) heavier multi-start on the full 8-dim from the symmetric optimum
x_best = np.array([z_best[0], z_best[1], z_best[2], z_best[3],
                   z_best[4], -z_best[4], z_best[5], z_best[5]])
v_best = norm_of(x_best[0:2], x_best[2:4], np.diag(x_best[4:6]),
                 np.diag(x_best[6:8]))


def obj8(x8):
    return norm_of(x8[0:2], x8[2:4], np.diag(x8[4:6]), np.diag(x8[6:8]))


for i in range(12):
    x0 = x_best + rng.normal(size=8) * (0.01 if i < 6 else 0.05)
    r = minimize(obj8, x0, method="Nelder-Mead",
                 options={"maxiter": 2500, "xatol": 1e-14, "fatol": 1e-16})
    if r.fun < v_best:
        v_best, x_best = float(r.fun), r.x.copy()
for _ in range(2):
    r = minimize(obj8, x_best, method="Nelder-Mead",
                 options={"maxiter": 6000, "xatol": 1e-14, "fatol": 1e-16})
    if r.fun < v_best:
        v_best, x_best = float(r.fun), r.x.copy()
print("the full 8-dim refined: %.15f (gap %.2e)" % (v_best, v_best - VOL_IX),
      flush=True)
print("  coords: %s" % ["%.10f" % c for c in x_best])
np.save("/home/z/my-project/github_repos/master/scripts/shadow_refined.npy",
        x_best)

# (c) the flat-ridge residuals at the refined optimum
x12 = np.concatenate([x_best, np.zeros(4)])
G, Cm, rho = build_GC(x_best[0:2], x_best[2:4], np.diag(x_best[4:6]),
                      np.diag(x_best[6:8]))
K = G @ Cm @ G
K = 0.5 * (K + K.T)
w, V = eigh(K, G)
lam0 = float(w[-1])
Vtop = V[:, -2:]
print("the double: %.2e; lambda0 = %.12f; the V support:" %
      (w[-1] - w[-2], lam0), flush=True)
print(Vtop, flush=True)


def M_of(xv):
    Aa = np.array([[xv[4], xv[8]], [xv[9], xv[5]]])
    Ab = np.array([[xv[6], xv[10]], [xv[11], xv[7]]])
    Gx, Cmx, _ = build_GC(xv[0:2], xv[2:4], Aa, Ab)
    Kx = Gx @ Cmx @ Gx
    Kx = 0.5 * (Kx + Kx.T)
    return Kx - lam0 * Gx


t1 = 1e-5
print("the flat-ridge (Aa block, coords 4,5,8,9) W1 residuals:")
for j in (4, 5, 8, 9):
    d = np.zeros(12)
    d[j] = 1.0
    W1j = Vtop.T @ (M_of(x12 + t1 * d) - M_of(x12 - t1 * d)) / (2 * t1) \
        @ Vtop
    print("  j=%d: |W1| = %.2e" % (j, np.max(np.abs(W1j))))

# the escape re-descended from the refined shadow


def norm12(x):
    Aa = np.array([[x[4], x[8]], [x[9], x[5]]])
    Ab = np.array([[x[6], x[10]], [x[11], x[7]]])
    return norm_of(x[0:2], x[2:4], Aa, Ab)


xx = x12.copy()
bv = norm12(xx)
for _ in range(4):
    r = minimize(norm12, xx, method="Nelder-Mead",
                 options={"maxiter": 8000, "xatol": 1e-12, "fatol": 1e-14})
    if r.fun < bv:
        bv, xx = float(r.fun), r.x.copy()
print("the escape from the refined shadow: %.15f (delta %.4e)" %
      (bv, v_best - bv))
print("  the move: %s" % ["%.6f" % c for c in (xx - x12)])
np.save("/home/z/my-project/github_repos/master/scripts/escape_refined.npy",
        xx)
