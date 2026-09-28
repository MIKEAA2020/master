#!/usr/bin/env python3
"""
Task 8-b: THE n=4 RECORD-PHASE BOUNDARY (exact Weingarten machinery, d=2).

Order 2 of the current session: "the n=4 boundary (~0.383)".

Manuscript targets (quantum-circuits v22, sec:n4n5, d=2):
  crossings:  (L=4,6) 0.35820, (6,8) 0.37899, (8,10) 0.3823  ->  p_c^(4) ~ 0.383
  drift:      0.0208 -> 0.0033 between successive pairs
  R(p*=0.383) = ln(l1/lsig)/ln(l1/leps): 0.1315/0.1829/0.2142/0.2378 (L=4,6,8,10)
               two-term marginal fit R = 1/4 - 0.90/lnL + 0.46/ln^2 L (res <= 8e-4)
  multiplet (L=8, p=0.36): triv > std*std (9x) > two*two (4x) > std*sgn (9x)
               > sgn*sgn (1x), second triv (eps) below all spin multiplets,
               L*ln(l1/leps) = 5.2
  slope:      dX_L/dp = C L^{3/2} (1 + 0.45/ln L)  (q=4 marginal, 1/nu = 3/2)
  p=0: 24-fold eigenvalue 1;  p=1: rank one, lambda = (4/35)^L
       [= (n! d^2 / Z_4)^L, Z_4 = sum_sigma 4^{c(sigma)} = 840]

Machinery (all n-generic, validated bottom-up):
  W_{p,n}(pi|mu,nu) = sum_sigma Wg_{d^2}(pi^-1 sigma) T(sigma,mu) T(sigma,nu)
  T(sigma,mu) = (1-p) d^{c(sigma^-1 mu)} + p d
  M1[pi,sigma] = prod_k W[pi_k | sigma_k, sigma_{k+1}]  (ring over m = L/2 bonds)
  A = G^{1/2} M1 G^{-1/2}   (per-bond Gram G(pi,sigma) = d^{2 c(pi^-1 sigma)})
  Op = A A^T  (symmetric PSD, same nonzero spectrum as the one-period operator)
  iterative ring contraction (BLAS GEMM sweeps) for m=2..5;
  isotypic (S4 x S4) sectors via group-averaged start vectors;
  validations: sweep vs dense (m=2), n=2 vs exact Ising, n=3 vs manuscript
  anchors (0.836807/0.834268/0.831750 at L=6, p=0.02, 1+4+1 pattern).

Stages: V (validation) -> S (scan L=4,6,8) -> M5 (L=10, float32) -> F (figure).
Checkpoints written to pscan_n4_results.json after every stage.
"""
import json
import sys
import time
import itertools

import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh
from scipy.interpolate import CubicSpline

D = 2
OUT_JSON = "/home/z/my-project/scripts/pscan_n4_results.json"
OUT_PNG = "/home/z/my-project/download/pscan_n4_boundary.png"
SEED = 7

STAGES = sys.argv[1] if len(sys.argv) > 1 else "VSMF"

results = {}


def save():
    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=1, default=float)


def log(*a):
    print(*a)
    sys.stdout.flush()


# ================= permutation machinery (n-generic) =================
def perm_compose(a, b):
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


def cycle_type(a):
    """sorted tuple of cycle lengths."""
    seen = [False] * len(a)
    out = []
    for i in range(len(a)):
        if not seen[i]:
            ln = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = a[j]
                ln += 1
            out.append(ln)
    return tuple(sorted(out))


class PermGroup:
    def __init__(self, n):
        self.n = n
        self.perms = list(itertools.permutations(range(n)))
        self.idx = {p: i for i, p in enumerate(self.perms)}
        self.cycles = np.array([n_cycles(p) for p in self.perms])
        self.cmul = {}
        for i, p in enumerate(self.perms):
            for j, q in enumerate(self.perms):
                self.cmul[(i, j)] = self.idx[perm_compose(p, q)]
        N = len(self.perms)
        self.Cinv = np.zeros((N, N), dtype=int)
        for i, p in enumerate(self.perms):
            ip = self.idx[perm_inv(p)]
            for j in range(N):
                self.Cinv[i, j] = self.cmul[(ip, j)]
        # left/right multiplication index maps
        self.mapL = np.zeros((N, N), dtype=int)   # mapL[a, i] = idx(a * p_i)
        self.mapR = np.zeros((N, N), dtype=int)   # mapR[b, i] = idx(p_i * b)
        for a, p in enumerate(self.perms):
            for i, q in enumerate(self.perms):
                self.mapL[a, i] = self.cmul[(a, i)]
                self.mapR[a, i] = self.cmul[(i, a)]


# character tables: classes -> list of (size, centralizer, chars per irrep)
# irrep order fixed below; CHI[name] gives values per class.
def class_tables(n):
    if n == 2:
        # classes: e (1), trans (1)
        return {
            "classes": [tuple([1, 1]), tuple([2])],
            "size": [1, 1],
            "cent": [2, 1],
            "CHI": {"triv": [1, 1], "sgn": [1, -1]},
            "dims": {"triv": 1, "sgn": 1},
        }
    if n == 3:
        # classes: e(1), trans(3), 3cyc(2)
        return {
            "classes": [tuple([1, 1, 1]), tuple(sorted([2, 1])), tuple([3])],
            "size": [1, 3, 2],
            "cent": [6, 2, 3],
            "CHI": {"triv": [1, 1, 1], "std": [2, 0, -1], "sgn": [1, -1, 1]},
            "dims": {"triv": 1, "std": 2, "sgn": 1},
        }
    if n == 4:
        # classes: e(1), (12)(6), (12)(34)(3), (123)(8), (1234)(6)
        # (cycle lengths sorted ascending, matching cycle_type())
        return {
            "classes": [(1, 1, 1, 1), (1, 1, 2), (2, 2), (1, 3), (4,)],
            "size": [1, 6, 3, 8, 6],
            "cent": [24, 4, 8, 3, 4],
            "CHI": {
                "triv": [1, 1, 1, 1, 1],
                "sgn": [1, -1, 1, 1, -1],
                "two": [2, 0, 2, -1, 0],
                "std": [3, 1, -1, 0, -1],
                "stdsgn": [3, -1, -1, 0, 1],
            },
            "dims": {"triv": 1, "sgn": 1, "two": 2, "std": 3, "stdsgn": 3},
        }
    raise ValueError(n)


