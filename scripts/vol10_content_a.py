# -*- coding: utf-8 -*-
"""vol10_content_a.py — The Rank-Defect Theorem (Vol X): chapters 1-6 +
tables + figures. All statements anchored to the session's verification
batteries (rank_defect.py, exp1_spectral.py, exp2_coarsening.py,
exp3_sheaf.py and their results JSONs)."""

FIGURES = {
    "main": ("/home/z/my-project/download/figures/rank_defect_theorem.png",
             "Figure 1 — The rank-defect theorem beyond the ring, three "
             "fronts. (a) The classification: the (arrow, visible complex "
             "mode) plane, log scale, with the exact witnesses — the "
             "driven 3-ring in the iff domain, the doubly-stochastic "
             "witness with its real spectrum {1, 2/5, -1/5} and D = "
             "(1/15) ln 3 in the hidden-arrow quadrant, the Gaussian "
             "AR(2) with its complex covariance modes and exactly zero "
             "arrow in the fake-arrow quadrant, the Laplace MA(1) and the "
             "symmetric chain — over the Birkhoff-polytope hit-and-run "
             "cloud (68.6% real spectrum: the hidden-arrow quadrant has "
             "positive measure). (b) The one-way valve and the reflection "
             "theorem: the exact block reversal KL of the observed record "
             "under the sensor lattices of the driven rings — the "
             "identity and chirality-keeping sensors keep the arrow "
             "(growing linearly in the block length), while every "
             "reflection-orbit sensor launders it to exactly zero at "
             "every block length. (c) The chat's Experiment 1, honestly "
             "run: the AAK/balanced-truncation cross-entropy against the "
             "three baselines at matched order, against the true entropy "
             "rate — the interval containment 10/10, the task knee at "
             "order 3, and the honest baseline split."),
}

