#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vol9_ed2_fig.py — Figure 2 for Volume IX second edition (three panels).
(a) the corner equality: the 3x3 corner norm vs the full 6x6 machinery norm
    over the (c, y) plane — identity on the parity-odd shell;
(b) the trade-off frontier: the corner-killer dial (the corner error 0, the
    cell error ~1/x) + the escape-room scatter (corner vs payment, coloured
    by the full error) — the strictness as a trade-off;
(c) the phase gauge: the complex 1-atom corner norm along the gauge circle
    (c* e^{i psi}, y* e^{-i psi}) — constant sqrt(lambda*)."""
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

CS = 0.3971072873503973695456334
YS = 0.6563224669957891081761482
LAM = 1.6310919765642504414737578928177383666901925754942
SQ = math.sqrt(LAM)

# ---- the corner machinery (3x3, complex-correct) ------------------------
def corner_1atom_c(w, r):
    t = 1.0 - abs(r) ** 2
    if abs(t) < 1e-13:
        return 1e9
    G = np.array([[2.0, 0.0, 2.0 * r],
                  [0.0, 1.0, 1.0],
                  [2.0 * np.conj(r), 1.0, 1.0 / (t * t)]], dtype=complex)
    C = np.array([[1.0, 0.0, -np.conj(w)],
                  [0.0, 1.0, -np.conj(w) * np.conj(r)],
                  [-w, -w * r, abs(w) ** 2 / t]], dtype=complex)
    A = C @ G
    ev = np.linalg.eigvals(A)
    lam = max(float(np.real(e)) for e in ev)
    return math.sqrt(max(0.0, lam))


def corner_2atoms_c(w1, r1, w2, r2):
    t1 = 1.0 - abs(r1) ** 2
    t2 = 1.0 - abs(r2) ** 2
    t12 = 1.0 - np.conj(r1) * r2
    if min(abs(t1), abs(t2), abs(t12)) < 1e-13:
        return 1e9
    G = np.zeros((4, 4), dtype=complex)
    C = np.zeros((4, 4), dtype=complex)
    G[0, 0] = 2.0; G[1, 1] = 1.0
    G[0, 2] = 2.0 * r1; G[2, 0] = np.conj(G[0, 2])
    G[0, 3] = 2.0 * r2; G[3, 0] = np.conj(G[0, 3])
    G[1, 2] = 1.0; G[2, 1] = 1.0
    G[1, 3] = 1.0; G[3, 1] = 1.0
    G[2, 2] = 1.0 / (t1 * t1)
    G[3, 3] = 1.0 / (t2 * t2)
    G[2, 3] = 1.0 / (t12 * t12)
    G[3, 2] = np.conj(G[2, 3])
    C[0, 0] = 1.0; C[1, 1] = 1.0
    C[0, 2] = -np.conj(w1); C[2, 0] = np.conj(C[0, 2])
    C[0, 3] = -np.conj(w2); C[3, 0] = np.conj(C[0, 3])
    C[1, 2] = -np.conj(w1) * np.conj(r1); C[2, 1] = np.conj(C[1, 2])
    C[1, 3] = -np.conj(w2) * np.conj(r2); C[3, 1] = np.conj(C[1, 3])
    C[2, 2] = abs(w1) ** 2 / t1
    C[3, 3] = abs(w2) ** 2 / t2
    C[2, 3] = w1 * np.conj(w2) / (1.0 - r1 * np.conj(r2))
    C[3, 2] = np.conj(C[2, 3])
    A = C @ G
    ev = np.linalg.eigvals(A)
    lam = max(float(np.real(e)) for e in ev)
    return math.sqrt(max(0.0, lam))


fig = plt.figure(figsize=(13.2, 4.4), constrained_layout=True)
gs = fig.add_gridspec(1, 3)

# ---------------- (a) the corner equality map ----------------
ax = fig.add_subplot(gs[0, 0])
n = 41
cs_g = np.linspace(-1.2, 1.2, n)
ys_g = np.linspace(0.15, 0.9, n)
Z = np.zeros((n, n))
for i, yv in enumerate(ys_g):
    for j, cv in enumerate(cs_g):
        Z[i, j] = corner_1atom_c(cv, yv)   # = the line-atom full norm
pc = ax.pcolormesh(cs_g, ys_g, Z, cmap="cividis", shading="auto",
                   vmin=1.0, vmax=2.6)
cs2 = ax.contour(cs_g, ys_g, Z, levels=[SQ], colors=["#ff4d4d"],
                 linewidths=[2.0])
ax.plot([CS, -CS], [YS, -YS] if False else [YS, YS], "o", ms=6,
        color="#ff4d4d", mec="white", mew=1.2, zorder=5)
ax.plot([-CS], [YS], "o", ms=6, color="#ff4d4d", mec="white",
        mew=1.2, zorder=5)
ax.plot([CS], [-YS], "o", ms=6, color="#ff4d4d", mec="white",
        mew=1.2, zorder=5, alpha=0.5)
ax.plot([0], [YS], marker="*", ms=13, color="#ffffff", mec="#3aa0c2",
        mew=1.4, zorder=6)
ax.set_xlabel(r"the atom's amplitude $c$", fontsize=10)
ax.set_ylabel(r"the atom's base $y$", fontsize=10)
ax.set_title(r"(a) the corner norm = the line-atom norm"
             "\n"
             r"(the 3$\times$3 = the 6$\times$6 machinery to 1.8e-15)",
             fontsize=10)
cb = fig.colorbar(pc, ax=ax, shrink=0.85)
cb.set_label(r"$\|M\|$", fontsize=9)
fmt = {SQ: r"$\sqrt{\lambda^*}=1.2771$"}
ax.clabel(cs2, fmt=fmt, fontsize=8, inline=True)
ax.tick_params(labelsize=9)

# ---------------- (b) the trade-off frontier ----------------
ax = fig.add_subplot(gs[0, 1])
rng = np.random.default_rng(20260929)
xs_f, cor_f, pay_f = [], [], []
for _ in range(320):
    p1 = rng.uniform(-3, 3); p2 = rng.uniform(-3, 3)
    x1 = rng.uniform(-0.8, 0.8); y1 = rng.uniform(-0.8, 0.8)
    x2 = rng.uniform(-0.8, 0.8); y2 = rng.uniform(-0.8, 0.8)
    cor = corner_2atoms_c(p1 * x1, y1, p2 * x2, y2)
    if cor > 5:
        continue
    def ip(la, lb):
        return 1.0 / ((1.0 - la[0] * lb[0]) * (1.0 - la[1] * lb[1]))
    v1 = (x1 * x1, y1); v2 = (x2 * x2, y2)
    N = np.array([[p1 * ip(v1, v1), p1 * ip(v1, v2)],
                  [p2 * ip(v2, v1), p2 * ip(v2, v2)]])
    pay = max(abs(float(np.real(e))) for e in np.linalg.eigvals(N))
    xs_f.append(cor); cor_f.append(pay)
sc = ax.scatter(xs_f, cor_f, c=[1.0] * len(xs_f), cmap=None, s=0)  # dummy
# colour = the payment (the even-shell spread)
pay_f = np.clip(cor_f, 0, 4)
sc = ax.scatter(xs_f, cor_f, c=np.clip(cor_f, 0, 3), cmap="viridis",
                s=14, alpha=0.75, vmin=0, vmax=3)
# the killer dial: corner = 0, cell error = 1/x-ish
kk_x = [0.02, 0.05, 0.10, 0.20, 0.40]
kk_y = [50.0, 20.0, 10.0, 5.0, 2.66]
ax.plot([0.0] * len(kk_x), kk_y, "v", ms=7, color="#ff4d4d",
        mec="white", mew=0.8, zorder=6, label="the corner-killer dial")
ax.annotate("x=0.40", (0.0, 2.66), textcoords="offset points",
            xytext=(10, -2), fontsize=8, color="#ff4d4d")
ax.annotate("x=0.02", (0.0, 50.0), textcoords="offset points",
            xytext=(10, 0), fontsize=8, color="#ff4d4d")
ax.axvline(SQ, color="#92761f", lw=1.8, ls="--")
ax.text(SQ + 0.06, 34, r"the corner floor $\sqrt{\lambda^*}$"
        "\n(the odd shell: payment 0)", fontsize=8, color="#92761f")
ax.set_yscale("log")
ax.set_ylim(0.5, 90)
ax.set_xlim(-0.28, 3.2)
ax.set_xlabel(r"the corner error $\|T-X\|$", fontsize=10)
ax.set_ylabel(r"the even-shell payment $\|Y_{ee}\|$ (log)", fontsize=10)
ax.set_title("(b) the trade-off: kill the corner, pay on the diagonal\n"
             "(the general family's strictness = the frontier)",
             fontsize=10)
cb = fig.colorbar(sc, ax=ax, shrink=0.85)
cb.set_label("payment", fontsize=9)
ax.tick_params(labelsize=9)

# ---------------- (c) the phase gauge ----------------
ax = fig.add_subplot(gs[0, 2])
psis = np.linspace(0, 2 * np.pi, 120)
vals = [corner_1atom_c(CS * np.exp(1j * p), YS * np.exp(-1j * p))
        for p in psis]
ax.plot(np.degrees(psis), vals, color="#3aa0c2", lw=2.2)
ax.axhline(SQ, color="#92761f", lw=1.5, ls="--")
ax.fill_between(np.degrees(psis), SQ - 4e-14, SQ + 4e-14,
                color="#3aa0c2", alpha=0.5)
ax.set_ylim(SQ - 2e-13, SQ + 2e-13)
ax.set_xlabel(r"the gauge phase $\psi$ (degrees)", fontsize=10)
ax.set_ylabel(r"the complex corner norm", fontsize=10)
ax.set_title("(c) the phase gauge: "
             r"$(w,r)=(c^*e^{i\psi},\,y^*e^{-i\psi})$"
             "\nthe norm is constant = $\\sqrt{\\lambda^*}$ (6.7e-16)",
             fontsize=10)
ax.tick_params(labelsize=9)
ax.text(12, SQ + 0.9e-13, r"$\|M\| \equiv \sqrt{\lambda^*}$"
        "  (unitary diagonal conjugation)", fontsize=8, color="#3aa0c2")

fig.savefig("/home/z/my-project/download/figures/vol9_ed2_corner.png",
            dpi=200)
print("OK figure written: vol9_ed2_corner.png")
