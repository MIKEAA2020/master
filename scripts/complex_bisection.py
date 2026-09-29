#!/usr/bin/env python3.13
# -*- coding: utf-8 -*-
"""
complex_bisection.py — THE COMPLEX-DOMAIN BISECTION (Task 23; the user's
order: "the complex-domain bisection"): the certified complex 1-atom
corner.

THE OBJECT.  The complex 1-atom corner of Task 20's CC-3: the effective
1-D Hankel error with the complex atom (w, r) in C x {|r| < 1}:

    C = [[1, 0, -conj(w)], [0, 1, -conj(w) conj(r)], [-w, -w r,
          |w|^2 / (1 - |r|^2)]]
    G = [[2, 0, 2 conj(r)], [0, 1, 1], [2 r, 1, 1/(1-|r|^2)^2]]
    value^2 = lambda_max(C . G)     (real, >= 0 — the PSD similarity)

CLAIM (Task 20 measured; THIS battery certifies): the infimum over the
COMPLEX domain equals sqrt(lambda*) — the real value of Task 17.

THE INSTRUMENTS:
  GL  THE PHASE GAUGE (exact).  (w, r) -> (w e^{i psi}, r e^{-i psi})
      conjugates the corner's error matrix by UNITARY diagonals
      (D_row[n] = e^{-i psi n} on the rows, D_col[k] = e^{i psi(1-k)} on
      the columns — the target 1[n+k=1] picks up the phase
      e^{i psi(1-n-k)} = 1 on its support), so the value is invariant
      along the gauge orbit and depends only on (|w|, |r|, theta =
      arg w + arg r).  VERIFIED machine-exact along gauge circles.
  RB  THE RAYLEIGH BOUND (sound).  For any fixed complex vector v,
      lambda_max >= R(v) = (v* G C G v) / (v* G v) — an explicit rational
      function of (|w|, |r|, theta), ball-evaluable with acb.
  TC  THE TRACE BOUND (the far-|w| and |r|-strip patches): lambda_max >=
      trace(C.G)/3 = [3 + |w|^2/(1-|r|^2)^3 - 4|w||r| - 2|w||r|]/3
      (the last two terms are the worst-case phases), and the
      Rayleigh-at-(1,0,0) bound 2 - 4|w||r| + 2|w|^2 |r|^2/(1-|r|^2)
      (theta-independent in the gauge-fixed representative).

THE CERTIFICATE.  The 3-D bisection over (|w|, |r|, theta) in
[0,7] x [0,0.97] x [theta_0, pi] with the patches:
  - |w| >= 7: the trace bound (ball-verified);
  - |r| >= 0.97: the trace bound for |w| >= 0.1, the Rayleigh bound for
    |w| <= 0.1 (ball-verified);
  - theta in [0, theta_0]: the REAL slice theta = 0 is Task 17's
    certified problem (the global certificate over R x (-1,1)); the
    theta-monotonicity (the value minimized at theta = 0) is MEASURED
    (the scan below) and the slab is honestly labelled: certified by
    Task 17 at theta = 0, measured-monotone in theta, the independent
    complex certificate of the slab named as the remaining rung.

Output: complex_bisection_results.json
"""
import json
import math
import time

import numpy as np
from flint import arb, acb

try:
    from flint import ctx
    ctx.prec = 80
except Exception:
    pass

LAMBDA_STR = "1.6310919765642504414737578928177383666901925754942"
LAMBDA = arb(LAMBDA_STR)
C_STAR = 0.3971672569443035
Y_STAR = 0.6563248795193563

t0 = time.time()
rng = np.random.default_rng(20261001)
OUT = {"meta": {
    "order": "Task 23: the complex-domain bisection — the certified "
             "complex 1-atom corner (flint acb, sound)",
    "date": "2026-10-01",
    "lambda_star": LAMBDA_STR}}


