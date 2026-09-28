# -*- coding: utf-8 -*-
"""vol6_content_a.py — The Dictionary (Vol VI): chapters 1-7 + tables + figures."""

FIGURES = {
    "bt1a": ("/home/z/my-project/github_master/download/figures/bt1a_dictionary.png",
             "Figure 1 — The dictionary, measured on three fronts. (a) The outcome ladder as "
             "the rank filtration: the ECD five-outcome partition of a presentation, computed "
             "from the Hankel matrix of the quotient alone, as a function of the register "
             "budget b — the outcome steps from resource failure (R) to bounded success at "
             "exactly b = rank(M), the completed merged matrix's rank. (b) The quantum "
             "confrontation: the monitored-circuit strobe's reachability-Hankel rank (lambda-"
             "one-normalized transfer chain, squares) against the corpus's proved law "
             "3·2^(L/2−2) (line) at m = 2..5 — thm:rank is the R-clause of the dictionary "
             "read on the quantum interface, exact at every benchmark point and rank one at "
             "p = 1. (c) The RockSample confrontation: the E2-measured belief distortion "
             "against the interface width q (circles) and the dictionary's trajectory-level "
             "prediction (squares) — correlation 0.97, with the q = 3 structural break typed "
             "from the quantizer's own transition graph as the degenerate-completion regime."),
}

