#!/usr/bin/env python3
"""debug_complex.py — brute-force the 6x6 C and G over words and compare
with the closed forms, on a complex config, entry by entry."""
import numpy as np
import itertools
import math

# inline copies of the machinery (avoid importing the battery's top level)

rng = np.random.default_rng(3)

# a complex config with distinct scales
B = np.array([0.3 + 0.2j, -0.1 + 0.4j])
C = np.array([0.5 - 0.1j, 0.2 + 0.3j])
Aa = np.array([[0.2 + 0.1j, -0.1 + 0.15j], [0.05 - 0.2j, 0.1 + 0.05j]])
Ab = np.array([[0.3, 0.1j], [-0.1j, 0.25 + 0.05j]])

# brute force over words of length <= L (for the Grams the tails matter,
# so compare on a config where the tails are tiny... use small A's)
L = 9
words = [""]
for k in range(1, L + 1):
    words += ["".join(p) for p in itertools.product("ab", repeat=k)]


def parikh(w):
    return (w.count("a"), w.count("b"))


def word_matrix(w):
    M = np.eye(2, dtype=complex)
    for ch in w:
        M = M @ (Aa if ch == "a" else Ab)
    return M


# the basis functions on the word list
def b_i(i, u):
    return 1.0 if parikh(u) == [(0, 0), (1, 0), (0, 1), (1, 1)][i] else 0.0


def f_k(k, u):
    return (B @ word_matrix(u))[k]


# G brute force (truncated)
betas = [(0, 0), (1, 0), (0, 1), (1, 1)]
G_bf = np.zeros((6, 6), dtype=complex)
for i in range(4):
    for j in range(4):
        G_bf[i, j] = sum(b_i(i, u) * b_i(j, u) for u in words)
    for k in range(2):
        G_bf[i, 4 + k] = sum(b_i(i, u) * f_k(k, u) for u in words)
        G_bf[4 + k, i] = sum(np.conj(f_k(k, u)) * b_i(i, u) for u in words)
for k in range(2):
    for k2 in range(2):
        G_bf[4 + k, 4 + k2] = sum(np.conj(f_k(k, u)) * f_k(k2, u)
                                  for u in words)

# C brute force: c_i(v) = target coeff (real), c_{4+k}(v) = -(A_v C)_k
def c_coeff(i, v):
    if i < 4:
        pv = parikh(v)
        return 1.0 if pv == (1 - betas[i][0], 1 - betas[i][1]) else 0.0
    k = i - 4
    return -(word_matrix(v) @ C)[k]


C_bf = np.zeros((6, 6), dtype=complex)
for i in range(6):
    for j in range(6):
        C_bf[i, j] = sum(c_coeff(i, v) * np.conj(c_coeff(j, v))
                         for v in words)

# the closed forms from the machinery (rebuild inline)
Kc = (np.kron(np.conj(Aa), Aa) + np.kron(np.conj(Ab), Ab))
X = np.outer(C, np.conj(C))
Lc = np.linalg.solve(np.eye(4) - Kc, X.reshape(4, order="F")).reshape(2, 2, order="F")
Kr = (np.kron(Aa.T, np.conj(Aa).T) + np.kron(Ab.T, np.conj(Ab).T))
Xr = np.outer(np.conj(B), B)
Lr = np.linalg.solve(np.eye(4) - Kr, Xr.reshape(4, order="F")).reshape(2, 2, order="F")

print("Lc closed:\n", Lc)
print("Lc brute (2x2 block of C_bf[4:6,4:6]):\n", C_bf[4:6, 4:6])
print("Lc diff:", np.abs(Lc - C_bf[4:6, 4:6]).max())
print()
print("Lr closed:\n", Lr)
print("Lr brute (G_bf[4:6,4:6]):\n", G_bf[4:6, 4:6])
print("Lr diff:", np.abs(Lr - G_bf[4:6, 4:6]).max())

# block sums
FBu_bf = {}
FBv_bf = {}
for b in betas:
    Su = np.zeros(2, complex); Sv = np.zeros(2, complex)
    for w in words:
        if parikh(w) == b:
            Su = Su + B @ word_matrix(w)
            Sv = Sv + word_matrix(w) @ C
    FBu_bf[b] = Su
    FBv_bf[b] = Sv

G_cf = np.zeros((6, 6), complex)
C_cf = np.zeros((6, 6), complex)
for i, b in enumerate(betas):
    G_cf[i, i] = [1, 1, 1, 2][i]
    C_cf[i, i] = [2, 1, 1, 1][i]
    comp = (1 - b[0], 1 - b[1])
    for k in range(2):
        G_cf[i, 4 + k] = FBu_bf[b][k]
        G_cf[4 + k, i] = np.conj(FBu_bf[b][k])
        C_cf[i, 4 + k] = -np.conj(FBv_bf[comp][k])
        C_cf[4 + k, i] = -FBv_bf[comp][k]
G_cf[4:6, 4:6] = Lr
C_cf[4:6, 4:6] = Lc

print("\nG diff (closed vs brute, off-diagonal blocks):",
      np.abs(G_cf[:4, 4:] - G_bf[:4, 4:]).max())
print("C diff (closed vs brute, off-diagonal blocks):",
      np.abs(C_cf[:4, 4:] - C_bf[:4, 4:]).max())
print("C diag diff:", np.abs(np.diag(C_cf)[:4] - np.diag(C_bf)[:4]).max())

A = C_cf @ G_cf
ev = np.linalg.eigvals(A)
lam = max(float(np.real(e)) for e in ev)
print("\nmachinery-form norm^2 (C_cf @ G_cf):", lam)

# the dense referee inline (complex-correct)
def dense_ref(L):
    ws = [""]
    for k in range(1, L + 1):
        ws += ["".join(p) for p in itertools.product("ab", repeat=k)]
    n = len(ws)
    M = np.zeros((n, n), dtype=complex)
    for i, u in enumerate(ws):
        Mu = word_matrix(u)
        for j, v in enumerate(ws):
            Mv = word_matrix(v)
            s = (parikh(u)[0] + parikh(v)[0], parikh(u)[1] + parikh(v)[1])
            cell = 1.0 if s == (1, 1) else 0.0
            M[i, j] = cell - (B @ Mu @ Mv @ C)
    return float(np.linalg.svd(M, compute_uv=False)[0])

print("dense referee norm (L=11):", dense_ref(11))
print("dense referee norm (L=13):", dense_ref(13))
