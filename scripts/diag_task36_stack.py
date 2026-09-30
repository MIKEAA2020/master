#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diag_task36_stack.py — the anatomy of the live stack's uncertified
boxes (the 26/31 that the partial-sum certificate missed)."""
import json
import math
import sys

import numpy as np
from flint import arb

sys.path.insert(0, "/home/z/my-project/github_repos/master/scripts")

SCR = "/home/z/my-project/github_repos/master/scripts/"
LAMBDA_F = float("1.6310919765642504414737578928177383666901925754942")

# import the probe's machinery by file execution (the functions only)
src = open(SCR + "probe_task36b.py").read()
head = src.split("# ------------------------------------------------------------------\n# P-e")[0]
exec(head)

ck = json.load(open(SCR + "free_class_wall_ckpt.json"))
stack = ck["stack"]
print("the live stack: %d entries" % len(stack))
for idx, (rec, depth) in enumerate(stack):
    box = tuple(tuple(e) for e in rec)
    c = np.array([0.5 * (lo + hi) for (lo, hi) in box])
    wmax = max(b[1] - b[0] for b in box)
    Aa = np.array([[c[4], c[8]], [c[9], c[5]]])
    Ab = np.array([[c[6], c[10]], [c[11], c[7]]])
    K = np.kron(Aa, Aa) + np.kron(Ab, Ab)
    rho = max(abs(np.linalg.eigvals(K)))
    best, bN = None, None
    for N in (2, 4, 8, 16, 32):
        z1, z2 = unstable_pair_float(c, N)
        zs = list(Z_FIX) + ([z1, z2] if z1 is not None else [])
        for z in zs:
            q = cert_iv(xballs(box), z, N)
            if q is not None and (best is None or float(q) > best):
                best, bN = float(q), N
    # the float value at the center (the machinery or the formal)
    Bv, Cv = c[0:2], c[2:4]
    val, rho2 = norm_of(Bv, Cv, Aa, Ab) if 'norm_of' in dir() else (None, None)
    if val is None:
        src2 = open(SCR + "probe_task36.py").read()
        exec(src2.split("# ------------------------------------------------------------------\n# THE FLOAT PARTIAL")[0])
        val, rho2 = norm_of(Bv, Cv, Aa, Ab)
    print("stack[%2d] d=%2d w=%.1e rho=%.4f |B|=%6.1f |C|=%5.2f "
          "|A|max=%.2f val=%.4f cert=%.4f@N%d %s"
          % (idx, depth, wmax, rho, np.linalg.norm(Bv),
             np.linalg.norm(Cv), max(abs(c[4:12])), val,
             best if best is not None else float("nan"),
             bN if bN else -1,
             "PASS" if best is not None and best > LAMBDA_F else "fail"))