TABLES = {
    "mandate": {
        "caption": "Table 1 — The order, itemized and answered: the two "
                   "links named at the close of Task 14's ledger, the "
                   "theorem package or experiment that discharges each, "
                   "its status, and its verification in this session's "
                   "batteries",
        "header": ["The ordered link", "The deliverable", "Status",
                   "Verification"],
        "ratios": [0.26, 0.34, 0.17, 0.23],
        "font": 7.3,
        "rows": [
            ["(1) The rank-defect theorem's generalization beyond the "
             "ring — which stationary processes satisfy arrow <=> rank "
             "defect",
             "The classification: T1 soundness (reversible => real "
             "spectrum, so a visible complex mode is a sound arrow "
             "witness); T2 the two failure modes with exact witnesses "
             "and the positive-measure scan; T3 the N-ring rank-doubling "
             "law (all N, the iff's natural home); T4/T4b the one-way "
             "valve (DPI) and the reflection-laundering theorem — the "
             "ring's arrow is its chirality",
             "PROVED (T1, T3, T4, T4b) and WITNESSED (T2, both failure "
             "modes, both directions)",
             "rank_defect.py: 1000/1000 reversible chains real-spectrum; "
             "the B3 hit-and-run 68.6% real-spectrum; the rational "
             "spectrum certificate exact; the rank law 6/6 for N = 3..8; "
             "the block KLs exact; the reflection theorem's kept/laundered "
             "split exact"],
            ["(2) The chat's Experiments 1-3 — the spectral compression "
             "of sequence models, the sensor-coarsening scan, the sheaf "
             "diagnostics",
             "Experiment 1 on the chat's own synthetic branch (the "
             "driven 6-ring through a 4-symbol sensor, a known-minimal "
             "WFA): the exact Gramian machinery, the AAK interval, the "
             "baseline triad. Experiment 2 on the chat's Tiger branch: "
             "the exact alpha-backup, the obstruction/register/curvature "
             "scan, the record-side exchangeability theorem. Experiment "
             "3 on the compositional split: the token-sheaf coboundary "
             "energy vs the OOD gap",
             "RUN at full audit strength; every one of the chat's "
             "quantitative predictions adjudicated honestly",
             "exp1/exp2/exp3 batteries with results JSONs: the AAK "
             "interval 10/10; the register 9 -> 9153; the exchangeability "
             "deviation below 3.5e-18; the task-level-perfect / "
             "seed-level-null split measured"],
        ],
    },
    "quadrants": {
        "caption": "Table 2 — The quadrant classification, witness by "
                   "witness: the arrow D (the exact reversal divergence), "
                   "the Hankel rank, the visible complex modes, and the "
                   "verdict for both arrow witnesses (the Task-14 rank "
                   "witness sv2 and the complex-mode witness)",
        "header": ["The witness", "Arrow D", "Hankel rank",
                   "Complex modes", "sv2-witness", "complex-witness"],
        "ratios": [0.30, 0.11, 0.11, 0.13, 0.17, 0.18],
        "font": 7.0,
        "rows": [
            ["Driven 3-ring (a=.32, b=.18), identity observable",
             "0.0596", "2", "2 (0.25±0.1212i)", "consistent (the iff "
             "domain)", "SOUND: complex => driven"],
            ["Doubly-stochastic [[.6,.4,0],[.2,.2,.6],[.2,.4,.4]]",
             "(1/15)ln3 = 0.0732", "1", "0 (spectrum {1, 2/5, -1/5} "
             "exact)", "HIDDEN ARROW (miss)", "HIDDEN ARROW (miss)"],
            ["Symmetric chain [[.5,.3,.2],[.3,.2,.5],[.2,.5,.3]]",
             "0 (detailed balance exact)", "2 (modes ±√7/10)",
             "0", "FAKE ARROW (false positive)", "silent (correctly)"],
            ["Gaussian AR(2), roots 0.8 e^{±iπ/5}",
             "0 (Toeplitz swap, error 0.0)", "2", "2",
             "FAKE ARROW (false positive)", "FAKE ARROW (the linear "
             "stratum launders)"],
            ["Laplace MA(1), x = eps - 0.7 eps'",
             "0.0182 ± 0.0004 (exact-integral MC)", "2 "
             "(finite support)", "0", "HIDDEN ARROW (miss)",
             "HIDDEN ARROW (miss)"],
            ["Gaussian AR(1) (the OU baseline, process level)",
             "0", "1", "0", "silent", "silent"],
        ],
    },
    "ringlaw": {
        "caption": "Table 3 — The N-ring rank-doubling law, N = 3..8: the "
                   "equilibrium rank (the pair-merging), the driven rank, "
                   "the defect, and the closed-form check Im lambda_j = "
                   "(a-b) sin(2 pi j / N) — the reversible slice IS the "
                   "spectral-merging locus, which is exactly why the ring "
                   "satisfies the iff",
        "header": ["N", "Equilibrium rank", "Driven rank", "Defect δ",
                   "Predicted δ", "Circulant spectrum error"],
        "ratios": [0.10, 0.21, 0.17, 0.15, 0.15, 0.22],
        "font": 8.0,
        "rows": [
            ["3", "1", "2", "1", "1", "machine-exact"],
            ["4", "2", "3", "1", "1", "machine-exact"],
            ["5", "2", "4", "2", "2", "machine-exact"],
            ["6", "3", "5", "2", "2", "machine-exact"],
            ["7", "3", "6", "3", "3", "machine-exact"],
            ["8", "4", "7", "3", "3", "machine-exact"],
        ],
    },
}

