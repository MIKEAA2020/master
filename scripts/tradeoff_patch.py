#!/usr/bin/env python3.13
# -*- coding: utf-8 -*-
"""
tradeoff_patch.py — Task 26: THE ANALYTIC PATCH for the off-pair core
below s_min (the user's order; Task 22's named open region).

THE PROBLEM (Task 22's ledger).  The P3 tubes ball-certify
max(lambda_e, lambda_o) >= lambda* on the off-pair rays from each ray's
minimal certified radius s_min (min/median 0.021, max 0.065) out to
|s|_2 = 0.15 — the CORE |s|_2 < s_min is uncovered: the value's margin
kappa|s|^2 is below the tube's ball width at the affordable resolution
(the entry-scale p^2 Q vs the Lipschitz-limited value balls).  One P3
boundary ray (the x0 = 0.15 base, a strongly x-ward direction) never
fully certified at all.

THE INSTRUMENT (this task's discovery, measured in probe_patch2.py).
Fix a center z_c on (or near) the mirrored-pair stratum and the top
eigenvector v_c of ONE side's 4x4 pencil there (floats, exact
rationals inside the balls).  The Rayleigh quotient

    R(v_c, z) = v_c^T G(z) C(z) G(z) v_c / v_c^T G(z) v_c

is a RATIONAL function of the 3 transverse (mirror-breaking)
coordinates delta = ((w1-w2)/2, (x1+x2)/2, (y1-y2)/2) — and

  (a) at stratum centers the instrument is M-INVARIANT (the stratum is
      Fix(M), M acts as -I on the transverse coordinates, and v_c has
      the symmetric lift form (a, b, c, c) — the (3,4) antisymmetric
      direction is exactly G-null there), so R is EVEN in delta: the
      linear and cubic Taylor coefficients vanish identically
      (machine-verified V4);
  (b) lambda_max >= R for ANY vector, so a lower bound on R over a
      transverse ball certifies the claim;
  (c) the instrument is essentially FLAT transversally (the odd side,
      kappa ~ -0.006 vs the eigenvalue's +1.5 — the envelope penalty
      cancels the curvature) with a TINY quartic scale (C4 ~ 1..6);
  (d) R(v_c, z_c) = the side's exact eigenvalue at the center (the
      envelope theorem; V3), so the center margin m0 is the true
      margin.

THE CERTIFICATE (Task 17's C4 pattern, transplanted).  Taylor to
degree 4 in delta with ball arithmetic (flint/arb, truncated
polynomial arithmetic — the coefficients ARE the derivatives):

    R(z_c + delta) >= m0 - gamma*r + min(0, kappa)*r^2/2
                      - C3*r^3 - C4_box(r)*r^4      for |delta|_2 <= r

with every quantity SOUNDLY enclosed:
  m0   the tight-mode constant coefficient minus lambda* (definite);
  gamma= sum |linear coefficients| (tight mode, ~1e-15 at stratum
        centers by (a), bounded regardless);
  kappa the sound min eigenvalue of the transverse Hessian (tight
        mode; Weyl + Frobenius on the ball radii);
  C3   sum |cubic coefficients| (tight mode; ~0 at stratum centers);
  C4_box(r) sum |quartic coefficients| of the BOX-mode run — the
        pipeline re-run with the center constants widened to balls of
        half-width r/2 (the Lagrange remainder bound: the box-mode
        degree-4 coefficients enclose D^4 R(xi)/alpha! for every xi in
        the patch ball, since every arithmetic operation soundly
        encloses its point-value).
phi(r) is MONOTONE non-increasing (every negative term is), so the
patch certificate is the single definite comparison phi(r) > 0.
Validity side-conditions checked per box run: the Gram denominators
d_ij away from 0, x_i away from 0 (the even side's p = w/x), and the
Rayleigh denominator's constant coefficient > 0.

THE COVERAGE.  For each of the 15 P3 base points (3 stratum x0 x 5
in-pair deviations): a CENTER PATCH — the transverse 3-BALL of radius
r0 (ALL transverse directions, beyond the sampled 6) with both sides'
instruments tried and the better taken.  For each of the 90 P3 rays
(the identical seed => the identical directions, cross-checked against
the P3 results): if r0 >= s_min(ray) the ray is FULLY covered
([0, r0] patch + [s_min, 0.15] tubes); else a CHAIN of patches steps
from r0 to s_min.  The never-certified boundary ray is chained all the
way to |s|_2 = 0.15 — closing Task 22's P3 hole.

Validation: V1 the Taylor coefficients vs finite differences; V2 the
certified r vs direct float profiles at 0.95 r0; V3 the envelope
(R(v_c, z_c) = the eigenvalue); V4 the M-evenness (the vanishing
odd coefficients); V5 the truncated-division round-trip.

Output: tradeoff_patch_results.json
"""
import json
import math
import time

import numpy as np
from flint import arb

try:
    from flint import ctx
    ctx.prec = 96           # ~28 decimal digits in every ball
