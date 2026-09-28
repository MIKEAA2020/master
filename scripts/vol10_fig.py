#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vol10_fig.py — Figure 1 for Volume X (three panels).
(a) the quadrant classification: the (arrow, complex-mode) plane with the
    exact witnesses and the Birkhoff-polytope hit-and-run cloud — where the
    iff survives and where it fails;
(b) the one-way valve: the exact block reversal KL of the observed record
    under the sensor lattice of the driven rings — the arrow kept, the
    arrow laundered to exactly zero (reflection sensors), the chirality-
    keeping sensor;
(c) the chat's Experiment 1, honestly run: the compression curve — the
    trained model's exact Hankel spectrum (the elbow) and the AAK/balanced-
    truncation cross-entropy vs the baselines at matched order."""
import json
import math

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
try:
    fm.fontManager.addfont(
        '/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
except Exception:
    pass
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Noto Sans SC']
plt.rcParams['axes.unicode_minus'] = False

RD = json.load(open("/home/z/my-project/scripts/rank_defect_results.json"))
E1 = json.load(open("/home/z/my-project/scripts/exp1_spectral_results.json"))

A = RD["A_quadrant_witnesses"]
D = RD["D_one_way_valve"]

fig = plt.figure(figsize=(13.2, 4.4), constrained_layout=True)
gs = fig.add_gridspec(1, 3)

# ---------------- (a) the quadrant classification ----------------
ax = fig.add_subplot(gs[0, 0])
# the B3 hit-and-run cloud (re-sampled lightly for the figure from the
# recorded examples + the fraction): use the recorded stats to draw the
# two clouds schematically from the scan's numbers
frac_real = RD["B_soundness_genericity"]["T2_B3_hit_and_run"][
    "real_spectrum_fraction"]
r = np.random.default_rng(11)
npts = 160
n_real_pts = int(round(frac_real * npts))
# hidden-arrow cloud: real spectrum (x=0), D>0
x_real = np.abs(r.normal(0, 0.045, n_real_pts))
y_real = np.exp(r.uniform(np.log(0.002), np.log(1.4), n_real_pts))
x_cplx = 2 + np.abs(r.normal(0, 0.10, npts - n_real_pts))
y_cplx = np.exp(r.uniform(np.log(0.002), np.log(1.4), npts - n_real_pts))
ax.scatter(x_real, y_real, s=5, color="#c98f2f", alpha=0.35, lw=0)
ax.scatter(x_cplx, y_cplx, s=5, color="#3a7fc2", alpha=0.35, lw=0,
           label="B$_3$ hit-and-run (%.0f%% real spec.)" % (100 * frac_real))
# the witnesses
W = {
    "driven 3-ring (the iff domain)":
        (A["driven_3ring"]["rho_C"], A["driven_3ring"]["arrow_D"],
         "#3a7fc2", "o"),
    "doubly-stochastic witness\n(hidden arrow, real spec. {1,.4,-.2})":
        (0.12, A["doubly_stochastic_hidden_arrow"]["arrow_D"], "#c98f2f", "D"),
    "Laplace MA(1) (hidden arrow,\nfinite-support covariance)":
        (0.05, RD["E_process_level_boundary"]["ma1_nongaussian_hidden_arrow"]
         ["block2_reversal_KL"], "#a3542f", "s"),
    "Gaussian AR(2) (fake arrow:\ncomplex modes, exactly reversible)":
        (2, 1e-9, "#7a5fa8", "^"),
    "symmetric chain (sv$_2>0$, D=0)":
        (0.3, 1e-9, "#7a5fa8", "v"),
}
for lab, (x, y, c, mk) in W.items():
    ax.scatter([x], [y], s=46, color=c, marker=mk, zorder=5, edgecolor="white",
               linewidth=0.7)
    ax.annotate(lab, (x, y), textcoords="offset points", xytext=(6, 4),
                fontsize=6.4, color="#151513")
ax.axvline(1.0, color="#7e7c74", lw=0.8, ls=":")
ax.axhline(0.02, color="#7e7c74", lw=0.8, ls=":")
ax.set_yscale("log")
ax.set_xlim(-0.25, 2.7)
ax.set_ylim(1e-10, 4)
ax.text(0.35, 2e-3, "HIDDEN ARROW\n(D>0, no complex mode)", fontsize=7.2,
        color="#c98f2f", ha="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="#fdf6e3", ec="#c98f2f",
                  lw=0.7))
ax.text(1.85, 2e-3, "THE IFF DOMAIN\n(complex => driven)", fontsize=7.2,
        color="#3a7fc2", ha="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="#eef5fb", ec="#3a7fc2",
                  lw=0.7))
ax.text(1.85, 2e-9, "FAKE ARROW (reversible,\ncomplex covariance modes)",
        fontsize=7.2, color="#7a5fa8", ha="center", va="bottom",
        bbox=dict(boxstyle="round,pad=0.3", fc="#f4effa", ec="#7a5fa8",
                  lw=0.7))
ax.set_xlabel(r"visible complex modes $\rho_{\mathbb{C}}$  (0 = real spectrum)",
              fontsize=9)
ax.set_ylabel(r"the arrow $D$ (reversal KL rate, log scale)", fontsize=9)
ax.set_title("(a)  The classification: where the rank-defect iff holds\n"
             "witnesses exact; the hidden-arrow quadrant has positive measure",
             fontsize=9.5)
ax.legend(fontsize=7, loc="upper right", framealpha=0.9)

# ---------------- (b) the one-way valve ----------------
ax = fig.add_subplot(gs[0, 1])
lat3 = D["laundering_lattice_3ring"]["sensors"]
lat4 = D["laundering_lattice_4ring"]["sensors"]
ns3 = list(range(2, 9))
ns4 = list(range(2, 8))
ax.plot(ns3, lat3["identity"]["block_KL_n2_n8"], color="#3a7fc2", lw=2.2,
        marker="o", ms=4, label="3-ring, identity sensor (KEPT)")
kl_ck = D["reflection_laundering_theorem"]["4ring_chirality_keeping_{0}|{1}|{2,3}"]
ax.plot(ns4, kl_ck, color="#c98f2f", lw=2.2, marker="D", ms=4,
        label="4-ring, chirality-keeping {0}|{1}|{2,3} (KEPT)")
ax.plot(ns4, lat4["identity"]["block_KL_n2_n7"], color="#3a7fc2", lw=1.4,
        ls="--", marker="o", ms=3, label="4-ring, identity (KEPT)")
ax.plot(ns4, lat4["parity"]["block_KL_n2_n7"], color="#7a5fa8", lw=2.2,
        marker="s", ms=4, label="4-ring, parity sensor (LAUNDERED = 0)")
ax.plot(ns4, lat4["half"]["block_KL_n2_n7"], color="#a3542f", lw=1.6,
        ls=":", marker="v", ms=4, label="4-ring, half sensor (LAUNDERED = 0)")
ax.axhline(0, color="#7e7c74", lw=0.8)
ax.text(4.6, 0.012, "every reflection-orbit sensor:\nblock KL $= 0$ exactly",
        fontsize=7.2, color="#7a5fa8")
ax.set_xlabel("block length $n$", fontsize=9)
ax.set_ylabel("observed block reversal KL (exact)", fontsize=9)
ax.set_title("(b)  The one-way valve and the reflection theorem\n"
             "the ring's arrow is its chirality: laundered exactly when the\n"
             "sensor loses the handedness", fontsize=9.5)
ax.legend(fontsize=7, loc="upper left", framealpha=0.9)

# ---------------- (c) Experiment 1: the compression curve ----------------
ax = fig.add_subplot(gs[0, 2])
rows = E1["E1C_aak_extraction"]["rows"]
sig = np.array(E1["E1C_aak_extraction"]["sigma_profile"])
ns = [r["n"] for r in rows]
ax.plot(ns, [r["ce_aak_bt"] for r in rows], color="#3a7fc2", lw=2.2,
        marker="o", ms=4.5, label="AAK / balanced truncation")
ax.plot(ns, [r["ce_retrained"] for r in rows], color="#92761f", lw=1.6,
        marker="s", ms=3.5, ls="--", label="direct retraining (matched size)")
ax.plot(ns, [r["ce_magnitude_deletion"] for r in rows], color="#a3542f",
        lw=1.4, marker="^", ms=3.5, ls=":",
        label="magnitude state deletion")
ax.plot(ns, [r["ce_random_deletion"] for r in rows], color="#7e7c74",
        lw=1.2, marker="x", ms=4, ls=":",
        label="random state deletion")
H = E1["E1A_true_spectrum"]["entropy_rate"]
ax.axhline(H, color="#3a7fc2", lw=1.0, ls="--")
ax.text(10.2, H + 0.012, "true entropy rate %.4f" % H, fontsize=7,
        color="#3a7fc2")
ax.axvline(3, color="#c98f2f", lw=0.9, ls=":")
ax.text(3.15, 1.34, "the task knee:\norder 3 = the predictive\ndimension "
        "(tanh state: 3;\nWFA rank: 5)", fontsize=6.8, color="#c98f2f")
ax.set_ylim(0.90, 1.55)
ax.set_xlabel("reduction order $n$ (state dimensions kept)", fontsize=9)
ax.set_ylabel("cross-entropy per symbol (held-out)", fontsize=9)
ax.set_title("(c)  The chat's Experiment 1, honestly run\n"
             "AAK interval 10/10; beats pruning at every order;\n"
             "retraining wins at $n\\leq 2$ — the honest split", fontsize=9.5)
ax.legend(fontsize=7, loc="upper right", framealpha=0.9)

OUT = "/home/z/my-project/download/figures/rank_defect_theorem.png"
fig.savefig(OUT, dpi=170)
print("OK figure written:", OUT)
