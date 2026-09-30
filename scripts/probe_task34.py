#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe_task34.py — Task 34's design probes (before the engine edit):

P-1 the pipeline cost (the old box-mode patch_box on sample boxes);
P-2 the DPP (the derivative-penalty patch mode) r-gain: the two-scale
    certificate ((m0, gamma, kappa, C3) at the box-scale widening 2h,
    C4 at the full-region widening 2h + r) vs the old all-at-2h+r;
P-3 V-F the pi-rotation symmetry: norm6 invariance under
    (x1,y1,x2,y2) -> (-x1,-y1,-x2,-y2) (both atoms, p unchanged);
P-4 V-G the BDC closed forms: the exact identities
    R6(e0) = 2 - 4x1y1p1 - 4x2y2p2 + p'Lc p,
    R6(e4) = p1^2/d11^2 + 2p1p2/d12^2 + d11*(2+x1^2+y1^2+4x1^2y1^2)
             - 12p1x1y1 - 2*d11*p2*T2/d12 + d11*p2^2/(d12^2*d22),
    R6(e5) (the swap image);
P-5 V-H the linear CS bound: d12 >= max(d11, d22)/2 on the open
    disc-pair (the poison-free ratio bound d11/d12 <= 2);
P-6 the BDC bounds on the LIVE frontier: the 43 deep stack branches +
    the recorded stall boxes (the certificate's margin at each).
"""
import json
import math
import time

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

# ---- the corpus loads (the TP machinery + the ball helpers) ----
t0 = time.time()
src_tp = open(SCR + "tradeoff_patch.py").read()
_i = src_tp.index("V5: the TP algebra")
_cut = src_tp.rindex("\n#", 0, _i) + 1
ns_tp = {}
exec(compile(src_tp[:_cut], "tp_head", "exec"), ns_tp)
pipeline = ns_tp["pipeline"]
IDX = ns_tp["IDX"]
BY_DEG = ns_tp["BY_DEG"]
up = ns_tp["up"]
ab = ns_tp["ab"]
extract = ns_tp["extract"]
phi_ok = ns_tp["phi_ok"]
R_CAP = ns_tp["R_CAP"]
print("corpus loaded (%.1fs), R_CAP = %s" % (time.time() - t0, R_CAP))

C_STAR = 0.3971672569443035
Y_STAR = 0.6563248795193563
W_STAR = C_STAR / 2.0
MU4 = [1.0, 1.0, 1.0, 2.0]
COMP4 = [3, 2, 1, 0]


def norm6_float(p1, x1, y1, p2, x2, y2):
    d11 = 1.0 - x1 * x1 - y1 * y1
    d12 = 1.0 - x1 * x2 - y1 * y2
    d22 = 1.0 - x2 * x2 - y2 * y2
    if min(d11, d12, d22) <= 0.0:
        return None, None, None
    Lc = [[1.0 / d11, 1.0 / d12], [1.0 / d12, 1.0 / d22]]
    Lr = [[p1 * p1 / d11, p1 * p2 / d12],
          [p2 * p1 / d12, p2 * p2 / d22]]
    s = [[1.0, 1.0], [x1, x2], [y1, y2], [2.0 * x1 * y1, 2.0 * x2 * y2]]
    pk = [p1, p2]
    G = np.zeros((6, 6))
    C = np.zeros((6, 6))
    for i in range(4):
        G[i, i] = MU4[i]
        C[i, i] = MU4[COMP4[i]]
        for k in range(2):
            G[i, 4 + k] = pk[k] * s[i][k]
            G[4 + k, i] = G[i, 4 + k]
            C[i, 4 + k] = -s[COMP4[i]][k]
            C[4 + k, i] = C[i, 4 + k]
    G[4, 4] = Lr[0][0]; G[4, 5] = Lr[0][1]
    G[5, 4] = Lr[1][0]; G[5, 5] = Lr[1][1]
    C[4, 4] = Lc[0][0]; C[4, 5] = Lc[0][1]
    C[5, 4] = Lc[1][0]; C[5, 5] = Lc[1][1]
    lam = max(float(np.real(e)) for e in np.linalg.eigvals(C @ G))
    return lam, G, C


def R6_float(v, p1, x1, y1, p2, x2, y2):
    lam, G, C = norm6_float(p1, x1, y1, p2, x2, y2)
    v = np.array(v, dtype=float)
    return float(v @ G @ C @ G @ v) / float(v @ G @ v), lam


rng = np.random.default_rng(20260930)

# ============================== P-3: V-F the pi-rotation
vf = 0.0
for _ in range(240):
    p1, p2 = rng.uniform(-3, 3, 2)
    r1, r2 = rng.uniform(0.05, 0.9, 2)
    th1, th2 = rng.uniform(0, 2 * math.pi, 2)
    x1, y1 = r1 * math.cos(th1), r1 * math.sin(th1)
    x2, y2 = r2 * math.cos(th2), r2 * math.sin(th2)
    la = norm6_float(p1, x1, y1, p2, x2, y2)[0]
    lb = norm6_float(p1, -x1, -y1, p2, -x2, -y2)[0]
    vf = max(vf, abs(la - lb))
print("\nP-3  V-F the pi-rotation symmetry: max diff %.2e (240 samples)"
      % vf)

# ============================== P-4: V-G the BDC closed forms
vg0 = vg4 = vg5 = 0.0
for _ in range(240):
    p1, p2 = rng.uniform(-8, 8, 2)
    r1, r2 = rng.uniform(0.05, 0.95, 2)
    th1, th2 = rng.uniform(0, 2 * math.pi, 2)
    x1, y1 = r1 * math.cos(th1), r1 * math.sin(th1)
    x2, y2 = r2 * math.cos(th2), r2 * math.sin(th2)
    d11 = 1 - x1 ** 2 - y1 ** 2
    d12 = 1 - x1 * x2 - y1 * y2
    d22 = 1 - x2 ** 2 - y2 ** 2
    if min(d11, d12, d22) <= 0:
        continue
    Lc = np.array([[1 / d11, 1 / d12], [1 / d12, 1 / d22]])
    # e0
    r_e0 = R6_float((1, 0, 0, 0, 0, 0), p1, x1, y1, p2, x2, y2)[0]
    f_e0 = 2 - 4 * x1 * y1 * p1 - 4 * x2 * y2 * p2 \
        + (np.array([p1, p2]) @ Lc @ np.array([p1, p2]))
    vg0 = max(vg0, abs(r_e0 - f_e0))
    # e4
    T2 = 2 * x2 * y2 + y2 * x1 + x2 * y1 + 2 * x1 * y1
    r_e4 = R6_float((0, 0, 0, 0, 1, 0), p1, x1, y1, p2, x2, y2)[0]
    f_e4 = p1 ** 2 / d11 ** 2 + 2 * p1 * p2 / d12 ** 2 \
        + d11 * (2 + x1 ** 2 + y1 ** 2 + 4 * x1 ** 2 * y1 ** 2) \
        - 12 * p1 * x1 * y1 - 2 * d11 * p2 * T2 / d12 \
        + d11 * p2 ** 2 / (d12 ** 2 * d22)
    vg4 = max(vg4, abs(r_e4 - f_e4))
    # e5 (the swap image)
    T1p = 2 * x1 * y1 + y1 * x2 + x1 * y2 + 2 * x2 * y2
    r_e5 = R6_float((0, 0, 0, 0, 0, 1), p1, x1, y1, p2, x2, y2)[0]
    f_e5 = p2 ** 2 / d22 ** 2 + 2 * p1 * p2 / d12 ** 2 \
        + d22 * (2 + x2 ** 2 + y2 ** 2 + 4 * x2 ** 2 * y2 ** 2) \
        - 12 * p2 * x2 * y2 - 2 * d22 * p1 * T1p / d12 \
        + d22 * p1 ** 2 / (d12 ** 2 * d11)
    vg5 = max(vg5, abs(r_e5 - f_e5))
print("P-4  V-G the closed forms (240 samples): e0 %.2e / e4 %.2e / "
      "e5 %.2e" % (vg0, vg4, vg5))

# ============================== P-5: V-H the linear CS bound
vh = 0.0
for _ in range(2000):
    r1, r2 = rng.uniform(0.05, 0.999, 2)
    th1, th2 = rng.uniform(0, 2 * math.pi, 2)
    x1, y1 = r1 * math.cos(th1), r1 * math.sin(th1)
    x2, y2 = r2 * math.cos(th2), r2 * math.sin(th2)
    d11 = 1 - x1 ** 2 - y1 ** 2
    d12 = 1 - x1 * x2 - y1 * y2
    d22 = 1 - x2 ** 2 - y2 ** 2
    if min(d11, d12, d22) <= 0:
        continue
    vh = max(vh, max(d11, d22) / 2.0 - d12)   # must be <= 0
print("P-5  V-H the linear CS bound d12 >= max(d11,d22)/2: max "
      "violation %.2e (2000 samples)" % vh)

# ============================== P-2: the DPP r-gain
def patch_box_old(wlo, whi, xlo, xhi, ylo, yhi, vecs, niter=5):
    wc, xc, yc = 0.5 * (wlo + whi), 0.5 * (xlo + xhi), 0.5 * (ylo + yhi)
    hmax = 0.5 * max(whi - wlo, xhi - xlo, yhi - ylo)
    center = (wc, xc, yc, wc, -xc, yc)
    best = None
    for (ve, vo) in vecs:
        for side, v in (("o", vo), ("e", ve)):
            if v is None:
                continue
            lo, hi = 2e-5, min(R_CAP, 0.12)
            r_ok = None
            for _ in range(niter):
                mid_r = 0.5 * (lo + hi)
                box_r = 2.0 * hmax + mid_r
                R, err = pipeline(center, v, side, box_r=box_r)
                if R is None:
                    hi = mid_r
                    continue
                m0 = R.c[0] - LAMBDA
                if not ((m0 > 0) and (not m0.overlaps(arb(0)))):
                    hi = mid_r
                    continue
                gamma, kap, C3 = extract(R)
                C4 = sum(up(R.c[i]) for i in BY_DEG[4])
                if phi_ok(m0, gamma, kap, C3, C4, mid_r):
                    r_ok, lo = mid_r, mid_r
                else:
                    hi = mid_r
            if r_ok is not None and (best is None or r_ok > best[0]):
                best = (r_ok, side, "old")
    return best


def patch_box_dpp(wlo, whi, xlo, xhi, ylo, yhi, vecs, niter=7):
    """THE DERIVATIVE-PENALTY PATCH MODE: (m0, gamma, kappa, C3) from
    the box-scale widening 2*hmax (the coefficients at the UNKNOWN
    center c' in the box — the derivative penalty, first order in h),
    C4 from the full-region widening 2*hmax + r (the Lagrange
    remainder over box + ball).  Same certificate shape as the
    corpus's tight mode (patch_at: tight coefficients + widened C4),
    generalized from hmax=0 to hmax>0."""
    wc, xc, yc = 0.5 * (wlo + whi), 0.5 * (xlo + xhi), 0.5 * (ylo + yhi)
    hmax = 0.5 * max(whi - wlo, xhi - xlo, yhi - ylo)
    center = (wc, xc, yc, wc, -xc, yc)
    best = None
    for (ve, vo) in vecs:
        for side, v in (("o", vo), ("e", ve)):
            if v is None:
                continue
            Rb, errb = pipeline(center, v, side, box_r=2.0 * hmax)
            if Rb is None:
                continue
            m0 = Rb.c[0] - LAMBDA
            if not ((m0 > 0) and (not m0.overlaps(arb(0)))):
                continue
            gamma, kap, C3 = extract(Rb)
            lo, hi = 1e-4, min(R_CAP, 0.12)
            for _ in range(niter):
                mid = 0.5 * (lo + hi)
                Rbig, _ = pipeline(center, v, side,
                                   box_r=2.0 * hmax + mid)
                if Rbig is None:
                    hi = mid
                    continue
                C4 = sum(up(Rbig.c[i]) for i in BY_DEG[4])
                if phi_ok(m0, gamma, kap, C3, C4, mid):
                    lo = mid
                else:
                    hi = mid
            r_ok = lo if lo > 1e-4 else None
            if r_ok is not None and (best is None or r_ok > best[0]):
                best = (r_ok, side, "dpp")
    return best


def stratum_vecs_probe(wc, xc, yc):
    center = (wc, xc, yc, wc, -xc, yc)
    out = []
    try:
        lam_e, lam_o, v_e, v_o = ns_tp["evecs_at"](center)
        out.append((v_e, v_o))
    except Exception:
        pass
    return out


print("\nP-1/P-2  the patch instruments on sample stratum boxes:")
samples = [
    (W_STAR - 0.025, W_STAR + 0.025, 0.0, 0.05, Y_STAR - 0.025,
     Y_STAR + 0.025),
    (W_STAR - 0.025, W_STAR + 0.025, 0.05, 0.10, Y_STAR - 0.025,
     Y_STAR + 0.025),
    (W_STAR - 0.025, W_STAR + 0.025, 0.10, 0.15, Y_STAR - 0.025,
     Y_STAR + 0.025),
    (W_STAR - 0.05, W_STAR + 0.05, 0.0, 0.10, Y_STAR - 0.05,
     Y_STAR + 0.05),
    (W_STAR - 0.05, W_STAR + 0.05, 0.05, 0.15, Y_STAR + 0.0,
     Y_STAR + 0.10),
    (W_STAR - 0.05, W_STAR + 0.05, 0.10, 0.20, Y_STAR - 0.10,
     Y_STAR + 0.00),
]
t_old = t_dpp = 0.0
for (a, b, c, d, e, f) in samples:
    wc, xc, yc = 0.5 * (a + b), 0.5 * (c + d), 0.5 * (e + f)
    vecs = stratum_vecs_probe(wc, xc, yc)
    if not vecs:
        print("  box (%.3f,%.3f)x(%.3f,%.3f)x(%.3f,%.3f): no vecs"
              % (a, b, c, d, e, f))
        continue
    t1 = time.time()
    ro = patch_box_old(a, b, c, d, e, f, vecs)
    t2 = time.time()
    rd = patch_box_dpp(a, b, c, d, e, f, vecs)
    t3 = time.time()
    t_old += t2 - t1
    t_dpp += t3 - t2
    print("  box (%.3f,%.3f)x(%.3f,%.3f)x(%.3f,%.3f): old r = %s; "
          "DPP r = %s  [gain %s]"
          % (a, b, c, d, e, f,
             ("%.4f" % ro[0]) if ro else "None",
             ("%.4f" % rd[0]) if rd else "None",
             ("%.1fx" % (rd[0] / ro[0])) if (ro and rd) else "-"))
print("  timing: old %.2fs / DPP %.2fs per %d boxes"
      % (t_old, t_dpp, len(samples)))

# ============================== P-6: the BDC on the live frontier
def ivl_mag(lo, hi):
    return max(abs(lo), abs(hi))


def bdc_bounds(bx1, by1, bx2, by2, bp1, bp2):
    """the three BDC lower bounds as floats (sound: interval endpoint
    arithmetic, all inputs exact box endpoints)."""
    def sq_mag(lo, hi):
        return 0.0 if (lo <= 0 <= hi) else min(lo * lo, hi * hi)
    def sq_max(lo, hi):
        return max(lo * lo, hi * hi)
    # d-intervals over the box (the domain portion: d in (0, d_hi])
    d11_hi = 1.0 - (sq_mag(bx1[0], bx1[1]) + sq_mag(by1[0], by1[1]))
    d22_hi = 1.0 - (sq_mag(bx2[0], bx2[1]) + sq_mag(by2[0], by2[1]))
    d11_lo = 1.0 - (sq_max(bx1[0], bx1[1]) + sq_max(by1[0], by1[1]))
    d22_lo = 1.0 - (sq_max(bx2[0], bx2[1]) + sq_max(by2[0], by2[1]))
    d12_hi = 1.0 - min(bx1[0] * bx2[0], bx1[1] * bx2[1]) \
        - min(by1[0] * by2[0], by1[1] * by2[1])
    # e0 (any box)
    b_e0 = 2.0 - 4.0 * ivl_mag(bx1[0], bx1[1]) * ivl_mag(by1[0], by1[1]) \
        * ivl_mag(bp1[0], bp1[1]) \
        - 4.0 * ivl_mag(bx2[0], bx2[1]) * ivl_mag(by2[0], by2[1]) \
        * ivl_mag(bp2[0], bp2[1])
    # e4 / e5 (sign-definite p, same-sign product for the cross term)
    b_e4 = b_e5 = None
    p1sd = bp1[0] > 0 or bp1[1] < 0
    p2sd = bp2[0] > 0 or bp2[1] < 0
    same = ((bp1[0] > 0 and bp2[0] > 0)
            or (bp1[1] < 0 and bp2[1] < 0))
    if p1sd and p2sd and same and d11_hi > 0 and d22_hi > 0 \
            and d12_hi > 0:
        p1min = min(abs(bp1[0]), abs(bp1[1]))
        p2min = min(abs(bp2[0]), abs(bp2[1]))
        p1max = ivl_mag(bp1[0], bp1[1])
        p2max = ivl_mag(bp2[0], bp2[1])
        T2m = 2.0 * ivl_mag(bx2[0], bx2[1]) * ivl_mag(by2[0], by2[1]) \
            + ivl_mag(by2[0], by2[1]) * ivl_mag(bx1[0], bx1[1]) \
            + ivl_mag(bx2[0], bx2[1]) * ivl_mag(by1[0], by1[1]) \
            + 2.0 * ivl_mag(bx1[0], bx1[1]) * ivl_mag(by1[0], by1[1])
        T1m = 2.0 * ivl_mag(bx1[0], bx1[1]) * ivl_mag(by1[0], by1[1]) \
            + ivl_mag(by1[0], by1[1]) * ivl_mag(bx2[0], bx2[1]) \
            + ivl_mag(bx1[0], bx1[1]) * ivl_mag(by2[0], by2[1]) \
            + 2.0 * ivl_mag(bx2[0], bx2[1]) * ivl_mag(by2[0], by2[1])
        x1y1m = ivl_mag(bx1[0], bx1[1]) * ivl_mag(by1[0], by1[1])
        x2y2m = ivl_mag(bx2[0], bx2[1]) * ivl_mag(by2[0], by2[1])
        b_e4 = p1min ** 2 / d11_hi ** 2 + 2.0 * p1min * p2min / d12_hi ** 2 \
            - 12.0 * p1max * x1y1m - 4.0 * p2max * T2m
        b_e5 = p2min ** 2 / d22_hi ** 2 + 2.0 * p1min * p2min / d12_hi ** 2 \
            - 12.0 * p2max * x2y2m - 4.0 * p1max * T1m
    return b_e0, b_e4, b_e5


ck = json.load(open(SCR + "abelian_cover4d_ckpt.json"))
stack = ck["stack"]
print("\nP-6  the BDC on the live state:")
n_pass_e0 = n_pass_e45 = n_fail = 0
margins = []
for i, e in enumerate(stack):
    if e[6] < 10:      # the untouched root quadrants: skip
        continue
    b_e0, b_e4, b_e5 = bdc_bounds(e[0], e[1], e[2], e[3], e[4], e[5])
    m = None
    if b_e0 is not None and b_e0 > LAMBDA_F:
        n_pass_e0 += 1
        m = b_e0 - LAMBDA_F
    elif b_e4 is not None and b_e4 > LAMBDA_F:
        n_pass_e45 += 1
        m = b_e4 - LAMBDA_F
    elif b_e5 is not None and b_e5 > LAMBDA_F:
        n_pass_e45 += 1
        m = b_e5 - LAMBDA_F
    else:
        n_fail += 1
        best = max(x for x in (b_e0, b_e4, b_e5) if x is not None)
        m = best - LAMBDA_F
    margins.append(m)
print("  the 43 deep frontier branches: e0-pass %d, e4/e5-pass %d, "
      "fail %d; the worst bound margin %+.3e"
      % (n_pass_e0, n_pass_e45, n_fail, min(margins)))

st = ck["b_stalls"]
n_pass_e0 = n_pass_e45 = n_fail = 0
margins = []
for s in st[:500]:
    b_e0, b_e4, b_e5 = bdc_bounds(s[0], s[1], s[2], s[3], s[4], s[5])
    if b_e0 is not None and b_e0 > LAMBDA_F:
        n_pass_e0 += 1
        margins.append(b_e0 - LAMBDA_F)
    elif b_e4 is not None and b_e4 > LAMBDA_F:
        n_pass_e45 += 1
        margins.append(b_e4 - LAMBDA_F)
    elif b_e5 is not None and b_e5 > LAMBDA_F:
        n_pass_e45 += 1
        margins.append(b_e5 - LAMBDA_F)
    else:
        n_fail += 1
        margins.append(0.0)
print("  the 500 recorded stall boxes: e0-pass %d, e4/e5-pass %d, "
      "fail %d" % (n_pass_e0, n_pass_e45, n_fail))

# random far-field boxes: the e0's small-p coverage rate
n_e0 = 0
for _ in range(400):
    bx1 = tuple(sorted(rng.uniform(-0.9, 0.9, 2)))
    by1 = tuple(sorted(rng.uniform(-0.9, 0.9, 2)))
    bx2 = tuple(sorted(rng.uniform(-0.9, 0.9, 2)))
    by2 = tuple(sorted(rng.uniform(-0.9, 0.9, 2)))
    hw = 0.5 * (bx1[1] - bx1[0])
    bp1 = tuple(sorted(rng.uniform(-0.2, 0.2, 2)))
    bp2 = tuple(sorted(rng.uniform(-0.2, 0.2, 2)))
    b_e0, _, _ = bdc_bounds(bx1, by1, bx2, by2, bp1, bp2)
    if b_e0 > LAMBDA_F:
        n_e0 += 1
print("  random small-|p| boxes (|p|<=0.2, w~%.2f): the e0 pass rate "
      "%d/400" % (0.2, n_e0))
print("\nprobe done")