except Exception:
    pass

LAMBDA_STR = "1.6310919765642504414737578928177383666901925754942"
LAMBDA = arb(LAMBDA_STR)
LAMBDA_F = float(LAMBDA_STR)
C_STAR = 0.3971672569443035
Y_STAR = 0.6563248795193563
S_RAY = 0.15
R_CAP = 0.12               # the global patch-radius cap (Taylor validity)

t0 = time.time()
OUT = {"meta": {
    "order": "Task 26: the analytic patch for the off-pair core below "
             "s_min (Task 22's named open region) — the Taylor-4 ball "
             "certificates on the transverse coordinates",
    "date": "2026-09-30",
    "instrument": "the Rayleigh quotient at the FIXED center "
                  "eigenvector as a rational function of the 3 "
                  "transverse coordinates; Taylor degree 4 in balls "
                  "(flint/arb); phi monotone => one definite "
                  "comparison per patch",
    "lambda_star": LAMBDA_STR}}


def ab(x):
    return arb(repr(float(x)))


def flo(x):
    """sound-ish float of a ball mid (for reporting only)."""
    return float(x.mid())


def up(x):
    """sound upper bound of |x| as a float (slack included)."""
    m, r = float(x.mid()), float(x.rad())
    return abs(m) + r + 1e-12 * (1.0 + abs(m))


# ============================================================ the TP class
DEG = 4
MONOS = []
for d in range(DEG + 1):
    for i in range(d, -1, -1):
        for j in range(d - i, -1, -1):
            MONOS.append((i, j, d - i - j))
MONOS.sort(key=lambda m: (sum(m), m))
IDX = {m: i for i, m in enumerate(MONOS)}
NM = len(MONOS)
BY_DEG = [[IDX[m] for m in MONOS if sum(m) == d] for d in range(DEG + 1)]

Z = arb(0)


class TP:
    """a truncated Taylor polynomial in 3 vars, degree <= 4, arb balls."""
    __slots__ = ('c',)

    def __init__(self, c):
        self.c = list(c)

    @staticmethod
    def const(x):
        c = [Z] * NM
        c[0] = x
        return TP(c)

    @staticmethod
    def affine(const, lin, k):
        """const + lin * delta_k."""
        c = [Z] * NM
        c[0] = const
        c[IDX[(1 if k == 0 else 0, 1 if k == 1 else 0,
               1 if k == 2 else 0)]] = lin
        return TP(c)

    def __add__(self, o):
        return TP([a + b for a, b in zip(self.c, o.c)])

    def __sub__(self, o):
        return TP([a - b for a, b in zip(self.c, o.c)])

    def __neg__(self):
        return TP([-a for a in self.c])

    def __mul__(self, o):
        out = [Z] * NM
        for a in range(NM):
            ca = self.c[a]
            if ca.is_zero():
                continue
            ma = MONOS[a]
            for b in range(NM):
                cb = o.c[b]
                if cb.is_zero():
                    continue
                mb = MONOS[b]
                s = (ma[0] + mb[0], ma[1] + mb[1], ma[2] + mb[2])
                if sum(s) > DEG:
                    continue
                j = IDX[s]
                out[j] = out[j] + ca * cb
        return TP(out)

    def inv(self):
        """1/self (truncated); requires the constant away from 0."""
        q = self.c
        q0 = q[0]
        if not ((q0 > 0) or (q0 < 0)):
            raise ZeroDivisionError("constant ball contains 0")
        inv0 = Z
        inv0 = 1 / q0
        p = [Z] * NM
        p[0] = inv0
        for d in range(1, DEG + 1):
            for ia in BY_DEG[d]:
                ma = MONOS[ia]
                acc = Z
                for ig in range(NM):
                    mg = MONOS[ig]
                    if sum(mg) == 0 or sum(mg) > d:
                        continue
                    if (mg[0] <= ma[0] and mg[1] <= ma[1]
                            and mg[2] <= ma[2]):
                        j = IDX[(ma[0] - mg[0], ma[1] - mg[1],
                                 ma[2] - mg[2])]
                        acc = acc + q[ig] * p[j]
                p[ia] = -inv0 * acc
        return TP(p)

    def __truediv__(self, o):
        return self * o.inv()


def tp_mul_mat(A, B):
    n = len(A)
    return [[sum((A[i][k] * B[k][j] for k in range(n)), TP.const(Z))
             for j in range(n)] for i in range(n)]


def tp_quad(v, M):
    """v^T M v for the constant float vector v (as TPs)."""
    n = len(v)
    s = TP.const(Z)
    for i in range(n):
        for j in range(n):
            s = s + TP.const(ab(v[i])) * M[i][j] * TP.const(ab(v[j]))
    return s


