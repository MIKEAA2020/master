#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""quick_amalgam_check.py — verify the analytical discovery BEFORE building Vol IX.

CLAIM: for the two-golden amalgam (phi = 1 at (0,0),(1,0),(0,1)), the atom
psi*(gamma) = 2^{-|gamma|} (lambda = (1/2,1/2), p = 1) attains
    ||K_phi - K_psi*|| = sigma_2 = 1 EXACTLY,
with error spectrum (1, -1, -1). If true, Vol VIII's D(1) = 1.0369 strict-failure
was an artifact of the tail-penalized surrogate objective.
"""
import math
import numpy as np

# ---- the amalgam K on the full grid (|beta| <= Gb) -------------------------
Gb = 14
def grid_of(n, K):
    g = []
    def rec(i, rem, cur):
        if i == n:
            g.append(tuple(cur)); return
        for j in range(rem + 1):
            rec(i + 1, rem - j, cur + [j])
    rec(0, K, [])
    return sorted(g, key=lambda a: (sum(a), a))

def mu_of(alpha):
    k = sum(alpha)
    r = math.factorial(k)
    for a in alpha:
        r //= math.factorial(a)
    return r

G = grid_of(2, Gb)
gidx = {a: i for i, a in enumerate(G)}
MU = {a: mu_of(a) for a in G}

def K_of(phi, grid, gidx, mu):
    M = np.zeros((len(grid), len(grid)))
    for b in grid:
        for a in grid:
            M[gidx[b], gidx[a]] = phi.get(tuple(x + y for x, y in zip(b, a)), 0.0)
    d = np.array([mu[a] ** 0.5 for a in grid])
    return d[:, None] * M * d[None, :]

phi_amalgam = {(0, 0): 1.0, (1, 0): 1.0, (0, 1): 1.0}
K2 = K_of(phi_amalgam, G, gidx, MU)
s2 = np.linalg.svd(K2, compute_uv=False)
print("amalgam sigma (top 4):", [round(float(x), 12) for x in s2[:4]])

# ---- the atom: lambda = (1/2, 1/2), p = 1 ----------------------------------
la, lb, p = 0.5, 0.5, 1.0
v = np.array([MU[a] ** 0.5 * la ** a[0] * lb ** a[1] for a in G])
A = p * np.outer(v, v)
M = K2 - A
nrm = np.linalg.norm(M, 2)
print("||K - A|| on grid |beta|<=%d: %.15f" % (Gb, nrm))
print("vs sigma_2 = 1        : %.15f   diff = %.3e" % (1.0, nrm - 1.0))

# ---- exact 3-dim reduction (basis e0, f=(e1+e2)/sqrt2, t=tail-normalized) --
e0 = np.zeros(len(G)); e0[gidx[(0, 0)]] = 1.0
f = (np.zeros(len(G)) + 0.0)
f[gidx[(1, 0)]] = 1.0 / math.sqrt(2)
f[gidx[(0, 1)]] = 1.0 / math.sqrt(2)
# tail: v minus its H3 compression
vH3 = np.zeros(len(G))
for a in [(0, 0), (1, 0), (0, 1)]:
    vH3[gidx[a]] = v[gidx[a]]
t = v - vH3
t_norm = np.linalg.norm(t)
t_hat = t / t_norm
B = np.column_stack([e0, f, t_hat])
M3 = B.T @ M @ B
ev = np.sort(np.linalg.eigvalsh(M3))[::-1]
print("error spectrum on (e0, f, t_hat):", [round(float(x), 12) for x in ev])
print("expected (1, -1, -1)")

# identities
rho = la**2 + lb**2
print("rho = %.6f   ||v||^2 = %.6f   (1/(1-rho) = %.6f)" % (rho, v @ v, 1/(1-rho)))
print("||t||^2 = %.6f   (sigma_2^2/sigma_1 = %.6f)" % (t_norm**2, 1.0/2.0))

# ---- the Vol VIII surrogate objective at this point ------------------------
def surrogate(p, r, th):
    la_, lb_ = r * math.cos(th), r * math.sin(th)
    rho_ = r * r
    v_ = np.array([MU[a] ** 0.5 * la_ ** a[0] * lb_ ** a[1] for a in G])
    A_ = p * np.outer(v_, v_)
    box = np.linalg.norm(K2 - A_, 2)
    tail = rho_ ** 9 / (1 - rho_)            # Gb=8 in Vol VIII
    tb = abs(p) * (2 * float(np.linalg.norm(v_)) * math.sqrt(tail) + tail)
    return box + tb

print("Vol VIII surrogate at (p=1, lam=(1/2,1/2)): %.4f  (their optimum: 1.0369)" % surrogate(1.0, math.sqrt(0.5), math.pi/4))

# ---- general amalgam sweep: c0, ca, cb real --------------------------------
print("\n--- the general real amalgam: closure + spectrum (sigma2, -sigma2, -sigma2) ---")
for (c0, ca, cb) in [(1.0, 1.0, 1.0), (1.0, 0.8, 0.6), (2.0, 1.0, 1.0),
                     (0.5, 1.0, 1.0), (0.5, 0.7, -0.4), (3.0, 0.3, 1.1),
                     (1.0, -1.0, 0.5), (0.8, 1.2, 0.9)]:
    phi = {(0, 0): c0, (1, 0): ca, (0, 1): cb}
    K = K_of(phi, G, gidx, MU)
    sv = np.linalg.svd(K, compute_uv=False)
    C2 = ca**2 + cb**2
    G_ = math.sqrt(c0**2 + 4 * C2)
    s1 = (c0 + G_) / 2
    s2v = (G_ - c0) / 2
    # canonical atom
    las, lbs, ps = ca / s1, cb / s1, c0
    vv = np.array([MU[a] ** 0.5 * las ** a[0] * lbs ** a[1] for a in G])
    AA = ps * np.outer(vv, vv)
    MM = K - AA
    nrmv = np.linalg.norm(MM, 2)
    # error spectrum on (u1, u2, t_hat): u1 = top eigvec, u2 = bottom eigvec
    w, U = np.linalg.eigh(K)
    order = np.argsort(np.abs(w))[::-1]
    u1 = U[:, order[0]]; u2 = U[:, order[1]]
    vvH = np.zeros(len(G))
    for a in [(0, 0), (1, 0), (0, 1)]:
        vvH[gidx[a]] = vv[gidx[a]]
    tt = vv - vvH
    tt = tt / np.linalg.norm(tt)
    Bm = np.column_stack([u1, u2, tt])
    M3g = Bm.T @ MM @ Bm
    evg = np.sort(np.linalg.eigvalsh(M3g))[::-1]
    ok = abs(nrmv - s2v) < 1e-9
    print("c0=%4.1f ca=%4.1f cb=%4.1f | sigma2*=%.9f  ||M||=%.9f  closed=%s | "
          "spectrum=(%.6f, %.6f, %.6f)  target=(%.6f, %.6f, %.6f)"
          % (c0, ca, cb, s2v, nrmv, "YES" if ok else "NO",
             evg[0], evg[1], evg[2], s2v, -s2v, -s2v))
