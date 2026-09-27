# -*- coding: utf-8 -*-
"""bt_content_a.py — The Bridge Theorems (Vol II): chapters 1-6 + tables (content module)."""

FIGURE_DIAGRAM = "/home/z/my-project/scripts/diagram_bridge.png"

TABLES = {
    "audit": {
        "caption": "Table 1 — The audit: DeepSeek's points against Volume I and against this volume",
        "header": ["DeepSeek's point", "In Volume I", "In this volume"],
        "ratios": [0.36, 0.27, 0.37],
        "font": 7.9,
        "rows": [
            ["The natural bridge: policies are transducers, sensors are rate constraints, obstructions are lower bounds on rate", "Absorbed as-is — the spine of its Chapters 2–4 and Tables 1–3", "Confirmed, and extended to all thirteen corpus lines"],
            ["Bridge Theorem 1: the obstruction datum is isomorphic to the viability curvature", "Never stated; DeepSeek's formulation not discussed anywhere", "Corrected to the two-step chain (BT1); the open link isolated and named"],
            ["Bridge Theorem 2: R(D) equals the minimum per-optic Lipschitz constant", "Never stated", "Corrected to the sandwich (BT2): Lipschitz achievability against AAK converse"],
            ["Bridge Theorem 3: the intercept principle is fixed-point non-existence", "Never stated", "Corrected to enrichment-first (BT3); proved halves separated from the sketch"],
            ["The earlier avatars: Theorem A (rate–obstruction duality), B (AAK–sheaf), C (determination index = slope)", "Absent — only the opus-5 avatar (obstruction = qualitative Hankel spectrum) appears", "Retyped: B is ill-typed and repaired; C survives as a corollary-candidate of BT2"],
            ["The transfer principle: adjoint existence, vanishing obstruction, and the rate floor as one statement", "Absent", "Stated as the target theorem of the bridge paper, retyped in the graded home"],
            ["Two clusters; the chess paper is an outlier that should stay separate", "Silently overridden — the chess paper was given its own chapter", "Corrected on the facts (six roles, not five) and re-derived: instance, not pillar"],
            ["Risk: forced marriage — juxtaposition posing as unification", "Answered implicitly, by the docking-without-forcing argument", "Made explicit; the corrected theorems are falsifiable targets"],
            ["Risk: a quantitative sheaf theory is needed and does not yet exist", "Implicit — the graded category proposed as the compositional home", "Promoted from risk to prerequisite: the enrichment is the load-bearing gap"],
            ["Risk: the 238-page problem, and the staged publication path", "Not addressed", "The path updated against the live submission pipeline (Chapter 8)"],
            ["Risk: community reception — concrete algorithms or nothing", "Not addressed", "Answered from the corpus: certifying DP, Z3 closures, E. coli, chess amplification"],
            ["Risk: the curvature may be formal, defined by decree", "Partially — the r = +0.395 differential is displayed", "Answered as predictor; the isomorphism question isolated as BT1a"],
            ["Risk: optics are deterministic and cannot carry partial observability", "Not addressed", "Answered: the StCon(B) sheaf carries observability, optics carry wiring"],
            ["Risk: the homotopy fixed-point extension may be vacuous", "Partially — proof-sketch status honestly flagged", "The content condition stated: existence and non-existence cases both named"],
            ["The two continuations: multiletter AAK via optic composition; Cesaro–Spohn and the arrow of time", "Not addressed — multiletter AAK listed as open, the arrow of time never mentioned", "Both stated, as a proof strategy and as a conjecture with witnesses (Chapter 9)"],
        ],
    },
    "theorems": {
        "caption": "Table 2 — The bridge theorems: as DeepSeek stated them, as the corpus supports them, corrected",
        "header": ["DeepSeek's statement", "What the corpus actually proves", "The corrected statement", "Status"],
        "ratios": [0.23, 0.27, 0.32, 0.18],
        "font": 7.7,
        "rows": [
            ["BT1: o(P) ∈ H<super>2</super>(U,F) is isomorphic to Ω<sub>viab</sub> — an isomorphism, not an analogy",
             "The datum is λ<sub>ε</sub> plus the nested spaces Γ<sub>set</sub> ⊇ Γ<sub>eff</sub> ⊇ Γ<sub>B</sub>; ECD v47 itself: “no cohomological completeness statement is inferred”",
             "A two-step chain: obstruction ↔ Hankel row and rank structure (open); spectrum → curvature (the refinement–resolution bridge, proved); curvature → regulation (small-loop holonomy, proved, with data)",
             "One open link"],
            ["BT2: R(D) is the minimum per-optic Lipschitz constant of an optic implementing the transducer",
             "Per-optic analytic Lipschitz bounds and the Banach contraction 0.697 of the KM-averaged seven-map update (achievability); AAK/Nehari floors (converse)",
             "The sandwich: σ<sub>k+1</sub> bounds D*(k) from below, the optic chain's constants bound achievable distortion from above; equality at the optimum is the graded small-gain law",
             "Both sides proved; equality open"],
            ["BT3: the intercept principle is equivalent to non-existence of a fixed point of the homotopy extension",
             "Intercept: no right or left adjoint, affine non-representability, the no-programming theorem (proved); contraction and terminal-coalgebra maxRAF give existence (proved); the HoTT extension is proof-sketch",
             "Enrichment first: once the cost-enriched graded category is built, the intercept becomes non-existence of a fixed point of the currying endomorphism, and the two proved halves become cases of one theorem",
             "Blocked on the enrichment"],
            ["Theorem A: R(D) equals the minimum over sheaf-theoretic refinements of the obstruction datum",
             "Not attempted; as stated it equates a real-valued function with a class-valued invariant",
             "The zero-slice shadow survives retyping: R(0) is bounded below by the log of the rank-ladder level; the general statement is BT2's sandwich",
             "Retyped"],
            ["Theorem B: Hankel singular values are exactly the dimensions of sheaf cohomology groups",
             "Rank and row distinctions are the integer facts; singular values are the metric relaxation",
             "Rank ↔ interface dimension; distinct rows ↔ fibre conflicts; σ<sub>k</sub> ↔ metric obstruction — the integer and real shadows of one ladder",
             "Ill-typed; repaired"],
            ["Theorem C: the determination index equals the slope of R(D) at the optimal point",
             "The determination-index calculus is proved, as the computational face of the frontier",
             "Survives as a corollary-candidate of BT2: the slope interpretation is what the sandwich would fix at the optimum",
             "Well-typed; open"],
        ],
    },
    "risks": {
        "caption": "Table 3 — The risk register: DeepSeek's risks, the corpus's answers, the residuals",
        "header": ["DeepSeek's risk", "The corpus's answer", "Residual"],
        "ratios": [0.29, 0.45, 0.26],
        "font": 8.0,
        "rows": [
            ["Forced marriage: the frameworks share a theme, not mathematics",
             "Thirteen lines dock without forcing; the two-step chain makes the identification checkable link by link; the quantum papers supply the hard instances that would falsify BT1a",
             "Until BT1a is proved, the charge stands in weakened form"],
            ["A quantitative sheaf theory is required and immature",
             "Confirmed — and promoted: the cost-enriched graded category is the prerequisite construction, named as such rather than deplored",
             "The enrichment itself"],
            ["The 238-page problem; publication strategy",
             "The corpus's own status discipline (proof manifest, compendium, honest statuses) plus the staged path updated in Chapter 8",
             "Editorial labour only"],
            ["Community reception: category theory must yield algorithms",
             "The certificate discipline is the answer: certifying DP with width guarantees, Z3 exact closures, Lean InterceptCert, E. coli r-values, the chess amplification theorem with empirical wins",
             "The bridge paper must lead with the sandwich, not the vocabulary"],
            ["The curvature may be formal, defined by decree",
             "It predicts where regulation lives — r = +0.395 against a −0.083 null, 93.4–100% of second-order response at boundaries — which is substantive as a predictor",
             "Predictive content is separate from the isomorphism BT1a"],
            ["Optics are deterministic; partial observability does not fit",
             "The StCon(B) sheaf carries observability — the compatibility rung made functorial — while optics carry the wiring; the pair is, in substance, the monadic extension DeepSeek demanded",
             "The pairing should be stated as one construction"],
            ["The homotopy fixed-point extension may be vacuous",
             "The corpus itself marks it proof-sketch; the content condition is now explicit — existence cases (contraction, maxRAF) and non-existence cases (intercept) must both derive from one statement",
             "The HoTT section remains a sketch"],
            ["Empirical validation is biological, not AI",
             "The chess society is the AI-side instance: six roles, CSR state sufficiency, Theorem 2* amplification, wins against monolithic baselines",
             "No POMDP-benchmark paper yet — the one empty cell of the grid"],
        ],
    },
}

