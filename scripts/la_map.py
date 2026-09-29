#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""la_map.py — terrain map for the global certificate.

With lc(P1core) = -(1-y^2)^3 < 0 on |y|<1 and the cubic real-rooted
(spec(C.G) real >= 0, block-UT), the BAD event
    lambda_1(c,y) < lam*
is equivalent to the sigma-triple
    P(lam*) < 0  and  dP/dLam(lam*) < 0  and  d2P/dLam2(lam*) < 0.
Map the three functions over the (c, y) domain; locate the curve
P(lam*)=0; check for stall candidates (all three <= 0).
"""
import numpy as np
import sympy as sp

cs, ys, ls = sp.symbols('c y lambda', real=True)
t = 1 - ys**2
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
A = sp.expand(C * G)
idx1 = [1, 3, 4]
A1 = sp.Matrix(3, 3, lambda i, j: A[idx1[i], idx1[j]])
den = sp.Integer(1)
for e in A1:
    n, d = sp.fraction(sp.together(e))
    den = sp.lcm(den, d)
A1c = sp.expand(A1 * den)
P1 = sp.expand((A1c - ls * den * sp.eye(3)).det())
P1core = sp.expand(sp.cancel(P1 / ((ys**2 - 1)**6)))
lcoeff = sp.Poly(P1core, ls).all_coeffs()[0]
print("leading lambda^3 coeff:", sp.sstr(sp.factor(sp.cancel(lcoeff))))
# -(y-1)^3 (y+1)^3 = +(1-y^2)^3 > 0 on |y|<1:  POSITIVE leading coeff.
assert sp.simplify(lcoeff - t**3) == 0, "unexpected leading coeff!"
# With lc > 0:  BAD (lam_1 < lam*) <=> P>0 and P'>0 and P''>0 (real-rooted);
# and P(lam*) <= 0 => lam_1 >= lam*  (classical, unconditional).

dPl = sp.diff(P1core, ls)
d2Pl = sp.diff(P1core, ls, 2)

lam0 = 1.6310919765642504414737578928177383666901925754942
Pf = sp.lambdify((cs, ys), P1core.subs(ls, lam0), 'numpy')
Df = sp.lambdify((cs, ys), dPl.subs(ls, lam0), 'numpy')
Sf = sp.lambdify((cs, ys), d2Pl.subs(ls, lam0), 'numpy')

# grid: c in [-8, 8] (log-dense near 0), y in (-0.999, 0.999)
cgrid = np.unique(np.concatenate([np.linspace(-8, 8, 1201),
                                  np.linspace(-1, 1, 801)]))
ygrid = np.linspace(-0.999, 0.999, 1001)
CC, YY = np.meshgrid(cgrid, ygrid)
PV, DV, SV = Pf(CC, YY), Df(CC, YY), Sf(CC, YY)
bad = (PV > 0) & (DV > 0) & (SV > 0)
stall = (PV >= 0) & (DV >= 0) & (SV >= 0)
print("grid %dx%d: triple>0 (BAD) count = %d, triple>=0 (stall cand) = %d"
      % (len(cgrid), len(ygrid), bad.sum(), stall.sum()))
if bad.any():
    idx = np.argwhere(bad)
    print("  bad sample pts:", [(round(cgrid[i[1]], 3), round(ygrid[i[0]], 3))
                                for i in idx[:: max(1, len(idx)//8)][:8]])
# where is P>0?
print("P>0 fraction: %.3f | P'>0 fraction: %.3f | P''>0 fraction: %.3f"
      % ((PV > 0).mean(), (DV > 0).mean(), (SV > 0).mean()))
# the witness structure: which of the three is <= 0 where P>0
pw = (PV > 0)
print("on {P>0}: P'<=0 frac %.3f, P''<=0 frac %.3f" %
      ((DV[pw] <= 0).mean() if pw.any() else -1,
       (SV[pw] <= 0).mean() if pw.any() else -1))

# the curve P=0: Delta(lam*, y) > 0 region and the roots c±(y)
Acf = sp.lambdify(ys, sp.Poly(P1core, cs).all_coeffs()[0].subs(ls, lam0), 'numpy')
Bcf = sp.lambdify(ys, sp.Poly(P1core, cs).all_coeffs()[1].subs(ls, lam0), 'numpy')
Ccf = sp.lambdify(ys, sp.Poly(P1core, cs).all_coeffs()[2].subs(ls, lam0), 'numpy')
yy = ygrid
a_v, b_v, c_v = Acf(yy), Bcf(yy), Ccf(yy)
disc = b_v**2 - 4 * a_v * c_v
pos = disc > 0
print("Delta(lam*,y)>0 y-range:", (yy[pos].min(), yy[pos].max()) if pos.any() else "EMPTY",
      "| count", pos.sum(), "| max disc", disc.max())
if pos.any():
    for yv in yy[pos][:: max(1, pos.sum()//6)][:6]:
        a, b, cc = Acf(yv), Bcf(yv), Ccf(yv)
        r1 = (-b + np.sqrt(b * b - 4 * a * cc)) / (2 * a)
        r2 = (-b - np.sqrt(b * b - 4 * a * cc)) / (2 * a)
        # evaluate P', P'' at these curve points
        print("   y=%.4f: c-roots (%.4f, %.4f): P'=(%.3f, %.3f) P''=(%.3f, %.3f)"
              % (yv, r1, r2, Df(r1, yv), Df(r2, yv), Sf(r1, yv), Sf(r2, yv)))
# near the optimum
c0, y0 = 0.3971072873503973695456334, 0.6563224669957891081761482
for (c, y) in [(c0, y0), (c0*1.001, y0*1.001), (c0*0.999, y0*0.999),
               (c0, y0*1.0005), (c0, y0*0.9995), (0, 0.5), (2.0, 0.5),
               (-3.0, -0.7), (5.0, 0.9)]:
    print("   (c=%.4f, y=%.4f): P=%+.3e P'=%+.3e P''=%+.3e"
          % (c, y, Pf(c, y), Df(c, y), Sf(c, y)))
