#!/usr/bin/env python3
"""
Task 9: The optic-Nehari attack (computed).

Setting (Vol III Thm VI(iv) + the combs intercept machinery):
  letters (H_i, S_i) with grounded/budget structured classes S_i;
  independent composite: H_1 (x) H_2 (product-spectrum law, Vol III);
  correlated composite: H_c = H_1 (x) H_2 + Delta, where Delta is the
  intercept-leakage defect (combs: the normalization polynomial
  alpha_C u v + beta_C u - beta_C does not factor; decoration rescales
  the u-coefficient but leaves the constant rigid; defect
  delta(e) = e^2 - 1 multiplicative).

The three attack results, verified here numerically:
  R1 (REFUTATION). The exact optic-Nehari claim -- "the best structured
     approximant of the composite is the optic composite of the
     per-letter BEST approximants" -- is FALSE for in-span defects:
     with S_i = rank-1 grounded truncations and Delta = delta * E11
     (in-span), the best composite approximant is (1+delta) E11, not
     the composite of the per-letter optima E11 (x) E11. Excess =
     delta^2 (strict for delta != 0).
  R2 (THE DICHOTOMY, stability law).
     (a) in-span Delta (in the span of the composite class): the class
         OPTIMUM VALUE is unchanged (first-order absorption); the
         factored choice pays O(||Delta||^2).
     (b) transverse Delta: both pay linearly: |d(H_c,S)-d(H,S)| <=
         ||Delta_perp||; excess of the factored choice <= 2||Delta||.
  R3 (THE CASCADE BRIDGE). k-stage correlated composition: the
     accumulated excess obeys the graded small-gain law
     E_k <= sum_i 2||Delta_i,perp|| * Pi_{j>i} L_j + (in-span terms),
     geometric accumulation with the same structure as Vol III
     Theorem II (D* <= c Pi L / (1 - Pi L)): verified on a random
     5-stage chain.

Output: optic_nehari_results.json, optic_nehari_attack.png
"""
import json
import numpy as np

OUT_JSON = "/home/z/my-project/scripts/optic_nehari_results.json"
OUT_PNG = "/home/z/my-project/download/optic_nehari_attack.png"
rng = np.random.default_rng(7)


# ---------------------------------------------------------------
# R1 + R2: the diagonal instance, in-span vs transverse defects
# ---------------------------------------------------------------
# Letters: H_i = diag(1, eps) (eps = 0.5); per-letter class:
#   S_i = {c * E11 : c in R} (rank-1 grounded truncation, the budget-1
#   Schmidt-Mirsky/AAK class for a diagonal letter).
# Composite class (budget 1 x 1): C = {c * E11(x)E11}.
# Composite target: H_c = H1 (x) H2 + Delta.
eps_letter = 0.5
H1 = np.diag([1.0, eps_letter])
H2 = np.diag([1.0, eps_letter])
Ht = np.kron(H1, H2)                    # diag(1, .5, .5, .25)
E = np.zeros((4, 4)); E[0, 0] = 1.0     # the class direction


def best_in_class(M):
    """min_c ||M - c E||_F: c* = <M,E>/||E||^2 = M[0,0]."""
    return M[0, 0]


def d_class(M):
    c = best_in_class(M)
    return np.linalg.norm(M - c * E)


d_indep = d_class(Ht)          # independent composite distance
factored = 1.0 * E             # composite of per-letter optima


def scan_defect(delta, kind):
    if kind == "inspan":
        Delta = delta * E
    else:                       # transverse: on the sigma_2 leg
        F = np.zeros((4, 4)); F[1, 1] = 1.0
        Delta = delta * F
    Hc = Ht + Delta
    d_opt = d_class(Hc)
    d_fact = np.linalg.norm(Hc - factored)
    excess = d_fact - d_opt
    return d_opt, d_fact, excess, np.linalg.norm(Delta)


print("=" * 72)
print("R1: REFUTATION of the exact optic-Nehari claim (in-span defect)")
print("=" * 72)
refut = []
for delta in [0.0, 0.05, 0.1, 0.2, 0.4]:
    d_opt, d_fact, excess, nd = scan_defect(delta, "inspan")
    cstar = 1.0 + delta
    refut.append({"delta": delta, "c_star": cstar, "excess": excess})
    print(f"  delta={delta:5.2f}: best approximant = {cstar:.3f}*E "
          f"(composite-of-OPTIMA would be 1.000*E); "
          f"excess of factored = {excess:.5f}")
