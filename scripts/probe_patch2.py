#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe_patch2.py — the clean probe: the FIXED center-eigenvector instrument.

The instrument R(v0, z) (the Rayleigh quotient of the chosen side at the
center's top eigenvector, v0 FIXED) is M-invariant (v0 = (a, b, c, c) the
lifted form on the stratum), so its transverse gradient vanishes exactly.
Measures at each base point:
  - m0 (the instrument margin at the center);
  - all 3 transverse Hessian eigenvalues (fixed instrument);
  - C3, C4 (the cubic/quartic scales at the center, central differences);
  - the DIRECT margin profile out to r = 0.12 along random directions;
  - the Taylor-vs-direct agreement at r = 0.05.
"""
import math
import numpy as np

LAMBDA_F = 1.6310919765642504414737578928177383666901925754942
C_STAR = 0.3971672569443035
Y_STAR = 0.6563248795193563

from probe_patch import (float_mats, top_evec, top_eval, rayleigh,
                         trans_params)


def probe_fixed(x0, dw, dyb, rng):
    wbar = 0.5 * (C_STAR + dw)
    ybar = Y_STAR + dyb
    z = (wbar, x0, ybar)
    G_e, C_e, G_o, C_o = float_mats(*trans_params(z, (0, 0, 0)))
    lam_e, lam_o = top_eval(C_e, G_e), top_eval(C_o, G_o)
    res = {"base": (x0, dw, dyb), "lam_e": lam_e, "lam_o": lam_o}
    best = None
    for side, (G, C) in (("o", (G_o, C_o)), ("e", (G_e, C_e))):
        v0 = top_evec(C, G)

        def R_of(dlt):
            mats = float_mats(*trans_params(z, dlt))
            Gx, Cx = (mats[2], mats[3]) if side == "o" else (mats[0], mats[1])
            return rayleigh(v0, Gx, Cx)

        m0 = R_of((0, 0, 0)) - LAMBDA_F
        # the transverse Hessian (central differences)
        h = 2e-4
        H = np.zeros((3, 3))
        for i in range(3):
            for j in range(i, 3):
                ei = np.zeros(3); ei[i] = h
                ej = np.zeros(3); ej[j] = h
                H[i, j] = (R_of(ei + ej) - R_of(ei - ej)
                           - R_of(-ei + ej) + R_of(-ei - ej)) / (4 * h * h)
                H[j, i] = H[i, j]
        evs = np.linalg.eigvalsh(H)
        # the cubic/quartic scales along 10 random directions
        c3, c4 = 0.0, 0.0
        for _ in range(10):
            u = rng.normal(size=3); u /= np.linalg.norm(u)
            hh = 6e-3
            f = [R_of(hh * k * u) for k in range(-2, 3)]
            d3 = (f[4] - 2 * f[3] + 2 * f[1] - f[0]) / (2 * hh ** 3) / 6.0
            d4 = (f[4] - 4 * f[3] + 6 * f[2] - 4 * f[1] + f[0]) / hh ** 4 / 24.0
            c3 = max(c3, abs(d3)); c4 = max(c4, abs(d4))
        # the direct margin profile + the Taylor check at r = 0.05
        prof = []
        for rr in (0.02, 0.05, 0.08, 0.12):
            worst = 1e9
            for _ in range(12):
                u = rng.normal(size=3); u /= np.linalg.norm(u)
                worst = min(worst, R_of(rr * u) - LAMBDA_F)
            prof.append((rr, worst))
        row = {"side": side, "m0": m0, "H_eigs": [float(v) for v in evs],
               "C3": c3, "C4": c4, "profile": prof}
        res[side] = row
        if best is None or m0 > best[1]:
            best = (side, m0)
    return res


rng = np.random.default_rng(11)
base_points = []
for x0 in (0.45, 0.3, 0.15):
    for (dw, dyb) in [(0.0, 0.0), (0.1, 0.0), (-0.1, 0.0),
                      (0.0, 0.05), (0.0, -0.05)]:
        base_points.append((x0, dw, dyb))

for (x0, dw, dyb) in base_points:
    r = probe_fixed(x0, dw, dyb, rng)
    for side in ("o", "e"):
        rr = r[side]
        profs = "; ".join("r=%.2f: %+.1e" % (a, b) for a, b in rr["profile"])
        print("(%.2f, %+.2f, %+.2f) %s: m0=%+.2e  H=[%s]  C3=%.1f C4=%.1f"
              % (x0, dw, dyb, side, rr["m0"],
                 ", ".join("%+.3f" % v for v in rr["H_eigs"]),
                 rr["C3"], rr["C4"]))
        print("        direct profile: %s" % profs)
    print()
