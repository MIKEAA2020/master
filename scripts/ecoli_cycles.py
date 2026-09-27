#!/usr/bin/env python3
"""
Task 8: E. coli cycle-size scan for the 0.361 relaxation rate.

Prediction tested (Vol III, Theorem II / Prediction 1):
  the viability cascade relaxes geometrically per closed cycle with rate
  -ln(0.92^6 * 1.15) = -ln(0.697) ~ 0.361 per cycle; i.e. the approach of
  the response to its asymptote over cycle index k follows 1 - 0.697^k,
  a semi-log slope of 0.361 per cycle.

Experiment (following the corpus protocol, mcm_main v22:
  sequential knockouts by L1-MOMA, closed cycles A -> AB -> B -> WT):
  1. load iJO1366 (glucose minimal, aerobic), reference = pFBA state.
  2. screen viable single/double knockouts (FBA biomass >= 0.1 mu_WT).
  3. for each gene pair: traverse the closed cycle K=16 times,
     each step = L1-MOMA projection (min ||v - v_ref||_1, S v = 0,
     current knockout bounds).
  4. record the state after each full traversal; estimate the fixed
     point v_inf (last state); residuals r_k = ||v_k - v_inf||_1;
     drift D_k = ||v_k - v_0||_1.
  5. fit ln r_k vs k (linear) -> relaxation rate per cycle; compare to
     0.361. Also fit D_k = D_inf (1 - rho^k).

Output: /home/z/my-project/scripts/ecoli_cycles_results.json
        /home/z/my-project/download/ecoli_cycle_scan.png
Progressive checkpointing after each pair.
"""
import json
import re
import time
import numpy as np
from scipy import sparse
from scipy.optimize import linprog

MODEL = ("/home/z/my-project/github_repos/metabolic-curvature-"
         "measure/data/bigg_models/iJO1366.json")
OUT_JSON = "/home/z/my-project/scripts/ecoli_cycles_results.json"
OUT_PNG = "/home/z/my-project/download/ecoli_cycle_scan.png"
N_PAIRS = 20
K_CYCLES = 16
VIABLE_FRAC = 0.1
PRED_RATE = -np.log(0.92 ** 6 * 1.15)      # 0.361 per cycle


# ---------------- model parsing ----------------
class Model:
    def __init__(self, path):
        M = json.load(open(path))
        self.rxn_ids = [r['id'] for r in M['reactions']]
        self.met_ids = [m['id'] for m in M['metabolites']]
        self.ridx = {r: i for i, r in enumerate(self.rxn_ids)}
        self.midx = {m: i for i, m in enumerate(self.met_ids)}
        n_r, n_m = len(self.rxn_ids), len(self.met_ids)
        self.lb = np.array([r['lower_bound'] for r in M['reactions']])
        self.ub = np.array([r['upper_bound'] for r in M['reactions']])
        obj = np.array([r.get('objective_coefficient', 0) or 0
                        for r in M['reactions']])
        self.bio = int(np.argmax(obj))
        rows, cols, vals = [], [], []
        for j, r in enumerate(M['reactions']):
            for met, sto in r['metabolites'].items():
                rows.append(self.midx[met])
                cols.append(j)
                vals.append(sto)
        self.S = sparse.csc_matrix(
            (vals, (rows, cols)), shape=(n_m, n_r))
        # GPR: parse each rule ONCE into an evaluable token list
        self.gpr_tokens = {}
        for j, r in enumerate(M['reactions']):
            rule = r.get('gene_reaction_rule', '') or ''
            toks = tokenize_gpr(rule)
            if toks:
                self.gpr_tokens[j] = toks
        self.gene_set = set()
        for toks in self.gpr_tokens.values():
            for t in toks:
                if t not in ('(', ')', 'and', 'or'):
                    self.gene_set.add(t)


def tokenize_gpr(rule):
    if not rule or rule.isspace():
        return []
    rule = rule.replace('(', ' ( ').replace(')', ' ) ')
    toks = rule.split()
    out = []
    for t in toks:
        tl = t.lower()
        if tl == 'and' or tl == 'or':
            out.append(tl)
        elif t in ('(', ')'):
            out.append(t)
        elif t:
            out.append(t)
    return out


def eval_gpr(tokens, ko, cache):
    """evaluate GPR with knocked-out gene set ko (True = active).
    Recursive descent: expr = term (or term)*; term = factor (and factor)*
    factor = '(' expr ')' | gene."""
    key = (id(tokens), len(ko))
    pos = [0]

    def peek():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def factor():
        t = peek()
        if t == '(':
            pos[0] += 1
            val = expr()
            if peek() == ')':
                pos[0] += 1
            return val
        pos[0] += 1
        return t not in ko          # gene active iff not knocked out

    def term():
        v = factor()
        while peek() == 'and':
            pos[0] += 1
            v = v and factor()
        return v

    def expr():
        v = term()
        while peek() == 'or':
            pos[0] += 1
            v = v or term()
        return v

    return expr()