def gram_centralizers(n):
    """Z_n = sum_sigma (d^2)^{c(sigma)} for the p=1 rank-one anchor."""
    N = np.arange(1, n + 1)
    tot = 0
    for p in itertools.permutations(range(n)):
        tot += (D * D) ** n_cycles(p)
    return tot


# ================= Weingarten channel (n-generic) =================
def weingarten_gram(Sg, d):
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


def bond_W(Sg, d, p, dtype=np.float64):
    G, Ginv = weingarten_gram(Sg, d)
    T = site_map_T(Sg, d, p)
    W = np.einsum("ps,sm,sn->pmn", Ginv, T, T)
    return W.astype(dtype), G.astype(dtype)


def gram_sqrt(Sg, d, dtype=np.float64):
    G, _ = weingarten_gram(Sg, d)
    ev, V = np.linalg.eigh(G)
    gh = (V * np.sqrt(np.maximum(ev, 0))) @ V.T
    gm = (V / np.sqrt(np.maximum(ev, 1e-300))) @ V.T
    return G.astype(dtype), gh.astype(dtype), gm.astype(dtype)


# ================= BLAS ring-contraction sweeps =================
def apply_M1(V, W, m):
    """(M1 V)[pi_1..pi_m] = sum_sigma prod_k W[pi_k|sigma_k, sigma_{k+1}] (ring).
    V: tensor (N,)*m on sigma legs. Returns tensor (N,)*m on pi legs."""
    N = W.shape[0]
    if m == 2:
        return np.einsum("pab,qba,ab->pq", W, W, V, optimize=True)
    # step 1: C[pi_1, sig_1, sig_2, sig_3..sig_m] = W[pi_1,sig_1,sig_2]*V
    Wr = W.reshape((N, N, N) + (1,) * (m - 2))
    Vr = V.reshape((1,) + (N,) * m)
    C = Wr * Vr
    del Vr
    # steps k = 2..m-1
    for k in range(2, m):
        # canonical C axes: pi_1..pi_{k-1}, sig_1, sig_k, sig_{k+1},
        #                   sig_{k+2}..sig_m   (m+1 legs)
        # regroup to (sig_k, sig_{k+1}, REST)
        perm = [k, k + 1] + list(range(0, k - 1)) + [k - 1] + list(range(k + 2, m + 1))
        Ct = np.ascontiguousarray(C.transpose(perm)).reshape(N, N, -1)
        R = Ct.shape[2]
        T = np.empty((N, N, R), dtype=V.dtype)
        for l in range(N):
            np.matmul(W[:, :, l], Ct[:, l, :], out=T[l])
        del C, Ct
        # T axes: [sig_{k+1}, pi_k, REST=(pi_1..pi_{k-1}, sig_1, sig_{k+2}..sig_m)]
        nrest = (k - 1) + 1 + (m - k - 1)
        Tr = T.reshape((N, N) + (N,) * nrest)
        del T
        # target: pi_1..pi_k, sig_1, sig_{k+1}, sig_{k+2}..sig_m
        perm2 = (list(range(2, 2 + k - 1)) + [1] + [2 + k - 1] + [0]
                 + list(range(2 + k, m + 1)))
        C = Tr.transpose(perm2)
        del Tr
    # final bond m: W_m[pi_m, sig_m, sig_1]
    Cf = np.ascontiguousarray(C).reshape(-1, N * N)      # (pi's, sig_1, sig_m) flat
    Wt = W.transpose(0, 2, 1).reshape(N, N * N)          # (pi_m, sig_1, sig_m) flat
    U = Cf @ Wt.T
    return U.reshape((N,) * (m - 1) + (N,))


def apply_M1_T(V, W, m):
    """(M1^T V)[sig_1..sig_m] = sum_pi prod_k W[pi_k|sig_k, sig_{k+1}] V[pi].
    V: tensor (N,)*m on pi legs. Returns tensor (N,)*m on sigma legs."""
    N = W.shape[0]
    if m == 2:
        return np.einsum("pab,qba,pq->ab", W, W, V, optimize=True)
    # step 1
    C = np.tensordot(W, V, axes=(0, 0))     # (sig_1, sig_2, pi_2..pi_m)
    for k in range(2, m):
        # canonical axes: sig_1..sig_k, pi_k, pi_{k+1}..pi_m
        # axes: [0..k-1]=sig_1..sig_k, [k]=pi_k, [k+1..m]=pi_{k+1}..pi_m
        perm = [k - 1, k] + list(range(0, k - 1)) + list(range(k + 1, m + 1))
        Ct = np.ascontiguousarray(C.transpose(perm)).reshape(N, N, -1)
        R = Ct.shape[2]
        T = np.empty((N, R, N), dtype=V.dtype)
        for s in range(N):
            np.matmul(Ct[s].T, W[:, s, :], out=T[s])
        del C, Ct
        # T axes: [sig_k=s, REST=(sig_1..sig_{k-1}, pi_{k+1}..pi_m), sig_{k+1}]
        nrest = (k - 1) + (m - k)
        Tr = T.reshape((N,) + (N,) * nrest + (N,))
        del T
        # target: sig_1..sig_{k+1}, pi_{k+1}..pi_m
        perm2 = (list(range(1, 1 + k - 1)) + [0] + [m] + list(range(k, m)))
        C = Tr.transpose(perm2)
        del Tr
    # final: out[sig_1..sig_m] = sum_{pi_m} C[sig_1..sig_m, pi_m] W[pi_m, sig_m, sig_1]
    # C axes: [sig_1..sig_m, pi_m]
    a = C.transpose(0, m - 1, m, *range(1, m - 1))       # (sig_1, sig_m, pi_m, MID..)
    Wa = W.transpose(2, 1, 0)                            # (sig_1, sig_m, pi_m)
    out = np.einsum("abj...,abj->a...b", a, Wa, optimize=True)
    return out