CHAPTERS_A = [
{
"title": "What DeepSeek Actually Demanded",
"blocks": [
("p", "The DeepSeek conversation is a fifth synthesis of the corpus — earlier than the four recorded in the master file, and stricter than any of them. Across its full arc it moved from venue scouting, through a gap analysis of AI-adjacent theory, to a demand that the corpus be unified — and it refused to let the word “unified” be used loosely. Its position condensed into three rulings. First, the natural bridge: a policy is a transducer, a sensor limitation is a rate constraint, an obstruction is a lower bound on rate — the two pillars already speak about the same objects in different languages. Second, the dictionary is not the unification: “whether it constitutes a genuine unification or merely a juxtaposition depends on whether you can prove a theorem that neither framework can prove alone.” Third, the critical tests: after reading the viability pair, it named three bridge theorems — obstruction datum isomorphic to viability curvature; the rate–distortion function equal to a minimum per-optic Lipschitz constant; the intercept principle equivalent to fixed-point non-existence — and delivered the verdict this volume takes as its brief."),
("quote", "The bridge is constructible; it is not yet constructed. … But could is not does. The unification is a research program, not a result."),
("p", "DeepSeek also supplied the apparatus around the theorems: an earlier triad of candidate theorems (A, B, C) that it later sharpened; a transfer principle joining adjoint existence, vanishing obstruction, and the rate floor; a two-cluster reading in which the physics trio, causal descent, and bounded transduction could merge while the chess paper stayed separate; a staged publication path beginning with a fifteen-to-twenty-page bridge paper; two rounds of named risks — forced marriage, the missing quantitative sheaf theory, the 238-page problem, community reception, then curvature-by-decree, deterministic optics, a possibly vacuous homotopy extension, and biological-only validation; and, at the very end, two offered continuations: a constructive proof of the multiletter AAK theorem via optic composition, or stationary Cesaro aggregation connected to the Spohn entropy-production formula in an arrow-of-time theorem."),
("p", "The question this volume answers is blunt: did Volume I build these bridges, and did it address these points? The answer, established item by item in the next chapter, is that Volume I built the dictionary and the docking grid — one legitimate layer of bridge-building, and the layer DeepSeek itself supplied first — but it did not state DeepSeek's theorems, did not adjudicate them, did not correct them, silently overrode its chess verdict, and dropped its path and its two continuations. Volume I was built on the master file's four syntheses; the DeepSeek conversation is a fifth synthesis with its own demands, and it deserved explicit adjudication rather than silent absorption. This volume supplies that adjudication — and then does the part of the bridge-building that can honestly be done without proving new mathematics: restating each theorem in a form the corpus actually supports, correcting the statements that the corpus contradicts, isolating each one's open core, and docking the two continuations."),
]},
{
"title": "The Audit: What Volume I Did and Did Not Do",
"blocks": [
("p", "“Building the bridges” resolves into three levels, and the audit must keep them apart. Level one is the dictionary: the Rosetta table, the slot-grid, the corpus map — the demonstration that every line of work studies the same factorization constraint under different names. Level two is the theorem layer: bridge statements, well typed against the corpus, each with a status and a proof strategy. Level three is the proofs themselves. DeepSeek's demand was explicit that level one does not suffice: a dictionary is what it offered for free, and the theorems are what it demanded."),
("p", "Volume I delivered level one, fully and well. Its Tables 1 and 3 are the Rosetta table and the docking grid; its Chapter 4 builds the Hankel bridge; its Chapter 12 proposes the compositional home. On level two it delivered one avatar — opus 5's identification of the obstruction datum with the qualitative Hankel spectrum — stated as the corpus's headline reading, but without proof status, without DeepSeek's competing formulation, and without the corrections that a line-level reading of the sources forces. On level three it claimed nothing, correctly: no honest document could. What it did not do was the adjudication. DeepSeek's fifteen specific points — the three bridge theorems, the earlier triad, the transfer principle, the cluster verdict, the eight risks, the staged path, the two continuations — meet the reader of Volume I nowhere. Five of them are absorbed implicitly where DeepSeek's view coincided with the four-model synthesis; one, the chess verdict, is silently overridden; the rest are simply absent. Table 1 records the full reckoning."),
("table", "audit"),
("p", "The pattern in the table is instructive, and owning it is the point of this chapter. Where DeepSeek's reading agreed with the master file's syntheses, its points were absorbed and their origin went uncredited. Where it disagreed — on the chess paper — Volume I followed the four models and let the disagreement pass in silence, which is the worst of the available options: the reader cannot tell an override from an oversight. And where DeepSeek was specific to DeepSeek — the exact statements of the bridge theorems, the risk register, the staged path, the two continuations — the points were dropped, though they are precisely the parts of that conversation with research content. The corrections that follow are therefore not decorative: each one moves a DeepSeek claim to a statement the corpus either proves or isolates as open, and each is grounded in a line-level citation rather than a recollection."),
]},
{
"title": "Correction One: What the Obstruction Datum Actually Is",
"blocks": [
("p", "DeepSeek's Bridge Theorem 1, in both of its avatars, rests on a characterization of the obstruction datum that the corpus does not support. Its statement: “The obstruction datum from causal descent is a cohomological invariant o(P) ∈ H<super>2</super>(U, F) that measures the failure of local-to-global assembly.” The actual object, in the current monograph (v47), is the extensional obstruction datum of the section “Well-formedness, semantic outcomes, and transport”: the local-success bit λ<sub>ε</sub> together with the nested global spaces Γ<sub>set</sub> ⊇ Γ<sub>eff</sub> ⊇ Γ<sub>B</sub> — a record of which of the five diagnostic outcomes (local failure, compatibility failure, effectivity failure, resource failure, bounded success) obtains, and where. It is set-level and extensional. It carries a transport proposition and a diagnostic-equivalence discipline, and the monograph is explicit about its reach: the gluing results concern graphs of bijective binary constraints, and “no higher-arity, homotopy, or cohomological completeness statement is inferred.”"),
("p", "The correction matters because the shape of DeepSeek's theorem is an isomorphism claim, and isomorphism claims are exactly as strong as their typing. Equating a nested-space record with a differential-geometric curvature form is not a theorem-shaped sentence until some functor carries one to the other — and the corpus deliberately declines to assert that such a functor exists. Two readings of DeepSeek's intent are possible. The charitable reading is that it idealized the datum into a Čech-style shadow and equated the shadows; then the theorem has a missing construction — the shadow itself — as its first obligation. The strict reading is that the statement is ill-typed as written. Either way the repair is the same: the identification must be factorized, and the corpus already supplies the factorization — through the Hankel spectrum."),
("p", "The well-typed version of DeepSeek's intuition is the one the four models converged on, and it is the first link of the corrected chain: distinct Hankel rows are fibre conflicts (merged histories with incompatible obligations — the local-failure witness, in the first pillar's vocabulary); the Hankel rank is the minimal interface size for exact realizability; the rank filtration is the ladder the nested spaces climb; and where exact realizability fails, the singular values measure the obstruction's magnitude. This is BT1a: the obstruction datum is recoverable from — and refined by — the qualitative Hankel structure of the bottleneck. It is a genuine conjecture, not a theorem: no result in the corpus proves the recovery. But it is well typed, it is grounded in a dictionary that holds row-by-row, and it is falsifiable — the quantum-interface papers supply the hard instances where a failure would show. The remaining links of the chain are theorems, and Chapter 5 assembles them."),
]},
{
"title": "The Corrected Bridge Theorems",
"blocks": [
("p", "Table 2 states the six theorems — DeepSeek's three, and the earlier triad they sharpened — in three columns: as stated, what the corpus actually proves, and the corrected statement. The pattern of the corrections is uniform, and it is the substantive contribution of this volume: DeepSeek repeatedly equated two objects in one step where the corpus supports a chain of typed maps with a single open link. That is not a defect of its programme; it is the programme, made precise. An equation demands everything at once; a factorized identification can be checked link by link, proved partially, and refuted locally."),
("table", "theorems"),
("p", "Three of the six deserve their corrections spelled out. Theorem B, as stated — Hankel singular values are exactly the dimensions of cohomology groups — is ill-typed outright: real numbers cannot equal integers. What is true, and what the corpus proves in fragments, is a two-shadow discipline: the integer shadow (rank counts interfaces; distinct rows count conflicts) and the real shadow (singular values price the failure). DeepSeek's Theorem A fails the same way at full generality — a real-valued function cannot equal a class-valued invariant — but its zero-distortion slice survives retyping as a floor: exact realizability at width k fails precisely when the rank ladder outruns k, and the log of that ladder level is a rate. Theorem C is the one statement DeepSeek got well-typed on the first pass, and the corrected view upgrades its status: if BT2's sandwich closes at the optimum, the determination index — the number of observations needed to determine the action — is fixed as the slope, which makes C a corollary-candidate rather than an independent conjecture."),
("p", "BT2's correction is the most instructive, because DeepSeek's statement quietly conflated two directions of bound that the corpus keeps scrupulously apart. The viability pair proves an achievability side: per-optic analytic Lipschitz bounds for the seven typed bridges, and a Banach contraction, with constant 0.697, of the Krasnoselskii–Mann-averaged update — constructive convergence, distortion accumulating controllably along the chain. The transduction corpus proves a converse side: AAK/Nehari floors that no k-state machine can beat. DeepSeek equated the rate–distortion function with the minimum Lipschitz constant — achievability masquerading as the frontier. The corrected statement is a sandwich: the floor from the operator side, the ceiling from the optic side, and the frontier squeezed between them. The equality of floor and ceiling at the optimum — the graded small-gain law — is the open core, and it is the same missing law that Volume I's compositional-home chapter already named for feedback. One open link, not a missing theory."),
]},
{
"title": "The Two-Step Chain",
"blocks": [
("p", "Figure 1 assembles the corrected BT1. The top band shows DeepSeek's bridge as stated: a single claimed arrow from the obstruction datum to the viability curvature, type defect marked. The chain below replaces it with three typed links. Link one, open: BT1a, the identification of the obstruction datum with the qualitative Hankel structure of the bottleneck — distinct rows as fibre conflicts, rank as interface size, the rank filtration as the nested-space ladder. Link two, proved: the refinement–resolution bridge of the metabolic manuscript (Theorem B<super>prime</super>) — discrete active-set jump measures converge weakly to continuous curvature densities under spatial averaging, in the Kantorovich–Rubinstein flat norm, inside the resolution window h ≪ σ ≪ L<sub>var</sub> and not outside it, with total-variation convergence failing by triangulation anisotropy. Link three, proved, with data: the small-loop viability–holonomy theorem of the companion — endpoint erosion of a viability margin is bounded, to leading order, by the viability-weighted curvature — and the empirical differential that makes it substantive: curvature predicts the transcription layer at r = +0.395 across 424 genes while the protein layer shows a −0.083 null."),
("figure", None),
("stats", [("3", "typed links in the corrected obstruction chain"), ("2", "of them theorems the corpus already proves"), ("1", "open link — BT1a, the bridge paper's target")]),
("p", "The chain is not a compromise between DeepSeek's demand and the corpus's reach; it is an upgrade of the demand's shape. An isomorphism is checkable only in the whole; a chain is checkable link by link, and two of these links are already theorems with the full certificate discipline behind them. There is also a recursion worth savouring, because it is the programme's own epistemology applied to its own unification: the proved bridge between spectrum and curvature is itself a resolution-limited statement — it holds inside a smoothing window and fails outside it, exactly as the corpus's charts and ladders hold and fail. The bridge between obstruction and curvature is itself a bounded observer. A referee who accepts the refinement–resolution bridge has already accepted the method by which the unification must proceed."),
("p", "What remains open is thereby isolated with unusual precision. BT1a is a dictionary-plus-recovery conjecture: it demands a theorem that recovers the five diagnostic outcomes and the nested-space filtration from the Hankel structure of the quotient — and nothing else. It is the natural first target of the bridge paper, the hardest of the open links, and the one whose proof would collapse the remaining distance between DeepSeek's programme and the corpus's own architecture, because the other two links are already in print."),
]},
{
"title": "The Chess Verdict, Corrected",
"blocks": [
("p", "DeepSeek's ruling on the chess paper was categorical: it is Cluster B, an outlier, operating at a different level of abstraction, sharing none of the categorical machinery, and it should remain a separate contribution — mentionable as an application domain, never a pillar. Volume I gave the paper its own chapter and a row in the docking grid, and neither acknowledged the dissent nor argued against it. That silence is what this chapter repairs, because the disagreement is real and the resolution is instructive: both sides were partly right, and the facts decide the split."),
("p", "First, the facts, because DeepSeek's assessment contains a demonstrable error: it describes “a Society of Specialised LLMs with five roles.” The paper has six — Generator, Aesthetic Critic, Analytic Critic, Deterministic Verifier, Adversarial Attacker, and Coordinator — with the neuro-symbolic Translator implemented as a recursive instantiation of the same six-role motif. The error is small but diagnostic: DeepSeek never read the paper in full; it worked from the title and search snippets, as its own transcript records. Its own method demands that a verdict on mathematical content be derived from the text, so the verdict must be re-derived — and the re-derivation, from the full twenty-seven pages, produces a finer result than either the original ruling or Volume I's silent inclusion."),
("p", "The re-derived verdict: DeepSeek's structural criterion — a pillar must share the mathematical machinery — is correct, and the chess paper fails it, exactly as DeepSeek said. The paper contributes no categorical or operator-theoretic machinery. What it contributes is two slot-instances of the programme's fixed theorem-types for language agents: the CSR state-sufficiency theorem — the register contains the information needed, the interface side — and Theorem 2*, the amplification bound with critic-guided retention — the frontier-and-wall side, showing that even modest beam widths and depths yield exponential success-probability amplification. Together with its empirical results against monolithic baselines, the paper is the programme's existence proof in silicon: bounded observers, composed under a graded interface, attaining a certified frontier no single bounded observer reaches. So the correction refines rather than reverses: pillar-status denied, agreeing with DeepSeek, on the machinery criterion; instance-status granted, correcting the “keep it separate” into “dock it as an instance” — which is, in the end, precisely the compromise DeepSeek itself allowed for (“you could mention it as an application domain”) and precisely what Volume I's grid row records. The difference is that it is now argued, cited, and reconciled with the dissent instead of asserted over it."),
]},
]
