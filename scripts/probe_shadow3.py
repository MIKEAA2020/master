#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_shadow3.py — the full fact sheet for the corrected escape story:
(1) Task 29's free point — the coupling attribution (zero the couplings);
(2) the dense L=10 cross-check orderings; (3) harder abelian multi-start;
(4) free-class multi-start; (5) H2 (the L operator) on the flat ridge at
the SYMMETRIC shadow — the infinitesimal escape verdict; (6) the t^2
scaling along the flattest/most-negative ridge directions."""
import math
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize

rng = np.random.default_rng(23)

exec(open("/home/z/my-project/github_repos/master/scripts/"
          "probe_shadow2.py").read().split("VOL_IX = ")[0])

VOL_IX = 1.277142689665
TASK29_FREE = 1.2771421170091146
X_AB8 = np.array([2.77175129, -2.771744134, 1.0, 1.0,
                 0.07152188, -0.071722572, 0.656323579, 0.656321527])
X_SYM = np.load("/home/z/my-project/github_repos/master/scripts/"
                "shadow_refined.npy")


def norm12(x):
    Aa = np.array([[x[4], x[8]], [x[9], x[5]]])
    Ab = np.array([[x[6], x[10]], [x[11], x[7]]])
    return norm_of(x[0:2], x[2:4], Aa, Ab)


# re-derive Task 29's free point (the deterministic descent from the
# rounded abelian lift — the reproduction gate)
X_FREE = np.concatenate([X_AB8, np.zeros(4)])
for _ in range(3):
    r = minimize(norm12, X_FREE, method="Nelder-Mead",
                 options={"maxiter": 8000, "xatol": 1e-12, "fatol": 1e-14})
    if r.fun < norm12(X_FREE):
        X_FREE = r.x.copy()
print("the free point re-derived: %.15f (gate %.2e)" %
      (norm12(X_FREE), abs(norm12(X_FREE) - TASK29_FREE)), flush=True)


print("=" * 70)
print("(1) the coupling attribution of Task 29's free point")
v_free = norm12(X_FREE)
x_noc = X_FREE.copy()
x_noc[8:12] = 0.0
v_noc = norm12(x_noc)
print("  the free point: %.15f; couplings zeroed: %.15f "
      "(the couplings buy %.3e)" % (v_free, v_noc, v_noc - v_free))
print("  the symmetric abelian: %.15f; the free point is lower by %.3e"
      % (norm12(np.concatenate([X_SYM, np.zeros(4)])),
         norm12(np.concatenate([X_SYM, np.zeros(4)])) - v_free))

print("=" * 70)
print("(2) the dense L=10 cross-check (the orderings)")


def words_up_to(K):
    out = []
    for l in range(K + 1):
        for i in range(2 ** l):
            out.append("".join("a" if (i >> (l - 1 - j)) & 1 == 0
                               else "b" for j in range(l)))
    return out


def dense_sv(x, K=10):
    Aa = np.array([[x[4], x[8]], [x[9], x[5]]])
    Ab = np.array([[x[6], x[10]], [x[11], x[7]]])
    B, C = x[0:2], x[2:4]
    W = words_up_to(K)
    n = len(W)
    E = np.zeros((n, n))
    for i, u in enumerate(W):
        for j, v in enumerate(W):
            uv = u + v
            E[i, j] = (1.0 if (uv.count("a"), uv.count("b")) == (1, 1)
                       else 0.0) - float(B @ word_matrix(Aa, Ab, uv) @ C)
    return float(np.linalg.svd(E, compute_uv=False)[0])


d_free = dense_sv(X_FREE)
d_sym = dense_sv(np.concatenate([X_SYM, np.zeros(4)]))
d_ix = dense_sv(np.concatenate([X_AB8, np.zeros(4)]))
print("  dense L=10: free %.9f | symmetric %.9f | Vol IX point %.9f"
      % (d_free, d_sym, d_ix))
print("  the dense ordering: free below symmetric by %.2e (the exact "
      "machinery says %.2e)" % (d_sym - d_free,
                                norm12(np.concatenate([X_SYM,
                                                       np.zeros(4)])) - v_free))

print("=" * 70)
print("(3) harder abelian multi-start")


def obj8(x8):
    return norm_of(x8[0:2], x8[2:4], np.diag(x8[4:6]), np.diag(x8[6:8]))


best_ab, x_best = obj8(X_SYM), X_SYM.copy()
seeds = [X_SYM, X_FREE[:8], np.array([2.77175129, -2.771744134, 1.0, 1.0,
                                      0.07152188, -0.071722572,
                                      0.656323579, 0.656321527])]
for i in range(18):
    seeds.append(X_SYM + rng.normal(size=8) * (0.03 if i < 9 else 0.15))
for i in range(8):
    seeds.append(X_FREE[:8] + rng.normal(size=8) * 0.03)
for s in seeds:
    r = minimize(obj8, s, method="Nelder-Mead",
                 options={"maxiter": 2500, "xatol": 1e-14, "fatol": 1e-16})
    if r.fun < best_ab - 1e-15:
        best_ab, x_best = float(r.fun), r.x.copy()
print("  the abelian best over %d starts: %.15f (vs the free %.15f; "
      "gap %.3e)" % (len(seeds), best_ab, v_free, best_ab - v_free))
print("  coords: %s" % ["%.9f" % c for c in x_best])

print("=" * 70)
print("(4) free-class multi-start (12 starts)")
best_fr, xf_best = v_free, X_FREE.copy()
for i in range(12):
    x0 = np.concatenate([X_SYM + rng.normal(size=8) * 0.05,
                         rng.normal(size=4) * 0.05])
    r = minimize(norm12, x0, method="Nelder-Mead",
                 options={"maxiter": 2500, "xatol": 1e-12, "fatol": 1e-14})
    if r.fun < best_fr:
        best_fr, xf_best = float(r.fun), r.x.copy()
r = minimize(norm12, xf_best, method="Nelder-Mead",
             options={"maxiter": 6000, "xatol": 1e-12, "fatol": 1e-14})
if r.fun < best_fr:
    best_fr, xf_best = float(r.fun), r.x.copy()
print("  the free best: %.15f (couplings %s)" %
      (best_fr, ["%.5f" % c for c in xf_best[8:12]]))
print("  the abelian-vs-free scan gap: %.3e" % (best_ab - best_fr))

print("=" * 70)
print("(5) H2 on the flat ridge at the SYMMETRIC shadow")
x_star = np.concatenate([X_SYM, np.zeros(4)])
G, Cm, rho = build_GC(x_star[0:2], x_star[2:4],
                      np.diag(x_star[4:6]), np.diag(x_star[6:8]))
K = G @ Cm @ G
K = 0.5 * (K + K.T)
w, V = eigh(K, G)
lam0 = float(w[-1])
Vtop = V[:, -2:]
Vm = V[:, :-2]
w_m = w[:-2]
print("  the double %.2e; the isolation %.4f" % (w[-1] - w[-2],
                                                 w[-2] - w[-3]))


def M_of(xv):
    Aa = np.array([[xv[4], xv[8]], [xv[9], xv[5]]])
    Ab = np.array([[xv[6], xv[10]], [xv[11], xv[7]]])
    Gx, Cmx, _ = build_GC(xv[0:2], xv[2:4], Aa, Ab)
    Kx = Gx @ Cmx @ Gx
    Kx = 0.5 * (Kx + Kx.T)
    return Kx - lam0 * Gx


M0 = K - lam0 * G
T1, T2 = 1e-5, 3e-4
M1e = []
for j in range(12):
    d = np.zeros(12)
    d[j] = 1.0
    M1e.append((M_of(x_star + T1 * d) - M_of(x_star - T1 * d)) / (2 * T1))
W1 = [Vtop.T @ Mj @ Vtop for Mj in M1e]
print("  the flat-ridge W1 residuals: %s" %
      ["%.1e" % np.max(np.abs(W1[j])) for j in (4, 5, 8, 9)])
print("  the cone coordinates' mu_max: %s" %
      ["%+.3f" % np.linalg.eigvalsh(W1[j])[-1] for j in
       (0, 1, 2, 3, 6, 7, 10, 11)])

Uj = [Vtop.T @ Mj @ Vm for Mj in M1e]
Dinv = np.diag(1.0 / (lam0 - w_m))


def d2M(j, k, t=T2):
    ej = np.zeros(12)
    ej[j] = 1.0
    ek = np.zeros(12)
    ek[k] = 1.0
    if j == k:
        return (M_of(x_star + t * ej) - 2 * M0 +
                M_of(x_star - t * ej)) / (t * t)
    return (M_of(x_star + t * (ej + ek)) - M_of(x_star + t * (ej - ek)) -
            M_of(x_star - t * (ej - ek)) + M_of(x_star - t * (ej + ek))) \
        / (4 * t * t)


def T_jk(j, k):
    return 0.5 * (Vtop.T @ d2M(j, k) @ Vtop) + Uj[j] @ Dinv @ Uj[k].T


RID = [4, 5, 8, 9]
Tr = {}
for a in range(4):
    for b in range(a, 4):
        Tr[(a, b)] = T_jk(RID[a], RID[b])


def L_ridge(u4):
    S = np.zeros((2, 2))
    for a in range(4):
        for b in range(4):
            if u4[a] != 0.0 and u4[b] != 0.0:
                S = S + u4[a] * u4[b] * Tr[(min(a, b), max(a, b))]
    return S


def c_ridge(u4):
    return float(np.linalg.eigvalsh(L_ridge(u4))[-1])


# the pure curvatures and the sphere minimum on the ridge
print("  the ridge pure curvatures (coords 4,5,8,9): %s" %
      ["%.4f" % c_ridge(np.eye(4)[i]) for i in range(4)])
best = (1e9, None)
for _ in range(3000):
    u = rng.normal(size=4)
    u /= np.linalg.norm(u)
    cv = c_ridge(u)
    if cv < best[0]:
        best = (cv, u)
u_min = best[1]
r = minimize(lambda z: c_ridge(np.asarray(z) / np.linalg.norm(z)),
             u_min, method="Nelder-Mead",
             options={"maxiter": 2000, "xatol": 1e-12, "fatol": 1e-14})
if r.fun < best[0]:
    u_min = r.x / np.linalg.norm(r.x)
    best = (float(r.fun), u_min)
print("  THE RIDGE CURVATURE MINIMUM kappa_ridge = %.6e" % best[0])
print("  the direction: %s" % ["%.4f" % v for v in u_min])

print("=" * 70)
print("(6) the t-scaling: the theory vs the direct machinery")


def lam_top(x):
    Aa = np.array([[x[4], x[8]], [x[9], x[5]]])
    Ab = np.array([[x[6], x[10]], [x[11], x[7]]])
    Gx, Cmx, _ = build_GC(x[0:2], x[2:4], Aa, Ab)
    Kx = Gx @ Cmx @ Gx
    Kx = 0.5 * (Kx + Kx.T)
    ww, _ = eigh(Kx, Gx)
    return float(ww[-1])


# (a) the pure directions first (the theory: +14.11, +12.13)
for name, u in [("e_4 (Aa diag)", np.array([1, 0, 0, 0.])),
                ("e_9 (Aa coupling)", np.array([0, 0, 0, 1.]))]:
    for t in (1e-3, 3e-3, 1e-2):
        xs = x_star.copy()
        xs[RID] = x_star[RID] + t * u
        print("    %-18s t=%.4f: dlam = %+.6e (theory t^2*c = %+.6e)"
              % (name, t, lam_top(xs) - lam0,
                 t ** 2 * c_ridge(u)))

# (b) the mixed direction u_min (the theory: -228.7)
for t in (3e-4, 1e-3, 3e-3, 1e-2, 3e-2):
    xs = x_star.copy()
    xs[RID] = x_star[RID] + t * u_min
    print("    u_min             t=%.4f: dlam = %+.6e (theory %+.6e)"
          % (t, lam_top(xs) - lam0, t ** 2 * best[0]))

# (c) the T step validation at the symmetric point
drift = 0.0
for a in range(4):
    for t_alt in (1e-3, 1e-4):
        j = RID[a]
        ej = np.zeros(12)
        ej[j] = 1.0
        alt = 0.5 * (Vtop.T @ ((M_of(x_star + t_alt * ej) - 2 * M0 -
                                M_of(x_star - t_alt * ej)) /
                               (t_alt * t_alt)) @ Vtop) + \
            Uj[j] @ Dinv @ Uj[j].T
        ref = Tr[(a, a)]
        drift = max(drift, float(np.linalg.norm(alt - ref) /
                                 np.linalg.norm(ref)))
print("    the T step-validation drift at the symmetric point: %.2e"
      % drift)
print("    the L_ridge(u_min) matrix:\n%s" % L_ridge(u_min))
print("    the ridge T entries (lambda_max):")
for a in range(4):
    print("      %s" % ["%+9.3f" % float(np.linalg.eigvalsh(
          Tr[(min(a, b), max(a, b))])[-1]) for b in range(4)])