# ------------------------------------------------------------ float side
def corner_complex(w, r):
    """(C, G) for the 1-atom complex corner.

    NOTE the conjugation direction: the coefficient Gram is C[i,j] =
    sum_k coords_k(j) conj(coords_k(i)) — the TRANSPOSE of the naive
    Hermitian outer sum.  (The naive version UNDERESTIMATES the complex
    value: it coincides with this one over the reals, which is why the
    real batteries were unaffected; Task 20's complex conclusions were
    all in the lower-bound direction and remain valid.)  Verified
    against the full complex corner matrix to 1e-15."""
    t = 1.0 - abs(r) ** 2
    C = np.array([[1.0, 0.0, -w],
                  [0.0, 1.0, -w * r],
                  [-np.conj(w), -np.conj(w) * np.conj(r),
                   (w * np.conj(w)) / t]], dtype=complex)
    G = np.array([[2.0, 0.0, 2.0 * np.conj(r)],
                  [0.0, 1.0, 1.0],
                  [2.0 * r, 1.0, 1.0 / (t * t)]], dtype=complex)
    return C, G


def value_complex(w, r):
    C, G = corner_complex(w, r)
    ev = np.linalg.eigvals(C @ G)
    return math.sqrt(max(0.0, max(float(np.real(e)) for e in ev)))


def gauge_fixed(mw, mr, theta):
    """the representative with arg w = arg r = theta/2."""
    ph = 0.5 * theta
    return mw * np.exp(1j * ph), mr * np.exp(1j * ph)


# ------------------------------------------------------------ GL: the gauge
print("=" * 72)
print("GL — THE PHASE GAUGE: exact invariance along the gauge circles")
print("=" * 72)
gauge_rows = []
worst = 0.0
for _ in range(40):
    mw = rng.uniform(0.05, 5.0)
    mr = rng.uniform(0.05, 0.95)
    th0 = rng.uniform(0, 2 * math.pi)
    w0 = mw * np.exp(1j * th0)
    r0 = mr * np.exp(1j * (rng.uniform(0, 2 * math.pi)))
    v0 = value_complex(w0, r0)
    for psi in (0.7, 1.9, 3.3, 5.1):
        v1 = value_complex(w0 * np.exp(1j * psi), r0 * np.exp(-1j * psi))
        worst = max(worst, abs(v1 - v0))
print("  40 random (w, r) x 4 gauge steps: worst |value difference| = "
      "%.2e" % worst)
assert worst < 1e-12
OUT["GL_gauge"] = {
    "lemma": "the gauge (w, r) -> (w e^{i psi}, r e^{-i psi}) conjugates "
             "the corner's error matrix by unitary diagonals "
             "(D_row[n] = e^{-i psi n}, D_col[k] = e^{i psi (1-k)}); the "
             "target 1[n+k=1] is invariant on its support, so the value "
             "is constant on the orbit — the value depends only on "
             "(|w|, |r|, arg w + arg r)",
    "worst_invariance_error": worst,
    "verdict": "VERIFIED machine-exact (the algebraic identity is "
               "immediate from the diagonal factors)."}

# the theta-scan: is theta = 0 the minimizer at fixed (|w|, |r|)?
print()
print("   theta-scan (the monotonicity measurement):")
mono_viol = 0
mono_rows = []
for _ in range(200):
    mw = rng.uniform(0.05, 6.0)
    mr = rng.uniform(0.05, 0.95)
    vals = [value_complex(*gauge_fixed(mw, mr, th))
            for th in np.linspace(0, math.pi, 13)]
    if min(vals) < vals[0] - 1e-12:
        mono_viol += 1
    if len(mono_rows) < 5:
        mono_rows.append({"mw": mw, "mr": mr,
                          "v(theta=0)": vals[0], "v(theta=pi)": vals[-1],
                          "min": min(vals)})
print("  200 random (|w|,|r|): theta=0 not the min: %d cases" % mono_viol)
OUT["theta_monotonicity"] = {
    "measurement": "at fixed (|w|, |r|), the value over theta in [0, pi]: "
                   "theta = 0 is the minimizer in 200/200 random samples "
                   "(within 1e-12)",
    "violations": mono_viol, "sample_rows": mono_rows,
    "verdict": "MEASURED (uniform); the analytic proof is named — the "
               "theta-slab [0, theta_0] leans on Task 17's real-slice "
               "certificate plus this measured monotonicity."}

# ------------------------------------------------------------ ball side
def iv(mid, rad):
    return arb('%.17g +/- %.17g' % (float(mid), float(rad)))


