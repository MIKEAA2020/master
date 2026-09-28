#!/usr/bin/env python3
"""Check the ([211],[211]) sector top (the manuscript's 'std*sgn ninefold')
at L=8 and L=4, p=0.36, with the deflated solver; also dense-verify at L=4."""
import numpy as np
from pscan_n4 import Problem, bond_W, D, lanczos_sector

out = []


def log(*a):
    print(*a, flush=True)


for prm, tag in [(Problem(4, 2), "L=4"), (Problem(4, 4), "L=8")]:
    W, _ = bond_W(prm.Sg, D, 0.36)
    mv = lambda v: prm.matvec(v, W)
    v = prm.starts["triv"].copy()
    v = v / np.linalg.norm(v)
    for i in range(400):
        w = mv(v)
        nw = np.linalg.norm(w)
        v2 = w / nv if (nv := np.linalg.norm(w)) > 0 else v
        if np.linalg.norm(v2 - v) < 1e-13:
            v = v2
            break
        v = v2
    lam1 = float(v @ mv(v))
    mv_d = lambda x: mv(x) - lam1 * float(x @ v) * v
    rng = np.random.default_rng(11)
    secs = [("std", ("std", "std")), ("two", ("two", "two")),
            ("stdsgn211", ("stdsgn", "stdsgn")), ("sgn", ("sgn", "sgn"))]
    log(f"{tag} p=0.36 (lam1={lam1:.8f}):")
    for name, pair in secs:
        v0 = prm._project(rng.standard_normal(prm.dim), pair[0], pair[1])
        proj = lambda x, pp=pair: prm._project(x, pp[0], pp[1])
        vals, _ = lanczos_sector(mv_d, v0, k=1, max_steps=60, tol=1e-9,
                                 project=proj, proj_every=1, cycles=3)
        log(f"   {name}: {vals[0]:.8f}")
    if prm.dim == 576:
        # dense verification
        Op = np.zeros((576, 576))
        for i in range(576):
            e = np.zeros(576)
            e[i] = 1.0
            Op[:, i] = mv(e)
        ev, vecs = np.linalg.eigh(Op)
        for name, pair in secs:
            for k in range(575, -1, -1):
                u = vecs[:, k]
                pu = prm._project(u, pair[0], pair[1])
                if np.linalg.norm(pu - u) / np.linalg.norm(u) < 1e-6:
                    log(f"   dense {name}: {ev[k]:.8f}")
                    break
