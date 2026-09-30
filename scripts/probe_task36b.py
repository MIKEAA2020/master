#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe_task36b.py — THE COVERAGE PROBE (the decisive test): the SOUND
interval version of the free e4/e5 partial-sum certificate evaluated
on the wall's ACTUAL stall records + the live stack, plus the fixed
P-c (the true X-cancellation conic).

THE SOUND CERTIFICATE (the interval tier, flint/arb prec 96):
    value^2 >= R_N(z) = [P(z) + Q_N(z)] / D(z)
  over the box, with:
    P    the polynomial part (degree <= 4) — the exact interval range;
    Q_N  the partial-sum sandwich (Fu^T z)^T (sum_{n<=N} T_n) (Fu^T z)
         with T_n built by the interval word-power recursion
         T_{n+1} = Aa T_n Aa^T + Ab T_n Ab^T  (sound interval 2x2s);
    D    the constant z'MU z.
  The certificate PASSES the box when the interval lower bound of
  [P + Q_N] exceeds lambda* * D — for EVERY N tried (the N-ladder),
  because Q_N is a pointwise sound lower bound on the true Q at every
  IN-CLASS point of the box (the out-of-class points are vacuous —
  not competitors).

THE COVERAGE TEST (P-e): load free_class_wall_ckpt.json — the 2000
recorded stall boxes (the far-out census + the boundary caps) + the
live stack (the boundary grind) — and count the certified fraction
per N and per instrument tier.  THE DECISIVE VERDICT for the battery
integration.

THE X-CANCELLATION CONIC (P-c fixed): the true cancellation — the
unstable left-eigenvector u of K with the conic u . (C (x) C) = 0
solved for C (the real roots); the B-side conic for the right-
eigenvector of K.  Both solved -> the fully in-class rho > 1 point
(the formal-solve ground truth).

Output: probe_task36b_results.json
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

BLOCKS = [((0, 0), [""]), ((1, 0), ["a"]), ((0, 1), ["b"]),
          ((1, 1), ["ab", "ba"])]
MU = {(0, 0): 1.0, (1, 0): 1.0, (0, 1): 1.0, (1, 1): 2.0}
BETAS = [b for (b, _) in BLOCKS]
NC = {b: (1 - b[0], 1 - b[1]) for b in BETAS}

OUT = {"meta": {"order": "Task 36 probe B: the sound interval "
                         "certificate + the coverage on the actual "
                         "stalls",
                "date": "2026-10-01",
                "lambda_star": LAMBDA_STR}}


# ------------------------------------------------------------------
# the interval machinery
# ------------------------------------------------------------------
def ball(mid, rad):
    return arb("%.17g +/- %.17g" % (mid, max(rad, 0.0)))


def xballs(box):
    return [ball(0.5 * (lo + hi), 0.5 * (hi - lo))
            for (lo, hi) in box]


def i2(xb):
    Aa = [[xb[4], xb[8]], [xb[9], xb[5]]]
    Ab = [[xb[6], xb[10]], [xb[11], xb[7]]]
    return Aa, Ab


def imm(A, Bm):
    return [[A[0][0] * Bm[0][0] + A[0][1] * Bm[1][0],
             A[0][0] * Bm[0][1] + A[0][1] * Bm[1][1]],
            [A[1][0] * Bm[0][0] + A[1][1] * Bm[1][0],
             A[1][0] * Bm[0][1] + A[1][1] * Bm[1][1]]]


def Fu_Fv_iv(xb):
    """the interval class-block sums (degree <= 2)."""
    Aa, Ab = i2(xb)
    Bv = [xb[0], xb[1]]
    Cv = [xb[2], xb[3]]
    FBu, FBv = {}, {}
    for (beta, words) in BLOCKS:
        Su = [arb(0), arb(0)]
        Sv = [arb(0), arb(0)]
        for w in words:
            Mw = [[arb(1), arb(0)], [arb(0), arb(1)]]
            for ch in w:
                Mw = imm(Mw, Aa if ch == "a" else Ab)
            Su = [Su[0] + Bv[0] * Mw[0][0] + Bv[1] * Mw[1][0],
                  Su[1] + Bv[0] * Mw[0][1] + Bv[1] * Mw[1][1]]
            Sv = [Sv[0] + Mw[0][0] * Cv[0] + Mw[0][1] * Cv[1],
                  Sv[1] + Mw[1][0] * Cv[0] + Mw[1][1] * Cv[1]]
        FBu[beta] = Su
        FBv[beta] = Sv
    return FBu, FBv


