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
| `download/` | The four volumes (PDF) + all scan figures + editable sources + reference papers. |
| `scripts/` | Every generation and computation script (LaTeX builders, scan engines, results JSON, logs). |
| `worklog.md` | The full session-by-session task log (Task IDs 0–8). |
| `PREFERENCES.md` | Standing user preferences (English-only protocol, credential storage, commit protocol). |

## The four volumes

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

## The computation record (exact scans, anchor-first discipline)

| Scan | Script | Result |
|---|---|---|
| Record-phase p-scan, n=2 (Ising exact) | `scripts/pscan_n2.py` | Kink at 0.23381 exact; Onsager fit R²=0.9902; anchors to 6–9 decimals. |
| Record-phase p-scan, n=3 (Weingarten) | `scripts/pscan_n3.py` | Crossing ladder 0.271→0.297 → 0.305(3); manuscript anchors to 6 decimals. |
| **Record-phase boundary, n=4** | `scripts/pscan_n4.py`, `repair_n4.py` | **CONFIRMED at the exact level**: crossings (4,6) 0.358313 [ms 0.35820, dev 1.1e-4], (6,8) 0.379079 [ms 0.37899, dev 9e-5], drift 0.0208 exact; R-ladder 0.1314/0.1827/0.2140 [ms 0.1315/0.1829/0.2142]; L·ln(λ1/λε) = 5.15 [5.2]; multiplet order exact (1+9+4+9+1, ε below all spin); endpoints exact: 24-fold at p=0, (4/35)^L rank-one at p=1. L=10 leg not run (resource limit, noted in JSON). Solver post-mortems (sector escape + v1-deflated matvec fix) in `scripts/repair_n4.log`. |
| E. coli cycle-size scan | `scripts/ecoli_cycles.py`, `ecoli_cycles2.py` | LP layer k-relaxation 0.249/cycle R²=1.000; one-pass saturation theorem; 0.361 = certified slowest cascade case; drift law slope 1.001. |
| Optic-Nehari attack | `scripts/optic_nehari.py` | Refutation of the naive composite (excess = δ², slope 1.991); dichotomy theorem + 2‖Δ‖ envelope; 12/12 small-gain accumulation. |

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