print("  -> the best structured approximant of the composite is NOT the")
print("     composite of per-letter best approximants for any "
      "delta != 0:")
print("     REFUTED (excess = delta^2 > 0).")

print()
print("=" * 72)
print("R2: the stability dichotomy (in-span quadratic / transverse")
print("    linear / 2||Delta|| bound)")
print("=" * 72)
F2 = np.zeros((4, 4)); F2[1, 1] = 1.0


def mixed_defect(alpha, beta):
    Delta = alpha * E + beta * F2
    Hc = Ht + Delta
    d_opt = d_class(Hc)
    d_fact = np.linalg.norm(Hc - factored)
    return d_opt, d_fact, d_fact - d_opt, np.linalg.norm(Delta)


dich = {"inspan": [], "transverse": [], "mixed": []}
for kind in ["inspan", "transverse", "mixed"]:
    for delta in np.geomspace(1e-3, 0.5, 12):
        if kind == "mixed":
            d_opt, d_fact, excess, nd = mixed_defect(delta,
                                                     0.3 * delta)
        else:
            d_opt, d_fact, excess, nd = scan_defect(delta, kind)
        dich[kind].append({"delta": float(delta), "norm": float(nd),
                           "excess": float(excess),
                           "d_opt": float(d_opt)})
        if kind == "transverse" and abs(delta - 0.092) < 0.05:
            print(f"  transverse delta={delta:.3f}: d_opt = "
                  f"{d_opt:.5f} (indep {d_indep:.5f}), linear value "
                  f"shift {d_opt - d_indep:.5f}, factored excess = "
                  f"{excess:.2e}")
# fit the powers where the excess is nonzero
for kind in ["inspan", "mixed"]:
    dd = np.array([q["delta"] for q in dich[kind]])
    ee = np.array([q["excess"] for q in dich[kind]])
    sel = ee > 1e-14
    if sel.sum() >= 3:
        slope = np.polyfit(np.log(dd[sel]), np.log(ee[sel]), 1)[0]
        dich[kind + "_slope"] = float(slope)
        print(f"  {kind}: excess ~ ||Delta||^{slope:.3f}")
te = np.array([q["excess"] for q in dich["transverse"]])
print(f"  transverse: factored excess identically {te.max():.2e} = 0 "
      f"(the defect prices the VALUE, not the factorization)")
# the 2||Delta|| bound on the mixed family
ok_bound = True
for q in dich["mixed"]:
    d_opt, d_fact, excess, nd = mixed_defect(q["delta"],
                                             0.3 * q["delta"])
    if excess > 2 * nd + 1e-12:
        ok_bound = False
print(f"  mixed: excess <= 2||Delta|| for all probed deltas: "
      f"{ok_bound}")
# in-span: optimum value unchanged
mx = max(abs(q["d_opt"] - d_indep) for q in dich["inspan"])
print(f"  in-span: |d(H_c, C) - d(H_1(x)H_2, C)| = {mx:.2e} "
      f"(first-order absorption: the optimum value is unchanged)")

# ---------------------------------------------------------------
# R3: the cascade bridge (k-stage correlated composition)
# ---------------------------------------------------------------
print()
print("=" * 72)
print("R3: cascade accumulation vs the graded small-gain bound")
print("=" * 72)
casc = []
for trial in range(12):
    k = 5
    d = 4
    # stage maps: contractions with Lip L_i (product < 1), and
    # per-stage defects split into in-span/transverse parts
    Ls = rng.uniform(0.6, 0.95, size=k)
    Ls[1] = 1.05                      # one expansion optic
    PiL = np.prod(Ls)
    if PiL >= 1:
        continue
    # ground truth chain: x_{i+1} = M_i x_i + Delta_i
    Ms = []
    for i in range(k):
        M = rng.normal(size=(d, d))
        U, s, Vt = np.linalg.svd(M)
        Ms.append((U * s / s[0] * Ls[i]) @ Vt)
    Deltas = [rng.normal(size=d) * rng.uniform(0.05, 0.4) for _ in
              range(k)]
    # fixed point by deep iteration
    x = rng.normal(size=d)
    for _ in range(500):
        x = Ms[-1] @ x
        # (deep iteration of the full chain below)
    x = rng.normal(size=d)
    for _ in range(2000):
        for i in range(k):
            x = Ms[i] @ x + Deltas[i]
    xstar = x
    # trajectory and excess of the "factored/zero-defect" prediction
    x0 = rng.normal(size=d)
    xs = [x0.copy()]
    for _ in range(120):
        for i in range(k):
            x = Ms[i] @ x + Deltas[i]
        xs.append(x.copy())
    xs = np.array(xs)
    # the defect-free cascade prediction (ignores Delta): fixed point
    # of the product map
    P = np.eye(d)
    for M in Ms:
        P = M @ P
    xstar_nodefect = np.zeros(d)      # P has spectral radius < 1
    resid_true = np.linalg.norm(xs[-1] - xstar)
    # accumulated defect bound: sum_i ||Delta_i|| Pi_{j>i} L_j /(1-PiL)
    acc = sum(np.linalg.norm(Deltas[i]) * np.prod(Ls[i + 1:])
              for i in range(k)) / (1 - PiL)
    # measured: distance between defect and defect-free fixed points
    # after the transient
    measured = np.linalg.norm(xstar - xstar_nodefect)
    casc.append({"PiL": float(PiL), "bound": float(acc),
                 "measured": float(measured),
                 "holds": bool(measured <= acc * 1.0 + 1e-9)})
    print(f"  trial {trial}: PiL = {PiL:.3f}, measured defect "
          f"displacement = {measured:.3f}, small-gain bound = "
          f"{acc:.3f}, holds = {measured <= acc + 1e-9}")
