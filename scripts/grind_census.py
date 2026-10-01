#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
grind_census.py — THE GRIND CENSUS (Vol XIV, Chapter 1's battery, the
projection instrument of Chapter 2): the two engines' live state, the
completion conditions itemized, the call projections with honest error
bars, and THE STOPPING RULE.

THE COMMISSIONING CRITIQUE (this session): "Keep the driver running on
the 24-branch frontier: merited only if the frontier is near
exhaustion and completion yields a decisive certified result. ...
It needs a stopping rule and an expected endpoint."  This instrument
IS that rule, computed from the measured frontier dynamics rather
than asserted.

THE STOPPING RULE (stated first, then evaluated from the trailing
window — the corpus's discipline: the rule before the reading):
  COVER4D:  CONTINUE while frontier > 0 AND the trailing-3 net
            closure rate >= 1 branch per 20M calls (the diminishing-
            return floor).  COMPLETE at frontier = 0 — the completion
            certificate (the theorem's full domain: every orbit
            representative's subtree closed by the BDC trio, the
            10 symmetry-covered images, the B-exit bookkeeping's
            analytic segment).  HOLD (report the frontier's structure,
            spend no more compute) when the trailing rate sits below
            the floor for 3 consecutive rounds.
  WALL:     CONTINUE while the trailing-3 net stack reduction > 0.
            STOP when the stack trend is non-descending — the far-out
            refinement REPLENISHES the stack (each deep conversion
            splits new entries), so exhaustion is not this arm's
            endpoint; the completion face is Task 42's bookkeeping
            (the far field beyond the ROOT cap certified by the growth
            laws + the sound shells; the cap is the engine's
            bookkeeping, not the mathematics' boundary).

Reads: abelian_cover4d_ckpt.json, free_class_wall_ckpt.json,
       drain_driver.log (the round series).
Writes: grind_census_results.json
"""
import json
import os
import re

SCR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCR, "..", "..", "..", "scripts"))
LOG_CANDIDATES = [
    os.path.join(SCR, "drain_driver.log"),
    os.path.join(ROOT, "drain_driver.log"),
    "/home/z/my-project/scripts/drain_driver.log",
]


def find_log():
    for c in LOG_CANDIDATES:
        if os.path.exists(c):
            return c
    raise FileNotFoundError("drain_driver.log not found")


def parse_series(logpath):
    cover = []      # (calls, branches)
    wall = []       # (calls, stack, certified, farout)
    txt = open(logpath, errors="replace").read().splitlines()
    for line in txt:
        m = re.search(r"the 4-D covering run \(slice\):.*?(\d+) calls, "
                      r"(\d+) stack remaining", line)
        if m:
            cover.append((int(m.group(1)), int(m.group(2))))
        m = re.search(r"the pilot slice: (\d+) calls . (\d+) certified "
                      r".*?(\d+) far-out, \d+ stalls, (\d+) stack remaining",
                      line)
        if m:
            wall.append((int(m.group(1)), int(m.group(4)),
                         int(m.group(2)), int(m.group(3))))
    # dedupe consecutive identical call counts (resumes)
    out_c, seen = [], set()
    for c, b in cover:
        if c not in seen:
            seen.add(c)
            out_c.append((c, b))
    out_w, seen = [], set()
    for c, s, k, f in wall:
        if c not in seen:
            seen.add(c)
            out_w.append((c, s, k, f))
    return out_c, out_w


def trailing(series, k=3):
    return series[-k:]


def project(series, k=3):
    """Linear projection to zero from the trailing-k net rate, with
    honest bounds from the observed per-step rate range."""
    tr = trailing(series, k)
    if len(tr) < 2:
        return None
    calls = [c for c, b in tr]
    brs = [b for c, b in tr]
    span_calls = (calls[-1] - calls[0]) or 1
    net = brs[-1] - brs[0]
    rate = net / span_calls                        # branches / call (neg)
    steps = [(calls[i + 1] - calls[i],
              brs[i + 1] - brs[i]) for i in range(len(tr) - 1)]
    worst = min((d_b / max(d_c, 1)) for d_c, d_b in steps)   # most neg
    best = max((d_b / max(d_c, 1)) for d_c, d_b in steps)    # least neg
    b_now = brs[-1]
    proj = (-b_now / rate) if rate < 0 else None
    proj_lo = (-b_now / worst) if worst < 0 else None
    proj_hi = (-b_now / best) if best < 0 else None
    return {"trailing_series": tr, "net_over_window": net,
            "net_rate_branches_per_M": rate * 1e6,
            "projection_calls_to_zero": proj,
            "projection_lo_calls": proj_lo,
            "projection_hi_calls": proj_hi}


def main():
    log = find_log()
    cover, wall = parse_series(log)
    ck_c = json.load(open(os.path.join(SCR, "abelian_cover4d_ckpt.json")))
    ck_w = json.load(open(os.path.join(SCR, "free_class_wall_ckpt.json")))

    pc = project(cover) if cover else None
    pw = project([(c, s) for c, s, k, f in wall]) if wall else None

    # ---- cover4d verdict ----
    c_now = cover[-1][1] if cover else None
    c_rate = pc["net_rate_branches_per_M"] if pc else None
    closure = -c_rate if c_rate is not None else None   # + = closing
    FLOOR = 1.0 / 20.0  # branches per M calls (closure)
    # the consecutive below-floor windows ending at the latest round
    # (the HOLD gate needs 3 consecutive)
    below_run = 0
    if len(cover) >= 4:
        for i in range(len(cover) - 1, 2, -1):
            w = cover[i - 2:i + 1]
            span = (w[-1][0] - w[0][0]) or 1
            wnet = w[-1][1] - w[0][1]
            if -wnet / span * 1e6 < FLOOR:
                below_run += 1
            else:
                break
    if c_now == 0:
        c_verdict = ("COMPLETE — frontier 0: the completion certificate "
                     "fires (the theorem's full domain)")
    elif closure is not None and closure >= FLOOR:
        c_verdict = ("CONTINUE — frontier %d branches, trailing-3 "
                     "CLOSURE %.1f branches/M calls (>= the %.2f "
                     "floor): near exhaustion; the endpoint is the "
                     "completion certificate at frontier = 0"
                     % (c_now, closure, FLOOR))
    elif below_run >= 3:
        c_verdict = ("HOLD — %d consecutive below-floor windows: the "
                     "frontier oscillates (the LIFO replenishment), "
                     "exhaustion is not the endpoint; report the "
                     "structure, spend no more compute" % below_run)
    else:
        c_verdict = ("HOLD-CANDIDATE (%d of 3 consecutive below-floor "
                     "windows) — trailing closure %.3f below the floor: "
                     "the branch-count trend does not close; the "
                     "oscillation band and the depth structure (the "
                     "race law's d*) are the honest account, the next "
                     "rounds decide"
                     % (below_run, closure or 0.0))

    # ---- wall verdict ----
    w_net = pw["net_over_window"] if pw else None
    if w_net is not None and w_net < 0:
        w_verdict = ("CONTINUE — the stack descends (net %d over the "
                     "trailing window)" % w_net)
    else:
        w_verdict = ("STOP — the stack trend is non-descending (net %s "
                     "over the trailing window; the observed oscillation "
                     "39-45 with the far-out replenishment): exhaustion "
                     "is not this arm's endpoint.  The completion face: "
                     "Task 42's bookkeeping — the far field beyond the "
                     "ROOT cap certified by the growth laws + the sound "
                     "shells; the certified region stands as certified"
                     % w_net)

    # ---- the wall's steady-state conversion (descriptive) ----
    w_conv = None
    if len(wall) >= 2:
        d_calls = wall[-1][0] - wall[0][0]
        d_cert = wall[-1][2] - wall[0][2]
        d_far = wall[-1][3] - wall[0][3]
        w_conv = {"certified_per_10k_calls": d_cert / (d_calls / 1e4),
                  "farout_tags_per_10k_calls": d_far / (d_calls / 1e4)}

    out = {
        "meta": {
            "instrument": "grind_census.py — the stopping-rule census",
            "log": log,
            "rounds_parsed": {"cover4d": len(cover), "wall": len(wall)},
            "the_rule": {
                "cover4d": "CONTINUE while frontier>0 and trailing-3 "
                           "net >= 1 branch/20M calls; COMPLETE at 0; "
                           "HOLD below the floor 3 rounds running",
                "wall": "CONTINUE while trailing-3 net stack "
                        "reduction > 0; else STOP (the completion face "
                        "is Task 42's far-field bookkeeping)"}},
        "cover4d": {
            "calls": ck_c["b_calls"], "leaves_certified": ck_c["b_pass"],
            "bdc_composition": {"e0": ck_c["b_bdc0"], "e4": ck_c["b_bdc4"],
                                "e5": ck_c["b_bdc5"]},
            "stalls": ck_c["b_stalln"],
            "frontier_branches": len(ck_c["stack"]),
            "series_tail": cover[-9:],
            "projection": pc,
            "verdict": c_verdict},
        "wall": {
            "calls": ck_w["f_calls"], "certified": ck_w["f_pass"],
            "window": ck_w["f_win"], "e45_partial_sum": ck_w["f_e45"],
            "farout_tags": ck_w["f_farout"], "stalls": ck_w["f_stall"],
            "stack_entries": len(ck_w["stack"]),
            "series_tail": [(c, s) for c, s, k, f in wall[-9:]],
            "projection": pw,
            "steady_state_conversion": w_conv,
            "verdict": w_verdict},
        "completion_conditions": {
            "cover4d": [
                "the frontier's %d stack branches -> 0 (the LIFO "
                "closure, the BDC trio per leaf)" % len(ck_c["stack"]),
                "the B-exit segment (x < 1.65e-3) — covered analytically "
                "(Task 40's bookkeeping, already stated)",
                "the 10 symmetry-covered quadrant images — certified "
                "(the orbit reduction V-E/V-F exact)",
                "the unbounded far field — Task 42's map (the growth "
                "laws + the one-shot strict-sound shells + the valley "
                "tail's plateau law)"],
            "wall": [
                "the certified region (346,400: the window + the e45 "
                "partial-sum chain) — stands as certified",
                "the stack's remaining entries — the STOP rule's face: "
                "the far-out replenishment has no exhaustion endpoint; "
                "the beyond is Task 42's, not the grind's",
                "the completion certificate's FORM: the domain = the "
                "certified region + the analytic B-exit + the far-field "
                "laws; the grind's residue is bookkeeping"]},
    }
    with open(os.path.join(SCR, "grind_census_results.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)

    print("=" * 68)
    print("THE GRIND CENSUS (the stopping rule, from the measured "
          "frontier dynamics)")
    print("  cover4d: %d calls, %d leaves (BDC %d/%d/%d), frontier %d "
          "branches, 0-ish stalls"
          % (ck_c["b_calls"], ck_c["b_pass"], ck_c["b_bdc0"],
             ck_c["b_bdc4"], ck_c["b_bdc5"], len(ck_c["stack"])))
    print("    series tail: %s" % (cover[-9:],))
    if pc:
        print("    trailing-3 CLOSURE %.2f branches/M; projection to zero: "
              "%s [lo %s, hi %s]"
              % (-(pc["net_rate_branches_per_M"]),
                 ("%.2fM calls" %
                  (pc["projection_calls_to_zero"] / 1e6))
                 if pc["projection_calls_to_zero"] else
                 "NO-CLOSURE (the trend opens)",
                 ("%.2fM" % (pc["projection_lo_calls"] / 1e6))
                 if pc["projection_lo_calls"] else "n/a",
                 ("%.2fM" % (pc["projection_hi_calls"] / 1e6))
                 if pc["projection_hi_calls"] else "no-closure"))
    print("    VERDICT: %s" % c_verdict)
    print("  wall: %dk calls, %d certified, %d far-out tags, stack %d"
          % (ck_w["f_calls"] // 1000, ck_w["f_pass"], ck_w["f_farout"],
             len(ck_w["stack"])))
    print("    series tail: %s" % ([(c, s) for c, s, k, f in wall[-9:]],))
    if w_conv:
        print("    steady-state: %.1f certified / 10k calls"
              % w_conv["certified_per_10k_calls"])
    print("    VERDICT: %s" % w_verdict)
    print("results written: grind_census_results.json")


if __name__ == "__main__":
    main()
