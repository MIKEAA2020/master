# -*- coding: utf-8 -*-
"""vol8_content_a.py — The Abelianized Rung and the T_k Classification (Vol VIII):
chapters 1-6 + tables + figures. All statements anchored to the corpus files and
the session's verification battery (abelian_rung.py, abelian_rung_results.json)."""

FIGURES = {
    "main": ("/home/z/my-project/download/figures/abelian_rung.png",
             "Figure 1 — The abelianized rung, measured on three fronts. "
             "(a) The multinomial mountain: the transport-obstruction profile "
             "sqrt(mu(beta) mu(gamma-beta)) over the decompositions of "
             "gamma = (6,6), on a log colour scale — the profile runs from 1 "
             "at the axis corners (no defect) to sqrt(C(12,6)) = 30.4 at the "
             "centre, and the defect ratio rho(gamma) = sqrt(mu(gamma)) is "
             "exactly this spread, growing like 2^k (pi k)^(-1/4) on balanced "
             "cells. (b) The multinomial budget: the lambda-plane in which "
             "every admissible reweighting lives — the atom interior "
             "sum lambda_a^2 < 1, the isometry sphere sum lambda_a^2 = 1 (the "
             "multiplicative gradings, the exact AAK class, with Vol VII's "
             "isotropic V and the single-axis vertices marked), and the "
             "two-axis demand lambda = (1,1) sitting outside at total weight "
             "rho = 2 — the budget overdraft by the factor n = 2 that breaks "
             "the transport. (c) The sandwich on the rung: EYM floors against "
             "the certified exhaustive families, witness by witness — the "
             "golden case closed on the graded class at 0.6180, the "
             "gamma = (1,1) cell closed at M = 1 by the paired spectrum and "
             "open at M = 2 in [1.000, 1.319], and the two-golden amalgam "
             "where the exhaustive rank-1 family measures D(1) = 1.0369 > "
             "sigma_2 = 1 — the first witnessed strict failure."),
}

