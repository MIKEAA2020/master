#!/usr/bin/env python3
"""
Task 7-a: The record-phase p-scan at n=2 (exact) — final version.

Rules established by pscan_diag.py (validated against the dense spectrum):
  lambda_1   = (even sector, 0 minus-branches)          [all p]
  lambda_sig = (odd, 0 minus)  for p < p_c             [Kaufman BC switch]
             = (odd, 1 minus)  for p > p_c             (equal at p_c)
  lambda_eps = (even, 2 minus)                          [all p]
  X_sigma -> 2 pi beta_d/4 = 0.942, X_eps -> 2 pi 2 beta_d = 7.540 at p_c
  ratio -> x_sigma/x_eps = 1/8 exactly.
Production-cell anchors: Lambda(1) finite-L table -0.077984/-0.079362/
-0.079901 at p=0.16 (L=8/12/16) -> thermodynamic -0.081015 (Houtappel).
All Kaufman products computed in log space (no overflow at large L).
"""
import json
import numpy as np

D = 2
PC = (2 - (0.6 + np.sqrt(0.36 + 1.0))) / 1.0     # 0.2338096210...
OUT_JSON = "/home/z/my-project/scripts/pscan_n2_results.json"
OUT_PNG = "/home/z/my-project/download/pscan_record_phase_kinks.png"


def consts(d, p):
    th = d - (d - 1) * p
    a = (d * d * th * th - 1.0) / (d ** 4 - 1)
    b = th / (d * d + 1)
    c = (d * d - th * th) / (d ** 4 - 1)
    Kd = 0.25 * np.log(a / c)
    Kh = 0.25 * np.log(a * c / b ** 2)
    W0 = (a * c * b * b) ** 0.25
    return Kd, Kh, W0


def kaufman_log_lambdas(m, Kd, Kh, W0, p=None):
    """log-space closed-form eigenvalues:
    (ln lam1, ln lam_sig, ln lam_eps) with the Kaufman branch switch.
    p is used only for the branch switch; pass None to keep odd-0."""
    ch = np.cosh(2 * Kd); shd = np.sinh(2 * Kd)
    chh = np.cosh(2 * Kh); shh = np.sinh(2 * Kh)
    K_even = (2 * np.arange(1, m + 1) - 1) * np.pi / m
    K_odd = 2 * np.pi * np.arange(0, m) / m

    def wpair(Ks):
        k = np.asarray(Ks)
        Q = ch ** 2 * chh + shd ** 2 * shh - shh * np.cos(k)
        R = 2 * shd * np.cos(k / 2)
        disc = np.sqrt(np.maximum(Q ** 2 - R ** 2, 0.0))
        return Q + disc, Q - disc          # w^+, w^-

    base = m * np.log(2 * W0 ** 2)
    wpe, wme = wpair(K_even)
    wpo, wmo = wpair(K_odd)
    ln_l1 = base + np.sum(np.log(wpe))
    # sigma: odd sector max with the branch rule
    ln_odd0 = base + np.sum(np.log(wpo))
    r_o = wmo / wpo
    j0 = 0  # k=0 is in K_odd (index 0)
    ln_odd1 = ln_odd0 - np.log(wpo[j0]) + np.log(wmo[j0])
    if p is None or p <= PC:
        ln_sig = ln_odd0
    else:
        ln_sig = ln_odd1
    # epsilon: even sector, best 2-minus product
    r_e = wme / wpe
    jj = np.argsort(r_e)[::-1][:2]
    ln_eps = ln_l1 + np.sum(np.log(r_e[jj]))
    return ln_l1, ln_sig, ln_eps


def build_S(m, Kd, Kh):
    n = 1 << m
    bits = ((np.arange(n)[:, None] >> np.arange(m - 1, -1, -1)[None, :]) & 1)
    s = 1 - 2 * bits
    sc = np.roll(s, -1, axis=1)
    dh = np.exp(Kh * np.sum(s * sc, axis=1))
    E = np.exp(Kd * (s @ s.T + s @ sc.T))
    sq = np.sqrt(dh)
    return sq[:, None] * E * sq[None, :], s


