#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seed_dose_response.py — THE TOKEN-COVERAGE-MATCHED DOSE-RESPONSE POOL
(Vol XIV, Chapter 4 §4.10's commissioned battery — the one remaining
nameable upgrade, now a decided experiment).

THE PRE-REGISTRATION (download/seed_dose_preregistration.md, committed
at cd42256 BEFORE this battery's data — the commit is the timestamp):
  H5-a THE POOLED         geometry-level Spearman over the 30 matched
     DOSE-RESPONSE        geometries, both seed blocks (UPGRADE iff
                          p<0.05 and rho>0 in BOTH).
  H5-b THE WITHIN-SIZE    block-centered Spearman, within-block
     ARRANGEMENT TEST     permutation (the strict claim: coverage
                          removed).
  H5-c THE SIZE-DOSE      the curve + the saturation rule (TESTABLE
     CURVE                iff >=2 of 5 size blocks have within-block
                          err std > 0.03) + the cliff test (an
                          adjacent step >= 0.50 with no intermediate).
  THE GUARD               energy-matched pairs (|dE|<0.01) disagreeing
                          on err by > 0.15 -> REFUTED (the guard).
  VERDICTS                UPGRADE / TIER-ONLY / UNTESTED (saturation)
                          / REFUTED (the guard).
  Reproduction-first: full_49 x seeds 1000-1011 through the IMPORTED
  instrument path must reproduce the banked exp3 numbers (E to 1e-9,
  OOD acc exact) before any pool run — else ABORT.

THE POOL: the 49-pair grid minus a uniformly random partial matching
(removed pairs share no row and no column -> every token keeps 6 or 7
examples; the count profile IDENTICAL within a size, +-1 across):
sizes 44-48 x geometry seeds {31,37,41,43,47,53} x model seeds
1000-1011 (block A) + 2000-2011 (block B).  732 runs total
(12 gate + 360 + 360), ~0.3 s each, resumable via JSONL.

Output: seed_dose_runs.jsonl (per-run records, the checkpoint) +
seed_dose_results.json (the analyses + the pre-registered verdicts —
the ONLY upgrade paths, per the pre-registration).
"""
import json
import math
import os
import sys
import time

import numpy as np

import seed_boundary as SB          # the instrument, VERBATIM (imported)

t0 = time.time()
SCR = os.path.dirname(os.path.abspath(__file__))
RUNS_JSONL = os.path.join(SCR, "seed_dose_runs.jsonl")
OUT_JSON = os.path.join(SCR, "seed_dose_results.json")
BANKED_JSON = os.path.join(SCR, "exp3_sheaf_results.json")

P = 7
SIZES = (44, 45, 46, 47, 48)
GSEEDS = (31, 37, 41, 43, 47, 53)
BLOCK_A = list(range(1000, 1012))
BLOCK_B = list(range(2000, 2012))
N_PERM = 10000
STAT_RNG = 20261002               # this battery's fixed stat seed

SPEARMAN = SB.spearman
PEARSON = SB.pearson
FISHER_CI = SB.fisher_ci


# ---------------------------------------------------------------------
# THE MATCHED GEOMETRY (the pre-registration's §1, fixed)
# ---------------------------------------------------------------------
def build_matched_split(size, gseed):
    """The 49-grid minus a uniformly random partial matching of size
    49-s: the removed pairs share no row and no column, so every row
    and column token keeps 6 or 7 training examples (the profile
    IDENTICAL across geometries of the same size; every token >= 4 ->
    no degenerate-E cells)."""
    r = np.random.default_rng(gseed)
    rows = r.permutation(P)
    cols = r.permutation(P)
    k = P * P - size                       # 1..5 removed pairs
    removed = {(int(rows[i]), int(cols[i])) for i in range(k)}
    # the validation the pre-registration's construction guarantees
    assert len(removed) == k, "matching degenerated"
    assert ({a for a, _ in removed} == set(rows[:k].tolist()))
    assert ({b for _, b in removed} == set(cols[:k].tolist()))
    all_pairs = [(a, b) for a in range(P) for b in range(P)]
    tr = [p for p in all_pairs if p not in removed]
    ood = sorted(removed)
    # every token >= 4 examples (the instrument's threshold)
    for tok in range(P):
        assert sum(1 for a, _ in tr if a == tok) >= 4
        assert sum(1 for _, b in tr if b == tok) >= 4
    return tr, ood


def run_one(spec):
    (battery, split, gseed, width, seed) = spec
    if split == "full_49":
        tr, ood = SB.build_split(7, 7)
    elif split == "matched_geo":
        tr, ood = build_matched_split(gseed // 100, gseed % 100)
    else:
        raise ValueError(split)
    m, rec = SB.train_recorded(tr, seed, width)
    acc_tr, nll_tr, _ = SB.eval_model(m, tr)
    acc_ood, nll_ood, conf_wrong = SB.eval_model(m, ood)
    rec.update({"battery": battery, "split": split, "gseed": gseed,
                "width": width, "seed": seed, "n_train": len(tr),
                "n_ood": len(ood), "train_acc": acc_tr,
                "ood_acc": acc_ood, "ood_nll": nll_ood,
                "ood_wrong_confidence": conf_wrong,
                "coboundary_energy": rec["E_3000"]})
    return rec


def run_key(rec):
    return "%s|%s|g%d|w%d|s%d" % (rec["battery"], rec["split"],
                                   rec["gseed"], rec["width"],
                                   rec["seed"])


# ---------------------------------------------------------------------
# THE SPEC LIST (gate first — reproduction before new data)
# ---------------------------------------------------------------------
specs = []
for sd in range(1000, 1012):                               # the GATE
    specs.append(("GATE", "full_49", 0, 64, sd))
for size in SIZES:                                         # block A
    for gs in GSEEDS:
        for sd in BLOCK_A:
            specs.append(("POOL", "matched_geo", size * 100 + gs, 64, sd))
for size in SIZES:                                         # block B
    for gs in GSEEDS:
        for sd in BLOCK_B:
            specs.append(("POOLB", "matched_geo", size * 100 + gs, 64, sd))

GATE_KEYS = {"GATE|full_49|g0|w64|s%d" % sd for sd in range(1000, 1012)}


def load_done():
    done = {}
    if os.path.exists(RUNS_JSONL):
        for line in open(RUNS_JSONL):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                done[run_key(rec)] = rec
            except json.JSONDecodeError:
                continue
    return done


def gate_check(done):
    banked = json.load(open(BANKED_JSON))
    bank = {(r["split"], r["seed"]): r for r in banked["runs"]}
    worst_dE, fails = 0.0, []
    for sd in range(12):
        k = "GATE|full_49|g0|w64|s%d" % (1000 + sd)
        if k not in done:
            return None                                     # not ready
        r = done[k]
        b = bank[("full_49", sd)]
        dE = abs(r["coboundary_energy"] - b["coboundary_energy"])
        worst_dE = max(worst_dE, dE)
        if dE > 1e-9 or r["ood_acc"] != b["ood_acc"]:
            fails.append((sd, dE, r["ood_acc"], b["ood_acc"]))
    if fails:
        print("GATE FAIL — the import path perturbed the instrument "
              "(%d mismatches):" % len(fails))
        for f in fails[:6]:
            print("   ", f)
        sys.exit(1)
    print("GATE PASS — 12/12 full_49 runs reproduce the banked numbers "
          "through the IMPORTED instrument (worst |dE| = %.2e, OOD acc "
          "exact)" % worst_dE)
    return worst_dE


# ---------------------------------------------------------------------
# THE STATISTICS (the Task-44 machinery, this battery's fixed seed)
# ---------------------------------------------------------------------
def perm_p(x, y, stat=PEARSON, n_perm=N_PERM, within=None):
    """Two-sided permutation p; if within is given, y is permuted only
    within the blocks (H5-b's block-preserving permutation)."""
    rng = np.random.default_rng(STAT_RNG)
    obs = stat(x, y)
    y = np.array(y, float)
    cnt = 0
    for _ in range(n_perm):
        if within is None:
            yp = rng.permutation(y)
        else:
            yp = y.copy()
            for idx in within:
                yp[idx] = yp[rng.permutation(np.array(idx))]
        if abs(stat(x, yp)) >= abs(obs):
            cnt += 1
    return float((cnt + 1) / (n_perm + 1)), obs


def bootstrap_ci(x, y, n_boot=N_PERM):
    rng = np.random.default_rng(STAT_RNG + 1)
    x, y = np.array(x, float), np.array(y, float)
    n = len(x)
    stats = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        if x[idx].std() < 1e-12 or y[idx].std() < 1e-12:
            continue
        stats.append(PEARSON(x[idx], y[idx]))
    if not stats:
        return (float("nan"), float("nan"))
    stats = np.sort(np.array(stats))
    return (float(np.percentile(stats, 2.5)),
            float(np.percentile(stats, 97.5)))


# ---------------------------------------------------------------------
# THE ANALYSIS (the pre-registered rules — the ONLY upgrade paths)
# ---------------------------------------------------------------------
def analyze(done, gate_worst_dE):
    def geo_rows(battery):
        rows = {}
        for r in done.values():
            if r["battery"] != battery:
                continue
            g = (r["gseed"] // 100, r["gseed"] % 100)
            rows.setdefault(g, []).append(r)
        out = []
        for (size, gs), rs in sorted(rows.items()):
            E = [x["coboundary_energy"] for x in rs]
            err = [1.0 - x["ood_acc"] for x in rs]
            out.append({"size": size, "gseed": gs, "n": len(rs),
                        "E_mean": float(np.mean(E)),
                        "E_std": float(np.std(E)),
                        "err_mean": float(np.mean(err)),
                        "err_std": float(np.std(err))})
        return out

    A = geo_rows("POOL")
    B = geo_rows("POOLB")

    def pooled(rows_a, rows_b):
        """The two blocks' runs pooled per geometry (24 seeds)."""
        pd = {}
        for r in done.values():
            if r["battery"] not in ("POOL", "POOLB"):
                continue
            g = (r["gseed"] // 100, r["gseed"] % 100)
            pd.setdefault(g, []).append(r)
        out = []
        for (size, gs), rs in sorted(pd.items()):
            E = [x["coboundary_energy"] for x in rs]
            err = [1.0 - x["ood_acc"] for x in rs]
            out.append({"size": size, "gseed": gs, "n": len(rs),
                        "E_mean": float(np.mean(E)),
                        "E_std": float(np.std(E)),
                        "err_mean": float(np.mean(err)),
                        "err_std": float(np.std(err))})
        return out

    POO = pooled(A, B)

    def xy(rows):
        return ([r["E_mean"] for r in rows], [r["err_mean"] for r in rows])

    # ---- H5-a: the pooled dose-response, per block ----
    h5a = {}
    for tag, rows in (("block_A", A), ("block_B", B)):
        x, y = xy(rows)
        p, obs = perm_p(x, y, stat=SPEARMAN)
        h5a[tag] = {"n": len(rows), "spearman": obs,
                    "pearson": PEARSON(x, y), "perm_p": p,
                    "fisher_ci95": FISHER_CI(PEARSON(x, y), len(rows)),
                    "bootstrap_ci95": bootstrap_ci(x, y)}

    # ---- H5-b: the within-size arrangement test, per block ----
    h5b = {}
    for tag, rows in (("block_A", A), ("block_B", B)):
        blocks, cx, cy = [], [], []
        for size in SIZES:
            sub = [r for r in rows if r["size"] == size]
            if not sub:
                continue
            mE = float(np.mean([r["E_mean"] for r in sub]))
            mY = float(np.mean([r["err_mean"] for r in sub]))
            idx = [i for i, r in enumerate(rows) if r["size"] == size]
            blocks.append(idx)
            for r in sub:
                cx.append(r["E_mean"] - mE)
                cy.append(r["err_mean"] - mY)
        p, obs = perm_p(cx, cy, stat=SPEARMAN, within=blocks)
        h5b[tag] = {"n": len(rows), "centered_spearman": obs,
                    "perm_p_withinblock": p}

    # ---- H5-c: the size-dose curve + saturation + cliff ----
    curve = []
    for size in SIZES:
        sub = [r for r in POO if r["size"] == size]
        e = [r["err_mean"] for r in sub]
        E = [r["E_mean"] for r in sub]
        curve.append({"size": size, "n_geo": len(sub),
                      "err_mean": float(np.mean(e)),
                      "err_std_across_geo": float(np.std(e)),
                      "E_mean": float(np.mean(E)),
                      "E_std_across_geo": float(np.std(E))})
    testable_blocks = [c["size"] for c in curve
                       if c["err_std_across_geo"] > 0.03]
    testable = len(testable_blocks) >= 2
    steps = [(curve[i + 1]["size"], curve[i]["err_mean"] -
              curve[i + 1]["err_mean"]) for i in range(len(curve) - 1)]
    cliff = [s for s in steps if abs(s[1]) >= 0.50]

    # ---- the matched-pair guard (pooled geometry means) ----
    guard = {"pairs_checked": 0, "max_derr": 0.0, "fired": False}
    for i in range(len(POO)):
        for j in range(i + 1, len(POO)):
            dE = abs(POO[i]["E_mean"] - POO[j]["E_mean"])
            if dE < 0.01:
                dY = abs(POO[i]["err_mean"] - POO[j]["err_mean"])
                guard["pairs_checked"] += 1
                guard["max_derr"] = max(guard["max_derr"], dY)
    guard["fired"] = guard["max_derr"] > 0.15

    # ---- THE VERDICT (the pre-registered classes, in order) ----
    a_ok = all(h5a[t]["perm_p"] < 0.05 and h5a[t]["spearman"] > 0
               for t in ("block_A", "block_B"))
    b_ok = all(h5b[t]["perm_p_withinblock"] < 0.05 and
               h5b[t]["centered_spearman"] > 0
               for t in ("block_A", "block_B"))
    if guard["fired"]:
        verdict = ("REFUTED (the guard) — matched-energy geometries "
                   "disagree on err by %.3f (> 0.15): whatever "
                   "correlation exists is not E-driven"
                   % guard["max_derr"])
    elif not testable:
        verdict = ("UNTESTED (saturation) — only %d of 5 size blocks "
                   "carry within-block err variance (> 0.03): the "
                   "honest status; the %s reading is the finding"
                   % (len(testable_blocks),
                      "CLIFF" if cliff else "level"))
    elif a_ok:
        verdict = ("UPGRADE — the pooled dose-response fires in BOTH "
                   "blocks (E orders OOD error within the matched "
                   "family): the diagnostic upgrades to a within-"
                   "family dose-response meter")
    else:
        verdict = ("TIER-ONLY — the pool is TESTABLE and H5-a fails "
                   "(p_A=%.4f, p_B=%.4f): the coherence-tier law's "
                   "final form — E's reach is the tier and only the "
                   "tier" % (h5a["block_A"]["perm_p"],
                             h5a["block_B"]["perm_p"]))

    out = {
        "meta": {
            "experiment": "THE PRE-REGISTERED TOKEN-COVERAGE-MATCHED "
                          "DOSE-RESPONSE POOL",
            "prereg": "download/seed_dose_preregistration.md "
                      "(committed at cd42256 before the data)",
            "instrument": "seed_boundary.py's machinery VERBATIM "
                          "(imported; the gate proves the import path)",
            "runs_total": len(done), "gate_worst_dE": gate_worst_dE,
            "wall_s": round(time.time() - t0, 1),
            "n_perm": N_PERM, "stat_rng": STAT_RNG,
            "pool": "sizes 44-48 x gseeds %s x 12+12 seeds"
                    % (GSEEDS,)},
        "geometries_pooled": POO,
        "block_A": A, "block_B": B,
        "H5a_pooled_dose_response": h5a,
        "H5b_within_size_arrangement": h5b,
        "H5c_size_dose_curve": curve,
        "testable": {"testable": testable,
                     "blocks_with_variance": testable_blocks},
        "cliff": {"steps_size_derr": steps, "cliff_steps": cliff},
        "matched_pair_guard": guard,
        "secondary_E_vs_size": [float(np.mean([r["E_mean"] for r
                                               in POO if r["size"] == s]))
                                for s in SIZES],
        "verdict": verdict,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1, default=float)

    print("=" * 68)
    print("THE MATCHED DOSE-RESPONSE POOL (%d runs, gate worst |dE| "
          "%.1e)" % (len(done), gate_worst_dE or 0))
    for c in curve:
        print("  size %d: err %.3f +- %.3f (across 6 geo)   E %.4f +- "
              "%.4f" % (c["size"], c["err_mean"],
                        c["err_std_across_geo"], c["E_mean"],
                        c["E_std_across_geo"]))
    for t in ("block_A", "block_B"):
        print("  H5-a %s: rho_S=%.3f (perm p=%.4f)   H5-b: "
              "centered rho=%.3f (within-block p=%.4f)"
              % (t, h5a[t]["spearman"], h5a[t]["perm_p"],
                 h5b[t]["centered_spearman"],
                 h5b[t]["perm_p_withinblock"]))
    print("  the guard: %d matched pairs, max |derr| = %.3f %s"
          % (guard["pairs_checked"], guard["max_derr"],
             "(FIRED)" if guard["fired"] else ""))
    print("  testable: %s (%s)   cliff steps: %s"
          % (testable, testable_blocks, cliff or "none"))
    print("  THE VERDICT: %s" % verdict)
    print("results written:", OUT_JSON)


def main():
    done = load_done()
    gate = gate_check(done)
    if gate is None:
        print("collecting the GATE runs (reproduction-first) ...")
    todo = [s for s in specs if ("%s|%s|g%d|w%d|s%d" % s) not in done]
    n_new = 0
    for spec in todo:
        if gate is None and GATE_KEYS <= set(done):
            gate = gate_check(done)      # exits on drift
        rec = run_one(spec)
        k = run_key(rec)
        done[k] = rec
        with open(RUNS_JSONL, "a") as f:
            f.write(json.dumps(rec) + "\n")
        n_new += 1
        if n_new % 24 == 0:
            print("  %d/%d new runs (%d total) — %.0fs elapsed, "
                  "~%.0fs left" % (n_new, len(todo), len(done),
                                   time.time() - t0,
                                   (time.time() - t0) / n_new *
                                   (len(todo) - n_new)))
    gate = gate_check(done)
    print("all %d runs complete (%d new this invocation, %.0fs)"
          % (len(done), n_new, time.time() - t0))
    analyze(done, gate)


if __name__ == "__main__":
    main()