TABLES = {
    "mandate": {
        "caption": "Table 1 — The order, itemized and answered: the two "
                   "remaining links named at the close of Volume VII, the "
                   "theorem package that discharges each, its proof status, "
                   "and its verification in this session's battery",
        "header": ["The ordered link", "The theorem delivered",
                   "Proof status", "Verification"],
        "ratios": [0.24, 0.34, 0.21, 0.21],
        "font": 7.3,
        "rows": [
            ["(1) The abelianized class as the intermediate rung — the "
             "transport fails there by exactly the multinomial weights",
             "Theorem A3: the exact Parikh reduction H = V_alpha D_mu^0.5 "
             "Cat_phi D_mu^0.5 V_alpha*; the Parikh-block lemma (the weights "
             "are forced on the approximant side); the localization theorem "
             "(K commutative-Hankel iff the support is axis-supported); the "
             "defect ratio rho(gamma) = sqrt(mu(gamma)) in closed form via "
             "the multivariate Vandermonde; the spectral law (sigma = the "
             "multinomial geometric-mean profile); the rank-inflation law "
             "(the box determinant); the atom classification and the budget "
             "obstruction",
             "PROVED (the reduction, the lemma, the localization, the two "
             "laws, the atom classification); the budget witness measured "
             "over the provably exhaustive rank-1 family",
             "Reduction machine-exact (2.2e-16) on six symbol families; "
             "10/10 weighted transports Hankel, 0/10 unweighted or random; "
             "the defect-ratio table exact on nine cells; the spectral law "
             "exact (0.0 error); box determinants +-c^R exact"],
            ["(2) The T_k classification beyond k = 0, which may rigidify "
             "the class to the geometric family",
             "Theorem S2: the collapse of all the T_k conditions into the "
             "single monoid homomorphism F(x,z) = prod_a f_a(z)^{m_a(x)} "
             "(the complete FORMAL classification — rich, not rigid); the "
             "isometric rigidity theorem: with the Gram = I constraint, the "
             "degree induction (the exact defect law) forces f_a = c_a z "
             "with sum c_a^2 = 1 — the multiplicative gradings, the "
             "per-letter anisotropic geometric family",
             "PROVED (both layers; the rigidity hypothesis confirmed and "
             "refined: the class rigidifies to the full per-letter sphere, "
             "of which the isotropic geometric family is the equal-weight "
             "slice)",
             "Homomorphism identity 12/12 with all T_k Hankel for random "
             "per-letter series; random columns fail 12/12; the defect law "
             "12/12 with worst deviation 2.8e-17; the cross-term law 6/6; "
             "non-monomial breakage 12/12; five gradings machine-exact"],
        ],
    },
    "localization": {
        "caption": "Table 2 — The transport-defect ratio, cell by cell: the "
                   "measured strip spread against the closed form "
                   "rho(gamma) = sqrt(mu(gamma)), and the balanced-cell "
                   "asymptotic (exact to the shown digits; the ratio column "
                   "converges to 1)",
        "header": ["Cell gamma", "mu(gamma)", "rho(gamma) = sqrt(mu) exact",
                   "2^k (pi k)^(-1/4) asymptotic", "ratio"],
        "ratios": [0.22, 0.20, 0.24, 0.20, 0.14],
        "font": 7.6,
        "rows": [
            ["(1,1)", "2", "1.41421", "1.50225", "0.94140"],
            ["(2,1)", "3", "1.73205", "-", "-"],
            ["(2,2)", "6", "2.44949", "2.52648", "0.96953"],
            ["(3,1)", "4", "2.00000", "-", "-"],
            ["(3,3)", "20", "4.47214", "4.56586", "0.97947"],
            ["(4,4)", "70", "8.36660", "8.49802", "0.98454"],
            ["(5,5)", "252", "15.87451", "16.07385", "0.98760"],
        ],
    },
    "rigidity": {
        "caption": "Table 3 — The T_k classification, layer by layer: what "
                   "each constraint adds, and what the battery measured",
        "header": ["Layer (constraints imposed)", "The resulting family",
                   "Rigid?", "Battery"],
        "ratios": [0.30, 0.34, 0.12, 0.24],
        "font": 7.3,
        "rows": [
            ["T_k Hankel for every k (the formal condition; Vol VII's S "
             "criterion, all k at once)",
             "The per-letter series family F(x,z) = prod_a f_a(z)^{m_a(x)} "
             "with f_a ARBITRARY formal series (constants allowed; "
             "multi-term allowed; zero series allowed)",
             "NO — rich",
             "12/12 random f_a pass every T_k; the homomorphism identity "
             "12/12; random columns fail 12/12"],
            ["+ l2 columns (boundedness of each w_k)",
             "The same family, with the constant-term condition sum_a "
             "|f_a(0)|^2 < 1 for w_0 (the T_0 shadow: Vol VII's "
             "multiplicative classification recovered)",
             "no",
             "The w_0 norm identity 1/(1 - sum f_a(0)^2) via the "
             "multinomial generating function, partial sums exact"],
            ["+ Gram = I (the isometry)",
             "f_a = c_a z EXACTLY (single term, degree 1) with "
             "sum_a c_a^2 = 1: the multiplicative gradings — the per-letter "
             "anisotropic geometric family; complex unit lambda are "
             "isometries but NOT Hankel-preserving (the (a,eps)/(eps,a) cut "
             "pair sees lambda_a vs its conjugate)",
             "YES",
             "The defect law 12/12 exact to 2.8e-17: "
             "||w_d||^2 = rho^d + sum_a |[z^d] f_a|^2; the cross-term law "
             "6/6; non-monomial breakage 12/12; five real gradings "
             "machine-exact (Gram, every T_k, transport, sigma)"],
        ],
    },
    "ledger": {
        "caption": "Table 4 — The honest ledger: what this session closed, "
                   "what it sharpened, and what it leaves open — the "
                   "boundary carried explicitly",
        "header": ["Item", "Status after this session", "Where"],
        "ratios": [0.34, 0.42, 0.24],
        "font": 7.6,
        "rows": [
            ["The abelianized reduction and the forced weights",
             "CLOSED — the rung is exactly the multinomial-weighted "
             "catalectic problem; machine-exact",
             "A3a, A3b"],
            ["The transport failure, in closed form",
             "CLOSED — rho(gamma) = sqrt(mu(gamma)) via the multivariate "
             "Vandermonde; exponential on balanced cells",
             "A3c"],
            ["The spectrum and the register of abelianized cells",
             "CLOSED — sigma = the multinomial profile (paired); register = "
             "prod(gamma_i + 1) (the box determinant)",
             "A3e, A3f"],
            ["The T_k classification beyond k = 0",
             "CLOSED — the homomorphism classification (formal) + the "
             "isometric rigidity to the multiplicative gradings (the "
             "per-letter sphere)",
             "S2a, S2b"],
            ["The exact AAK class on the rung",
             "CLOSED — the multiplicative gradings of the level-constant "
             "symbols; the golden witness machine-exact on the anisotropic "
             "family",
             "A3d, S2c"],
            ["The off-axis sandwich (the rung's own AAK problem)",
             "OPEN — the multinomial-weighted catalectic AAK problem; the "
             "gamma = (1,1) cell: D(2) in [1, 1.319]; the two-golden "
             "amalgam: D(1) = 1.0369 > 1 measured over the exhaustive rank-1 "
             "family (the budget overdraft); no closed-form minimum",
             "A3h"],
            ["The full classification of the rung's sandwich locus "
             "(which phi close exactly)",
             "OPEN — the closed families found (the gradings, the vertices) "
             "and the witnessed failures bracket it; the characterization "
             "is the natural next link",
             "outlook"],
            ["The off-class equality of Vol VII (Open 7.13 / constructive "
             "nc-AAK), Phi's uniqueness, Risk 4, the bounded benchmarks, "
             "the n = 4 L = 10 leg",
             "UNCHANGED — carried forward",
             "Vol VII ledger"],
        ],
    },
}

