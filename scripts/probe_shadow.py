#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_shadow.py — find the TRUE abelian optimizer (the NM polish stuck
at 1.2771486; Vol IX's optimum is 1.277142689665). Multi-start NM / Powell
/ BFGS on the 8-dim abelian objective; then the first-order cone (W1)
diagnostics at the best point: the LMI flat cone {d: W1(d) <= 0} and
whether the escape direction rides its boundary."""
import math
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize

rng = np.random.default_rng(7)

# ---- the machinery (verbatim from offclass_ncaak.py) ----
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
    return math.sqrt(max(max(float(np.real(e)) for e in ev), 0.0))


X_AB = np.array([2.77175129, -2.771744134, 1.0, 1.0,
                 0.07152188, -0.071722572,
                 0.656323579, 0.656321527])
VOL_IX = 1.277142689665


def obj8(x8):
    return norm_of(x8[0:2], x8[2:4], np.diag(x8[4:6]), np.diag(x8[6:8]))


print("start value: %.15f (Vol IX %.15f, gap %.2e)" %
      (obj8(X_AB), VOL_IX, obj8(X_AB) - VOL_IX))

best_x, best_v = X_AB.copy(), obj8(X_AB)

# 1) Powell from the rounded point
for meth in ("Powell", "Nelder-Mead", "BFGS"):
    try:
        r = minimize(obj8, X_AB, method=meth,
                     options={"maxiter": 20000, "xtol": 1e-14,
                              "ftol": 1e-16} if meth == "Powell" else
                     ({"maxiter": 20000, "xatol": 1e-13, "fatol": 1e-15}
                      if meth == "Nelder-Mead" else {"maxiter": 5000}))
        v = obj8(r.x)
        print("  %-12s -> %.15f (gap to Vol IX %.2e)" %
              (meth, v, v - VOL_IX))
        if v < best_v:
            best_v, best_x = v, r.x.copy()
    except Exception as e:
        print("  %-12s ERR %s" % (meth, e))

# 2) multi-start NM in the neighborhood
for i in range(30):
    x0 = X_AB + rng.normal(size=8) * (0.02 if i < 15 else 0.08)
    r = minimize(obj8, x0, method="Nelder-Mead",
                 options={"maxiter": 6000, "xatol": 1e-13, "fatol": 1e-15})
    v = obj8(r.x)
    if v < best_v - 1e-13:
        best_v, best_x = v, r.x.copy()
print("multi-start best: %.15f (gap to Vol IX %.2e)" %
      (best_v, best_v - VOL_IX))
print("  coords: %s" % ["%.9f" % c for c in best_x])

# 3) the descent from the best abelian point (the escape re-based)
x12 = np.concatenate([best_x, np.zeros(4)])


def norm12(x):
    Aa = np.array([[x[4], x[8]], [x[9], x[5]]])
    Ab = np.array([[x[6], x[10]], [x[11], x[7]]])
    return norm_of(x[0:2], x[2:4], Aa, Ab)


xx = x12.copy()
bv = norm12(xx)
for _ in range(3):
    r = minimize(norm12, xx, method="Nelder-Mead",
                 options={"maxiter": 8000, "xatol": 1e-12, "fatol": 1e-14})
    if r.fun < bv:
        bv, xx = float(r.fun), r.x.copy()
print("the escape from the best abelian point: %.15f (delta %.3e)" %
      (bv, best_v - bv))
print("  couplings: %s" % ["%.6f" % c for c in xx[8:12]])

# 4) the W1 cone diagnostics at the best abelian point
G, Cm, rho = build_GC(best_x[0:2], best_x[2:4],
                      np.diag(best_x[4:6]), np.diag(best_x[6:8]))
K = G @ Cm @ G
K = 0.5 * (K + K.T)
w, V = eigh(K, G)
lam0 = float(w[-1])
Vtop = V[:, -2:]
print("the double at the best point: %.2e (lambda0 %.12f)" %
      (w[-1] - w[-2], lam0))


def M_of(x12v):
    B, C = x12v[0:2], x12v[2:4]
    Aa = np.array([[x12v[4], x12v[8]], [x12v[9], x12v[5]]])
    Ab = np.array([[x12v[6], x12v[10]], [x12v[11], x12v[7]]])
    Gx, Cmx, _ = build_GC(B, C, Aa, Ab)
    Kx = Gx @ Cmx @ Gx
    Kx = 0.5 * (Kx + Kx.T)
    return Kx - lam0 * Gx


M0 = K - lam0 * G
W1 = []
t1 = 1e-5
for j in range(12):
    d = np.zeros(12)
    d[j] = 1.0
    W1.append(Vtop.T @ (M_of(x12 + t1 * d) - M_of(x12 - t1 * d))
              / (2 * t1) @ Vtop)
W1 = np.array(W1)
print("W1 per coordinate (2x2 eigenvalues, and mu_max):")
for j in range(12):
    ev = np.linalg.eigvalsh(W1[j])
    print("  j=%2d: mu = (%+.4f, %+.4f)  mu_max %+.4f" %
          (j, ev[0], ev[1], ev[1]))

# the LMI flat cone: is there d with W1(d) <= 0? sample + optimize
def mu_max_dir(d):
    return float(np.linalg.eigvalsh(sum(d[j] * W1[j] for j in range(12)))[-1])


best = (1e9, None)
for _ in range(4000):
    d = rng.normal(size=12)
    d /= np.linalg.norm(d)
    m = mu_max_dir(d)
    if m < best[0]:
        best = (m, d)
d0 = best[1]
r = minimize(lambda z: mu_max_dir(np.asarray(z) /
                                   np.linalg.norm(z)), d0,
             method="Nelder-Mead",
             options={"maxiter": 3000, "xatol": 1e-12, "fatol": 1e-14})
d_flat = r.x / np.linalg.norm(r.x)
print("the cone's flattest direction: mu_max(W1(d)) = %.3e" %
      mu_max_dir(d_flat))
d_esc = xx - x12
d_esc = d_esc / np.linalg.norm(d_esc)
print("the escape direction's first-order: mu_max(W1(d_esc)) = %.3e "
      "(|d| = %.4f)" % (mu_max_dir(d_esc), np.linalg.norm(xx - x12)))
print("  the flat direction: %s" % ["%.3f" % v for v in d_flat])
print("  the escape direction: %s" % ["%.3f" % v for v in d_esc])
print("  cosine(flat, escape) = %.4f" %
      abs(float(np.dot(d_flat, d_esc))))
np.save("/home/z/my-project/github_repos/master/scripts/"
        "shadow_best.npy", best_x)
