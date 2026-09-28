    print("E3: sensor efficiency scan (the wall at eps = 1/2)")
    E3 = {"eps": [], "mean_checks": [], "di_pred": [], "mean_reward": []}
    for eff in (0.55, 0.60, 0.65, 0.70, 0.80, 0.90, 0.95, 1.0):
        envs = [RockSample(4, 4, mp, eff) for mp in MAPS44[:10]]
        counter = [0]
        r = evaluate(envs, di_policy, 10, di_counter=counter)
        n_eps = r["n"]
        checks_per_ep = counter[0] / n_eps if n_eps else 0.0
        # theory: mean drift at d=1 (the typical first check distance)
        theta = 2 * eff - 1
        if theta >= 1.0 - 1e-12:
            mu1 = 40.0
            di_pred = (2 * BAND) / 40.0
        elif theta <= 1e-12:
            mu1 = 0.0
            di_pred = float("inf")
        else:
            mu1 = math.log((1 + theta) / (1 - theta))
            di_pred = (2 * BAND) / mu1
        E3["eps"].append(eff)
        E3["mean_checks"].append(float(checks_per_ep))
        E3["di_pred"].append(float(min(di_pred, 1e6)))
        E3["mean_reward"].append(r["mean"])
        print(f"  eps={eff:.2f}: checks/ep {checks_per_ep:5.2f} | DI theory {min(di_pred,1e6):7.2f} "
              f"| reward {r['mean']:6.2f}")

    # the pole: checks ~ c/(eps - 1/2): log-log slope -1
    ee = np.array(E3["eps"]) - 0.5
    dd = np.array([min(c, 1e6) for c in E3["mean_checks"]])
    mm = np.array(E3["di_pred"])
    mask = (ee > 0.01) & (dd > 0)
    slope_checks = np.polyfit(np.log(ee[mask]), np.log(dd[mask]), 1)[0]
    slope_pred = np.polyfit(np.log(ee[mask]), np.log(mm[mask]), 1)[0]
    E3["pole_fits"] = {"measured_checks_slope": float(slope_checks),
                       "theory_DI_slope": float(slope_pred)}
    print("  pole fit: measured slope %.3f vs theory %.3f (both -> -1: first-order wall)"
          % (slope_checks, slope_pred))

    # =====================================================================
    # Figure
    # =====================================================================
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.font_manager as fm
    fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.3), constrained_layout=True)

    ax = axes[0]
    bs = [100, 300, 800]
    van = [E1[f"vanilla_POMCP_random_{b}"]["mean"] for b in bs]
    van_ci = [E1[f"vanilla_POMCP_random_{b}"]["ci95"] for b in bs]
    ax.errorbar(bs, van, yerr=van_ci, fmt="o-", color="#94a3b8", lw=2,
                label="vanilla POMCP (random rollout)")
    ax.errorbar([300], [E1["DIrollout_POMCP_300"]["mean"]],
                yerr=[E1["DIrollout_POMCP_300"]["ci95"]], fmt="s--", color="#f59e0b",
                lw=1.8, label="POMCP with DI rollouts")
    ax.axhline(E1["DI_fixed_policy_nosearch"]["mean"], color="#2563eb", ls=":", lw=1.8,
               label="the DI program (belief-only, no search)")
    ax.axhline(E1["oracle_clairvoyant_bound"]["mean"], color="#111827", ls="--", lw=1.2,
               label="clairvoyant bound (perfect information)")
    ax.set_xscale("log")
    ax.set_xlabel("POMCP simulations per decision")
    ax.set_ylabel("mean discounted reward")
    ax.set_title("(a) E1: matched-budget comparison\nRockSample[4,4], eps = 0.9", fontsize=11)
    ax.legend(fontsize=7.4, loc="center right", framealpha=0.9)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1]
    qs = E2["widths"]
    ax.errorbar(qs, E2["means"], yerr=E2["cis"], fmt="o-", color="#0891b2", lw=2,
                label="compressed program (quantized beliefs)")
    ax.axhline(base, color="#111827", ls="--", lw=1.2, label="exact-posterior program")
    ax.annotate("q=3: belief reset\n(structural break)", xy=(3, 3.4), xytext=(5.2, 5.0),
                fontsize=8, color="#dc2626",
                arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.2))
    ax.set_xlabel("interface width q (log-odds levels; 0 = exact)")
    ax.set_ylabel("mean discounted reward")
    ax.set_title("(b) E2: the compression scan\nvalue vs belief-compression width", fontsize=11)
    ax.legend(fontsize=8, loc="lower right", framealpha=0.9)
    ax.grid(alpha=0.3)

    ax = axes[2]
    ee = np.array(E3["eps"]) - 0.5
    ax.loglog(ee, E3["mean_checks"], "o-", color="#dc2626", lw=2,
              label="measured checks per episode")
    ax.loglog(ee, E3["di_pred"], "--", color="#6b7280", lw=1.6,
              label="DI theory 2b/mu")
    ax.set_xlabel("eps - 1/2 (sensor informativeness)")
    ax.set_ylabel("checks to determine")
    ax.set_title("(c) E3: the sensor wall\nchecks vs informativeness", fontsize=11)
    ax.legend(fontsize=8, loc="upper left", framealpha=0.9)
    ax.grid(alpha=0.3, which="both")

    fig.suptitle("Risk 3 confronted on RockSample: the theory's instruments (compression, determination "
                 "index, wall) vs the named POMDP baseline", fontsize=12.5)
    fig.savefig(OUT_PNG, dpi=200)
    print("figure ->", OUT_PNG)

    with open(OUT_JSON, "w") as f:
        json.dump({"E1": E1, "E2": E2, "E3": E3}, f, indent=1)
    print("json ->", OUT_JSON)


if __name__ == "__main__":
    main()
