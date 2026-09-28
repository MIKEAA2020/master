#!/usr/bin/env python3
"""minpoly_cell2.py — the CORRECT elimination chain for lambda*'s polynomial.
Chain: R1 = res_y(P1core, dPdy), R2 = res_y(P1core, dPdc) (both in (lambda, c));
r2 = res_c(R1, R2) (univariate in lambda). Then the LLL-guess + exact
division proof."""
import sympy as sp
from fractions import Fraction
import mpmath as mp
import math
import json

# ---- the cubic + derivatives ------------------------------------------------
cs, ys, ls = sp.symbols('c y lambda')
t = 1 - ys**2
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
idx1 = [1, 3, 4]
A1 = sp.Matrix(3, 3, lambda i, j: A[idx1[i], idx1[j]])
den = sp.Integer(1)
for e in A1:
    n, d = sp.fraction(sp.together(e))
    den = sp.lcm(den, d)
A1c = sp.expand(A1 * den)
P1 = sp.expand((A1c - ls * den * sp.eye(3)).det())
P1core = sp.expand(sp.cancel(P1 / ((ys**2 - 1)**6)))
dPdc = sp.diff(P1core, cs)
dPdy = sp.diff(P1core, ys)
print("core cubic built (deg in lambda: %d)" % sp.Poly(P1core, ls).degree())

# ---- the correct elimination chain -------------------------------------------
R1 = sp.resultant(P1core, dPdy, ys)
print("R1: deg lambda %d, deg c %d" % (sp.Poly(R1, ls).degree(),
                                       sp.Poly(R1, cs).degree()))
R2 = sp.resultant(P1core, dPdc, ys)
print("R2: deg lambda %d, deg c %d" % (sp.Poly(R2, ls).degree(),
                                       sp.Poly(R2, cs).degree()))
g = sp.gcd(R1, R2)
if g != 1 and g != 0:
    print("common factor of degree", sp.Poly(g, ls, cs).total_degree())
r2 = sp.resultant(sp.expand(R1), sp.expand(R2), cs)
P_r2 = sp.Poly(r2, ls)
print("r2: degree in lambda =", P_r2.degree())
assert P_r2.gens == (ls,), "not univariate!"
r2 = sp.expand(sp.cancel(r2))
P_r2 = sp.Poly(r2, ls)
sq = sp.Poly(sp.cancel(r2 / sp.gcd(r2, sp.diff(r2, ls))), ls)
print("squarefree part degree:", sq.degree())
with open("/home/z/my-project/github_repos/master/scripts/"
          "minpoly_r2v2.txt", "w") as f:
    f.write(str(r2))
print("saved r2v2")

# ---- the high-precision stationary point --------------------------------------
mp.mp.dps = 200
fP = sp.lambdify((ls, cs, ys), P1core, 'mpmath')
fc = sp.lambdify((ls, cs, ys), dPdc, 'mpmath')
fy = sp.lambdify((ls, cs, ys), dPdy, 'mpmath')
sol = mp.findroot(lambda l_, c_, y_: (fP(l_, c_, y_), fc(l_, c_, y_),
                                       fy(l_, c_, y_)),
                  (mp.mpf('1.63109'), mp.mpf('0.397106'),
                   mp.mpf('0.656317')), tol=mp.mpf('1e-90'),
                  maxsteps=100)
lam = sol[0]
print("lambda* (50 digits):", mp.nstr(lam, 50))

# sanity: r2 vanishes at lambda*
r2f = sp.lambdify(ls, r2, 'mpmath')
print("r2(lambda*) =", mp.nstr(r2f(lam), 5))

# ---- the LLL relation search (incremental exact) --------------------------------


