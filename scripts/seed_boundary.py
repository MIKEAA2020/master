#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seed_boundary.py — THE PRE-REGISTERED SEED-BOUNDARY EXPERIMENT (Vol XIV,
Chapter 4's battery, commissioned by the critique: "the seed-level
boundary ... must be framed as a real experiment: clear hypotheses,
controls, metrics, falsification criteria, and independent
replication").

THE PRE-REGISTRATION (download/seed_boundary_preregistration.md —
committed BEFORE this battery ran; the commit is the timestamp):
  H1 THE SCOPE LAW      E is a task-geometry diagnostic, not a
                        seed-level predictor (TOST at delta=0.30).
  H2 THE TASK-LEVEL LAW E orders geometries as their OOD errors do
                        (geometry-level Spearman, energy-matched pairs).
  H3 THE MISSING        a training-dynamics covariate panel carries the
     COVARIATE TEST     seed-level signal E does not (|rho|>=0.5,
                        perm p<0.01, BH q<0.05, replicated in >=2/3).
  H4 FAMILY INVARIANCE  the H1 verdict class replicates at width
                        32/128.
  Reproduction-first: seeds 1000-1011 of the four original splits must
  reproduce the banked exp3_sheaf_results.json (E to 1e-9, OOD acc
  exact) BEFORE any new data is collected — else ABORT.

THE INSTRUMENT: exp3_sheaf.py's machinery VERBATIM (the Z_7 modular
addition task, the MLP 2-64-64-7, Adam full-batch 3000 steps, the
token-sheaf coboundary energy), width-parameterized (64 default =
bit-identical), plus PURE-READ instrumentation: E at checkpoints
500/1500/3000, losses at steps 100/300/1000, the gradient-norm
mean/std over the last 500 steps (none touch the RNG or the update
math — the reproduction gate proves it).