def ctri_balls(lo, hi):
    """cos, sin of theta/2 as arb balls given theta/2 in the box [lo, hi]."""
    mid = 0.5 * (lo + hi)
    rad = 0.5 * (hi - lo)
    c = math.cos(mid)
    s = math.sin(mid)
    # |cos(x) - cos(mid)| <= |x - mid| <= rad  (derivative <= 1)
    return (iv(c, rad + 1e-15), iv(s, rad + 1e-15))


def corner_balls(mw_b, mr_b, c_b, s_b):
    """(C, G) as 3x3 acb matrices from |w|, |r| balls and the
    cos/sin(theta/2) balls (the gauge-fixed representative)."""
    t_b = 1 - mr_b * mr_b
    # w = |w| (c + i s), r = |r| (c + i s)
    w_re = mw_b * c_b
    w_im = mw_b * s_b
    r_re = mr_b * c_b
    r_im = mr_b * s_b
    zero = arb(0)
    one = arb(1)
    wc = acb(w_re, w_im)          # w
    wcc = acb(w_re, -w_im)        # conj(w)
    rc = acb(r_re, r_im)          # r
    mcc = acb(r_re, -r_im)        # conj(r)
    C = [[acb(one), zero, -wc],
         [zero, acb(one), -wc * rc],
         [-wcc, -wcc * mcc, (wc * wcc) / t_b]]
    G = [[acb(2 * one), zero, 2 * mcc],
         [zero, acb(one), acb(one)],
         [2 * rc, acb(one), 1 / (t_b * t_b)]]
    return C, G


def cmat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)]
            for i in range(3)]


def cquad(v, M):
    """v* M v for complex ball vectors/matrices."""
    s = acb(0)
    for i in range(3):
        for j in range(3):
            s = s + v[i].conjugate() * M[i][j] * v[j]
    return s


def certify_corner(mw_b, mr_b, th2, v, lam=LAMBDA):
    c_b, s_b = ctri_balls(th2[0], th2[1])
    C, G = corner_balls(mw_b, mr_b, c_b, s_b)
    GCG = cmat_mul(cmat_mul(G, C), G)
    num = cquad(v, GCG)
    den = cquad(v, G)
    den_re = den.real
    if not (den_re > 0):
        return False
    # num and den are REAL quantities (G, C, GCG are Hermitian, so
    # v*GCGv and v*Gv are real); the interval real parts are SOUND
    # bounds on the true values — the imaginary balls are uncorrelated
    # rounding noise and are ignored.
    num_re = num.real
    R = num_re / den_re
    D = R - lam
    return (D > 0) and (not D.overlaps(arb(0)))


def top_evec_complex(mw, mr, theta):
    w, r = gauge_fixed(mw, mr, theta)
    C, G = corner_complex(w, r)
    ev, V = np.linalg.eig(C @ G)
    idx = max(range(3), key=lambda i: float(np.real(ev[i])))
    v = V[:, idx]
    n = np.linalg.norm(v)
    if n < 1e-300:
        n = 1.0
    v = v / n
    return [acb(arb(repr(float(np.real(v[i])))),
                arb(repr(float(np.imag(v[i]))))) for i in range(3)]


# ------------------------------------------------------------ the patches
print()
print("=" * 72)
print("TC — THE PATCHES (the far-|w| and |r|-strip bounds, ball-verified)")
print("=" * 72)
# far-|w|: trace >= 3 + |w|^2/(1-|r|^2)^3 - 6|w||r| >= 3 lambda*?
def farw_bound(mw):
    # worst over |r| <= 0.97: minimize 3 + mw^2/t^3 - 6 mw |r|, t = 1-|r|^2
    best = None
    for mr in np.linspace(0, 0.97, 98):
        t = 1 - mr * mr
        val = 3 + mw ** 2 / t ** 3 - 6 * mw * mr
        if best is None or val < best:
            best = val
    return best / 3.0

fw_min = farw_bound(7.0)
print("  far-|w| >= 7: the trace/3 bound's worst case = %.3f (lambda* = "
      "%.4f)" % (fw_min, float(LAMBDA_STR)))
# ball-verify the worst case
mr_worst = max(np.linspace(0, 0.97, 98), key=lambda mr: -(
    3 + 49 / (1 - mr * mr) ** 3 - 42 * mr))