def imT(M):
    """the transpose of an interval 2x2."""
    return [[M[0][0], M[1][0]], [M[0][1], M[1][1]]]


def word_powers_iv(Aa, Ab, CCt, N):
    """the interval word powers T_0..T_N (the sound recursion —
    THE FULL SANDWICH T_{n+1} = Aa T Aa^T + Ab T Ab^T; the in-session
    bugfix: the first version missed the right multiplication)."""
    Ts = [CCt]
    for _ in range(N):
        T = Ts[-1]
        Tn = imm(imm(Aa, T), imT(Aa))
        Tb = imm(imm(Ab, T), imT(Ab))
        Ts.append([[Tn[0][0] + Tb[0][0], Tn[0][1] + Tb[0][1]],
                   [Tn[1][0] + Tb[1][0], Tn[1][1] + Tb[1][1]]])
    return Ts


def cert_iv(xb, z, N):
    """THE SOUND INTERVAL CERTIFICATE R_N(z) over the box: the arb
    lower bound (the .a's are the sound lower endpoints of the
    numerator's interval; the denominator the constant).  Returns
    the arb lower bound on R_N (the numerator-lower / D) or None."""
    Aa, Ab = i2(xb)
    Bv = [xb[0], xb[1]]
    Cv = [xb[2], xb[3]]
    FBu, FBv = Fu_Fv_iv(xb)
    # Fu^T z (the 2-vector interval)
    fut = [arb(0), arb(0)]
    for i, b in enumerate(BETAS):
        for k in range(2):
            fut[k] = fut[k] + arb(z[i]) * FBu[b][k]
    # CC^T (the interval 2x2)
    CCt = [[Cv[0] * Cv[0], Cv[0] * Cv[1]],
           [Cv[1] * Cv[0], Cv[1] * Cv[1]]]
    Ts = word_powers_iv(Aa, Ab, CCt, N)
    # the sandwich (fut)^T (sum T_n) (fut): interval quadratic form
    T00 = arb(0)
    T01 = arb(0)
    T11 = arb(0)
    for T in Ts:
        T00 = T00 + T[0][0]
        T01 = T01 + T[0][1]
        T11 = T11 + T[1][1]
    f0, f1 = fut[0], fut[1]
    f00 = f0 * f0
    f01 = f0 * f1
    f11 = f1 * f1
    # the two evaluation modes: (i) the plain interval quadratic form
    Q_plain = T00 * f00 + T01 * f01 + T01 * f01 + T11 * f11
    # (ii) the PSD-CLAMPED form (T PSD at every point: v^T T v >=
    # T00 v0^2 + T11 v1^2 - 2 sqrt(T00 T11) |v0 v1| — the interval
    # uppers of the diagonals, the max of |v0 v1|)
    def up(b):
        return abs(float(b.mid())) + float(b.rad())

    def lo(b):
        return float(b.mid()) - float(b.rad())
    T00u, T11u = up(T00), up(T11)
    f00lo, f11lo = lo(f00), lo(f11)
    f01m = max(abs(lo(f01)), abs(up(f01)))
    clamp = (arb(lo(T00)) * arb(f00lo if f00lo > 0 else 0.0)
             + arb(lo(T11)) * arb(f11lo if f11lo > 0 else 0.0)
             - arb(2.0) * arb(math.sqrt(max(T00u * T11u, 0.0)))
             * arb(f01m))
    Q = Q_plain if float(Q_plain) > float(clamp) else clamp
    # the polynomial part P(z) — the exact interval range
    P = arb(0)
    for i, b in enumerate(BETAS):
        zi = arb(z[i])
        P = P + zi * zi * arb(MU[b]) * arb(MU[b]) * arb(MU[NC[b]])
        cross = arb(0)
        for k in range(2):
            cross = cross + FBv[NC[b]][k] * fut[k]
        P = P - arb(2) * zi * arb(MU[b]) * cross
    num = P + Q
    D = sum(MU[b] * z[i] ** 2 for i, b in enumerate(BETAS))
    if D <= 0:
        return None
    return num / arb(D)


