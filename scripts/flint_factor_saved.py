#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""flint_factor_saved.py — external factoring (FLINT) of the saved degree-1154
resultant artifact minpoly_r2v3.txt (the naive elimination of the saved cubic
stationarity system). Census: squarefree part, irreducible factors, degrees,
real roots, and which factor carries lambda*.
"""
import json
import re
import sys
import time

from flint import fmpz_poly

SRC = "/home/z/my-project/github_repos/master/scripts/minpoly_r2v3.txt"
OUT = "/home/z/my-project/github_repos/master/scripts/flint_factor_saved.json"
LAM50 = 1.6310919765642504414737578928177383666901925754942

s = open(SRC).read().strip()
print("loaded artifact: %d chars" % len(s))

# parse "NUM*lambda**k + NUM*lambda**j ... (+ CONST)"  (signs may have spaces)
terms = {}
for sign, num, k in re.findall(r'([+-])\s*(\d+)\*lambda\*\*(\d+)', '+' + s):
    terms[int(k)] = int(sign + num)
m = re.search(r'([+-])\s*(\d+)\s*$', s)
if m and 'lambda' not in s[m.start():]:
    terms[0] = terms.get(0, 0) + int(m.group(1) + m.group(2))
deg = max(terms)
n_missing = sum(1 for k in range(deg + 1) if k not in terms)
print("parsed: degree %d, %d terms present, %d zero coeffs" %
      (deg, len(terms), n_missing))
coeffs = [terms.get(k, 0) for k in range(deg + 1)]
p = fmpz_poly(coeffs)
print("fmpz_poly built; leading coeff digits:", len(str(abs(coeffs[deg]))))

t0 = time.time()
pp = p.derivative()
g = p.gcd(pp)
print("gcd(p, p') degree:", g.degree(), "  [%.1fs]" % (time.time() - t0))
psq = p // g
print("squarefree part degree:", psq.degree())

t0 = time.time()
fac = psq.factor()
print("factor() done in %.1fs" % (time.time() - t0))
print("factor() returns type:", type(fac))
try:
    content, pairs = fac
except Exception:
    pairs = fac
    content = None

import sympy as sp
x = sp.symbols('x')
census = []
for item in pairs:
    if isinstance(item, tuple) and len(item) == 2:
        f, e = item
    else:
        f, e = item, 1
    fl = [int(c) for c in f.coeffs()] if hasattr(f, 'coeffs') else None
    if fl is None:
        fl = list(f)
    d = len(fl) - 1
    ent = {"degree": d, "exp": int(e)}
    spf = sp.Poly(fl[::-1], x)   # fl is ascending -> reverse for sympy
    rroots = spf.intervals()          # [((a, b), mult), ...]
    ent["n_real_roots"] = len(rroots)
    ent["real_roots_intervals"] = [[str(a), str(b)] for (a, b), _ in rroots]
    hit = any(sp.Rational(a) < sp.Rational(LAM50).limit_denominator(10**40)
              < sp.Rational(b) for (a, b), _ in rroots)
    ent["contains_lambda_star"] = bool(hit)
    if d <= 60:
        ent["coeffs_desc"] = [str(c) for c in fl[::-1]]
    census.append(ent)
    if hit:
        lo_, hi_ = sp.Rational(rroots[0][0][0]), sp.Rational(rroots[0][0][1])
        for _ in range(80):
            mid = (lo_ + hi_) / 2
            if spf.eval(lo_) * spf.eval(mid) <= 0:
                hi_ = mid
            else:
                lo_ = mid
        print("  factor: degree %d (x%d), %d real roots  <<< contains "
              "lambda*: root = %.15f" % (d, e, len(rroots),
                                         float((lo_ + hi_) / 2)))
    else:
        print("  factor: degree %d (x%d), %d real roots" %
              (d, e, len(rroots)))

with open(OUT, "w") as f:
    json.dump({"source": "minpoly_r2v3.txt (degree %d)" % deg,
               "squarefree_degree": int(psq.degree()),
               "gcd_with_derivative_degree": int(g.degree()),
               "census": census}, f, indent=1)
print("saved", OUT)