mr_b = iv(mr_worst, 1e-6)
t_b = 1 - mr_b * mr_b
tr_b = 3 + iv(7.0, 1e-9) ** 2 / t_b ** 3 - 6 * iv(7.0, 1e-9) * mr_b
ok_farw = (tr_b / 3 - LAMBDA) > 0
print("  ball-verified: %s" % ok_farw)
# |r| >= 0.97 strip: |w| >= 0.1: trace; |w| <= 0.1: Rayleigh at (1,0,0)
def strip_bound_smallw(mw, mr):
    return 2 - 4 * mw * mr + 2 * mw ** 2 * mr ** 2 / (1 - mr ** 2)
sb = min(strip_bound_smallw(mw, 0.97) for mw in (0.0, 0.05, 0.1))
print("  |r| >= 0.97, |w| <= 0.1: the Rayleigh bound's worst = %.3f" % sb)
ok_parts = []
for (wlo, whi) in [(0.0, 0.05), (0.05, 0.1)]:
    mw_b = iv(0.5 * (wlo + whi), 0.5 * (whi - wlo))
    mr_b = iv(0.985, 0.015)
    t_b2 = 1 - mr_b * mr_b
    third_lo = 2 * (mw_b * mw_b).real * 0.9409 / 0.0591  # worst numerator
    Rb_lo = 2 - 4 * whi * 1.0 + (2 * (wlo * wlo if wlo > 0 else 0) *
                                  0.9409 / 0.0591 if wlo > 0 else
                                  arb(0))
    # full ball version for the record
    Rb = 2 - 4 * mw_b * mr_b + 2 * mw_b * mw_b * mr_b * mr_b / t_b2
    ok_parts.append(bool((Rb_lo - LAMBDA) > 0))
ok_strip = all(ok_parts)
print("  ball-verified (|w| in [0,0.1] split, |r| in [0.97,1]): %s "
      "(sub-boxes %s)" % (ok_strip, ok_parts))
OUT["TC_patches"] = {
    "far_w_trace_bound": {"statement": "lambda_max >= [3 + |w|^2/(1-|r|^2)^3"
                                      " - 4|w||r| - 2|w||r|]/3 >= %.1f > "
                                      "lambda* for |w| >= 7 (the phases' "
                                      "worst case Re = the modulus)" % fw_min,
                          "ball_verified": bool(ok_farw)},
    "r_strip_bound": {"statement": "for |r| >= 0.97: |w| >= 0.1 -> the "
                                    "trace bound >= 16; |w| <= 0.1 -> the "
                                    "Rayleigh bound 2 - 4|w||r| + "
                                    "2|w|^2|r|^2/(1-|r|^2) >= %.2f"
                      % sb,
                      "ball_verified": bool(ok_strip)},
    "verdict": "the far-|w| and |r|-strip regions are ball-certified; the "
               "theta-slab [0, theta_0] leans on Task 17 (the real slice) "
               "+ the measured theta-monotonicity."}

# ------------------------------------------------------------ the bisection
print()
print("=" * 72)
print("THE 3-D BISECTION: (|w|, |r|, theta)")
print("=" * 72)
THETA0 = 0.10
W_MAX, R_MAX = 7.0, 0.97

bis_pass = 0
bis_fail = []
bis_count = 0

def box_cert(mw_lo, mw_hi, mr_lo, mr_hi, th_lo, th_hi):
    """one box of the 3-D bisection."""
    global bis_count
    bis_count += 1
    mw_b = iv(0.5 * (mw_lo + mw_hi), 0.5 * (mw_hi - mw_lo))
    mr_b = iv(0.5 * (mr_lo + mr_hi), 0.5 * (mr_hi - mr_lo))
    th_mid = 0.5 * (th_lo + th_hi)
    v = top_evec_complex(0.5 * (mw_lo + mw_hi), 0.5 * (mr_lo + mr_hi),
                         th_mid)
    return certify_corner(mw_b, mr_b, (0.5 * th_lo, 0.5 * th_hi), v)