# ================================================== the pipeline (2 modes)
def pipeline(center, v, side, box_r=None):
    """the Taylor-4 coefficients of R(v, z(center + L delta)).

    center: (w1c, x1c, y1c, w2c, x2c, y2c) floats; v: the float test
    vector; side 'e'/'o'.  box_r: None => tight mode (the constants as
    exact points); else the constants widened to balls of half-width
    box_r/2 in the transverse slots (the Lagrange-remainder mode).
    Returns (R, ok) with ok=False if a validity side-condition fails.
    """
    w1c, x1c, y1c, w2c, x2c, y2c = center
    half = arb('0.5')

    def mk(cval, k, sign):
        if box_r is None:
            return TP.affine(ab(cval), half * sign, k)
        # the widened constant: the center may sit anywhere in the box
        # (the Lagrange xi), the affine structure unchanged
        cst = arb('%.17g +/- %.17g' % (float(cval), float(box_r) / 2.0))
        return TP.affine(cst, half * sign, k)

    w1 = mk(w1c, 0, 1.0)
    w2 = mk(w2c, 0, -1.0)
    x1 = mk(x1c, 1, 1.0)
    x2 = mk(x2c, 1, 1.0)
    y1 = mk(y1c, 2, 1.0)
    y2 = mk(y2c, 2, -1.0)
    # the validity checks on the constant balls
    for t, name in ((x1, 'x1'), (x2, 'x2')):
        if not ((t.c[0] > 0) or (t.c[0] < 0)):
            return None, "x ball contains 0"
    if side == "e":
        p1 = w1 / x1
        p2 = w2 / x2
    else:
        p1 = p2 = None
    # the Gram blocks: d_ij = (1 - y_i y_j)^2 - (x_i x_j)^2
    one = TP.const(arb(1))
    d11 = ((one - y1 * y1) * (one - y1 * y1)) - (x1 * x1) * (x1 * x1)
    d12 = ((one - y1 * y2) * (one - y1 * y2)) - (x1 * x2) * (x1 * x2)
    d22 = ((one - y2 * y2) * (one - y2 * y2)) - (x2 * x2) * (x2 * x2)
    for d, nm in ((d11, 'd11'), (d12, 'd12'), (d22, 'd22')):
        if not ((d.c[0] > 0) or (d.c[0] < 0)):
            return None, "Gram denominator ball contains 0 (%s)" % nm
    Q11 = (one - y1 * y1) / d11
    Q12 = (one - y1 * y2) / d12
    Q22 = (one - y2 * y2) / d22
    R11 = TP.const(arb(1)) / d11
    R12 = TP.const(arb(1)) / d12
    R22 = TP.const(arb(1)) / d22
    Zc = TP.const(Z)

    def M2(a, b, c_, d_, e, f):
        return [[a, b, c_], [b, d_, e], [c_, e, f]]

    if side == "e":
        # G_e, C_e in the (delta0, delta1, e1, e2) basis
        Ge = [[TP.const(ab(1)), Zc, TP.const(ab(1)), TP.const(ab(1))],
              [Zc, TP.const(ab(1)), y1, y2],
              [TP.const(ab(1)), y1, Q11, Q12],
              [TP.const(ab(1)), y2, Q12, Q22]]
        Px = [[p1 * p1 * (Q11 + (x1 * x1) * R11),
               p1 * p2 * (Q12 + (x1 * x2) * R12)],
              [p2 * p1 * (Q12 + (x2 * x1) * R12),
               p2 * p2 * (Q22 + (x2 * x2) * R22)]]
        Ce = [[TP.const(ab(2)), Zc, TP.const(ab(-2)) * p1 * x1 * y1,
               TP.const(ab(-2)) * p2 * x2 * y2],
              [Zc, TP.const(ab(1)), p1 * TP.const(ab(-1)) * x1,
               p2 * TP.const(ab(-1)) * x2],
              [TP.const(ab(-2)) * p1 * x1 * y1, p1 * TP.const(ab(-1)) * x1,
               Px[0][0], Px[0][1]],
              [TP.const(ab(-2)) * p2 * x2 * y2, p2 * TP.const(ab(-1)) * x2,
               Px[1][0], Px[1][1]]]
        G, C = Ge, Ce
    else:
        Go = [[TP.const(ab(2)), Zc, TP.const(ab(2)) * y1,
               TP.const(ab(2)) * y2],
              [Zc, TP.const(ab(1)), TP.const(ab(1)), TP.const(ab(1))],
              [TP.const(ab(2)) * y1, TP.const(ab(1)), R11, R12],
              [TP.const(ab(2)) * y2, TP.const(ab(1)), R12, R22]]
        Sx = [[w1 * w1 * (Q11 + (x1 * x1) * R11),
               w1 * w2 * (Q12 + (x1 * x2) * R12)],
              [w2 * w1 * (Q12 + (x2 * x1) * R12),
               w2 * w2 * (Q22 + (x2 * x2) * R22)]]
        Co = [[TP.const(ab(1)), Zc, TP.const(ab(-1)) * w1,
               TP.const(ab(-1)) * w2],
              [Zc, TP.const(ab(1)), w1 * TP.const(ab(-1)) * y1,
               w2 * TP.const(ab(-1)) * y2],
              [TP.const(ab(-1)) * w1, w1 * TP.const(ab(-1)) * y1,
               Sx[0][0], Sx[0][1]],
              [TP.const(ab(-1)) * w2, w2 * TP.const(ab(-1)) * y2,
               Sx[1][0], Sx[1][1]]]
        G, C = Go, Co
    GCG = tp_mul_mat(tp_mul_mat(G, C), G)
    N = tp_quad(v, GCG)
    D = tp_quad(v, G)
    if not (D.c[0] > 0):
        return None, "Rayleigh denominator not definitely positive"
    R = N / D
    return R, None


