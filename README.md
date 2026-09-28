# The Resolution Programme — Master Repository

**Author of the underlying corpus:** Amin Abaee (MIKEAA2020) · **Synthesis, scans and bridge work:** Super Z
**Latest update:** 2026-09-28 · This repository collects every creation from the assistant rounds,
committed and pushed after each session (standing protocol, see `PREFERENCES.md`).

## What is here

The repository is the delivery channel for the **Resolution Programme** synthesis of the whole
research corpus: a single line of mathematics — *constrained realizability* (behaviour factors
through what the agent can distinguish) — running from quantum circuits and combs, through
halting physics and automata, to metabolic curvature and sustainability governance.

| Path | Contents |
|---|---|
| `top-down of my work.txt` | The author's four-model external syntheses (astra / opus 5.5 / fable / opus 5) — the brief this programme answers. |
| `download/` | The eight volumes (PDF) + all scan figures + editable sources + reference papers. |
| `scripts/` | Every generation and computation script (LaTeX builders, scan engines, results JSON, logs). |
| `worklog.md` | The full session-by-session task log (Task IDs 0–12). |
| `PREFERENCES.md` | Standing user preferences (English-only protocol, credential storage, commit protocol). |

## The eight volumes

1. **The_Resolution_Programme_Grand_Unified_Picture.pdf** (Vol I, 18 pp) — the coherent,
   top-down, bird's-eye view: one primitive, two currencies, three faces, two walls, eight domains;
   the slot-grid for works (c)–(h) that the four external syntheses left open.
2. **The_Resolution_Programme_II_The_Bridge_Theorems.pdf** (Vol II, 16 pp) — every DeepSeek
   point adjudicated (as-is / corrected / open); the six bridge theorems restated with corrections
   and one isolated open link each; risk register; staged publication path.
3. **The_Resolution_Programme_III_New_Laws_New_Theorems_New_Physics.pdf** (Vol III, 21 pp) —
   the four laws of bounded observation, six new theorems (proved halves separated from open
   cores), nine falsifiable predictions, five capabilities, full provenance ledger.
4. **The_Resolution_Programme_IV_A_Theory_of_Bounded_Observation.pdf** (Vol IV, 20 pp) —
   the theory-level deliverable: record thermodynamics of bounded observers (postulates P1–P4,
   phase diagram, cascade dynamics) + the three ordered confrontations executed.
5. **The_Resolution_Programme_V_The_Remaining_Open_Links.pdf** (Vol V, 17 pp) —
   BT3's enrichment built (the cost-enriched graded category, the budget dichotomy, the guarded
   trace), BT2's equality closed to the corpus ceiling (exact quadratic gap form), Risk 3
   confronted on RockSample (the DI program vs POMCP: +45% at 10^4x less compute).
6. **The_Resolution_Programme_VI_The_Dictionary.pdf** (Vol VI, 15 pp) —
   BT1a attacked inside the enrichment: the dictionary as a morphism of sheaves on the budget
   lattice, six clauses proved, recovery audited 600/600, the quantum rank law recovered
   exactly, RockSample's compression break typed at correlation 0.97.
7. **The_Resolution_Programme_VII_The_Multiletter_Analytic_Theorem.pdf** (Vol VII, 18 pp) —
   the full analytic proof demanded of BT1a's remainder: the six demands discharged (the
   multiletter partial realization theorem with the closed-form commutativity obstruction, the
   uniform 2-eps law in every solid norm, the graded Fliess ladder, the norm-universal wall,
   the enriched naturality, the global sheaf morphism) and the multiletter AAK equality proved
   on the exact stated class of level-constant symbols — the transport sandwich, machine-exact
   (4.4e-16) with the golden-ratio witness (3.3e-16) — with the off-class boundary carried
   honestly as Open 7.13 / the constructive nc-AAK problem.
