#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_debug.py — localize the theory-vs-machinery discrepancy at the
symmetric shadow: (1) the Gram G's conditioning; (2) the eigen-frame
quality; (3) the incremental theory (mu^1, core, rep separately) vs the
direct eigenvalue along e_4 and the mixed direction; (4) the FD pieces'
step-stability."""
import numpy as np
from scipy.linalg import eigh

exec(open("/home/z/my-project/github_repos/master/scripts/"
          "probe_shadow2.py").read().split("VOL_IX = ")[0])

X_SYM = np.load("/home/z/my-project/github_repos/master/scripts/"
                "shadow_refined.npy")
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

print("(1) the Gram G's conditioning at the symmetric shadow:")
gev = np.linalg.eigvalsh(G)
print("    eig(G) = %s  (cond %.2e)" %
      (["%.4f" % v for v in gev], gev[-1] / max(gev[0], 1e-300)))
print("(2) the frame: V'GV-I = %.2e; residuals %.2e; V'M0V =\n%s"
      % (np.max(np.abs(Vtop.T @ G @ Vtop - np.eye(2))),
         max(np.linalg.norm(K @ Vtop[:, a] - w[-2 + a] * (G @ Vtop[:, a]))
             for a in range(2)), Vtop.T @ (K - lam0 * G) @ Vtop))
print("    the spectrum: %s" % ["%.6f" % v for v in w])


def M_of(xv):
    Aa = np.array([[xv[4], xv[8]], [xv[9], xv[5]]])
    Ab = np.array([[xv[6], xv[10]], [xv[11], xv[7]]])
    Gx, Cmx, _ = build_GC(xv[0:2], xv[2:4], Aa, Ab)
    Kx = Gx @ Cmx @ Gx
    Kx = 0.5 * (Kx + Kx.T)
    return Kx - lam0 * Gx


def lam_top(x):
    Aa = np.array([[x[4], x[8]], [x[9], x[5]]])
    Ab = np.array([[x[6], x[10]], [x[11], x[7]]])
    Gx, Cmx, _ = build_GC(x[0:2], x[2:4], Aa, Ab)
    Kx = Gx @ Cmx @ Gx
    Kx = 0.5 * (Kx + Kx.T)
    ww, _ = eigh(Kx, Gx)
    return float(ww[-1])


M0 = K - lam0 * G
D = np.diag(w_m - lam0)
Dinv = np.diag(1.0 / (lam0 - w_m))
RID = [4, 5, 8, 9]

print("(3) the incremental theory vs the direct, along e_4:")
j = 4
ej = np.zeros(12)
ej[j] = 1.0
for T1 in (1e-5, 1e-4):
    M1j = (M_of(x_star + T1 * ej) - M_of(x_star - T1 * ej)) / (2 * T1)
    W1j = Vtop.T @ M1j @ Vtop
    Uj = Vtop.T @ M1j @ Vm
    repj = Uj @ Dinv @ Uj.T
    print("    T1=%.0e: mu^1 = %+.3e (2x2 eig %s), |U| = %.4f, "
          "rep = %s" % (T1, float(np.linalg.eigvalsh(W1j)[-1]),
                        ["%+.2e" % v for v in
                         np.linalg.eigvalsh(W1j)],
                        np.linalg.norm(Uj),
                        ["%+.4f" % v for v in
                         np.linalg.eigvalsh(repj)]))
for T2 in (1e-3, 3e-4, 1e-4, 3e-5):
    M2j = (M_of(x_star + T2 * ej) - 2 * M0 +
           M_of(x_star - T2 * ej)) / (T2 * T2)
    corej = 0.5 * Vtop.T @ M2j @ Vtop
    print("    T2=%.0e: core = %s (|M2| = %.3f)" %
          (T2, ["%+.4f" % v for v in np.linalg.eigvalsh(corej)],
           np.linalg.norm(M2j)))

# the assembled theory vs the direct at several t
M1j = (M_of(x_star + 1e-5 * ej) - M_of(x_star - 1e-5 * ej)) / 2e-5
M2j = (M_of(x_star + 3e-4 * ej) - 2 * M0 +
       M_of(x_star - 3e-4 * ej)) / 9e-8
W1j = Vtop.T @ M1j @ Vtop
Uj = Vtop.T @ M1j @ Vm
corej = 0.5 * Vtop.T @ M2j @ Vtop
repj = Uj @ Dinv @ Uj.T
print("    t       direct-mu      theory(full)    theory(core)   "
      "theory(rep)")
for t in (1e-4, 3e-4, 1e-3, 3e-3):
    xs = x_star + t * ej
    dm = lam_top(xs) - lam0
    tf = float(np.linalg.eigvalsh(t * W1j + t * t * (corej + repj))[-1])
    tc = float(np.linalg.eigvalsh(t * W1j + t * t * corej)[-1])
    tr = float(np.linalg.eigvalsh(t * t * repj)[-1])
    print("    %.0e  %+.6e  %+.6e  %+.6e  %+.6e" % (t, dm, tf, tc, tr))

print("(4) the mixed direction (the T-cross check):")
u_mix = np.array([0.4781, 0.5199, 0.5170, 0.4836])
e_mix = np.zeros(12)
e_mix[RID] = u_mix
T1, T2 = 1e-5, 3e-4
M1m = (M_of(x_star + T1 * e_mix) - M_of(x_star - T1 * e_mix)) / (2 * T1)
M2m = (M_of(x_star + T2 * e_mix) - 2 * M0 +
       M_of(x_star - T2 * e_mix)) / (T2 * T2)
W1m = Vtop.T @ M1m @ Vtop
Um = Vtop.T @ M1m @ Vm
corem = 0.5 * Vtop.T @ M2m @ Vtop
repm = Um @ Dinv @ Um.T
print("    mu^1(mix) = %+.3e; core = %s; rep = %s" %
      (float(np.linalg.eigvalsh(W1m)[-1]),
       ["%+.3f" % v for v in np.linalg.eigvalsh(corem)],
       ["%+.3f" % v for v in np.linalg.eigvalsh(repm)]))
print("    t       direct-mu      theory(full)")
for t in (1e-4, 3e-4, 1e-3, 3e-3):
    xs = x_star + t * e_mix
    dm = lam_top(xs) - lam0
    tf = float(np.linalg.eigvalsh(t * W1m + t * t * (corem + repm))[-1])
    print("    %.0e  %+.6e  %+.6e" % (t, dm, tf))

# (5) the KEY structural check: is the top eigenspace at x*+t*ej still
# double?  the branch structure along the ray
print("(5) the branch structure along e_4 (the top two at each t):")
for t in (1e-3, 1e-2):
    Aa = np.diag([x_star[4] + t, x_star[5]])
    Ab = np.diag([x_star[6], x_star[7]])
    Gx, Cmx, _ = build_GC(x_star[0:2], x_star[2:4], Aa, Ab)
    Kx = Gx @ Cmx @ Gx
    Kx = 0.5 * (Kx + Kx.T)
    ww, _ = eigh(Kx, Gx)
    print("    t=%.0e: the top three: %s" %
          (t, ["%.9f" % v for v in ww[-3:]]))
