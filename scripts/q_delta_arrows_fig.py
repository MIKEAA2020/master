#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure for the Q–Delta / arrow-strata battery: three panels.
(1) the Q–Delta_II plane with the channel families and the two bound
    violations; (2) the stratification plane (chi vs Q) with the record /
    quantum / thermo strata; (3) the 3-state ring: the entropy production
    vs the SECOND Hankel singular value (the rank witness) with the
    equilibrium ridge."""
import json
import math
import numpy as np
import matplotlib.font_manager as fm
try:
    fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
except Exception:
    pass
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Noto Sans SC']
plt.rcParams['axes.unicode_minus'] = False

R = json.load(open('/home/z/my-project/scripts/q_delta_arrows_results.json'))['verdicts']

GOLD = '#91751f'
DARK = '#4d4631'
RED = '#a94438'
BLUE = '#3d6b8e'
GREEN = '#5c7a4a'
GRAY = '#8a8577'

fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.35), constrained_layout=True)

# ---------------- Panel 1: the Q–Delta_II plane ----------------
ax = axes[0]
ps = np.linspace(0.001, 0.999, 120)
ax.plot(1 - ps, [max(0.0, 1.0 - (lambda x: 0 if x <= 0 or x >= 1 else
                                  -x * math.log2(x) - (1 - x) * math.log2(1 - x))(pp / 2)) for pp in ps],
        color=BLUE, lw=1.8, label='dephasing $Q=1-H_2(p/2)$')
ax.plot(1 - ps, [max(0.0, 1.0 - (lambda x: 0 if x <= 0 or x >= 1 else
                                  -x * math.log2(x) - (1 - x) * math.log2(1 - x))(3 * pp / 4) -
                  3 * pp / 4 * math.log2(3)) for pp in ps],
        color=RED, lw=1.8, label='depolarizing')
ax.plot(1 - 2 * ps, np.maximum(0, 1 - 2 * ps), color=GREEN, lw=1.8,
        label='erasure $Q=\\max(0,2\\Delta-1)$')
# the measured plane rows (CONV-II)
rows = R['C_Q_Delta_plane']['plane_rows']
ax.scatter([r['Delta_II'] for r in rows if r['channel'] == 'AD'],
           [r['Q'] for r in rows if r['channel'] == 'AD'],
           color=DARK, s=34, zorder=5, marker='s', label='amplitude damping')
ax.scatter([r['Delta_II'] for r in rows if r['channel'] == 'qutrit_depol'],
           [r['Q'] for r in rows if r['channel'] == 'qutrit_depol'],
           color=GOLD, s=44, zorder=6, marker='^', label='qutrit depol.')
ax.plot([0, 1], [0, 1], color=GRAY, lw=1.0, ls='--', label='$Q=\\Delta$ line')
ax.annotate('qutrit at $p\\!=\\!0.05$:\n$Q=1.189>\\Delta=0.95$\n(dimension-broken)',
            xy=(0.95, 1.189), xytext=(0.30, 1.02), fontsize=8.0, color=GOLD,
            arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.0))
ax.set_xlabel('$\\Delta_{II}$ (Choi-state eigenvalue gap)')
ax.set_ylabel('coherent information $Q$')
ax.set_title('(1) The $Q$–$\\Delta_{II}$ plane: no universal law\n'
             'CONV-I violations 15/22; chord lemma 300/300', fontsize=10)
ax.legend(fontsize=7.4, loc='lower right', framealpha=0.9)
ax.set_xlim(0, 1.02)
ax.set_ylim(-0.08, 1.35)

# ---------------- Panel 2: the stratification plane ----------------
ax = axes[1]
st = R['D_stratification']['strata_table']
mk = {'identity': ('o', DARK), 'unitary (Hadamard)': ('o', DARK),
      'dephasing p=0.25': ('D', BLUE), 'FULL dephasing p=1.0': ('P', RED),
      'depolarizing p=0.25': ('s', GREEN), 'erasure p=0.25': ('^', GOLD),
      'amplitude damping g=0.4': ('v', GRAY)}
lbl = {'identity': 'identity', 'unitary (Hadamard)': 'unitary',
       'dephasing p=0.25': 'dephasing $p\\!=\\!0.25$',
       'FULL dephasing p=1.0': 'FULL dephasing',
       'depolarizing p=0.25': 'depolarizing',
       'erasure p=0.25': 'erasure', 'amplitude damping g=0.4': 'amp. damping'}
for r in st:
    m, c = mk[r['channel']]
    ax.scatter(r['chi_classical'], r['Q_quantum'], marker=m, color=c,
               s=90, zorder=5, edgecolors='white', linewidths=0.8)
    ax.annotate(lbl[r['channel']],
                (r['chi_classical'], r['Q_quantum']),
                textcoords='offset points', xytext=(8, -3), fontsize=7.6,
                color=c)
ax.plot([0, 1], [1, 0], color=GRAY, lw=0.9, ls=':')
ax.annotate('FULL dephasing:\n$\\chi\\!=\\!1$, $Q\\!=\\!0$ — the honest\n'
            '"classical, not quantum"\nwitness (EB endpoint)',
            xy=(1.0, 0.0), xytext=(0.34, 0.10), fontsize=7.6, color=RED,
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.0))
ax.annotate('chat claimed dephasing HERE\n($Q\\!=\\!0$ for all $p$) — refuted;\n'
            'measured $Q\\!=\\!0.456$',
            xy=(1.0, 0.456), xytext=(0.30, 0.72), fontsize=7.6, color=BLUE,
            arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.0))
ax.set_xlabel('classical stratum: Holevo capacity $\\chi$')
ax.set_ylabel('quantum stratum: coherent info. $Q$')
ax.set_title('(2) The stratification plane: independent strata\n'
             'erasure: $\\chi=(1+Q)/2$ exactly (2:1 schedules)', fontsize=10)
ax.set_xlim(-0.04, 1.12)
ax.set_ylim(-0.15, 1.12)

# ---------------- Panel 3: the ring: the rank witness ----------------
ax = axes[2]
rg = R['E_arrow_baselines']['three_state_ring']['grid']
sig = [r['sigma'] for r in rg]
sv2 = [r['sv2'] for r in rg]
sv1 = [r['sv1'] for r in rg]
sc = ax.scatter(sig, sv2, c=sv1, cmap='viridis', s=16, alpha=0.9,
                edgecolors='none', zorder=4)
ax.axvline(0.0, color=RED, lw=1.4, ls='--')
ax.annotate('equilibrium ridge $a\\!=\\!b$:\n$\\sigma\\!=\\!0$ exactly, '
            '$\\sigma_2\\!=\\!0$ (rank 1),\nbut $\\sigma_1>0$ — the GAP '
            'survives\nthe vanishing arrow',
            xy=(0.001, 0.004), xytext=(0.10, 0.115), fontsize=7.8,
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.0))
ax.set_xlabel('entropy production $\\sigma=(a-b)\\ln(a/b)$  (= reversal '
              'divergence, exact)')
ax.set_ylabel('second Hankel singular value $\\sigma_2$')
ax.set_title('(3) THE RANK WITNESS on the 3-state ring\n'
             '$\\sigma_2>0 \\Leftrightarrow \\sigma>0$: the arrow is a '
             'rank defect', fontsize=10)
plt.colorbar(sc, ax=ax, label='$\\sigma_1$ (memory scale)', pad=0.015)

fig.suptitle('The arrow strata: the multi-channel $Q$–$\\Delta$ battery — '
             'conventions, stratification, and the arrow as a rank defect',
             fontsize=11.5, color=DARK, y=1.06)
out = '/home/z/my-project/download/figures/q_delta_arrows.png'
fig.savefig(out, dpi=200, facecolor='white')
print('saved', out)