# ------------------------------------------------------------------
# the certificate driver: the N-ladder + the z-menu
# ------------------------------------------------------------------
def unstable_pair_float(x, N):
    """the adaptive e4/e5 carriers at the float center (the probe's
    P-f: the generalized eigenproblem of the Fu-sandwich)."""
    Bv, Cv = x[0:2], x[2:4]
    Aa = np.array([[x[4], x[8]], [x[9], x[5]]])
    Ab = np.array([[x[6], x[10]], [x[11], x[7]]])
    FBu, FBv = {}, {}
    for (beta, words) in BLOCKS:
        Su = np.zeros(2)
        for w in words:
            Mw = np.eye(2)
            for ch in w:
                Mw = Mw @ (Aa if ch == "a" else Ab)
            Su = Su + Bv @ Mw
        FBu[beta] = Su
    CCt = np.outer(Cv, Cv)
    T = CCt.copy()
    for _ in range(N):
        T = Aa @ T @ Aa.T + Ab @ T @ Ab.T
    M = np.zeros((4, 4))
    for i, bi in enumerate(BETAS):
        for j, bj in enumerate(BETAS):
            M[i, j] = float(FBu[bi] @ T @ FBu[bj])
    MUd = np.diag([MU[b] for b in BETAS])
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
N_LADDER = (2, 4, 8, 16, 32)


def cert_box(box, Nmax=32, adaptive=True):
    """the box certificate: the N-ladder + the z-menu; returns
    (passed, the best N, the best lower bound, the z used)."""
    xb = xballs(box)
    c = np.array([0.5 * (lo + hi) for (lo, hi) in box])
    best = None
    for N in N_LADDER:
        if N > Nmax:
            break
        zs = list(Z_FIX)
        if adaptive:
            z1, z2 = unstable_pair_float(c, N)
            if z1 is not None:
                zs = zs + [z1, z2]
        for z in zs:
            q = cert_iv(xb, z, N)
            if q is None:
                continue
            m = q - LAMBDA
            if (m > 0) and (not m.overlaps(arb(0))):
                if best is None or float(q) > best[2]:
                    best = (True, N, float(q), tuple(z))
        if best is not None:
            return best
    qb = cert_iv(xb, Z_FIX[0], N_LADDER[-1])
    return (False, None, float(qb) if qb is not None else None, None)


# ------------------------------------------------------------------
# P-e: THE COVERAGE on the actual stalls + the live stack
# ------------------------------------------------------------------
print("=" * 76)
print("P-e — THE COVERAGE on the wall's actual stalls + the live stack")
print("=" * 76)
ck = json.load(open(SCR + "free_class_wall_ckpt.json"))
stalls = ck["f_stalls"]
stack = ck["stack"]
print("  the checkpoint: %d stall records, %d live stack entries"
      % (len(stalls), len(stack)))

# the stall records: (box, depth, value_center, rho_center)
res_stall = {"n": len(stalls), "certified": 0, "by_N": {},
             "by_rho_band": {}}
uncert = []
for (rec, depth, val, rho) in stalls:
    box = tuple(tuple(e) for e in rec)
    (passed, N, q, z) = cert_box(box)
    if passed:
        res_stall["certified"] += 1
        res_stall["by_N"][N] = res_stall["by_N"].get(N, 0) + 1
    else:
        uncert.append((rho, val, q, depth))
    band = ("rho<1" if rho < 1 else
            "1<=rho<1.2" if rho < 1.2 else "rho>=1.2")
    res_stall["by_rho_band"].setdefault(band, [0, 0])
    res_stall["by_rho_band"][band][1] += 1
    if passed:
        res_stall["by_rho_band"][band][0] += 1
