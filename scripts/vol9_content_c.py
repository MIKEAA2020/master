#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vol9_content_c.py — The Sandwich Locus, SECOND EDITION: the closure
chapters + the empirical face (Experiments 1-3) + the record synthesis.

The second edition's mandate (the user's order): integrate the chat's
Experiments 1-3 and the "it and bit from record" conclusion into Volume IX,
and bring the volume's own open interval — the cell's D(2) in [1.000,
1.2771] — up to date with the closure delivered in Volume XI and the
line-atom battery, plus this session's strictness chain and complex
completions.
"""

CHAPTERS_C = [
    {"title": "Second Edition Preface: The Cell Is Closed",
     "blocks": [
        ("p", "This volume's first edition closed on an honest interval: "
              "the (1,1) cell's two-state distance D(2) lay in [1.000, "
              "1.2771], the floor proved unattainable by the rank wall, "
              "the ceiling measured over the complete rank-two family, "
              "the exact value named as the smallest instance of the "
              "multinomial-weighted catalectic Adamjan-Arov-Krein "
              "problem. The second edition opens with the announcement "
              "that the interval is closed at its upper end, and closed "
              "exactly. The line-atom battery of Volume XI reduced the "
              "cell's optimum to a two-parameter boundary family — the "
              "line atom psi = c 1[gamma_1 = 1] y^gamma_2, the limit of "
              "the parity-odd mirrored pairs as the pair's separation "
              "runs to the boundary — and solved its cubic stationarity "
              "system to ninety digits: D(2) = sqrt(lambda*) = "
              "1.27714211290844623900730137526434780654. The minimal "
              "polynomial of lambda* is 108x^3 - 415x^2 + 522x - 216, "
              "irreducible over the rationals, obtained by external "
              "factoring of the degree-seventy-four eliminant and "
              "confirmed independently by factoring the saved degree-"
              "1154 resultant artifact; the minimal polynomial of D(2) "
              "itself is 108x^6 - 415x^4 + 522x^2 - 216. The value this "
              "volume could only bound is an algebraic point of degree "
              "three."),
        ("p", "The certificate is global over the line-atom family: a "
              "strip patch (the Schur identity and the pencil bound, "
              "certifying lambda_max above 1.775 for |y| beyond the strip "
              "edge), a far-c patch (the trace identity, above 10/3 for "
              "|c| at or beyond seven), and a middle bisection — two "
              "million seven hundred thousand interval boxes certified "
              "by sound Taylor-shift ball arithmetic, zero failures — "
              "with the attainment exact to 1e-91 at the stationary "
              "point (c*, y*) = (0.39710728735039737, 0.656322466995789"
              "11) and its flip. What remained open after that "
              "certificate was the bridge from the line-atom family to "
              "the full rank-two variety — the subject of the next "
              "chapter, which upgrades the numerical escape-room "
              "evidence of Volume XI to a theorem on the parity-odd "
              "shell and a sharp structural reduction on the rest."),
        ("quote", "The cell's D(2), closed. D(2) = sqrt(lambda*) where "
                  "lambda* is the unique real root of 108x^3 - 415x^2 + "
                  "522x - 216, numerically 1.6310919765642504414737578. "
                  "The value 1.27714211290844623900730137526434780654 is "
                  "attained by the line atom at (c*, y*) and its flip, "
                  "certified globally over the line-atom family by the "
                  "four-component certificate, and connected to the full "
                  "rank-two variety by the corner-reduction chain of the "
                  "next chapter: proved on the parity-odd shell, reduced "
                  "to an explicit trade-off on the general family."),
        ("stats", [("D(2) = 1.2771421129", "the closed value: sqrt of "
                    "lambda*, the cubic's root"),
                   ("108x^3-415x^2+522x-216", "lambda*'s minimal "
                    "polynomial (D(2): the degree-6 even part)"),
                   ("2,719,552 boxes · 0 failures", "the global "
                    "certificate; attainment -1.3e-91")]),
     ]},
    {"title": "The Corner Reduction: The Strictness Chain",
     "blocks": [
        ("p", "The bridge from the line atom to the full variety is "
              "built on one structural observation. The cell's Hankel "
              "H(u, v) = 1[Parikh(uv) = (1,1)] is nonzero only when the "
              "a-counts of u and v have opposite parity, so in the "
              "a-parity block decomposition of l2(A*) the target is "
              "purely off-diagonal, and for ANY approximant the error's "
              "(odd-row, even-column) block is a lower bound for the "
              "whole norm. Compress further to the CORNER — the rows "
              "with exactly one a (the words b^i a b^j) against the "
              "columns with none (the words b^k) — and the corner of "
              "the error is the Hankel matrix of the symbol 1[i+j+k = "
              "1] minus psi's corner values, a one-dimensional-looking "
              "object whose rows with i+j = n are (n+1) many words: the "
              "MULTIPLICITY-WEIGHTED one-dimensional Hankel problem. "
              "The approximant's corner is the effective one-dimensional "
              "atom sum: for psi = p_1 lambda_1^gamma + p_2 "
              "lambda_2^gamma with lambda_i = (x_i, y_i), the corner "
              "symbol is w_1 r_1^n + w_2 r_2^n with (w_i, r_i) = "
              "(p_i x_i, y_i). This transfer is exact, and the corner "
              "norm is the largest eigenvalue of a closed three-by-three "
              "or four-by-four generalized eigenproblem whose entries "
              "are rational in the effective atoms — the machinery "
              "verified against the full cell machinery to 1.8e-15 and "
              "against the dense corner referee."),
        ("p", "On the parity-odd shell the chain closes into a theorem. "
              "A gamma_1-odd-supported approximant — the mirrored pair "
              "family of Volume XI's anatomy, the class that carried the "
              "measured optimum — has vanishing diagonal blocks and its "
              "error's (odd, even) block is the stacked matrix of the "
              "corner rows above the beyond-corner rows (the words with "
              "three and more a's). Stacking rows only increases the "
              "norm, so the pair's error is at least its corner error, "
              "and the pair's corner is a SINGLE effective atom (2px, "
              "y): the line-atom problem itself, whose global "
              "certificate delivers the bound. THE PARITY-ODD SHELL "
              "THEOREM: every mirrored-pair approximant has error at "
              "least sqrt(lambda*), with equality only in the boundary "
              "refinement x to 0 — the line atom. Volume XI's measured "
              "anatomy — the parity-odd structure, the refinement, the "
              "optimality of the line atom — is now a proved statement, "
              "machine-verified at every link: the corner equality at "
              "2.2e-16, the stack inequality with zero violations over "
              "the scan, the corner infimum re-deriving sqrt(lambda*) "
              "to 1.1e-15 at the flip of (c*, y*). The three-parameter "
              "family never beats its own boundary."),
        ("p", "Why the theorem does not automatically extend to the "
              "general two-atom family is the battery's sharpest "
              "discovery. The weighted one-dimensional TWO-atom "
              "infimum is zero: the odd one-dimensional pair (w, -w), "
              "(r, -r) with r to 0 and w = c/2r converges to the point "
              "mass delta_1 itself — the corner is KILLABLE, so the "
              "corner bound alone is vacuous off the odd shell. But the "
              "killer pays everywhere else: placed on the cell with the "
              "x-amplitudes at 0.05 its error is 20.0, and the trade-off "
              "dial is exact — at x = 0.02, 0.05, 0.10, 0.20, 0.40 the "
              "cell errors are 50.0, 20.0, 10.0, 5.0, 2.7 while the "
              "corner stays at zero. The atoms that kill the corner "
              "must carry amplitude p_i = w_i/x_i that explodes on the "
              "a-even shell — the diagonal blocks — and the battery "
              "isolates the exact mechanism: the error norm squared "
              "dominates the largest eigenvalue of the positive "
              "semidefinite sum Y_ee Y_ee* + (T_2 - X_eo)(T_2 - "
              "X_eo)*, the payment plus the corner, both living on the "
              "even-row space. The strictness of the cell at the "
              "general level is this TRADE-OFF, not a corner "
              "obstruction; the escape-room scan through the corner "
              "lens — two hundred eighty-five configurations, none "
              "below the line-atom value, the best full error 1.560 "
              "with its corner at 1.435 and its payment at 0.240 — "
              "measures the frontier. The certified semialgebraic "
              "statement over the six-parameter family is the named "
              "open certificate, now reduced to a clean and explicit "
              "problem."),
        ("table", "strictness_chain"),
        ("figure", "corner"),
        ("p", "The anisotropic and affine corners close the free odd "
              "shell's escape. The odd-constrained two-state weighted "
              "automata — B = (0, b), C = (c, 0), A_a anti-diagonal, "
              "A_b diagonal, the general gamma_1-odd free family — have "
              "corners of the crossed form w alpha^i beta^(j+k): a "
              "three-parameter family containing the line atom as "
              "alpha = beta. The domain-guarded scan returns the "
              "crossed corner infimum exactly at the line-atom value "
              "with alpha = beta = y* recovered, the affine "
              "degenerations sit above at 1.4142 = sqrt(2), and the "
              "FULL six-parameter odd-shell scan through the free "
              "machinery lands on 1.2771421129 with the line-atom "
              "parameters recovered (the anti-diagonal entry a_12 "
              "collapsing to zero, alpha = beta = 0.6563): the free odd "
              "shell does not escape, and the anisotropy is a liability "
              "there exactly as the pair separation is on the abelian "
              "side."),
     ]},
    {"title": "The Complex and the Affine: The Identity Completions",
     "blocks": [
        ("p", "The first edition's complex coverage was honest but "
              "partial: the plain complex atoms were searched, the "
              "complex affine family excluded as outside the certified "
              "machinery's scope. The completion battery rebuilds the "
              "free-cell machinery over the complex field with the "
              "conjugations made explicit — the coefficient Gram is the "
              "sum of c(v)c(v)*, the reachable Grams are the conjugated "
              "Lyapunov identities with the operators conjugate-"
              "transposed — and validates the result twice: against the "
              "original machinery on real configurations to 1.3e-15, "
              "and against a complex-corrected dense word-space referee "
              "on thirty-six converged configurations to 3.6e-4. The "
              "corner reduction transfers verbatim (the a-parity block "
              "argument is index-level, field-agnostic): over the "
              "complex field the effective atoms (p_i x_i, y_i) "
              "conjugate properly in the corner Grams, the mirrored "
              "complex pair's stack stays tight at zero violation, and "
              "two hundred general complex pairs respect the corner "
              "bound with the minimum gap 0.094."),
        ("p", "The complex scans return the line-atom value everywhere. "
              "The complex one-atom corner infimum is sqrt(lambda*) "
              "exactly — and the optimizer is not real but GAUGED: "
              "|w| = c*, |r| = y* with opposite phases, the scan's "
              "point (-0.217 + 0.333i, -0.359 - 0.550i) sitting on the "
              "circle (w, r) = (c* e^{i psi}, y* e^{-i psi}). The "
              "PHASE GAUGE: the corner matrix of the gauged atom "
              "conjugates the real corner by unitary diagonal matrices "
              "— the row phase e^{-i(i+j)psi} against the column phase "
              "e^{-ik psi} — so the norm is invariant along the circle, "
              "verified at nine phase values to 6.7e-16, and the "
              "complex one-atom family reduces to the real one. The "
              "complex FREE scan — the full two-state complex weighted "
              "automata, twenty real parameters, the complex escape "
              "room of Open 7.13 — lands at 1.2771471 against 1.2771421: "
              "no escape at the measured level, the abelian shadow "
              "bounding the complex free class as it bounds the real "
              "one. The identity battery closes the completions: the "
              "conjugation symmetry (w, r) to (w-bar, r-bar) exact at "
              "zero, the isospectral doubling of the complex line "
              "atom's six-by-six spectrum at 1.1e-11, the flip (c, y) "
              "to (-c, -y) exact over the complex field, and the "
              "dilation identity's free target sigma_1 = sqrt(2) "
              "reproduced exactly. What remains honestly open over the "
              "complex field is the certified certificate — the ball-"
              "arithmetic bisection covered the real strip, and the "
              "complex domain's four real parameters await the extended "
              "run — and the complex trade-off, which is the same "
              "reduced problem as the real one."),
     ]},
    {"title": "The Empirical Face I: Spectral Compression",
     "blocks": [
        ("p", "The first edition ended at the theory's edge; the second "
              "edition gives the volume its empirical face by "
              "integrating the three experiments the proceeded chat "
              "designed against the programme — run at full audit "
              "strength in Volume X's battery and recorded here as the "
              "sandwich theory's contact with data. The first "
              "experiment attacks the corpus's central object directly: "
              "the spectral compression of sequence models, the "
              "Adamjan-Arov-Krein budget measured on a process this "
              "programme owns completely. The true process is the "
              "driven six-ring (a = 0.32, b = 0.18) observed through "
              "the four-symbol sensor s(i) = i mod 4 — an HMM whose "
              "observed process has a known minimal realization. The "
              "exact joint-probability Hankel over sixty-four-by-"
              "sixty-four prefix-suffix contexts returns machine-exact "
              "rank five — the sensor's collisions cost the process one "
              "dimension against its six hidden states — and the "
              "entropy rate, computed by the exact forward filter over "
              "four hundred thousand steps, is 0.9559 nats per symbol. "
              "The models: a linear state-space RNN whose Hankel "
              "singular values and reductions are exact closed-form "
              "objects through the Gramian machinery — certified "
              "before trusted, the balanced-transform certificate "
              "holding at 8e-16, the error-system Hankel norms "
              "cross-validated against a direct block SVD — and a "
              "vanilla tanh RNN measured empirically, three seeds "
              "each."),
        ("p", "The compression verdict is the sandwich theory's own "
              "prediction landing on data. The tanh RNN reaches "
              "cross-entropy 0.959 against the entropy floor 0.9559 "
              "— essentially optimal prediction — from a state whose "
              "spectrum collapses from sixteen dimensions to three at "
              "the one percent tolerance; the linear RNN's Gramian "
              "profile crosses the true rank five at the five percent "
              "tolerance; and the learned transition spectra carry the "
              "chiral complex pair in all three linear seeds — the "
              "models learn the record, rediscovering the arrow's "
              "spectral signature, not a smoothed surrogate. The AAK "
              "interval holds ten of ten along the balanced-"
              "truncation extraction ladder: the measured Hankel-norm "
              "error lies between the floor sigma_(n+1) and the tail "
              "sum at every order, exactly as the theorem demands, "
              "with the error-to-floor ratios at 1.00 on the boundary "
              "orders and 1.02 to 1.31 inside. The chat's curve-match "
              "prediction is thus confirmed in the strongest honest "
              "sense — different norms must disagree somewhere — and "
              "the knee prediction is exact: the cross-entropy curve "
              "flattens at order three, the predictive dimension, "
              "where the sigma profile has its own elbow (sigma_2 = "
              "4.77 dropping to sigma_3 = 0.89), matching the tanh "
              "model's three-dimensional state. The realization rank "
              "overcounts the information dimension by the modes that "
              "carry the joint law but not predictive entropy — the "
              "budget counts realizations, the task counts sufficient "
              "statistics, and the gap between them is the volume's "
              "own gap between the EYM floor and the realizable "
              "distance."),
        ("p", "The baseline adjudication splits honestly and the split "
              "is the theory's lesson. Against random state deletion "
              "the AAK extraction wins at every order — 1.11 to 1.48 "
              "against 0.98 to 1.38 on the cross-entropy scale — and "
              "against magnitude deletion it wins or ties everywhere. "
              "But against matched-size direct retraining the "
              "truncated model loses at the bottom orders: at order "
              "one the fresh small model reaches 1.12 against 1.30, "
              "at order two 1.04 against 1.38, tying only from order "
              "three. The truncation inherits structure a tiny model "
              "cannot use; retraining adapts. The sigma spectrum is a "
              "compression budget — the elbow predicts the knee "
              "exactly — but the budget is the linear realization's, "
              "and the sufficient statistic is smaller: the empirical "
              "shadow of the rank wall, measured on a process the "
              "programme controls to machine exactness."),
     ]},
    {"title": "The Empirical Face II: The Register and the Obstruction",
     "blocks": [
        ("p", "The second experiment is the coarsening scan the chat "
              "designed against the register theory: a POMDP with a "
              "restricted sensor, swept from full observability to "
              "noise, the memory requirements of the optimal policy "
              "measured exactly. The benchmark is the canonical Tiger "
              "— hidden side, open-left or open-right for +10 correct "
              "or -100 wrong, listen at cost one with accuracy kappa — "
              "because it admits exact machinery at every coarsening: "
              "the finite-horizon alpha-vector backup with exact "
              "upper-envelope pruning (the monotone chain drops only "
              "never-maximal lines, and the pruning returns the "
              "belief regions and their kinks in linear time — the "
              "O(n^3) kink search that blocked the chat's design "
              "replaced), the obstruction datum computed by enumerating "
              "all twenty-seven memoryless one-state controllers, the "
              "register as the alpha-count. The scan runs kappa from "
              "1.0 down to 0.5."),
        ("p", "The register law is the scan's headline and it is "
              "Volume VIII's inflation law measured on the control "
              "side. The optimal policy's alpha-count grows from 9 at "
              "full accuracy through 59, 34, 44, 45 — and then "
              "explodes to 9153 at kappa = 0.60: the curse of history "
              "made visible in a single number, the register "
              "inflating exactly as the sensor coarsens, until the "
              "game itself collapses to the stall regime (the optimal "
              "value listen-out-the-horizon at -8, the register "
              "falling back to 280 and 4). The obstruction iff holds "
              "at every kappa: the datum is positive exactly when the "
              "optimal policy needs memory, including the stall "
              "boundary where the optimum is itself memoryless and "
              "the datum vanishes. The quantitative layer is recorded "
              "honestly rather than rounded up: on the informative "
              "range the obstruction correlates with the oracle gap "
              "at Pearson 0.38 — weak — and the chat's weighted-"
              "curvature prediction is refuted outright, the "
              "visit-weighted curvature ANTI-correlating at -0.95 "
              "because the closed-loop visitation concentrates on the "
              "flat listen-and-stall paths as the gap grows: the "
              "finite-horizon stall confound, identified and measured. "
              "What survives is the structure — the iff exact, the "
              "inflation dramatic — and the confound itself is the "
              "finding the chat's design could not have anticipated."),
        ("p", "The record side of the experiment returned a theorem "
              "instead of a curve, and the second edition records it "
              "as such because it is this volume's own subject: the "
              "Tiger's listen record is conditionally iid given the "
              "hidden side, so every block law is the exchangeable "
              "mixture — one-half product of the left-channel "
              "densities plus one-half product of the right — which "
              "is invariant under index reversal. The record's arrow "
              "is identically zero at every sensor quality, verified "
              "on all sixteen four-blocks at every kappa to 3.5e-18. "
              "The chat's bridge from control performance to the "
              "arrow of time cannot be tested on memoryless-sensor "
              "benchmarks: the record stratum degenerates by "
              "construction, and the honest experiment separates the "
              "strata it was meant to conflate — the obstruction "
              "measures the memory the controller needs, the record "
              "measures the temporal structure the source carries, "
              "and on the Tiger they are decoupled exactly. The "
              "bridge lives on sources with temporal structure, the "
              "class the laundering theorems of the reversal-group "
              "volume cover."),
     ]},
    {"title": "The Empirical Face III: The Sheaf Stratum",
     "blocks": [
        ("p", "The third experiment is the compositional-"
              "generalization branch: the chat's sheaf diagnostic — "
              "nonvanishing cohomology tracking training failure, the "
              "harmonic norm correlating with the validation gap — "
              "run on the minimal two-token compositional task where "
              "every number is exact. Modular addition on Z_7, the "
              "pair (a, b) mapped to (a + b) mod 7, a 2-64-64-7 ReLU "
              "MLP trained to convergence, twelve seeds per split, on "
              "four splits: the compositional quadrant (train both "
              "operands in 0..3, sixteen pairs, thirty-three held "
              "out), an intermediate split, the full-grid control, "
              "and a scattered random-60 split whose held-out pairs "
              "are compositions of trained tokens. The sheaf is the "
              "cellular sheaf on the bipartite token graph — fourteen "
              "token vertices, the training pairs as edges, vertex "
              "stalks the hidden activation space, edge restrictions "
              "the per-token PCA projectors — and the diagnostic is "
              "the coboundary energy of the identity section: for "
              "each training edge, the normalized disagreement "
              "between the row-token and column-token reconstructions "
              "of the shared activation. The failure of local "
              "representations to glue into a global section, made "
              "computable."),
        ("p", "The compositional failure reproduces exactly as the "
              "literature reports: training accuracy 1.000 on every "
              "split and seed, held-out accuracy 0.073 on the "
              "compositional split, 0.006 on the intermediate, 0.000 "
              "on the scattered random-60, 1.000 on the control. The "
              "sheaf's verdict splits cleanly, and the split is the "
              "experiment's honest result. Task-level: the mean "
              "coboundary energy orders the four splits exactly as "
              "their errors do — 0.541 control, 0.577 compositional, "
              "0.594 intermediate, 0.615 scattered, against errors "
              "0, 0.927, 0.994, 1.000 — a perfect ordering: the "
              "energy predicts WHICH task geometry fails. Seed-level: "
              "within a split the correlation between energy and "
              "error across the twelve seeds is null to slightly "
              "negative (-0.20 and -0.18 on the informative splits). "
              "The pooled 0.59 is split-dominated and flagged as "
              "such. The chat's harmonic-norm claim is confirmed at "
              "the task level and refuted at the seed level on this "
              "benchmark — the honest split that single-run "
              "experiments cannot express because they cannot "
              "separate the two variances. The sheaf diagnostic is a "
              "geometry-of-the-task predictor, not a which-random-"
              "seed-fails predictor: the obstruction datum of the "
              "second experiment's theory, measured on the "
              "representation stratum."),
        ("table", "experiments"),
     ]},
    {"title": "It and Bit from Record",
     "blocks": [
        ("p", "The proceeded chat's final synthesis — it and bit from "
              "record — lands on the corpus's Born-record program, and "
              "the second edition closes by stating the landing "
              "precisely. The stratification that survives the audit: "
              "the RECORD stratum is the preserved classical block of "
              "the channel's spectrum — the dephasing top-degeneracy, "
              "the block the environment cannot contract — measured by "
              "the multiplicative gradings of the abelianized rung; "
              "the QUANTUM stratum is the contracted coherence block, "
              "measured by the coherent information, the stratum the "
              "experiments of this edition's empirical face probe "
              "from the learning side (the chiral pair the linear "
              "RNNs learn; the register the Tiger's controller "
              "inflates; the sheaf glue the MLPs fail to build); the "
              "THERMODYNAMIC stratum is the reversal-pair asymmetry — "
              "not a spectral gap but a rank defect, the arrow "
              "detected by the Hankel rank, the mode count of the "
              "non-reversible pair. Three strata, three instruments, "
              "one object: the Hankel operator's structure — which is "
              "this volume's object from its first page to this one."),
        ("p", "The cell's closure is the purest instance of the "
              "synthesis. The line atom — the optimal two-state "
              "approximant to the cell — is a statement about how "
              "much of the (1,1) coupling a rank-two record can "
              "carry: the answer is an algebraic number, degree "
              "three, the distance 1.2771421129084462 above the "
              "unconstrained floor. The rank wall forbids the floor; "
              "the corner reduction shows the parity-odd record "
              "cannot beat the boundary; the trade-off shows the "
              "general record pays elsewhere; the phase gauge shows "
              "the complex record adds freedom but not distance. The "
              "sandwich — the EYM floor below, the abelianized "
              "ceiling above — is the price of realizability, and "
              "the price is now known exactly at the smallest "
              "instance: it and bit from record, priced in a cubic "
              "irreducible over the rationals."),
     ]},
    {"title": "The Honest Ledger, Second Edition",
     "blocks": [
        ("p", "Updated statuses, with the changes this edition "
              "carries. The cell's D(2): CLOSED — sqrt(lambda*), the "
              "cubic minimal polynomial, the global line-atom "
              "certificate, the parity-odd shell theorem, the corner "
              "reduction, the complex completions; the remaining open "
              "piece is the certified semialgebraic trade-off over "
              "the general six-parameter family, now an explicit "
              "named problem (the corner-plus-payment inequality), "
              "and the complex-field extension of the ball-arithmetic "
              "certificate. The amalgam closed form and the lens "
              "criterion: unchanged, proved, machine-exact. The "
              "retraction of Volume VIII's witness: standing, the "
              "methodological lesson (upper-bound objectives do not "
              "locate minima) now twice confirmed — the surrogate "
              "artifact there, the corner-killer's false promise "
              "here. The empirical face: integrated, with the three "
              "experiments' verdicts — the AAK interval exact and "
              "the knee exact with the baselines split honestly; the "
              "register law exact with the curvature prediction "
              "refuted and the record-side degeneracy proved; the "
              "sheaf ordering perfect at the task level and null at "
              "the seed level. The longer programme: Open 7.13's "
              "constructive side and the abelian-shadow equality "
              "beyond the witness remain the named analytic "
              "frontier; the n = 4 ladder's L = 10 leg; the "
              "Lyapunov-cohomology correspondence. The next links "
              "this edition names: the trade-off certificate, the "
              "complex bisection, and the free corner's trilinear "
              "structure — the escape room's exact anatomy, stated "
              "as a problem for the first time."),
     ]},
]

TABLES_C = {
    "strictness_chain": {
        "caption": "Table 5 — The strictness chain, second edition: the "
                   "corner-reduction package, its proof status, and its "
                   "machine verification",
        "header": ["The chain's link", "Statement", "Status",
                   "Verification"],
        "ratios": [0.20, 0.37, 0.19, 0.24],
        "font": 7.3,
        "rows": [
            ["T1 the corner reduction",
             "||cell error|| >= ||corner error||, the corner = the "
             "multiplicity-weighted 1-D Hankel over the (|u|_a = 1) x "
             "(|v|_a = 0) words, with the effective atoms (p_i x_i, y_i)",
             "PROVED (block interlacing + the compression; field-"
             "agnostic, real and complex)",
             "the 3x3 = the line-atom 6x6 to 1.8e-15; 300 random "
             "configs, 0 violations; complex 200 configs, 0 violations"],
            ["T2 the parity-odd shell theorem",
             "every gamma_1-odd rank-2 approximant (the mirrored pair "
             "family) has error >= sqrt(lambda*), equality only at the "
             "boundary line atom (x -> 0)",
             "PROVED (the stack argument + Task 17's global "
             "certificate)",
             "the corner infimum re-derived at 1.2771421129 to "
             "1.1e-15 at the flip (c*, y*); the pair-never-beats-"
             "limit check: zero violations"],
            ["T3 the 1-D closure discovery",
             "the weighted 1-D TWO-atom infimum is ZERO (the odd pair "
             "converges to delta_1) — the corner is killable; the "
             "general family's strictness is the trade-off",
             "MEASURED + the mechanism isolated (the killer pays "
             "1/x on the a-even shell)",
             "the killer at x = 0.02..0.40 gives cell errors 50.0, "
             "20.0, 10.0, 5.0, 2.7 with corner 0; the PSD-sum "
             "identity exact"],
            ["T4 the anisotropic corners",
             "the crossed corner (the odd-constrained free family) "
             "and the affine degenerations do not beat the line atom",
             "MEASURED (domain-guarded scans)",
             "crossed infimum = 1.2771421129 with alpha = beta = y* "
             "recovered; affine at 1.4142; the full 6-param odd shell "
             "lands on the line-atom parameters"],
            ["C the complex completions",
             "the corner, the free class, and every identity over C: "
             "no complex escape; the phase gauge reduces the complex "
             "1-atom corner to the real one",
             "PROVED (the gauge = unitary diagonal conjugation); the "
             "scans measured",
             "the gauge circle at 6.7e-16; the complex free infimum "
             "1.2771471; the identities (doubling, flip, "
             "conjugation, dilation) all machine-exact"],
        ],
    },
    "experiments": {
        "caption": "Table 6 — The empirical face integrated: the three "
                   "experiments' headline verdicts at audit strength",
        "header": ["The experiment", "The chat's prediction",
                   "The verdict", "The headline numbers"],
        "ratios": [0.16, 0.27, 0.24, 0.33],
        "font": 7.3,
        "rows": [
            ["1 spectral compression",
             "the distortion-rate curve matches the sigma_(n+1) "
             "bounds; the extraction beats distillation baselines",
             "the AAK interval exact 10/10; the knee exact; the "
             "curve-match honest (ratios 1.00-1.31); the baselines "
             "SPLIT",
             "WFA rank 5 exact; entropy 0.9559; tanh compresses 16 "
             "-> 3 at 1%; the knee at order 3 = the sigma_3 elbow; "
             "vs retraining: 1.12/1.30 and 1.04/1.38 at orders 1-2, "
             "ties from 3"],
            ["2 the coarsening scan",
             "the obstruction datum tracks the memory requirement; "
             "curvature predicts the gap's magnitude",
             "the iff EXACT at every kappa; the register law exact; "
             "the weighted-curvature claim REFUTED; the record-side "
             "degeneracy PROVED",
             "the register 9, 59, 34, 44, 45, 9153, 280, 4; the "
             "explosion at kappa = 0.60; r = 0.38 obstruction-gap; "
             "r = -0.95 weighted curvature; the record arrow < "
             "3.5e-18 at every kappa"],
            ["3 the sheaf diagnostics",
             "nonvanishing cohomology tracks failure; the harmonic "
             "norm correlates with the validation gap",
             "the task-level ordering PERFECT; the seed-level "
             "correlation NULL; the pooled number split-dominated",
             "OOD 0.073/0.006/0.000/1.000; energies 0.541/0.577/"
             "0.594/0.615 — the exact same ordering; seed-level "
             "-0.20/-0.18"],
        ],
    },
}

STATS_C = [
    ("D(2) = sqrt(lambda*)", "1.2771421129", "the closed value"),
    ("minpoly lambda*", "108x^3-415x^2+522x-216", "irreducible, degree 3"),
    ("corner equality", "1.8e-15", "3x3 vs the 6x6 machinery"),
    ("parity-odd shell", "PROVED", "T2, with Task 17"),
    ("1-D two-atom inf", "0", "the corner is killable"),
    ("phase gauge", "6.7e-16", "complex = real"),
]