CHAPTERS_A = [
    {"title": "The Mandate: Two Links, One Ladder",
     "blocks": [
         ("p",
          "Volume VII closed with a ledger and a boundary. The seven demands of the "
          "full-proof order were discharged, the multiletter AAK equality was proved "
          "on the exact class of level-constant symbols, and the remaining links were "
          "named. Two of them were named as the next natural attacks: the abelianized "
          "class as the intermediate rung, where the transport was expected to fail by "
          "exactly the multinomial weights; and the classification of the Hankel-"
          "preserving isometries beyond the T_0 layer, which might rigidify the exact "
          "class to the geometric family. This volume is the execution of that order. "
          "Both links are now theorems with batteries, and the two answers turn out to "
          "be two views of one object: the multinomial measure of the Parikh lattice."),
         ("p",
          "The shape of the answer is worth stating before the machinery. The "
          "abelianized symbols — those that see a word only through the counts of its "
          "letters — form a genuine intermediate rung between the level-constant class "
          "where Volume VII's transport succeeds and the full multiletter class where "
          "the problem is open. On this rung the transport fails for a reason that is "
          "now completely explicit: the Hankel operator of an abelianized symbol is an "
          "isometric copy of a commutative Hankel matrix conjugated by the diagonal of "
          "square-rooted multinomial coefficients, and that diagonal is precisely what "
          "the classical theory cannot absorb. Where the weights collapse — the level "
          "rung, where the fibre counts sum to n^k — the transport succeeds; where "
          "they are trivial — the coordinate axes, where every fibre is a single word "
          "— it succeeds again; and everywhere else it fails by the exact ratio "
          "rho(gamma) = sqrt(mu(gamma)), the square root of the multinomial "
          "coefficient of the cell."),
         ("quote",
          "The order's two items are one theorem seen from two sides: the transport "
          "fails by exactly the multinomial weights (item 1), and the admissible "
          "reweightings that survive every T_k are exactly the per-letter geometric "
          "family whose total squared weight is one — the multinomial budget (item 2). "
          "The isometry sphere of the classification is the boundary of the atom "
          "domain of the approximation problem."),
         ("p",
          "The verification battery for this volume is abelian_rung.py, eight parts, "
          "with results in abelian_rung_results.json. Every identity claimed in the "
          "text is machine-checked: the Parikh reduction to 2.2e-16 across six symbol "
          "families, the forced-weight lemma in both directions, the defect-ratio law "
          "on nine cells to 1e-12, the spectral law with error exactly 0.0, the box "
          "determinants to machine precision, the golden-ratio witness on the "
          "anisotropic graded class to 5e-16, the defect law of the rigidity induction "
          "to 2.8e-17 over twelve random instances, and the strict-failure witness "
          "measured over a rank-1 family that is provably exhaustive. As in every "
          "volume of this programme, the honest boundary is drawn where the proofs "
          "stop, not where the optimism would like it."),
     ]},
    {"title": "The Intermediate Rung: Parikh, Multinomials, and the Exact Reduction",
     "blocks": [
         ("p",
          "Fix the alphabet S with n letters and let m: S* to N^n be the Parikh map, "
          "sending a word to the vector of its per-letter counts. A symbol h is "
          "abelianized when h(w) = phi(m(w)) for some function phi on the lattice: "
          "the symbol sees the multiset of letters and nothing else. The level-"
          "constant class of Volume VII is the special case where phi depends only on "
          "the total degree, and the one-letter case is the degenerate case n = 1 "
          "where the Parikh map is the length. The fibre over a lattice point alpha — "
          "the set of words with those letter counts — contains mu(alpha) = "
          "|alpha|!/(alpha_1! ... alpha_n!) words, the multinomial coefficient, and "
          "these counts are the measure of the rung."),
         ("p",
          "The fibre structure gives a canonical isometry V_alpha from l2(N^n) into "
          "l2(S*), mapping the basis vector at alpha to the unit-normalized indicator "
          "of its fibre. The first theorem of the volume is the exact reduction: for "
          "every abelianized symbol, the multiletter Hankel operator H_h factors as "
          "V_alpha K V_alpha* with K(beta, alpha) = sqrt(mu(beta) mu(alpha)) "
          "phi(beta + alpha). The matrix K is the commutative Hankel — the "
          "catalecticant of the form with coefficients phi — conjugated on both sides "
          "by the diagonal of square-rooted multinomials. The identity is proved by "
          "entrywise computation, and the battery verifies it to 2.2e-16 on six symbol "
          "families: level-constant, the (1,1) and (2,1) cells, an axis-supported "
          "symbol, a multiplicative grading, and a random abelianized symbol. Singular "
          "values and rank are preserved exactly, as any isometric conjugation "
          "preserves them."),
         ("p",
          "Two anchors make the reduction honest rather than merely true. First, the "
          "level rung of Volume VII is recovered inside it: lumping the lattice by "
          "total degree gives an isometry L with V = V_alpha L, and for level-constant "
          "phi the transported matrix collapses to L H_psi L* with psi(k) = phi(k) "
          "n^{k/2} — the exact formula of Volume VII, reproduced by the battery to "
          "2.2e-16. The collapse happens because the fibre counts sum by level: "
          "sum over |alpha| = k of mu(alpha) equals n^k, depending only on k. Second, "
          "the one-letter sanity: for n = 1 the multinomial weights are identically 1, "
          "the Parikh lattice is the degree axis, and the reduction says the "
          "multiletter Hankel is the classical one-letter Hankel — verified exactly, "
          "as it must be. The rung is genuinely intermediate: it contains the level "
          "class strictly, and is contained in the full class strictly, for every "
          "n >= 2."),
     ]},
    {"title": "The Weights Are Forced: The Parikh-Block Lemma",
     "blocks": [
         ("p",
          "An approximation theory on the rung needs to know which operators on the "
          "Parikh side are themselves Hankel after transport. The answer is the "
          "second theorem, the Parikh-block lemma: an operator of the form "
          "V_alpha K' V_alpha* is a multiletter Hankel operator if and only if K' "
          "carries the same multinomial weights — that is, K'(beta, alpha) = "
          "sqrt(mu(beta) mu(alpha)) psi(beta + alpha) for some psi — in which case "
          "the transported operator is precisely the Hankel of the abelianized symbol "
          "psi composed with m. The approximants on the rung are forced to live in "
          "the same weighted family as the target."),
         ("p",
          "The proof of the forced direction is a cut argument. If the transported "
          "matrix is Hankel with symbol g, then for every word x the value g(x) must "
          "agree across all cuts of x, and the entries across a cut depend only on "
          "the Parikh pair (m(u), m(v)) of the cut pieces. Every decomposition beta "
          "<= gamma is realized by a cut of some word — take any word of Parikh beta "
          "and concatenate any word of Parikh gamma - beta — so the value must in "
          "fact depend only on the sum beta + alpha. Unwinding the fibre "
          "normalization gives exactly the weighted catalectic form. The battery "
          "checks both directions: ten random weighted catalectics transport to "
          "Hankel operators (10/10), ten random block matrices fail (0/10), and the "
          "unweighted transport fails with a recorded conflict of exactly the "
          "multinomial ratio."),
         ("p",
          "That recorded conflict is worth seeing in digits because it is the whole "
          "story in one entry pair. Transport the commutative Hankel without the "
          "weights and look at the word ab. The cut (eps, ab) produces the entry "
          "psi(1,1) divided by sqrt(mu(0,0) mu(1,1)) = 1.414, while the cut (a, b) "
          "produces psi(1,1) divided by sqrt(mu(1,0) mu(0,1)) = 2.0 — the same word, "
          "the same symbol value, two different transported entries, their ratio "
          "exactly 1/sqrt(2), the reciprocal of the square root of the (1,1) "
          "multinomial. The battery measures this pair at 1.4142 and 2.0 against the "
          "predicted 1.4142. The weights are not a technical inconvenience; they are "
          "the difference between a well-defined symbol and a contradiction, and any "
          "approximant that wants to compete on the rung must pay them in full."),
         ("p",
          "The lemma has an immediate structural consequence: the structured "
          "approximation problem on the rung is exactly the problem of minimizing "
          "the operator norm of D_mu^0.5 (Cat_phi - Cat_psi) D_mu^0.5 over symbols "
          "psi whose catalectic has rank at most M. The rung inherits the "
          "commutative-multivariable Hankel approximation problem — with the "
          "multinomial diagonal attached. This is the precise sense in which the rung "
          "is intermediate: it is the commutative problem, reweighted by the measure "
          "of the lattice. Every closed and open question that follows in this volume "
          "is a statement about that diagonal."),
     ]},
    {"title": "The Localization Theorem: Where the Transport Survives",
     "blocks": [
         ("p",
          "The transport of the one-letter theory through V_alpha would need the "
          "transported matrix K to be a commutative Hankel itself — entries depending "
          "on beta + alpha alone. The localization theorem says exactly when this "
          "happens: K is a commutative Hankel if and only if the multinomial weights "
          "are decomposition-constant on the support of phi, which happens if and "
          "only if the support is contained in the union of coordinate axes (with the "
          "origin). On the axes every fibre is a single word, mu = 1, and the weights "
          "are trivial; off the axes they vary, and the variation is the failure."),
         ("p",
          "The failure is measured by a closed form, and the closed form is the "
          "heart of the order's first item. For a cell gamma, consider the profile "
          "of weights sqrt(mu(beta) mu(gamma - beta)) as beta ranges over the "
          "decompositions. The multivariate Vandermonde identity gives "
          "mu(beta) mu(gamma - beta) / mu(gamma) = the product of binomials "
          "C(gamma_i, beta_i) divided by C(|gamma|, |beta|), which is at most 1 — "
          "the denominator is the sum of the numerator over the whole degree slice — "
          "with equality exactly at the axis extremes. So the profile runs from 1 "
          "(at beta = the axis projection, where both fibres are single words) to "
          "sqrt(mu(gamma)) (at beta = 0 or beta = gamma), and the transport defect "
          "ratio is rho(gamma) = sqrt(mu(gamma)), exactly, for every off-axis cell. "
          "The battery confirms this on nine cells to 1e-12, including the "
          "near-axis cells like (4,1) where the ratio is a modest 2.24 and the "
          "balanced cells where it grows without bound."),
         ("table", "localization"),
         ("p",
          "The growth law deserves its own sentence because it is the quantitative "
          "face of the obstruction. On balanced cells gamma = (k, k) the defect "
          "ratio is sqrt(C(2k, k)), which behaves like 2^k divided by the fourth "
          "root of pi k: exponential in the degree, tempered only by a polynomial "
          "prefactor. The battery's growth table shows the measured ratios against "
          "this asymptotic converging from 0.94 at k = 1 to 0.99 at k = 5. The "
          "transport does not merely fail off the axes; it fails worse and worse as "
          "the letters of a cell balance out, which is exactly the regime where the "
          "abelianized rung is most distinct from both the level rung and the axes. "
          "The multinomial mountain of Figure 1(a) is this profile for gamma = (6,6), "
          "running from 1 at the corners to 30.4 at the centre."),
         ("p",
          "Between the two extremes the localization theorem leaves no gap. Where "
          "the support is axis-supported, K is a commutative Hankel — the battery "
          "measures the entry consistency defect at exactly 0.0 — and the rung's "
          "problem embeds in the commutative theory with trivial weights. Where any "
          "mass sits off-axis, the entry conflict on the gamma-strip is phi(gamma) "
          "times (rho(gamma) - 1), measured at 0.621 for the (1,1) cell loaded with "
          "1.5, exactly as predicted. The transport survives precisely on the set "
          "where the multinomial measure is degenerate, and nowhere else on the rung. "
          "This is item one of the order, discharged in closed form."),
     ]},
    {"title": "The Spectrum Is the Multinomial Profile",
     "blocks": [
         ("p",
          "The single-cell abelianized symbols — h(w) = c on the fibre of gamma and "
          "zero elsewhere — have a completely explicit spectral theory, and it is the "
          "cleanest demonstration that the multinomial weights are not an artifact of "
          "the transport but the intrinsic geometry of the rung. For such a symbol "
          "the transported matrix K is a monomial matrix: one nonzero entry per row "
          "and per column, sitting at (beta, gamma - beta) with value c times "
          "sqrt(mu(beta) mu(gamma - beta)). The singular values of a monomial matrix "
          "are the absolute values of its entries, so the spectrum of the cell is "
          "exactly the list of geometric means of complementary multinomial "
          "coefficients, scaled by c, and the rank is the number of decompositions, "
          "the product of the (gamma_i + 1)."),
         ("p",
          "The battery verifies the spectral law with error exactly 0.0 on four "
          "cells: the (1,1) cell has sigma = (sqrt 2, sqrt 2, 1, 1) and rank 4; the "
          "(2,1) cell has sigma = (2.2517, 2.2517, 1.8385, 1.8385, 1.3, 1.3) and rank "
          "6; the (2,2) cell has nine singular values up to 1.7146 and rank 9; the "
          "(3,1) cell has eight and rank 8. A structural feature visible in every "
          "one of these lists is the pairing: the strip matrix is symmetric with "
          "zero diagonal blocks, so its eigenvalues come in plus-minus pairs and the "
          "spectrum is doubly occupied. The pairing has a sandwich consequence "
          "recorded in the witness chapter — at M = 1 the EYM floor equals the norm "
          "and the trivial approximant closes the gap — so the honest failure slots "
          "of a cell begin at M = 2."),
         ("p",
          "The rank statement generalizes from cells to boxes, and the "
          "generalization is the register-inflation law. For a symbol supported in "
          "the downset box [0, gamma] with corner coefficient c nonzero, the box "
          "section of the catalectic has determinant plus-or-minus c raised to the "
          "box dimension — the reversal is the unique permutation of the box with "
          "beta + pi(beta) <= gamma for every beta, forced layer by layer from the "
          "corner inward, so every other permutation of the determinant expansion "
          "hits a zero entry — and hence the catalectic rank is exactly the number "
          "of lattice points of the box, the product of the (gamma_i + 1). The "
          "battery computes these determinants on random box-supported symbols and "
          "recovers c^R to machine precision, with rank R in every instance."),
         ("p",
          "At the same total degree k, the level rung registers k + 1 and the "
          "abelianized rung registers the product of the (gamma_i + 1), which on "
          "balanced cells is quadratic in k: the (k, k) cell registers (k+1)^2 "
          "against the level's 2k + 1, an inflation factor that grows linearly in k. "
          "The register — the minimal machine, the resource of the framework's "
          "rank-register clause — is inflated by the multinomial geometry itself. "
          "The abelianized ab/ba cell, with h(ab) = h(ba) = 1, registers 4; Volume "
          "VII's non-abelianized partial-realization witness, with h(ab) = 1 and "
          "h(ba) = 0, extends at register 2. Abelianizing the symbol is not the cheap "
          "direction: the symmetry constraint on the symbol side costs machine "
          "states, and the cost is again the multinomial count."),
     ]},
    {"title": "The T_k Collapse: The Homomorphism Classification",
     "blocks": [
         ("p",
          "The second ordered item concerns the structure theory of Volume VII: W, "
          "with columns w_k, is Hankel-preserving when T_k = the sum of w_i w_j* over "
          "i + j = k is a Hankel operator for every k, and Volume VII classified "
          "only the T_0 layer — w_0 multiplicative, the per-letter products with "
          "squared sum below one, plus the delta at the empty word. The question "
          "left open was what the conditions for k >= 1 add. The answer begins with "
          "an observation that collapses the entire tower into a single algebraic "
          "condition: forming the column-series F(x, z) = the sum of w_k(x) z^k, all "
          "the T_k conditions hold at once exactly when F(x, z) F(y, z) depends on "
          "the pair (x, y) only through the concatenation xy — that is, exactly when "
          "x maps to F(x, dot) as a monoid homomorphism from the free monoid into "
          "the formal power series under the Cauchy product."),
         ("p",
          "Because the Cauchy product is commutative, any such homomorphism factors "
          "through the abelianization, and the homomorphisms of the lattice N^n are "
          "the per-letter powers: F(x, z) is the product over letters of "
          "f_a(z)^{m_a(x)}, with f_a arbitrary per-letter formal series. This is the "
          "complete formal classification, and it is emphatically not rigid. The "
          "family is vast: the per-letter series may have constant terms, several "
          "terms, zero terms; the battery draws random multi-term series for both "
          "letters, builds the columns by polynomial arithmetic, and verifies the "
          "homomorphism identity on random word pairs (12/12) and the Hankel "
          "property of every T_k up to degree twelve (12/12). Random columns fail "
          "the same tests 12/12. T_0's multiplicative classification is recovered as "
          "the k = 0 shadow — the constant term of the series — and nothing in the "
          "formal layer rigidifies anything."),
         ("p",
          "The geometric family of Volume VII and the multiplicative gradings of "
          "this volume are the monomial sub-family: f_a = c_a z, a single term of "
          "degree one per letter. Within the monomial family the Gram matrix is "
          "diagonal with entries (sum |c_a|^2)^k, so the family is a family of "
          "weighted gradings whose total weight rho = sum c_a^2 controls everything: "
          "rho < 1 gives bounded contractions, rho = 1 gives isometries, rho > 1 "
          "gives unbounded operators. The reweightings of Volume VII are the "
          "isotropic points of this family. The rigidity question — whether the "
          "conditions beyond T_0 force the class into something small — is therefore "
          "a question about what the isometry constraint does to the per-letter "
          "series, and that is the next chapter's theorem."),
         ("table", "rigidity"),
     ]},
]

CHAPTERS_A_EXTRA = []