print("  THE STALL RECORDS: %d/%d CERTIFIED (%.1f%%)"
      % (res_stall["certified"], len(stalls),
         100.0 * res_stall["certified"] / max(len(stalls), 1)))
print("    by N: %s" % res_stall["by_N"])
for band, (p, t) in sorted(res_stall["by_rho_band"].items()):
    print("    %-10s %d/%d" % (band, p, t))
if uncert:
    rhos = [u[0] for u in uncert]
    vals = [u[1] for u in uncert]
    print("    the uncertified: rho %.3f..%.3f, center values "
          "%.4f..%.4f" % (min(rhos), max(rhos), min(vals), max(vals)))
OUT["Pe_stalls"] = res_stall

# the live stack (the boundary grind — the boxes still splitting)
res_stack = {"n": len(stack), "certified": 0, "by_N": {}}
for (rec, depth) in stack:
    box = tuple(tuple(e) for e in rec)
    (passed, N, q, z) = cert_box(box)
    if passed:
        res_stack["certified"] += 1
        res_stack["by_N"][N] = res_stack["by_N"].get(N, 0) + 1
print("  THE LIVE STACK (the boundary grind): %d/%d CERTIFIED (%.1f%%)"
      % (res_stack["certified"], len(stack),
         100.0 * res_stack["certified"] / max(len(stack), 1)))
print("    by N: %s" % res_stack["by_N"])
OUT["Pe_stack"] = res_stack


# ------------------------------------------------------------------
# P-c (fixed): the true X-cancellation conic
# ------------------------------------------------------------------
print()
print("=" * 76)
print("P-c — the TRUE X-cancellation (the conic on the unstable mode)")
print("=" * 76)
def kron4(Aa, Ab):
    return np.kron(Aa, Aa) + np.kron(Ab, Ab)


def conic_solution(u):
    """solve u . (C (x) C) = 0: u0 C0^2 + (u1+u2) C0 C1 + u3 C1^2 = 0
    for the real C (up to scale); None if no real root."""
    a, b, c = u[0], u[1] + u[2], u[3]
    if abs(c) < 1e-12:
        if abs(a) < 1e-12:
            return None
        return np.array([0.0, 1.0]) if abs(b) > 1e-12 else None
    disc = b * b - 4.0 * a * c
    if disc < 0:
        return None
    r1 = (-b + math.sqrt(disc)) / (2.0 * c)
    r2 = (-b - math.sqrt(disc)) / (2.0 * c)
    # pick the root with the smaller magnitude
    r = r1 if abs(r1) <= abs(r2) else r2
    return np.array([1.0, r])