TABLES = {
    "clauses": {
        "caption": "Table 1 — The six clauses of BT1a-star: the dictionary between the "
                   "obstruction datum and the Hankel structure of the quotient, stated in "
                   "the enrichment, proved where the corpus allows, and verified",
        "header": ["Clause", "The dictionary's claim", "Proof status", "Verification"],
        "ratios": [0.13, 0.42, 0.24, 0.21],
        "font": 7.4,
        "rows": [
            ["(i) rows",
             "LocalAdm at a record is the box intersection of the fibre's Hankel rows "
             "widened by the tolerance; local failure (L) is exactly Hankel row conflict: "
             "some fibre's b-truncated rows have diameter above 2·eps",
             "PROVED (Lemma 1: a response valid for every world of the fibre is a point "
             "in every widened row; the intersection is empty exactly at the conflict)",
             "Battery: 457 L-instances typed identically from the matrix and from the "
             "presentation's own semantics"],
            ["(ii) gluing",
             "The restriction equations of the presentation are the Hankel shift "
             "equations y[q(u), a·t] = y[q(ua), t]; compatibility failure (D) is exactly "
             "the partial merged Hankel's completion obstruction: some shift-class box "
             "is empty",
             "PROVED (Lemma 2: the completion system is interval intersection plus "
             "equality propagation — union-find; decidable in near-linear time)",
             "Battery: 6 D-instances, all agreeing; the D-rung is thin (the accumulated "
             "level-crossing drift regime) — itself a finding"],
            ["(iii) wall",
             "On finite presentations effectivity failure (K) is vacuous (every box "
             "point is computable); the non-vacuous region is unbounded behaviour, and "
             "its boundary is the enrichment's own wall: the guarded trace exists iff "
             "L < 1",
             "PROVED (Finiteness Lemma + the fusion with bt3's T4/T3: geometric "
             "convergence below, first-order pole at the wall)",
             "Wall scan: closed form d* = delta/(1−L) exact to 1e-12 below; divergence "
             "above; ceiling log-log slope −1.000"],
            ["(iv) rank",
             "The minimal register realizing the merged sequential behaviour is the rank "
             "of the completed matrix M (the graded Fliess theorem: a register-n machine "
             "realizes the behaviour iff M factors through R^n; a rank-r factorization "
             "is a machine); resource failure (R) is exactly rank(M) > b",
             "PROVED (Lemma 3, both directions; the corpus's thm:rank is this clause "
             "read on the strobe interface)",
             "Register ladder 25/25 (outcome flips R to ok exactly at rank); thm:rank "
             "recovered exactly, 16/16 rows, m = 2..5"],
            ["(v) magnitude",
             "The obstruction's magnitude is the singular tail: the best register-n "
             "distortion is sigma-{n+1}(M) in the spectral norm (Eckart-Young-Mirsky for "
             "finite matrices; AAK/Nehari in the analytic Hankel case), and the "
             "entrywise tolerance-type distortion is bounded by it",
             "PROVED for finite matrices (EYM cited, equality verified); the analytic "
             "case inherited as cited, with Open 7.13's status carried honestly",
             "19/19 EYM checks (spectral equality at machine precision, entrywise "
             "bound); RockSample distortion curve at correlation 0.97"],
            ["(vi) naturality",
             "The dictionary is a morphism of sheaves on the budget lattice: "
             "post-composition by a (lambda, d)-graded morphism moves every clause by "
             "the C2 law — fibre diameters by lambda·diam + d, the L-threshold to "
             "(2·eps − d)/lambda, the register by at most +1 (the affine shift adds the "
             "rank-one constant), the tail by lambda·sigma",
             "PROVED as the C2 inequalities applied clause by clause — the morphism "
             "problem Volume V said the category finally had both sides to state",
             "80/80 on all three naturality audits (affine diameters exact, rank <= +1, "
             "sigma bounds)"],
        ],
    },
    "battery": {
        "caption": "Table 2 — The recovery battery: three presentation families engineered "
                   "to hit different rungs of the ladder, cross-checked against the register "
                   "budgets",
        "header": ["Family", "Construction", "Rung targeted", "Checks", "Agreement"],
        "ratios": [0.10, 0.38, 0.22, 0.14, 0.16],
        "font": 7.6,
        "rows": [
            ["F1",
             "random machines (3-6 states, 2 letters) with aggressive random quotients "
             "(2-6 records over 22 histories) — the observational merging far coarser "
             "than the behaviour's distinctions",
             "L (row conflicts everywhere)", "300", "300/300"],
            ["F2",
             "drift machines (states on a cycle, slowly drifting outputs) with level "
             "quotients (k = 2-4 state windows) and depth-3 tests — the accumulated "
             "level-crossing drift along deep shift chains",
             "D (gluing breaks while every "
             "single fibre stays admissible)", "100", "100/100"],
            ["F3",
             "random machines (4-8 states) with level quotients (k = 2-5), scanned over "
             "register budgets b in {1, 2, 3, 99}",
             "R and ok (rank vs budget)", "200", "200/200"],
            ["all",
             "outcome tally across the 600 checks: L 457, D 6, K 0, R 52, ok 85 — K "
             "exactly zero, as the Finiteness Lemma predicts; rank stability across "
             "in-box completion samples: 70.1% with zero spread (max spread 4, the "
             "completion-choice effect recorded honestly)",
             "the five-rung partition, "
             "populated", "600", "600/600"],
        ],
    },
    "corpus": {
        "caption": "Table 3 — The two corpus confrontations: the dictionary read on the "
                   "quantum strobe and on the RockSample compressor",
        "header": ["Instance", "The corpus's object", "The dictionary's reading", "Verdict"],
        "ratios": [0.12, 0.28, 0.36, 0.24],
        "font": 7.4,
        "rows": [
            ["quantum",
             "the monitored-circuit strobe (qc_v22, thm:rank): the compressed transfer "
             "operator on the bond space 2^(L/2) has rank exactly 3·2^(L/2−2) for "
             "p in [0,1), rank 1 at p = 1",
             "the quotient is the bond compression (2^L to 2^(L/2)); the merged "
             "behaviour's reachability Hankel is the stacked powers of the "
             "lambda-one-normalized operator; its rank is the interface's residual "
             "register — the R-clause read on the corpus's own interface",
             "EXACT: 16/16 rows (m = 2..5, the manuscript's benchmark p's and the "
             "p = 1 endpoint); the p to 1 interior is numerically degenerate toward "
             "the endpoint collapse — the exact statement there rests on the corpus's "
             "own Z[p] certificates"],
            ["RockSample",
             "the E2 compression scan (Vol V): q = 2 blind commit (value 14.94 above "
             "the exact 14.21, distortion 0.124), q = 3 structural break (3.40, "
             "0.2965, 'the belief resets to the prior on every read'), q = 4 partial "
             "(10.50), q >= 5 full (~14.2)",
             "the q-level compressor is the presentation's quotient; the completion "
             "question is the quantized transition graph on levels, typed from the "
             "prior level per read: ATOMIC (jump to an extreme), ABSORBED (return to "
             "the prior), GRADUAL (an intermediate level — accumulation)",
             "TYPED: q = 2 all-atomic (9/9 reads commit, mean 1.0 reads — the blind "
             "interface); q = 3 atomic+absorbed with ZERO gradual reads (14 absorbed, "
             "4 atomic) — the degenerate completion, the measured break; q = 4 nine "
             "gradual reads (partial); q >= 5 sixteen gradual (full). The "
             "trajectory-level distortion predictor tracks the E2 curve at "
             "correlation 0.97"],
        ],
    },
    "ledger": {
        "caption": "Table 4 — The bridge ledger after this volume: the DeepSeek six, "
                   "re-adjudicated",
        "header": ["Theorem", "As DeepSeek stated it", "Status at the close of Volume V",
                   "Status after this volume"],
        "ratios": [0.09, 0.27, 0.31, 0.33],
        "font": 7.4,
        "rows": [
            ["BT1a",
             "the obstruction datum is isomorphic to the viability curvature (one "
             "arrow)",
             "the sole deep open link: the dictionary-plus-recovery theorem between "
             "the extensional diagnostics and the operator structure, with the "
             "enrichment now existing to state it",
             "CLOSED IN THE COMPUTABLE PART: stated as a sheaf morphism "
             "(BT1a-star), six clauses proved (rows, gluing, wall, rank, magnitude, "
             "naturality), the recovery verified 600/600, and the corpus confronted "
             "twice. The analytic generality remains open and is now the ONLY "
             "remainder of this link"],
            ["BT1",
             "o(P) in H-squared is isomorphic to the curvature",
             "two-step chain with BT1a open, the other links proved",
             "UNCHANGED where it was proved; the open first link is now bounded to "
             "the analytic case — the finite and graded part is a theorem"],
            ["BT2",
             "R(D) is the minimum per-optic Lipschitz constant",
             "closed as far as the corpus allows (the ceiling identity, the exact "
             "quadratic gap, the thin equality locus)",
             "STRENGTHENED: the magnitude clause identifies the sandwich's floor "
             "side with the Hankel singular tail — the floor inherits Open 7.13 "
             "through the same AAK boundary the dictionary now names"],
            ["BT3",
             "the intercept principle is fixed-point non-existence",
             "DONE: built, retyped, proved (the budget dichotomy)",
             "STRENGTHENED: the wall is now load-bearing twice — it is also the "
             "K-rung of the obstruction ladder (the effectivity boundary), fusing "
             "the dichotomy with the diagnostics"],
        ],
    },
}