def per_axis(V, M, m):
    """contract every axis with matrix M: T'_{..., i_k, ...} = sum_j M[i_k, j] T_{..., j, ...}"""
    T = V
    for k in range(m):
        T = np.moveaxis(np.tensordot(M, T, axes=([1], [k])), 0, k)
    return T


# ================= sector-safe Lanczos =================
def lanczos_sector(matvec, v0, k=1, max_steps=60, tol=1e-9, cycles=3,
                    project=None, proj_every=1):
    """Lanczos with full reorthogonalization, restarted only from the
    sector's own top Ritz vector, with periodic exact re-projection onto
    the isotypic sector.  Two failure modes of generic solvers are closed:
    (a) ARPACK pads the basis with random vectors once the Krylov space
    exhausts the small invariant sector (escapes the sector outright);
    (b) plain Lanczos normalizes by the shrinking residual beta, which
    amplifies out-of-sector rounding noise by 1/beta per step until the
    global top emerges as a spurious Ritz value.  Periodic exact projection
    kills (b); Ritz-restart-only kills (a)."""
    dtype = v0.dtype
    v = v0 / np.linalg.norm(v0)
    n = v0.shape[0]
    vals = None
    for cyc in range(cycles):
        V = np.zeros((max_steps, n), dtype=dtype)
        alphas = np.zeros(max_steps)
        betas = np.zeros(max(max_steps - 1, 1))
        V[0] = v
        j = 0
        for j in range(max_steps):
            w = matvec(V[j])
            alphas[j] = float(np.dot(V[j], w))
            w = w - alphas[j] * V[j]
            if j > 0:
                w = w - betas[j - 1] * V[j - 1]
            for _ in range(2):  # full reorthogonalization (twice)
                w = w - V[:j + 1].T @ (V[:j + 1] @ w)
            if project is not None and (j % proj_every == proj_every - 1):
                w = project(w)
                w = w - V[:j + 1].T @ (V[:j + 1] @ w)
            bn = float(np.linalg.norm(w))
            if j + 1 < max_steps:
                betas[j] = bn
            if bn < 1e-12 * max(1.0, abs(alphas[j])):
                break  # happy breakdown: invariant subspace exhausted
            if j + 1 < max_steps:
                V[j + 1] = w / bn
        jj = j + 1
        T = np.diag(alphas[:jj])
        for i in range(jj - 1):
            T[i, i + 1] = betas[i]
            T[i + 1, i] = betas[i]
        tvals, tvecs = np.linalg.eigh(T)
        order = np.argsort(tvals)[::-1]
        kk = min(k, jj)
        vals = [float(x) for x in tvals[order][:kk]]
        if jj < max_steps or jj < 2:  # breakdown -> converged
            y = tvecs[:, order[0]]
            x = V[:jj].T @ y
            if project is not None:
                x = project(x)
            return vals, (x / np.linalg.norm(x)).astype(dtype)
        res = [betas[jj - 2] * abs(tvecs[order[i], jj - 1])
               for i in range(kk)]
        if all(r < tol * max(1.0, abs(vv)) for r, vv in zip(res, vals)):
            y = tvecs[:, order[0]]
            x = V[:jj].T @ y
            if project is not None:
                x = project(x)
            return vals, (x / np.linalg.norm(x)).astype(dtype)
        # restart from the top Ritz vector (stays in the sector)
        y = tvecs[:, order[0]]
        x = V[:jj].T @ y
        if project is not None:
            x = project(x)
        v = (x / np.linalg.norm(x)).astype(dtype)
    return vals, v


# ================= operator and sectors =================
class Problem:
    def __init__(self, n, m, dtype=np.float64):
        self.Sg = PermGroup(n)
        self.n = n
        self.m = m
        self.N = len(self.Sg.perms)
        self.dtype = dtype
        self.dim = self.N ** m
        self.G, self.gh, self.gm = gram_sqrt(self.Sg, D, dtype)
        self.tab = class_tables(n)
        self.cls_of = [self.tab["classes"].index(cycle_type(p))
                       for p in self.Sg.perms]
        rng = np.random.default_rng(SEED)
        self.starts = {}
        self.starts["triv"] = np.ones(self.dim, dtype=dtype)
        for name in self.tab["CHI"]:
            if name == "triv":
                continue
            if name == "stdsgn":
                # mixed sector std (left) x sgn (right), the manuscript's
                # "std*sgn ninefold" -- NOT the [211] irrep on both sides
                continue
            v = rng.standard_normal(self.dim).astype(dtype)
            self.starts[name] = self._project(v, name, name)
        if n == 4:
            v = rng.standard_normal(self.dim).astype(dtype)
            self.starts["stdsgn"] = self._project(v, "std", "sgn")
        self.last = {}

    def _take_lr(self, V, amap):
        """relabel every axis x -> perms[amap[x]] (gather per axis)."""
        T = V
        for k in range(self.m):
            T = T.take(amap, axis=k)
        return T

    def _project(self, v, rho, rho2):
        """project onto the (rho x rho2) isotypic component of the diagonal
        S_n x S_n action sigma_k -> a sigma_k b (P = P_L^rho P_R^rho2)."""
        f = self.tab["dims"][rho]
        f2 = self.tab["dims"][rho2]
        chi = self.tab["CHI"][rho]
        chi2 = self.tab["CHI"][rho2]
        N = self.N
        V = v.reshape((N,) * self.m)
        # left
        acc = np.zeros_like(V)
        for a in range(N):
            w = chi[self.cls_of[a]]
            if w == 0:
                continue
            acc += w * self._take_lr(V, self.Sg.mapL[a])
        acc *= (f / (N * 1.0))
        # right
        acc2 = np.zeros_like(V)
        for b in range(N):
            w = chi2[self.cls_of[b]]
            if w == 0:
                continue
            acc2 += w * self._take_lr(acc, self.Sg.mapR[b])
        acc2 *= (f2 / (N * 1.0))
        return acc2.reshape(-1)

    def matvec(self, v, W):
        """Op = A A^T with A = G^{1/2} M1 G^{-1/2} (symmetric PSD)."""
        m, N = self.m, self.N
        V = v.reshape((N,) * m)
        # A^T v = Gm M1^T Gh v
        w = per_axis(V, self.gh, m)
        w = apply_M1_T(w, W, m)
        w = per_axis(w, self.gm, m)
        # A w = Gh M1 Gm w
        u = per_axis(w, self.gm, m)
        u = apply_M1(u, W, m)
        u = per_axis(u, self.gh, m)
        return u.reshape(-1)

    def solve(self, p, sectors, kmap=None, tol=1e-9, warm=True,
              max_steps=None, cycles=3):
        """top eigenvalues per isotypic sector at monitoring rate p
        (sector-safe Lanczos with periodic exact re-projection)."""
        W, _ = bond_W(self.Sg, D, p, self.dtype)
        out = {}
        mv = lambda v: self.matvec(v, W)
        if max_steps is None:
            max_steps = 60 if self.dim < 10**6 else 24
        if self.dim <= 20000:
            proj_every = 1
        elif self.dim <= 500000:
            proj_every = 3
        else:
            proj_every = 5
        for sec in sectors:
            k = (kmap or {}).get(sec, 1)
            pair = ("std", "sgn") if sec == "stdsgn" else (sec, sec)
            proj = lambda x: self._project(x, pair[0], pair[1])
            if warm and sec in self.last:
                v0 = self.last[sec].astype(self.dtype)
            else:
                v0 = self.starts[sec].copy()
            vals, vec = lanczos_sector(mv, v0, k=k, max_steps=max_steps,
                                       tol=tol, cycles=cycles,
                                       project=proj, proj_every=proj_every)
            self.last[sec] = vec.astype(self.dtype)
            out[sec] = vals
        return out


