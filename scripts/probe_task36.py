#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe_task36.py — THE FREE e4/e5 UNSTABLE-MODE DIVERGENCE FORMS (Task 36's
named assignment: close the rho-boundary residue the way Task 34 closed
the abelian one).

THE FORMALIZATION (the Task-34 mirror).  The abelian BDC certified the
disc-edge divergence layer with the exact e0/e4/e5 Rayleigh corner
identities — the closed forms whose LEADING terms diverge at the domain
wall (1/d11^2, d11 -> 0+) while the poison stays bounded.  THE FREE
ANALOGUE: the domain wall is the Gram wall rho(K) = 1 (the bounded-
Hankel class boundary), and the divergence lives in the Lyapunov
blocks:

    Lc = sum_{n>=0} T_n,   T_0 = CC^T,  T_{n+1} = Aa T_n Aa^T + Ab T_n Ab^T

(the word-power recursion — each T_n = sum_{|w|=n} Mw CC^T Mw^T is PSD;
the partial sums are PSD-monotone increasing toward Lc, CONVERGENT for
every in-class point — including the rho >= 1 X-cancellation strata
where the formal Neumann diverges but the true Gramian exists).

THE CERTIFICATE (the free e4/e5 form).  At the class vectors
v = (z, 0) (the reach-part zero — THE DENOMINATOR IS CONSTANT:
v'Gv = sum mu_i z_i^2, no Gramian entries, no poison):

    value^2 >= R(z) = [P(z) + Q(z)] / D(z),
    P(z)   = sum_i mu_c_i mu_i^2 z_i^2
             - 2 sum_{i,k} mu_i z_i Fv[comp_i]_k (Fu^T z)_k
              (POLYNOMIAL, degree <= 4 — the exact interval range),
    Q(z)   = (Fu^T z)^T Lc (Fu^T z)
           >= (Fu^T z)^T (sum_{n<=N} T_n) (Fu^T z) = Q_N(z)
              (the PARTIAL-SUM sandwich — sound for every in-class
              point, POLYNOMIAL (degree 2N+4), NO CONVERGENCE NEEDED),
    D(z)   = sum_i mu_i z_i^2 (constant).

THE TWO MODES (the e4/e5 naming): the reach-space carriers — the z-
vectors whose Fu^T z aligns with the two eigendirections of the 2x2
partial-sum matrix (the UNSTABLE MODES: the most-observable directions
of the word powers) — the adaptive pair from the box center's
generalized eigenproblem (Fu-block-sandwich vs MU).

THE SOUNDNESS LOGIC (the whole competitor class):
  - in-class points (the bounded Hankel: BOTH Gramians finite — the
    rho < 1 interior AND the rho >= 1 X-cancellation strata):
    Q >= Q_N for every N — the certificate is a sound lower bound;
  - out-of-class points (an unstable mode excited on the C-side with
    C =/= 0, or on the B-side with B =/= 0): the Hankel norm is
    INFINITE — the point is NOT a competitor — vacuous;
  - the C = 0 / B = 0 cancellations: the zero-function anchors (the
    corner value EXACTLY 2 — the e0 anchor).

PROBES:
  P-a  the anchor + the soundness direction at the known in-domain
       points (the certificate <= the full float value);
  P-b  the divergence at the near-locus chain (rho -> 1 from both
       sides): the partial sums' growth vs N, the certificate crossing
       lambda*;
  P-c  the X-cancellation strata (rho > 1, the C-side cancelled): the
       partial sums CONVERGE — the certificate still sound, the value
       finite (the formal-solve agreement);
  P-d  the out-of-class divergence (rho > 1, excited): the partial
       sums' EXPONENTIAL growth — the certificate -> infinity;
  P-e  THE COVERAGE on the wall's actual stalls (the 2000 recorded
       records + the live stack): the certified fraction per N — the
       decisive test;
  P-f  the adaptive unstable-mode pair vs the fixed Z_VECS (the gain).

