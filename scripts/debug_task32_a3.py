#!/usr/bin/env python3
"""debug_task32_a3.py — check the 3x3 sector reduction at mirrored points."""
import math
import numpy as np

SRC = "/home/z/my-project/github_repos/master/scripts/free_cell.py"
src = open(SRC).read()
head = src[:src.index('# =====================================================================\n# PART A')]
ns = {}
exec(compile(head, 'fc_head', 'exec'), ns)
free_cell_exact_norm = ns['free_cell_exact_norm']
kron4 = ns['kron4']
lyap = ns['lyap']
lyap_T = ns['lyap_T']
BLOCKS = ns['BLOCKS']
MU = ns['MU']

def build_A(B, C, Aa, Ab):
    Lc, _ = lyap(Aa, Ab, np.outer(C, C))
    Lr, _ = lyap_T(Aa, Ab, np.outer(B, B))
    FBu, FBv = {}, {}
    for (beta, words) in BLOCKS:
        Su = np.zeros(2); Sv = np.zeros(2)
        for w in words:
            Mw = np.eye(2)
            for ch in w:
                Mw = Mw @ (Aa if ch == "a" else Ab)
            Su = Su + B @ Mw
            Sv = Sv + Mw @ C
        FBu[beta] = Su; FBv[beta] = Sv
    G = np.zeros((6, 6)); Cmat = np.zeros((6, 6))
    betas = [b for (b, _) in BLOCKS]
    for i, b in enumerate(betas):
        G[i, i] = MU[b]
        comp = (1 - b[0], 1 - b[1])
        Cmat[i, i] = MU[comp]
        for k in range(2):
            G[i, 4 + k] = FBu[b][k]; G[4 + k, i] = FBu[b][k]
            Cmat[i, 4 + k] = -FBv[comp][k]; Cmat[4 + k, i] = -FBv[comp][k]
    G[4:6, 4:6] = Lr
    Cmat[4:6, 4:6] = Lc
    return Cmat @ G, G, Cmat

c, y, x = 0.4, 0.6, 0.05
p = c / (2 * x)
B = np.array([p, -p]); Cv = np.array([1.0, 1.0])
Aa = np.diag([x, -x]); Ab = np.diag([y, y])
A, G, Cm = build_A(B, Cv, Aa, Ab)
w = np.linalg.eigvals(A)
print("6x6 spectrum:", sorted(np.round(np.real(w), 10)))
norm6 = float(math.sqrt(max(np.real(w))))
print("norm6 = %.12f  vs machinery %.12f" % (
    norm6, free_cell_exact_norm(B, Cv, Aa, Ab)[0]))

# the u_+-sector: rows/cols (1,0), (1,1), u_+
# the odd blocks are indices 1 ((1,0)) and 3 ((1,1)) in BLOCKS order
# BLOCKS = [((0,0),), ((1,0),), ((0,1),), ((1,1),)]
U = np.zeros((6, 3))
U[1, 0] = 1.0          # block (1,0)
U[3, 1] = 1.0          # block (1,1)
U[4, 2] = 1/math.sqrt(2)
U[5, 2] = 1/math.sqrt(2)
# the projection of A onto the sector: since the sector is A-invariant
# (A[odd, u_-] = 0 etc.), the sector's matrix = U^T A U with U orthonormal
A3 = U.T @ A @ U
print("\nA3 (U^T A U):")
print(np.round(A3, 6))
w3 = np.linalg.eigvals(A3)
print("A3 spectrum:", sorted(np.round(np.real(w3), 10)))

# invariance check: A U should stay in the sector
R = A @ U
resid = R - U @ A3
print("\nsector invariance residual: %.2e" % np.linalg.norm(resid))

# compare against the closed form
D = (1 - y * y) ** 2 - x ** 4
G3 = np.array([[1.0, 0.0, math.sqrt(2) * p * x],
               [0.0, 2.0, 2 * math.sqrt(2) * p * x * y],
               [math.sqrt(2) * p * x, 2 * math.sqrt(2) * p * x * y,
                2 * p * p * x * x / D]])
C3 = np.array([[1.0, 0.0, -math.sqrt(2) * y],
               [0.0, 1.0, -math.sqrt(2)],
               [-math.sqrt(2) * y, -math.sqrt(2),
                2 * (1 - y * y) / D]])
A3cf = C3 @ G3
print("closed-form A3:")
print(np.round(A3cf, 6))
print("\ndifference |A3 - A3cf| = %.3e" % np.linalg.norm(A3 - A3cf))
print("A3cf spectrum:", sorted(np.round(np.real(np.linalg.eigvals(A3cf)), 10)))