# ---------------- LP wrappers ----------------
def solve_lp(c, S, lb, ub, extra=None):
    """min c.x s.t. S x = 0 (or extra rows), lb <= x <= ub."""
    n = len(lb)
    A = S
    b = np.zeros(S.shape[0])
    if extra is not None:
        A2, b2 = extra
        A = sparse.vstack([S, A2], format='csc')
        b = np.concatenate([b, b2])
    res = linprog(c, A_eq=A, b_eq=b, bounds=list(zip(lb, ub)),
                  method='highs')
    if not res.success:
        return None
    return res.x


def fba(model, lb, ub):
    c = np.zeros(len(lb))
    c[model.bio] = -1.0
    x = solve_lp(c, model.S, lb, ub)
    return -c @ x if x is not None else None, x


def pfba_state(model, lb, ub):
    """max biomass then min ||v||_1 (parsimonious), deterministic."""
    mu, x = fba(model, lb, ub)
    if x is None:
        return None, None
    n = len(lb)
    # min ||v||_1: vars (v, p, n): p - n = v, p,n >= 0, sum p+n min,
    # biomass fixed at optimum (tolerance)
    c2 = np.concatenate([np.zeros(n), np.ones(n), np.ones(n)])
    I = sparse.eye(n, format='csc')
    A2 = sparse.hstack([I, -I, I], format='csc')
    row = np.zeros(n)
    row[model.bio] = 1.0
    A3 = sparse.hstack([sparse.csr_matrix(row), sparse.csr_matrix(
        (1, 2 * n))], format='csc')
    A2full = sparse.vstack([A2, A3], format='csc')
    b2 = np.concatenate([np.zeros(n), [mu * (1 - 1e-9)]])
    lb2 = np.concatenate([lb, np.zeros(2 * n)])
    ub2 = np.concatenate([ub, np.full(2 * n, np.inf)])
    Sfull = sparse.hstack([model.S, sparse.csr_matrix(
        (model.S.shape[0], 2 * n))], format='csc')
    x2 = solve_lp(c2, Sfull, lb2, ub2, extra=(A2full, b2))
    if x2 is None:
        return mu, x
    return mu, x2[:n]


def l1_moma(model, lb, ub, v_ref):
    """min ||v - v_ref||_1 s.t. S v = 0, lb <= v <= ub."""
    n = len(lb)
    c = np.concatenate([np.zeros(n), np.ones(n), np.ones(n)])
    I = sparse.eye(n, format='csc')
    A2 = sparse.hstack([I, -I, I], format='csc')
    b2 = v_ref
    Sfull = sparse.hstack([model.S, sparse.csr_matrix(
        (model.S.shape[0], 2 * n))], format='csc')
    lb2 = np.concatenate([lb, np.zeros(2 * n)])
    ub2 = np.concatenate([ub, np.full(2 * n, np.inf)])
    x = solve_lp(c, Sfull, lb2, ub2, extra=(A2, b2))
    if x is None:
        return None
    return x[:n]


def ko_bounds(model, ko_genes):
    lb = model.lb.copy()
    ub = model.ub.copy()
    for j, toks in model.gpr_tokens.items():
        if not eval_gpr(toks, ko_genes, None):
            lb[j] = 0.0
            ub[j] = 0.0
    return lb, ub


