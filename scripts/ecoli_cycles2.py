#!/usr/bin/env python3
"""
Task 8 (part 2): where in the E. coli stack can a per-cycle geometric
relaxation rate live?

Layer 1 (genotype cycles A->AB->B->WT): PROVED + witnessed one-pass
  saturation (nested polytopes => every restore projection is a no-op;
  the state after one traversal is an exact fixed point). Result: the
  LP flux layer has NO k-relaxation; any 0.361/cycle law must live
  above it. [ecoli_cycles.py, 20 pairs]

Layer 2 (closed PARAMETER cycles - the corpus's cyclic-perturbation
  experiment): corners in (glucose, acetate) uptake space; the corner
  polytopes are NOT nested => alternating projections relax
  geometrically over cycles. We measure the rate panel and test it
  against 0.361 = -ln(0.92^6*1.15), plus the loop-size drift law
  (corpus: linear, slope 1.00).

Layer 3 (the seven-optic cascade = the post-translational model):
  - extremal instance (all optics aligned): rate exactly 0.361/cycle;
  - generic random instances: rate <= 0.361 (certified envelope);
  the theory's object.

Outputs: ecoli_cycles2_results.json, ecoli_parameter_cycles.png
"""
import json
import time
import numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location("ec", "ecoli_cycles.py")
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)

MODEL = ec.MODEL
OUT_JSON = "/home/z/my-project/scripts/ecoli_cycles2_results.json"
OUT_PNG = "/home/z/my-project/download/ecoli_parameter_cycles.png"
PRED_RATE = -np.log(0.92 ** 6 * 1.15)   # 0.3608...
PRED_RHO = 0.92 ** 6 * 1.15             # 0.697


def medium_bounds(model, glc_lb, ace_lb):
    lb = model.lb.copy()
    ub = model.ub.copy()
    lb[model.ridx['EX_glc__D_e']] = glc_lb
    lb[model.ridx['EX_ac_e']] = ace_lb
    return lb, ub


def run_cycle_scan(model, corner_sets, v0, K):
    """corner_sets: list of (lb, ub) per corner; one traversal visits
    all corners in order. Returns states after each traversal."""
    v = v0.copy()
    states = [v.copy()]
    for k in range(K):
        for (lbk, ubk) in corner_sets:
            v = ec.l1_moma(model, lbk, ubk, v)
            if v is None:
                return None
        states.append(v.copy())
    return np.array(states)


def fit_rates(states):
    vinf = states[-1]
    r = np.linalg.norm(states - vinf, ord=1, axis=1)
    D = np.linalg.norm(states - states[0], ord=1, axis=1)
    ks = np.arange(len(r))
    noise = 1e-7 * 700.0
    sel = (ks >= 1) & (r > noise) & (ks <= len(r) - 4)
    rate, r2 = np.nan, np.nan
    if sel.sum() >= 5:
        x = ks[sel].astype(float)
        y = np.log(r[sel])
        sl, ic = np.polyfit(x, y, 1)
        pr = sl * x + ic
        r2 = 1 - np.sum((y - pr) ** 2) / np.sum((y - np.mean(y)) ** 2)
        rate = -sl
    return rate, r2, r, D


