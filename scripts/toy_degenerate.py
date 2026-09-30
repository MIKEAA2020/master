#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""toy_degenerate.py — validate the degenerate second-order formula on a
toy symmetric pencil with a double top: M(t) = M0 + t A + t^2 B (N = I).
Theory: lam(t) = lam0 + lam_max( t V'AV + t^2 ( V'BV/2... wait — with the
parametrization M(t) = M0 + tA + tB2 t^2 (B2 = the quadratic coefficient):
lam(t) = lam0 + lam_max( t*V'AV + t^2*( V'B2 V + VA(m')(m'AV ...
Direct: eigvalsh(M(t))[-1]."""
import numpy as np

rng = np.random.default_rng(5)

n = 6
# a symmetric M0 with a double top
Q = np.linalg.qr(rng.normal(size=(n, n)))[0]
M0 = Q @ np.diag([0.3, 0.5, 0.9, 1.2, 2.0, 2.0]) @ Q.T
M0 = 0.5 * (M0 + M0.T)
lam0 = 2.0
w, V = np.linalg.eigh(M0)
Vtop = V[:, -2:]
Vm = V[:, :-2]
w_m = w[:-2]
D = np.diag(w_m - lam0)             # negative

A = rng.normal(size=(n, n))
A = 0.5 * (A + A.T)
B2 = rng.normal(size=(n, n))        # the t^2 coefficient (not 1/2 of it)
B2 = 0.5 * (B2 + B2.T)


def M_of_t(t):
    return M0 + t * A + (t * t) * B2


def lam_direct(t):
    return float(np.linalg.eigvalsh(M_of_t(t))[-1])


# the theory: mu = eig of [ t*V'AV + t^2*( V'B2V + V'A Vm D^-1 Vm' A V ) ]
# (note: M = M0 + tA + t^2 B2 -> M^1(e) = A, M^2(e,e) = 2 B2 -> core
#  = (1/2) V' M^2 V = V' B2 V)
rep = Vtop.T @ A @ Vm @ np.linalg.inv(D) @ Vm.T @ A @ Vtop


def lam_theory(t):
    Mm = t * (Vtop.T @ A @ Vtop) + (t * t) * (
        Vtop.T @ B2 @ Vtop - rep)
    return lam0 + float(np.linalg.eigvalsh(Mm)[-1])


print(" t        direct              theory             diff")
for t in (1e-3, 3e-3, 1e-2, 3e-2, 0.1):
    d, th = lam_direct(t), lam_theory(t)
    print("  %.4f  %.12f  %.12f  %+.2e" % (t, d, th, d - th))

# also check with the FD-style extraction (as in the battery): the M^1 and
# M^2 from central differences of M_of_t
def M1_fd(t=1e-5):
    return (M_of_t(t) - M_of_t(-t)) / (2 * t)


def M2_fd(t=3e-4):
    return (M_of_t(t) - 2 * M0 + M_of_t(-t)) / (t * t)


M1x = M1_fd()
M2x = M2_fd()
print("FD accuracy: |M1-A| %.2e, |M2-2B2| %.2e" %
      (np.linalg.norm(M1x - A), np.linalg.norm(M2x - 2 * B2)))

rep_fd = Vtop.T @ M1x @ Vm @ np.linalg.inv(D) @ Vm.T @ M1x @ Vtop


def lam_theory_fd(t):
    Mm = t * (Vtop.T @ M1x @ Vtop) + (t * t) * (
        0.5 * Vtop.T @ M2x @ Vtop - rep_fd)
    return lam0 + float(np.linalg.eigvalsh(Mm)[-1])


print(" t        direct          theory(FD)")
for t in (1e-3, 3e-2):
    print("  %.4f  %.12f  %.12f  %+.2e" %
          (t, lam_direct(t), lam_theory_fd(t),
           lam_direct(t) - lam_theory_fd(t)))
