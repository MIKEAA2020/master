#!/usr/bin/env python3
"""Task 8-d: repair and complete the n=4 scan.

Defect found: for sectors whose top is NOT the global top (std, two,
stdsgn, sgn -- and the second triv eigenvalue), the Lanczos can escape
the sector once the sector top's VALUE approaches the global top lambda_1
(near the record-phase boundary): rounding noise along the v1 direction is
amplified by the 1/beta normalization, and with proj_every = 3 the periodic
re-projection no longer keeps up.  Consequence: X_8 erratic for p >~ 0.375
and the (6,8) crossing biased low.  lambda_1 solves are immune (the triv
sector contains the global top).

Fix: DEFLATED MATVEC  mv_d(x) = Op x - lambda_1 (x.v1) v1  -- removes the
escape channel exactly and leaves every other sector's spectrum untouched;
plus per-step sector re-projection.  Verified at m=2 against the dense
reference; the L=8 std values then match the power-iteration values.

This script: (1) rebuilds the L=8 grid (lambda_1, lambda_sigma, lambda_eps
at 0.383), multiplet at p=0.36, crossings, R, slope; (2) runs the L=10 leg
(float32, 4 points + lambda_eps at 0.383); (3) updates the results JSON in
place; (4) regenerates the figure via stage F.
"""
import json
import time

import numpy as np
from scipy.interpolate import CubicSpline

from pscan_n4 import Problem, bond_W, D, lanczos_sector, X_of

JSON = "/home/z/my-project/scripts/pscan_n4_results.json"


def log(*a):
    print(*a)
    import sys
    sys.stdout.flush()


def converge_v1(pr, W, v0, iters=500, tol=1e-13):
    """power iteration for the global top (triv sector -- immune)."""
    mv = lambda v: pr.matvec(v, W)
    v = v0 / np.linalg.norm(v0)
    for i in range(iters):
        w = mv(v)
        nw = np.linalg.norm(w)
        if nw < 1e-30:
            break
        v2 = w / nw
        if np.linalg.norm(v2 - v) < tol:
            v = v2
            break
        v = v2
    return v, float(v @ mv(v))


def sector_top_deflated(pr, W, v1, lam1, sector, pair, v0=None, k=1,
                        max_steps=60, tol=1e-9):
    """top of an isotypic sector (or the 2nd triv) with the deflated matvec."""
    mv = lambda x: pr.matvec(x, W) - lam1 * float(x @ v1) * v1
    if v0 is None:
        v0 = pr.starts[sector].copy()
    # orthogonalize the start to v1 (for the 2nd-triv use especially)
    v0 = v0 - float(v0 @ v1) * v1
    proj = lambda x: pr._project(x, pair[0], pair[1])
    return lanczos_sector(mv, v0, k=k, max_steps=max_steps, tol=tol,
                          project=proj, proj_every=1, cycles=3)