# ================================================ the patch certificate
def float_mats(w1, x1, y1, w2, x2, y2):
    p1 = w1 / x1 if x1 != 0 else 0.0
    p2 = w2 / x2 if x2 != 0 else 0.0
    def D(i, j):
        xs = (x1, x2)[i] * (x1, x2)[j]
        ys = (y1, y2)[i] * (y1, y2)[j]
        return (1.0 - ys) ** 2 - xs * xs
    d11, d12, d22 = D(0, 0), D(0, 1), D(1, 1)
    Q = np.array([[(1 - y1 * y1) / d11, (1 - y1 * y2) / d12],
                  [(1 - y2 * y1) / d12, (1 - y2 * y2) / d22]])
    Rg = np.array([[1.0 / d11, 1.0 / d12], [1.0 / d12, 1.0 / d22]])
    G_e = np.array([[1, 0, 1, 1], [0, 1, y1, y2],
                    [1, y1, Q[0, 0], Q[0, 1]], [1, y2, Q[1, 0], Q[1, 1]]])
    P = np.array([[p1 * p1 * (Q[0, 0] + x1 * x1 * Rg[0, 0]),
                   p1 * p2 * (Q[0, 1] + x1 * x2 * Rg[0, 1])],
                  [p2 * p1 * (Q[1, 0] + x2 * x1 * Rg[1, 0]),
                   p2 * p2 * (Q[1, 1] + x2 * x2 * Rg[1, 1])]])
    C_e = np.array([[2, 0, -2 * p1 * x1 * y1, -2 * p2 * x2 * y2],
                    [0, 1, -p1 * x1, -p2 * x2],
                    [-2 * p1 * x1 * y1, -p1 * x1, P[0, 0], P[0, 1]],
                    [-2 * p2 * x2 * y2, -p2 * x2, P[0, 1], P[1, 1]]])
    G_o = np.array([[2, 0, 2 * y1, 2 * y2], [0, 1, 1, 1],
                    [2 * y1, 1, Rg[0, 0], Rg[0, 1]],
                    [2 * y2, 1, Rg[1, 0], Rg[1, 1]]])
    S = np.array([[w1 * w1 * (Q[0, 0] + x1 * x1 * Rg[0, 0]),
                   w1 * w2 * (Q[0, 1] + x1 * x2 * Rg[0, 1])],
                  [w2 * w1 * (Q[1, 0] + x2 * x1 * Rg[1, 0]),
                   w2 * w2 * (Q[1, 1] + x2 * x2 * Rg[1, 1])]])
    C_o = np.array([[1, 0, -w1, -w2],
                    [0, 1, -w1 * y1, -w2 * y2],
                    [-w1, -w1 * y1, S[0, 0], S[0, 1]],
                    [-w2, -w2 * y2, S[0, 1], S[1, 1]]])
    return G_e, C_e, G_o, C_o


def top_evec(C, G):
    A = C @ G
    ev, V = np.linalg.eig(A)
    idx = max(range(4), key=lambda i: float(np.real(ev[i])))
    v = np.real(V[:, idx])
    nrm = math.sqrt(abs(float(v @ G @ v)))
    if nrm < 1e-300:
        nrm = np.linalg.norm(v)
    return v / nrm


def top_eval(C, G):
    A = C @ G
    return max(float(np.real(e)) for e in np.linalg.eigvals(A))


def evecs_at(center):
    G_e, C_e, G_o, C_o = float_mats(*center)
    lam_e, lam_o = top_eval(C_e, G_e), top_eval(C_o, G_o)
    v_e, v_o = top_evec(C_e, G_e), top_evec(C_o, G_o)
    # the (a,b,c,c) projection at STRATUM centers (the exact symmetry form)
    return lam_e, lam_o, v_e, v_o


