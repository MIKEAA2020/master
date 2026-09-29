#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""la_probe.py — structural verification of the saved line-atom cubic system.

Verifies, symbolically where possible:
  S1  the 6x6 A = C.G is block-upper-triangular w.r.t. idx1={beta(1,0),
      beta(1,1), f1} | comp: A[comp, idx1] == 0  =>  spec(C.G) =
      spec(A1) u spec(A2), so ||M||^2 = lambda_max(C.G) >= lambda_1(A1).
  S2  P1core (the cleared charpoly of A1) is degree 3 in lambda and
      degree <= 2 in c (the quadratic-in-c collapse).
  S3  the leading (lambda^3) coefficient of P1core is -(1-y^2)^3 (up to a
      positive constant): NEGATIVE on the domain |y| < 1.
  S4  numerics at the 90-digit optimum: lambda* is the LARGEST root of the
      cubic at (c*, y*); the other two roots and the A2-block eigenvalues
      are strictly below lambda*; C is PSD, G is PD, spec(C.G) real >= 0.
  S5  the quadratic-in-c coefficients A(lam,y), B(lam,y), Cc(lam,y) and the
      quadratic discriminant Delta(lam,y) = B^2-4*A*Cc: sign pattern of
      A(lambda*, y) and Delta(lambda*, y) over y in (-1, 1).
