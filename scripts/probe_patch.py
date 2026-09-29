#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe_patch.py — the design probe for Task 26 (the analytic patch).

Measures, at the 15 P3 base points, in the 3 transverse (mirror-breaking)
coordinates delta = (w1-w2)/2, (x1+x2)/2, (y1-y2)/2:

  m0      the instrument margin R(v0, z0) - lambda*  (the Rayleigh value
          at the center eigenvector = the eigenvalue up to float eps);
  kappa_R the min eigenvalue of the 3x3 transverse Hessian of the
          instrument R(v(delta), z(delta)) at delta = 0, for the FIXED
          vector (B = 0) and the AFFINE-TRACKED vector (B = the
          eigenvector's central-difference derivative);
  C3, C4  the cubic and quartic derivative scales of the instrument at
          the center (finite differences);
  phi(r)  the patch certificate profile
          m0 - gamma*r + (kappa/2) r^2 - C3*r^3 - C4*r^4
          evaluated at the P3 core radius r = 0.021.

Pure floats (measurement, not certificate).  Decides the patch design.
"""
import math
import numpy as np

LAMBDA_F = 1.6310919765642504414737578928177383666901925754942
C_STAR = 0.3971672569443035
Y_STAR = 0.6563248795193563


def float_mats(w1, x1, y1, w2, x2, y2):
    p1 = w1 / x1 if x1 != 0 else 0.0
    p2 = w2 / x2 if x2 != 0 else 0.0
    def D(i, j):
        xs = (x1, x2)[i] * (x1, x2)[j]
        ys = (y1, y2)[i] * (y1, y2)[j]
        return (1.0 - ys) ** 2 - xs * xs
    d11, d12, d22 = D(0, 0), D(0, 1), D(1, 1)
    Q = np.array([[(1 - y1 * y1) / d11, (1 - y1 * y2) / d12],
                  [(1 - y2 * y1) / d12, (1 - y2 * y2) / d22]])
    R = np.array([[1.0 / d11, 1.0 / d12], [1.0 / d12, 1.0 / d22]])
    G_e = np.array([[1, 0, 1, 1], [0, 1, y1, y2],
                    [1, y1, Q[0, 0], Q[0, 1]], [1, y2, Q[1, 0], Q[1, 1]]])
    P = np.array([[p1 * p1 * (Q[0, 0] + x1 * x1 * R[0, 0]),
                   p1 * p2 * (Q[0, 1] + x1 * x2 * R[0, 1])],
                  [p2 * p1 * (Q[1, 0] + x2 * x1 * R[1, 0]),
                   p2 * p2 * (Q[1, 1] + x2 * x2 * R[1, 1])]])
    C_e = np.array([[2, 0, -2 * p1 * x1 * y1, -2 * p2 * x2 * y2],
                    [0, 1, -p1 * x1, -p2 * x2],
                    [-2 * p1 * x1 * y1, -p1 * x1, P[0, 0], P[0, 1]],
                    [-2 * p2 * x2 * y2, -p2 * x2, P[0, 1], P[1, 1]]])
    G_o = np.array([[2, 0, 2 * y1, 2 * y2], [0, 1, 1, 1],
                    [2 * y1, 1, R[0, 0], R[0, 1]],
                    [2 * y2, 1, R[1, 0], R[1, 1]]])
    S = np.array([[w1 * w1 * (Q[0, 0] + x1 * x1 * R[0, 0]),
                   w1 * w2 * (Q[0, 1] + x1 * x2 * R[0, 1])],
                  [w2 * w1 * (Q[1, 0] + x2 * x1 * R[1, 0]),
                   w2 * w2 * (Q[1, 1] + x2 * x2 * R[1, 1])]])
    C_o = np.array([[1, 0, -w1, -w2],
                    [0, 1, -w1 * y1, -w2 * y2],
                    [-w1, -w1 * y1, S[0, 0], S[0, 1]],
                    [-w2, -w2 * y2, S[0, 1], S[1, 1]]])
    return G_e, C_e, G_o, C_o


def top_evec(C, G):
    A = C @ G
    ev, V = np.linalg.eig(A)
    idx = max(range(4), key=lambda i: float(np.real(ev[i])))
    v = np.real(V[:, idx])
    nrm = math.sqrt(abs(float(v @ G @ v)))
    if nrm < 1e-300:
        nrm = np.linalg.norm(v)
    return v / nrm


def top_eval(C, G):
    A = C @ G
    return max(float(np.real(e)) for e in np.linalg.eigvals(A))


def rayleigh(v, G, C):
    GCG = G @ C @ G
    return float(v @ GCG @ v) / float(v @ G @ v)


def trans_params(z, dlt):
    """z = (wbar, x0, ybar, dw, dyb) base; dlt the 3 transverse coords.
    Returns (w1, x1, y1, w2, x2, y2)."""
    wbar, x0, ybar = z
    s1, s2, s3 = dlt
    return (wbar + 0.5 * s1, x0 + 0.5 * s2, ybar + 0.5 * s3,
            wbar - 0.5 * s1, -x0 + 0.5 * s2, ybar - 0.5 * s3)


def probe_base(x0, dw, dyb):
    wbar = 0.5 * (C_STAR + dw)
    ybar = Y_STAR + dyb
    z = (wbar, x0, ybar)
    G_e, C_e, G_o, C_o = float_mats(*trans_params(z, (0, 0, 0)))
    lam_e, lam_o = top_eval(C_e, G_e), top_eval(C_o, G_o)
    side = "o" if lam_o >= lam_e else "e"
    G, C = (G_o, C_o) if side == "o" else (G_e, C_e)
    v0 = top_evec(C, G)

    def R_of(dlt, v):
        Gx, Cx = (float_mats(*trans_params(z, dlt))[2:4] if side == "o"
                  else float_mats(*trans_params(z, dlt))[:2])
        return rayleigh(v, Gx, Cx)

    # m0: the Rayleigh at the center eigenvector (fixed)
    m0_fixed = R_of((0, 0, 0), v0) - LAMBDA_F

    # the eigenvector's derivative B (central differences)
    hB = 1e-5
    B = np.zeros((4, 3))
    for i in range(3):
        dp = np.zeros(3); dp[i] = hB
        vp = top_evec(*((float_mats(*trans_params(z, dp))[2:4] if side == "o"
                         else float_mats(*trans_params(z, dp))[:2]))) if False else top_evec(
            *(float_mats(*trans_params(z, dp))[2:4] if side == "o"
              else float_mats(*trans_params(z, dp))[:2]))
        vm = top_evec(*(float_mats(*trans_params(z, -dp))[2:4] if side == "o"
                        else float_mats(*trans_params(z, -dp))[:2]))
        B[:, i] = (vp - vm) / (2 * hB)

    def v_tracked(dlt):
        return v0 + B @ np.asarray(dlt)

    # the transverse Hessian (central differences) for both instruments
    def hessian(instr):
        h = 2e-4
        H = np.zeros((3, 3))
        for i in range(3):
            for j in range(i, 3):
                ei = np.zeros(3); ei[i] = h
                ej = np.zeros(3); ej[j] = h
                vpp = instr(ei + ej); vpm = instr(ei - ej)
                vmp = instr(-ei + ej); vmm = instr(-ei - ej)
                H[i, j] = (vpp - vpm - vmp + vmm) / (4 * h * h)
                H[j, i] = H[i, j]
        return H

    H_fixed = hessian(lambda d: R_of(d, v0))
    H_track = hessian(lambda d: R_of(d, v_tracked(d)))
    m0_track = R_of((0, 0, 0), v_tracked((0, 0, 0))) - LAMBDA_F

    # the gradient of the tracked instrument (should be ~0: envelope)
    def gradient(instr):
        h = 1e-5
        g = np.zeros(3)
        for i in range(3):
            dp = np.zeros(3); dp[i] = h
            g[i] = (instr(dp) - instr(-dp)) / (2 * h)
        return g
    g_track = gradient(lambda d: R_of(d, v_tracked(d)))

    # the cubic/quartic scale: 4th differences along random unit dirs
    rng = np.random.default_rng(7)
    c3, c4 = 0.0, 0.0
    for _ in range(8):
        u = rng.normal(size=3); u /= np.linalg.norm(u)
        h = 5e-3
        f = [R_of(h * k * u, v_tracked(h * k * u)) for k in range(-2, 3)]
        # 4th difference / h^4 ~ D4; 3rd difference / h^3 ~ D3
        d3 = (f[4] - 2 * f[3] - 0 * f[2] + 2 * f[1] - f[0]) / (2 * h ** 3)
        d4 = (f[4] - 4 * f[3] + 6 * f[2] - 4 * f[1] + f[0]) / h ** 4
        c3 = max(c3, abs(d3) / 6.0)
        c4 = max(c4, abs(d4) / 24.0)
    return {"base": (x0, dw, dyb), "side": side, "lam_o": lam_o,
            "m0": m0_fixed, "m0_track": m0_track,
            "kappa_fixed": float(np.linalg.eigvalsh(H_fixed)[0]),
            "kappa_track": float(np.linalg.eigvalsh(H_track)[0]),
            "gmax": float(np.max(np.abs(g_track))),
            "C3": c3, "C4": c4,
            "H_track_eigs": [float(v) for v in np.linalg.eigvalsh(H_track)]}


base_points = []
for x0 in (0.45, 0.3, 0.15):
    for (dw, dyb) in [(0.0, 0.0), (0.1, 0.0), (-0.1, 0.0),
                      (0.0, 0.05), (0.0, -0.05)]:
        base_points.append((x0, dw, dyb))

print("%-18s %5s %10s %10s %10s %10s %8s %8s %8s" %
      ("base", "side", "m0", "m0_track", "kap_fix", "kap_trk",
       "gmax", "C3", "C4"))
rows = []
for (x0, dw, dyb) in base_points:
    r = probe_base(x0, dw, dyb)
    rows.append(r)
    print("%-18s %5s %10.2e %10.2e %10.3f %10.3f %8.1e %8.1f %8.1f" %
          ("(%.2f, %+.2f, %+.2f)" % (x0, dw, dyb), r["side"], r["m0"],
           r["m0_track"], r["kappa_fixed"], r["kappa_track"],
           r["gmax"], r["C3"], r["C4"]))

# the phi profile at the P3 core radius for the hardest bases
print()
print("phi(r) = m0 - g*r + (kappa/2) r^2 - C3 r^3 - C4 r^4  (tracked):")
for r in rows:
    if r["base"][0] == 0.15 and r["base"][1] == 0.0 and r["base"][2] == 0.0:
        for rad in (0.01, 0.021, 0.03, 0.05):
            phi = (r["m0_track"] - r["gmax"] * rad
                   + 0.5 * r["kappa_track"] * rad ** 2
                   - r["C3"] * rad ** 3 - r["C4"] * rad ** 4)
            print("  base (0.15, 0, 0): phi(%.3f) = %+.3e" % (rad, phi))
        break