# ================= dense reference (validation) =================
def dense_M1(Sg, W, m):
    from functools import reduce
    N = len(Sg.perms)
    dim = N ** m
    M1 = np.zeros((dim, dim))
    for si in range(dim):
        sig = []
        x = si
        for k in range(m - 1, -1, -1):
            sig.append(x % N)
            x //= N
        sig = sig[::-1]
        vs = [W[:, sig[k], sig[(k + 1) % m]] for k in range(m)]
        col = reduce(np.multiply.outer, vs)
        M1[:, si] = col.reshape(-1)
    return M1


def dense_A(Sg, W, m, gh, gm):
    M1 = dense_M1(Sg, W, m)
    Gh = np.eye(1)
    Gm = np.eye(1)
    for _ in range(m):
        Gh = np.kron(Gh, gh)
        Gm = np.kron(Gm, gm)
    return Gh @ M1 @ Gm


# ================= stage V: validation =================
def stage_V():
    log("=" * 72)
    log("STAGE V: VALIDATION (sweeps, n=2 Ising, n=3 anchors, n=4 exact)")
    log("=" * 72)
    val = {}

    # V.1  n=4, m=2: sweep vs dense
    Sg4 = PermGroup(4)
    for p in [0.02, 0.36, 0.5]:
        W, _ = bond_W(Sg4, D, p)
        G, gh, gm = gram_sqrt(Sg4, D)
        rng = np.random.default_rng(3)
        V = rng.standard_normal((24, 24))
        U1 = apply_M1(V, W, 2)
        U2 = apply_M1_T(V, W, 2)
        M1d = dense_M1(Sg4, W, 2)
        d1 = np.max(np.abs(U1 - (M1d @ V.reshape(-1)).reshape(24, 24)))
        d2 = np.max(np.abs(U2 - (M1d.T @ V.reshape(-1)).reshape(24, 24)))
        log(f"  m=2 sweep vs dense @p={p}: |M1-M1d|={d1:.2e}, "
            f"|M1T-M1d.T|={d2:.2e}")
        val[f"dense_m2_p{p}"] = [float(d1), float(d2)]
    # V.2  n=4, m=3: sweep vs direct einsum ring reference
    W, _ = bond_W(Sg4, D, 0.36)
    rng = np.random.default_rng(4)
    V = rng.standard_normal((24, 24, 24))
    U1 = apply_M1(V, W, 3)
    U1ref = np.einsum("pab,qbc,rca,abc->pqr", W, W, W, V, optimize=True)
    d1 = np.max(np.abs(U1 - U1ref))
    U2 = apply_M1_T(V, W, 3)
    U2ref = np.einsum("pab,qbc,rca,pqr->abc", W, W, W, V, optimize=True)
    d2 = np.max(np.abs(U2 - U2ref))
    log(f"  m=3 sweep vs einsum @p=0.36: dev M1={d1:.2e}, M1T={d2:.2e}")
    val["dense_m3"] = [float(d1), float(d2)]

    # V.3  n=4, m=2: Op top-2 vs dense svd(A)^2; commutation with S4xS4
    pr = Problem(4, 2)
    W, _ = bond_W(Sg4, D, 0.36)
    opv = pr.matvec(np.ones(576), W)
    Ad = dense_A(Sg4, W, 2, pr.gh, pr.gm)
    sv = np.linalg.svd(Ad, compute_uv=False)
    eigs = np.linalg.eigvalsh(Ad @ Ad.T)
    lam_iter = eigs[-1]
    # power-iterate Op for top eigenvalue
    v = np.ones(576)
    for _ in range(200):
        w = pr.matvec(v, W)
        nv = np.linalg.norm(w)
        v2 = w / nv
        if np.linalg.norm(v2 - v / np.linalg.norm(v)) < 1e-13:
            v = v2
            break
        v = v2
    lam_pw = v @ pr.matvec(v, W)
    log(f"  m=2: svd(A)^2 top = {sv[0]**2:.12f}, eig(AA^T) = "
        f"{eigs[-1]:.12f}, power(Op) = {lam_pw:.12f}")
    val["op_vs_dense_m2"] = float(lam_pw - sv[0] ** 2)
    # commutation: Op(R v) = R(Op v) with the DIAGONAL action
    # sigma_k -> a sigma_k b on every bond simultaneously
    rng = np.random.default_rng(5)
    v = rng.standard_normal(576)
    a, b = 5, 9
    map_ab = [pr.Sg.cmul[(a, pr.Sg.cmul[(i, b)])] for i in range(24)]
    map_ab = np.array(map_ab)
    Rv = v.reshape(24, 24).take(map_ab, axis=0).take(map_ab, axis=1)
    lhs = pr.matvec(Rv.reshape(-1), W).reshape(24, 24)
    rhs = pr.matvec(v, W).reshape(24, 24)
    rhs = rhs.take(map_ab, axis=0).take(map_ab, axis=1)
    dc = np.max(np.abs(lhs - rhs))
    log(f"  commutation [Op, R(a,b)] (m=2, diagonal): {dc:.2e}")
    val["commutation_m2"] = float(dc)

    # V.4  n=2 vs exact Ising
    sys.path.insert(0, "/home/z/my-project/scripts")
    import pscan_n2 as ps2
    pr2 = Problem(2, 4)
    devs = []
    for p in [0.05, 0.16, 0.233679, 0.30, 0.45, 0.60, 0.999]:
        W2, _ = bond_W(pr2.Sg, D, p)
        vals = pr2.solve(p, ["triv"], kmap={"triv": 1}, warm=False,
                         tol=1e-12)
        lam = vals["triv"][0]
        Kd, Kh, W0 = ps2.consts(D, p)[:3]
        ln1, _, _ = ps2.kaufman_log_lambdas(4, Kd, Kh, W0, p=p)
        devs.append(abs(np.log(lam) - ln1))
        log(f"  n=2 Ising check p={p}: ln lam dev = {devs[-1]:.2e}")
    val["n2_ising_max_dev"] = float(max(devs))

    # V.5  n=3 manuscript anchors (L=6, p=0.02)
    pr3 = Problem(3, 3)
    W3, _ = bond_W(pr3.Sg, D, 0.02)
    vals = pr3.solve(0.02, ["triv", "std", "sgn"], warm=False, tol=1e-12)
    a_triv, a_std, a_sgn = (vals["triv"][0], vals["std"][0],
                            vals["sgn"][0])
    log(f"  n=3 anchors L=6 p=0.02: triv={a_triv:.6f} [0.836807], "
        f"std={a_std:.6f} [0.834268], sgn={a_sgn:.6f} [0.831750]")
    val["n3_anchors"] = {k: float(v[0]) for k, v in vals.items()}
    # full top-8 (1+4+1 pattern) -- random start to reach all sectors
    op = LinearOperator((216, 216), matvec=lambda v: pr3.matvec(v, W3))
    vtop = np.random.default_rng(6).standard_normal(216)
    vals8, _ = eigsh(op, k=8, which="LA", v0=vtop, tol=1e-12)
    vals8 = np.sort(vals8)[::-1]
    log(f"  n=3 full top-8: {np.round(vals8, 6)}  [1+4+1 pattern]")
    val["n3_top8"] = [float(x) for x in vals8]

    # V.6  n=4 endpoints: p=0 (24-fold at 1), p=1 (rank one (4/35)^L)
    W0, _ = bond_W(Sg4, D, 0.0)
    pr0 = Problem(4, 2)
    Op2 = np.zeros((576, 576))
    for i in range(576):
        e = np.zeros(576)
        e[i] = 1.0
        Op2[:, i] = pr0.matvec(e, W0)
    ev0 = np.linalg.eigvalsh(Op2)
    mult2 = int(np.sum(np.abs(ev0 - 1.0) < 1e-9))
    log(f"  n=4 p=0 (L=4, dense): top={ev0[-1]:.12f}, multiplicity of 1:"
        f" {mult2}  [manuscript: n!=24-fold]")
    pr3m = Problem(4, 3)
    lam_top0 = pr3m.solve(0.0, ["triv"], kmap={"triv": 2}, warm=False,
                          tol=1e-12)["triv"]
    log(f"  n=4 p=0 (L=6): triv top = {lam_top0[0]:.12f}")
    val["n4_p0"] = {"top_L4_dense": float(ev0[-1]), "mult_at_1_L4": mult2,
                    "top_L6": float(lam_top0[0])}
    Z4 = gram_centralizers(4)
    for L in [4, 6, 8]:
        m = L // 2
        prm = Problem(4, m)
        W1, _ = bond_W(Sg4, D, 1.0)
        vv = np.ones(prm.dim)
        for _ in range(300):
            w = prm.matvec(vv, W1)
            nv = np.linalg.norm(w)
            if nv < 1e-30:
                break
            vv2 = w / nv
            if np.linalg.norm(vv2 - vv) < 1e-13:
                vv = vv2
                break
            vv = vv2
        lam1 = float(vv @ prm.matvec(vv, W1))
        tgt = (24 * D * D / Z4) ** L
        log(f"  n=4 p=1 L={L}: lam1={lam1:.6e}  [(4/35)^L={tgt:.6e}]"
            f"  ratio={lam1 / tgt:.8f}")
        val.setdefault("n4_p1", {})[str(L)] = {
            "lam": lam1, "target": tgt, "ratio": lam1 / tgt}
    log(f"  Z_4(d^2=4) = {Z4}  [840]")
    val["Z4"] = int(Z4)

    # V.7  Burnside triv-sector dims (orbit counts) for m=2..5
    sizes = class_tables(4)["size"]
    cents = class_tables(4)["cent"]
    burns = {}
    for m in range(2, 6):
        nb = sum(s * s * c ** m for s, c in zip(sizes, cents)) // 576
        burns[m] = nb
    log(f"  Burnside triv-sector dims (m=2..5): {burns}  [5, 43, 681, 14491]")
    val["burnside_triv"] = {str(k): int(v) for k, v in burns.items()}

    results["validation"] = val
    save()
    ok = (max(devs) < 1e-9 and abs(a_triv - 0.836807) < 2e-6
          and abs(a_std - 0.834268) < 2e-6
          and abs(a_sgn - 0.831750) < 2e-6 and mult2 >= 24)
    log(f"VALIDATION {'PASS' if ok else 'CHECK'}")
    return ok


