#!/usr/bin/env python3
"""Diagnostic: determine the exact Kaufman parity rules. Self-contained."""
import numpy as np

D = 2


def consts(d, p):
    th = d - (d - 1) * p
    a = (d * d * th * th - 1.0) / (d ** 4 - 1)
    b = th / (d * d + 1)
    c = (d * d - th * th) / (d ** 4 - 1)
    Kd = 0.25 * np.log(a / c)
    Kh = 0.25 * np.log(a * c / b ** 2)
    W0 = (a * c * b * b) ** 0.25
    return Kd, Kh, W0


def pc2_closed(d):
    beta_d = (d * d - 1) / (d * d + 1)
    return (d - (beta_d + np.sqrt(beta_d ** 2 + 1))) / (d - 1)


def build_S(m, Kd, Kh):
    n = 1 << m
    bits = ((np.arange(n)[:, None] >> np.arange(m - 1, -1, -1)[None, :]) & 1)
    s = 1 - 2 * bits
    sc = np.roll(s, -1, axis=1)
    dh = np.exp(Kh * np.sum(s * sc, axis=1))
    E = np.exp(Kd * (s @ s.T + s @ sc.T))
    sq = np.sqrt(dh)
    return sq[:, None] * E * sq[None, :], s


def full_spectrum_sectors(m, Kd, Kh, W0):
    S, s = build_S(m, Kd, Kh)
    n = S.shape[0]
    flip = np.arange(n) ^ ((1 << m) - 1)
    ev = {}
    for parity, name in [(+1, "even"), (-1, "odd")]:
        reps = np.array([i for i in range(n) if i < flip[i]])
        dim = len(reps)
        u = np.zeros((n, dim))
        u[reps, np.arange(dim)] = 1.0
        u[flip[reps], np.arange(dim)] = parity
        u /= np.sqrt(2.0)
        W = u.T @ S @ u
        sv = np.linalg.svd(W, compute_uv=False) ** 2
        ev[name] = W0 ** (2 * m) * sv
    return ev


def candidate_products(m, Kd, Kh, W0):
    Q = lambda k: (np.cosh(2 * Kd) ** 2 * np.cosh(2 * Kh)
                   + np.sinh(2 * Kd) ** 2 * np.sinh(2 * Kh)
                   - np.sinh(2 * Kh) * np.cos(k))
    R = lambda k: 2 * np.sinh(2 * Kd) * np.cos(k / 2)
    wp = lambda k: Q(k) + np.sqrt(max(Q(k) ** 2 - R(k) ** 2, 0.0))
    wm = lambda k: Q(k) - np.sqrt(max(Q(k) ** 2 - R(k) ** 2, 0.0))
    K_even = (2 * np.arange(1, m + 1) - 1) * np.pi / m
    K_odd = 2 * np.pi * np.arange(0, m) / m
    base = (2 * W0 ** 2) ** m
    out = {}
    for name, Ks in [("even", K_even), ("odd", K_odd)]:
        wps = np.array([wp(k) for k in Ks])
        wms = np.array([wm(k) for k in Ks])
        r = wms / wps
        out[(name, 0)] = base * np.prod(wps)
        j = int(np.argmax(r))
        out[(name, 1)] = base * np.prod(wps) * r[j]
        jj = np.argsort(r)[::-1][:2]
        out[(name, 2)] = base * np.prod(wps) * np.prod(r[jj])
    return out


pc = pc2_closed(D)
print("p_c =", pc)
for p in [0.16, pc, 0.24, 0.30, 0.40]:
    m = 5
    Kd, Kh, W0, = consts(D, p)[:3]
    ev = full_spectrum_sectors(m, Kd, Kh, W0)
    cands = candidate_products(m, Kd, Kh, W0)
    print(f"\n--- p={p:.6f}, m={m} (L=10) ---")
    print("dense even top4:", np.round(ev["even"][:4], 6))
    print("dense odd  top4:", np.round(ev["odd"][:4], 6))
    for key in [("even", 0), ("even", 1), ("even", 2), ("odd", 0),
                ("odd", 1), ("odd", 2)]:
        print(f"    closed {key}: {cands[key]:.6f}")

print("\n\nX_L = L ln(lam1/lam_cand) at p_c  (sigma target 2*pi*b/4=0.942,"
      " epsilon 2*pi*2b=7.54)")
beta_d = 3.0 / 5.0
for L in [8, 16, 32, 64, 128, 256, 512]:
    m = L // 2
    Kd, Kh, W0 = consts(D, pc)[:3]
    cands = candidate_products(m, Kd, Kh, W0)
    l1 = cands[("even", 0)]
    row = "  ".join(
        f"{cnd[0]}{cnd[1]}:{L * np.log(l1 / cands[cnd]):7.3f}"
        for cnd in [("odd", 0), ("odd", 1), ("odd", 2), ("even", 1),
                    ("even", 2)])
    print(f"    L={L:4d}  {row}")

# Houtappel quadrature check at p=0.40 (bulk target 0.683844659)
def f_houtappel(K1, K2, K3, ngrid=1024):
    t = 2 * np.pi * (np.arange(ngrid) + 0.5) / ngrid
    c1, c2 = np.cos(t), np.cos(t)
    s3t = np.cos(np.add.outer(t, t))
    ch1, ch2, ch3 = np.cosh(2 * K1), np.cosh(2 * K2), np.cosh(2 * K3)
    sh1, sh2, sh3 = np.sinh(2 * K1), np.sinh(2 * K2), np.sinh(2 * K3)
    bracket = (ch1 * ch2 * ch3 + sh1 * sh2 * sh3
               - sh1 * c1[:, None] - sh2 * c2[None, :] - sh3 * s3t)
    dt = 2 * np.pi / ngrid
    return np.log(2.0) + (np.log(bracket).sum() * dt * dt) / (8 * np.pi ** 2)


print("\nHoutappel at p=0.40 (bulk lambda_inf target 0.683844659):")
Kd, Kh, W0 = consts(D, 0.40)[:3]
for ng in [512, 1024, 2048, 4096]:
    fH = f_houtappel(Kd, Kd, Kh, ngrid=ng)
    print(f"    ngrid={ng:5d}: {np.exp(np.log(W0) + fH):.9f}")

# Kaufman large-L as thermodynamic proxy at 0.40:
for L in [256, 1024, 4096]:
    m = L // 2
    cands = candidate_products(m, *consts(D, 0.40)[:3])
    print(f"    Kaufman L={L}: {cands[('even', 0)] ** (1.0 / L):.9f}")
