#!/usr/bin/env python3
"""
Task 7-b: The record-phase p-scan at n=3 (exact Weingarten bond channel).

Construction (qc_v22, prop:general-n(iii) + thm:general-n):
  T_p(sigma,tau)   = (1-p) d^{c(sigma^-1 tau)} + p d          [site map]
  W_{p,3}(pi|mu,nu)= sum_sigma Wg_{d^2}(pi^-1 sigma) T(sigma,mu) T(sigma,nu)
      Wg_{d^2} = inverse of Gram G(pi,sigma) = (d^2)^{c(pi^-1 sigma)}
  Compressed operator C^(3) = K_e J_o K_o J_e on even-bond labels (S_3)^m:
      (C y)_pi = sum_sigma prod_k W(pi_k | sigma_k, sigma_{k+1})
                           * prod_k W(sigma_k | y_{k-1}, y_k)
  Symmetric solver: eigenvalues of C = eigenvalues of A A^T,
      A = G^{1/2} M1 G^{-1/2},  M1[pi,sigma] = prod_k W(pi_k|sigma_k,sigma_{k+1}),
      per-bond Gram g(sigma,tau) = d^{2 c(sigma^-1 tau)}.

Validation anchors (manuscript, d=2):
  L=6, p=0.02: top levels 0.836807 (triv), 0.834268 (4-fold std*std),
               0.831750 (sgn)
  p=1: rank one, lambda = [6/(5*6)]^L = (1/5)^L
  rank: L=4 -> 21, L=6 -> 216, L=8 -> 1202   (r_3(L) formula)
  n=2 cross-check: the same pipeline at n=2 must reproduce the Ising
  lambdas exactly (validates the W-table before trusting n=3).

Scan: X_L^{(3)}(p) = L ln(lambda_triv / lambda_std); crossing ladder
L=4,6,8 (dense) -> p_c^{(3)} (manuscript: 0.305(3)).
"""
import json
import itertools
import numpy as np

D = 2
OUT_JSON = "/home/z/my-project/scripts/pscan_n3_results.json"


# ---------------- permutation machinery ----------------
def perm_compose(a, b):
    """(a o b)(x) = a[b[x]]  with perms as tuples."""
    return tuple(a[bx] for bx in b)


def perm_inv(a):
    inv = [0] * len(a)
    for i, ai in enumerate(a):
        inv[ai] = i
    return tuple(inv)


def n_cycles(a):
    seen = [False] * len(a)
    cnt = 0
    for i in range(len(a)):
        if not seen[i]:
            cnt += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = a[j]
    return cnt


class PermGroup:
    def __init__(self, n):
        self.n = n
        self.perms = list(itertools.permutations(range(n)))
        self.idx = {p: i for i, p in enumerate(self.perms)}
        self.cycles = np.array([n_cycles(p) for p in self.perms])
        self.cmul = {}      # (i,j) -> index of perms[i]*perms[j]
        for i, p in enumerate(self.perms):
            for j, q in enumerate(self.perms):
                self.cmul[(i, j)] = self.idx[perm_compose(p, q)]
        self.C = np.zeros((len(self.perms),) * 2)
        for (i, j), k in self.cmul.items():
            self.C[i, j] = k      # C[i,j] = index of p_i^{-1} p_j? -> fix:
        # We need index(p_i^{-1} p_j):
        self.Cinv = np.zeros_like(self.C)
        for i, p in enumerate(self.perms):
            ip = self.idx[perm_inv(p)]
            for j in range(len(self.perms)):
                self.Cinv[i, j] = self.cmul[(ip, j)]


S3 = PermGroup(3)
S2 = PermGroup(2)


def weingarten_gram(Sg, d):
    """G(pi,sigma) = (d^2)^{c(pi^-1 sigma)}; returns G and G^{-1}."""
    N = len(Sg.perms)
    G = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            k = int(Sg.Cinv[i, j])
            G[i, j] = (d * d) ** Sg.cycles[k]
    return G, np.linalg.inv(G)


def site_map_T(Sg, d, p):
    N = len(Sg.perms)
    T = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            k = int(Sg.Cinv[i, j])
            T[i, j] = (1 - p) * d ** Sg.cycles[k] + p * d
    return T


def bond_W(Sg, d, p):
    """W[pi, mu, nu] = sum_sigma Wg(pi^-1 sigma) T(sigma,mu) T(sigma,nu)."""
    G, Ginv = weingarten_gram(Sg, d)
    T = site_map_T(Sg, d, p)
    N = len(Sg.perms)
    W = np.einsum('ps,sm,sn->pmn', Ginv, T, T)
    return W, G