CHAPTERS_A = [
    {"title": "The Order and the State",
     "blocks": [
        ("p", "The order for this session was fixed before the session began: attack "
              "BT1a inside the new enrichment, because the category now exists to state "
              "it, and push everything, including anything from the previous round that "
              "had not been pushed. The first half of the order was administrative and "
              "was executed first: eight files from the Volume V round — the volume "
              "extracts, the body and cover PDFs, the benchmark log, and the tail "
              "content module — were committed and pushed as adb26b4 before any new "
              "mathematics was written. The second half is this volume."),
        ("p", "The state the order inherited is recorded in Volume V's closing chapter, "
              "and its last mathematical sentence is the one this session takes as its "
              "mandate: with BT3 built and BT2 closed to the corpus's own conditional "
              "ceiling, BT1a is no longer one of three open links but the one, and the "
              "enrichment now exists to state it in — the obstruction datum is a section "
              "of the budget lattice's failure sheaf, and its identification with Hankel "
              "structure is a morphism problem in a category that finally has both "
              "sides. That sentence was a promise: it named where BT1a should live "
              "without saying what it says there. This volume cashes the promise. The "
              "statement is made precise, its parts are proved where the corpus's own "
              "foundations allow, the parts that close are confronted with the corpus's "
              "hardest instances, and the parts that do not close are bounded to a "
              "single named boundary — the analytic case, the same boundary that Open "
              "7.13 has been carrying honestly since Volume II."),
        ("p", "What BT1a demands, in Volume II's words, is a dictionary-plus-recovery "
              "theorem: a theorem that recovers the five diagnostic outcomes and the "
              "nested-space filtration from the Hankel structure of the quotient — and "
              "nothing else. The demand decomposes, once the enrichment supplies the "
              "typing, into six clauses, and the six clauses are not equally hard. The "
              "row dictionary is a definition chase with content. The gluing dictionary "
              "turns ECD's restriction equations into the Hankel shift equations and "
              "inherits a classical decidability. The rank dictionary is the weighted-"
              "realization theorem the automata monograph already carries, now graded. "
              "The magnitude dictionary is Eckart-Young-Mirsky on the finite side and "
              "AAK on the analytic side, and the boundary between them is honest. The "
              "finiteness lemma is trivial and load-bearing: it says exactly where the "
              "hardest rung of the ladder can and cannot live. And naturality is the "
              "C2 law of the enrichment applied clause by clause — the morphism "
              "problem, solved by the category it was stated in."),
     ]},

    {"title": "The Statement: BT1a-Star in the Enrichment",
     "blocks": [
        ("p", "Fix the cost-enriched graded category of interfaces built in Volume V: "
              "the affine cost monoid Q of (lambda, d) pairs, the budget filtration on "
              "hom-sets, the decoration endomorphism, and the guarded trace. Its finite "
              "part is where the statement lives. A presentation there consists of a "
              "sequential behaviour f from input histories to a normed value space — "
              "the corpus's weighted-automaton normal form, with the Hankel shift law "
              "f(u·a·t) = f(ua·t) automatic; a family of tests t with monotone costs, "
              "so that the budget b truncates the tests to those of cost at most b and "
              "the truncation is closed under taking suffixes; an observational "
              "quotient q merging the histories the interface can distinguish; a "
              "tolerance eps; and a register budget b."),
        ("p", "On one side stands the obstruction datum, exactly as the halting-physics "
              "monograph defines it: the local-success bit together with the nested "
              "spaces of global families, cutting every presentation into one of five "
              "outcomes — local failure, compatibility failure, effectivity failure, "
              "resource failure, or bounded success — asked in that order. As eps and "
              "b vary, the outcome assignment sweeps a monotone section over the "
              "budget lattice: the failure sheaf. On the other side stands the Hankel "
              "matrix of the behaviour, its fibre-row structure under the quotient, "
              "the partial merged Hankel with its shift-equivalence classes, the "
              "completed matrix with its rank and singular values: the spectral sheaf, "
              "over the same lattice."),
        ("p", "BT1a-star is the claim that there is a morphism of sheaves between them — "
              "the dictionary Phi — with the obstruction datum equal to the dictionary "
              "applied to the spectrum. The morphism is not a metaphor: it is a "
              "commutation requirement with the budget lattice's own action, and the "
              "action is the C2 grading of the enrichment, so the dictionary is "
              "natural precisely when its clauses move under post-composition the way "
              "the cost algebra says they must. The six clauses of Table 1 are the "
              "component statements of this one morphism, one per rung of the "
              "diagnostic ladder plus the naturality that binds them. Each is stated, "
              "proved where it closes, and verified; the balance of this volume walks "
              "them in order, then confronts the corpus, then keeps the ledger."),
        ("quote", "An isomorphism is checkable only in the whole; a chain is checkable "
                  "link by link. A sheaf morphism is checkable stalk by stalk — and "
                  "the budget lattice supplies the stalks."),
     ]},

    {"title": "Clause One: The Row Dictionary",
     "blocks": [
        ("p", "Local failure is Hankel row conflict. The proof is short enough to give "
              "in full, because its shortness is the point: the enrichment's typing "
              "makes the identification nearly forced. A response at a record r is "
              "admissible at tolerance eps when it is valid for every world the "
              "interface has merged into r — that is, when its value at every test t "
              "lies within eps of the behaviour's value f(u·t) for every history u in "
              "the fibre. The set of admissible responses is therefore the "
              "intersection, test by test, of the intervals obtained by widening each "
              "fibre row's entries by eps. That intersection is empty exactly when "
              "some test sees two worlds of the same fibre whose values differ by more "
              "than twice the tolerance — which is to say, exactly when the fibre's "
              "b-truncated Hankel rows have diameter above 2·eps. The merged record "
              "cannot serve what it has merged: distinct rows are fibre conflicts, "
              "verbatim as Volume II's dictionary demanded."),
        ("p", "The battery stresses the clause three hundred times over: family F1 "
              "generates random machines under aggressive random quotients, where the "
              "observational merging is far coarser than the behaviour's distinctions "
              "and local failure is the generic outcome. The dictionary, computed from "
              "the matrix alone — fibre row diameters, nothing else — types every one "
              "of the four hundred and fifty-seven L-instances identically to the "
              "presentation's own set-theoretic semantics. The agreement is not "
              "surprising once the lemma is proved, and that is the honest form of the "
              "result: the surprise was Volume II's, when the identification was a "
              "conjecture without a proof; the proof turns the conjecture into an "
              "audit, and the audit passes."),
        ("p", "One constant deserves its own sentence, because it is the kind of detail "
              "that separates a dictionary from an analogy: the conflict threshold is "
              "2·eps, not eps, and the reason is the geometry of the admissible set. A "
              "single response must stand within eps of every world it serves, so the "
              "worlds may disagree with each other by up to twice the tolerance before "
              "no server exists. The constant is forced by the ball-intersection "
              "structure, it is the same constant the monograph's local-admissibility "
              "definition carries implicitly, and getting it wrong would mispredict "
              "every boundary instance in the battery. The dictionary gets it right "
              "because it is not translating between two formalisms — it is reading "
              "one object through two notations."),
     ]},

    {"title": "Clause Two: The Gluing Dictionary",
     "blocks": [
        ("p", "Compatibility failure is the partial Hankel's completion obstruction. "
              "The identification has two halves, and both are theorem-shaped. First: "
              "the restriction equations of the presentation — the diagrams a global "
              "family must commute with, ECD's compatibility — are, in interface "
              "language, exactly the Hankel shift equations. A global family assigns a "
              "response value to every record-and-test pair; the restriction equations "
              "force the assignment to cohere across the input dynamics, and the "
              "coherence condition is that the value at the record of u followed by "
              "the test a·t equals the value at the record of ua followed by the test "
              "t. That is the shift-invariance law of a sequential behaviour's Hankel "
              "matrix, verbatim. Second: the family space is the solution set of those "
              "equations within the admissibility boxes, and because the equations are "
              "equalities between variables while the boxes are intervals, the "
              "solution set is computed by propagating the equalities — a union-find "
              "over the variables, each class carrying the intersection of its "
              "members' boxes. Gluing fails exactly when some class box is empty: "
              "locally every fibre is servable, but the equations chain the services "
              "together and the chained intervals miss."),
        ("p", "This is the classical partial realization problem — completing partial "
              "Markov-parameter data to a sequential behaviour — arriving inside the "
              "programme's own diagnostics, and it carries the classical problem's "
              "decidability with it: interval intersection plus equality propagation "
              "is near-linear time. The battery's family F2 hunts the rung with "
              "machines built for it: drift machines whose states ride a cycle with "
              "slowly drifting outputs, presented through level quotients and read by "
              "depth-3 tests. The mechanism is accumulation: each single fibre of the "
              "quotient stays within the tolerance — no row conflict, local "
              "admissibility everywhere — but the shift equations chain three boxes "
              "deep and the level-crossing drift adds up along the chain until the "
              "intersection empties. Six of the six hundred checks land on the D-rung, "
              "every one typed identically from the matrix and from the semantics, "
              "and the thinness of the rung is itself a measurement: compatibility "
              "failure lives in a narrow regime of tolerance against quantization "
              "step, which is the abstract form of exactly the phenomenon the "
              "RockSample compressor measures at q = 3."),
        ("p", "The D-rung's dictionary also settles a question Volume II left implicit: "
              "why the gluing obstruction has no cohomological shadow in the corpus. "
              "The monograph is explicit that no cohomological completeness is "
              "inferred, and the dictionary explains the restraint: the gluing "
              "obstruction here is an interval emptiness on a finite chain of "
              "equalities — decidable, constructible, witness-carrying — not a "
              "torsion class. DeepSeek's instinct to reach for H-squared was the "
              "idealization; the honest object is the completion system, and its "
              "decidability is what makes the bridge paper's second rung a theorem "
              "rather than a programme."),
     ]},

    {"title": "Clause Three: The Finiteness Lemma and the Wall",
     "blocks": [
        ("p", "Effectivity failure is the enrichment's wall. The clause has two "
              "halves, one trivial and one deep, and the trivial one is load-bearing. "
              "The finiteness lemma: on a finite presentation, every solution of the "
              "completion system is a finite object with rational-bounded coordinates, "
              "hence computable; the effective family space is the whole family "
              "space, and the K-rung is empty. The battery confirms the emptiness "
              "directly — zero K-outcomes in six hundred checks — which is the "
              "unusual case of a theorem being verified by the absence of its "
              "counterexamples: the lemma predicts the tally, and the tally obeys. "
              "The lemma's function is to locate the rung's non-vacuous region: "
              "unbounded behaviour, where the completion system is infinite and the "
              "question of a computable solution becomes real."),
        ("p", "And there, the enrichment's own wall is the boundary. The non-vacuous "
              "region is governed by the guarded trace — the feedback loop's "
              "distortion accounting, Volume V's T4 — which exists exactly when the "
              "loop's contraction L is below one: below, the unrolled costs converge "
              "geometrically to the closed form, and the convergence is effective, "
              "computable to any demanded precision in logarithmically many steps; at "
              "the wall, the closed form's ceiling is a first-order pole; above, the "
              "unrolling diverges and no effective procedure exists at all. The wall "
              "scan re-measures the three regimes in this session's arithmetic: the "
              "closed form holds to one part in ten to the twelve below, the "
              "divergence is confirmed above, and the ceiling's log-log slope at the "
              "wall is minus one to three decimals — the budget-lattice instance of "
              "the one-wall law, now doing double duty. It was already the intercept "
              "principle's fixed-point boundary; it is now also the effectivity "
              "boundary of the obstruction ladder. The K-rung of BT1a and the "
              "dichotomy law of BT3 are the same wall seen from two sides, which is "
              "the kind of coincidence the programme has learned to call a fusion "
              "rather than an accident."),
        ("p", "The honest boundary of the clause is the no-go territory: beyond the "
              "wall, the corpus's own undecidability results — the halting-side "
              "statements the monograph carries — are what makes the effectivity "
              "question non-trivial, and the dictionary does not and cannot resolve "
              "them; it locates them. That localization is the clause's contribution: "
              "the deepest rung of the diagnostic ladder no longer floats free of the "
              "enrichment's arithmetic — it is pinned to L = 1, where the pole lives."),
     ]},

    {"title": "Clause Four: The Rank Dictionary and the Ladder",
     "blocks": [
        ("p", "Resource failure is rank. The clause is the graded form of the "
              "weighted-realization theorem the automata monograph has carried since "
              "its first version: a register of size n realizes the merged behaviour "
              "on the truncated tests exactly when the completed matrix factors "
              "through an n-dimensional space — rank at most n — and conversely every "
              "rank-r factorization of the matrix assembles into a machine with "
              "r states, the shift-consistency of the completed matrix making the "
              "transition structure well-defined. The proof is two constructions, one "
              "in each direction, both elementary; the grading's contribution is that "
              "the theorem now holds at every test budget, because monotone test "
              "costs make the truncation suffix-closed and the shift equations "
              "respect it."),
        ("p", "The ladder theorem is the clause's other half, and it is where Volume "
              "II's metaphor — the rank filtration is the ladder the nested spaces "
              "climb — becomes a pair of measured monotonicities. In the register "
              "coordinate: hold the tolerance and the resolution fixed, and sweep "
              "the budget b; the outcome steps from resource failure to bounded "
              "success at exactly b equal to the completed matrix's rank — a "
              "staircase with its tread at the rank, verified in every eligible "
              "instance of the battery, twenty-five of twenty-five. In the "
              "resolution coordinate: hold the tolerance and the register fixed, and "
              "sweep the test budget c; the register needed is nondecreasing along "
              "the feasible regime — seventy-nine of eighty, the one exception "
              "recorded with its completion-choice explanation — and the outcome "
              "itself is antitone: obstructions appear as resolution grows and never "
              "vanish, eighty of eighty. Coarse interfaces cannot see their own "
              "defects; resolution is what exposes them; and the nested spaces "
              "Gamma-set containing Gamma-eff containing Gamma-B climb exactly the "
              "rank filtration while it happens. The resolution window — the "
              "metabolic manuscript's h below sigma below L — has found its "
              "interface-side avatar."),
        ("p", "The corpus confrontation is immediate and exact. The monitored-circuit "
              "strobe of the quantum manuscript is an interface: the bond compression "
              "is its observational quotient, the compressed transfer operator is its "
              "merged behaviour, and the reachability Hankel — the stacked powers of "
              "the lambda-one-normalized operator, the corpus's own normalization "
              "convention — has rank exactly equal to the operator's rank. The "
              "manuscript's thm:rank says that rank is 3·2^(L/2−2), independent of "
              "the monitoring rate, with rank one at full monitoring. The dictionary "
              "recovers it: sixteen rows across m = 2 to 5 at the manuscript's "
              "released benchmark rates and the full-monitoring endpoint, every row "
              "matching the proved law exactly under the normalized stack with "
              "relative tolerance. The corpus's rank theorem was proved by "
              "certificate arithmetic over the integers; the dictionary reads it off "
              "the Hankel structure; the two derivations agree, which is the "
              "confrontation's whole content — the R-clause of BT1a is not merely "
              "analogous to thm:rank, it is thm:rank, restated in the category where "
              "the obstruction datum lives."),
     ]},

    {"title": "Clause Five: The Magnitude Dictionary",
     "blocks": [
        ("p", "The obstruction's magnitude is the singular tail. Where exact "
              "realization fails, Volume II demanded, the singular values measure the "
              "obstruction's size; the demand sharpens, inside the dictionary, into "
              "two statements with different statuses. On finite matrices: the best "
              "achievable distortion of a register-n interface is the (n+1)-st "
              "singular value of the completed matrix in the spectral norm — the "
              "Eckart-Young-Mirsky theorem, cited and verified, with the entrywise "
              "tolerance-type distortion bounded by the same value, since the "
              "spectral norm dominates every entry. Nineteen of nineteen checks "
              "pass at machine precision. On analytic Hankel operators: the same "
              "statement with operator norms and analytic rank is the "
              "Adamyan-Arov-Krein and Nehari theory, and it is inherited as cited, "
              "with its multiletter unconditional-floor question — Open 7.13, "
              "carried honestly since Volume II — attached to it by name. The "
              "boundary between proved and inherited is exactly the boundary between "
              "the finite part of the category and its analytic completion, and the "
              "volume does not blur it."),
        ("p", "The clause earns its place in the bridge ledger through what it does to "
              "BT2's sandwich. The graded small-gain law closes the ceiling at the "
              "guarded-trace identity; the floor was the AAK converse, conditional on "
              "the open multiletter characterization. The magnitude clause now "
              "identifies the floor with the Hankel singular tail of the same "
              "completed matrix the dictionary already reads for its rank clause — "
              "the sandwich's two sides are two singular indices of one object, the "
              "ceiling the guarded trace of the loop and the floor the tail beyond "
              "the budget. The equality locus between them, measured thin in Volume "
              "V, is thereby the question of when the trace's closed form meets the "
              "tail's truncation — a single question about one matrix rather than a "
              "confrontation between two theories. The unification the programme was "
              "asked for, on this clause, is literal."),
        ("p", "The RockSample confrontation gives the magnitude clause its empirical "
              "face, and its honest anomaly. The distortion the compressor inflicts "
              "is predicted at the trajectory level — the single-rock Wald walk with "
              "the stopping rule acting on the quantized belief, because the policy "
              "acts on what it sees — and the prediction tracks the measured E2 "
              "curve at correlation 0.97 across six widths. The single-step "
              "quantization error does not track it, and the gap is the clause's "
              "content: at the degenerate width q = 3, the distortion is not the "
              "rounding error of one update but the accumulated divergence of a "
              "stuck belief from a walking truth — the absorbing dynamics the "
              "gluing clause names, priced by the magnitude clause. The q = 2 anomaly "
              "is recorded with equal honesty: the distortion is predicted, the "
              "value is not monotone in it, because committing early wins in this "
              "environment — the value functional exploits the blind interface, "
              "which is a fact about RockSample, not a failure of the dictionary."),
     ]},
]