pcres = []
rng = np.random.default_rng(360)
for trial in range(12):
    Aa = rng.uniform(0.4, 1.4, (2, 2)) * rng.choice([-1, 1], (2, 2))
    Ab = rng.uniform(0.05, 0.5, (2, 2))
    K = kron4(Aa, Ab)
    ev = np.linalg.eigvals(K)
    rho = max(abs(ev))
    if rho <= 1.05:
        continue
    # the unstable left-eigenvector: K^T u = lam u, |lam| = rho
    lam = ev[np.argmax(abs(ev))]
    w, U = np.linalg.eig(K.T)
    j = np.argmin(abs(w - lam))
    u = np.real(U[:, j])
    if np.linalg.norm(np.imag(U[:, j])) > 1e-8:
        continue
    C = conic_solution(u)
    if C is None:
        continue
    # the B-side conic: the right-eigenvector v of K (lam), the
    # transpose constraint: v . (B (x) B) = 0 with vec(BB^T) — the
    # Lr recursion uses K^T: vec(BB^T) ⊥ the unstable LEFT-eigvecs
    # of K^T = the RIGHT-eigvecs of K
    w2, U2 = np.linalg.eig(K)
    j2 = np.argmin(abs(w2 - lam))
    v_ = np.real(U2[:, j2])
    B = conic_solution(v_)
    if B is None:
        B = np.zeros(2)
    x = np.array([B[0], B[1], C[0], C[1],
                  Aa[0, 0], Aa[1, 1], Ab[0, 0], Ab[1, 1],
                  Aa[0, 1], Aa[1, 0], Ab[0, 1], Ab[1, 1]])
    # the formal solve (the X-cancelled truth)
    Lc_f = np.linalg.solve(
        np.eye(4) - K, np.outer(x[2:4], x[2:4]).reshape(4, order="F")
        ).reshape(2, 2, order="F")
    # the partial-sum convergence: the word powers' growth stalls
    Ts = [np.outer(x[2:4], x[2:4])]
    for _ in range(64):
        T = Ts[-1]
        Ts.append(Aa @ T @ Aa.T + Ab @ T @ Ab.T)
    nrm = [float(np.linalg.norm(T)) for T in Ts]
    conv = nrm[-1] < 5.0 * np.median(nrm[:8])
    # the certificate's N-chain (float, the box = the point)
    box = [(xi, xi) for xi in x]
    chain = []
    for N in (4, 16, 32):
        q = cert_iv(xballs(box), Z_FIX[0], N)
        chain.append(float(q) if q is not None else None)
    # the formal value (the pencil with the formal Lc/Lr)
    Bv, Cv = x[0:2], x[2:4]
    Lr_f = np.linalg.solve(
        np.eye(4) - K, np.outer(Bv, Bv).reshape(4, order="F")
        ).reshape(2, 2, order="F") if np.max(np.abs(Bv)) > 0 \
        else np.zeros((2, 2))
    val_f = None
    try:
        G = np.zeros((6, 6))
        Cmat = np.zeros((6, 6))
        FBu, FBv = {}, {}
        for (beta, words) in BLOCKS:
            Su = np.zeros(2)
            Sv = np.zeros(2)
            for w in words:
                Mw = np.eye(2)
                for ch in w:
                    Mw = Mw @ (Aa if ch == "a" else Ab)
                Su = Su + Bv @ Mw
                Sv = Sv + Mw @ Cv
            FBu[beta] = Su
            FBv[beta] = Sv
        for i, b in enumerate(BETAS):
            G[i, i] = MU[b]
            Cmat[i, i] = MU[NC[b]]
            for k in range(2):
                G[i, 4 + k] = FBu[b][k]
                G[4 + k, i] = FBu[b][k]
                Cmat[i, 4 + k] = -FBv[NC[b]][k]
                Cmat[4 + k, i] = -FBv[NC[b]][k]
        G[4:6, 4:6] = Lr_f
        Cmat[4:6, 4:6] = Lc_f
        val_f = math.sqrt(max(max(float(np.real(e))
                                  for e in np.linalg.eigvals(Cmat @ G)), 0))
    except Exception:
        pass
    print("  rho %.3f: the partial norms %s — %s; cert chain %s; "
          "formal value %s"
          % (rho, "%.2f->%.2g" % (nrm[1], nrm[-1]),
             "CONVERGES" if conv else "diverges",
             " ".join("%.4f" % c_ for c_ in chain if c_ is not None),
             "%.6f" % (val_f * val_f) if val_f else "n/a"))
    pcres.append({"rho": float(rho), "converges": bool(conv),
                  "cert_chain": chain,
                  "formal_value_sq": float(val_f * val_f)
                  if val_f else None})
OUT["Pc_xcancellation_conic"] = pcres

# the soundness check: cert_chain <= formal_value^2 on the convergent
# cases
viol = 0
for r in pcres:
    if r["converges"] and r["formal_value_sq"] is not None:
        for c_ in r["cert_chain"]:
            if c_ is not None and c_ > r["formal_value_sq"] + 1e-9:
                viol += 1
print("  the soundness (cert <= formal value on the convergent "
      "strata): %d violations" % viol)
OUT["Pc_soundness_violations"] = viol

print()
print("probe B complete")
with open(SCR + "probe_task36b_results.json", "w") as f:
    json.dump(OUT, f, indent=1)