# ---------------- chain construction ----------------
def decode(i, m, N):
    out = []
    x = i
    for k in range(m - 1, -1, -1):
        out.append(x % N)
        x //= N
    return out[::-1]


def build_M1(Sg, W, m):
    """M1[pi, sigma] = prod_k W(pi_k | sigma_k, sigma_{k+1}), ring.
    Column for sigma = outer product over bonds k of W[:, sig_k, sig_{k+1}]."""
    from functools import reduce
    N = len(Sg.perms)
    dim = N ** m
    M1 = np.zeros((dim, dim))
    for si in range(dim):
        sig = decode(si, m, N)
        vs = [W[:, sig[k], sig[(k + 1) % m]] for k in range(m)]
        col = reduce(np.multiply.outer, vs)     # shape (N,)*m
        M1[:, si] = col.reshape(-1)
    return M1


def build_M2(Sg, W, m):
    """M2[sigma, y] = prod_k W(sigma_k | y_{k-1}, y_k), ring."""
    from functools import reduce
    N = len(Sg.perms)
    dim = N ** m
    M2 = np.zeros((dim, dim))
    for yi in range(dim):
        y = decode(yi, m, N)
        vs = [W[:, y[(k - 1) % m], y[k]] for k in range(m)]
        # W[tau | y_{k-1}, y_k] as a vector over sigma_k:
        # W[mu, nu, pi] with mu=y_{k-1}, nu=y_k -> vector index pi
        col = reduce(np.multiply.outer, vs)
        M2[:, yi] = col.reshape(-1)
    return M2


def gram_sqrt_chain(Sg, d, m, sign):
    """per-bond g^{sign*1/2} as (N^m x N^m) matrix = kron of 6x6."""
    G, _ = weingarten_gram(Sg, d)
    ev, V = np.linalg.eigh(G)
    g = V @ np.diag(np.exp(sign * 0.5 * np.log(np.maximum(ev, 1e-300)))) @ V.T
    M = np.eye(N_dim(Sg, m))
    for _ in range(m):
        M = np.kron(M, g)
    return M


def N_dim(Sg, m):
    return len(Sg.perms) ** m


def top_eigs_chain(Sg, d, p, m, k=8):
    """eigenvalues of C = svals(A)^2, A = G^{1/2} M1 G^{-1/2}; top k."""
    W, G = bond_W(Sg, d, p)
    M1 = build_M1(Sg, W, m)
    N = len(Sg.perms)
    ev, V = np.linalg.eigh(G)
    gh = V @ np.diag(np.sqrt(np.maximum(ev, 0))) @ V.T
    gm = V @ np.diag(1.0 / np.sqrt(np.maximum(ev, 1e-300))) @ V.T
    Gh = np.eye(1)
    Gm = np.eye(1)
    for _ in range(m):
        Gh = np.kron(Gh, gh)
        Gm = np.kron(Gm, gm)
    A = Gh @ M1 @ Gm
    sv = np.linalg.svd(A, compute_uv=False)
    return sv[:k] ** 2, sv[:k]


# ---------------- n=2 cross-validation ----------------
def n2_check():
    print("n=2 cross-validation of the pipeline (W-table -> chain -> Ising):")
    import pscan_n2 as ps2
    devs = []
    for m in [3, 4]:
        for p in [0.05, 0.16, 0.20, ps2.PC, 0.30, 0.40, 0.60]:
            W2, G2 = bond_W(S2, D, p)
            M1 = build_M1(S2, W2, m)
            N = len(S2.perms)
            ev, V = np.linalg.eigh(G2)
            gh = V @ np.diag(np.sqrt(np.maximum(ev, 0))) @ V.T
            gm = V @ np.diag(1.0 / np.sqrt(np.maximum(ev, 1e-300))) @ V.T
            Gh = np.eye(1); Gm = np.eye(1)
            for _ in range(m):
                Gh = np.kron(Gh, gh); Gm = np.kron(Gm, gm)
            A = Gh @ M1 @ Gm
            sv = np.linalg.svd(A, compute_uv=False)
            lam = sv[0] ** 2
            # compare with the Ising lambda_1 (per period, L = 2m):
            Kd, Kh, W0 = ps2.consts(D, p)[:3]
            ln1, lns, lne = ps2.kaufman_log_lambdas(m, Kd, Kh, W0, p=p)
            devs.append(abs(np.log(lam) - ln1))
    print(f"   max |ln lam1(chain) - ln lam1(Ising)| = {max(devs):.2e}")
    return max(devs)