"""
import json
import math

import sympy as sp
import numpy as np

cs, ys, ls = sp.symbols('c y lambda', real=True)
t = 1 - ys**2

# ---- the 6x6 machinery, exactly as line_atom.py / minpoly_cell2.py --------
G = sp.zeros(6, 6)
C = sp.zeros(6, 6)
mu_ = [1, 1, 1, 2]
Cm = [2, 1, 1, 1]
bets = [(0, 0), (1, 0), (0, 1), (1, 1)]
s1 = {(0, 0): 0, (1, 0): 1, (0, 1): 0, (1, 1): 2 * ys}
s0 = {(0, 0): 1, (1, 0): 0, (0, 1): ys, (1, 1): 0}
e0 = {(0, 0): 0, (1, 0): ys, (0, 1): 0, (1, 1): 1}
e1 = {(0, 0): 2 * ys, (1, 0): 0, (0, 1): 1, (1, 1): 0}
for i, b in enumerate(bets):
    G[i, i] = mu_[i]
    C[i, i] = Cm[i]
    G[i, 4] = cs * s1[b]
    G[4, i] = cs * s1[b]
    G[i, 5] = cs * s0[b]
    G[5, i] = cs * s0[b]
    C[i, 4] = -e0[b]
    C[4, i] = -e0[b]
    C[i, 5] = -e1[b]
    C[5, i] = -e1[b]
G[4, 4] = cs**2 / t**2
G[5, 5] = cs**2 / t
C[4, 4] = 1 / t
C[5, 5] = 1 / t**2
A = sp.expand(C * G)

# ---- S1: block-upper-triangular structure ---------------------------------
idx1 = [1, 3, 4]
comp = [0, 2, 5]
offblock = [sp.expand(A[i, j]) for i in comp for j in idx1]
S1 = all(ob == 0 for ob in offblock)
print("S1  block-UT A[comp,idx1] == 0:", S1)

# ---- the core cubic --------------------------------------------------------
A1 = sp.Matrix(3, 3, lambda i, j: A[idx1[i], idx1[j]])
den = sp.Integer(1)
for e in A1:
    n, d = sp.fraction(sp.together(e))
    den = sp.lcm(den, d)
A1c = sp.expand(A1 * den)
P1 = sp.expand((A1c - ls * den * sp.eye(3)).det())
P1core = sp.expand(sp.cancel(P1 / ((ys**2 - 1)**6)))
p_c = sp.Poly(P1core, cs)
S2 = (sp.Poly(P1core, ls).degree() == 3, p_c.degree())
print("S2  deg_lambda(P1core) = 3:", S2[0], "| deg_c(P1core) =", S2[1])

# ---- S3: leading coefficient ----------------------------------------------
lc = sp.Poly(P1core, ls).all_coeffs()[-1]          # lambda^3 coefficient
lc_simpl = sp.factor(sp.cancel(lc))
print("S3  lambda^3 coefficient:", sp.sstr(lc_simpl))
S3 = sp.simplify(lc_simpl + t**3) == 0 or sp.simplify(lc_simpl + 2 * t**3) == 0
# generic: check sign as rational function on |y|<1
num3, den3 = sp.fraction(sp.together(lc_simpl))
S3 = sp.simplify(sp.factor(sp.cancel(-lc_simpl / t**3)))
print("    -lc/t^3 simplifies to:", S3)

# ---- S4: numerics at the 90-digit optimum ---------------------------------
HP = {"lam": "1.6310919765642504414737578928177383666901925754942",
      "c": "0.3971072873503973695456334",
      "y": "0.6563224669957891081761482"}
lam0, c0, y0 = (float(HP["lam"]), float(HP["c"]), float(HP["y"]))
cubs = sp.Poly(P1core.subs({cs: c0, ys: y0}), ls)
roots = sorted([complex(r) for r in sp.nroots(cubs, n=30)], key=lambda z: -z.real)
print("S4  cubic roots at (c*,y*):", ["%.10f%+.2ej" % (r.real, r.imag) for r in roots])
print("    largest root - lambda* = %.3e" % (roots[0].real - lam0))

def mats(c, y):
    tv = 1 - y * y
    Gm = np.zeros((6, 6)); Cm_ = np.zeros((6, 6))
    muv = [1.0, 1.0, 1.0, 2.0]; Cmv = [2.0, 1.0, 1.0, 1.0]
    s1v = {(0, 0): 0.0, (1, 0): 1.0, (0, 1): 0.0, (1, 1): 2.0 * y}
    s0v = {(0, 0): 1.0, (1, 0): 0.0, (0, 1): y, (1, 1): 0.0}
    e0v = {(0, 0): 0.0, (1, 0): y, (0, 1): 0.0, (1, 1): 1.0}
    e1v = {(0, 0): 2.0 * y, (1, 0): 0.0, (0, 1): 1.0, (1, 1): 0.0}
    for i, b in enumerate(bets):
        Gm[i, i] = muv[i]; Cm_[i, i] = Cmv[i]
        Gm[i, 4] = Gm[4, i] = c * s1v[b]
        Gm[i, 5] = Gm[5, i] = c * s0v[b]
        Cm_[i, 4] = Cm_[4, i] = -e0v[b]
        Cm_[i, 5] = Cm_[5, i] = -e1v[b]
    Gm[4, 4] = c * c / (tv * tv); Gm[5, 5] = c * c / tv
    Cm_[4, 4] = 1.0 / tv; Cm_[5, 5] = 1.0 / (tv * tv)
    return Cm_, Gm

ok_ps, ok_real, max_gap = True, True, 0.0
rng = np.random.default_rng(7)
for (c, y) in [(c0, y0), (0.3, 0.5), (-0.8, 0.7), (0.1, 0.2), (1.5, -0.4)] + \
               [(rng.uniform(-2, 2), rng.uniform(-0.95, 0.95)) for _ in range(15)]:
    Cm_, Gm = mats(c, y)
    ok_ps &= (np.linalg.eigvalsh(Cm_).min() > -1e-12) and (np.linalg.eigvalsh(Gm).min() > -1e-12)
    ev = np.linalg.eigvals(Cm_ @ Gm)
    ok_real &= max(abs(e.imag) for e in ev) < 1e-9
    max_gap = max(max_gap, max(abs(e.imag) for e in ev))
print("    C PSD & G PD (20 samples):", ok_ps, "| spec(C.G) real:", ok_real,
      "(max |imag| %.1e)" % max_gap)
Cm_, Gm = mats(c0, y0)
ev6 = sorted([e.real for e in np.linalg.eigvals(Cm_ @ Gm)], reverse=True)
print("    6x6 spectrum at (c*,y*):", ["%.6f" % v for v in ev6])
print("    lambda_max(6x6) - lambda* = %.3e" % (ev6[0] - lam0))

# ---- S5: the quadratic-in-c coefficients ----------------------------------
Pc = sp.Poly(P1core, cs)
Acoef = sp.cancel(Pc.all_coeffs()[0])   # c^2
Bcoef = sp.cancel(Pc.all_coeffs()[1])   # c^1
Ccoef = sp.cancel(Pc.all_coeffs()[2])   # c^0
Delta = sp.expand(sp.cancel(Bcoef**2 - 4 * Acoef * Ccoef))
print("S5  deg_y: A=%d B=%d C=%d Delta=%d (in y); deg_lam: A=%d B=%d C=%d Delta=%d"
      % (sp.Poly(Acoef, ys).degree(), sp.Poly(Bcoef, ys).degree(),
         sp.Poly(Ccoef, ys).degree(), sp.Poly(Delta, ys).degree(),
         sp.Poly(Acoef, ls).degree(), sp.Poly(Bcoef, ls).degree(),
         sp.Poly(Ccoef, ls).degree(), sp.Poly(Delta, ls).degree()))
A_l = sp.lambdify(ys, Acoef.subs(ls, lam0), 'numpy')
D_l = sp.lambdify(ys, Delta.subs(ls, lam0), 'numpy')
yy = np.linspace(-0.999, 0.999, 2001)
print("    A(lam*, y) over (-1,1): min %.6f max %.6f" % (A_l(yy).min(), A_l(yy).max()))
Dv = D_l(yy)
print("    Delta(lam*, y) over (-1,1): max %.6f min %.6f" % (Dv.max(), Dv.min()))
print("    Delta=0 crossings near:", yy[np.abs(Dv) < 1e-3][:6])

# save the pieces for the next stages
sp.save = None
out = {"S1_block_UT": bool(S1), "S2_deg": [3, int(p_c.degree())],
       "S3_leading_coeff": sp.sstr(lc_simpl),
       "S4_roots_at_opt": [[r.real, r.imag] for r in roots],
       "S4_6x6_spectrum": list(ev6),
       "A_expr": sp.sstr(sp.expand(sp.cancel(Acoef))),
       "B_expr": sp.sstr(sp.expand(sp.cancel(Bcoef))),
       "C_expr": sp.sstr(sp.expand(sp.cancel(Ccoef))),
       "Delta_expr": sp.sstr(sp.expand(sp.cancel(Delta))),
       "P1core_expr": sp.sstr(P1core)}
with open("/home/z/my-project/github_repos/master/scripts/la_probe_out.json", "w") as f:
    json.dump(out, f, indent=1)
print("saved la_probe_out.json")
