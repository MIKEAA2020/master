#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sandwich_locus_fig.py — Figure 1 for Volume IX (three panels).
(a) the amalgam closed form: the triple equioscillation across the family;
(b) the sandwich-locus map: the measured gap valley over the first-shell plane;
(c) the calibrated sandwich: floors vs best-attained, witness by witness."""
import json
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
try:
    fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
except Exception:
    pass
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Noto Sans SC']
plt.rcParams['axes.unicode_minus'] = False

RES = json.load(open("/home/z/my-project/scripts/sandwich_locus_results.json"))
V = RES["verdicts"]
A = V["A_amalgam_closed_form"]
B = V["B_lens_criterion"]
C = V["C_locus_map"]
D = V["D_cell_M2"]

fig = plt.figure(figsize=(13.2, 4.4), constrained_layout=True)
gs = fig.add_gridspec(1, 3)

# ---------------- (a) the amalgam closed form ----------------
ax = fig.add_subplot(gs[0, 0])
c0s = np.linspace(0.25, 3.0, 40)
s2s, s1s = [], []
for c0 in c0s:
    ca, cb = 0.8, 0.6
    C2 = ca * ca + cb * cb
    G_ = math.sqrt(c0 * c0 + 4 * C2)
    s1 = (c0 + G_) / 2
    s2s.append((G_ - c0) / 2)
    s1s.append(s1)
s2s = np.array(s2s)
ax.plot(c0s, s2s, color="#3aa0c2", lw=2.2, label=r"$+\sigma_2$ (the block)")
ax.plot(c0s, -s2s, color="#92761f", lw=2.2, ls="--",
        label=r"$-\sigma_2$ ($\hat u_2$ and the block)")
ax.fill_between(c0s, -s2s, s2s, color="#3aa0c2", alpha=0.06)
ax.axhline(0, color="#7e7c74", lw=0.8)
# the identities annotation
ax.text(0.32, 0.62, r"$\rho^*=\sigma_2/\sigma_1$" + "\n" +
        r"$\|v^*\|^2=\sigma_1/c_0$" + "\n" +
        r"$\|t^*\|^2=\sigma_2^2/(c_0\sigma_1)$" + "\n" +
        r"spectrum $(\sigma_2,-\sigma_2,-\sigma_2)$",
        fontsize=8.5, color="#151513",
        bbox=dict(boxstyle="round,pad=0.4", fc="#ebeae8", ec="#c5bfac", lw=0.8))
ax.set_xlabel(r"the corner coefficient $c_0$  (axes fixed at $c_a=0.8,\ c_b=0.6$)",
              fontsize=9)
ax.set_ylabel("error eigenvalues", fontsize=9)
ax.set_title("(a)  The amalgam closed form:\ntriple equioscillation, identical across the family",
             fontsize=10)
ax.legend(fontsize=8, loc="lower right", framealpha=0.9)
ax.tick_params(labelsize=8)

# ---------------- (b) the locus map ----------------
ax = fig.add_subplot(gs[0, 1])
grid = C["grid"]
c0v = sorted(set(g["c0"] for g in grid))
cabv = sorted(set(g["cab"] for g in grid))
Z = np.full((len(cabv), len(c0v)), np.nan)
for g in grid:
    i = cabv.index(g["cab"])
    j = c0v.index(g["c0"])
    Z[i, j] = g["gap"] if g["gap"] is not None else 0.0
X, Y = np.meshgrid(c0v, cabv)
pcm = ax.pcolormesh(X, Y, Z, cmap="viridis_r",
                    norm=matplotlib.colors.LogNorm(vmin=1e-6, vmax=max(2.3e-1, np.nanmax(Z))),
                    shading="nearest")
# the closed slice: cab = 0 line
ax.axhline(0.0, color="#e05b5b", lw=2.4, label="the amalgam slice (CLOSED, gap 4e-16)")
cb = fig.colorbar(pcm, ax=ax, pad=0.02)
cb.set_label(r"measured gap $D(1)-\sigma_2$ (log scale)", fontsize=8)
cb.ax.tick_params(labelsize=7)
ax.set_xlabel(r"$c_0$", fontsize=9)
ax.set_ylabel(r"$c_{ab}$ (the corner coupling)", fontsize=9)
ax.set_title("(b)  The sandwich locus at $M=1$:\nthe gap valley over the first-shell plane",
             fontsize=10)
ax.legend(fontsize=7.5, loc="upper right", framealpha=0.9)
ax.tick_params(labelsize=8)

# ---------------- (c) the calibrated sandwich ----------------
ax = fig.add_subplot(gs[0, 2])
items = [
    ("golden amalgam\n$M{=}1$ (retracted 1.0369)", 1.0, 1.0, True),
    ("2-atom targets\n$M{=}1$ (30/30)", 1.0, 1.0, True),
    ("affine targets\n$M{=}1$ (8/8)", 1.0, 1.0, True),
    ("first-shell valley\n$M{=}1$ (284 open)", 1.0, 1.23, False),
    ("the $(1,1)$ cell\n$M{=}2$ (rank wall)", 1.0, 1.2771, False),
]
ypos = np.arange(len(items))[::-1]
for y, (name, floor, top, closed) in zip(ypos, items):
    if closed:
        ax.plot([floor], [y], marker="o", color="#2e7d32", ms=9, zorder=5)
        ax.text(floor + 0.012, y, "  CLOSED (gap $\\leq$ 1e-9, exact norm)",
                va="center", fontsize=7.6, color="#2e7d32")
    else:
        ax.plot([floor, top], [y, y], color="#92761f", lw=6, alpha=0.55,
                solid_capstyle="butt")
        ax.plot([floor], [y], marker="|", color="#151513", ms=14, mew=1.6)
        ax.plot([top], [y], marker="|", color="#151513", ms=14, mew=1.6)
        ax.text(top + 0.012, y, "interval [{:.4f}, {:.4f}]".format(floor, top),
                va="center", fontsize=7.6, color="#7e7c74")
ax.axvline(1.0, color="#3aa0c2", lw=1.0, ls=":", alpha=0.8)
# the retracted point
ax.plot([1.0369], [ypos[0]], marker="x", color="#c62828", ms=9, mew=2)
ax.text(1.0369, ypos[0] + 0.34, "Vol VIII's 1.0369\n(the surrogate artifact)\nRETRACTED",
        fontsize=7.0, color="#c62828", ha="center")
ax.set_yticks(ypos)
ax.set_yticklabels([it[0] for it in items], fontsize=7.8)
ax.set_xlim(0.985, 1.36)
ax.set_xlabel(r"$D(M)$ against the EYM floor (all floors $=1$ after normalization)",
              fontsize=8.5)
ax.set_title("(c)  The sandwich, recalibrated:\nfloors, closures, intervals — and the retraction",
             fontsize=10)
ax.tick_params(labelsize=8)
ax.grid(axis="x", alpha=0.25, lw=0.5)

out = "/home/z/my-project/download/figures/sandwich_locus.png"
fig.savefig(out, dpi=170)
print("OK figure:", out)