# ================= stage S: scan at L=4,6,8 =================
def X_of(lam1, lam_sig, L):
    return L * np.log(lam1 / lam_sig)


def stage_S():
    log("=" * 72)
    log("STAGE S: THE n=4 CROSSING SCAN (L=4,6,8; float64)")
    log("=" * 72)
    grid = list(np.round(np.arange(0.30, 0.45 + 1e-9, 0.0025), 6))
    if 0.383 not in grid:
        grid.append(0.383)
        grid = sorted(grid)
    scan = {"grid": [float(x) for x in grid]}
    Xs = {}
    lam_store = {}
    grids = {}
    for L in [4, 6, 8]:
        m = L // 2
        pr = Problem(4, m)
        t0 = time.time()
        if L == 8:
            gL = sorted(set([round(x, 6) for x in
                             [0.33, 0.34, 0.35, 0.36, 0.37, 0.375, 0.378,
                              0.381, 0.383, 0.385, 0.388, 0.39, 0.395,
                              0.40, 0.42]]))
            grids[L] = gL
        else:
            gL = grid
            grids[L] = grid
        rows = []
        if L <= 6:
            for p in gL:
                vals = pr.solve(p, ["triv", "std"],
                                kmap={"triv": 2, "std": 1})
                l1, leps = vals["triv"][0], vals["triv"][1]
                lsig = vals["std"][0]
                rows.append((p, l1, leps, lsig))
        else:
            # warm k=1 solves for the curves (fast); leps only at the
            # R-ratio point p* = 0.383 with a fresh k=2 solve
            for p in gL:
                vals = pr.solve(p, ["triv", "std"],
                                kmap={"triv": 1, "std": 1})
                rows.append((p, vals["triv"][0], None, vals["std"][0]))
            vals = pr.solve(0.383, ["triv"], kmap={"triv": 2},
                            warm=False, tol=1e-10)
            for i, r in enumerate(rows):
                if abs(r[0] - 0.383) < 1e-12:
                    rows[i] = (r[0], r[1], vals["triv"][1], r[3])
        Xs[L] = np.array([X_of(r[1], r[3], L) for r in rows])
        lam_store[L] = {"l1": [r[1] for r in rows],
                        "leps": [r[2] for r in rows],
                        "lsig": [r[3] for r in rows]}
        results["scan_partial"] = {
            "grids": {str(k): [float(x) for x in grids[k]] for k in grids},
            "Xs": {str(k): [float(x) for x in Xs[k]] for k in Xs},
            "lams": {str(k): lam_store[k] for k in lam_store}}
        save()
        j = gL.index(0.383)
        log(f"  L={L}: {len(gL)} pts in {time.time()-t0:.0f}s; "
            f"X(0.383)={Xs[L][j]:.4f}, X({gL[0]})={Xs[L][0]:.4f}, "
            f"X({gL[-1]})={Xs[L][-1]:.4f}")
    # crossings via spline + bisection
    spl = {L: CubicSpline(grids[L], Xs[L]) for L in Xs}

    def cross(L1, L2):
        f = lambda t: spl[L1](t) - spl[L2](t)
        lo = max(grids[L1][0], grids[L2][0]) + 1e-6
        hi = min(grids[L1][-1], grids[L2][-1]) - 1e-6
        gg = np.arange(lo, hi, 0.0002)
        vv = f(gg)
        for i in range(len(gg) - 1):
            if (vv[i] > 0) != (vv[i + 1] > 0):
                a, b, fa = gg[i], gg[i + 1], vv[i]
                for _ in range(60):
                    mid = 0.5 * (a + b)
                    fm = f(mid)
                    if (fm > 0) == (fa > 0):
                        a, fa = mid, fm
                    else:
                        b = mid
                return 0.5 * (a + b)
        return None

    cr = {}
    for pair in [(4, 6), (6, 8)]:
        c = cross(*pair)
        cr[str(pair).replace(" ", "")] = c
        log(f"  crossing {pair}: {c:.6f}")
    ms = {"(4,6)": 0.35820, "(6,8)": 0.37899}
    for k, v in ms.items():
        log(f"    manuscript: {k} -> {v}  (dev {abs(cr[k]-v):.2e})")
    # R ratio at p*=0.383
    R = {}
    for L in [4, 6, 8]:
        ls = lam_store[L]
        j = grids[L].index(0.383)
        assert ls["leps"][j] is not None
        R[L] = np.log(ls["l1"][j] / ls["lsig"][j]) / np.log(
            ls["l1"][j] / ls["leps"][j])
    log(f"  R(0.383): L=4 {R[4]:.4f} [0.1315], L=6 {R[6]:.4f} [0.1829], "
        f"L=8 {R[8]:.4f} [0.2142]")
    # two-term marginal fit over available sizes
    Ls = np.array([4, 6, 8], float)
    y = np.array([R[L] for L in [4, 6, 8]])
    Afit = np.stack([np.ones_like(Ls), 1 / np.log(Ls), 1 / np.log(Ls) ** 2], 1)
    coef, *_ = np.linalg.lstsq(Afit, y, rcond=None)
    log(f"  R fit: 1/4 target; fit R = {coef[0]:.4f} {coef[1]:+.3f}/lnL "
        f"{coef[2]:+.3f}/ln^2L  [ms: 1/4 - 0.90/lnL + 0.46/ln^2L]")
    # multiplet ordering at L=8, p=0.36
    pr8 = Problem(4, 4)
    mult = pr8.solve(0.36, ["triv", "std", "two", "stdsgn", "sgn"],
                     kmap={"triv": 2})
    l1, leps = mult["triv"][0], mult["triv"][1]
    log(f"  multiplet L=8 p=0.36: triv={l1:.6f} > std={mult['std'][0]:.6f} "
        f"> two={mult['two'][0]:.6f} > stdsgn={mult['stdsgn'][0]:.6f} "
        f"> sgn={mult['sgn'][0]:.6f}; eps={leps:.6f} "
        f"(below all spin? {leps < mult['sgn'][0]})")
    log(f"    L ln(l1/leps) = {8*np.log(l1/leps):.2f}  [manuscript: 5.2]")
    # chi4 curvature peaks (kink sharpening)
    chi = {}
    for L in [4, 6, 8]:
        f = np.array([np.log(x) / L for x in lam_store[L]["l1"]])
        c2 = np.gradient(np.gradient(f, grids[L]), grids[L])
        i = int(np.argmax(c2))
        chi[L] = {"p_peak": float(grid[i]), "height": float(c2[i])}
        log(f"  chi4 L={L}: peak p={grid[i]:.4f} height={c2[i]:.4f}")
    # slope exponent at p* = 0.383: dX/dp ~ C L^{3/2}(1+0.45/lnL)
    slopes = {}
    for L in [4, 6, 8]:
        slopes[L] = float(spl[L](0.383, 1))
    Ls = np.log([4, 6, 8])
    ys = np.log([abs(slopes[L]) for L in [4, 6, 8]])
    b, a = np.polyfit(Ls, ys, 1)
    log(f"  slope exponent at p*=0.383: {b:.3f}  [q=4 target 3/2]; "
        f"slopes { {k: round(v,3) for k,v in slopes.items()} }")
    scan.update({
        "crossings": {k: (v if v is None else float(v))
                      for k, v in cr.items()},
        "R_at_0383": {str(k): float(v) for k, v in R.items()},
        "R_fit": [float(x) for x in coef],
        "multiplet_L8_p036": {k: v for k, v in mult.items()},
        "Lln_l1leps_L8": float(8 * np.log(l1 / leps)),
        "chi4": chi,
        "slope_exponent_0383": float(b),
        "slopes_0383": {str(k): v for k, v in slopes.items()},
        "Xs": {str(L): [float(x) for x in Xs[L]] for L in Xs},
        "grids": {str(L): [float(x) for x in grids[L]] for L in grids},
        "lams": {str(L): lam_store[L] for L in lam_store},
    })
    results["scan"] = scan
    save()
    return grid, Xs, spl


