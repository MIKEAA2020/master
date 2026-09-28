#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""abelian_rung_fig.py — the three-panel figure for Volume VIII.
(a) the multinomial mountain: the transport-obstruction profile
    sqrt(mu(beta) mu(gamma-beta)) over decompositions (log colour scale);
(b) the multinomial budget: the lambda-plane — the atom interior, the
    isometry sphere (the multiplicative gradings), the isotropic point,
    the vertices, and the two-axis demand outside the budget;
(c) the sandwich on the rung: EYM floors vs certified families, per
    witness (the closed golden witnesses; the open cell interval; the
    strict-failure amalgam interval).
"""
import math
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

fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.3), constrained_layout=True)

# ---------------- (a) the multinomial mountain ----------------
g1, g2 = 6, 6
P = np.zeros((g1 + 1, g2 + 1))
for j in range(g1 + 1):
    for l in range(g2 + 1):
        mu_b = math.factorial(j + l) / (math.factorial(j) * math.factorial(l))
        rj, rl = g1 - j, g2 - l
        mu_a = math.factorial(rj + rl) / (math.factorial(rj) * math.factorial(rl))
        P[j, l] = math.sqrt(mu_b * mu_a)
im = axes[0].imshow(np.log10(P), origin='lower', cmap='viridis',
                    extent=[0, g2, 0, g1], aspect='auto')
cbar = fig.colorbar(im, ax=axes[0], shrink=0.85, pad=0.02)
cbar.set_label('log10 profile value', fontsize=8)
axes[0].set_xlabel(r'beta_2 (letters b in the prefix)', fontsize=9)
axes[0].set_ylabel(r'beta_1 (letters a in the prefix)', fontsize=9)
axes[0].set_title('(a) The multinomial mountain, gamma = (6,6)\n'
                  'profile $\\sqrt{\\mu(\\beta)\\mu(\\gamma-\\beta)}$ over the '
                  'decompositions', fontsize=10)
axes[0].annotate('corners: 1\n(no defect)', xy=(0.15, 5.7), fontsize=8,
                 color='white', ha='left')
axes[0].annotate('centre: $\\sqrt{C(12,6)}\\approx$ 30.4',
                 xy=(2.0, 3.1), fontsize=8, color='white')
axes[0].text(0.5, -0.34,
             'defect ratio $\\rho(\\gamma)=\\sqrt{\\mu(\\gamma)}$ — exactly the '
             'strip spread;\naxes 1, balanced cells exponential '
             '$\\sim 2^k(\\pi k)^{-1/4}$',
             transform=axes[0].transAxes, ha='center', fontsize=8, color=DARK)

# ---------------- (b) the multinomial budget ----------------
th = np.linspace(0, 2 * np.pi, 400)
ax = axes[1]
ax.fill(np.cos(th), np.sin(th), color=BLUE, alpha=0.13)
ax.plot(np.cos(th), np.sin(th), color=BLUE, lw=2)
ax.plot(0.8, 0.6, 'o', color=GOLD, ms=9)
ax.annotate('multiplicative gradings\n(the exact AAK class)\n'
            r'$\Sigma\lambda_a^2 = 1$', xy=(0.8, 0.6), xytext=(0.62, 0.86),
            fontsize=8, color=DARK, arrowprops=dict(arrowstyle='-', color=GREY))
ax.plot(0, 0, 'o', color=DARK, ms=6)
ax.annotate('atoms (rank-1 approximants)\n' r'$\Sigma\lambda_a^2 < 1$',
            xy=(0.16, 0.16), xytext=(0.30, 0.30), fontsize=8, color=DARK,
            arrowprops=dict(arrowstyle='-', color=GREY))
ax.plot(1 / math.sqrt(2), 1 / math.sqrt(2), 's', color=GOLD, ms=7)
ax.annotate('isotropic point = Vol VII V\n' r'$(1/\sqrt{n}, 1/\sqrt{n})$',
            xy=(0.707, 0.707), xytext=(-0.98, 0.78), fontsize=8, color=DARK,
            arrowprops=dict(arrowstyle='-', color=GREY))
for x, y, lab in [(1, 0, 'vertex $e_a$'), (0, 1, 'vertex $e_b$')]:
    ax.plot(x, y, 'D', color=GOLD, ms=6)
    ax.annotate(lab, xy=(x, y), xytext=(x - 0.33, y - 0.13), fontsize=8,
                color=DARK)
ax.plot(1, 1, 'X', color=RED, ms=11)
ax.annotate('the two-axis demand\n' r'$\lambda=(1,1)$: $\rho=2$ — the budget'
            '\noverdraft (factor $n$)', xy=(1, 1), xytext=(0.18, 1.12),
            fontsize=8, color=RED)
ax.plot([1, 0.707], [1, 0.707], '--', color=RED, lw=1.2, alpha=0.7)
ax.set_xlim(-1.15, 1.45); ax.set_ylim(-1.25, 1.45)
ax.set_aspect('equal')
ax.set_xlabel(r'$\lambda_a$', fontsize=9)
ax.set_ylabel(r'$\lambda_b$', fontsize=9)
ax.set_title('(b) The multinomial budget\n'
             r'admissible reweightings: $\Sigma_a\lambda_a^2 \leq 1$'
             ' (bounded), $=1$ (isometric)', fontsize=10)
ax.axhline(0, color=GREY, lw=0.5, alpha=0.5)
ax.axvline(0, color=GREY, lw=0.5, alpha=0.5)

# ---------------- (c) the sandwich on the rung ----------------
ax = axes[2]
rows = [
    ("golden on the graded class (M=1)", 0.618, 0.618, GOLD, 'CLOSED'),
    ("gamma=(1,1) cell (M=1)", 1.41421, 1.41421, BLUE, 'CLOSED (paired)'),
    ("gamma=(1,1) cell (M=2)", 1.0, 1.3188, GREY, 'OPEN'),
    ("two-golden amalgam (M=1)", 1.0, 1.0369, RED, 'STRICT FAILURE'),
]
ypos = np.arange(len(rows))[::-1]
for (label, lo, hi, col, tag), y in zip(rows, ypos):
    if abs(hi - lo) < 1e-9:
        ax.plot([lo], [y], 'o', color=col, ms=9)
    else:
        ax.plot([lo, hi], [y, y], '-', color=col, lw=3.5,
                solid_capstyle='butt', alpha=0.85)
        ax.plot([lo], [y], '|', color=col, ms=13, mew=2.5)
        ax.plot([hi], [y], '|', color=col, ms=13, mew=2.5)
    ax.annotate(tag, xy=(max(hi, lo) + 0.06, y), fontsize=7.5, color=col,
                va='center')
ax.set_yticks(ypos)
ax.set_yticklabels([r[0] for r in rows], fontsize=8)
ax.set_xlabel('structured distance $D(M)$ (operator norm) — floor vs '
              'certified family', fontsize=9)
ax.set_xlim(0.4, 2.15)
ax.set_title('(c) The sandwich on the rung\nEYM floor $\\sigma_{M+1}$ (bar '
             'ends) vs the exhaustive families', fontsize=10)
ax.grid(axis='x', color=GREY, alpha=0.25, lw=0.6)
ax.axhline(0, color='white')
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

fig.suptitle('The abelianized rung and the $T_k$ classification — the '
             'multinomial weights as the exact obstruction',
             fontsize=11.5, color=DARK, y=1.06)
OUT = '/home/z/my-project/download/figures/abelian_rung.png'
fig.savefig(OUT, dpi=170, facecolor='white')
print('figure written:', OUT)
