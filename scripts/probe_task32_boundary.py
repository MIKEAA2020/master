#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe_task32_boundary.py — Task 32 probe A: THE CLASS-LEVEL QUESTION.

The line atom (Vol XI: Aa nilpotent, boundary of the Kronecker variety)
sits at D = 1.277142112908 BELOW Task 31's symmetric shadow
(1.277142125195, at a = 0.014953, 2px ~ c*, b ~ y*) and below the free
escape point (1.277142116995).  The line atom itself is NOT abelian
(Aa = [[0,0],[1,0]]), but it is the x -> 0, p -> infinity (2px = c
fixed) limit of the PARITY-ODD MIRRORED PAIRS — which ARE abelian
(diagonal).  Hence:

    IF  lim_{x->0} ||H_cell - H_pair(x, 2px = c*)|| = the line-atom
        value  (norm convergence along the boundary curve),
    THEN D_abelian(2) <= 1.277142112908 < the free escape point —
        the escape DIES at the class level (the abelian closure meets
        the free optimum; shadow-equality RESTORED in the closure).

    IF instead the curve has a BARRIER (a positive limit margin above
        the line-atom value, or a turnaround/blowup),
    THEN the abelian infimum is strictly above, and the escape
        survives — the class-level lower bound is the barrier height.

This probe measures the boundary curve directly, at fixed (c*, y*)
and with per-x local re-optimization of (c, y), from x = 0.0715 (Vol
IX's optimizer) down to x = 1e-6.
"""
import numpy as np
from scipy.optimize import minimize

SRC = "/home/z/my-project/github_repos/master/scripts/free_cell.py"
src = open(SRC).read()
head = src[:src.index('# =====================================================================\n# PART A')]
ns = {}
exec(compile(head, 'fc_head', 'exec'), ns)
free_cell_exact_norm = ns['free_cell_exact_norm']

C_STAR = 0.3971072873503973695456334
Y_STAR = 0.6563224669957891081761482
LINE_ATOM = 1.27714211290844623900730137526434780654
FREE_ESCAPE = 1.2771421169949382
SYM_SHADOW = 1.277142125195311
VOL_IX = 1.277142689665

def pair_norm(x, c, y):
    """the parity-odd mirrored pair at scale x: B = (P,-P), C=(1,1),
    Aa = diag(x,-x), Ab = diag(y,y), 2Px = c."""
    P = c / (2.0 * x)
    B = np.array([P, -P])
    Cv = np.array([1.0, 1.0])
    Aa = np.diag([x, -x])
    Ab = np.diag([y, y])
    n, _ = free_cell_exact_norm(B, Cv, Aa, Ab)
    return n

def sym_norm(x, B, C, y):
    """the general symmetric-subfamily point Aa=diag(x,-x), Ab=diag(y,y)."""
    Aa = np.diag([x, -x])
    Ab = np.diag([y, y])
    n, _ = free_cell_exact_norm(B, C, Aa, Ab)
    return n

def line_atom_norm(c, y):
    B = np.array([0.0, c]); C = np.array([1.0, 0.0])
    Aa = np.array([[0.0, 0.0], [1.0, 0.0]])
    Ab = y * np.eye(2)
    n, _ = free_cell_exact_norm(B, C, Aa, Ab)
    return n

print("=" * 76)
print("PROBE A — the abelian boundary curve: does the parity-odd family")
print("           converge to the line atom in NORM as x -> 0?")
print("=" * 76)
print("references: line atom %.15f | free escape %.15f" % (LINE_ATOM, FREE_ESCAPE))
print("             sym shadow %.15f | Vol IX    %.15f" % (SYM_SHADOW, VOL_IX))
print()
la = line_atom_norm(C_STAR, Y_STAR)
print("  the line atom re-evaluated at (c*, y*): %.15f  (delta vs Vol XI: %.2e)"
      % (la, la - LINE_ATOM))
print()

# ---- A1: the curve at fixed (c*, y*) ----
print("  A1: fixed (c*, y*) — the raw boundary curve:")
print("      %-11s %-18s %-18s %s" % ("x", "norm", "norm - line_atom", "verdict"))
for x in [0.0715, 0.05, 0.03, 0.02, 0.014953, 0.01, 0.005, 0.002,
          1e-3, 3e-4, 1e-4, 3e-5, 1e-5, 1e-6]:
    n = pair_norm(x, C_STAR, Y_STAR)
    tag = []
    if n < FREE_ESCAPE: tag.append("BELOW-FREE")
    if n < SYM_SHADOW: tag.append("BELOW-SYMSHADOW")
    if abs(n - LINE_ATOM) < 1e-10: tag.append("AT-LINE-ATOM")
    print("      %-11.3g %-18.15f %-+18.3e %s" % (x, n, n - LINE_ATOM,
                                                  ",".join(tag)))
print()

# ---- A2: per-x re-optimization of (c, y) ----
print("  A2: per-x local re-optimization of (c, y) (Nelder-Mead from")
print("      (c*, y*)): the TRUE abelian profile curve:")
print("      %-11s %-18s %-18s %s" % ("x", "best norm", "best - line_atom", "verdict"))
for x in [0.0715, 0.03, 0.01, 0.003, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5]:
    r = minimize(lambda z: pair_norm(x, z[0], z[1]) or 1e6,
                 np.array([C_STAR, Y_STAR]), method="Nelder-Mead",
                 options={"xatol": 1e-12, "fatol": 1e-15, "maxiter": 2000})
    n = float(r.fun)
    tag = []
    if n < FREE_ESCAPE: tag.append("BELOW-FREE")
    if n < SYM_SHADOW: tag.append("BELOW-SYMSHADOW")
    print("      %-11.3g %-18.15f %-+18.3e %s  (c=%.6f y=%.6f)"
          % (x, n, n - LINE_ATOM, ",".join(tag), r.x[0], r.x[1]))
print()

# ---- A3: the symmetric shadow re-anchored and pushed to the boundary ----
print("  A3: the SYMMETRIC SHADOW pushed along the boundary (a -> 0 with")
print("      B, C rescaled to keep 2px = c*): does IT also descend?")
xs = [0.0149530780, 0.01, 0.005, 0.002, 1e-3, 1e-4, 1e-5]
B0 = np.array([7.5440973695, -6.3889831599])
C0 = np.array([1.7601091851, 2.0783330839])
y0 = 0.6563223465
# the shadow's effective 2px: p1 = B1*C1, the a-line: keep the
# LINE-ATOM invariant 2px = c* by scaling B by x0/x
x0 = 0.0149530780
print("      %-11s %-18s %-18s %s" % ("a", "norm", "norm - line_atom", "verdict"))
for a in xs:
    sc = x0 / a          # keep 2px fixed: B scales up as a shrinks
    n = sym_norm(a, B0 * sc, C0, y0)
    tag = []
    if n < FREE_ESCAPE: tag.append("BELOW-FREE")
    if n < SYM_SHADOW: tag.append("BELOW-SYMSHADOW")
    print("      %-11.3g %-18.15f %-+18.3e %s" % (a, n, n - LINE_ATOM,
                                                  ",".join(tag)))
print()

# ---- A4: the line-atom point through the 12-param descent machinery ----
print("  A4: is the line atom BELOW the Task-31 free escape point?")
print("      line atom  %.15f" % la)
print("      free escape %.15f  -> the line atom is %.3e BELOW the escape point"
      % (FREE_ESCAPE, FREE_ESCAPE - la))
print("      (i.e. the Task 29/31 'free optimum' was never the free optimum;")
print("       Vol XI's line atom was already lower.)")