# ================= stage M5: L=10 leg (float32) =================
def stage_M5(grid, Xs, spl):
    log("=" * 72)
    log("STAGE M5: THE L=10 LEG (m=5, bond space 24^5 = 7,962,624; float32)")
    log("=" * 72)
    L = 10
    m = 5
    pr = Problem(4, 5, dtype=np.float32)
    pts = [0.376, 0.379, 0.381, 0.383, 0.385, 0.388]
    rows = []
    t0 = time.time()
    for p in pts:
        if abs(p - 0.383) < 1e-12:
            vals = pr.solve(p, ["triv", "std"], kmap={"triv": 2, "std": 1},
                            tol=3e-6, warm=False)
            leps = vals["triv"][1]
        else:
            vals = pr.solve(p, ["triv", "std"], kmap={"triv": 1, "std": 1},
                            tol=3e-6)
            leps = None
        l1, lsig = vals["triv"][0], vals["std"][0]
        X = X_of(l1, lsig, L)
        rows.append((p, l1, leps, lsig, X))
        log(f"  L=10 p={p}: l1={l1:.8f} lsig={lsig:.8f}  X={X:.4f}   "
            f"[{time.time()-t0:.0f}s]")
    # (8,10) crossing by spline on the L=10 curve vs L=8 spline
    spl10 = CubicSpline([r[0] for r in rows], [r[4] for r in rows])
    f = lambda t: spl[8](t) - spl10(t)
    gg = np.arange(rows[0][0], rows[-1][0], 0.0002)
    vv = f(gg)
    cr810 = None
    for i in range(len(gg) - 1):
        if (vv[i] > 0) != (vv[i + 1] > 0):
            a, b, fa = gg[i], gg[i + 1], vv[i]
            for _ in range(60):
                mid = 0.5 * (a + b)
                fm = f(mid)
                if (fm > 0) == (fa > 0):
                    a, fa = mid, fm
                else:
                    b = mid
            cr810 = 0.5 * (a + b)
            break
    log(f"  crossing (8,10): {cr810}  [manuscript: 0.3823]")
    # R at 0.383 for L=10
    R10 = None
    j = min(range(len(rows)), key=lambda i: abs(rows[i][0] - 0.383))
    if abs(rows[j][0] - 0.383) < 1e-9 and rows[j][2] is not None:
        r = rows[j]
        R10 = float(np.log(r[1] / r[3]) / np.log(r[1] / r[2]))
        log(f"  R(0.383) L=10: {R10:.4f}  [manuscript: 0.2378]")
    # float64 spot check at p=0.383 (single power sweep, if memory allows)
    log("  float64 spot-check at p=0.383 (memory permitting)...")
    try:
        pr64 = Problem(4, 5, dtype=np.float64)
        W64, _ = bond_W(pr64.Sg, D, 0.383, np.float64)
        v = pr64.starts["triv"].copy()
        for _ in range(80):
            w = pr64.matvec(v, W64)
            nv = np.linalg.norm(w)
            v2 = w / nv
            if np.linalg.norm(v2 - v) < 1e-12:
                v = v2
                break
            v = v2
        lam64 = float(v @ pr64.matvec(v, W64))
        j32 = min(range(len(rows)), key=lambda i: abs(rows[i][0] - 0.383))
        log(f"    l1 float64 = {lam64:.10f} vs float32 = "
            f"{rows[j32][1]:.10f}  (dev {abs(lam64-rows[j32][1]):.2e})")
        results.setdefault("scan", {})["L10_float64_l1"] = lam64
    except MemoryError:
        log("    float64 spot-check skipped (MemoryError)")
    # slope exponent incl. L=10
    slopes = {L: float(spl[L](0.383, 1)) for L in [4, 6, 8]}
    slopes[10] = float(spl10(0.383, 1))
    Ls = np.log([4, 6, 8, 10])
    ys = np.log([abs(slopes[L]) for L in [4, 6, 8, 10]])
    b, a = np.polyfit(Ls, ys, 1)
    log(f"  slope exponent (L=4..10) at 0.383: {b:.3f} [target 3/2]")
    # full 4-point R fit
    if R10 is not None:
        Ls = np.array([4, 6, 8, 10], float)
        y = np.array([results["scan"]["R_at_0383"]["4"],
                      results["scan"]["R_at_0383"]["6"],
                      results["scan"]["R_at_0383"]["8"], R10])
        Afit = np.stack([np.ones_like(Ls), 1 / np.log(Ls),
                         1 / np.log(Ls) ** 2], 1)
        coef, *_ = np.linalg.lstsq(Afit, y, rcond=None)
        res = y - Afit @ coef
        log(f"  R fit (4 pts): {coef[0]:.4f} {coef[1]:+.3f}/lnL "
            f"{coef[2]:+.3f}/ln^2L, max residual {np.max(np.abs(res)):.1e}"
            f"  [ms: 1/4 -0.90/lnL +0.46/ln^2L, resid <= 8e-4]")
        results["scan"]["R_fit_4pt"] = [float(x) for x in coef]
        results["scan"]["R_fit_4pt_maxres"] = float(np.max(np.abs(res)))
    results["scan"].update({
        "L10_rows": [[float(x) for x in r] for r in rows],
        "crossing_8_10": None if cr810 is None else float(cr810),
        "R10_0383": None if R10 is None else float(R10),
        "slope_exponent_4_10": float(b),
        "slopes_0383_L10": {str(k): v for k, v in slopes.items()},
    })
    save()
    return rows, spl10


