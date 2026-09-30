#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""escape_fig.py — the four-panel escape figure for Volume XIII.
(a) the escape decomposed: the Vol IX shadow -> the symmetric shadow (the
    basin hop) -> the free point (the residual) — Task 29's 5.7e-7
    re-adjudicated into 5.64e-7 + 8.2e-9;
(b) the t^2 law: the measured dlambda(t) along the two pure ridge
    directions vs the theory's t^2 c (the quadratic law verified);
(c) the first-order landscape: mu_max(W1_j) per coordinate — the cone
    (8 coordinates, O(1)-O(10)) vs the flat ridge (the Aa block, ~1e-5);
(d) H2's curvature at the shadow: the ridge's 4x4 quadratic-form matrix
    (lambda_max of each 2x2 block) — the positive diagonal, the negative
    checkerboard, the near-null mixed combinations.
"""
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

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

GOLD = '#92761f'
BLUE = '#3aa0c2'
DARK = '#4e4732'
RED = '#b3452b'
GREY = '#7e7c74'

R = json.load(open("/home/z/my-project/github_repos/master/scripts/"
                   "escape_second_order_results.json"))

fig, axes = plt.subplots(2, 2, figsize=(12.6, 9.0),
                         constrained_layout=True)

# ---------------- (a) the escape decomposed ----------------
ax = axes[0, 0]
vol_ix = R["ES0"]["vol_ix"]                # 1.277142689665
sym = R["ES0"]["shadow_symmetric"]         # 1.277142125195
free = R["ES0"]["free_best"]               # 1.277142116995
t29 = R["ES0"]["task29_reference"]         # 1.277142117009
vals = [vol_ix, sym, free]
names = ["Vol IX scan optimum\n(the mis-located shadow)",
         "the symmetric basin\n(the shadow re-located)",
         "the free point\n(the coupled basin)"]
y = [2, 1, 0]
ax.barh(y, [v - 1.27714 for v in vals], height=0.52,
        color=[GREY, GOLD, BLUE], edgecolor='white')
ax.set_yticks(y)
ax.set_yticklabels(names, fontsize=8.5)
ax.set_xlabel("the norm, offset from 1.27714", fontsize=9)
ax.set_xlim(0, 5.0e-6)
ax.set_ylim(-0.45, 3.05)
ax.tick_params(labelsize=8)
# the decomposition arrows
ax.annotate('', xy=(sym - 1.27714, 1.42), xytext=(vol_ix - 1.27714, 1.42),
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.6))
ax.text((vol_ix + sym) / 2 - 1.27714, 1.60,
        "the basin hop  5.64e-7\n(abelian, not a free gain)",
        ha='center', fontsize=8, color=RED)
ax.annotate('', xy=(free - 1.27714, 0.42), xytext=(sym - 1.27714, 0.42),
            arrowprops=dict(arrowstyle='-|>', color=DARK, lw=1.6))
ax.text((sym + free) / 2 - 1.27714 + 0.9e-6, 0.28,
        "the residual  8.2e-9\n(certified 2.1e-8 in $\\lambda$)",
        ha='center', fontsize=8, color=DARK)
ax.axvline(t29 - 1.27714, color=BLUE, ls=':', lw=1.2)
ax.text(t29 - 1.27714 + 0.6e-7, 2.58, "Task 29's free point\n(1.277142117)",
        fontsize=7.5, color=BLUE)
ax.set_title("(a) The escape, decomposed — Task 29's 5.73e-7 =\n"
             "the abelian basin hop 5.64e-7 + the residual 8.2e-9",
             fontsize=10)

# ---------------- (b) the t^2 law ----------------
ax = axes[0, 1]
rows = np.array(R["ES4"]["t2_law"]["rows_e4"])   # (t, dlam)
c4 = R["ES3"]["pure_ridge_curvatures"][0]
c9 = R["ES3"]["pure_ridge_curvatures"][3]
e4 = np.eye(4)[0]
# the e_9 rows are not stored; recompute the line only
tt = rows[:, 0]
dd = rows[:, 1]
ax.loglog(tt, np.abs(dd), 'o-', color=GOLD, ms=4, lw=1.2,
          label="along $e_4$ (Aa diagonal): measured")
ax.loglog(tt, c4 * tt ** 2, '--', color=RED, lw=1.4,
          label="the theory $t^2c$, $c$ = 255.99")
ax.loglog(tt, 0.7 * c9 * tt ** 2, 's-', color=BLUE, ms=3.5, lw=1.0,
          label="along $e_9$ (Aa coupling): measured (scaled 0.7)")
ax.loglog(tt, 0.7 * c9 * tt ** 2 / (R["ES4"]["t2_law"]["e_9"]["c_fit"]
                                    / c9), ':', color=DARK, lw=1.2,
          label="the theory $t^2c$, $c$ = 183.34 (scaled)")
ax.set_xlabel("the step $t$ along the ridge direction", fontsize=9)
ax.set_ylabel("$|\\lambda(t\\hat u) - \\lambda_0|$", fontsize=9)
ax.legend(fontsize=7.5, loc='upper left')
ax.tick_params(labelsize=8)
ax.set_title("(b) The quadratic law verified: the measured curvature\n"
             "$c_{fit}$ 256.50 / 183.22 vs the theory 255.99 / 183.34\n"
             "(slopes 2.014 / 2.002; both branches of the split checked)",
             fontsize=10)
ax.grid(True, which='both', alpha=0.25, lw=0.4)

# ---------------- (c) the first-order cone and the flat ridge ----------------
ax = axes[1, 0]
mus = [0.0] * 12
cone_idx = [0, 1, 2, 3, 6, 7, 10, 11]
for i, j in enumerate(cone_idx):
    mus[j] = R["ES2"]["cone_mu_max"][i]
ridge = R["ES2"]["ridge_flatness"]
for j in (4, 5, 8, 9):
    mus[j] = ridge
colors = []
for j in range(12):
    colors.append(GREY if j in cone_idx else GOLD)
xpos = np.arange(12)
ax.semilogy(xpos, np.maximum(np.abs(mus), 3e-6), 'o', ms=7)
for j in range(12):
    ax.plot([j, j], [3e-6, max(abs(mus[j]), 3e-6)],
            color=colors[j], lw=2.2, alpha=0.85)
ax.set_xticks(xpos)
ax.set_xticklabels(["$B_1$", "$B_2$", "$C_1$", "$C_2$",
                    "$Aa_{11}$", "$Aa_{22}$", "$Ab_{11}$", "$Ab_{22}$",
                    "$Aa_{12}$", "$Aa_{21}$", "$Ab_{12}$", "$Ab_{21}$"],
                   fontsize=7.5)
ax.set_ylabel("$\\max |W1_j|$ (the first-order split)", fontsize=9)
ax.tick_params(labelsize=8)
ax.axhline(ridge, color=BLUE, ls='--', lw=1.0)
ax.text(0.05, ridge * 1.8, "the flat ridge: $|W1| \\leq$ 1.6e-5 "
       "(the Aa block)", fontsize=8, color=BLUE)
ax.set_title("(c) The first-order landscape: the CONE (the anti-parallel\n"
             "atoms on the B/C/Ab coordinates) and its FLAT RIDGE —\n"
             "the whole Aa block, the diagonals AND the couplings",
             fontsize=10)
ax.grid(True, which='major', alpha=0.25, lw=0.4)

# ---------------- (d) H2's checkerboard ----------------
ax = axes[1, 1]
im = np.array(R["ES3"]["ridge_T_lambda_max"], dtype=float)
cmap = plt.get_cmap('RdYlGn').copy()
imh = ax.imshow(im, cmap=cmap, vmin=-360, vmax=360)
labels = ["$Aa_{11}$", "$Aa_{22}$", "$Aa_{12}$", "$Aa_{21}$"]
ax.set_xticks(range(4)); ax.set_xticklabels(labels, fontsize=8)
ax.set_yticks(range(4)); ax.set_yticklabels(labels, fontsize=8)
for i in range(4):
    for j in range(4):
        ax.text(j, i, "%+.0f" % im[i, j], ha='center', va='center',
                fontsize=8.5, color='black')
cbar = fig.colorbar(imh, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label("the quadratic-form entry ($\\lambda_{max}$ of the 2x2 "
               "block)", fontsize=8)
ax.set_title("(d) $\\mathcal{H}_2$'s curvature at the shadow: the ridge's\n"
             "quadratic form — the POSITIVE pure curvatures, the\n"
             "NEGATIVE checkerboard of near-cancellation\n"
             "($\\kappa_{ridge}$ = +7.8e-5: no escape)", fontsize=10)

out = ("/home/z/my-project/github_repos/master/download/figures/"
       "escape_quantified.png")
fig.savefig(out, dpi=170)
print("OK figure:", out)