CHAPTERS_A = [
    {"title": "The mandate", "blocks": [
        ("p", "Task 14 closed on two open frontiers, and the order that "
              "opens this volume names them exactly: the rank-defect "
              "theorem's generalization beyond the ring — the question of "
              "which stationary processes actually satisfy the equivalence "
              "arrow iff rank defect that the 3-state ring exhibited — and "
              "the chat's Experiments 1 through 3, the three legs of the "
              "empirical program that the DeepSeek thread had designed "
              "and this programme had not yet run. The first is a "
              "classification problem about the mathematical objects this "
              "corpus has carried since Volume II: the arrow of time as a "
              "reversal divergence, the Hankel rank as the memory "
              "stratum, and the sensor as the record's boundary. The "
              "second is an audit problem: three experiments, each with a "
              "published prediction, each to be run at the programme's "
              "full discipline — anchor-first, exact where exactness is "
              "available, honestly labelled where it is not."),
        ("p", "The recovered chat defines the three experiments precisely "
              "(transcript lines 3497-3556). Experiment 1 hypothesizes "
              "that the Hankel singular values of a trained sequence "
              "model predict the optimal compression rate, that the "
              "AAK-optimal extraction beats pruning and distillation "
              "baselines at matched parameter count, and that the "
              "distortion-rate curve matches the sigma_{n+1} lower "
              "bounds. Experiment 2 hypothesizes that the obstruction "
              "datum of a partially observed control problem predicts "
              "when a finite-state policy fails to exist and that the "
              "viability-weighted curvature measures the severity. "
              "Experiment 3 hypothesizes that the sheaf cohomology of a "
              "network's local computations predicts training failures, "
              "with the harmonic norm correlating with the validation "
              "gap. Each of these is tested below on the branch of its "
              "own benchmark family that admits exact machinery, and "
              "each returns a split verdict that this volume records "
              "without varnish."),
        ("table", "mandate"),
        ("p", "The standing honesty discipline of the corpus applies "
              "throughout: every number below is either computed exactly "
              "in this session's batteries (rank_defect.py, "
              "exp1_spectral.py, exp2_coarsening.py, exp3_sheaf.py, all "
              "with results JSONs) or it is labelled with its estimation "
              "error. Two mid-session retractions and repairs happened "
              "during the battery construction itself — an eigenvector "
              "biorthogonality bug that briefly misclassified the driven "
              "ring, and a truncation-convention transpose that briefly "
              "produced unstable reduced models — and both were caught by "
              "the anchor discipline before any claim was read off. The "
              "machinery sections below state the certificates that were "
              "checked."),
    ]},
    {"title": "The objects and the classification", "blocks": [
        ("p", "Fix the objects once. For a stationary process X, the "
              "arrow A(X) is the time-reversal divergence: for a finite "
              "Markov chain with stationary distribution pi and "
              "transition P, the exact rate D = sum over i, j of pi_i "
              "P_ij ln(pi_i P_ij / pi_j P_ji); for a process with a "
              "finite alphabet, the exact block reversal KL sum_u p(u) "
              "ln(p(u)/p(rev u)), computable by finite sums whenever the "
              "law is finite. The rank rho(X) is the rank of the "
              "covariance Hankel [c(i+j)] of the observed process — the "
              "number of exponential modes of the autocovariance, the "
              "Kronecker-type law that Volume II's bridge theorems and "
              "Volume VII's analytic machinery have been orbiting all "
              "along. The complex count rho_C is the number of visible "
              "modes with nonzero imaginary part. Task 14's discovery on "
              "the 3-ring was sv2 > 0 iff driven; this volume asks what "
              "that equivalence really is."),
        ("p", "The answer is a classification with four quadrants and "
              "four theorems. T1 (soundness): a visible complex mode is a "
              "sound arrow witness, because reversible chains are "
              "pi-self-adjoint and therefore real-spectrum. T2 (the two "
              "failure modes): off the ring the equivalence fails in both "
              "directions — the hidden arrow, where an irreversible chain "
              "has an all-real spectrum (and the Birkhoff-polytope scan "
              "shows this quadrant has positive measure, 68.6 percent "
              "under the hit-and-run sampling), and the fake arrow, where "
              "a reversible process has complex covariance modes (the "
              "Gaussian AR(2), and the symmetric chain whose indicator "
              "sees two distinct real modes so that sv2 is positive with "
              "zero arrow). T3 (the ring, every N): the equivalence's "
              "natural home — on the N-state cyclic ring the reversible "
              "slice is exactly the spectral-merging locus, the visible "
              "rank doubles when the arrow turns on, and the iff holds "
              "for every observable except the parity-affine family. T4 "
              "and T4b (the one-way valve and the reflection theorem): "
              "sensors are coordinate-wise channels, so the observed "
              "arrow never exceeds the source arrow and a reversible "
              "source stays reversible under every sensor; and on the "
              "ring every reflection is a reversal symmetry, so every "
              "reflection-invariant sensor launders the arrow exactly."),
        ("table", "quadrants"),
        ("p", "The last row of Table 2 is the OU baseline of Task 14 "
              "returned to its process-level home: reversible, "
              "single-mode, silent. The first row is the ring in the "
              "domain where the equivalence holds; the middle four rows "
              "are the boundary cases that break it in both directions. "
              "The doubly-stochastic witness deserves its own remark: "
              "its spectrum is certified in exact rational arithmetic — "
              "the characteristic polynomial coefficients match 6/5, "
              "3/25, and -2/25 as fractions — and its arrow is exactly "
              "(1/15) ln 3, while its indicator's covariance is a single "
              "exponential (2/9)(2/5)^m, verified term by term in "
              "fractions. The record of this chain is rank 1: the arrow "
              "is completely invisible to both witnesses, not because the "
              "chain is nearly reversible but because its irreversibility "
              "is carried by the flow structure rather than the spectrum."),
    ]},
    {"title": "Theorem T1 — soundness", "blocks": [
        ("p", "The theorem: if an ergodic finite chain is reversible with "
              "respect to pi, then P is self-adjoint in the "
              "pi-weighted inner product, hence has real spectrum; "
              "therefore a visible complex eigenvalue is a sound witness "
              "of non-reversibility, and the visible complex mode of the "
              "observed process's covariance is a sound witness of the "
              "arrow. The proof is two lines — detailed balance pi_i "
              "P_ij = pi_j P_ji says exactly that the pi-symmetrized "
              "matrix is symmetric — but its contrapositive is the "
              "engine of every arrow witness this programme has used: "
              "complex spectrum implies irreversible implies D > 0. What "
              "the theorem does not say, and what the next section "
              "witnesses, is the converse."),
        ("p", "The verification is exhaustive on the sampled families. "
              "One thousand random walks on one thousand random "
              "undirected graphs (N between 3 and 8) are reversible by "
              "construction (degree stationary, detailed balance verified "
              "to a maximum violation of 8.3e-17), and every one has an "
              "all-real spectrum — the maximum imaginary part over the "
              "entire sample is 6.8e-17, machine zero. In the other "
              "direction, every sampled chain with a complex eigenvalue "
              "has strictly positive reversal KL, four thousand out of "
              "four thousand. The soundness direction is not a "
              "probabilistic statement; it is a theorem verified to "
              "exhaustion because it could not fail. The interesting "
              "mathematics lives in the two ways the converse fails, and "
              "in the exact structure that makes the ring the place "
              "where it does not fail at all."),
    ]},
    {"title": "Theorem T2 — the two failure modes", "blocks": [
        ("p", "The hidden arrow first. The witness chain of Table 2 is "
              "doubly stochastic (so the stationary distribution is "
              "uniform and the reversal KL has the clean closed form "
              "(1/15) ln 3), non-symmetric, and carries the rational "
              "spectrum {1, 2/5, -1/5}. Its indicator observable sees "
              "exactly one exponential mode, so the Hankel rank is 1 and "
              "sv2 is zero at machine precision: both the Task-14 rank "
              "witness and the refined complex-mode witness report "
              "nothing while the arrow is strictly positive. At the "
              "process level the Laplace MA(1) does the same with "
              "continuous state: its autocovariance has finite support "
              "(rank 2, all modes degenerate at zero), yet its 2-block "
              "reversal KL is 0.0182 with a standard error of 0.0004, "
              "computed by an inner integral that is exact — the "
              "log-integrand is piecewise linear in the shared "
              "innovation, so each segment integrates in closed form — "
              "and only the outer expectation is Monte Carlo. The same "
              "machinery with Gaussian innovations returns exactly zero, "
              "the classical boundary: the MA(1) is reversible if and "
              "only if its innovations are Gaussian."),
        ("p", "The fake arrow second. The symmetric chain is reversible "
              "by construction with distinct real eigenvalues "
              "{1, +sqrt(7)/10, -sqrt(7)/10}, so its indicator sees two "
              "distinct exponential modes and sv2 is strictly positive "
              "with zero arrow: the rank count is a mode count, not an "
              "arrow detector. The Gaussian AR(2) with roots "
              "0.8 exp(±i pi/5) is sharper still: its covariance Hankel "
              "has rank 2 with a genuine complex-conjugate mode pair, "
              "and its reversal KL is exactly zero — the block "
              "covariance is Toeplitz in |i-j| and therefore "
              "swap-invariant, verified to 0.0 at block lengths 2, 4, "
              "and 8. Every real stationary Gaussian process is "
              "reversible; the linear-Gaussian stratum launders the "
              "complex-mode witness exactly the way the reflection "
              "sensors launder the ring's arrow in Theorem T4b. Soundness "
              "of the complex witness is a jump-process theorem; the "
              "continuous linear stratum is exempt."),
        ("p", "And the failure is generic, not exotic. The hit-and-run "
              "sampler on the Birkhoff polytope B3 — four-dimensional, "
              "uniform-stationary chains — finds that 68.6 percent of "
              "sampled doubly-stochastic 3-state chains have an all-real "
              "spectrum with strictly positive reversal divergence, with "
              "the divergence ranging up to 1.39. For random 4-state "
              "stochastic matrices the all-real fraction is 36.8 percent. "
              "The hidden-arrow quadrant has positive measure: the "
              "equivalence arrow iff rank defect fails generically off "
              "the abelian slice, in exactly the direction the "
              "doubly-stochastic witness exemplifies. The ring was never "
              "the typical case; it was the structured case, and the "
              "next theorem says precisely what the structure is."),
    ]},
    {"title": "Theorem T3 — the ring, every N", "blocks": [
        ("p", "On the N-state cyclic ring with forward rate a, backward "
              "rate b, and self-loop 1-a-b, the transition matrix is "
              "circulant, so its spectrum is the closed form lambda_j = "
              "1-a-b+a omega^j + b omega^{-j} with omega = exp(2 pi i / "
              "N). The imaginary part is exactly (a-b) sin(2 pi j / N) — "
              "verified machine-exact for every N from 3 to 8 — so the "
              "spectrum is real if and only if a = b, and at a = b the "
              "spectrum is real and degenerate: the pairs (j, N-j) merge. "
              "This is the mechanism the 3-ring exhibited and the "
              "N-generalization makes explicit: the reversible slice is "
              "the spectral-merging locus. The observable's covariance "
              "sees one exponential per distinct eigenvalue, so the "
              "visible rank at equilibrium is floor((N-1)/2) plus one "
              "more if N is even, and the driven rank is N-1 — every "
              "pair splits into its conjugate halves. Table 3 records the "
              "law for N = 3 to 8, six of six, with the defect delta "
              "equal to floor((N-1)/2)."),
        ("table", "ringlaw"),
        ("p", "The boundary is as sharp as the law. The equivalence holds "
              "on the ring for every observable whose DFT support touches "
              "a pair (j, N-j) with j not 0 or N/2 — for odd N that is "
              "every non-constant observable. For even N the "
              "parity-affine observables, the functions of x mod 2, see "
              "only the real j = N/2 mode: their rank profile is the same "
              "at equilibrium and under driving, and the arrow is "
              "invisible to them. The parity sensor on the driven 4-ring "
              "realizes this exactly — the observed process is the "
              "flip/stay chain, reversible, block reversal KL zero at "
              "every block length to 1.7e-18 — which is not a degenerate "
              "truncation but the sharpest statement of the whole "
              "theorem: memory without the arrow, a record that keeps "
              "its correlation and loses its handedness."),
    ]},
    {"title": "Theorems T4 and T4b — the one-way valve and the reflection "
              "laundering", "blocks": [
        ("p", "The one-way valve is the data-processing inequality in the "
              "record's clothing. A sensor is a coordinate-wise channel "
              "applied to the source process; the block law of the "
              "observed record is the pushforward of the source's block "
              "law; and the KL divergence contracts under pushforward. "
              "Two consequences: the observed arrow never exceeds the "
              "source arrow (verified in exact block arithmetic at every "
              "block length on every sensor of the laundering lattices), "
              "and a reversible source stays reversible under every "
              "sensor — the lumped symmetric chain's block KL is zero at "
              "every block length, to 5.7e-18. The record cannot "
              "fabricate the arrow. It can only inherit it, degrade it, "
              "or destroy it, and the destruction has an exact "
              "characterization that the battery discovered in its own "
              "zeros."),
        ("p", "The exact zeros came first as a surprise: on the 3-ring, "
              "every single non-identity sensor launders the arrow "
              "completely — the block KL is zero at every block length "
              "for {0}|{1,2}, for {0,2}|{1}, for {0,1}|{2}, and "
              "trivially for the constant sensor. The theorem behind the "
              "zeros is the reflection-laundering theorem: if a symmetry "
              "rho of the state space conjugates the dynamics to its own "
              "time reversal (rho P rho^{-1} = the reversed chain), then "
              "every rho-invariant sensor launders the arrow exactly — "
              "the reversal of the law is the rho-conjugate of the law, "
              "and the sensor is rho-blind. On the N-ring every "
              "reflection is such a reversal symmetry, because reflecting "
              "the ring swaps clockwise and counterclockwise, which is "
              "exactly swapping a and b, which is exactly the stationary "
              "time reversal at uniform pi. So the ring's arrow is its "
              "chirality — its circulation direction — and the record "
              "loses the arrow exactly when it loses the handedness."),
        ("p", "The theorem's predictions were then tested against a "
              "designed counterexample: on the driven 4-ring, the "
              "three-block sensor {0}|{1}|{2,3} breaks all four "
              "reflections, so it is chirality-keeping and the arrow must "
              "survive — and it does, with a strictly positive block KL "
              "of 0.453 at block length 7, while both reflection-orbit "
              "controls ({0}|{1,2,3} and the two-block sensors) launder "
              "to exactly zero. Figure 1(b) shows the split: the identity "
              "and chirality-keeping sensors hold the arrow at every "
              "block length, growing linearly at the reversal rate, "
              "while the parity and half sensors sit on the axis at "
              "machine zero. The 3-ring, having no chirality-preserving "
              "coarsening other than the identity, is the minimal chiral "
              "record: its arrow survives only at full resolution. The "
              "complex pair of the rank-doubling law is the chiral mode; "
              "killing the handedness kills both."),
    ]},
]