# ================= stage F: figure =================
def stage_F():
    log("=" * 72)
    log("STAGE F: FIGURE")
    log("=" * 72)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if "scan" not in results:
        results.update(json.load(open(OUT_JSON)))
    sc = results["scan"]
    grid = np.array(sc["grid"])
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4),
                             constrained_layout=True)
    ax = axes[0]
    colors = {4: "#b3541e", 6: "#3a6b8f", 8: "#5a8f3a", 10: "#7d3a8f"}
    for L in [4, 6, 8]:
        gx = sc.get("grids", {}).get(str(L), sc["grid"])
        ax.plot(gx, sc["Xs"][str(L)], lw=1.6, color=colors[L],
                label=f"$X_L$, $L={L}$")
    if "L10_rows" in sc:
        xs = [row[0] for row in sc["L10_rows"]]
        ys = [row[4] for row in sc["L10_rows"]]
        ax.plot(xs, ys, "o-", ms=3.5, lw=1.6, color=colors[10],
                label=r"$X_L$, $L=10$ (float32)")
    def spl_pair(Ls, v):
        # value of the X_L curves at their intersection point v
        L1, L2 = Ls
        if str(L1) in sc.get("Xs", {}) and str(L1) in sc.get("grids", {}):
            return float(CubicSpline(sc["grids"][str(L1)],
                                     sc["Xs"][str(L1)])(v))
        return 0.0
    for pair, L1L2 in [("(4,6)", (4, 6)), ("(6,8)", (6, 8)),
                       ("(8,10)", (8, 10))]:
        tgt = {("(4,6)"): 0.35820, ("(6,8)"): 0.37899,
               ("(8,10)"): 0.3823}[pair]
        v = (sc.get("crossing_8_10") if pair == "(8,10)"
             else sc["crossings"].get(pair))
        ax.axvline(tgt, color="gray", ls=":", lw=1.0, alpha=0.8)
        if v:
            ystar = spl_pair(L1L2, v)
            ax.plot([v], [ystar], "kx", ms=8, mew=2, zorder=6)
            ax.annotate(f"{v:.4f}", (v, ystar), textcoords="offset points",
                        xytext=(6, 8), fontsize=9, color="k")
    ax.axhline(0, color="gray", lw=0.8)
    ax.set_xlabel(r"monitoring rate $p$")
    ax.set_ylabel(r"$X_L = L\,\ln(\lambda_1/\lambda_\sigma)$")
    ax.set_title(r"$n=4$ record-phase boundary: crossing ladder"
                 "\n" r"[manuscript $p_c^{(4)}\approx 0.383$]")
    ax.legend(fontsize=9, loc="upper right")
    ax.set_xlim(0.30, 0.45)
    ax.grid(alpha=0.25)

    ax = axes[1]
    Rm = {4: 0.1315, 6: 0.1829, 8: 0.2142, 10: 0.2378}
    Ls = np.array([4, 6, 8], float)
    Rv = [sc["R_at_0383"][str(int(L))] for L in Ls]
    if sc.get("R10_0383") is not None:
        Ls = np.array([4, 6, 8, 10], float)
        Rv = Rv + [sc["R10_0383"]]
    ax.plot(np.log(Ls), Rv, "o", color="#b3541e", ms=7, zorder=5,
            label="this scan")
    ax.plot(np.log([4, 6, 8, 10]), [Rm[L] for L in [4, 6, 8, 10]], "s",
            mfc="none", color="#3a6b8f", ms=7, label="manuscript")
    Lc = np.linspace(np.log(3.6), np.log(11.5), 100)
    if sc.get("R_fit_4pt"):
        c = sc["R_fit_4pt"]
    else:
        c = sc["R_fit"]
    ax.plot(Lc, c[0] + c[1] / Lc + c[2] / Lc ** 2, "--", color="gray",
            lw=1.4, label=r"fit $R=a-b/\ln L+c/\ln^2 L$")
    ax.axhline(0.25, color="k", ls=":", lw=1.2)
    ax.text(np.log(3.7), 0.253, r"$q=4$ target $x_\sigma/x_\varepsilon=1/4$",
            fontsize=9)
    ax.set_xlabel(r"$\ln L$")
    ax.set_ylabel(r"$R=\ln(\lambda_1/\lambda_\sigma)/"
                  r"\ln(\lambda_1/\lambda_\varepsilon)$")
    ax.set_title("marginal $q=4$ amplitude ratio at $p^*=0.383$\n"
                 "(log-slow convergence)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.25)

    fig.savefig(OUT_PNG, dpi=170)
    log(f"  figure -> {OUT_PNG}")
    results["figure"] = OUT_PNG
    save()


if __name__ == "__main__":
    t00 = time.time()
    ok = True
    grid = Xs = spl = None
    if "V" in STAGES:
        ok = stage_V()
    if "S" in STAGES and ok:
        grid, Xs, spl = stage_S()
    if "M" in STAGES and ok:
        if grid is None:
            sc = results["scan"]
            grid = sc["grid"]
            Xs = {int(k): np.array(v) for k, v in sc["Xs"].items()}
            spl = {int(k): CubicSpline(grid, v)
                   for k, v in Xs.items()}
        stage_M5(grid, Xs, spl)
    if "F" in STAGES:
        stage_F()
    log(f"TOTAL {time.time()-t00:.0f}s")