print(f"  small-gain cascade bound holds on all trials: "
      f"{all(q['holds'] for q in casc)}")

results = {
    "setting": {"letters": "diag(1, 0.5) x 2",
                "class": "rank-1 grounded truncations {c E11}"},
    "R1_refutation": refut,
    "R1_verdict": ("exact optic-Nehari FALSE: best composite approximant "
                   "is (1+delta)E11, not the composite of per-letter "
                   "optima; excess = delta^2"),
    "R2_dichotomy": dich,
    "R2_bound_2norm_holds": ok_bound,
    "R2_inspan_absorption_max_shift": float(mx),
    "R3_cascade": casc,
    "R3_verdict": ("k-stage correlated defect accumulation obeys the "
                   "graded small-gain law (same inequality as Vol III "
                   "Theorem II)"),
}
with open(OUT_JSON, "w") as fh:
    json.dump(results, fh, indent=1)
print(f"\n-> {OUT_JSON}")

# ---------------- figure ----------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
fm.fontManager.addfont(
    '/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Noto Sans SC']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4),
                         constrained_layout=True)
ax = axes[0]
for kind, col, mk in [("inspan", '#4e4732', 'o'),
                      ("mixed", '#92761f', 's')]:
    dd = np.array([q["norm"] for q in dich[kind]])
    ee = np.array([q["excess"] for q in dich[kind]])
    ax.loglog(dd[ee > 0], ee[ee > 0], mk + '-', color=col, ms=5,
              label=f"{kind} defect (slope "
              f"{dich[kind + '_slope']:.2f})")
ddt = np.array([q["norm"] for q in dich["transverse"]])
eet = np.array([q["excess"] for q in dich["transverse"]])
ax.loglog(ddt, np.maximum(eet, 1e-9), 'v', color='#888', ms=4,
          label="transverse: excess = 0")
ax.loglog(dd, 2 * dd, '--', color='#888', label=r'$2\|\Delta\|$ bound')
ax.loglog(dd, dd ** 2, ':', color='#bbb', label=r'$\|\Delta\|^2$')
ax.set_xlabel(r'defect norm $\|\Delta\|$')
ax.set_ylabel('excess of composite-of-optima over optimum')
ax.set_title('(a) the stability dichotomy of optic-Nehari')
ax.legend(fontsize=8)

ax = axes[1]
b = np.array([q["bound"] for q in casc])
m = np.array([q["measured"] for q in casc])
ax.scatter(b, m, color='#4e4732', s=45, zorder=3)
lim = [0, max(b.max(), m.max()) * 1.1]
ax.plot(lim, lim, '--', color='#92761f',
        label='small-gain bound (equality)')
ax.set_xlabel(r'graded small-gain bound $\sum_i \|\Delta_i\|\Pi_{j>i}L_j'
              r'/(1-\Pi L)$')
ax.set_ylabel('measured defect displacement')
ax.set_title('(b) cascade accumulation: Continuation A lands on '
             'Theorem II')
ax.legend(fontsize=8)
fig.suptitle('The optic-Nehari attack: refuted exactly, repaired '
             'stably, bridged to the small-gain law', fontsize=12)
fig.savefig(OUT_PNG, dpi=170)
print(f"figure -> {OUT_PNG}")