def dense_lambdas(m, Kd, Kh, W0, p):
    """dense SVD check with sector projection + correct branch pick."""
    S, s = build_S(m, Kd, Kh)
    n = S.shape[0]
    flip = np.arange(n) ^ ((1 << m) - 1)
    reps = np.array([i for i in range(n) if i < flip[i]])
    dim = len(reps)
    out = {}
    for parity, name in [(+1, "even"), (-1, "odd")]:
        u = np.zeros((n, dim))
        u[reps, np.arange(dim)] = 1.0
        u[flip[reps], np.arange(dim)] = parity
        u /= np.sqrt(2.0)
        W = u.T @ S @ u
        sv = np.linalg.svd(W, compute_uv=False) ** 2
        out[name] = np.sort(W0 ** (2 * m) * sv)[::-1]
    ln_l1 = np.log(out["even"][0])
    ln_eps = np.log(out["even"][1])
    # dense odd top1 is the physical sigma (branch switch automatic)
    ln_sig = np.log(out["odd"][0])
    return ln_l1, ln_sig, ln_eps


def f_houtappel(K1, K2, K3, ngrid=1024):
    t = 2 * np.pi * (np.arange(ngrid) + 0.5) / ngrid
    c1 = np.cos(t)
    s3t = np.cos(np.add.outer(t, t))
    ch1, ch2, ch3 = np.cosh(2 * K1), np.cosh(2 * K2), np.cosh(2 * K3)
    sh1, sh2, sh3 = np.sinh(2 * K1), np.sinh(2 * K2), np.sinh(2 * K3)
    bracket = (ch1 * ch2 * ch3 + sh1 * sh2 * sh3
               - sh1 * c1[:, None] - sh1 * 0 - sh2 * c1[None, :]
               - sh3 * s3t)
    dt = 2 * np.pi / ngrid
    return np.log(2.0) + (np.log(bracket).sum() * dt * dt) / (8 * np.pi ** 2)


def XL(p, m):
    Kd, Kh, W0 = consts(D, p)[:3]
    ln1, lns, lne = kaufman_log_lambdas(m, Kd, Kh, W0, p=p)
    return 2 * m * (ln1 - lns)


def find_crossing(m1, m2, lo=0.20, hi=0.26):
    f = lambda p: XL(p, m1) - XL(p, m2)
    # grid scan for sign change (bracket safety)
    gs = np.arange(lo, hi, 0.001)
    vals = [f(p) for p in gs]
    for i in range(len(gs) - 1):
        if vals[i] == 0:
            return gs[i]
        if (vals[i] > 0) != (vals[i + 1] > 0):
            a, b = gs[i], gs[i + 1]
            fa = vals[i]
            for _ in range(70):
                mid = 0.5 * (a + b)
                fm = f(mid)
                if (fm > 0) == (fa > 0):
                    a, fa = mid, fm
                else:
                    b = mid
            return 0.5 * (a + b)
    return None