def main():
    R = json.load(open(JSON))
    sc = R["scan"]
    g6 = sc["grids"]["6"]
    X6 = np.array(sc["Xs"]["6"])

    # ---------------- L=8 rebuild ----------------
    log("=" * 70)
    log("L=8 REBUILD (deflated sector solver)")
    log("=" * 70)
    pr = Problem(4, 4)
    g8 = sc["grids"]["8"]
    lam = sc["lams"]["8"]
    t0 = time.time()
    v1_warm = pr.starts["triv"].copy()
    std_warm = None
    new_rows = []
    done = {}
    try:
        import os
        if os.path.exists("/home/z/my-project/scripts/repair_seed.json"):
            sd = json.load(open("/home/z/my-project/scripts/repair_seed.json"))
            done = {float(k): tuple(v) for k, v in sd.items()}
            log(f"  resuming with {len(done)} seeded L=8 rows")
    except Exception:
        done = {}
    for p in g8:
        if p in done:
            new_rows.append((p, done[p][0], done[p][1]))
            continue
        W, _ = bond_W(pr.Sg, D, p)
        v1, lam1 = converge_v1(pr, W, v1_warm)
        v1_warm = v1
        vals, vec = sector_top_deflated(pr, W, v1, lam1, "std", ("std", "std"),
                                        v0=std_warm)
        std_warm = vec
        new_rows.append((p, lam1, vals[0]))
        log(f"  p={p}: l1={lam1:.10f} lsig={vals[0]:.10f} "
            f"X={X_of(lam1, vals[0], 8):.4f}  [{time.time()-t0:.0f}s]")
    # cross-check against power iteration at three points
    lsig_map = {r[0]: r[2] for r in new_rows}
    for p in [0.375, 0.381, 0.383]:
        W, _ = bond_W(pr.Sg, D, p)
        u = pr.starts["std"].copy()
        u = u / np.linalg.norm(u)
        mv = lambda v: pr.matvec(v, W)
        for i in range(600):
            w = mv(u)
            nw = np.linalg.norm(w)
            u2 = w / nw
            if np.linalg.norm(u2 - u) < 1e-13:
                u = u2
                break
            u = u2
        pw = float(u @ mv(u))
        log(f"  power-vs-deflated check p={p}: deflated "
            f"{lsig_map[p]:.10f} vs power {pw:.10f} "
            f"(dev {abs(lsig_map[p]-pw):.2e})")
    # lambda_eps at 0.383 via deflated triv
    W, _ = bond_W(pr.Sg, D, 0.383)
    v1, lam1 = converge_v1(pr, W, pr.starts["triv"].copy())
    vals_eps, _ = sector_top_deflated(pr, W, v1, lam1, "triv",
                                      ("triv", "triv"),
                                      v0=pr.starts["triv"].copy())
    lam_eps = vals_eps[0]
    log(f"  lambda_eps(0.383) = {lam_eps:.10f}; ratio {lam_eps/lam1:.4f}; "
        f"L ln(l1/leps) = {8*np.log(lam1/lam_eps):.2f}  [manuscript: 5.2]")
    # multiplet at p=0.36, deflated
    W, _ = bond_W(pr.Sg, D, 0.36)
    v1c, lam1c = converge_v1(pr, W, pr.starts["triv"].copy())
    mult = {"triv": [lam1c]}
    for sec, pair in [("std", ("std", "std")), ("two", ("two", "two")),
                      ("stdsgn", ("std", "sgn")), ("sgn", ("sgn", "sgn"))]:
        vals, _ = sector_top_deflated(pr, W, v1c, lam1c, sec, pair)
        mult[sec] = vals
    vals_eps36, _ = sector_top_deflated(pr, W, v1c, lam1c, "triv",
                                        ("triv", "triv"),
                                        v0=pr.starts["triv"].copy())
    mult["eps36"] = vals_eps36
    # power cross-check of the mixed std x sgn sector top
    u = pr.starts["stdsgn"].copy()
    u = u / np.linalg.norm(u)
    mv36 = lambda v: pr.matvec(v, W)
    for i in range(600):
        w = mv36(u)
        nw = np.linalg.norm(w)
        if nw < 1e-30:
            break
        u2 = w / nw
        if np.linalg.norm(u2 - u) < 1e-13:
            u = u2
            break
        u = u2
    pw36 = float(u @ mv36(u))
    log(f"  std*sgn power cross-check: deflated {mult['stdsgn'][0]:.8f} vs "
        f"power {pw36:.8f} (dev {abs(mult['stdsgn'][0]-pw36):.2e})")
    log("  multiplet L=8 p=0.36 (deflated): "
        + ", ".join(f"{k}={v[0]:.8f}" for k, v in mult.items() if k != "eps36")
        + f"; eps={vals_eps36[0]:.8f}")
    order = [mult["triv"][0], mult["std"][0], mult["two"][0],
             mult["stdsgn"][0], mult["sgn"][0]]
    log(f"  ordering triv>std>two>stdsgn>sgn: {order == sorted(order, reverse=True)}"
        f"; eps below all spin: {vals_eps36[0] < min(order[1:])}")

    X8 = np.array([X_of(r[1], r[2], 8) for r in new_rows])
    spl8 = CubicSpline(g8, X8)
    spl6 = CubicSpline(g6, X6)

    def cross(f, lo, hi):
        gg = np.arange(lo, hi, 0.0002)
        vv = f(gg)
        for i in range(len(gg) - 1):
            if (vv[i] > 0) != (vv[i + 1] > 0):
                a, b, fa = gg[i], gg[i + 1], vv[i]
                for _ in range(60):
                    mid = 0.5 * (a + b)
                    fm = f(mid)
                    if (fm > 0) == (fa > 0):
                        a, fa = mid, fm
                    else:
                        b = mid
                return 0.5 * (a + b)
        return None

    lo, hi = max(g6[0], g8[0]) + 1e-6, min(g6[-1], g8[-1]) - 1e-6
    cr68 = cross(lambda t: spl6(t) - spl8(t), lo, hi)
    log(f"  crossing (6,8) rebuilt: {cr68}  [manuscript: 0.37899]")
    # X_4 crossing vs X_6 unchanged (both clean grids)
    g4 = sc["grids"]["4"]
    X4 = np.array(sc["Xs"]["4"])
    spl4 = CubicSpline(g4, X4)
    cr46 = cross(lambda t: spl4(t) - spl6(t), g4[0] + 1e-6, g4[-1] - 1e-6)
    log(f"  crossing (4,6) recheck: {cr46}  [manuscript: 0.35820]")
    # R at 0.383 for L=8
    lsig383 = {r[0]: r[2] for r in new_rows}[0.383]
    R8 = float(np.log(lam1 / lsig383) / np.log(lam1 / lam_eps))
    log(f"  R(0.383) L=8: {R8:.4f}  [manuscript: 0.2142]")

    sc["crossings"] = {"(4,6)": float(cr46), "(6,8)": float(cr68)}
    sc["R_at_0383"]["8"] = R8
    sc["lams"]["8"] = {"l1": [r[1] for r in new_rows],
                       "leps": [lam_eps if abs(r[0]-0.383) < 1e-9 else None
                                for r in new_rows],
                       "lsig": [r[2] for r in new_rows]}
    sc["Xs"]["8"] = [float(x) for x in X8]
    sc["multiplet_L8_p036"] = mult
    sc["Lln_l1leps_L8"] = float(8 * np.log(lam1 / lam_eps))
    sc["repair"] = "deflated sector solver applied to L=8"

    # ---------------- L=10 leg (float32) ----------------
    log("=" * 70)
    log("L=10 LEG (m=5, 24^5 = 7,962,624 bond labels, float32, deflated)")
    log("=" * 70)
    pr10 = Problem(4, 5, dtype=np.float32)
    pts = [0.379, 0.381, 0.383, 0.385, 0.387]
    t0 = time.time()
    v1w = pr10.starts["triv"].copy()
    stdw = None
    rows10 = []
    for p in pts:
        W, _ = bond_W(pr10.Sg, D, p, np.float32)
        v1, lam1f = converge_v1(pr10, W, v1w, iters=300, tol=1e-7)
        v1w = v1
        vals, vec = sector_top_deflated(pr10, W, v1, lam1f, "std",
                                        ("std", "std"), v0=stdw,
                                        max_steps=24, tol=3e-6)
        stdw = vec
        X = X_of(lam1f, vals[0], 10)
        rows10.append((p, float(lam1f), None, float(vals[0]), float(X)))
        log(f"  L=10 p={p}: l1={lam1f:.8f} lsig={vals[0]:.8f} X={X:.4f} "
            f"[{time.time()-t0:.0f}s]")
    # lambda_eps at 0.383
    W, _ = bond_W(pr10.Sg, D, 0.383, np.float32)
    v1, lam1f = converge_v1(pr10, W, pr10.starts["triv"].copy(), iters=300,
                            tol=1e-7)
    vals_eps, _ = sector_top_deflated(pr10, W, v1, lam1f, "triv",
                                      ("triv", "triv"),
                                      v0=pr10.starts["triv"].copy(),
                                      max_steps=24, tol=3e-6)
    lam_eps10 = vals_eps[0]
    j = [i for i, r in enumerate(rows10) if abs(r[0] - 0.383) < 1e-9][0]
    rows10[j] = (0.383, rows10[j][1], float(lam_eps10), rows10[j][3],
                 rows10[j][4])
    R10 = float(np.log(rows10[j][1] / rows10[j][3]) /
                np.log(rows10[j][1] / lam_eps10))
    log(f"  lambda_eps(0.383) L=10 = {lam_eps10:.8f}; R = {R10:.4f} "
        f"[manuscript: 0.2378]")
    spl10 = CubicSpline([r[0] for r in rows10], [r[4] for r in rows10])
    cr810 = cross(lambda t: spl8(t) - spl10(t), pts[0] + 1e-6, pts[-1] - 1e-6)
    log(f"  crossing (8,10): {cr810}  [manuscript: 0.3823]")
    # 4-point R fit
    Ls = np.array([4, 6, 8, 10], float)
    y = np.array([sc["R_at_0383"]["4"], sc["R_at_0383"]["6"],
                  sc["R_at_0383"]["8"], R10])
    Afit = np.stack([np.ones_like(Ls), 1 / np.log(Ls), 1 / np.log(Ls) ** 2], 1)
    coef, *_ = np.linalg.lstsq(Afit, y, rcond=None)
    res = np.max(np.abs(y - Afit @ coef))
    log(f"  R fit (4 pts): {coef[0]:.4f} {coef[1]:+.3f}/lnL "
        f"{coef[2]:+.3f}/ln^2L, max residual {res:.1e}  "
        f"[ms: 1/4 - 0.90/lnL + 0.46/ln^2L, resid <= 8e-4]")
    # slopes at 0.383 and exponent
    slopes = {4: float(spl4(0.383, 1)), 6: float(spl6(0.383, 1)),
              8: float(spl8(0.383, 1)), 10: float(spl10(0.383, 1))}
    b, a = np.polyfit(np.log([4, 6, 8, 10]),
                      np.log([abs(slopes[L]) for L in [4, 6, 8, 10]]), 1)
    log(f"  slope exponent at 0.383: {b:.2f}  [q=4 target 3/2]; "
        f"slopes {dict((k, round(v,2)) for k,v in slopes.items())}")
    sc["L10_rows"] = rows10
    sc["crossing_8_10"] = None if cr810 is None else float(cr810)
    sc["R10_0383"] = R10
    sc["R_fit_4pt"] = [float(x) for x in coef]
    sc["R_fit_4pt_maxres"] = float(res)
    sc["slope_exponent_4_10"] = float(b)
    sc["slopes_0383"] = {str(k): v for k, v in slopes.items()}
    sc["chi4"] = None  # dropped: coarse-grid curvature not informative at n=4

    with open(JSON, "w") as fh:
        json.dump(R, fh, indent=1, default=float)
    log("JSON updated.")


if __name__ == "__main__":
    main()