8. **The_Resolution_Programme_VIII_The_Abelianized_Rung.pdf** (Vol VIII, 15 pp) —
   the two remaining links of Vol VII discharged: (1) the abelianized class as the
   intermediate rung — the exact Parikh reduction (abelianized Hankel = commutative
   Hankel conjugated by the square-rooted multinomial coefficients, machine-exact
   2.2e-16), the forced-weight lemma, the localization theorem (transport survives
   iff the support is axis-supported; the defect ratio rho(gamma) = sqrt(mu(gamma))
   in closed form via the multivariate Vandermonde), the spectral law (cell spectra
   = the multinomial profile, paired), the rank-inflation law (box determinant,
   register = prod(gamma_i+1)), the atom classification and the budget obstruction;
   (2) the T_k classification beyond k=0 — the homomorphism classification (all T_k
   collapse into one monoid condition: F = prod f_a^{m_a}, rich and unrigid) plus
   the isometric rigidity: the degree induction with the exact defect law
   (||w_d||^2 = rho^d + sum |[z^d]f_a|^2, verified to 2.8e-17) forces the
   multiplicative gradings — the per-letter geometric sphere, confirmed and refined
   from the geometric-family guess. The sandwich measured honestly: golden on the
   graded class (0.6180339887, 4e-16), the cell open at M=2 in [1, 1.319], and
   the two-axis amalgam strictly failed: D(1) = 1.0369 > sigma_2 = 1 over the
   provably exhaustive rank-1 family — the multinomial budget overdrafted by n.

## The computation record (exact scans, anchor-first discipline)

| Scan | Script | Result |
|---|---|---|
| Record-phase p-scan, n=2 (Ising exact) | `scripts/pscan_n2.py` | Kink at 0.23381 exact; Onsager fit R²=0.9902; anchors to 6–9 decimals. |
| Record-phase p-scan, n=3 (Weingarten) | `scripts/pscan_n3.py` | Crossing ladder 0.271→0.297 → 0.305(3); manuscript anchors to 6 decimals. |
| **Record-phase boundary, n=4** | `scripts/pscan_n4.py`, `repair_n4.py` | **CONFIRMED at the exact level**: crossings (4,6) 0.358313 [ms 0.35820, dev 1.1e-4], (6,8) 0.379079 [ms 0.37899, dev 9e-5], drift 0.0208 exact; R-ladder 0.1314/0.1827/0.2140 [ms 0.1315/0.1829/0.2142]; L·ln(λ1/λε) = 5.15 [5.2]; multiplet order exact (1+9+4+9+1, ε below all spin); endpoints exact: 24-fold at p=0, (4/35)^L rank-one at p=1. L=10 leg not run (resource limit, noted in JSON). Solver post-mortems (sector escape + v1-deflated matvec fix) in `scripts/repair_n4.log`. |
| E. coli cycle-size scan | `scripts/ecoli_cycles.py`, `ecoli_cycles2.py` | LP layer k-relaxation 0.249/cycle R²=1.000; one-pass saturation theorem; 0.361 = certified slowest cascade case; drift law slope 1.001. |
| Optic-Nehari attack | `scripts/optic_nehari.py` | Refutation of the naive composite (excess = δ², slope 1.991); dichotomy theorem + 2‖Δ‖ envelope; 12/12 small-gain accumulation. |
| **The multiletter analytic theorem battery** | `scripts/bt1a_analytic.py` | Transport identity machine-exact (0.0–5.6e-17); singular values preserved (4.4e-16); the golden-ratio AAK witness exact to 3.3e-16; PR witness m*=2 with verified construction; 609/609 two-eps law in 5 norms; 10/10 graded-Fliess ladders; the wall norm-universal (pole slope −1.000); off-class gaps measured and reported open. |
| **The abelianized rung + T_k battery** | `scripts/abelian_rung.py` | Parikh reduction machine-exact (2.2e-16, 6 symbol families); weights forced (10/10 vs 0/10); defect ratios exact on 9 cells (rho = sqrt(mu)); spectral law error 0.0; box determinants +-c^R exact; golden on the anisotropic graded class (0.61803399, 4e-16); defect law 12/12 at 2.8e-17; complex-lambda negative check; amalgam strict failure D(1) = 1.0369 > 1 over the exhaustive rank-1 family. |

All scans run **anchor-reproduction-first**: the manuscript's own certified numbers are
reproduced to machine precision before any new claim is read off.

## Provenance discipline

Every statement in the volumes is labelled as one of: (i) already in the manuscripts
(file + version cited), (ii) derived in-session (computation or proof given), (iii) conjecture
(labelled open). See Vol III Table 4 for the full provenance ledger.

## Reproducing the scans

```bash
python3 scripts/pscan_n2.py      # n=2 exact Ising scan + validations
python3 scripts/pscan_n3.py      # n=3 Weingarten scan + validations
python3 scripts/pscan_n4.py      # n=4 scan (stages: V validation, S scan, M L=10 leg, F figure)
python3 scripts/ecoli_cycles.py  # needs iJO1366 model JSON + scipy/HiGHS
python3 scripts/optic_nehari.py  # defect-dichotomy computations
```

Dependencies: numpy, scipy, matplotlib (all scans); Playwright for the diagram HTML→PNG steps.
