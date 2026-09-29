#!/usr/bin/env python3
"""debug_complex2.py — fast vectorized referee vs the 6x6 machinery."""
import numpy as np
import itertools
import math

rng = np.random.default_rng(3)
B = np.array([0.3 + 0.2j, -0.1 + 0.4j])
C = np.array([0.5 - 0.1j, 0.2 + 0.3j])
Aa = np.array([[0.2 + 0.1j, -0.1 + 0.15j], [0.05 - 0.2j, 0.1 + 0.05j]])
Ab = np.array([[0.3, 0.1j], [-0.1j, 0.25 + 0.05j]])


def word_matrix(w, Aa, Ab):
    M = np.eye(2, dtype=complex)
    for ch in w:
        M = M @ (Aa if ch == "a" else Ab)
    return M


def ref_norm(B, C, Aa, Ab, L):
    ws = [""]
    for k in range(1, L + 1):
        ws += ["".join(p) for p in itertools.product("ab", repeat=k)]
    # vectorize: precompute A_w for all words
    Aws = np.array([word_matrix(w, Aa, Ab) for w in ws])   # (n, 2, 2)
    n = len(ws)
    BAu = np.einsum('i,nij->nj', B, Aws)          # B A_u  (n, 2)
    AvC = np.einsum('nij,j->ni', Aws, C)          # A_v C  (n, 2)
    # g(uv) = B A_u A_v C = (B A_u) . (A_v C)
    Gm = np.einsum('ni,mi->nm', BAu, AvC)         # (n, n) = g(uv)
    pu = np.array([[w.count("a"), w.count("b")] for w in ws])
    cell = np.zeros((n, n))
    s = pu[:, None, :] + pu[None, :, :]
    cell[(s[:, :, 0] == 1) & (s[:, :, 1] == 1)] = 1.0
    M = cell - Gm
    return float(np.linalg.svd(M, compute_uv=False)[0])


for L in (7, 9, 11):
    print("referee L=%d: %.9f" % (L, ref_norm(B, C, Aa, Ab, L)))

# the machinery: rebuild the 6x6
Kc = (np.kron(np.conj(Aa), Aa) + np.kron(np.conj(Ab), Ab))
X = np.outer(C, np.conj(C))
Lc = np.linalg.solve(np.eye(4) - Kc, X.reshape(4, order="F")).reshape(2, 2, order="F")
Kr = (np.kron(Aa.T, np.conj(Aa).T) + np.kron(Ab.T, np.conj(Ab).T))
Xr = np.outer(np.conj(B), B)
Lr = np.linalg.solve(np.eye(4) - Kr, Xr.reshape(4, order="F")).reshape(2, 2, order="F")
betas = [(0, 0), (1, 0), (0, 1), (1, 1)]
G = np.zeros((6, 6), complex); Cm = np.zeros((6, 6), complex)
FBu = {}; FBv = {}
for b in betas:
    Su = np.zeros(2, complex); Sv = np.zeros(2, complex)
    for w in ["".join(p) for k in range(5) for p in itertools.product("ab", repeat=k)]:
        if (w.count("a"), w.count("b")) == b:
            Su = Su + B @ word_matrix(w, Aa, Ab)
            Sv = Sv + word_matrix(w, Aa, Ab) @ C
    FBu[b] = Su; FBv[b] = Sv
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
A = Cm @ G
ev = np.linalg.eigvals(A)
print("\nGC eigenvalues:", sorted([complex(e) for e in ev], key=lambda z: -abs(z)))
lam = max(float(np.real(e)) for e in ev)
print("max Re eig:", lam, "-> norm", math.sqrt(max(0, lam)))
# the Hermitian route: eigvals of C^{1/2} G C^{1/2}
w_, V_ = np.linalg.eigh(Cm)
C1_2 = (V_ * np.sqrt(np.clip(w_, 0, None))) @ V_.conj().T
H = C1_2 @ G @ C1_2
evH = np.linalg.eigvalsh((H + H.conj().T) / 2)
print("Hermitian route max eig:", evH[-1], "-> norm", math.sqrt(max(0, evH[-1])))