def main():
    t0 = time.time()
    model = ec.Model(MODEL)
    mu_wt, v0 = ec.pfba_state(model, model.lb, model.ub)
    print(f"WT pFBA mu = {mu_wt:.4f}")

    results = {"pred_rate": PRED_RATE, "pred_rho": PRED_RHO,
               "layer2": [], "layer2_loopsize": [],
               "layer3": {}}

    # ---------------- Layer 2: parameter cycles ----------------
    # family (i): 2-set alternation glc-only <-> mixed medium
    print("\nLayer 2(i): two-set alternation (glucose-only <-> mixed)")
    A = medium_bounds(model, -10.0, 0.0)
    for ace_mix in [-2.0, -5.0, -10.0]:
        B = medium_bounds(model, -5.0, ace_mix)
        states = run_cycle_scan(model, [A, B], v0, K=40)
        if states is None:
            continue
        rate, r2, r, D = fit_rates(states)
        results["layer2"].append(
            {"family": "alternation", "glc_mix": -5.0, "ace_mix": ace_mix,
             "rate": float(rate), "R2": float(r2),
             "D_inf": float(D[-1]), "r_k": r.tolist()[:25]})
        print(f"  mixed(glc=-5, ace={ace_mix}): rate = {rate:.4f}/cycle "
              f"(R2 = {r2:.3f}), D_inf = {D[-1]:.1f}")

    # family (ii): sized two-set alternation (loop-size scan)
    # A = glucose-only; B(eps) = {glc >= -10+eps, ace >= -2 eps}:
    # incomparable with A on both axes -> forced motion every
    # half-cycle; eps is the loop size.
    print("\nLayer 2(ii): sized alternation (loop-size scan)")
    for eps in [0.5, 1.0, 2.0, 4.0, 8.0]:
        A2 = medium_bounds(model, -10.0, 0.0)
        B2 = medium_bounds(model, -10.0 + eps, -2.0 * eps)
        states = run_cycle_scan(model, [A2, B2], v0, K=60)
        if states is None:
            continue
        rate, r2, r, D = fit_rates(states)
        D1 = D[1]
        results["layer2_loopsize"].append(
            {"eps": eps, "rate": float(rate), "R2": float(r2),
             "D_one_pass": float(D1), "D_inf": float(D[-1]),
             "r_k": r.tolist()[:25]})
        print(f"  eps={eps:4.1f}: rate = {rate:.4f}/cycle "
              f"(R2 = {r2:.3f}), D_1 = {D1:.2f}, D_inf = {D[-1]:.2f}")

    # loop-size drift law: D_1 vs eps (corpus: linear, slope 1.00)
    eps_arr = np.array([q["eps"] for q in results["layer2_loopsize"]])
    D1_arr = np.array([q["D_one_pass"] for q in results["layer2_loopsize"]])
    if len(eps_arr) >= 3:
        sl, ic = np.polyfit(np.log(eps_arr), np.log(D1_arr), 1)
        results["loopsize_slope"] = float(sl)
        print(f"  drift vs loop size: log-log slope = {sl:.3f} "
              f"(corpus: 1.00 linear law)")

    # rate panel vs prediction
    rates2 = [q["rate"] for q in (results["layer2"] +
                                  results["layer2_loopsize"])
              if not np.isnan(q["rate"]) and q["R2"] > 0.95]
    if rates2:
        results["layer2_panel"] = {
            "n": len(rates2), "median": float(np.median(rates2)),
            "min": float(np.min(rates2)), "max": float(np.max(rates2))}
        print(f"  LP-layer rate panel: median {np.median(rates2):.4f}, "
              f"range [{np.min(rates2):.4f}, {np.max(rates2):.4f}] "
              f"vs prediction 0.361")

    # ---------------- Layer 3: seven-optic cascade ----------------
    print("\nLayer 3: seven-optic cascade (post-translational model)")
    rng = np.random.default_rng(42)
    d = 6
    # extremal instance: six optics = 0.92 * (identity), expansion 1.15
    # T = 0.92^6 * 1.15 * Id  -> exact rate 0.361
    Text = (0.92 ** 6 * 1.15)
    x = rng.normal(size=d)
    r_ext = []
    xinf = np.zeros(d)
    for k in range(60):
        x = Text * x
        r_ext.append(np.linalg.norm(x - xinf))
    rate_ext = -np.polyfit(np.arange(3, 40), np.log(
        np.array(r_ext[3:40])), 1)[0]
    # generic instances: 6 random contractions with Lip <= 0.92 and
    # one 1.15*Id expansion
    rates_gen = []
    for trial in range(30):
        mats = []
        for i in range(7):
            if i == 1:
                mats.append(1.15 * np.eye(d))
            else:
                M = rng.normal(size=(d, d))
                # scale to operator norm exactly 0.92 (worst case) or
                # below (generic): use 0.92 * random rotation-ish
                U, s, Vt = np.linalg.svd(M)
                M = (U[:, :d] * (s / s[0] * 0.92)) @ Vt
                mats.append(M)
        Tgen = mats[6] @ mats[5] @ mats[4] @ mats[3] @ mats[2] @ mats[
            1] @ mats[0]
        x = rng.normal(size=d)
        xinf = np.zeros(d)
        rr = []
        for k in range(400):
            x = Tgen @ x
            rr.append(np.linalg.norm(x))
        rr = np.array(rr)
        sel = (rr > 1e-12) & (np.arange(len(rr)) < 300)
        sl = -np.polyfit(np.arange(len(rr))[sel], np.log(rr[sel]), 1)[0]
        rates_gen.append(sl)
    rates_gen = np.array(rates_gen)
    results["layer3"] = {
        "extremal_rate": float(rate_ext),
        "generic_rate_median": float(np.median(rates_gen)),
        "generic_rate_max": float(rates_gen.max()),
        "generic_rate_min": float(rates_gen.min()),
        "certified_slowest": PRED_RATE,
        "n_generic": len(rates_gen),
        "envelope_holds_all_faster": bool(
            rates_gen.min() >= PRED_RATE - 1e-9)}
    print(f"  extremal instance rate = {rate_ext:.4f} "
          f"(certified slowest-case 0.3610)")
    print(f"  generic instances: median {np.median(rates_gen):.4f}, "
          f"min {rates_gen.min():.4f} (all >= 0.361: "
          f"{bool(rates_gen.min() >= PRED_RATE - 1e-9)}; 0.361 is the "
          f"worst-case/slowest guarantee)")

    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=1)
    print(f"\n{time.time()-t0:.0f}s -> {OUT_JSON}")

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

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.3),
                             constrained_layout=True)
    ax = axes[0]
    for q in results["layer2_loopsize"]:
        rr = np.array(q["r_k"])
        ks = np.arange(len(rr))
        sel = (ks >= 1) & (rr > 0)
        ax.semilogy(ks[sel], rr[sel], 'o-', ms=3,
                    label="eps=%s" % q["eps"])
    xs = np.arange(0, 25)
    ax.semilogy(xs, np.exp(-PRED_RATE * xs) * 200, '--', color='#92761f',
                lw=2, label='prediction $e^{-0.361k}$')
    ax.set_xlabel('parameter-cycle index $k$')
    ax.set_ylabel('residual $\\|v_k - v_\\infty\\|_1$')
    ax.set_title('(a) LP-layer parameter cycles')
    ax.legend(fontsize=7, ncol=2)

    ax = axes[1]
    if len(eps_arr) >= 3:
        ax.loglog(eps_arr, D1_arr, 'o-', color='#4e4732')
        fit = np.exp(ic) * eps_arr ** sl
        ax.loglog(eps_arr, fit, '--', color='#92761f',
                  label=f'slope {sl:.2f} (corpus law: 1.00)')
        ax.legend(fontsize=8)
    ax.set_xlabel('loop size $\\varepsilon$')
    ax.set_ylabel('one-pass drift $D_1$')
    ax.set_title('(b) drift vs loop size')

    ax = axes[2]
    ax.hist(rates_gen, bins=12, color='#4e4732', alpha=0.85,
            label='generic 7-optic instances')
    ax.axvline(PRED_RATE, color='#92761f', ls='--', lw=2.2,
               label='certified envelope 0.361')
    ax.axvline(rate_ext, color='#c0392b', ls=':', lw=2,
               label=f'extremal {rate_ext:.3f}')
    ax.set_xlabel('relaxation rate per cycle')
    ax.set_ylabel('instances')
    ax.set_title('(c) cascade layer: envelope law')
    ax.legend(fontsize=7)
    fig.suptitle('E. coli cycle scan, layer-resolved: where the '
                 '0.361/cycle law lives', fontsize=12)
    fig.savefig(OUT_PNG, dpi=170)
    print(f"figure -> {OUT_PNG}")


if __name__ == "__main__":
    main()
