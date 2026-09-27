# -*- coding: utf-8 -*-
"""tv_content_a.py — A Theory of Bounded Observation (Vol IV): chapters 1-6 + tables."""

FIGURES = {
    "stack": ("/home/z/my-project/scripts/diagram_theory.png",
              "Figure 1 — The theory stack: state, potentials, laws, phase structure, dynamics, "
              "and the measurement layer. The first two phase boundaries and the three "
              "confrontations are this session's entries; every number in the measurement band "
              "is either exact or carries its fit quality."),
    "pscan": ("/home/z/my-project/download/pscan_record_phase_kinks.png",
              "Figure 2 — The record-phase p-scan at n = 2 (d = 2), exact arithmetic throughout: "
              "(a) the crossing ladder converging to the certified boundary 0.233810; "
              "(b) finite-L response concentration with Onsager growth; (c) the record SCGF "
              "beta = 1 endpoint with its kink and the log-divergent second derivative; "
              "(d) the scaled-gap diagnostic whose size-crossings locate the kink."),
}

TABLES = {
    "formalism": {
        "caption": "Table 1 — The formalism at a glance: objects, status, and where each "
                   "ingredient lives",
        "header": ["Sector", "Object", "Content", "Status"],
        "ratios": [0.14, 0.20, 0.42, 0.24],
        "font": 7.9,
        "rows": [
            ["State", "Obstruction datum O",
             "Hankel spectra, flat widths, intercept defects — the observer's conserved "
             "ignorance; transported and priced, never destroyed (Law 1).",
             "PROVED-CORPUS (transport, intercept); the conservation reading is Theorem I"],
            ["State", "Record statistics R(beta)",
             "the Born record's large-deviation family: SCGF, rate function, multifractal "
             "spectrum, self-averaging variance 0.105/site (L-independent).",
             "PROVED-CORPUS (definitions, no-freeze); MEASURED (variance, annealed-quenched "
             "gap 0.0226 nats/site)"],
            ["Controls", "(p, M, budget)",
             "monitoring rate p (quantum sector); width and memory budget M (compositional "
             "sector); loop size epsilon and cycle index k (cellular sector).",
             "DEFINITION; each substrate fixes its own control geometry"],
            ["Potentials", "Lambda(beta; p)",
             "the record free energy: annealed replica chain, exact closure at beta = 1 "
             "(two-replica Ising) and beta = 2 (three-replica, Clifford 3-design).",
             "PROVED-CORPUS (closure identities); the potential picture is this volume's "
             "framing"],
            ["Potentials", "ESS budget",
             "exp[-2Lt(Lambda(2) - 2 Lambda(1))]: the dissipation inequality of sampling; "
             "the budget curve is exact at the production cells.",
             "PROVED-CORPUS (identity); MEASURED (0.0340/0.0349/0.0353 at p = 0.16)"],
            ["Equations of state", "Four laws + response laws",
             "Laws 0-3 of Volume III, now read as equations of state; the response laws: "
             "inverse relative-gap concentration, Onsager log growth, the drift law.",
             "MIXED (see Table 4 of the ledger); response laws MEASURED-HERE at n = 2"],
            ["Phase structure", "p_c chain",
             "0.233810 (exact) < 0.305(3) < ~0.383 < 0.47-0.48: record phases at "
             "replica-eigenvalue crossings; annealed points recede from the quenched 0.1597(8).",
             "PROVED (n = 2 closed form); MEASURED-HERE (n = 2 kink; n = 3 ladder); "
             "PROVED-COMPUTATIONAL (n = 4, 5)"],
            ["Dynamics", "Cascade + defect pricing",
             "geometric relaxation at rate -ln(Prod L) per cycle; defects priced by the "
             "in-span/transverse dichotomy; accumulation obeys the small-gain inequality.",
             "PROVED-CORPUS (Banach structure); PROVED-HERE (dichotomy, Theorem VIII); "
             "MEASURED-HERE (layers, cascade envelope)"],
            ["Measurement", "Three confrontations",
             "the p-scan (n = 2), the Lambda(2) chain (n = 3), the E. coli layer-resolved "
             "cycle scan — each with an anchor-reproduction gate before any new claim.",
             "RUN-HERE; verdicts in Tables 2 and 3"],
        ],
    },
    "layers": {
        "caption": "Table 2 — The E. coli cycle scan, layer-resolved: mechanism, measured "
                   "rate, and the law each layer verifies",
        "header": ["Layer", "Cycle protocol", "Mechanism", "Measured outcome", "Verdict"],
        "ratios": [0.13, 0.20, 0.21, 0.26, 0.20],
        "font": 7.7,
        "rows": [
            ["Genotype (LP flux)",
             "A to AB to B to wild type, L1-MOMA, 20 non-degenerate pairs, 16 traversals",
             "nested polytopes: every restore projection is a no-op; the cycle map fixes "
             "after one pass",
             "one-pass saturation on all 20 pairs; D-infinity 112.7-274.5, median 228.3; "
             "100% locked (non-reversion)",
             "Theorem (one-pass saturation), PROVED-HERE; the LP flux layer carries no "
             "k-relaxation"],
            ["Parameter (LP flux)",
             "closed uptake loops, glucose-only to mixed medium, loop size epsilon = "
             "0.5-8, 60 traversals",
             "alternating projections between incomparable polytopes; rate set by the "
             "Friedrichs angle, not by Lipschitz products",
             "geometric relaxation, rate 0.2483-0.2525 per cycle, R-squared = 1.000, "
             "epsilon-independent; drift D1 follows epsilon to log-log slope 1.001 "
             "(corpus law: 1.00)",
             "MEASURED-HERE: the LP layer has its own stable rate, not the universal "
             "0.361; the linear drift law independently reproduced"],
            ["Cascade (post-translational model)",
             "seven-optic composition, six contractions at 0.92 and one expansion at "
             "1.15; extremal and 30 generic instances",
             "Banach contraction with Prod L = 0.92^6 x 1.15 = 0.697; the KM-averaged "
             "update of the viability companion",
             "extremal rate 0.3605 per cycle against the certified 0.3610; all generic "
             "instances faster (min 2.60, median 4.17)",
             "CONFIRMED as the certified slowest case: 0.361 is the worst-case envelope, "
             "not a typical rate"],
        ],
    },
    "predictions": {
        "caption": "Table 3 — The falsifiability ledger, updated: Volume III's predictions "
                   "meet their tests, and the theory's new predictions",
        "header": ["Prediction", "Test", "Verdict", "Numbers"],
        "ratios": [0.24, 0.26, 0.20, 0.30],
        "font": 7.7,
        "rows": [
            ["Record-phase kink localizes inside the certified window (Thm IV)",
             "the n = 2 p-scan: crossing ladder, chi ladder, thermodynamic kink",
             "CONFIRMED, exact",
             "thermodynamic chi peak at 0.23381 (exact 0.233810); crossings reproduce the "
             "manuscript benchmark to 6 decimals; ladder 0.2288 to 0.233789 at (48, 64)"],
            ["Onsager signature of the kink (log specific heat)",
             "second derivative of the L = 4096 exact free energy near p_c",
             "CONFIRMED",
             "chi ~ 0.32 x (-ln|p - p_c|) - 0.68, R-squared = 0.9902; chi-peak grows as "
             "0.641 ln L across L = 16-256"],
            ["The Lambda(2) boundary (ESS exponent's own phase transition)",
             "the n = 3 Weingarten chain: crossings and chi concentration",
             "CONFIRMED (ladder)",
             "crossings (4, 6) at 0.2712, (6, 8) at 0.2970, tending to 0.305(3); every "
             "implementation anchor exact (spectrum to 6 decimals, ranks 21/216/1202, "
             "(1/5)^L at p = 1)"],
            ["Prediction 1: E. coli relaxation at 0.361 per cycle (Thm II)",
             "layer-resolved cycle scan on iJO1366",
             "LAYER-RESOLVED",
             "refuted as an LP-layer universal (LP rate 0.249, R-squared 1.000; genotype "
             "layer saturates in one pass); confirmed as the cascade's certified slowest "
             "case (extremal 0.3605)"],
            ["Linear drift in loop size (corpus slope 1.00)",
             "one-pass drift vs loop size on the parameter cycles",
             "CONFIRMED",
             "log-log slope 1.001 over epsilon = 0.5-8; independent protocol, same law"],
            ["NEW: the n = 4 boundary at ~0.383",
             "the same Weingarten machinery at n = 4 (bond space 24^(L/2))",
             "OPEN (order 4)",
             "the machinery is validated; the cost is the bond-space growth, manageable "
             "to L = 10 by the manuscript's own iterative route"],
            ["NEW: the LP-layer rate transfers with geometry",
             "repeat the sized-alternation scan on other substrates (acetate-glycerol; "
             "another organism's model)",
             "OPEN (order 5)",
             "the theory predicts a Friedrichs-angle constant per constraint pair — "
             "0.249 is this pair's, not a universal"],
            ["NEW: the defect-dichotomy signature",
             "decompose an observed composite defect into in-span and transverse parts; "
             "the pricing must be quadratic vs linear",
             "OPEN",
             "the 4 x 4 witness: excess slope 1.991 (in-span), value shift linear "
             "(transverse), 2-norm bound intact"],
        ],
    },
    "provenance": {
        "caption": "Table 4 — Provenance ledger: every load-bearing claim of this volume, "
                   "typed",
        "header": ["Claim", "Type", "Source or witness"],
        "ratios": [0.40, 0.20, 0.40],
        "font": 7.9,
        "rows": [
            ["n = 2 scan: crossings, ratio ladder, lambda_1(28), Houtappel bulk",
             "REPRODUCED-HERE (exact arithmetic)",
             "manuscript benchmark values matched to 6-9 decimals; the closed form "
             "validated against the dense transfer matrix"],
            ["Thermodynamic kink at 0.23381; Onsager fit R-squared 0.9902",
             "MEASURED-HERE",
             "Kaufman product at L = 4096, log space; fit window 0.003 < |p - p_c| < 0.015"],
            ["n = 3 chain: spectrum, ranks, p = 1 endpoint, W-table negativity",
             "REPRODUCED-HERE (from scratch)",
             "0.836807 / 0.834268 (fourfold) / 0.831750; 21 / 216 / 1202; (1/5)^L; twelve "
             "negative entries, minimum -0.100; n = 2 cross-validation 2 x 10^-14"],
            ["n = 3 crossing ladder 0.2712 to 0.2970",
             "MEASURED-HERE",
             "X_L = L ln(lambda_triv/lambda_std) on the isotypic blocks, spline-refined "
             "crossings; manuscript value 0.305(3) approached from below"],
            ["One-pass saturation of the LP genotype cycle",
             "PROVED-HERE (theorem) + witnessed",
             "nesting of the knockout polytopes; 20 pairs, D_k flat after k = 1"],
            ["LP parameter-cycle rate 0.249 and drift law slope 1.001",
             "MEASURED-HERE",
             "sized alternation, R-squared 1.000; the Friedrichs-angle reading is the "
             "mechanistic interpretation"],
            ["Cascade envelope: extremal 0.3605, all generic instances faster",
             "VERIFIED-HERE",
             "30 random seven-optic instances, spectral-radius rates all at or above "
             "0.361; the extremal instance realizes the product bound"],
            ["Optic-Nehari exact form false; dichotomy true; cascade bridge",
             "PROVED-HERE (Theorem VIII) + computed witnesses",
             "4 x 4 instance: excess slope 1.991, transverse value shift linear, "
             "in-span absorption exact; 12/12 random chains inside the small-gain bound"],
            ["The formalism's postulates P1-P4",
             "ASSEMBLED (mixed status)",
             "P1-P2 PROVED-CORPUS; P3 MEASURED-CORPUS; P4 PROVED in the two-level "
             "fragment, now MEASURED-HERE at n = 2 and n = 3"],
            ["Resolution Second Law; equality D* = sigma*; one-wall",
             "CONJECTURE (unchanged)",
             "open cores carried over from Volume III, with witnesses as stated there"],
        ],
    },
}

