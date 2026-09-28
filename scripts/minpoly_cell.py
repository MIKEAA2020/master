#!/usr/bin/env python3
"""minpoly_cell.py — the exact minimal polynomial of the cell's D(2)^2.

The line-atom reduction (line_atom.py): the eigenproblem decouples by the
gamma_1-parity into two 3x3 blocks; the top eigenvalue lives in the
gamma_1 = 1 block with an explicit CUBIC characteristic polynomial
P1(lambda, c, y). The optimum of D(2) over the line-atom family is the
stationary point: P1 = dP1/dc = dP1/dy = 0. This script computes the
elimination polynomial (the resultant chain) and factors it to extract
the MINIMAL POLYNOMIAL of lambda* = D(2)^2.
"""
import sympy as sp
import math
import os
import signal

OUT_DIR = "/home/z/my-project/github_repos/master/scripts"


def alarm(sig, frame):
    raise TimeoutError()


signal.signal(signal.SIGALRM, alarm)

cs, ys, ls = sp.symbols('c y lambda')
t = 1 - ys**2
G = sp.zeros(6, 6)
C = sp.zeros(6, 6)
mu = [1, 1, 1, 2]
Cm = [2, 1, 1, 1]
bets = [(0, 0), (1, 0), (0, 1), (1, 1)]
s1 = {(0, 0): 0, (1, 0): 1, (0, 1): 0, (1, 1): 2 * ys}
s0 = {(0, 0): 1, (1, 0): 0, (0, 1): ys, (1, 1): 0}
e0 = {(0, 0): 0, (1, 0): ys, (0, 1): 0, (1, 1): 1}
e1 = {(0, 0): 2 * ys, (1, 0): 0, (0, 1): 1, (1, 1): 0}
for i, b in enumerate(bets):
    G[i, i] = mu[i]
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
print("P1core degrees: in lambda %d, total %d" %
      (sp.Poly(P1core, ls).degree(),
       sp.Poly(P1core, ls, cs, ys).total_degree()))

# the elimination chain
r1 = sp.resultant(P1core, dPdy, ys)
print("res1 done: deg in lambda %d, in c %d" %
      (sp.Poly(r1, ls).degree(), sp.Poly(r1, cs).degree()))
r2 = sp.resultant(sp.expand(r1), sp.expand(dPdc), cs)
print("res2 done: degree in lambda %d" % sp.Poly(r2, ls).degree())
with open(os.path.join(OUT_DIR, "minpoly_r2.txt"), "w") as f:
    f.write(str(sp.Poly(r2, ls).as_expr()))
print("saved r2")

# factor with a generous alarm
try:
    signal.alarm(1500)
    fac = sp.Poly(r2, ls).factor_list()
    signal.alarm(0)
    target = 1.6310919766
    for f, m in fac[1]:
        for rt in sp.nroots(f):
            if abs(complex(rt).imag) < 1e-10 \
               and abs(complex(rt).real - target) < 1e-5:
                print()
                print("THE MINIMAL POLYNOMIAL OF lambda* (degree %d):"
                      % f.degree())
                print(f.as_expr())
                print("root: %.14f -> D(2) = sqrt(root) = %.14f"
                      % (complex(rt).real, math.sqrt(complex(rt).real)))
                with open(os.path.join(OUT_DIR, "minpoly_lambda.txt"),
                          "w") as f2:
                    f2.write(str(f.as_expr()) + "\n")
                break
except TimeoutError:
    print("factorization timed out; r2 saved for the follow-up")