THE BATTERIES (864 runs, ~0.3 s each, resumable via JSONL):
  GATE  4 original splits x seeds 1000-1011 (the reproduction gate)
  A     the scope test: compositional_16 / intermediate_36 /
        random_24 x n=96 (seeds 1000-1095)
  AREP  the independent replication block: compositional_16 x n=96
        (seeds 2000-2095 — a disjoint seed base)
  CTRL  full_49 + random_60 x n=48 (the specificity/floor controls)
  FAM   comp_16 + interm_36 at width 32/128 x n=48 (H4)
  GEO   16 random geometries (sizes 16..44 x geometry seeds 11/23) x
        n=12 (H2's pool + the energy-matched pairs)

Output: seed_boundary_runs.jsonl (per-run records, the checkpoint) +
seed_boundary_results.json (the analyses + the pre-registered
verdicts — the ONLY upgrade paths, per the pre-registration).
"""
import json
import math
import os
import sys
import time

import numpy as np

t0 = time.time()
SCR = os.path.dirname(os.path.abspath(__file__))
RUNS_JSONL = os.path.join(SCR, "seed_boundary_runs.jsonl")
OUT_JSON = os.path.join(SCR, "seed_boundary_results.json")
BANKED_JSON = os.path.join(SCR, "exp3_sheaf_results.json")

P = 7
STEPS = 3000
K_PCA = 3
N_PERM = 10000
STAT_RNG = 20261001


# ---------------------------------------------------------------------
# THE exp3 INSTRUMENT, VERBATIM (width-parameterized; 64 = identical)
# ---------------------------------------------------------------------
def onehot_inputs(pairs):
    X = np.zeros((len(pairs), 2 * P))
    for t, (a, b) in enumerate(pairs):
        X[t, a] = 1.0
        X[t, P + b] = 1.0
    return X


def labels(pairs):
    return np.array([(a + b) % P for a, b in pairs])


class MLP:
    def __init__(self, seed, hid=64):
        r = np.random.default_rng(seed)
        self.W1 = r.normal(0, math.sqrt(2.0 / (2 * P)), (2 * P, hid))
        self.W2 = r.normal(0, math.sqrt(2.0 / hid), (hid, hid))
        self.W3 = r.normal(0, math.sqrt(2.0 / hid), (hid, P))
        self.b1 = np.zeros(hid)
        self.b2 = np.zeros(hid)
        self.b3 = np.zeros(P)

    def hidden(self, X):
        h1 = np.maximum(X @ self.W1 + self.b1, 0.0)
        h2 = np.maximum(h1 @ self.W2 + self.b2, 0.0)
        return h1, h2

    def logits(self, X):
        h1, h2 = self.hidden(X)
        return h2 @ self.W3 + self.b3

    def params(self):
        return [self.W1, self.W2, self.W3, self.b1, self.b2, self.b3]


def token_projectors(m, train_pairs, k=K_PCA):
    X = onehot_inputs(train_pairs)
    _, h2 = m.hidden(X)
    row_ex = {a: [] for a in range(P)}
    col_ex = {b: [] for b in range(P)}
    for t, (a, b) in enumerate(train_pairs):
        row_ex[a].append(h2[t])
        col_ex[b].append(h2[t])
    projs = {}
    for tag, exs_map in (("row", row_ex), ("col", col_ex)):
        for tok, exs in exs_map.items():
            if len(exs) < k + 1:
                projs[(tag, tok)] = None
                continue
            M = np.array(exs)
            Mc = M - M.mean(axis=0)
            U, s, Vt = np.linalg.svd(Mc, full_matrices=False)
            V = Vt[:k].T
            projs[(tag, tok)] = V
    return projs


def coboundary_energy(m, train_pairs, projs, k=K_PCA):
    X = onehot_inputs(train_pairs)
    _, h2 = m.hidden(X)
    h2 = h2 - h2.mean(axis=0)
    energies = []
    for t, (a, b) in enumerate(train_pairs):
        Vi = projs[("row", a)]
        Vj = projs[("col", b)]
        if Vi is None or Vj is None:
            continue
        h = h2[t]
        ri = Vi @ (Vi.T @ h)
        rj = Vj @ (Vj.T @ h)
        energies.append(float(np.sum((ri - rj) ** 2) /
                              (np.sum(h ** 2) + 1e-12)))
    return float(np.mean(energies)) if energies else 0.0


def eval_model(m, pairs):
    if not pairs:
        return 1.0, 0.0, 0.0
    X = onehot_inputs(pairs)
    y = labels(pairs)
    logits = m.logits(X)
    pred = logits.argmax(axis=1)
    acc = float((pred == y).mean())
    pout = np.exp(logits - logits.max(axis=1, keepdims=True))
    pout = pout / pout.sum(axis=1, keepdims=True)
    conf_wrong = []
    for t in range(len(y)):
        if pred[t] != y[t]:
            conf_wrong.append(float(pout[t, pred[t]]))
    nll = float(-np.log(pout[np.arange(len(y)), y] + 1e-300).mean())
    return acc, nll, (float(np.mean(conf_wrong)) if conf_wrong else 0.0)


def build_split(train_a, train_b):
    pairs = [(a, b) for a in range(train_a) for b in range(train_b)]
    all_pairs = [(a, b) for a in range(P) for b in range(P)]
    ood = [p for p in all_pairs if p not in pairs]
    return pairs, ood


def build_random_split(n_train, seed=5):
    r = np.random.default_rng(seed)
    idx = sorted(r.choice(P * P, size=n_train, replace=False))
    tr = [((i // P), (i % P)) for i in idx]
    ood = [p for p in [(a, b) for a in range(P) for b in range(P)]
           if p not in tr]
    return tr, ood


# ---------------------------------------------------------------------
# THE TRAINED RUN — exp3's loop VERBATIM + pure-read instrumentation
# ---------------------------------------------------------------------
def train_recorded(train_pairs, seed, width=64, steps=STEPS, lr=0.01):
    m = MLP(seed, width)
    X = onehot_inputs(train_pairs)
    y = labels(train_pairs)
    Y = np.eye(P)[y]
    mW = [np.zeros_like(p) for p in m.params()]
    vW = [np.zeros_like(p) for p in m.params()]
    ps = m.params()
    rec = {"loss_100": None, "loss_300": None, "loss_1000": None,
           "gn_mean": None, "gn_std": None,
           "E_500": None, "E_1500": None, "E_3000": None}
    gn_tail = []
    nll = 0.0
    for s in range(steps):
        h1 = np.maximum(X @ m.W1 + m.b1, 0.0)
        h2 = np.maximum(h1 @ m.W2 + m.b2, 0.0)
        logits = h2 @ m.W3 + m.b3
        pout = np.exp(logits - logits.max(axis=1, keepdims=True))
        pout = pout / pout.sum(axis=1, keepdims=True)
        nll = float(-np.log(pout[np.arange(len(y)), y] + 1e-300).mean())
        if s == 99:
            rec["loss_100"] = nll
        elif s == 299:
            rec["loss_300"] = nll
        elif s == 999:
            rec["loss_1000"] = nll
        dlog = pout.copy()
        dlog[np.arange(len(y)), y] -= 1.0
        dlog /= len(y)
        dW3 = h2.T @ dlog
        db3 = dlog.sum(axis=0)
        dh2 = dlog @ m.W3.T
        dz2 = dh2 * (h2 > 0)
        dW2 = h1.T @ dz2
        db2 = dz2.sum(axis=0)
        dh1 = dz2 @ m.W2.T
        dz1 = dh1 * (h1 > 0)
        dW1 = X.T @ dz1
        db1 = dz1.sum(axis=0)
        grads = [dW1, dW2, dW3, db1, db2, db3]
        if s >= steps - 500:
            gn_tail.append(math.sqrt(sum(float(np.sum(g * g))
                                         for g in grads)))
        for i, (pp, g) in enumerate(zip(ps, grads)):
            mW[i] = 0.9 * mW[i] + 0.1 * g
            vW[i] = 0.999 * vW[i] + 0.001 * g * g
            mh = mW[i] / (1 - 0.9 ** (s + 1))
            vh = vW[i] / (1 - 0.999 ** (s + 1))
            pp -= lr * mh / (np.sqrt(vh) + 1e-8)
        if s == 499 or s == 1499 or s == steps - 1:
            projs = token_projectors(m, train_pairs)
            E = coboundary_energy(m, train_pairs, projs)
            rec["E_500" if s == 499 else
                "E_1500" if s == 1499 else "E_3000"] = E
    rec["train_nll_final"] = nll
    rec["gn_mean"] = float(np.mean(gn_tail))
    rec["gn_std"] = float(np.std(gn_tail))
    return m, rec


def run_one(spec):
    (battery, split, gseed, width, seed) = spec
    if split == "compositional_16":
        tr, ood = build_split(4, 4)
    elif split == "intermediate_36":
        tr, ood = build_split(6, 6)
    elif split == "full_49":
        tr, ood = build_split(7, 7)
    elif split == "random_60":
        tr, ood = build_random_split(30, 5)
    elif split == "random_24":
        tr, ood = build_random_split(24, 7)
    elif split == "random_geo":
        tr, ood = build_random_split(gseed // 100, gseed % 100)
    else:
        raise ValueError(split)
    m, rec = train_recorded(tr, seed, width)
    acc_tr, nll_tr, _ = eval_model(m, tr)
    acc_ood, nll_ood, conf_wrong = eval_model(m, ood)
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
# THE SPEC LIST (gate order first — reproduction before new data)
# ---------------------------------------------------------------------
ORIG_SPLITS = ["compositional_16", "intermediate_36", "full_49",
               "random_60"]
SCOPE_SPLITS = ["compositional_16", "intermediate_36", "random_24"]

specs = []
for sp in ORIG_SPLITS:                                   # the GATE runs
    for sd in range(1000, 1012):
        specs.append(("GATE", sp, 0, 64, sd))
for sp in ["compositional_16", "intermediate_36"]:        # A: 1012-1095
    for sd in range(1012, 1096):                          # (the gate's
        specs.append(("A", sp, 0, 64, sd))                # 12 complete
for sd in range(1000, 1096):                             #  the 96)
    specs.append(("A", "random_24", 0, 64, sd))           # A: new split
for sd in range(2000, 2096):                             # AREP: n=96
    specs.append(("AREP", "compositional_16", 0, 64, sd))
for sp in ["full_49", "random_60"]:                      # CTRL: n=48
    for sd in range(1012, 1048):
        specs.append(("CTRL", sp, 0, 64, sd))
for sp in ["compositional_16", "intermediate_36"]:       # FAM
    for w in (32, 128):
        for sd in range(1000, 1048):
            specs.append(("FAM", sp, 0, w, sd))
for size in (16, 20, 24, 28, 32, 36, 40, 44):            # GEO
    for gs in (11, 23):
        for sd in range(1000, 1012):
            specs.append(("GEO", "random_geo", size * 100 + gs, 64, sd))


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


# ---------------------------------------------------------------------
# THE REPRODUCTION GATE (before any new data)
# ---------------------------------------------------------------------
def gate_check(done):
    banked = json.load(open(BANKED_JSON))
    bank = {(r["split"], r["seed"]): r for r in banked["runs"]}
    worst_dE, fails = 0.0, []
    for sp in ORIG_SPLITS:
        for sd in range(12):
            k = "GATE|%s|g0|w64|s%d" % (sp, 1000 + sd)
            if k not in done:
                return None                                # not ready
            r = done[k]
            b = bank[(sp, sd)]
            dE = abs(r["coboundary_energy"] - b["coboundary_energy"])
            worst_dE = max(worst_dE, dE)
            if dE > 1e-9 or r["ood_acc"] != b["ood_acc"]:
                fails.append((sp, sd, dE, r["ood_acc"], b["ood_acc"]))
    if fails:
        print("GATE FAIL — instrument drift (%d mismatches):" % len(fails))
        for f in fails[:6]:
            print("   ", f)
        sys.exit(1)
    print("GATE PASS — 48/48 runs reproduce the banked exp3 numbers "
          "(worst |dE| = %.2e, OOD acc exact)" % worst_dE)
    return worst_dE


# ---------------------------------------------------------------------
# THE STATISTICS (numpy-only, fixed permutation seed)
# ---------------------------------------------------------------------
def pearson(x, y):
    x, y = np.array(x, float), np.array(y, float)
    if x.std() < 1e-12 or y.std() < 1e-12:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def rankdata(v):
    v = np.array(v, float)
    order = np.argsort(v, kind="mergesort")
    ranks = np.empty(len(v), float)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(x, y):
    return pearson(rankdata(x), rankdata(y))


def fisher_ci(r, n, conf=0.95):
    z = math.atanh(max(-0.999999, min(0.999999, r)))
    se = 1.0 / math.sqrt(n - 3)
    zm = 1.959963984540054 if conf == 0.95 else 1.6448536269514722
    return (math.tanh(z - zm * se), math.tanh(z + zm * se))


def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def perm_p(x, y, stat=pearson, n_perm=N_PERM):
    rng = np.random.default_rng(STAT_RNG)
    obs = stat(x, y)
    y = np.array(y, float)
    cnt = 0
    for _ in range(n_perm):
        yp = rng.permutation(y)
        if abs(stat(x, yp)) >= abs(obs):
            cnt += 1
    return float((cnt + 1) / (n_perm + 1)), obs


def tost_p(r, n, delta=0.30):
    z = math.atanh(max(-0.999999, min(0.999999, r)))
    se = 1.0 / math.sqrt(n - 3)
    zd = math.atanh(delta)
    p_low = 1.0 - phi((z + zd) / se)     # H0: rho <= -delta
    p_high = phi((z - zd) / se)          # H0: rho >= +delta
    return float(max(p_low, p_high))


def bootstrap_ci(x, y, n_boot=N_PERM):
    rng = np.random.default_rng(STAT_RNG + 1)
    x, y = np.array(x, float), np.array(y, float)
    n = len(x)
    stats = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        if x[idx].std() < 1e-12 or y[idx].std() < 1e-12:
            continue
        stats.append(pearson(x[idx], y[idx]))
    if not stats:
        return (float("nan"), float("nan"))
    stats = np.sort(np.array(stats))
    return (float(np.percentile(stats, 2.5)),
            float(np.percentile(stats, 97.5)))


def bh_fdr(pvals, q=0.05):
    m = len(pvals)
    order = np.argsort(np.array(pvals))
    adj = {}
    prev = 1.0
    for rank_i in range(m - 1, -1, -1):
        i = order[rank_i]
        val = min(prev, pvals[i] * m / (rank_i + 1))
        prev = val
        adj[i] = val
    return {i: adj[i] for i in range(m)}, [i for i in adj if adj[i] < q]


def full_stats(x, y, label="", stat=pearson):
    n = len(x)
    r = pearson(x, y)
    rs = spearman(x, y)
    p, _ = perm_p(x, y, stat=stat)
    return {"label": label, "n": n, "pearson": r, "spearman": rs,
            "fisher_ci95": fisher_ci(r, n), "perm_p": p,
            "tost_p_delta030": tost_p(r, n),
            "bootstrap_ci95": bootstrap_ci(x, y)}


# ---------------------------------------------------------------------
# THE VERDICT RULES (pre-registered — the ONLY upgrade paths)
# ---------------------------------------------------------------------
COVARIATES = ["E_500", "E_1500", "loss_100", "loss_300", "loss_1000",
              "train_nll_final", "gn_mean", "gn_std",
              "ood_wrong_confidence"]


def scope_rule(split_stats, rep_stat=None):
    """H1's rule, verbatim from the pre-registration."""
    var_splits = [s for s in split_stats if s["ood_std"] > 0.02]
    if not var_splits:
        return "FLOOR (no OOD variance — control only)"
    strong = [s for s in var_splits
              if abs(s["r"]) >= 0.30 and s["p"] < 0.01]
    tost_ok = all(s["tost"] < 0.05 for s in var_splits)
    if strong:
        confirmed = (rep_stat is not None and
                     (rep_stat["r"] * strong[0]["r"]) > 0 and
                     rep_stat["p"] < 0.05 and
                     abs(rep_stat["r"]) >= 0.30)
        return ("REFUTED — E is a seed-level signal" if confirmed else
                "NARROWED — strong split-level signal, replication "
                "pending/block absent")
    if tost_ok:
        return "LAW — equivalence to |rho|<0.30 established"
    return "NARROWED — measured, below practical predictivity, CI open"


GATE_KEYS = {"GATE|%s|g0|w64|s%d" % (sp, sd)
             for sp in ORIG_SPLITS for sd in range(1000, 1012)}


def main():
    done = load_done()
    gate = gate_check(done)
    if gate is None:
        print("collecting the GATE runs (reproduction-first) ...")
    todo = [s for s in specs if ("%s|%s|g%d|w%d|s%d" % s) not in done]
    n_new = 0
    for spec in todo:
        if gate is None and GATE_KEYS <= set(done):
            gate = gate_check(done)     # exits on drift
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


def analyze(done, gate_worst_dE):
    all_recs = list(done.values())

    def sel(battery=None, split=None, width=None, seeds=None):
        out = []
        for r in all_recs:
            if battery and r["battery"] not in battery:
                continue
            if split and r["split"] != split:
                continue
            if width and r["width"] != width:
                continue
            if seeds and not (seeds[0] <= r["seed"] < seeds[1]):
                continue
            out.append(r)
        return out

    # ---------------- H1: the scope test --------------------------
    scope = {}
    for sp in SCOPE_SPLITS:
        runs = sel({"GATE", "A"}, sp, 64)
        x = [r["coboundary_energy"] for r in runs]
        y = [1 - r["ood_acc"] for r in runs]
        st = full_stats(x, y, sp)
        st["ood_std"] = float(np.std(y))
        scope[sp] = st
    rep_runs = sel({"AREP"}, "compositional_16", 64)
    rep = full_stats([r["coboundary_energy"] for r in rep_runs],
                     [1 - r["ood_acc"] for r in rep_runs],
                     "AREP comp_16 (seeds 2000-2095)")
    split_stats = [{"r": s["pearson"], "p": s["perm_p"],
                    "tost": s["tost_p_delta030"],
                    "ood_std": s["ood_std"], "split": sp}
                   for sp, s in scope.items()]
    h1 = scope_rule(split_stats, rep)

    # ---------------- the secondary endpoint ----------------------
    secondary = {sp: full_stats(
        [r["coboundary_energy"] for r in sel({"GATE", "A"}, sp, 64)],
        [r["ood_wrong_confidence"] for r in sel({"GATE", "A"}, sp, 64)],
        sp + " E vs wrong-OOD confidence") for sp in SCOPE_SPLITS}

    # ---------------- H3: the covariate panel ---------------------
    cov = {}
    for sp in SCOPE_SPLITS:
        runs = sel({"GATE", "A"}, sp, 64)
        y = [1 - r["ood_acc"] for r in runs]
        stats_list = []
        for cname in COVARIATES:
            x = [r[cname] for r in runs]
            stats_list.append(full_stats(x, y, cname))
        pvals = [s["perm_p"] for s in stats_list]
        adj, _ = bh_fdr(pvals)
        for i, s in enumerate(stats_list):
            s["bh_q"] = adj[i]
        cov[sp] = stats_list
    upgrades = []
    for cname_i, cname in enumerate(COVARIATES):
        sig = [sp for sp in SCOPE_SPLITS
               if next(s for s in cov[sp]
                       if s["label"] == cname)["bh_q"] < 0.05]
        big = [sp for sp in sig
               if abs(next(s for s in cov[sp]
                           if s["label"] == cname)["pearson"]) >= 0.50
               and next(s for s in cov[sp]
                        if s["label"] == cname)["perm_p"] < 0.01]
        if len(big) >= 2:
            upgrades.append((cname, big))
    h3 = ("UPGRADE — seed-level predictor(s) found: %s" % upgrades
          if upgrades else
          "NEGATIVE — no covariate of the panel reaches the "
          "pre-registered bar (|rho|>=0.5, p<0.01, BH q<0.05, >=2/3 "
          "splits) with n=96 per split")

    # ---------------- H2: the geometry level ----------------------
    geos = []
    for sp in SCOPE_SPLITS + ["full_49", "random_60"]:
        runs = sel({"GATE", "A", "CTRL"}, sp, 64)
        if runs:
            geos.append({"name": sp, "kind": "original",
                         "n": len(runs),
                         "E": float(np.mean([r["coboundary_energy"]
                                             for r in runs])),
                         "err": float(np.mean([1 - r["ood_acc"]
                                               for r in runs]))})
    for size in (16, 20, 24, 28, 32, 36, 40, 44):
        for gs in (11, 23):
            runs = [r for r in all_recs
                    if r["battery"] == "GEO"
                    and r["gseed"] == size * 100 + gs]
            geos.append({"name": "rand%d/g%d" % (size, gs),
                         "kind": "geo", "n": len(runs),
                         "E": float(np.mean(
                             [r["coboundary_energy"] for r in runs])),
                         "err": float(np.mean([1 - r["ood_acc"]
                                               for r in runs]))})
    gE = [g["E"] for g in geos]
    gY = [g["err"] for g in geos]
    h2_stat = full_stats(gE, gY, "geometry level (n=20 geometries)",
                          stat=spearman)
    matched = []
    for i in range(len(geos)):
        for j in range(i + 1, len(geos)):
            dE = abs(geos[i]["E"] - geos[j]["E"])
            dO = abs(geos[i]["err"] - geos[j]["err"])
            if dE < 0.01:
                matched.append({"a": geos[i]["name"], "b": geos[j]["name"],
                                "dE": dE, "dOOD": dO})
    max_dOOD_matched = max([m["dOOD"] for m in matched], default=0.0)
    h2 = ("HOLDS — geometry-level Spearman %.3f, perm p=%.4f; "
          "matched-energy pairs max |dOOD| %.3f (< 0.15)"
          % (h2_stat["spearman"], h2_stat["perm_p"], max_dOOD_matched))
    if h2_stat["perm_p"] >= 0.05 or max_dOOD_matched > 0.15:
        h2 = ("REFUTED — " + h2)

    # ---------------- H4: family invariance -----------------------
    fam = {}
    for w in (32, 64, 128):
        for sp in ["compositional_16", "intermediate_36"]:
            runs = [r for r in all_recs
                    if r["split"] == sp and r["width"] == w
                    and (r["battery"] in ("GATE", "A", "FAM"))]
            st = full_stats([r["coboundary_energy"] for r in runs],
                            [1 - r["ood_acc"] for r in runs],
                            "%s w%d (n=%d)" % (sp, w, len(runs)))
            st["ood_std"] = float(np.std([1 - r["ood_acc"]
                                          for r in runs]))
            fam["%s_w%d" % (sp, w)] = st
    fam_verdicts = {k: scope_rule([{"r": s["pearson"],
                                    "p": s["perm_p"],
                                    "tost": s["tost_p_delta030"],
                                    "ood_std": s["ood_std"],
                                    "split": k}])
                    for k, s in fam.items()
                    if s["ood_std"] > 0.02}
    h4_classes = sorted(set(v.split(" ")[0] for v in fam_verdicts.values()))
    h4 = ("INVARIANT — verdict class %s identical across widths"
          % h4_classes if len(h4_classes) == 1 else
          "WIDTH-DEPENDENT — verdict classes differ: %s"
          % {k: v for k, v in fam_verdicts.items()})

    # ---------------- the pooled confound -------------------------
    pooled_runs = sel({"GATE", "A", "CTRL"}, None, 64)
    pooled = full_stats([r["coboundary_energy"] for r in pooled_runs],
                        [1 - r["ood_acc"] for r in pooled_runs],
                        "pooled (scope+controls, n=%d)" % len(pooled_runs))

    # ---------------- the controls' specificity --------------------
    ctrl = {}
    for sp in ORIG_SPLITS:
        runs = sel({"GATE", "A", "CTRL"}, sp, 64)
        ctrl[sp] = {"n": len(runs),
                    "E_mean": float(np.mean([r["coboundary_energy"]
                                             for r in runs])),
                    "E_std": float(np.std([r["coboundary_energy"]
                                           for r in runs])),
                    "ood_acc_std": float(np.std([r["ood_acc"]
                                                 for r in runs]))}

    out = {
        "meta": {
            "experiment": "THE PRE-REGISTERED SEED-BOUNDARY EXPERIMENT",
            "prereg": "download/seed_boundary_preregistration.md "
                      "(committed before the run)",
            "instrument": "exp3_sheaf.py verbatim (width-parameterized), "
                          "reproduction-gated",
            "runs_total": len(all_recs),
            "gate_worst_dE": gate_worst_dE,
            "wall_s": round(time.time() - t0, 1),
            "n_perm": N_PERM, "stat_rng": STAT_RNG},
        "H1_scope": {"per_split": scope, "independent_replication": rep,
                     "verdict": h1},
        "secondary_hallucination": secondary,
        "H3_covariates": {"per_split": cov, "verdict": h3},
        "H2_task_level": {"geometries": geos, "stat": h2_stat,
                          "energy_matched_pairs": matched,
                          "verdict": h2},
        "H4_family": {"per_cell": fam, "verdicts": fam_verdicts,
                      "verdict": h4},
        "pooled_confound": pooled,
        "controls": ctrl,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1, default=float)

    print("\n" + "=" * 68)
    print("H1 THE SCOPE LAW: %s" % h1)
    for sp, s in scope.items():
        print("   %-16s r=%+.3f  CI95 [%.3f, %.3f]  perm p=%.4f  "
              "TOST p=%.4f  (ood_std %.3f, n=%d)"
              % (sp, s["pearson"], s["fisher_ci95"][0],
                 s["fisher_ci95"][1], s["perm_p"],
                 s["tost_p_delta030"], s["ood_std"], s["n"]))
    print("   replication block: r=%+.3f (p=%.4f, n=%d)"
          % (rep["pearson"], rep["perm_p"], rep["n"]))
    print("H2 THE TASK-LEVEL LAW: %s" % h2)
    print("H3 THE COVARIATE PANEL: %s" % h3)
    for sp in SCOPE_SPLITS:
        top = sorted(cov[sp], key=lambda s: -abs(s["pearson"]))[:3]
        print("   %-16s top: %s" % (sp, "; ".join(
            "%s r=%+.3f (q=%.3f)" % (s["label"], s["pearson"],
                                     s["bh_q"]) for s in top)))
    print("H4 FAMILY INVARIANCE: %s" % h4)
    print("   pooled (the confound): r=%.3f (n=%d)"
          % (pooled["pearson"], pooled["n"]))
    print("results written:", OUT_JSON)


if __name__ == "__main__":
    main()