def lll(basis, delta=Fraction(3, 4)):
    n = len(basis)
    m = len(basis[0])
    B = [list(map(int, row)) for row in basis]
    mu = [[Fraction(0)] * n for _ in range(n)]
    bs = [[Fraction(0)] * m for _ in range(n)]
    c = [Fraction(0)] * n
    for i in range(n):
        bs[i] = [Fraction(x) for x in B[i]]
        for j in range(i):
            num = sum(bs[i][k] * bs[j][k] for k in range(m))
            den2 = c[j]
            mu[i][j] = num / den2 if den2 != 0 else Fraction(0)
            bs[i] = [bs[i][k] - mu[i][j] * bs[j][k] for k in range(m)]
        c[i] = sum(x * x for x in bs[i])
    k = 1
    steps = 0
    while k < n:
        steps += 1
        if steps > 40000:
            break
        for j in range(k - 1, -1, -1):
            if abs(mu[k][j]) > Fraction(1, 2):
                r = mu[k][j]
                rr = r.numerator // r.denominator
                if r - rr > Fraction(1, 2):
                    rr += 1
                if rr != 0:
                    B[k] = [B[k][q] - rr * B[j][q] for q in range(m)]
                    for i2 in range(j):
                        mu[k][i2] -= rr * mu[j][i2]
                    mu[k][j] -= rr
        if c[k] >= (delta - mu[k][k - 1] ** 2) * c[k - 1]:
            k += 1
        else:
            mval = mu[k][k - 1]
            B[k], B[k - 1] = B[k - 1], B[k]
            if mval == 0:
                for j in range(k - 1):
                    mu[k][j], mu[k - 1][j] = mu[k - 1][j], mu[k][j]
                c[k], c[k - 1] = c[k - 1], c[k]
            else:
                Bnew = c[k] + mval ** 2 * c[k - 1]
                mu[k][k - 1] = mval * c[k - 1] / Bnew
                cnew_k = c[k] * c[k - 1] / Bnew
                c[k - 1] = Bnew
                c[k] = cnew_k
                for j in range(k - 1):
                    tt = mu[k - 1][j]
                    mu[k - 1][j] = mu[k][j] - mval * tt
                    mu[k][j] = tt + mu[k][k - 1] * mu[k - 1][j]
            k = max(k - 1, 1)
    return B


def find_relation(lam, DEG, PREC=170):
    mp.mp.dps = PREC + 40
    pows = [lam**k for k in range(DEG + 1)]
    X = mp.mpf(10) ** PREC
    rows = []
    for k, p in enumerate(pows):
        row = [int(mp.nint(X * p))] + [1 if j == k else 0
                                       for j in range(DEG + 1)]
        rows.append(row)
    L = lll(rows)
    out = []
    for r in L:
        if abs(r[0]) > 10**15:
            continue
        coeffs = r[1:]
        if all(a == 0 for a in coeffs):
            continue
        g = 0
        for a in coeffs:
            g = math.gcd(g, abs(a))
        if g == 0:
            continue
        cc = [a // g for a in coeffs]
        while cc and cc[-1] == 0:
            cc.pop()
        if len(cc) < 2:
            continue
        if cc[-1] < 0:
            cc = [-a for a in cc]
        val = sum(mp.mpf(a) * lam**k for k, a in enumerate(cc))
        if abs(val) < mp.mpf(10) ** (-PREC // 3):
            out.append(cc)
    return out


# the degree of the target is unknown; search from small degrees upward
found = None
for deg in range(2, 13):
    cands = find_relation(lam, deg, PREC=120)
    if cands:
        found = cands[0]
        print("relation at degree", deg)
        break
if found is None:
    # one big search at a higher degree
    cands = find_relation(lam, 20, PREC=180)
    if cands:
        found = cands[0]
        print("relation at degree 20 search")
if found is None:
    print("no relation found; r2v2 saved for external factoring")
    raise SystemExit

cand = sp.Poly(found, ls)
print("candidate (degree %d, max coeff %d):" %
      (cand.degree(), max(abs(a) for a in found)))
print(cand.as_expr())

# ---- the PROOF ----------------------------------------------------------------
q, rem = divmod(P_r2, cand)
print("divides r2 exactly:", rem.is_zero)
if rem.is_zero:
    roots = [complex(r) for r in sp.nroots(cand)]
    rroots = sorted([r.real for r in roots if abs(r.imag) < 1e-15],
                    reverse=True)
    print("real roots:", [round(r, 12) for r in rroots])
    top = rroots[0]
    print("lambda* = %.15f" % top)
    print("D(2) = sqrt(lambda*) = %.15f" % math.sqrt(top))
    with open("/home/z/my-project/github_repos/master/scripts/"
              "minpoly_facts.json", "w") as f:
        json.dump({
            "lambda_star_50_digits": mp.nstr(lam, 50),
            "c_star": mp.nstr(sol[1], 25),
            "y_star": mp.nstr(sol[2], 25),
            "minimal_polynomial": str(cand.as_expr()),
            "degree": cand.degree(),
            "max_coeff": max(abs(a) for a in found),
            "divides_resultant_exactly": True,
            "D2_sqrt": math.sqrt(top),
            "real_roots": rroots}, f, indent=1)
    print("saved minpoly_facts.json")