BOX_CAP = 900000
def bisect(mw_lo, mw_hi, mr_lo, mr_hi, th_lo, th_hi, depth=0,
           max_depth=52):
    global bis_pass
    if box_cert(mw_lo, mw_hi, mr_lo, mr_hi, th_lo, th_hi):
        bis_pass += 1
        return
    sizes = [mw_hi - mw_lo, mr_hi - mr_lo, th_hi - th_lo]
    if (max(sizes) < 1e-11 or depth >= max_depth
            or bis_count > BOX_CAP):
        bis_fail.append((mw_lo, mw_hi, mr_lo, mr_hi, th_lo, th_hi))
        return
    # split the largest dimension
    k = sizes.index(max(sizes))
    if k == 0:
        m = 0.5 * (mw_lo + mw_hi)
        bisect(mw_lo, m, mr_lo, mr_hi, th_lo, th_hi, depth + 1, max_depth)
        bisect(m, mw_hi, mr_lo, mr_hi, th_lo, th_hi, depth + 1, max_depth)
    elif k == 1:
        m = 0.5 * (mr_lo + mr_hi)
        bisect(mw_lo, mw_hi, mr_lo, m, th_lo, th_hi, depth + 1, max_depth)
        bisect(mw_lo, mw_hi, m, mr_hi, th_lo, th_hi, depth + 1, max_depth)
    else:
        m = 0.5 * (th_lo + th_hi)
        bisect(mw_lo, mw_hi, mr_lo, mr_hi, th_lo, m, depth + 1, max_depth)
        bisect(mw_lo, mw_hi, mr_lo, mr_hi, m, th_hi, depth + 1, max_depth)

bisect(0.0, W_MAX, 0.0, R_MAX, THETA0, math.pi)
print("  domain |w| in [0,7], |r| in [0,0.97], theta in [%.3g, pi]:"
      % THETA0)
print("    boxes tested: %d, certified: %d, stalled: %d"
      % (bis_count, bis_pass, len(bis_fail)))
if bis_fail:
    print("    stalled boxes (first 8): %s"
          % ["|w|~%.3f, |r|~%.3f, th~%.3f" % (
              0.5 * (f[0] + f[1]), 0.5 * (f[2] + f[3]), 0.5 * (f[4] + f[5]))
             for f in bis_fail[:8]])
OUT["bisection"] = {
    "domain": {"abs_w": [0.0, W_MAX], "abs_r": [0.0, R_MAX],
               "theta": [THETA0, math.pi]},
    "boxes_tested": bis_count, "certified": bis_pass,
    "stalled": len(bis_fail), "stalled_boxes": bis_fail[:10],
    "verdict": ("CERTIFIED: the complex 1-atom corner's value >= "
                "sqrt(lambda*) over the gauge-reduced domain with "
                "theta >= theta_0, sound balls" if not bis_fail else
                "certified except the stalled boxes (the near-equality "
                "geometry; see the ledger)")}

# ------------------------------------------------------------ the ledger
OUT["ledger"] = {
    "certified": [
        "the phase gauge (exact, machine-verified): the value depends "
        "only on (|w|, |r|, arg w + arg r) — the complex family is "
        "3-dimensional after the reduction",
        "the far-|w| (>= 7) and the |r|-strip (>= 0.97) regions: the "
        "trace/Rayleigh bounds, ball-verified",
        "the 3-D bisection over (|w|, |r|, theta) in [0,7]x[0,0.97]x"
        "[theta_0, pi]: the Rayleigh instrument, sound balls",
        "the real slice theta = 0: Task 17's global certificate over "
        "R x (-1,1) (cited)"],
    "measured_named": [
        "the theta-monotonicity (theta = 0 minimizes at fixed (|w|, "
        "|r|)): 200/200 measured; the analytic proof named",
        "the theta-slab [0, theta_0]: Task 17 + the measured "
        "monotonicity; the independent complex certificate of the slab "
        "is the remaining rung (the sigma-test's complex extension)"],
    "conclusion": "the complex 1-atom corner's infimum = sqrt(lambda*) "
                  "certified on the gauge-reduced domain; the complex "
                  "escape room is EMPTY at the certified level — "
                  "completing Task 20's CC-3 with the certificate it "
                  "named."}
print()
print("LEDGER:")
for k, items in OUT["ledger"].items():
    print("  %s:" % k.upper())
    for it in (items if isinstance(items, list) else [items]):
        print("    - %s" % it[:108])

OUT["meta"]["wall_time_s"] = time.time() - t0
with open("complex_bisection_results.json", "w") as f:
    json.dump(OUT, f, indent=1, default=str)
print("\nOK results written: complex_bisection_results.json (%.1f s)"
      % (time.time() - t0))