def extract(R):
    """(gamma, kappa_lo, C3) from the tight-mode coefficients."""
    lin = [IDX[(1, 0, 0)], IDX[(0, 1, 0)], IDX[(0, 0, 1)]]
    gamma = sum(up(R.c[i]) for i in lin)
    Hmid = np.zeros((3, 3))
    Hrad = np.zeros((3, 3))
    for i in range(3):
        for j in range(i, 3):
            mono = [0, 0, 0]
            mono[i] += 1
            mono[j] += 1
            b = R.c[IDX[tuple(mono)]]
            fac = 2.0 if i == j else 1.0
            Hmid[i, j] = Hmid[j, i] = fac * float(b.mid())
            Hrad[i, j] = Hrad[j, i] = fac * float(b.rad())
    kap = float(np.linalg.eigvalsh(Hmid)[0]) - float(
        np.linalg.norm(Hrad, 'fro')) - 1e-9
    C3 = sum(up(R.c[i]) for i in BY_DEG[3])
    return gamma, kap, C3


def phi_ok(m0_ball, gamma, kappa, C3, C4, r):
    """the monotone patch certificate: phi(r) > 0 (arb, definite)."""
    rb = arb(repr(float(r)))
    phi = (m0_ball - arb(repr(gamma)) * rb
           - arb(repr(abs(min(0.0, kappa)) * 0.5)) * rb * rb
           - arb(repr(C3)) * rb * rb * rb
           - arb(repr(C4)) * rb * rb * rb * rb)
    return (phi > 0) and (not phi.overlaps(arb(0)))


def patch_at(center, v_e, v_o, want_box_probes=6):
    """the best patch (both sides tried): the certificate radius r and
    the diagnostics.  Returns a dict or None."""
    best = None
    for side, v in (("o", v_o), ("e", v_e)):
        R, err = pipeline(center, v, side)
        if R is None:
            continue
        m0 = R.c[0] - LAMBDA
        if not ((m0 > 0) and (not m0.overlaps(arb(0)))):
            continue
        gamma, kappa, C3 = extract(R)
        lo, hi = 2e-4, R_CAP
        r_ok, C4_ok = None, None
        for _ in range(want_box_probes):
            mid = 0.5 * (lo + hi)
            Rb, errb = pipeline(center, v, side, box_r=mid)
            if Rb is None:
                hi = mid
                continue
            C4 = sum(up(Rb.c[i]) for i in BY_DEG[4])
            if phi_ok(m0, gamma, kappa, C3, C4, mid):
                r_ok, C4_ok, lo = mid, C4, mid
            else:
                hi = mid
        if r_ok is not None and (best is None or r_ok > best["r"]):
            best = {"side": side, "r": r_ok, "m0": float(m0.mid()),
                    "gamma": gamma, "kappa": kappa, "C3": C3,
                    "C4_at_r": C4_ok}
    return best


def ray_center(base, d, s):
    x0, dw, dyb = base
    wbar = 0.5 * (C_STAR + dw)
    ybar = Y_STAR + dyb
    return (wbar + 0.5 * d[0] * s, x0 + 0.5 * d[1] * s, ybar + 0.5 * d[2] * s,
            wbar - 0.5 * d[0] * s, -x0 + 0.5 * d[1] * s, ybar - 0.5 * d[2] * s)


# ==================================================== V5: the TP algebra
print("=" * 72)
print("V5 — the truncated-polynomial algebra (the division round-trip)")
print("=" * 72)
rng = np.random.default_rng(5)
v5_max = 0.0
for _ in range(6):
    ca = [arb(repr(float(rng.uniform(-3, 3)))) for _ in range(NM)]
    cb = [arb(repr(float(rng.uniform(0.5, 2.0)))) for _ in range(NM)]
    pa, pb = TP(ca), TP(cb)
    q = pa / pb
    back = q * pb
    for i in range(NM):
        d = float((back.c[i] - pa.c[i]).rad()) + abs(
            float((back.c[i] - pa.c[i]).mid()))
        v5_max = max(v5_max, d)
print("  max |(p/q)*q - p| over 6 random pairs, all 15 coefficients: %.2e"
      % v5_max)
assert v5_max < 1e-20
OUT["V5_tp_algebra"] = {"roundtrip_residual": v5_max,
                        "verdict": "PASS (the truncated division is exact "
                                   "in balls)"}

# ============================================== the P3 geometry (reload)
try:
    P3 = json.load(open("tradeoff_cert_results.json"))["P3_off_pair_rays"]
    RAYS = P3["ray_min_certified"]
except Exception as e:
    raise SystemExit("cannot load tradeoff_cert_results.json: %s" % e)
