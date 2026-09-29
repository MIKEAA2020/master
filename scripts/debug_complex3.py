#!/usr/bin/env python3
"""debug_complex3.py — reproduce the battery's CC-1(b) failing config."""
import numpy as np
import itertools

rng = np.random.default_rng(20260930)
# the same sequence as CC-1(b): first (a) consumed 25*4 normal draws
for _ in range(25):
    rng.normal(size=2); rng.normal(size=2)
    rng.normal(size=(2, 2)); rng.normal(size=(2, 2)) * 0.4

fails = []
for trial in range(12):
    B = rng.normal(size=2) + 1j * rng.normal(size=2)
    C = rng.normal(size=2) + 1j * rng.normal(size=2)
    Aa = rng.normal(size=(2, 2)) * 0.35 + 1j * rng.normal(size=(2, 2)) * 0.35
    Ab = rng.normal(size=(2, 2)) * 0.35 + 1j * rng.normal(size=(2, 2)) * 0.35

    # machinery (inline, the fixed version)
    Kc = (np.kron(np.conj(Aa), Aa) + np.kron(np.conj(Ab), Ab))
    rho = max(abs(np.linalg.eigvals(Kc)))
    if rho >= 1.0 - 1e-12:
        print(trial, "unstable, skip")
        continue
    X = np.outer(C, np.conj(C))
    Lc = np.linalg.solve(np.eye(4) - Kc, X.reshape(4, order="F")).reshape(2, 2, order="F")
    Kr = (np.kron(Aa.T, np.conj(Aa).T) + np.kron(Ab.T, np.conj(Ab).T))
    Xr = np.outer(np.conj(B), B)
    Lr = np.linalg.solve(np.eye(4) - Kr, Xr.reshape(4, order="F")).reshape(2, 2, order="F")
    # block sums over exact-Parikh classes (blocks (i,j) <= (1,1))
    FBu = {}; FBv = {}
    for (i, j) in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        Su = np.zeros(2, complex); Sv = np.zeros(2, complex)
        for k in range(0, 3):
            for p in itertools.product("ab", repeat=k):
                w = "".join(p)
                if (w.count("a"), w.count("b")) == (i, j):
                    M = np.eye(2, dtype=complex)
                    for ch in w:
                        M = M @ (Aa if ch == "a" else Ab)
                    Su = Su + B @ M
                    Sv = Sv + M @ C
        FBu[(i, j)] = Su; FBv[(i, j)] = Sv
    betas = [(0, 0), (1, 0), (0, 1), (1, 1)]
    G = np.zeros((6, 6), complex); Cm = np.zeros((6, 6), complex)
    for i, b in enumerate(betas):
        G[i, i] = [1, 1, 1, 2][i]
        Cm[i, i] = [2, 1, 1, 1][i]
        comp = (1 - b[0], 1 - b[1])
        for k in range(2):
            G[i, 4 + k] = FBu[b][k]
            G[4 + k, i] = np.conj(FBu[b][k])
            Cm[i, 4 + k] = -np.conj(FBv[comp][k])
            Cm[4 + k, i] = -FBv[comp][k]
    G[4:6, 4:6] = Lr
    Cm[4:6, 4:6] = Lc
    ev = np.linalg.eigvals(Cm @ G)
    lam = max(float(np.real(e)) for e in ev)
    n_mach = np.sqrt(max(0.0, lam))

    # referee (vectorized, complex-correct)
    L = 9
    ws = [""]
    for k in range(1, L + 1):
        ws += ["".join(p) for p in itertools.product("ab", repeat=k)]
    Aws = []
    for w in ws:
        M = np.eye(2, dtype=complex)
        for ch in w:
            M = M @ (Aa if ch == "a" else Ab)
        Aws.append(M)
    Aws = np.array(Aws)
    n = len(ws)
    BAu = np.einsum('i,nij->nj', B, Aws)
    AvC = np.einsum('nij,j->ni', Aws, C)
    Gm = np.einsum('ni,mi->nm', BAu, AvC)
    pu = np.array([[w.count("a"), w.count("b")] for w in ws])
    s = pu[:, None, :] + pu[None, :, :]
    cell = np.zeros((n, n))
    cell[(s[:, :, 0] == 1) & (s[:, :, 1] == 1)] = 1.0
    Mm = cell - Gm
    n_ref = float(np.linalg.svd(Mm, compute_uv=False)[0])
    rel = abs(n_mach - n_ref) / max(1.0, abs(n_ref))
    flag = "FAIL" if rel > 5e-3 else "ok"
    print("%2d  rho=%.3f  mach=%.9f  ref=%.9f  rel=%.2e  %s"
          % (trial, rho, n_mach, n_ref, rel, flag))
    if rel > 5e-3:
        fails.append((B, C, Aa, Ab, n_mach, n_ref))
if fails:
    B, C, Aa, Ab, nm, nr = fails[0]
    print("\nfirst failing config:")
    print("B =", B); print("C =", C); print("Aa =", Aa); print("Ab =", Ab)
    print("mach:", nm, " ref:", nr)