# ---------------- isotypic classification (S_3 x S_3) ----------------
CHI3 = {  # S3 character table: [triv, std, sgn]
    "triv": [1, 1, 1], "std": [2, 0, -1], "sgn": [1, -1, 1]}
CLASS_OF = [0, 1, 1, 1, 2, 2]  # e; 3 transpositions (class 1); 2 3-cycles
# S3 perms list order from itertools: (012),(013... let's compute properly:
def s3_class(p):
    c = n_cycles(p)
    return {3: 0, 2: 1, 1: 2}[c]  # 3 cycles=id, 2 cycles=transposition, 1 cycle=3-cycle


def isotypic_projector(Sg, m, lam_name):
    """P_{lam lam} on bond labels: (d_lam^2/36) sum_{a,b} chi(a)chi(b) R(a,b)
    where R(a,b) acts as tau_k -> a tau_k b on every bond."""
    chi = CHI3[lam_name]
    dl = {"triv": 1, "std": 2, "sgn": 1}[lam_name]
    N = len(Sg.perms)
    dim = N ** m
    P = np.zeros((dim, dim))
    for ai, a in enumerate(Sg.perms):
        ca = s3_class(a)
        for bi, b in enumerate(Sg.perms):
            cb = s3_class(b)
            w = chi[ca] * chi[cb]
            if w == 0:
                continue
            # action: label sigma_k -> a sigma_k b (compose)
            # build index map
            idxmap = np.zeros(dim, dtype=int)
            for si in range(dim):
                x = si
                sig = []
                for k in range(m - 1, -1, -1):
                    sig.append(x % N)
                    x //= N
                sig = sig[::-1]
                y = 0
                for k in range(m):
                    y = y * N + Sg.cmul[(ai, Sg.cmul[(sig[k], bi)])]
                idxmap[si] = y
            P += w * np.eye(dim)[idxmap]
    return (dl * dl / 36.0) * P


def chain_blocks(d, p, m, cache={}):
    """top eigenvalue in triv, std, sgn isotypic blocks of C.
    p-independent projectors and Gram sqrts cached per m."""
    if m not in cache:
        N = len(S3.perms)
        G, _ = weingarten_gram(S3, d)
        ev, V = np.linalg.eigh(G)
        gh = V @ np.diag(np.sqrt(np.maximum(ev, 0))) @ V.T
        gm = V @ np.diag(1.0 / np.sqrt(np.maximum(ev, 1e-300))) @ V.T
        Gh = np.eye(1)
        Gm = np.eye(1)
        for _ in range(m):
            Gh = np.kron(Gh, gh)
            Gm = np.kron(Gm, gm)
        projs = {}
        for lam in ["triv", "std", "sgn"]:
            P = isotypic_projector(S3, m, lam)
            # orthonormal basis of the block range
            w, Uv = np.linalg.eigh(P)
            keep = w > 0.5
            projs[lam] = Uv[:, keep]
        cache[m] = (Gh, Gm, projs)
    Gh, Gm, projs = cache[m]
    W, G = bond_W(S3, d, p)
    M1 = build_M1(S3, W, m)
    A = Gh @ M1 @ Gm
    out = {}
    for lam in ["triv", "std", "sgn"]:
        Uv = projs[lam]
        B = Uv.T @ A @ Uv
        sv = np.linalg.svd(B, compute_uv=False)
        out[lam] = sv[0] ** 2
    return out, A


