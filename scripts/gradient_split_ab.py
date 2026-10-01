#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gradient_split_ab.py — TL-6: THE GRADIENT-PRIORITIZED SPLIT A/B
(Task 38's actionable corollary, validated BEFORE the engine edit).

THE LAW BEING TESTED (tail_law_results.json, TL-3b): the far-out
radius is carried by the A-off-diagonal couplings (Aa10 > Ab10 >
Ab01 > Aa01, with C1/B0 secondary) — but split12's width-first rule
equilibriates RELATIVE WIDTHS, so the carriers receive only 4/12 of
the splits -> the measured 0.135 bits/level.  Scoring the split by
rel_k * G_k (G = the TL-3b population gradient profile) targets the
largest first-order radius contribution per split — the predicted
~2x per-level decay, hence ~2x the far-out certification rate.

THE PROBE (the engine's own machinery, the live stack — NO
checkpoint mutation, the F_* counters snapshotted/restored):
  AB-0  the fresh profile check: the dV*W ranking at 6 live stack
        boxes (the banked law on the CURRENT frontier).
  AB-A  the stock arm: run_engine12's loop verbatim (width-first
        split12 everywhere), 4000 calls, on a copy of the live
        stack.
  AB-B  the gradient arm: the same, with the FAR-OUT branch's
        splits scored rel_k * G_k (the boundary/split branches keep
        the stock rule — the surgical engine edit's exact scope).
  AB-V  the verdict: the e45-per-call ratio B/A, the median
        depth-to-convert, the stall counts (the soundness guard).

Output: gradient_split_ab_results.json
"""
import ast
import json
import time

import numpy as np

t0 = time.time()
SCR = "/home/z/my-project/github_repos/master/scripts/"

# ---------------------------------------------------------------------
# load the wall's machinery WITHOUT running the engine (the
# tail_law.py AST-filter pattern: exec every top-level def/assign
# except Expr statements and the `remaining = run_engine12()` driver)
# ---------------------------------------------------------------------
src = open(SCR + "free_class_wall.py").read()
tree = ast.parse(src)
ns = {"__name__": "fcw_machinery", "__file__": SCR + "free_class_wall.py"}
for node in tree.body:
    if isinstance(node, ast.Expr):
        continue
    if isinstance(node, ast.Assign):
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if "remaining" in targets:
            continue
    mod = ast.Module([node], type_ignores=[])
    try:
        exec(compile(mod, "fcw_machinery", "exec"), ns)
    except Exception:
        pass
fcw = ns

LAMBDA = fcw["LAMBDA"]
SCALES = fcw["SCALES"]
N_LADDER = fcw["N_LADDER"]
e45_partial = fcw["e45_partial"]
e45_zmenu = fcw["e45_zmenu"]
xballs = fcw["xballs"]
split12 = fcw["split12"]
cover_leaf12 = fcw["cover_leaf12"]

FAROUT_CAP = fcw["FAROUT_CAP"]
BOUNDARY_CAP = fcw["BOUNDARY_CAP"]
DEPTH_CAP = fcw["DEPTH_CAP"]
WIDTH_CAP = fcw["WIDTH_CAP"]
CNAMES = ["F_PASS", "F_WIN", "F_E0", "F_E45", "F_RAYL",
          "F_BOUND", "F_FAROUT", "F_STALL", "F_CALLS"]

OUT = {"meta": {
    "order": "TL-6: the gradient-prioritized split A/B — Task 38's "
             "actionable corollary, validated before the engine edit",
    "date": "2026-10-01",
    "budget_calls_per_arm": 4000,
    "lambda_star": fcw["LAMBDA_STR"]}}

DIMNAMES = ["B0", "B1", "C0", "C1", "Aa00", "Aa11", "Ab00",
            "Ab11", "Aa01", "Aa10", "Ab01", "Ab10"]
# the TL-3b population profile (6 stack cases, normalized Aa10=1.0;
# Aa01/C1 below top-4 in some cases -> 0.55/0.50; the non-carriers
# at the 0.10 floor — below every case's top-4; B0 top-4 once)
G_W = [0.25, 0.10, 0.10, 0.50,
       0.10, 0.10, 0.10, 0.10,
       0.55, 1.00, 0.65, 0.85]


def e45_float_margin(c, Ns=N_LADDER):
    xb = xballs([(xi, xi) for xi in c])
    best = None
    for N in Ns:
        for z in e45_zmenu(c, N):
            q = e45_partial(xb, np.array(z), N)
            if q is not None:
                v = float(q)
                if best is None or v > best:
                    best = v
    return best


def split12_grad(box):
    """the gradient-prioritized split: the coordinate with the
    largest first-order radius contribution rel_k * G_k (the
    TL-3b population profile), NOT the largest relative width."""
    widths = [b[1] - b[0] for b in box]
    rel = [w / s for (w, s) in zip(widths, SCALES)]
    k = max(range(12), key=lambda i: rel[i] * G_W[i])
    mid = 0.5 * (box[k][0] + box[k][1])
    a = [list(b) for b in box]
    b2 = [list(b) for b in box]
    a[k][1] = mid
    b2[k][0] = mid
    return (tuple(tuple(e) for e in a), tuple(tuple(e) for e in b2))


def snap():
    return {n: fcw[n][0] for n in CNAMES}


def restore(s):
    for n in CNAMES:
        fcw[n][0] = s[n]


def run_arm(stack0, budget, use_grad):
    """run_engine12's loop verbatim on a COPY of the live stack; the
    far-out branch's splits gradient-scored iff use_grad (the
    surgical engine edit's exact scope); the F_* counters
    snapshotted and restored — NO checkpoint mutation."""
    stack = list(stack0)
    calls = 0
    conv_depths = []
    stalls = 0
    rcount = {}
    s0 = snap()
    t = time.time()
    while stack and calls < budget:
        (box, depth) = stack.pop()
        calls += 1
        res = cover_leaf12(box, depth)
        rcount[res] = rcount.get(res, 0) + 1
        if res == "pass":
            conv_depths.append(depth)
            continue
        if res == "farout":
            if (depth >= FAROUT_CAP or
                    max(b[1] - b[0] for b in box) < WIDTH_CAP):
                stalls += 1
            else:
                sp = split12_grad(box) if use_grad else split12(box, depth)
                stack.append((sp[0], depth + 1))
                stack.append((sp[1], depth + 1))
            continue
        cap = BOUNDARY_CAP if res == "boundary" else DEPTH_CAP
        if (depth >= cap or
                max(b[1] - b[0] for b in box) < WIDTH_CAP):
            stalls += 1
        else:
            sp = split12(box, depth)
            stack.append((sp[0], depth + 1))
            stack.append((sp[1], depth + 1))
    dt = time.time() - t
    deltas = {n: fcw[n][0] - s0[n] for n in CNAMES}
    restore(s0)
    med = (sorted(conv_depths)[len(conv_depths) // 2]
           if conv_depths else None)
    return {"calls": calls, "wall_s": round(dt, 1),
            "results": rcount, "conversions": len(conv_depths),
            "median_conv_depth": med, "stalls": stalls,
            "counter_deltas": deltas,
            "stack_remaining": len(stack)}


# =====================================================================
# AB-0 — the fresh profile check on the CURRENT stack
# =====================================================================
print("=" * 76)
print("AB-0 — the fresh TL-3b profile check (6 live stack boxes)")
print("=" * 76)
ck = json.load(open(SCR + "free_class_wall_ckpt.json"))
stack0 = [(tuple(tuple(e) for e in b), d) for (b, d) in ck["stack"]]
n0 = len(stack0)
print("  the live stack: %d entries (depths %d..%d)" %
      (n0, min(d for (_, d) in stack0), max(d for (_, d) in stack0)))

order = sorted(range(n0), key=lambda i: -stack0[i][1])  # deepest first
step = max(1, n0 // 6)
pick = order[::step][:6]     # the live far-out lineages (d-max side)
rows = []
for idx in pick:
    box, depth = stack0[idx]
    c = np.array([0.5 * (lo + hi) for (lo, hi) in box])
    V0 = e45_float_margin(c, Ns=(2,))
    if V0 is None:
        print("    idx %2d (d%-3d) V0 unresolved — skipped" % (idx, depth))
        continue
    contribs = []
    for k in range(12):
        h = 1e-4 * SCALES[k]
        cp = c.copy()
        cp[k] += h
        Vp = e45_float_margin(cp, Ns=(2,))
        cmv = c.copy()
        cmv[k] -= h
        Vm = e45_float_margin(cmv, Ns=(2,))
        if Vp is not None and Vm is not None:
            dV = abs(float(Vp) - float(Vm)) / (2 * h)
            contribs.append((DIMNAMES[k], dV * (box[k][1] - box[k][0])))
    tot = sum(t[1] for t in contribs)
    if tot <= 0 or not contribs:
        print("    idx %2d (d%-3d) V0=%.2e — the profile unresolvable "
              "(all partials flat/None) — skipped" % (idx, depth, float(V0)))
        continue
    contribs.sort(key=lambda t: -t[1])
    top = ", ".join("%s %.0f%%" % (nm, 100 * s / tot)
                    for (nm, s) in contribs[:4])
    print("    idx %2d (d%-3d) V0=%.2e  carriers: %s"
          % (idx, depth, float(V0), top))
    rows.append({"idx": idx, "depth": depth, "V0": float(V0),
                 "top4": [(nm, float(s)) for (nm, s) in contribs[:4]]})
OUT["AB0_profile"] = rows

# =====================================================================
# AB-A / AB-B — the controlled arms (identical start stack)
# =====================================================================
print()
print("=" * 76)
print("AB-A — the stock arm (width-first split12, 4000 calls)")
print("=" * 76)
armA = run_arm(stack0, 4000, use_grad=False)
print("  calls %d in %.1fs (%.0f calls/s) | results %s" %
      (armA["calls"], armA["wall_s"],
       armA["calls"] / max(armA["wall_s"], 1e-9), armA["results"]))
print("  conversions %d (median depth %s) | stalls %d | "
      "dF_E45 %d | stack %d -> %d" %
      (armA["conversions"], armA["median_conv_depth"], armA["stalls"],
       armA["counter_deltas"]["F_E45"], n0, armA["stack_remaining"]))

print()
print("=" * 76)
print("AB-B — the gradient arm (far-out splits rel*G, 4000 calls)")
print("=" * 76)
armB = run_arm(stack0, 4000, use_grad=True)
print("  calls %d in %.1fs (%.0f calls/s) | results %s" %
      (armB["calls"], armB["wall_s"],
       armB["calls"] / max(armB["wall_s"], 1e-9), armB["results"]))
print("  conversions %d (median depth %s) | stalls %d | "
      "dF_E45 %d | stack %d -> %d" %
      (armB["conversions"], armB["median_conv_depth"], armB["stalls"],
       armB["counter_deltas"]["F_E45"], n0, armB["stack_remaining"]))

OUT["AB_A"] = armA
OUT["AB_B"] = armB

# =====================================================================
# AB-V — the verdict
# =====================================================================
print()
print("=" * 76)
print("AB-V — the verdict")
print("=" * 76)
eA = armA["counter_deltas"]["F_E45"]
eB = armB["counter_deltas"]["F_E45"]
cA = armA["conversions"]
cB = armB["conversions"]
rateA = eA / armA["calls"] if armA["calls"] else 0.0
rateB = eB / armB["calls"] if armB["calls"] else 0.0
ratio = (rateB / rateA) if rateA > 0 else None
cratio = (cB / cA) if cA > 0 else None
print("  the e45 rate: stock %.4f/call vs gradient %.4f/call" %
      (rateA, rateB))
if ratio is not None:
    print("  THE RATIO: %.2fx (the conversions ratio %.2fx)" %
          (ratio, cratio or 0.0))
else:
    print("  THE RATIO: undefined (stock arm converted %d e45 — "
          "a null result, no engine edit on this evidence)" % eA)
verdict = {
    "e45_rate_stock": rateA, "e45_rate_gradient": rateB,
    "ratio": ratio, "conversions_ratio": cratio,
    "median_conv_depth_stock": armA["median_conv_depth"],
    "median_conv_depth_gradient": armB["median_conv_depth"],
    "stalls_stock": armA["stalls"], "stalls_gradient": armB["stalls"],
    "decision": ("DEPLOY (the far-out gradient split into the engine)"
                 if (ratio is not None and ratio >= 1.4
                     and armB["stalls"] == 0)
                 else ("HOLD (the evidence insufficient or the stalls "
                       "regressed — no engine edit)"
                       if ratio is None or armB["stalls"] > 0
                       else "HOLD (the ratio below the 1.4x bar)"))}
OUT["AB_V_verdict"] = verdict
print("  DECISION: %s" % verdict["decision"])
print("  (the soundness guard: the split is a plain coordinate "
      "bisection either way — certification is per-box; only the "
      "split ORDER changes)")

json.dump(OUT, open(SCR + "gradient_split_ab_results.json", "w"),
          indent=1)
print()
print("results written — wall time %.1f s" % (time.time() - t0))
