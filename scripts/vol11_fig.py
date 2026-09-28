#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vol11_fig.py — Figure 1 for Volume XI (three panels).
(a) the arrow-preserving sensor lattice on a manufactured non-circulant
    self-converse witness: the rho-invariant sensors launder exactly
    (machine zero), the rho-breaking sensors keep the arrow — the
    reflection-laundering theorem beyond the ring;
(b) the binary block structure: the resolution floor of the binary arrow
    (n = 2 telescoping identity, n = 3 run-counting identity, first arrow
    at n = 4 on 2+2 lumps; 3-state binary lumps reversible at every
    length);
(c) the shadow sandwich on the ab/ba cell: the EYM floor 1, the abelian
    optimum 1.2771427 carried by the parity-odd mirrored pair, the free
    scans clustered above it — the escape room is empty."""
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

RG = json.load(open("/home/z/my-project/github_repos/master/scripts/"
                    "reversal_group_results.json"))
FC = json.load(open("/home/z/my-project/github_repos/master/scripts/"
                    "free_cell_results.json"))

fig = plt.figure(figsize=(10.5, 3.9), constrained_layout=True)
gs = fig.add_gridspec(1, 3)

# ---------------- (a) the sensor lattice on the self-converse witness ----
ax = fig.add_subplot(gs[0, 0])
row = RG["B_normal_form_laundering"]["laundering_theorem_beyond_ring"][
    "rows"][0]
sensors = row["sensors"]
inv = sorted([(k, v) for k, v in sensors.items() if v["rho_invariant"]],
             key=lambda kv: -max(kv[1]["block_KL_n2_n6"]))
brk = sorted([(k, v) for k, v in sensors.items() if not v["rho_invariant"]],
             key=lambda kv: max(kv[1]["block_KL_n2_n6"]))
vals = ([max(1e-19, max(v["block_KL_n2_n6"])) for _, v in inv]
        + [max(1e-19, max(v["block_KL_n2_n6"])) for _, v in brk])
cols = (["#3a7fc2"] * len(inv) + ["#c98f2f"] * len(brk))
ax.bar(range(len(vals)), vals, color=cols, width=0.72, edgecolor="none")
ax.set_yscale("log")
ax.set_ylim(1e-19, 3e-3)
ax.set_xlabel("sensors of the N=4 self-converse witness (partitions)",
              fontsize=13)
ax.set_ylabel("observed block reversal KL (max, $n$=2..6)", fontsize=13)
ax.set_title("(a) The arrow-preserving sensor lattice\n"
             "off the circulant class", fontsize=15)
ax.axvline(len(inv) - 0.5, color="#7e7c74", lw=0.9, ls="--")
ax.annotate("rho-invariant:\nKL = 0 exactly", (0.4, 1e-13), fontsize=12.5,
            color="#3a7fc2")
ax.annotate("rho-breaking:\nthe arrow survives", (len(inv) + 0.6, 1e-13),
            fontsize=12.5, color="#c98f2f")
ax.tick_params(labelsize=12)
ax.set_xticks([])

# ---------------- (b) the binary block structure -------------------------
ax = fig.add_subplot(gs[0, 1])
bs = RG["D_laundering_routes_deceptive"]["binary_block_structure"]
per_n = bs["boundary_2plus2"]["example_per_n_KL_n2_n6"]
ns = list(range(2, 2 + len(per_n)))
ax.plot(ns, [max(1e-19, v) for v in per_n], "o-", color="#c98f2f", lw=2,
        ms=7, label="random 2+2 lump (rank 4)")
ax.plot(ns, [1e-19] * len(ns), "s-", color="#3a7fc2", lw=1.6, ms=5,
        label="any 3-state binary lump")
ax.set_yscale("log")
ax.set_ylim(1e-19, 1e-1)
ax.set_xlabel("block length $n$", fontsize=13)
ax.set_ylabel("binary block reversal KL", fontsize=13)
ax.set_title("(b) The binary resolution floor\n"
             "of the arrow of time", fontsize=15)
ax.annotate("$n$=2: telescoping identity", (2.05, 2e-17), fontsize=12.5,
            color="#7e7c74")
ax.annotate("$n$=3: run-counting identity", (3.0, 5e-17), fontsize=12.5,
            color="#7e7c74")
ax.annotate("first binary arrow:\nthe 4-block", (4.15, 1.2e-4), fontsize=12.5,
            color="#c98f2f")
ax.legend(fontsize=11.8, loc="lower right", frameon=False)
ax.tick_params(labelsize=12)

# ---------------- (c) the shadow sandwich on the cell --------------------
ax = fig.add_subplot(gs[0, 2])
B = FC["B_free_scan"]
C = FC["C_anatomy_certificates"]
an = C["abelian_optimizer_anatomy"]
po = C["reduced_parity_odd_family"]["params_p_x_y"]
items = [
    ("EYM floor $\\sigma_3$", 1.0, "#7e7c74", "floor"),
    ("parity-odd pair (3 par.)", C["reduced_parity_odd_family"]["best"],
     "#a3542f", "opt"),
    ("abelian two-atom", C["abelian_optimizer_anatomy"]["value"],
     "#c98f2f", "opt"),
    ("free: diagonal WFA", B["abelian_diagonal_subscan"]["best"],
     "#3a7fc2", "scan"),
    ("free: symmetric WFA", B["symmetric_subscan"]["best"], "#3a7fc2",
     "scan"),
    ("free: full 12-par. WFA", B["full_scan"]["best"], "#3a7fc2", "scan"),
    ("escape scan (min)", min(r["best_with_atom1_near_sphere"]
                              for r in C["escape_scan"]["rows"]),
     "#7a5fa8", "scan"),
]
ypos = np.arange(len(items))[::-1]
for (lab, v, c, kind), y in zip(items, ypos):
    ax.barh(y, v - 0.96, left=0.96, color=c, height=0.62, alpha=0.92,
            edgecolor="none")
    ax.text(0.965, y, lab, ha="right", va="center", fontsize=12, color=c)
    ax.text(v + 0.004, y, "%.4f" % v, ha="left", va="center", fontsize=11.8,
            color="#151513")
ax.set_yticks([])
ax.set_xlim(0.96, 1.315)
ax.set_xlabel("distance to the rank-2 class (operator norm)", fontsize=13)
ax.set_title("(c) The shadow sandwich on the ab/ba cell\n"
             "the escape room is empty", fontsize=15)
ax.axvline(1.0, color="#151513", lw=1.1)
ax.text(1.001, len(items) - 0.35, "floor attained? NO — the rank wall",
        fontsize=12, color="#151513")
ax.tick_params(labelsize=12)
ax.annotate("atoms: $(x,y)$, $(-x,y)$, weights $p,-p$\n"
            "the approximant lives on the $\\gamma_1$-odd shell",
            (1.30, 1.1), fontsize=11.8, color="#a3542f", ha="right")
ax.annotate("non-commutative perturbations\nnever improve (60/60)",
            (1.30, 0.1), fontsize=11.8, color="#3a7fc2", ha="right")

fig.suptitle("The reversal group, the binary floor, and the abelian shadow",
             fontsize=16.5, y=1.06)
out = ("/home/z/my-project/github_repos/master/download/figures/"
       "reversal_shadow.png")
fig.savefig(out, dpi=200, facecolor="white")
print("saved:", out)