# =====================================================================
if __name__ == "__main__":
    results = {}
    print("=" * 72)
    print("n=3 RECORD-PHASE P-SCAN (Weingarten bond channel, d=2)")
    print("=" * 72)

    # 0. n=2 cross-validation
    dev2 = n2_check()
    results["n2_cross_validation_max_dev"] = float(dev2)

    # 1. W-table sanity: negative entries at small p
    W, G = bond_W(S3, D, 0.0)
    nneg = int(np.sum(W < -1e-12))
    Wmin = W.min()
    print(f"\nW-table at p=0: {nneg} negative entries (manuscript: twelve "
          f"of 216), min = {Wmin:.3f} (manuscript: e.g. -0.10)")
    results["W_neg_entries_p0"] = {"count": nneg, "min": float(Wmin)}

    # 2. anchors: L=6, p=0.02 top levels
    lam, _ = chain_blocks(D, 0.02, 3)
    print(f"\nanchors at L=6, p=0.02: triv={lam['triv']:.6f} "
          f"[0.836807], std={lam['std']:.6f} [0.834268], "
          f"sgn={lam['sgn']:.6f} [0.831750]")
    results["anchor_L6_p002"] = {k: float(v) for k, v in lam.items()}

    # full-spectrum top eigenvalues (degeneracy pattern 1+4+1):
    ev, sv = top_eigs_chain(S3, D, 0.02, 3, k=8)
    print("   full spectrum top-8:", np.round(ev, 6))
    results["anchor_L6_p002_full_top8"] = ev.tolist()

    # 3. p=1 rank-one + (1/5)^L
    for L in [4, 6, 8]:
        ev, sv = top_eigs_chain(S3, D, 1.0, L // 2, k=3)
        target = (1.0 / 5.0) ** L
        print(f"   p=1, L={L}: lam1 = {ev[0]:.8e}  [(1/5)^L = {target:.8e}]"
              f"  lam2/lam1 = {ev[1] / ev[0]:.2e}")
    # 4. ranks
    ranks = {}
    for L in [4, 6, 8]:
        ev, sv = top_eigs_chain(S3, D, 0.30, L // 2, k=200000)
        rk = int(np.sum(sv > 1e-9 * sv[0]))
        ranks[L] = rk
    print(f"   ranks at p=0.30: {ranks}  [formula: L=4->21, L=6->216,"
          f" L=8->1202]")
    results["ranks_p030"] = ranks

    # 5. THE SCAN: crossing ladder for X_L^{(3)} = L ln(lam_triv/lam_std)
    print("\nTHE n=3 CROSSING SCAN:")
    scan = {}
    grid = np.arange(0.26, 0.40, 0.0025)
    Xs = {}
    for L in [4, 6, 8]:
        m = L // 2
        X = []
        for p in grid:
            lam, _ = chain_blocks(D, p, m)
            X.append(L * np.log(lam["triv"] / lam["std"]))
        Xs[L] = np.array(X)
        print(f"   X_{L}: p=0.28 -> {Xs[L][8]:.4f}, p=0.31 -> "
              f"{Xs[L][20]:.4f}, p=0.36 -> {Xs[L][40]:.4f}")

    # crossings via cubic-spline interpolation of the X_L curves
    from scipy.interpolate import CubicSpline
    splines = {L: CubicSpline(grid, Xs[L]) for L in Xs}

    def cross_n3(L1, L2):
        f = lambda t: splines[L1](t) - splines[L2](t)
        gg = np.arange(0.26, 0.40, 0.0002)
        vals = f(gg)
        for i in range(len(gg) - 1):
            if (vals[i] > 0) != (vals[i + 1] > 0):
                a, b = gg[i], gg[i + 1]
                fa = vals[i]
                for _ in range(50):
                    mid = 0.5 * (a + b)
                    fm = f(mid)
                    if (fm > 0) == (fa > 0):
                        a, fa = mid, fm
                    else:
                        b = mid
                return 0.5 * (a + b)
        return None

    crossings = {}
    for pair in [(4, 6), (6, 8)]:
        crossings[str(pair)] = cross_n3(*pair)
    print(f"   crossings: {crossings}  [manuscript p_c^(3) = 0.305(3)]")
    scan["crossings"] = crossings

    # extrapolation: (4,6) and (6,8) crossings + manuscript ladder context
    # 6. chi_L^{(3)} concentration (kink sharpening) on the n=3 chain
    chi3 = {}
    fine = np.arange(0.27, 0.36, 0.002)
    for L in [4, 6, 8]:
        m = L // 2
        f = []
        for p in fine:
            lam, _ = chain_blocks(D, p, m)
            f.append(np.log(lam["triv"]) / L)
        f = np.array(f)
        chi = np.gradient(np.gradient(f, fine), fine)
        j = int(np.argmax(chi))
        chi3[L] = {"p_peak": float(fine[j]), "chi_peak": float(chi[j])}
        print(f"   L={L}: chi3 peak at p={fine[j]:.4f}, "
              f"height {chi[j]:.4f}")
    scan["chi3"] = chi3
    results["scan"] = scan

    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=1, default=float)
    print(f"\nresults -> {OUT_JSON}")
