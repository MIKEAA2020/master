#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bt1a_analytic_fig.py — the figure for Volume VII: three panels.
(a) the transport sandwich on the exact class: sigma_{M+1} vs the measured
    multiletter structured distance (transported Prony approximants), with
    the golden-ratio witness;
(b) the register: the graded Fliess ladder + the PR rank floors (the
    commutativity witness's cut-web);
(c) the boundary: on-class sandwich gaps vs off-class measured gaps —
    the honest open boundary (Open 7.13)."""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
    try:
        fm.fontManager.addfont(f)
    except Exception:
        pass
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

R = json.load(open("/home/z/my-project/scripts/bt1a_analytic_results.json"))
V = R["verdicts"]

fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.3), constrained_layout=True)
INK = "#1c2733"; ACC = "#8a1f2d"; GO = "#b07818"; GR = "#3a6b5a"

# ---------------- (a) the sandwich on the exact class ----------------
ax = axes[0]
sw = V["A2_transport_sandwich"]["sandwich"]
Ms = [s["M"] for s in sw]
sig = [s["sigma_{M+1}"] for s in sw]
err = [s["err_ML(measured)"] for s in sw]
gap = [s["sandwich_gap_ML"] for s in sw]
ax.plot(Ms, sig, "o-", color=ACC, lw=1.8, ms=6, label=r"$\sigma_{M+1}(H)$ (EYM floor)")
ax.plot(Ms, err, "s--", color=INK, lw=1.4, ms=6,
        label=r"$\|H - V\Gamma_M V^*\|_{\rm op}$ (transported)")
for m, s, e, g in zip(Ms, sig, err, gap):
    ax.annotate(f"gap {g:.1e}", (m, (s + e) / 2 + 0.004), fontsize=7.2,
                ha="center", color="#5a5a5a")
gw = V["A2_transport_sandwich"]["golden_ratio_witness"]
ax.set_title("(a) The sandwich on the exact class $\\mathcal{V}$\n"
             "equality $D_{\\rm Hankstr}(M)=\\sigma_{M+1}$ for all $M$; "
             "transport machine-exact;\n"
             f"golden witness $\\psi=(1,1)$: optimum "
             f"{gw['prony_optimum']:.12f} = $\\sigma_2$ = "
             f"{gw['sigma_2']:.12f} (err {gw['match_err']:.0e})",
             fontsize=8.6, color=INK)
ax.set_xlabel("rank budget $M$", fontsize=9)
ax.set_ylabel("operator norm", fontsize=9)
ax.legend(fontsize=7.8, loc="upper right")
ax.tick_params(labelsize=8)
ax.grid(alpha=0.25, lw=0.5)

# ---------------- (b) the register ladder + the cut web ---------------
ax = axes[1]
gf = V["GF_graded_fliess"]["cases"]
for c in gf[:5]:
    ax.step(range(len(c["ladder"])), c["ladder"], where="post",
            lw=1.5, alpha=0.85,
            label=f"dim {c['machine_dim']}: r(b), floor {c['global_rank']}")
cw = V["PR_partial_realization"]["commutativity_witness"]["cut_web_analysis"]
ax.axhline(cw["rank"], color=ACC, ls=":", lw=1.6)
ax.annotate("PR witness: rank(M) = 2 = m*\n(dim 1 killed by the\n"
            "commutativity obstruction\n$h(ab)=h(ba)$ forced)",
            (0.35, cw["rank"] + 0.13), fontsize=7.6, color=ACC)
ax.set_title("(b) The graded Fliess ladder\nmonotone budget-graded ranks "
             "$r(b)$; attainment at\n$b\\geq m-1$ (spanning words); the "
             "register = the span\nof the Nerode classes (Fliess, graded)",
             fontsize=8.6, color=INK)
ax.set_xlabel("budget $b$ (word-length cost)", fontsize=9)
ax.set_ylabel("rank $r(b)$", fontsize=9)
ax.legend(fontsize=7.2, loc="lower right")
ax.tick_params(labelsize=8)
ax.grid(alpha=0.25, lw=0.5)

# ---------------- (c) the honest boundary -----------------------------
ax = axes[2]
off = V["I_off_class_boundary"]["instances"]
Ms_off = [off[i]["M"] + 0.06 * i for i in range(len(off))]
gaps_off = [off[i]["measured_gap"] for i in range(len(off))]
sig_off = [off[i]["sigma_{M+1}"] for i in range(len(off))]
ub_off = [off[i]["alternating_upper_bound"] for i in range(len(off))]
on_gaps = [s["sandwich_gap_ML"] for s in sw]
ax.bar(np.arange(len(on_gaps)) - 0.18, on_gaps, width=0.34,
       color=GR, alpha=0.9, label="ON class $\\mathcal{V}$: sandwich gap "
       "(optimizer artifact, $\\to$ 0 at the golden case)")
ax.bar(np.arange(len(gaps_off)) + 0.2 + 0.2, gaps_off, width=0.34,
       color=ACC, alpha=0.85, label="OFF class: measured structured gap "
       "(only $\\sigma\\leq D$ provable — Open 7.13)")
ax.set_yscale("log")
ax.set_title("(c) The boundary, honestly measured\non the exact class the "
             "equality is proved and machine-checked;\noff it, no equality "
             "is available — the recorded open\nboundary (Lacroce's "
             "constructive nc-AAK)",
             fontsize=8.6, color=INK)
ax.set_xlabel("instance (rank budgets $M$)", fontsize=9)
ax.set_ylabel("gap to $\\sigma_{M+1}$ (log scale)", fontsize=9)
ax.legend(fontsize=7.2, loc="upper left")
ax.tick_params(labelsize=8)
ax.grid(alpha=0.25, lw=0.5, axis="y")

fig.savefig("/home/z/my-project/download/figures/bt1a_analytic.png",
            dpi=200)
print("figure written")
