# -*- coding: utf-8 -*-
"""vol8_content_b.py — The Abelianized Rung and the T_k Classification (Vol VIII):
chapters 7-12."""

CHAPTERS_B = [
    {"title": "The Isometric Rigidity: The Defect Law",
     "blocks": [
         ("p",
          "Impose the isometry — the Gram matrix equal to the identity — on the "
          "per-letter series family, and the rigidity the order anticipated arrives. "
          "The proof is a degree induction driven by an exact formula, the defect "
          "law. Step zero: the norm of w_0 is one, and w_0 is the multiplicative "
          "function built from the constant terms f_a(0); by the multinomial "
          "generating function its squared norm is 1 plus the geometric series of "
          "the total squared constant, which equals one only when every constant "
          "term vanishes. So f_a(0) = 0 for every letter: the columns are strictly "
          "positive-degree, and w_0 is exactly the delta at the empty word. Step "
          "one: w_1 is the vector of degree-one coefficients c_a on the single "
          "letters, and its unit norm fixes sum |c_a|^2 = 1 — the live letters "
          "already carry the whole weight budget."),
         ("p",
          "The induction step is where the higher coefficients die. Suppose all "
          "coefficients of every f_a vanish between degrees 2 and m. Then for k at "
          "most m the column w_k is exactly the multiplicative level vector — c to "
          "the Parikh exponent on the words of length k — and its norm is rho^k = 1 "
          "as it must be. At degree m + 1 the column acquires exactly two kinds of "
          "new contributions: the level-(m+1) main part, contributing rho^{m+1}, and "
          "the single-letter contributions, the coefficients of z^{m+1} in each "
          "f_a, contributing their squared magnitudes — and nothing else, because "
          "the mixed corrections are pushed beyond degree m+1 by the induction "
          "hypothesis. The defect law is the resulting identity: the squared norm of "
          "w_{m+1} equals rho^{m+1} plus the sum of the squared (m+1)-th "
          "coefficients. The isometry demands equality with rho^{m+1} = 1, so every "
          "(m+1)-th coefficient vanishes. Induction: f_a = c_a z, single term, "
          "degree one, and the weight budget is exactly spent."),
         ("p",
          "The battery verifies the defect law directly, and it is the tightest "
          "measurement of the volume: twelve random instances with injected "
          "degree-d perturbations, the law holding with worst deviation 2.8e-17. "
          "The single-letter contributions to w_d sit on level 1, where w_1 lives, "
          "so the Gram also acquires the exact cross-term w_1 dotted with w_d equal "
          "to the sum of c_a gamma_a — verified 6/6 — a second, independent "
          "violation of the identity. Non-monomial series with two higher terms "
          "break the Gram in twelve of twelve random instances, and the monomial "
          "family with rho not equal to 1 scales as rho^k exactly. The rigidity "
          "theorem follows: the Hankel-preserving isometries are exactly the "
          "multiplicative gradings, w_k(x) = 1[|x| = k] times the per-letter "
          "exponential of m(x), with sum of the squared per-letter weights equal "
          "to one."),
         ("p",
          "Two sharpenings complete the statement. First, the rigidity lands on the "
          "real sphere: complex unit lambda give isometries but not Hankel "
          "preservation, because the cut pair (a, eps) and (eps, a) demands "
          "lambda_a and its conjugate agree — the battery records the conflict at "
          "|2 Im lambda_a| = 0.8 for the tested instance. Second, the user's "
          "geometric-family guess is confirmed and refined: the isotropic point — "
          "all letters weighted equally, c_a = 1/sqrt(n) — is Volume VII's V, but "
          "the exact class is the whole per-letter sphere, and the anisotropy is "
          "genuine new freedom that T_k for k >= 1 is precisely what pins down. "
          "The rigidification is to the multiplicative gradings, the per-letter "
          "geometric family, of which the isotropic grading is one point and the "
          "vertices — single live letters — are the axis-supported extremes."),
     ]},
    {"title": "The Exact Class Assembled: Gradings, Vertices, and the Golden Witness",
     "blocks": [
         ("p",
          "The rigidity theorem assembles the exact class. By Volume VII's "
          "W-generic clause — the sandwich transports through any Hankel-preserving "
          "isometry — and by the classification, the multiletter AAK equality holds "
          "on the multiplicative gradings of the level-constant symbols: h(w) = "
          "psi(|w|) times the product of lambda_a^{m_a(w)}, with the per-letter "
          "weights on the real unit sphere. The transport is explicit: W_lambda H_psi "
          "W_lambda* has entries lambda^{m(x)} psi(|x| + |y|) lambda^{m(y)} = "
          "lambda^{m(xy)} psi(|xy|), a Hankel operator whose symbol is exactly the "
          "graded one; the isometry preserves singular values; and the classical "
          "one-letter AAK approximant transports along with everything else."),
         ("p",
          "The battery exercises the whole chain on five weight vectors — the "
          "anisotropic (0.8, 0.6), the isotropic pair, a lopsided (0.28, 0.96), a "
          "signed (-0.6, 0.8), and (0.6, 0.8) — and every link is machine-exact: "
          "the Gram at 8.9e-16 or better, every T_k Hankel, the transport identity "
          "at 0.0, singular values preserved to 4.4e-16. The golden-ratio witness "
          "runs on the anisotropic grading: the graded symbol built from the "
          "one-letter golden symbol (1, 1) has second singular value 0.6180339887 "
          "— the golden ratio conjugate, exact to the last digit — and the "
          "transported rank-one Prony approximant, optimized at window six in the "
          "operator norm, attains 0.6180339887498945 against the floor "
          "0.6180339887498949, a gap of 4e-16. The approximant is verified Hankel "
          "with defect 0.0, of rank one, and its distance equals the one-letter "
          "distance through the isometry to 5.6e-17."),
         ("p",
          "The vertex gradings deserve their own paragraph because they repair an "
          "incomplete statement from the axis analysis. A vertex lambda = e_a "
          "concentrates the entire budget on one letter: the columns pick out the "
          "single words a^k, the isometry is trivial, and the transported class is "
          "the single-axis family — symbols supported on the powers of one letter, "
          "with the per-letter symbol arbitrary, not merely geometric. The battery "
          "runs the vertex transport end to end: the Gram and the transport "
          "identity at 0.0, every T_k Hankel, and the golden witness on the "
          "single-axis symbol attaining 0.6180339887498943 against the golden floor, "
          "with the isometry distance identity exact to 3.3e-16. The single-axis "
          "class closes for arbitrary per-letter symbols because the vertex "
          "transport needs nothing geometric: the axis has one word per level, and "
          "the budget is spent on exactly that letter."),
         ("p",
          "The pooled identity is the last structural piece: for genuine direct "
          "sums of one-letter Hankels, the (M+1)-th pooled singular value equals "
          "the minimum over allocations of the maximum of the per-letter floors — "
          "the greedy allocation identity, verified exactly over M from 0 to 6 on "
          "a random pair of one-letter symbols. It is the mechanism behind any "
          "future multi-axis closure. But the two-axis symbols themselves are not "
          "direct sums: their Parikh-block matrices amalgamate over the origin — "
          "the shared empty-word row and column glue the per-letter blocks, and "
          "the amalgam of two rank-one per-letter blocks has rank three, not two. "
          "The battery records this corner tax explicitly. The corner is the "
          "first symptom of the budget obstruction, which the witness chapter "
          "turns into a measured strict failure."),
     ]},
    {"title": "The Atoms and the Budget",
     "blocks": [
         ("p",
          "The rank-one approximants on the rung have a complete classification, "
          "and it is the same classification again. A bounded weighted catalectic "
          "of rank one is an atom: psi'(gamma) = p times the product of "
          "lambda_a^{gamma_a}, with the total squared weight strictly below one. "
          "The proof is the two-by-two-minor argument on the rank-one catalectic: "
          "the entries u(beta) v(alpha) must depend on beta + alpha, which forces "
          "both factors to be exponential in the lattice and the symbol to be a "
          "per-letter power; the degenerate cases collapse to zero. The "
          "conjugated atom is the outer product of the weighted exponential vector "
          "v(beta) = sqrt(mu(beta)) lambda^beta with itself, and the battery "
          "verifies the identity to 2.8e-17 with rank exactly one on three "
          "instances."),
         ("p",
          "The norm of the atom is where the multinomial generating function "
          "returns for the last time. The squared norm of v is the sum over the "
          "lattice of mu(alpha) times the product of |lambda_a|^{2 alpha_a} — and "
          "the multinomial theorem collapses this to the geometric series of rho = "
          "sum |lambda_a|^2, so the sum is 1/(1 - rho) and the atom's norm is "
          "|p|/(1 - rho). The battery verifies the partial sums over the level-"
          "truncated lattice against the exact geometric partial sums to 1e-10 and "
          "beyond, and the tail identity — the mass beyond the box is exactly "
          "rho^{k+1}/(1 - rho) — makes the truncation rigorous for the witness "
          "optimizations. Boundedness is exactly the condition rho < 1: the atom "
          "domain is the open unit ball of the weight plane."),
         ("p",
          "The domain's boundary is the isometry sphere of the rigidity theorem. "
          "The classification (Chapter 7) puts the exact transport class on the "
          "sphere sum lambda_a^2 = 1; the atom classification puts every rank-one "
          "approximant strictly inside it. The two parts of the order meet on this "
          "sphere, and Figure 1(b) draws the meeting: the interior is the "
          "approximation-theoretic regime, the circle is the transport-theoretic "
          "regime, the isotropic point is Volume VII's V, and the vertices are the "
          "single-axis extremes. One number governs both regimes — the total "
          "squared weight, the multinomial budget — and the next chapter shows a "
          "witness that fails precisely because it tries to overdraft it."),
         ("stats", [
             ("2.8e-17", "worst deviation of the rigidity defect law, 12/12 instances"),
             ("0.61803399", "the golden witness on the anisotropic graded class, exact to 4e-16"),
             ("1.0369 > 1", "the two-golden amalgam: D(1) measured over the exhaustive rank-1 family"),
         ]),
     ]},
    {"title": "The Witnesses: The Sandwich's Fate on the Rung",
     "blocks": [
         ("p",
          "Two witnesses calibrate the sandwich on the rung, one open and one "
          "strictly failed, and both are measured against floors that are proved "
          "and families that are exhaustive or honestly bounded. The first is the "
          "(1,1) cell itself: h(ab) = h(ba) = 1 and zero elsewhere. Its spectrum is "
          "(sqrt 2, sqrt 2, 1, 1) — paired, as every cell's is — so at M = 1 the "
          "EYM floor equals the operator norm and the zero approximant closes the "
          "sandwich trivially; the battery records this closure explicitly rather "
          "than hiding it. The open slot is M = 2, where the floor is 1. The "
          "two-atom family — a provably valid family of rank-at-most-two "
          "approximants — measures 1.3188, beating the trivial bound of sqrt 2 but "
          "not the floor: the atoms' values on the cell's strip are tied to their "
          "geometric tails by the same multinomial weights, and no member of the "
          "family reaches down. The cell's D(2) lives in [1.000, 1.319], and the "
          "exact value over all rank-two weighted catalectics — the polynomial-atom "
          "variants included — is open."),
         ("p",
          "The second witness is the strict failure. Take the two-axis symbol with "
          "the golden one-letter symbol on each axis: h(eps) = h(a) = h(b) = 1 and "
          "zero elsewhere — the smallest symbol that is genuinely two-axis. Its "
          "transported matrix has spectrum (2, 1, 0), so the EYM floor at M = 1 is "
          "exactly 1. The rank-at-most-one approximant family is exhaustive by the "
          "atom classification plus the zero, so D(1) is a three-parameter "
          "optimization, and the battery's twenty-four-start optimization converges "
          "to 1.0369. The floor is missed by 0.0369, and the miss is structural: "
          "matching the amalgam's first row would force lambda_a = lambda_b = 1, a "
          "total weight of rho = 2, but the atom domain requires rho < 1 and the "
          "isometry sphere sits at rho = 1. The two-axis demand overdrafts the "
          "multinomial budget by the factor n = 2."),
         ("quote",
          "The sandwich fails on the rung for a reason that is now completely "
          "explicit: the multinomial budget. The admissible reweightings — the "
          "approximants inside, the transports on the sphere — all live under the "
          "budget sum lambda_a^2 <= 1, because the multinomial generating function "
          "sums their squared masses to the geometric series of the total weight. "
          "A symbol that wants n axes fully active asks for a total weight of n. "
          "For n = 2 the overdraft is witnessed: D(1) = 1.0369 against the floor 1, "
          "over the provably exhaustive rank-1 family."),
         ("p",
          "The status of the two statements matters and is recorded carefully. "
          "The exhaustiveness of the rank-one family is proved — the atoms plus "
          "zero are all of it. The optimization over that family is numerical, "
          "multi-start, converged, with a rigorous truncation tail from the exact "
          "tail identity; the closed-form proof that the minimum exceeds the floor "
          "is not written here, and the ledger says so. What is proved is the "
          "structure: the failure, where it occurs, occurs because of the budget, "
          "and the budget is the multinomial measure. Figure 1(c) draws the "
          "calibration: the closed golden point on the graded class, the cell's "
          "open interval, and the amalgam's strict-failure interval, each with its "
          "floor marked."),
     ]},
    {"title": "What This Changes: The Register, the Corpus, and the Boundary",
     "blocks": [
         ("p",
          "For the corpus, the volume adds three theorems that stand on their own "
          "and connect outward. The exact reduction identifies the abelianized "
          "Hankel with the weighted catalecticant — the classical object of "
          "commutative algebra and invariant theory, the matrix of apolarity — "
          "reweighted by the multinomial measure; the rank-inflation law is the "
          "box-determinant lemma, an elementary but apparently new identity whose "
          "content is that the reversal is the unique surviving permutation; and "
          "the spectral law identifies the cell spectra with the geometric means "
          "of complementary multinomials. The commutative connection is recorded "
          "as context, honestly: the catalecticant literature is cited as the "
          "natural home of these matrices, and none of the volume's proofs depend "
          "on it."),
         ("p",
          "For the framework's clauses, the volume sharpens two registers. The "
          "rank-register clause — resource equals rank — now carries the "
          "inflation law: the abelianized cell at multidegree gamma registers the "
          "box count, polynomial of degree n - 1 in the total degree at balanced "
          "cells, against the level register's linear count; abelianization "
          "inflates the machine, and the multinomial count is the cost. The "
          "magnitude clause — the singular tail — now has the rung's measured "
          "floor structure: paired spectra for the cells, the multinomial profile "
          "as the spectrum itself, and the budget as the reason the profile "
          "cannot be matched cheaply. Both sharpenings are machine-checked and "
          "both are stated exactly where the boundary begins."),
         ("p",
          "For the boundary itself, the volume replaces one large open problem "
          "with a smaller and sharper one. Volume VII's off-class boundary was the "
          "constructive nc-AAK problem in full generality. The rung analysis "
          "splits it: on the transportable families the equality is proved; on "
          "the off-axis rung the problem is now the multinomial-weighted "
          "catalectic AAK problem — approximate a weighted commutative Hankel by "
          "weighted commutative Hankels of bounded catalectic rank in the "
          "operator norm — with the EYM floor always available, the exhaustive "
          "rank-one family classified, and the first strict failure witnessed "
          "and attributed. The natural next links are named in the ledger: the "
          "closed-form minimum for the amalgam witness, the polynomial-atom "
          "families for the M >= 2 slots, and the characterization of exactly "
          "which abelianized phi have the sandwich — the rung's own version of "
          "Open 7.13."),
         ("table", "ledger"),
     ]},
    {"title": "The Honest Ledger",
     "blocks": [
         ("p",
          "Both items of the order are discharged, and the discharge is "
          "asymmetric in the way the mathematics itself is asymmetric. Item one "
          "— the abelianized rung — is closed as a structure theory: the exact "
          "reduction, the forced weights, the localization, the two laws, the "
          "atoms, and the budget, with the sandwich's fate measured rather than "
          "claimed. Item two — the T_k classification — is closed in both "
          "layers: formally the homomorphism classification, which is rich "
          "rather than rigid, and isometrically the rigidity to the "
          "multiplicative gradings, which is the rigidity the order anticipated, "
          "refined from the isotropic geometric family to the full per-letter "
          "sphere. The junction is the theorem's shape: the transport's exact "
          "class and the approximation's rank-one class are the two regimes of "
          "one budget, and the budget is the multinomial measure of the Parikh "
          "lattice."),
         ("p",
          "What remains is honest and bounded. On the rung: the weighted-"
          "catalectic AAK problem, with the cell's M = 2 slot open in "
          "[1.000, 1.319] and the amalgam's M = 1 slot measured at 1.0369 "
          "against the floor 1 over the exhaustive rank-one family — the "
          "closed-form minimum, the higher-rank families, and the sandwich "
          "locus characterization are the named next attacks. Beyond the rung: "
          "Volume VII's ledger is unchanged — the off-class equality of Open "
          "7.13, the uniqueness of the dictionary at infinite dimension, Risk 4 "
          "(the submission decision, which remains the author's alone), the "
          "bounded benchmark extensions, and the n = 4 L = 10 leg. The "
          "programme's architecture is now eight volumes deep, and every one of "
          "them ends the same way: with the proofs that exist, the measurements "
          "that bound what does not, and the names of the links that are next."),
     ]},
]