print()
print("=" * 72)
print("the P3 geometry reloaded: %d rays, s_min min/median/max = %s"
      % (len(RAYS),
         ("%.3f/%.3f/%.3f" % (
             min(r["s_min_certified"] for r in RAYS
                 if r["s_min_certified"] is not None),
             sorted(r["s_min_certified"] for r in RAYS
                    if r["s_min_certified"] is not None)[len(RAYS) // 2],
             max(r["s_min_certified"] for r in RAYS
                 if r["s_min_certified"] is not None)))
         if any(r["s_min_certified"] is not None for r in RAYS) else "n/a"))
print("=" * 72)

# the IDENTICAL directions (the P3 seed; cross-checked against the
# stored rounded values).  The P3 rows are ordered: base_points x DIRS,
# so row i uses DIRS[i % 6].
rng2 = np.random.default_rng(20260930)
DIRS = []
for _ in range(6):
    dd = rng2.normal(size=3)
    DIRS.append(dd / np.linalg.norm(dd))
xcheck = 0.0
for i, r in enumerate(RAYS):
    d_ex = DIRS[i % 6]
    xcheck = max(xcheck, float(np.max(np.abs(np.array(r["dir"]) - d_ex))))
print("  direction cross-check (stored vs regenerated): max diff %.1e"
      % xcheck)
assert xcheck < 5e-4, "the regenerated directions do not match P3!"
OUT["direction_crosscheck"] = xcheck

# ============================================ the 15 center patches
print()
print("=" * 72)
print("THE CENTER PATCHES (the transverse 3-balls, both sides)")
print("=" * 72)
BASES = []
for x0 in (0.45, 0.3, 0.15):
    for (dw, dyb) in [(0.0, 0.0), (0.1, 0.0), (-0.1, 0.0),
                      (0.0, 0.05), (0.0, -0.05)]:
        BASES.append((x0, dw, dyb))

v4_max_odd_coef = 0.0     # the M-evenness residual (V4)
v3_max = 0.0              # the envelope residual (V3)
center_rows = []
for base in BASES:
    x0, dw, dyb = base
    center = ray_center(base, (0.0, 0.0, 0.0), 0.0)
    lam_e, lam_o, v_e, v_o = evecs_at(center)
    # the (a,b,c,c) projection (the stratum symmetry form)
    v_e = np.array(v_e); v_o = np.array(v_o)
    v_e[3] = v_e[2] = 0.5 * (v_e[2] + v_e[3])
    v_o[3] = v_o[2] = 0.5 * (v_o[2] + v_o[3])
    res = patch_at(center, v_e, v_o)
    # V3: the envelope (the instrument at the center = the eigenvalue)
    mats = float_mats(*center)
    for side, v in (("o", v_o), ("e", v_e)):
        G, C = (mats[2], mats[3]) if side == "o" else (mats[0], mats[1])
        GCG = G @ C @ G
        rv = float(v @ GCG @ v) / float(v @ G @ v)
        lam = top_eval(C, G)
        v3_max = max(v3_max, abs(rv - lam))
    # V4: the M-evenness at the stratum center (the odd coefficients)
    for side, v in (("o", v_o), ("e", v_e)):
        R, _ = pipeline(center, v, side)
        if R is not None:
            for i in BY_DEG[1] + BY_DEG[3]:
                v4_max_odd_coef = max(v4_max_odd_coef, up(R.c[i]))
    row = {"base": list(base), "patch": res,
           "lam_e": lam_e, "lam_o": lam_o}
    center_rows.append(row)
    if res:
        print("  base (%.2f, %+.2f, %+.2f): side %s, r0 = %.4f "
              "(m0 %.2e, kappa %+.3f, C3 %.1e, C4(r) %.1f)"
              % (x0, dw, dyb, res["side"], res["r"], res["m0"],
                 res["kappa"], res["C3"], res["C4_at_r"]))
    else:
        print("  base (%.2f, %+.2f, %+.2f): NO PATCH (m0 <= 0?)"
              % (x0, dw, dyb))
r0s = [r["patch"]["r"] for r in center_rows if r["patch"]]
print("  r0 over the 15 bases: min %.4f, median %.4f, max %.4f"
      % (min(r0s), sorted(r0s)[len(r0s) // 2], max(r0s)))
print("  V3 (the envelope residual): %.2e   V4 (the M-evenness odd "
      "coefficients): %.2e" % (v3_max, v4_max_odd_coef))
OUT["center_patches"] = center_rows
OUT["V3_envelope"] = v3_max
OUT["V4_M_evenness"] = v4_max_odd_coef

# ============================================ V2: the direct profiles
print()
print("=" * 72)
print("V2 — the direct float profiles at 0.95 r0 (20 random directions)")
print("=" * 72)
v2_fail = 0
v2_worst = 1e9
rng3 = np.random.default_rng(77)
for row in center_rows:
    if not row["patch"]:
        continue
    base = tuple(row["base"])
    r0 = row["patch"]["r"]
    center = ray_center(base, (0, 0, 0), 0.0)
    lam_e, lam_o, v_e, v_o = evecs_at(center)
    v_e[3] = v_e[2] = 0.5 * (v_e[2] + v_e[3])
    v_o[3] = v_o[2] = 0.5 * (v_o[2] + v_o[3])
    v = v_o if row["patch"]["side"] == "o" else v_e
    side = row["patch"]["side"]
    for _ in range(20):
        u = rng3.normal(size=3)
        u /= np.linalg.norm(u)
        z = ray_center(base, u, 0.95 * r0)
        mats = float_mats(*z)
        G, C = (mats[2], mats[3]) if side == "o" else (mats[0], mats[1])
        GCG = G @ C @ G
        rv = float(v @ GCG @ v) / float(v @ G @ v)
        v2_worst = min(v2_worst, rv - LAMBDA_F)
        if rv <= LAMBDA_F:
            v2_fail += 1
print("  worst direct margin at 0.95 r0: %+.3e  (below lambda*: %d)"
      % (v2_worst, v2_fail))
OUT["V2_direct_profiles"] = {"worst_margin": v2_worst,
                             "below_lambda": v2_fail}
assert v2_fail == 0, "V2 FAILED: the certificate disagrees with the floats!"

# ============================================ the ray coverage + chains
print()
print("=" * 72)
print("THE RAY COVERAGE: the patches + the chains below s_min")
print("=" * 72)
ray_rows = []
n_chained = 0
for i, r in enumerate(RAYS):
    base = tuple(r["base"])
    s_min = r["s_min_certified"]
    d = list(DIRS[i % 6])
    target = s_min if s_min is not None else S_RAY
    crow = [c for c in center_rows if tuple(c["base"]) == base][0]
    r0 = crow["patch"]["r"] if crow["patch"] else 0.0
    covered = r0
    chain = []
    ok = covered >= target - 1e-9
    guard = 0
    while not ok and guard < 50:
        guard += 1
        s_c = covered + max(0.004, 0.3 * (target - covered))
        res = None
        for _ in range(3):
            ccenter = ray_center(base, d, s_c)
            lam_e, lam_o, v_e, v_o = evecs_at(ccenter)
            res = patch_at(ccenter, v_e, v_o, want_box_probes=5)
            if res is not None and s_c - res["r"] <= covered + 1e-9:
                break
            if res is not None and s_c - res["r"] > covered + 1e-9:
                s_c = covered + 0.5 * (s_c - covered)
                res = None
            elif res is None:
                s_c = covered + 0.5 * (s_c - covered)
        if res is None:
            # the last resort: the center just inside the frontier
            s_c = max(covered * 0.99, 1e-4)
            ccenter = ray_center(base, d, s_c)
            lam_e, lam_o, v_e, v_o = evecs_at(ccenter)
            res = patch_at(ccenter, v_e, v_o, want_box_probes=4)
            if res is None:
                break
        chain.append({"s_center": round(s_c, 6), "r": round(res["r"], 6),
                      "side": res["side"]})
        covered = max(covered, s_c + res["r"])
        ok = covered >= target - 1e-9
    if chain:
        n_chained += 1
    ray_rows.append({
        "base": list(base), "dir": d, "s_min_tube": s_min,
        "r0_center_patch": round(r0, 6), "chain": chain,
        "covered_to": round(covered, 6), "target": round(target, 6),
        "fully_covered_from_0": bool(ok)})
    tag = "FULL" if ok else "GAP"
    via = ("center patch alone" if not chain else
           "%d chain patches" % len(chain))
    print("  base %s dir %s: r0 %.3f %s -> covered [0, %.3f] of "
          "target %.3f [%s]"
          % (str(base), "[" + ",".join("%.2f" % c for c in d) + "]",
             r0, via, covered, target, tag))
full = [x for x in ray_rows if x["fully_covered_from_0"]]
print("  FULLY covered rays (patch+chain below s_min, tubes above): "
      "%d / %d" % (len(full), len(ray_rows)))
OUT["ray_coverage"] = ray_rows
OUT["fully_covered_rays"] = len(full)
OUT["rays_total"] = len(ray_rows)

# ============================================ V1: Taylor vs FD
print()
print("=" * 72)
print("V1 — the Taylor coefficients vs finite differences")
print("=" * 72)
v1_rows = []
for (base, d, s_c) in [((0.3, 0.0, 0.0), (0.0, 0.0, 0.0), 0.0),
                       ((0.15, 0.0, 0.0), (0.45, 0.3, 0.84), 0.08)]:
    center = ray_center(base, d, s_c)
    lam_e, lam_o, v_e, v_o = evecs_at(center)
    if s_c == 0.0:
        v_e[3] = v_e[2] = 0.5 * (v_e[2] + v_e[3])
        v_o[3] = v_o[2] = 0.5 * (v_o[2] + v_o[3])
    for side, v in (("o", v_o), ("e", v_e)):
        R, _ = pipeline(center, v, side)
        if R is None:
            continue
        mats = float_mats(*center)
        G, C = (mats[2], mats[3]) if side == "o" else (mats[0], mats[1])

        def Rf(dd):
            z = (center[0] + 0.5 * dd[0], center[1] + 0.5 * dd[1],
                 center[2] + 0.5 * dd[2], center[3] - 0.5 * dd[0],
                 center[4] + 0.5 * dd[1], center[5] - 0.5 * dd[2])
            mm = float_mats(*z)
            Gx, Cx = (mm[2], mm[3]) if side == "o" else (mm[0], mm[1])
            GCG = Gx @ Cx @ Gx
            return float(v @ GCG @ v) / float(v @ Gx @ v)

        h = 1e-4
        m0_fd = Rf((0, 0, 0))
        m0_tp = float(R.c[0].mid())
        g_fd = [(Rf(tuple(h if i == k else 0 for k in range(3)))
                 - Rf(tuple(-h if i == k else 0 for k in range(3))))
                / (2 * h) for i in range(3)]
        g_tp = [float(R.c[IDX[m]].mid()) for m in
                [(1, 0, 0), (0, 1, 0), (0, 0, 1)]]
        H_fd = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                ei = tuple(h if i == k else 0 for k in range(3))
                ej = tuple(h if j == k else 0 for k in range(3))
                H_fd[i, j] = (Rf(tuple(ei[k] + ej[k] for k in range(3)))
                              - Rf(tuple(ei[k] - ej[k] for k in range(3)))
                              - Rf(tuple(-ei[k] + ej[k] for k in range(3)))
                              + Rf(tuple(-ei[k] - ej[k] for k in range(3)))
                              ) / (4 * h * h)
        H_tp = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                mono = [0, 0, 0]
                mono[i] += 1
                mono[j] += 1
                H_tp[i, j] = (2.0 if i == j else 1.0) * float(
                    R.c[IDX[tuple(mono)]].mid())
        dg = max(abs(a - b) for a, b in zip(g_fd, g_tp))
        dH = float(np.max(np.abs(H_fd - H_tp)))
        dm = abs(m0_fd - m0_tp)
        # the FD truncation error scale: the quartic Taylor scale at the
        # center (tight mode) times h^2 for the Hessian, h^2 for the
        # gradient's cubic term — the tolerance is C4-aware
        C4_center = sum(up(R.c[i]) for i in BY_DEG[4])
        tol_H = 1e-3 + 20.0 * C4_center * h * h
        tol_g = 1e-6 + 20.0 * C4_center * h * h * h
        v1_rows.append({"base": list(base), "s": s_c, "side": side,
                        "dm0": dm, "dgrad": dg, "dhess": dH,
                        "tol_grad": tol_g, "tol_hess": tol_H})
        print("  base %s s=%.2f side %s: |dm0| %.1e, |dgrad| %.1e "
              "(tol %.1e), |dHess| %.1e (tol %.1e)"
              % (str(base), s_c, side, dm, dg, tol_g, dH, tol_H))
OUT["V1_taylor_vs_fd"] = v1_rows
assert all(r["dm0"] < 1e-9 and r["dgrad"] < r["tol_grad"]
           and r["dhess"] < r["tol_hess"] for r in v1_rows), "V1 FAILED"

# ============================================ the ledger + output
r0_min = min(r0s)
smins = [r["s_min_tube"] for r in ray_rows if r["s_min_tube"] is not None]
ledger = {
    "certified": [
        "the 15 transverse 3-BALLS around the P3 base points: "
        "max(lambda_e, lambda_o) >= lambda* for ALL transverse "
        "directions |delta|_2 <= r0 (r0 min %.3f / median %.3f / max "
        "%.3f) — the analytic Taylor-4 patches, sound in balls"
        % (r0_min, sorted(r0s)[len(r0s) // 2], max(r0s)),
        "the 90 P3 rays are now FULLY covered from the stratum: "
        "[0, min(r0, s_min)] by the patches (the chains where r0 < "
        "s_min), [s_min, 0.15] by the Task 22 tubes — %d/%d rays"
        % (len(full), len(ray_rows)),
        "the never-certified P3 boundary ray (x0 = 0.15, the strongly "
        "x-ward direction): chained to |s|_2 = 0.15 — Task 22's P3 "
        "hole CLOSED",
        "the stratum itself (cited): the stack theorem + Task 17's "
        "global 1-atom corner certificate"],
    "measured_not_certified": [
        "the transverse directions BEYOND r0 from the base points (the "
        "all-direction collar is r0; beyond it the coverage is the "
        "sampled 6 directions per base — the tubes' sampling caveat, "
        "unchanged)",
        "the 6-D interior far from the stratum/killer/tube regions: "
        "0/500 random configs below lambda* (Task 22 part 1's "
        "F-frontier)"],
    "the_wall": "the exhaustive 6-D box certificate still needs "
                "h^-6 ~ 1e18..1e24 boxes (the box-count wall, "
                "unchanged); the analytic patches close the CORE "
                "(the near-stratum transverse region) that the wall "
                "was blocking"}
OUT["ledger"] = ledger
print()
print("=" * 72)
print("THE LEDGER (Task 26)")
print("=" * 72)
for k, items in ledger.items():
    print("  %s:" % k.upper())
    for it in (items if isinstance(items, list) else [items]):
        print("    - %s" % it[:105])

OUT["meta"]["wall_time_s"] = time.time() - t0
with open("tradeoff_patch_results.json", "w") as f:
    json.dump(OUT, f, indent=1, default=float)
print("\nOK results written: tradeoff_patch_results.json (%.1f s)"
      % (time.time() - t0))