Output: probe_task36_results.json
"""
import json
import math
import os

import numpy as np
from flint import arb

try:
    from flint import ctx
    ctx.prec = 96
except Exception:
    pass

SCR = "/home/z/my-project/github_repos/master/scripts/"
LAMBDA_STR = "1.6310919765642504414737578928177383666901925754942"
LAMBDA = arb(LAMBDA_STR)
LAMBDA_F = float(LAMBDA_STR)
SQRT_L = LAMBDA_F ** 0.5

BLOCKS = [((0, 0), [""]), ((1, 0), ["a"]), ((0, 1), ["b"]),
          ((1, 1), ["ab", "ba"])]
MU = {(0, 0): 1.0, (1, 0): 1.0, (0, 1): 1.0, (1, 1): 2.0}
BETAS = [b for (b, _) in BLOCKS]
NC = {b: (1 - b[0], 1 - b[1]) for b in BETAS}

OUT = {"meta": {"order": "Task 36 probe: the free e4/e5 unstable-mode "
                         "divergence forms",
                "date": "2026-10-01",
                "lambda_star": LAMBDA_STR}}

X_SYM8 = np.load(SCR + "shadow_refined.npy")
X_SYM = np.concatenate([X_SYM8, np.zeros(4)])
X_FREE = np.load(SCR + "escape_refined.npy")


# ------------------------------------------------------------------
# the float machinery (the corpus's build_GC — imported in-line)
# ------------------------------------------------------------------
def mats_of(x):
    Aa = np.array([[x[4], x[8]], [x[9], x[5]]])
    Ab = np.array([[x[6], x[10]], [x[11], x[7]]])
    return x[0:2], x[2:4], Aa, Ab


def kron4(Aa, Ab):
    return np.kron(Aa, Aa) + np.kron(Ab, Ab)


def lyap(Aa, Ab, X, trans=False):
    K = (np.kron(Aa.T, Aa.T) + np.kron(Ab.T, Ab.T) if trans
         else kron4(Aa, Ab))
    rho = max(abs(np.linalg.eigvals(K)))
    if np.max(np.abs(X)) < 1e-15:
        return np.zeros((2, 2)), rho
    if rho >= 1.0 - 1e-12:
        return None, rho
    v = np.linalg.solve(np.eye(4) - K, X.reshape(4, order="F"))
    return v.reshape(2, 2, order="F"), rho


def build_GC(B, C, Aa, Ab):
    Lc, rho = lyap(Aa, Ab, np.outer(C, C))
    if Lc is None:
        return None, None, rho
    Lr, _ = lyap(Aa, Ab, np.outer(B, B), trans=True)
    if Lr is None:
        return None, None, rho
    FBu, FBv = {}, {}
    for (beta, words) in BLOCKS:
        Su = np.zeros(2)
        Sv = np.zeros(2)
        for w in words:
            Mw = np.eye(2)
            for ch in w:
                Mw = Mw @ (Aa if ch == "a" else Ab)
            Su = Su + B @ Mw
            Sv = Sv + Mw @ C
        FBu[beta] = Su
        FBv[beta] = Sv
    G = np.zeros((6, 6))
    Cmat = np.zeros((6, 6))
    for i, b in enumerate(BETAS):
        G[i, i] = MU[b]
        Cmat[i, i] = MU[NC[b]]
        for k in range(2):
            G[i, 4 + k] = FBu[b][k]
            G[4 + k, i] = FBu[b][k]
            Cmat[i, 4 + k] = -FBv[NC[b]][k]
            Cmat[4 + k, i] = -FBv[NC[b]][k]
    G[4:6, 4:6] = Lr
    Cmat[4:6, 4:6] = Lc
    return G, Cmat, rho


def norm_of(B, C, Aa, Ab):
    G, Cmat, rho = build_GC(B, C, Aa, Ab)
    if G is None:
        return 1e6, rho
    ev = np.linalg.eigvals(Cmat @ G)
    return math.sqrt(max(max(float(np.real(e)) for e in ev), 0.0)), rho


# ------------------------------------------------------------------
# THE FLOAT PARTIAL-SUM MACHINERY (the word powers)
# ------------------------------------------------------------------
def word_powers(Aa, Ab, CCt, N):
    """T_0..T_N: T_0 = CCt, T_{n+1} = Aa T_n Aa^T + Ab T_n Ab^T.
    Returns the list [T_0, ..., T_N] (each PSD in exact arithmetic)."""
    Ts = [CCt.copy()]
    for _ in range(N):
        T = Ts[-1]
        Ts.append(Aa @ T @ Aa.T + Ab @ T @ Ab.T)
    return Ts


def Fu_Fv_float(B, C, Aa, Ab):
    """the finite class-block sums (degree <= 2 polynomials)."""
    FBu, FBv = {}, {}
    for (beta, words) in BLOCKS:
        Su = np.zeros(2)
        Sv = np.zeros(2)
        for w in words:
            Mw = np.eye(2)
            for ch in w:
                Mw = Mw @ (Aa if ch == "a" else Ab)
            Su = Su + B @ Mw
            Sv = Sv + Mw @ C
        FBu[beta] = Su
        FBv[beta] = Sv
    return FBu, FBv


def cert_float(x, z, N):
    """the FLOAT partial-sum certificate R_N(z) (the probe's
    measurement — the sound version is the interval one below):
    R_N(z) = [P(z) + Q_N(z)]/D(z)."""
    B, C, Aa, Ab = mats_of(x)
    FBu, FBv = Fu_Fv_float(B, C, Aa, Ab)
    FuTz = sum(z[i] * FBu[b] for i, b in enumerate(BETAS))
    Ts = word_powers(Aa, Ab, np.outer(C, C), N)
    Q_N = float(FuTz @ (sum(Ts)) @ FuTz)
    P = sum(MU[NC[b]] * (MU[b] * z[i]) ** 2 for i, b in enumerate(BETAS))
    P = P - 2.0 * sum(MU[b] * z[i] * float(FBv[NC[b]] @ FuTz)
                      for i, b in enumerate(BETAS))
    D = sum(MU[b] * z[i] ** 2 for i, b in enumerate(BETAS))
    return (P + Q_N) / D


def unstable_pair(x, N):
    """the adaptive e4/e5 carriers: the top-2 generalized eigenvectors
    of (M, MU) with M = the Fu-sandwich of the center's partial sum —
    the z-vectors whose Fu^T z aligns with the partial-sum matrix's
    dominant directions (the unstable modes)."""
    B, C, Aa, Ab = mats_of(x)
    FBu, FBv = Fu_Fv_float(B, C, Aa, Ab)
    Ts = word_powers(Aa, Ab, np.outer(C, C), N)
    Tsum = sum(Ts)
    # M[i,j] = sum_{k,l} Tsum[k,l] Fu_i[k] Fu_j[l]  (the z-sandwich)
    M = np.zeros((4, 4))
    for i, bi in enumerate(BETAS):
        for j, bj in enumerate(BETAS):
            M[i, j] = float(FBu[bi] @ Tsum @ FBu[bj])
    MUd = np.diag([MU[b] for b in BETAS])
    # the generalized eigenproblem M z = lam MU z
    try:
        w, V = np.linalg.eigh(np.linalg.solve(
            np.sqrt(MUd), M @ np.sqrt(MUd)))
        order = np.argsort(-w)
        z1 = np.sqrt(MUd) @ V[:, order[0]]
        z2 = np.sqrt(MUd) @ V[:, order[1]] if len(order) > 1 else None
        for zz in (z1, z2):
            if zz is not None and np.linalg.norm(zz) > 0:
                zz[:] = zz / np.linalg.norm(zz)
        return z1, z2
    except Exception:
        return None, None


Z_FIX = [np.array([1.0, 0.0, 0.0, 0.0]),
         np.array([0.0, 0.0, 0.0, 1.0]),
         np.array([0.5, 0.5, 0.5, 0.5]),
         np.array([0.0, 0.5, 0.5, 0.0])]


# ------------------------------------------------------------------
# P-a: the anchor + the soundness direction
# ------------------------------------------------------------------
print("=" * 76)
print("P-a — the anchor + the soundness (cert_N <= full value)")
print("=" * 76)
# the zero WFA: A arbitrary, B = C = 0: the value = 2 (the corner
# anchor); the certificate must return EXACTLY 2 (Q_N = 0, P = the
# pure corner)
rng = np.random.default_rng(36)
pa = []
worst = 0.0
for _ in range(20):
    Aa = rng.uniform(-1.5, 1.5, (2, 2))
    Ab = rng.uniform(-1.5, 1.5, (2, 2))
    xz = np.concatenate([np.zeros(4), Aa.flat, Ab.flat])
    # order: x[4]=Aa11, x[5]=Aa22, x[6]=Ab11, x[7]=Ab22,
    #        x[8]=Aa12, x[9]=Aa21, x[10]=Ab12, x[11]=Ab21
    xz = np.array([Aa[0, 0], Aa[1, 1], Ab[0, 0], Ab[1, 1],
                   Aa[0, 1], Aa[1, 0], Ab[0, 1], Ab[1, 0]])
    xz = np.concatenate([np.zeros(4), xz])
    v, rho = norm_of(*mats_of(xz))
    cN = max(cert_float(xz, z, 8) for z in Z_FIX)
    worst = max(worst, abs(cN - 2.0))
    pa.append((v, cN, rho))
print("  the zero-WFA anchor: |cert_N - 2| max %.2e over 20 random "
      "(Aa, Ab) [rho %.2f..%.2f]  (the e0 corner z)" %
      (worst, min(p[2] for p in pa), max(p[2] for p in pa)))
OUT["Pa_anchor"] = {"max_dev_2": float(worst), "n": 20}

# the soundness at the known in-domain points
for tag, x in [("the symmetric shadow", X_SYM),
               ("the free escape", X_FREE)]:
    v, rho = norm_of(*mats_of(x))
    row = []
    for N in (2, 4, 8, 16):
        z1, z2 = unstable_pair(x, N)
        zs = Z_FIX + ([z1, z2] if z1 is not None else [])
        cN = max(cert_float(x, z, N) for z in zs)
        row.append((N, cN, v * v))
    ok = all(c <= v * v + 1e-9 for (_, c, vv) in row)
    print("  %-20s value^2 %.10f (rho %.3f) — cert_N: %s  %s"
          % (tag, v * v, rho,
             " ".join("N=%d: %.6f" % (n, c) for (n, c, _) in row),
             "SOUND" if ok else "VIOLATION"))
    OUT["Pa_" + tag.replace(" ", "_")] = {
        "value_sq": float(v * v), "rho": float(rho),
        "cert_N": [(n, float(c)) for (n, c, _) in row],
        "sound": bool(ok)}

# ------------------------------------------------------------------
# P-b: the near-locus divergence chain (rho -> 1 from both sides)
# ------------------------------------------------------------------
print()
print("=" * 76)
print("P-b — the near-locus chain (scale A -> rho = 1)")
print("=" * 76)
pb = []
base = X_SYM.copy()
_, _, Aa0, Ab0 = mats_of(base)
K0 = kron4(Aa0, Ab0)
rho0 = max(abs(np.linalg.eigvals(K0)))
for tgt in (0.80, 0.90, 0.95, 0.98, 0.995, 0.999, 1.002, 1.01, 1.03):
    t = math.sqrt(tgt / rho0)
    x = base.copy()
    x[4:12] = x[4:12] * t
    B, C, Aa, Ab = mats_of(x)
    K = kron4(Aa, Ab)
    rho = max(abs(np.linalg.eigvals(K)))
    v, _ = norm_of(B, C, Aa, Ab)
    # the partial-sum growth: the max over z of Q_N's contribution
    growth = []
    for N in (2, 4, 8, 16, 32):
        z1, z2 = unstable_pair(x, N)
        zs = Z_FIX + ([z1, z2] if z1 is not None else [])
        cN = max(cert_float(x, z, N) for z in zs)
        growth.append((N, cN))
    fin = v < 1e5
    print("  rho %.4f: value^2 %s  cert: %s"
          % (rho, "%.6f" % (v * v) if fin else "INF (out)",
             " ".join("N=%d:%.3f" % (n, c) for (n, c) in growth)))
    pb.append({"rho": float(rho), "value_sq": float(v * v) if fin else None,
               "cert_N": [(n, float(c)) for (n, c) in growth]})
OUT["Pb_locus_chain"] = pb

# ------------------------------------------------------------------
# P-c: the X-cancellation strata (rho > 1, the C-side cancelled)
# ------------------------------------------------------------------
print()
print("=" * 76)
print("P-c — the X-cancellation strata (rho > 1, C-side cancelled)")
print("=" * 76)
pc = []
# the shear family: Aa = [[a, s],[0, b]] nilpotent-ish coupling; K's
# unstable left-eigenmatrix targeted, C chosen orthogonal (C_0 = 0 ->
# vec(CC^T) has e0-components zero)
for (a, b, s) in [(1.1, 0.3, 0.7), (0.9, 1.05, 0.4), (1.2, 0.2, 1.0)]:
    Aa = np.array([[a, s], [0.0, b]])
    Ab = np.array([[0.2, 0.1], [0.05, 0.15]])
    K = kron4(Aa, Ab)
    rho = max(abs(np.linalg.eigvals(K)))
    # the C-side cancellation: C = (0, c) kills the e0-e0 component of
    # CC^T; check the partial sums' convergence (the growth stalls)
    for c in (0.5,):
        C = np.array([0.0, c])
        B = np.array([0.3, -0.2])
        x = np.array([B[0], B[1], C[0], C[1],
                      Aa[0, 0], Aa[1, 1], Ab[0, 0], Ab[1, 1],
                      Aa[0, 1], Aa[1, 0], Ab[0, 1], Ab[1, 1]])
        # the partial sums Q_N(z*) at the unstable pair: convergence?
        vals = []
        for N in (4, 8, 16, 32, 64):
            z1, _ = unstable_pair(x, N)
            zs = Z_FIX + ([z1] if z1 is not None else [])
            cN = max(cert_float(x, z, N) for z in zs)
            vals.append(cN)
        # the formal solve (I-K)^{-1} (the X-cancelled truth)
        Lc_formal = np.linalg.solve(
            np.eye(4) - K, np.outer(C, C).reshape(4, order="F")
            ).reshape(2, 2, order="F")
        growing = vals[-1] > 1.3 * vals[2] if vals[2] > 0 else \
            vals[-1] > 10.0
        print("  a=%.2f b=%.2f s=%.2f: rho %.3f — cert N-chain %s "
              "-> %s" %
              (a, b, s, rho,
               " ".join("%.3f" % v_ for v_ in vals),
               "DIVERGES (excited)" if growing else "converges"))
        pc.append({"rho": float(rho), "cert_chain":
                   [float(v_) for v_ in vals],
                   "diverges": bool(growing),
                   "Lc_formal": [[float(Lc_formal[i, j])
                                  for j in range(2)]
                                 for i in range(2)]})
OUT["Pc_xcancellation"] = pc

# ------------------------------------------------------------------
# P-d: the out-of-class divergence (rho > 1, excited) — the growth law
# ------------------------------------------------------------------
print()
print("=" * 76)
print("P-d — the excited divergence (the growth law ~ rho^{2N})")
print("=" * 76)
pd = []
base2 = X_SYM.copy()
_, _, Aa0, Ab0 = mats_of(base2)
rho0b = max(abs(np.linalg.eigvals(kron4(Aa0, Ab0))))
for tgt in (1.05, 1.2, 1.5):
    t = math.sqrt(tgt / rho0b)
    x = base2.copy()
    x[4:12] = x[4:12] * t
    vals = []
    for N in (2, 4, 8, 16, 32):
        z1, _ = unstable_pair(x, N)
        zs = Z_FIX + ([z1] if z1 is not None else [])
        vals.append(max(cert_float(x, z, N) for z in zs))
    # the growth rate per doubling of N ~ rho^{2N}
    r2 = (vals[-1] / vals[2]) ** (1.0 / 30.0) if vals[2] > 0 else None
    print("  rho %.3f: cert N-chain %s (growth^(1/2N) %.3f)"
          % (tgt / rho0b * rho0b,
             " ".join("%.3g" % v_ for v_ in vals),
             r2 if r2 else -1))
    pd.append({"rho": float(tgt / rho0b * rho0b),
               "cert_chain": [float(v_) for v_ in vals],
               "rate_per_halfstep": float(r2) if r2 else None})
OUT["Pd_excited_growth"] = pd

print()
print("probe complete — the results in probe_task36_results.json")
with open(SCR + "probe_task36_results.json", "w") as f:
    json.dump(OUT, f, indent=1)