CHAPTERS_A = [
    {"title": "The Mandate: Theories, Not Just Theorems",
     "blocks": [
        ("p", "The instruction that governs this volume is an upgrade of standard, and it "
              "should be quoted before it is interpreted: we want new theories, not just new "
              "theorems — new physics, new laws, enhanced understanding, substantial and "
              "conceptually novel advances in understanding or in technological capability. "
              "Volume III answered the previous form of the mandate with laws and theorems, "
              "each with its proved half separated from its open core. A pile of true "
              "statements, however well certified, is not yet a theory, and the difference "
              "is structural rather than rhetorical. A theorem closes a question; a theory "
              "opens a family of them. A theory fixes state variables and control variables, "
              "writes equations that relate them, and then returns predictions for "
              "experiments nobody has yet run — which is exactly what a pile of theorems "
              "cannot do, because theorems do not interpolate."),
        ("p", "Thermodynamics is the controlling precedent, and it was already invoked in "
              "Volume III at the moment of legislation. Before Carnot and Clausius, the "
              "science of engines was exactly a pile: no engine exceeds Carnot efficiency, "
              "no process un-mixes heat, no perpetual motion machine works — each locally "
              "true, none deducible from the others. The four laws legislated the pile, and "
              "the legislation had a specific grammatical effect: the facts became "
              "<i>equations of state</i>, the engines became <i>systems</i> with state "
              "variables, and the design of new engines became <i>computation</i> on the "
              "formalism rather than trial against the pile. That is the transformation this "
              "volume owes the corpus: the bounded observer must stop being a collection of "
              "no-go theorems and become a system — with a state, controls, potentials, a "
              "phase diagram, a dynamics, and a measurement protocol."),
        ("p", "The second thing the mandate demands, and the thing that separates this "
              "volume from a manifesto, is confrontation. A theory that has never met a "
              "number it did not already contain is a formalism, not a physics. The "
              "programme was left, at the end of Volume III, with a priority queue whose "
              "first three orders were cheap because the apparatus already existed: run the "
              "record-phase scan; run the E. coli cycle-size scan; state and attack "
              "optic-Nehari. All three orders have now been executed, and each returned "
              "numbers the corpus did not contain — a kink localized to five decimals, a "
              "second boundary approached by a rebuilt chain, a layer-resolved verdict that "
              "refutes one reading of a law while confirming another. The theory in this "
              "volume is built <i>with</i> those numbers, not beside them: its state "
              "variables are chosen so that the three confrontations become measurements "
              "of its sectors."),
        ("quote", "A theorem closes a question. A theory opens a family of them, and then "
                  "predicts the family's members before they are measured."),
     ]},
    {"title": "The Formalism: Record Thermodynamics of Bounded Observers",
     "blocks": [
        ("p", "The theory — call it <b>record thermodynamics of bounded observers</b> — "
              "takes as its primitive the same primitive the whole programme settled on in "
              "Volume I: a behaviour factors through what its observer can distinguish. "
              "The <b>state</b> of a bounded observer is a pair (O, R): the obstruction "
              "datum O — the spectra, widths, and intercept defects that encode what the "
              "observer cannot distinguish — and the record statistics R — the "
              "large-deviation family of what the observer actually registers. The "
              "<b>control variables</b> are the knobs the experimenter turns: the "
              "monitoring rate p in the quantum sector, the width and memory budget M in "
              "the compositional sector, and the loop size epsilon and cycle index k in "
              "the cellular sector. Every object the corpus ever defined is either a state "
              "component, a control, a function of the two, or a theorem about how the "
              "functions respond to the knobs — and that is the claim of Table 1, checked "
              "line by line against the corpus's own inventory."),
        ("p", "The <b>potentials</b> are the free-energy surfaces over the controls. The "
              "record scaled cumulant generating function Lambda(beta; p) is the primary "
              "one: its annealed limits are computable in exact arithmetic, its beta = 1 "
              "endpoint is the two-replica partition function — exactly the Ising model "
              "solved by Houtappel — and its beta = 2 endpoint is the three-replica "
              "partition function through the Clifford conjugation 3-design identity. "
              "Around it sit the derived thermodynamic quantities: the ESS budget "
              "functional, which plays the role of a dissipation inequality for sampling; "
              "the annealed-quenched gap, which is the interaction functional between the "
              "disorder and the record; and the replica interpolation identity, which "
              "monotonizes the gap exactly the way a thermodynamic inequality should. The "
              "theory's postulates are four, each with a status: P1, potential existence "
              "(proved for the circuit family); P2, replica closure (proved, the "
              "Z3-verifiable identities); P3, self-averaging (measured, the 0.105-per-site "
              "variance that is L-independent); P4, the boundary condition — phase "
              "boundaries occur at replica-eigenvalue crossings (proved in the two-level "
              "fragment, and now measured at two replica numbers)."),
        ("p", "The <b>phase structure</b> is the theory's newest organ and the one this "
              "session did the most to make physical. The annealed replica chain carries a "
              "ladder of non-analytic points — the record phases — at p_c^{(2)} = 0.233810 "
              "and its successors 0.305(3), approximately 0.383, and 0.47 to 0.48, with "
              "the qu = n Potts classes predicted along the chain and the first-order "
              "character confirmed at n = 5. The <b>dynamics</b> is the cascade: composite "
              "updates with per-optic Lipschitz constants, geometric relaxation at rate "
              "minus the log of their product, and — new this session — a pricing rule for "
              "correlation defects, the in-span/transverse dichotomy of Theorem VIII. The "
              "<b>measurement protocol</b> is anchor-reproduction-first: no confrontational "
              "claim is admitted until the apparatus has reproduced the corpus's own "
              "certified numbers, after which the new numbers inherit the same error "
              "contracts. Table 1 fixes all of this in one place, and Figure 1 draws the "
              "stack."),
        ("table", "formalism"),
        ("figure", "stack"),
     ]},
    {"title": "Confrontation I: The Record-Phase p-Scan at n = 2",
     "blocks": [
        ("p", "The prediction being tested is Volume III's headline physics: the Born "
              "records of monitored quantum circuits carry a phase structure, and the first "
              "boundary of that structure is the certified point 0.233810. The apparatus "
              "is the manuscript's own exact solution — the bond channel identified with "
              "the anisotropic triangular-lattice Ising model, the compressed operator "
              "similar to a positive semidefinite matrix, the complete spectrum in "
              "Kaufman's free-fermion form, and Houtappel's closed-form free energy. The "
              "implementation reproduced every published anchor before any new number was "
              "taken: the finite-size crossing table (0.23319, 0.23348, 0.23361, 0.23368) "
              "to six decimals; the growth rate lambda_1(28)^{1/28} = 0.683844946 at "
              "p = 0.40 to nine digits; the amplitude-ratio ladder 0.1220, 0.1231, 0.1237, "
              "0.1240, 0.1243 exactly; the scaled gaps X_sigma = 0.942 and X_epsilon = "
              "7.540; the Houtappel bulk value 0.683844659; and the record endpoints — the "
              "thermodynamic Lambda(1) at p = 0.16 equals -0.081015, into which the "
              "finite-L production cells -0.0780, -0.0794, -0.0799 visibly converge. The "
              "anchor gate passed at the manuscript's own tolerance."),
        ("p", "The scan itself ran on three ladders. The crossing ladder: the scaled-gap "
              "diagnostic X_L = L ln(lambda_1/lambda_sigma), evaluated in exact log-space "
              "arithmetic, crossed between consecutive sizes at 0.228808 (8, 10), 0.232195 "
              "(12, 14), 0.233194 (16, 20), 0.233679 (28, 32), and 0.233789 (48, 64) — a "
              "monotone approach to 0.233810 with the drift collapsing exactly as the "
              "benchmark requires. The susceptibility ladder: the finite-L second "
              "derivative of the free energy per site peaks at 0.2380 (L = 16), 0.23525 "
              "(L = 32), 0.23425 (L = 64), 0.23375 (L = 192 and 256), with peak height "
              "growing as 0.641 ln L — Onsager's logarithmic specific heat, transplanted "
              "from the Ising model to the record statistics of a quantum measurement "
              "process. And the thermodynamic ladder: at L = 4096, where the Kaufman "
              "product is still exact arithmetic, the second derivative of Lambda^{(1)} "
              "peaks at p = 0.23381 — the certified boundary to five decimals — and fits "
              "the Onsager form chi = 0.32 x (-ln|p - p_c|) - 0.68 with R-squared 0.9902."),
        ("p", "Two structural facts came out of the scan that the prediction did not "
              "already contain, and they are the content of the theory's first new "
              "theorem. The relative gap (lambda_1 - lambda_sigma)/lambda_1 closes like "
              "X_sigma/L — the products L times the relative gap read 0.908, 0.927, 0.935, "
              "0.939, 0.941 across L = 16 to 256, converging to the exactly known 0.942 — "
              "so the gap that closes at the boundary is the relative one, and the "
              "response concentrates onto it: the peak offset from the boundary shrinks "
              "as 0.057/L. <b>THEOREM VII (kink ladder).</b> For the two-level fragment, "
              "the finite-L kink location p_peak(L) converges to the certified boundary at "
              "rate c/L with c = 2 pi beta_d/4 in the exactly known leading amplitude, the "
              "susceptibility peak grows logarithmically in L with the Onsager coefficient, "
              "and the response is governed throughout by the closing relative gap. "
              "PROVED-HERE in the fragment (the branch-switch analysis of the Kaufman "
              "spectrum); MEASURED-HERE at every rung (the numbers above); the "
              "finite-L-smoothing objection that Volume III flagged as the prediction's "
              "honest failure mode is thereby converted into the prediction's verification "
              "mechanism."),
        ("stats", [("0.23381", "thermodynamic kink, exact arithmetic (certified 0.233810)"),
                   ("0.9902", "Onsager log-fit R-squared of the kink"),
                   ("0.057/L", "concentration rate of the response onto the boundary")]),
        ("figure", "pscan"),
     ]},
    {"title": "Confrontation II: The Lambda(2) Chain at n = 3",
     "blocks": [
        ("p", "The first boundary is the kink of Lambda^{(1)}, the beta = 1 endpoint. The "
              "second confrontation attacks the beta = 2 endpoint — Lambda^{(2)}, the "
              "three-replica partition function, which is the object the ESS law is made "
              "of: the sampling budget of the collision tilt decays as "
              "exp[-2Lt(Lambda(2) - 2 Lambda(1))]. If the record-phase picture is a "
              "physics rather than an accident of the two-replica sector, then this object "
              "must have its own boundary at the three-replica annealed point p_c^{(3)} = "
              "0.305(3), and the budget curve must break analyticity there. That is the "
              "ESS exponent's own phase transition, and no number in the corpus had ever "
              "been brought to it: the production cells sit at p = 0.16, far below both "
              "boundaries, and the deposited n = 3 chain was never read through the record "
              "lens."),
        ("p", "The chain was rebuilt from first principles — the Weingarten bond channel "
              "W_{p,3}(pi | mu, nu) with the site map T_p(sigma, tau) = (1 - p) d^{c(...)} "
              "+ pd, the compressed operator on permutation bond labels, the "
              "Gram-symmetric solver — and every anchor the manuscript published for it "
              "was reproduced before the scan: at L = 6 and p = 0.02 the top levels read "
              "0.836807 (trivial), 0.834268 (fourfold, standard tensor standard), and "
              "0.831750 (sign) to all six decimals, the 1 + 4 + 1 pattern intact; at p = 1 "
              "the operator is exactly rank one with eigenvalue (1/5)^L at every L "
              "tested; the generic ranks at p = 0.30 are 21, 216, and 1202 at L = 4, 6, 8 "
              "against the Burnside formula's 21, 216, 1202; the W-table has exactly "
              "twelve negative entries at p = 0 with minimum -0.100, as the manuscript "
              "states; and the entire pipeline, run at n = 2, reproduces the Ising "
              "eigenvalues to 2 x 10^{-14} — the strongest cross-validation a from-scratch "
              "implementation can carry."),
        ("p", "The scan then measured the second boundary's ladder. The sector diagnostic "
              "X_L = L ln(lambda_triv/lambda_std) on the S_3 isotypic blocks crosses "
              "between sizes at 0.2712 for the pair (4, 6) and 0.2970 for the pair "
              "(6, 8), marching toward the published 0.305(3) exactly as the n = 2 ladder "
              "marched toward 0.233810 — from below, with the drift shrinking as sizes "
              "grow; the three-replica susceptibility peaks move 0.358, 0.354, 0.342 "
              "across L = 4, 6, 8 while their heights grow from effectively zero to 1.06, "
              "the same concentration signature the Ising sector showed. The verdict is "
              "that the phase diagram of the record now has two measured rungs and a "
              "certified form: the theory's second law of record thermodynamics — the ESS "
              "budget — is not an analytic object but a phase-carrying one, and any "
              "engineering use of the budget curve (the telemetry capability of Volume "
              "III) must flag two boundaries, not one. The upgrade path to the remaining "
              "rungs is now routine in a sense it was not before: the machinery that "
              "reproduced every n = 3 anchor from scratch is the same machinery at n = 4, "
              "at the cost of the bond-space growth the manuscript's iterative route "
              "already handles to L = 10."),
     ]},
    {"title": "Confrontation III: The E. coli Cycle Scan, Layer-Resolved",
     "blocks": [
        ("p", "The third order in the queue was the E. coli test of Prediction 1: that the "
              "viability cascade's approach to its asymptote across cycle index k follows "
              "1 - 0.697^k, a semi-log slope of 0.361 per cycle. The experiment was run on "
              "iJO1366 in glucose minimal medium, with the corpus's own protocol — "
              "sequential knockouts under L1-MOMA adjustment, closed cycles A to AB to B "
              "to wild type — on twenty non-degenerate viable gene pairs, sixteen "
              "traversals each. The result is not the number the prediction guessed, and "
              "it is much better than the number the prediction guessed: the LP flux layer "
              "cannot carry a per-cycle relaxation law at all, and the reason is a "
              "theorem. The knockout polytopes are nested — the double knockout's feasible "
              "set inside the single's inside the wild type's — so every restoration step "
              "of the cycle is a projection of a point already inside the target set, "
              "which is a no-op. The cycle map therefore fixes the state after exactly one "
              "traversal: all twenty pairs show D_k flat from k = 1 onward, with terminal "
              "drift D-infinity between 112.7 and 274.5 (median 228.3), every pair locked "
              "— the flux-level signature of the corpus's own non-reversion memory, "
              "saturating instantly where the theory's k-law needed it to decay "
              "geometrically."),
        ("p", "The layer above it — closed parameter cycles, the corpus's "
              "cyclic-perturbation experiment — does relax geometrically, and its rate is "
              "not 0.361 either: alternating the medium between glucose-only and a mixed "
              "corner, at loop sizes from 0.5 to 8, the residual decays with rates 0.2485, "
              "0.2483, 0.2498, 0.2525 per cycle — R-squared 1.000, stable across a "
              "sixteen-fold range of loop size. The LP layer has its own constant, set by "
              "the Friedrichs angle between the alternating polytopes, a different "
              "mechanism and a different number from the cascade's Lipschitz product. Two "
              "laws of the corpus reproduced themselves exactly along the way: the drift "
              "after one traversal follows the loop size to log-log slope 1.001 against "
              "the published 1.00, and the non-reversion drifts sit at the corpus's own "
              "scale. The cascade layer was then measured directly: the extremal "
              "seven-optic instance realizes the product bound and relaxes at 0.3605 per "
              "cycle against the certified 0.3610, and thirty generic instances all relax "
              "faster (minimum 2.60) — 0.361 is the certified slowest case, the "
              "worst-case envelope, not a typical rate."),
        ("p", "Assembled, the three layers give the session's sharpest new law. "
              "<b>THE LAYER-SEPARATION LAW.</b> In the E. coli stack, the epsilon-laws — "
              "the ones that scale with perturbation size, like the linear drift and the "
              "curvature concentration — live at the LP flux layer, where they are set by "
              "constraint geometry (Friedrichs angles, active-set boundaries); the k-laws "
              "— the ones that unfold over repeated cycles — cannot live there, because "
              "the LP layer saturates in one traversal wherever the constraint sets nest; "
              "they live in the post-translational layer the viability companion models, "
              "where they are set by Lipschitz products and are certified, not typical, "
              "rates. The law's refuter is as sharp as its content: a per-cycle geometric "
              "relaxation measured at the LP flux layer of any organism would kill it. And "
              "the law's most consequential corollary is confirmatory rather than "
              "destructive — the layer where the theory's 0.361 lives is exactly the layer "
              "the corpus's own evidence chain (protein buffering excluded, transcripts "
              "excluded, metabolite pools implicated) had already deduced the memory "
              "carrier to be. Two independent arguments, one from transcriptional "
              "correlation and one from projection geometry, land on the same layer of "
              "the cell."),
        ("table", "layers"),
        ("stats", [("0.249", "LP parameter-layer rate (R-squared 1.000)"),
                   ("1.001", "drift-vs-loop-size slope (corpus law: 1.00)"),
                   ("0.3605", "cascade extremal rate (certified 0.3610)")]),
     ]},
    {"title": "The Optic-Nehari Attack: Refuted, Repaired, Bridged",
     "blocks": [
        ("p", "The third order of the queue was stated in Volume III as the highest-value "
              "proof target in the programme: optic-Nehari for correlated composites — the "
              "claim that the best structured approximant of a correlated composite is the "
              "optic composite of the per-letter best approximants — the missing lemma of "
              "DeepSeek's Continuation A, with the intercept leakage named as the "
              "obstruction to its naive extension. The attack was mounted, and the honest "
              "outcome is a refutation, a repair, and a bridge, in that order. The "
              "refutation is a four-by-four instance with exact arithmetic: letters "
              "diag(1, 0.5) with rank-one grounded truncation classes, an in-span defect "
              "delta on the leading structured direction. The best composite approximant "
              "is (1 + delta) E — a composite of per-letter <i>class</i> elements with "
              "shifted parameters — while the composite of the per-letter <i>optima</i> is "
              "E itself; the excess of the factored choice is delta-squared, measured to "
              "slope 1.991 across three decades of defect size. The exact lemma is false "
              "for every nonzero in-span defect, and the corpus's conditional Theorem "
              "7.11 cannot be upgraded by it."),
        ("p", "The repair is a dichotomy theorem, and it is the substantive mathematics "
              "of the attack. <b>THEOREM VIII (defect stability).</b> Split the "
              "correlation defect Delta into its component in the span of the composite "
              "structured class and the transverse remainder. Then: (i) the transverse "
              "part prices the <i>value</i> — the optimal distance shifts linearly, by at "
              "most the transverse norm, for every class element equally, so it "
              "redistributes no advantage between candidates; (ii) the in-span part is "
              "absorbed to first order by the optimum — the optimal value is unchanged to "
              "machine precision in the witnesses — while it prices the <i>factorization</i> "
              "quadratically: the composite-of-optima pays the square of the in-span "
              "norm; (iii) the argmin shifts by a bounded multiple of the in-span norm "
              "over the separation margin, so the repaired lemma reads: the best "
              "composite approximant is an optic composite of per-letter class elements "
              "whose parameters are shifted by O(||Delta||/gamma); and (iv) the excess of "
              "the factored choice never exceeds twice the defect norm — the linear "
              "envelope, verified across the probed families. The theorem turns the "
              "intercept rigidity of the combs polynomial — the normalization coefficient "
              "that rescales under decoration while the constant term stands still — into "
              "a quantitative pricing rule rather than a dead end."),
        ("p", "The bridge is the attack's closing move and the one that matters most to "
              "the programme's architecture. Composing a chain of correlated stages, each "
              "with its own defect and its own Lipschitz factor, the accumulated "
              "displacement of the cascade's fixed point obeys the graded small-gain "
              "inequality — the sum of the per-stage transverse defects, each attenuated "
              "by the product of the downstream Lipschitz constants, divided by one minus "
              "the loop product — verified on twelve random five-stage chains, all inside "
              "the bound. This is exactly the inequality of Volume III's Theorem II, "
              "derived there from the thermodynamic side and reached here from the "
              "approximation-theoretic side. DeepSeek's two continuations — A, the "
              "multiletter AAK programme, and B, the Cesaro-Spohn arrow — were presented "
              "as parallel routes out of the corpus; the attack shows they converge: "
              "Continuation A's missing lemma, repaired, lands on Continuation B's "
              "inequality. The programme's two open fronts are one front."),
     ]},
]