# =====================================================================
def main():
    t0 = time.time()
    print("loading model...")
    model = Model(MODEL)
    print(f"  {len(model.rxn_ids)} reactions, {model.met_ids.__len__()} "
          f"metabolites, {len(model.gene_set)} genes, "
          f"biomass = {model.rxn_ids[model.bio]}")

    # WT reference
    mu_wt, v0 = pfba_state(model, model.lb, model.ub)
    print(f"  WT pFBA growth = {mu_wt:.6f}, ||v0||_1 = "
          f"{np.abs(v0).sum():.1f}")

    results = {"model": "iJO1366", "medium": "glucose minimal (BiGG "
               "default: EX_glc__D_e -10, EX_o2_e -1000)",
               "mu_wt": mu_wt, "K_cycles": K_CYCLES,
               "pred_rate": PRED_RATE, "pairs": []}

    # screening: viable single knockouts
    print("screening viable single knockouts...")
    genes = sorted(model.gene_set)
    viable = []
    for g in genes:
        lb, ub = ko_bounds(model, {g})
        mu, _ = fba(model, lb, ub)
        if mu is not None and mu >= VIABLE_FRAC * mu_wt:
            viable.append((g, mu))
    print(f"  {len(viable)} viable single knockouts of "
          f"{len(genes)} genes ({time.time()-t0:.0f}s)")

    # effective-gene screen: single-KO L1-MOMA drift from v0 > 1.0
    # (non-degenerate loops only, mirroring the corpus's protocol)
    print("screening effective genes (single-KO MOMA drift)...")
    effective = []
    for g, mu in viable:
        lb, ub = ko_bounds(model, {g})
        v1 = l1_moma(model, lb, ub, v0)
        if v1 is None:
            continue
        drift = float(np.abs(v1 - v0).sum())
        if drift > 1.0:
            effective.append((g, mu, drift))
    print(f"  {len(effective)} effective genes of {len(viable)} viable "
          f"({time.time()-t0:.0f}s)")

    # deterministic pair selection: sort by drift, pair halves
    effective.sort(key=lambda gm: -gm[2])   # decreasing drift
    half = len(effective) // 2
    pairs = []
    for i in range(N_PAIRS * 3):
        gA = effective[i][0]
        gB = effective[(i + half) % len(effective)][0]
        if gB == gA:
            continue
        lb, ub = ko_bounds(model, {gA, gB})
        mu, _ = fba(model, lb, ub)
        if mu is None or mu < VIABLE_FRAC * mu_wt:
            continue
        # first-cycle non-degeneracy: D_1 > 1.0
        v = v0.copy()
        for lbk, ubk in [ko_bounds(model, {gA}),
                         (lb.copy(), ub.copy()),
                         ko_bounds(model, {gB}),
                         (model.lb.copy(), model.ub.copy())]:
            v = l1_moma(model, lbk, ubk, v)
            if v is None:
                break
        if v is None or np.abs(v - v0).sum() <= 1.0:
            continue
        pairs.append((gA, gB))
        if len(pairs) >= N_PAIRS:
            break
    print(f"  {len(pairs)} non-degenerate viable pairs selected")

    for ip, (gA, gB) in enumerate(pairs):
        tp = time.time()
        # bounds per stage
        bA = ko_bounds(model, {gA})
        bAB = ko_bounds(model, {gA, gB})
        bB = ko_bounds(model, {gB})
        bWT = (model.lb.copy(), model.ub.copy())

        v = v0.copy()
        states = [v.copy()]
        ok = True
        for k in range(K_CYCLES):
            for (lbk, ubk) in [bA, bAB, bB, bWT]:
                v_new = l1_moma(model, lbk, ubk, v)
                if v_new is None:
                    ok = False
                    break
                v = v_new
            if not ok:
                break
            states.append(v.copy())
        if not ok:
            print(f"  [{ip+1}] {gA}+{gB}: LP failure, skipped")
            continue

        states = np.array(states)
        vinf = states[-1]
        r = np.linalg.norm(states - vinf, ord=1, axis=1)   # r_0..r_K
        D = np.linalg.norm(states - v0, ord=1, axis=1)
        ks = np.arange(len(r))
        # fit ln r_k vs k over the decaying, positive part (k >= 1,
        # r_k above noise floor)
        noise = 1e-7 * np.abs(v0).sum()
        sel = (ks >= 1) & (r > noise) & (np.arange(len(r)) <= len(r) - 3)
        rate = np.nan
        rr2 = np.nan
        if sel.sum() >= 4:
            xk = ks[sel].astype(float)
            yk = np.log(r[sel])
            slope, icept = np.polyfit(xk, yk, 1)
            pred = slope * xk + icept
            rr2 = 1 - np.sum((yk - pred) ** 2) / np.sum(
                (yk - np.mean(yk)) ** 2)
            rate = -slope
        # approach-to-asymptote fit D_k = D_inf (1 - rho^k):
        Dinf = D[-1]
        rho = np.nan
        rho_r2 = np.nan
        selD = (ks >= 1) & (Dinf - D > noise) & (ks <= len(r) - 3)
        if selD.sum() >= 4 and Dinf > noise:
            xk = ks[selD].astype(float)
            yk = np.log(Dinf - D[selD])
            sl, ic = np.polyfit(xk, yk, 1)
            pr = sl * xk + ic
            rho_r2 = 1 - np.sum((yk - pr) ** 2) / np.sum(
                (yk - np.mean(yk)) ** 2)
            rho = np.exp(sl)          # D_inf - D_k ~ rho^k
        rec = {"geneA": gA, "geneB": gB,
               "rates_residual": float(rate), "R2_residual": float(rr2),
               "rho_drift": float(rho), "R2_drift": float(rho_r2),
               "D_inf": float(Dinf), "D_k": D.tolist(),
               "r_k": r.tolist(), "locked": bool(Dinf > noise)}
        results["pairs"].append(rec)
        print(f"  [{ip+1}/{len(pairs)}] {gA} + {gB}: rate = "
              f"{rate:.4f}/cycle (R2={rr2:.3f}), rho_drift = "
              f"{rho if not np.isnan(rho) else float('nan'):.4f}, "
              f"D_inf = {Dinf:.1f}  [{time.time()-tp:.0f}s]")
        with open(OUT_JSON, "w") as fh:
            json.dump(results, fh, indent=1)

    # panel statistics
    rates = [p["rates_residual"] for p in results["pairs"]
             if not np.isnan(p["rates_residual"]) and p["R2_residual"] > 0.9]
    rhos = [p["rho_drift"] for p in results["pairs"]
            if not np.isnan(p["rho_drift"]) and p["R2_drift"] > 0.9]
    if rates:
        rates = np.array(rates)
        results["panel"] = {
            "n_geometric": len(rates),
            "rate_median": float(np.median(rates)),
            "rate_mean": float(rates.mean()),
            "rate_mad": float(np.median(np.abs(rates - np.median(rates)))),
            "rate_quartiles": [float(q) for q in
                                np.percentile(rates, [25, 50, 75])],
            "pred_rate": PRED_RATE,
        }
        print("\nPANEL: n =", len(rates),
              " rate median = %.4f" % np.median(rates),
              " (prediction 0.361), MAD = %.4f" %
              np.median(np.abs(rates - np.median(rates))))
    if rhos:
        rhos = np.array(rhos)
        results["panel_rho"] = {
            "n": len(rhos), "rho_median": float(np.median(rhos)),
            "rho_quartiles": [float(q) for q in
                              np.percentile(rhos, [25, 50, 75])],
            "pred_rho": 0.697}
        print("RHO: n =", len(rhos), " median = %.4f" % np.median(rhos),
              " (prediction 0.697)")
    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=1)
    print(f"\ntotal time {time.time()-t0:.0f}s -> {OUT_JSON}")

    # ---------------- figure ----------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.font_manager as fm
    fm.fontManager.addfont(
        '/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
    fm.fontManager.addfont(
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Noto Sans SC']
    plt.rcParams['axes.unicode_minus'] = False

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6),
                             constrained_layout=True)
    ax = axes[0]
    for p in results["pairs"]:
        rr = np.array(p["r_k"])
        ks = np.arange(len(rr))
        sel = (ks >= 1) & (rr > 0)
        ax.semilogy(ks[sel], rr[sel], '-', color='#4e4732', alpha=0.45,
                    lw=1.1)
    xs = np.arange(0, K_CYCLES + 1)
    ax.semilogy(xs, np.exp(-PRED_RATE * xs) * np.nan, color='#92761f')
    # predicted line anchored at a representative r_1
    if results["pairs"]:
        r1s = [p["r_k"][1] for p in results["pairs"] if len(p["r_k"]) > 2]
        if r1s:
            ax.semilogy(xs, np.median(r1s) * np.exp(-PRED_RATE * xs),
                        '--', color='#92761f', lw=2.2,
                        label='prediction $e^{-0.361k}$')
    ax.set_xlabel('closed-cycle index $k$')
    ax.set_ylabel('residual $\\|v_k - v_\\infty\\|_1$')
    ax.set_title('(a) E. coli closed-cycle relaxation '
                 '($A\\to AB\\to B\\to$WT, L1-MOMA)')
    ax.legend(fontsize=9)

    ax = axes[1]
    rates_all = [p["rates_residual"] for p in results["pairs"]
                 if not np.isnan(p["rates_residual"])]
    if rates_all:
        ax.hist(rates_all, bins=np.arange(0, 1.6, 0.08),
                color='#4e4732', alpha=0.85)
    ax.axvline(PRED_RATE, color='#92761f', ls='--', lw=2.2,
               label='prediction 0.361')
    if "panel" in results:
        ax.axvline(results["panel"]["rate_median"], color='#8a2be2',
                   ls=':', lw=2, label='median %.3f' %
                   results["panel"]["rate_median"])
    ax.set_xlabel('relaxation rate per cycle $-\\ln\\rho$')
    ax.set_ylabel('pairs')
    ax.set_title('(b) rate distribution vs the cascade prediction')
    ax.legend(fontsize=9)
    fig.suptitle('E. coli cycle-size scan: geometric relaxation vs '
                 'the graded small-gain rate 0.361/cycle', fontsize=12)
    fig.savefig(OUT_PNG, dpi=170)
    print(f"figure -> {OUT_PNG}")


if __name__ == "__main__":
    main()