# =====================================================================
if __name__ == "__main__":
    results = {"model": "n=2 exact annealed replica chain (Ising/Houtappel)",
               "d": D, "pc2_closed": PC}

    print("=" * 72)
    print("VALIDATION BLOCK")
    print("=" * 72)
    # 1. dense vs Kaufman (correct rules)
    devs = []
    for m in [2, 3, 4, 5, 6, 8]:
        for p in [0.05, 0.16, 0.20, 0.23, PC, 0.24, 0.30, 0.40, 0.60]:
            Kd, Kh, W0 = consts(D, p)[:3]
            dl = dense_lambdas(m, Kd, Kh, W0, p)
            kl = kaufman_log_lambdas(m, Kd, Kh, W0, p=p)
            devs.append(max(abs(a - b) for a, b in zip(dl, kl)))
    mx = max(devs)
    print(f"[1] dense SVD vs Kaufman (lam1, lam_sig, lam_eps): "
          f"max |d ln lambda| = {mx:.2e}   [target ~1e-12]")

    # 2. benchmark crossings
    bench = {}
    for pair in [(16, 20), (20, 24), (24, 28), (28, 32)]:
        bench[str(pair)] = find_crossing(pair[0] // 2, pair[1] // 2)
    print("[2] crossing ladder (manuscript: 0.23319 0.23348 0.23361 "
          "0.23368, exact 0.233810):")
    for k, v in bench.items():
        print(f"      p*({k}) = {v:.6f}" if v else f"p*({k}) = NOT FOUND")

    # 3. lambda_1(28)^(1/28) at p=0.40
    Kd, Kh, W0 = consts(D, 0.40)[:3]
    ln1, lns, lne = kaufman_log_lambdas(14, Kd, Kh, W0)
    l28 = np.exp(ln1 / 28.0)
    print(f"[3] lambda_1(28)^(1/28) at p=0.40 = {l28:.9f}"
          f"   [manuscript: 0.683844946]")

    # 4. ratio diagnostic at p_c
    ratios = {}
    for L in [16, 20, 24, 28, 32]:
        Kd, Kh, W0 = consts(D, PC)[:3]
        ln1, lns, lne = kaufman_log_lambdas(L // 2, Kd, Kh, W0, p=PC)
        ratios[L] = (ln1 - lns) / (ln1 - lne)
    print("[4] ratio at p_c (manuscript: 0.1220 0.1231 0.1237 0.1240 "
          "0.1243, exact 0.125):",
          " ".join(f"{v:.4f}" for v in ratios.values()))

    # 5. X_L limits at p_c
    xlim = {}
    for L in [64, 256]:
        Kd, Kh, W0 = consts(D, PC)[:3]
        ln1, lns, lne = kaufman_log_lambdas(L // 2, Kd, Kh, W0, p=PC)
        xlim[L] = {"X_sigma": L * (ln1 - lns), "X_eps": L * (ln1 - lne)}
    print("[5] X_L at p_c (targets 0.942 / 7.540):",
          {k: (round(v["X_sigma"], 4), round(v["X_eps"], 4))
           for k, v in xlim.items()})

    # 6. Houtappel quadrature + production cells
    Kd, Kh, W0 = consts(D, 0.40)[:3]
    fH40 = np.log(W0) + f_houtappel(Kd, Kd, Kh, ngrid=2048)
    Kd, Kh, W0 = consts(D, 0.16)[:3]
    fH16 = np.log(W0) + f_houtappel(Kd, Kd, Kh, ngrid=2048)
    Kd, Kh, W0 = consts(D, 0.22)[:3]
    fH22 = np.log(W0) + f_houtappel(Kd, Kd, Kh, ngrid=2048)
    print(f"[6] Houtappel bulk: p=0.40 -> {np.exp(fH40):.9f} "
          f"[target 0.683844659];  Lambda(1): p=0.16 -> {0.5 * fH16:.6f} "
          f"[finite-L trend -0.0780/-0.0794/-0.0799], p=0.22 -> "
          f"{0.5 * fH22:.6f} [trend -0.1064/-0.1083/-0.1091]")

    results["validation"] = {
        "max_dln_lambda_dense_vs_kaufman": mx,
        "benchmark_crossings": bench,
        "lambda1_28_p040": l28,
        "ratio_at_pc": {str(k): v for k, v in ratios.items()},
        "X_L_at_pc": {str(k): v for k, v in xlim.items()},
        "houtappel_bulk_p040": float(np.exp(fH40)),
        "Lambda1_p016_thermo": float(0.5 * fH16),
        "Lambda1_p022_thermo": float(0.5 * fH22),
    }

    # =================================================================
    print()
    print("=" * 72)
    print("THE RECORD-PHASE P-SCAN (n=2)")
    print("=" * 72)
    scan = {}

    # a) crossing ladder, many pairs
    pairs = [(8, 10), (10, 12), (12, 14), (14, 16), (16, 20), (20, 24),
             (24, 28), (28, 32), (32, 40), (40, 48), (48, 64)]
    cross = {}
    for pair in pairs:
        cross[str(pair)] = find_crossing(pair[0] // 2, pair[1] // 2)
    scan["crossing_ladder"] = cross
    print("crossing ladder ->", {k: (round(v, 6) if v else None)
                                 for k, v in cross.items()})
    print(f"   exact p_c^(2) = {PC:.6f}")

    # b) susceptibility ladder (exact Kaufman f_L)
    grid = np.arange(0.20, 0.27, 0.00025)
    chi_data = {}
    for L in [16, 24, 32, 48, 64, 96, 128, 192, 256]:
        m = L // 2
        f = np.array([kaufman_log_lambdas(m, *consts(D, p)[:3], p=p)[0] / L
                      for p in grid])
        chi = np.gradient(np.gradient(f, grid), grid)
        j = int(np.argmax(chi))
        chi_data[L] = {"p_peak": float(grid[j]),
                       "chi_peak": float(chi[j])}
        print(f"   L={L:4d}: chi peak p={grid[j]:.5f}, height "
              f"{chi[j]:.3f}")
    # Onsager ln L growth of the peak
    Ls = np.array(sorted(chi_data.keys()), dtype=float)
    hs = np.array([chi_data[int(L)]["chi_peak"] for L in Ls])
    A, B = np.polyfit(np.log(Ls), hs, 1)
    scan["onsager_chiL_lnL_fit"] = {"slope": float(A), "intercept": float(B)}
    print(f"   chi peak vs ln L: slope {A:.3f} (Onsager log growth)")
    scan["susceptibility"] = {str(k): v for k, v in chi_data.items()}

    # c) inverse-gap signature: the RELATIVE gap (lam1-lam_sig)/lam1 =
    #    1 - exp(-X_sigma/L) closes like X_sigma/L ~ 1/L at the boundary;
    #    the response concentrates onto it (Rayleigh-Schroedinger channel).
    ig = {"relative_gap_at_pc": {}, "peak_offset_vs_L": []}
    for L in [16, 32, 64, 128, 256]:
        m = L // 2
        ln1, lns, lne = kaufman_log_lambdas(m, *consts(D, PC)[:3], p=PC)
        ig["relative_gap_at_pc"][L] = float(1 - np.exp(lns - ln1))
        ig["relative_gap_at_pc"]["X_over_L_%d" % L] = float(
            L * (ln1 - lns) / L)
    # closure law: relgap * L -> X_sigma
    relL = {L: v for L, v in ig["relative_gap_at_pc"].items()
            if isinstance(L, int)}
    for L, v in relL.items():
        print(f"   L={L}: relative gap at p_c = {v:.5f}, "
              f"L*relgap = {L * v:.3f} -> X_sigma = 0.942")
    # concentration rate |p_peak - p_c| ~ c/L
    Ls2 = np.array([L for L in sorted(chi_data) if L >= 24], dtype=float)
    offs = np.array([abs(chi_data[int(L)]["p_peak"] - PC) for L in Ls2])
    sel2 = offs > 0
    cl, cl0 = np.polyfit(1.0 / Ls2[sel2], offs[sel2], 1)
    ig["concentration_rate_c"] = float(cl)
    print(f"   peak offset |p_peak-p_c| ~ {cl:.3f}/L (concentration rate)")
    scan["inverse_gap"] = ig

    # d) thermodynamic kink via Kaufman L=4096 (log-space, exact)
    LT = 4096
    mT = LT // 2
    p_coarse = np.arange(0.01, 0.65, 0.01)
    f_coarse = np.array([kaufman_log_lambdas(mT, *consts(D, p)[:3])[0] / LT
                         for p in p_coarse])
    pf = np.arange(PC - 0.02, PC + 0.02, 2.5e-4)
    f_fine = np.array([kaufman_log_lambdas(mT, *consts(D, p)[:3])[0] / LT
                       for p in pf])
    lam1_fine = 0.5 * f_fine
    chi_f = np.gradient(np.gradient(lam1_fine, pf), pf)
    jp = int(np.argmax(chi_f))
    print(f"   thermodynamic (L={LT}) Lambda(1) chi peak: p={pf[jp]:.5f} "
          f"[exact {PC:.6f}], height {chi_f[jp]:.2f}")
    # Onsager log fit away from the finite-L rounding
    sel = (np.abs(pf - PC) > 3e-3) & (np.abs(pf - PC) < 1.5e-2)
    x = -np.log(np.abs(pf[sel] - PC))
    y = chi_f[sel]
    Ao, Bo = np.polyfit(x, y, 1)
    pred = Ao * x + Bo
    r2 = 1 - np.sum((y - pred) ** 2) / np.sum((y - np.mean(y)) ** 2)
    print(f"   Onsager fit: chi ~ {Bo:.2f} {Ao:+.2f}*(-ln|p-pc|), "
          f"R^2 = {r2:.4f}")
    scan["thermo"] = {
        "p_grid": p_coarse.tolist(), "f_Lambda1": (0.5 * f_coarse).tolist(),
        "kink_peak_p": float(pf[jp]), "kink_peak_chi": float(chi_f[jp]),
        "onsager_fit": {"coef_of_minus_ln": float(Ao),
                        "const": float(Bo), "R2": float(r2)},
        "L_proxy": LT,
    }
    scan["Lambda1_p016"] = float(0.5 * fH16)

    results["scan"] = scan

    # =================================================================
    # FIGURE
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.font_manager as fm
    fm.fontManager.addfont(
        '/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
    fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Noto Sans SC']
    plt.rcParams['axes.unicode_minus'] = False

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.6),
                             constrained_layout=True)

    ax = axes[0, 0]
    pairs_s = [eval(k) for k in cross.keys()]
    xs = [max(p) for p in pairs_s]
    ys = [cross[k] for k in cross.keys() if cross[k]]
    ax.plot(xs[:len(ys)], ys, 'o-', color='#4e4732', ms=5,
            label='crossing $p^*(L_1,L_2)$')
    ax.axhline(PC, color='#92761f', ls='--',
               label='$p_c^{(2)}=0.233810$ (exact)')
    ax.set_xlabel('larger size $L_2$ of the crossing pair')
    ax.set_ylabel('$p^*$')
    ax.set_title('(a) kink-ladder convergence to the record-phase boundary')
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    for L in [16, 32, 64, 128, 256]:
        m = L // 2
        f = np.array([kaufman_log_lambdas(m, *consts(D, p)[:3])[0] / L
                      for p in grid])
        chi = np.gradient(np.gradient(f, grid), grid)
        ax.semilogy(grid, np.maximum(chi, 1e-6), label=f'$L={L}$')
    ax.axvline(PC, color='#92761f', ls='--')
    ax.set_xlabel('monitoring rate $p$')
    ax.set_ylabel('$\\chi_L = \\partial^2 f_L / \\partial p^2$')
    ax.set_title('(b) finite-$L$ response concentration (Onsager growth)')
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    ax.plot(pf, lam1_fine, color='#4e4732', lw=1.5)
    ax.axvline(PC, color='#92761f', ls='--')
    ax.set_xlabel('monitoring rate $p$')
    ax.set_ylabel('$\\Lambda^{(1)}(p)$ per site (nats)')
    ax.set_title('(c) record SCGF $\\beta{=}1$ endpoint — kink potential '
                 f'($L={LT}$ exact)')
    axin = ax.inset_axes([0.42, 0.12, 0.55, 0.55])
    axin.plot(pf, chi_f, color='#92761f')
    axin.axvline(PC, color='#4e4732', ls='--')
    axin.set_title('$\\partial^2 \\Lambda^{(1)}/\\partial p^2$ (Onsager)',
                   fontsize=8)

    ax = axes[1, 1]
    for L, col in [(64, '#4e4732'), (32, '#92761f')]:
        m = L // 2
        l1s = np.array([kaufman_log_lambdas(m, *consts(D, p)[:3], p=p)[0]
                        for p in grid])
        sigs = np.array([kaufman_log_lambdas(m, *consts(D, p)[:3], p=p)[1]
                         for p in grid])
        ax.plot(grid, L * (l1s - sigs), color=col, lw=1.5,
                label=f'$X_L$, $L={L}$')
    ax.axvline(PC, color='gray', ls=':')
    ax.set_xlabel('monitoring rate $p$')
    ax.set_ylabel('scaled gap $X_L(p)$')
    ax.set_title('(d) the crossing diagnostic $X_L$ (kink locator)')
    ax.legend(fontsize=8)

    fig.suptitle('Record-phase p-scan, $n=2$ replica chain ($d=2$): exact '
                 'kink localization at $p_c^{(2)} = 0.233810$',
                 fontsize=12)
    fig.savefig(OUT_PNG, dpi=170)
    print(f"\nfigure -> {OUT_PNG}")

    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=1)
    print(f"results -> {OUT_JSON}")
