#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""la_minpoly.py — the minimal polynomial of lambda* via external factoring.

The saved cubic stationarity system (P, dP/dc, dP/dy) collapses because
P1core is QUADRATIC in c:  P = A(lam,y) c^2 + B(lam,y) c + C(lam,y).
  dP/dc = 0   ->  c0 = -B/(2A)               (A != 0)
  P = 0       ->  Delta := B^2 - 4AC = 0      (the vertex value -Delta/4A)
  dP/dy = 0   ->  Nred = 0,  Nred = -B*By + 2A*Cy + 2*Ay*C
        (from N = Ay*B^2 - 2A*B*By + 4A^2*Cy = Ay*Delta + 2A*Nred,
         valid on {Delta = 0, A != 0}; the stratum A = B = 0 handled apart.)
Elimination: E(lam) = Res_y(Delta, Nred), computed EXACTLY by evaluating the
Sylvester determinant (fmpz_mat) at consecutive integer lambdas and
interpolating with finite differences (self-checked at an extra point).
Then EXTERNAL FACTORING (python-flint) of E; the irreducible factor having
lambda* as a root IS the minimal polynomial (irreducible over Q by FLINT).
Also: the minimal polynomial of sqrt(lambda*), the isolating interval of
lambda*, the degenerate stratum, and the critical-value census.
"""
import json
import time

import sympy as sp
from flint import fmpz_poly, fmpz_mat

t_wall = time.time()
cs, ys, ls = sp.symbols('c y lambda', real=True)
t = 1 - ys**2

# ---- the machinery + the core cubic (as in line_atom.py) -------------------
G = sp.zeros(6, 6); C = sp.zeros(6, 6)
mu_ = [1, 1, 1, 2]; Cm = [2, 1, 1, 1]
bets = [(0, 0), (1, 0), (0, 1), (1, 1)]
s1 = {(0, 0): 0, (1, 0): 1, (0, 1): 0, (1, 1): 2 * ys}
s0 = {(0, 0): 1, (1, 0): 0, (0, 1): ys, (1, 1): 0}
e0 = {(0, 0): 0, (1, 0): ys, (0, 1): 0, (1, 1): 1}
e1 = {(0, 0): 2 * ys, (1, 0): 0, (0, 1): 1, (1, 1): 0}
for i, b in enumerate(bets):
    G[i, i] = mu_[i]; C[i, i] = Cm[i]
    G[i, 4] = G[4, i] = cs * s1[b]
    G[i, 5] = G[5, i] = cs * s0[b]
    C[i, 4] = C[4, i] = -e0[b]
    C[i, 5] = C[5, i] = -e1[b]
G[4, 4] = cs**2 / t**2; G[5, 5] = cs**2 / t
C[4, 4] = 1 / t; C[5, 5] = 1 / t**2
A6 = sp.expand(C * G)
idx1 = [1, 3, 4]
A1 = sp.Matrix(3, 3, lambda i, j: A6[idx1[i], idx1[j]])
den = sp.Integer(1)
for e in A1:
    n, d = sp.fraction(sp.together(e))
    den = sp.lcm(den, d)
A1c = sp.expand(A1 * den)
P1 = sp.expand((A1c - ls * den * sp.eye(3)).det())
P1core = sp.expand(sp.cancel(P1 / ((ys**2 - 1)**6)))
assert sp.simplify(sp.Poly(P1core, ls).all_coeffs()[0] - t**3) == 0

# ---- the quadratic-in-c collapse -------------------------------------------
Pc = sp.Poly(P1core, cs)
Aq, Bq, Cq = [sp.expand(sp.cancel(c)) for c in Pc.all_coeffs()]
Ay, By, Cy = [sp.diff(q, ys) for q in (Aq, Bq, Cq)]
Delta = sp.expand(Bq**2 - 4 * Aq * Cq)
Nred = sp.expand(-Bq * By + 2 * Aq * Cy + 2 * Ay * Cq)
Nfull = sp.expand(Ay * Bq**2 - 2 * Aq * Bq * By + 4 * Aq**2 * Cy)
check = sp.expand(Nfull - (Ay * Delta + 2 * Aq * Nred))
assert sp.expand(check) == 0, "N reduction identity failed"
print("[1] quadratic collapse: deg_y A=%d B=%d C=%d Delta=%d Nred=%d; "
      "deg_lam A=%d B=%d C=%d Delta=%d Nred=%d"
      % (sp.Poly(Aq, ys).degree(), sp.Poly(Bq, ys).degree(),
         sp.Poly(Cq, ys).degree(), sp.Poly(Delta, ys).degree(),
         sp.Poly(Nred, ys).degree(),
         sp.Poly(Aq, ls).degree(), sp.Poly(Bq, ls).degree(),
         sp.Poly(Cq, ls).degree(), sp.Poly(Delta, ls).degree(),
         sp.Poly(Nred, ls).degree()))

# ---- verify the collapse at the 90-digit optimum ---------------------------
LAM = sp.Rational(0)  # placeholder
lam0 = sp.Float("1.6310919765642504414737578928177383666901925754942", 60)
c0v = sp.Float("0.3971072873503973695456334", 40)
y0v = sp.Float("0.6563224669957891081761482", 40)
subs0 = {ls: lam0, ys: y0v}
dv = complex(Delta.subs(subs0))
nv = complex(Nred.subs(subs0))
av = complex(Aq.subs(subs0))
cv_pred = -complex(Bq.subs(subs0)) / (2 * av)
print("[2] at (lam*, y*): Delta = %.3e | Nred = %.3e | A = %.4f | "
      "c_pred = %.10f (c* = %.10f)" % (abs(dv), abs(nv), av.real,
                                       cv_pred.real, c0v))
assert abs(dv) < 1e-25 and abs(nv) < 1e-25 and abs(av) > 1e-3

# ---- gcd strip ---------------------------------------------------------------
g = sp.gcd(Delta, Nred)
gdeg = 0 if g == 1 else sp.Poly(g, ls, ys).total_degree()
print("[3] gcd(Delta, Nred) total degree:", gdeg)
if gdeg and gdeg <= 8:
    print("    gcd =", sp.sstr(sp.factor(g)))
if g != 1:
    # also report gcd(A, B) — is the common factor the degenerate stratum?
    gab = sp.gcd(Aq, Bq)
    print("    gcd(A, B) total degree:",
          0 if gab == 1 else sp.Poly(gab, ls, ys).total_degree())
    Delta_s = sp.cancel(Delta / g)
    Nred_s = sp.cancel(Nred / g)
else:
    Delta_s, Nred_s = Delta, Nred
md = sp.Poly(Delta_s, ys).degree()
nd = sp.Poly(Nred_s, ys).degree()

# ---- E = Res_y(Delta_s, Nred_s) via exact integer interpolation ------------
dl = sp.Poly(Delta_s, ls).degree()
nl = sp.Poly(Nred_s, ls).degree()
deg_bound = md * nl + nd * dl
NPTS = deg_bound + 5
print("[4] Sylvester %dx%d, deg_lam bound %d, interpolating at %d points"
      % (md + nd, md + nd, deg_bound, NPTS))

dco = sp.Poly(Delta_s, ys).all_coeffs()   # descending, entries in Z[lambda]
nco = sp.Poly(Nred_s, ys).all_coeffs()


def sylv_det_at(k):
    fd = [int(sp.Poly(co, ls).eval(k)) for co in dco]
    gd = [int(sp.Poly(co, ls).eval(k)) for co in nco]
    if fd[0] == 0 or gd[0] == 0:
        return None  # degree drop at this k; skip via shifted grid
    m, n = len(fd) - 1, len(gd) - 1
    rows = []
    for i in range(n):                    # n rows of f, shifted
        rows.append([0] * i + fd + [0] * (n - 1 - i))
    for i in range(m):                    # m rows of g, shifted
        rows.append([0] * i + gd + [0] * (m - 1 - i))
    assert all(len(r) == m + n for r in rows)
    return int(fmpz_mat(rows).det())

vals, base = {}, 0
while len(vals) < NPTS + 1:
    v = sylv_det_at(base + len(vals))
    if v is None:
        base += 200
        vals = {}
        continue
    vals[len(vals)] = v
vlist = [vals[i] for i in range(NPTS + 1)]
print("    evaluations done (base %d), max digits: %d"
      % (base, max(len(str(abs(v))) for v in vlist)))

# Newton forward differences at the (possibly shifted) base, converted to
# the standard basis EXACTLY via sympy.
D = [vlist[:]]
for i in range(1, NPTS + 1):
    D.append([D[i - 1][j + 1] - D[i - 1][j] for j in range(len(D[i - 1]) - 1)])
import math
zz = sp.symbols('zz')
acc, prod = sp.Integer(0), sp.Integer(1)
for j in range(NPTS):
    if D[j][0] != 0:
        q, r = divmod(D[j][0], math.factorial(j))
        assert r == 0, "difference not divisible by j! at j=%d" % j
        acc += q * prod
    prod *= (zz - j)
Eexpr = sp.expand(acc.subs(zz, ls - base))
Ec = sp.Poly(Eexpr, ls).all_coeffs()   # descending
assert Ec[0] != 0
acoeff = [int(v) for v in reversed(Ec)]  # ascending
Edeg = len(acoeff) - 1
# self-check at the extra point
kchk = base + NPTS
pred = sum(acoeff[i] * (kchk ** i) for i in range(len(acoeff)))
assert pred == vlist[NPTS], "interpolation self-check FAILED"
print("[5] E(lam) interpolated: degree %d (bound %d), self-check at k=%d PASS"
      % (Edeg, deg_bound, kchk))

Epoly = fmpz_poly(acoeff)

# ---- EXTERNAL FACTORING (FLINT) ---------------------------------------------
t0 = time.time()
fac = Epoly.factor()
try:
    content, pairs = fac
except Exception:
    pairs, content = fac, None
print("[6] FLINT factored E in %.1fs: %d irreducible factors" %
      (time.time() - t0, len(pairs)))

census = []
Mfac = None
x = sp.symbols('x')
for item in pairs:
    f, e = item if isinstance(item, tuple) and len(item) == 2 else (item, 1)
    fl = [int(c) for c in f.coeffs()]
    d = len(fl) - 1
    spf = sp.Poly(fl[::-1], x)
    rr = spf.intervals()               # [((a, b), mult), ...]
    ent = {"degree": d, "exp": int(e),
           "n_real_roots": len(rr),
           "real_root_isolations": [[str(a), str(b)] for (a, b), _ in rr]}
    hit = False
    for (a, b), _m in rr:
        lo_, hi_ = sp.Rational(a), sp.Rational(b)
        if not (lo_ < sp.Rational(1631, 1000) < hi_ or
                (lo_ < sp.Rational(1632, 1000) and hi_ > sp.Rational(1630, 1000))):
            continue
        for _ in range(80):
            mid2 = (lo_ + hi_) / 2
            if spf.eval(lo_) * spf.eval(mid2) <= 0:
                hi_ = mid2
            else:
                lo_ = mid2
        if abs(float((lo_ + hi_) / 2) - float(lam0)) < 1e-10:
            hit = True
    ent["contains_lambda_star"] = bool(hit)
    if d <= 80:
        ent["coeffs_desc"] = [str(c) for c in fl[::-1]]
    census.append(ent)
    if hit:
        Mfac = (fl, spf, ent)
    print("    factor deg %d (x%d): %d real roots%s"
          % (d, e, len(rr), "   <<< lambda* lives here" if hit else ""))

assert Mfac is not None, "lambda* not found among the factors!"
Mcoeff, Msp, Ment = Mfac
Mdeg = Msp.degree()
print("[7] MINIMAL POLYNOMIAL of lambda*: degree %d" % Mdeg)
print("    ", Msp.as_expr())

# divisibility proof (exact, flint)
q, r = divmod(Epoly, fmpz_poly(Mcoeff))
assert all(int(c) == 0 for c in r.coeffs()), "M does not divide E!"
print("    exact division M | E: PASS (quotient degree %d)" % (len(q.coeffs()) - 1))

# lambda* isolating interval (exact bisection)
lo, hi = sp.Rational(0), sp.Rational(0)
for a, b in Ment["real_root_isolations"]:
    if sp.Rational(a) < sp.Rational(1631, 1000) < sp.Rational(b):
        lo, hi = sp.Rational(a), sp.Rational(b)
        break
assert hi != 0
for _ in range(120):
    mid = (lo + hi) / 2
    if Msp.eval(lo) * Msp.eval(mid) <= 0:
        hi = mid
    else:
        lo = mid
lam_star_exact = (lo + hi) / 2
print("[8] isolating interval width: 1e-%d; lambda* = %s"
      % (len(str((hi - lo).p)), sp.N(lam_star_exact, 60)))

# high-precision lambda* via mpmath Newton on M
import mpmath as mp
mp.mp.dps = 150
Mlam = sp.lambdify(x, Msp.as_expr(), 'mpmath')
root = mp.findroot(Mlam, mp.mpf(str(sp.N(lam_star_exact, 40))))
lam_hp = mp.nstr(root, 100)
print("    lambda* (100 digits):", lam_hp)
print("    D(2) = sqrt(lambda*) =", mp.nstr(mp.sqrt(root), 60))

# minimal polynomial of sqrt(lambda*)
Msq = sp.expand(Msp.as_expr().subs(x, x**2))
sqfac = sp.factor_list(Msq)
Dmin = None
for ff, ee in sqfac[1]:
    ff_poly = sp.Poly(ff, x)
    rr = ff_poly.intervals()
    for (a, b), _m in rr:
        if a < sp.Rational(128, 100) and b > sp.Rational(127, 100):
            lo_, hi_ = sp.Rational(a), sp.Rational(b)
            for _ in range(80):
                mid2 = (lo_ + hi_) / 2
                if ff_poly.eval(lo_) * ff_poly.eval(mid2) <= 0:
                    hi_ = mid2
                else:
                    lo_ = mid2
            if abs(float((lo_ + hi_) / 2) - 1.277142112908) < 1e-9:
                Dmin = (ff_poly, [a, b])
            break
if Dmin is not None:
    print("[9] minimal polynomial of D = sqrt(lambda*): degree %d"
          % Dmin[0].degree())
    print("    ", Dmin[0].as_expr())

# ---- the degenerate stratum A = B = 0 (+ C = 0, Cy = 0) ----------------------
t0 = time.time()
gb = sp.groebner([Aq, Bq, Cq, Cy], ls, ys, order='lex')
sols = sp.solve([Aq, Bq, Cq, Cy], [ls, ys], dict=True)
print("[10] degenerate stratum {A=B=C=Cy=0}: %s (%.1fs)"
      % (sols if sols else "EMPTY", time.time() - t0))

# ---- critical-value census (numerical) --------------------------------------
import numpy as np
crit = []
for ent in census:
    if ent["n_real_roots"] == 0:
        continue
    fl_desc = ent.get("coeffs_desc")
    if fl_desc is None:
        continue
    fl_np = np.array([float(v) for v in fl_desc])
    if np.any(np.abs(fl_np) > 1e30):
        continue
    for r in np.roots(fl_np):
        lh = float(np.real(r))
        if abs(np.imag(r)) > 1e-9 or lh < -0.5 or lh > 8:
            continue
        Dy = sp.Poly(Delta_s.subs(ls, lh), ys)
        Ny = sp.Poly(Nred_s.subs(ls, lh), ys)
        dcoef = np.array([float(v) for v in reversed(
            [sp.N(v, 30) for v in Dy.all_coeffs()])])
        ncoef = np.array([float(v) for v in reversed(
            [sp.N(v, 30) for v in Ny.all_coeffs()])])
        if np.any(np.abs(dcoef) > 1e25) or dcoef[0] == 0:
            continue
        for yr in np.roots(dcoef):
            if abs(np.imag(yr)) > 1e-8 or abs(float(np.real(yr))) > 0.999:
                continue
            yv = float(np.real(yr))
            nv_ = float(np.polyval(ncoef, yv))
            av_ = float(sp.N(Aq.subs({ls: lh, ys: yv}), 30))
            bv_ = float(sp.N(Bq.subs({ls: lh, ys: yv}), 30))
            scale = max(1.0, abs(float(np.polyval(np.abs(ncoef), yv))))
            if abs(nv_) < 1e-6 * scale and abs(av_) > 1e-10:
                crit.append({"lambda": lh, "y": yv,
                             "c": -bv_ / (2 * av_)})
crit_unique = []
for c_ in crit:
    if not any(abs(c_["lambda"] - u["lambda"]) < 1e-8 and
               abs(c_["y"] - u["y"]) < 1e-5 for u in crit_unique):
        crit_unique.append(c_)
print("[11] genuine stationary lifts (numeric): %d" % len(crit_unique))
for c_ in sorted(crit_unique, key=lambda z: z["lambda"]):
    print("    lambda = %.10f at (c, y) = (%.6f, %.6f) %s"
          % (c_["lambda"], c_["c"], c_["y"],
             "<-- the optimum" if abs(c_["lambda"] - 1.63109) < 1e-6 else ""))

OUT = {
 "meta": {"script": "la_minpoly.py",
          "engine": "python-flint 0.9.0 (external factoring)",
          "date": "2026-09-29", "wall_time_s": round(time.time() - t_wall, 1)},
 "quadratic_collapse": {
   "statement": "P1core = A(lam,y)c^2 + B(lam,y)c + Cc(lam,y); stationarity "
                "reduces to Delta = B^2-4AC = 0 and Nred = -B*By+2A*Cy+2*Ay*C "
                "= 0 at c0 = -B/(2A)",
   "deg_y": [sp.Poly(Aq, ys).degree(), sp.Poly(Bq, ys).degree(),
             sp.Poly(Cq, ys).degree(), sp.Poly(Delta, ys).degree(),
             sp.Poly(Nred, ys).degree()],
   "deg_lam": [sp.Poly(Aq, ls).degree(), sp.Poly(Bq, ls).degree(),
               sp.Poly(Cq, ls).degree(), sp.Poly(Delta, ls).degree(),
               sp.Poly(Nred, ls).degree()],
   "verification_at_optimum": {"Delta": abs(dv), "Nred": abs(nv),
                               "A": av.real, "c_pred": cv_pred.real,
                               "c_star": float(c0v)}},
 "eliminant": {
   "method": "Sylvester determinant evaluated at %d consecutive integers, "
             "finite-difference interpolation, self-check PASS" % NPTS,
   "degree": Edeg,
   "n_factors": len(pairs)},
 "minimal_polynomial_lambda": {
   "degree": Mdeg,
   "coeffs_desc": Ment.get("coeffs_desc"),
   "expression": sp.sstr(Msp.as_expr()),
   "divides_E_exactly": True,
   "lambda_star_100_digits": lam_hp,
   "D2_sqrt_60_digits": mp.nstr(mp.sqrt(root), 60),
   "isolating_interval": [str(lo), str(hi)]},
 "minimal_polynomial_D": ({"degree": Dmin[0].degree(),
                            "expression": sp.sstr(Dmin[0].as_expr())}
                           if Dmin else None),
 "degenerate_stratum": ("EMPTY" if not sols else
                        [str(s) for s in sols]),
 "critical_value_census": crit_unique,
}
with open("/home/z/my-project/github_repos/master/scripts/"
          "la_minpoly_results.json", "w") as f:
    json.dump(OUT, f, indent=1, default=str)
print("saved la_minpoly_results.json  [total %.1fs]" % (time.time() - t_wall))
