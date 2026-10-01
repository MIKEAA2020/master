# Session Summary 0013 — Tasks 46/47

## The volume's text complete; the last named item decided

The user's order: *"the remaining Vol XIV chapters (1–3, 5–7) now
write themselves around the decided state — then commission the
dose-response pool so even the last named item becomes a decided
experiment."*  Both executed.

- **Date**: 2026-10-02
- **HEAD at end**: (this session's final commit — Task 47)
- **Last Task ID**: 47

## Task 46 — the six chapters (commit `00ff3c5`)

Chapters 1, 2, 3, 5, 6, 7 written as records around the DECIDED
state (6,359 words; with Ch.4's 3,812 the volume's text is
complete): Ch1 the ledger's new shape (the typed rows + the census
verdicts verbatim + the completion conditions); Ch2 the grind
formalized (the race/fuel/N* laws + the stopping rule — the
continuation protocol SUPERSEDED); Ch3 the certificates' coverage
(THE COMPLETION CERTIFICATE'S FORM stated in advance); Ch5 the
method itself measured (the reproduction-first catches incl. this
session's flint import catch; the typed tiers + PRE-REGISTERED);
Ch6 the synthesis statement (the theorem's final form + the map);
Ch7 the ledger forward (the standing orders amended; the closing
statement).

## Task 47 — the pool commissioned and decided

The protocol order held exactly: the pre-registration
(`download/seed_dose_preregistration.md`) committed at `cd42256`
BEFORE the data; the instrument IMPORTED from `seed_boundary.py`
(gate 12/12 bit-identical, worst |ΔE| = 0.0 — the import path
perturbs nothing); the pool 30 matched geometries (49-grid minus a
random partial matching, sizes 44–48 × gseeds {31,37,41,43,47,53},
every token 6–7 examples, no degenerate-E cells) × 24 seeds in two
blocks = 720 runs (402 s).

**THE VERDICT (pre-registered class): UNTESTED (saturation) — and
the finding is the cliff:**
- err ≡ 1.000 ± 0.000 at EVERY matched geometry, size 44–48:
  2160/2160 held-out predictions failed; train accuracy ≡ 1.0000 in
  all 720 runs; wrong-confidence 0.749 — perfect memorization,
  CONFIDENT total failure on the missing fact.  No interpolation
  regime exists at the matched edge; the hypothesized graded-failure
  band does not exist.
- E's coverage dose is REAL: E monotone 0.5699 → 0.5491 across
  44 → 48 (descriptive Spearman vs. the dose = 0.899) — the
  diagnostic measures the dose; the error axis it was to order is
  constant (H5-a ρ_S = 0.000 both blocks; the guard silent: 253
  matched pairs, max |Δerr| = 0.000).
- The error landscape across the record: 49/49 vacuous-perfect,
  44–48/49 total confident failure, 36/49 0.984, 16/49 0.934,
  scattered ≥ 0.99 — error NOT monotone in coverage; the coherence
  boundary is a cliff, not a slope.

**The last named item is DECIDED as a decisive negative**: the
within-family dose-response axis does not exist in this instrument's
regime; the coherence-tier law stands as the final form.  Chapter 4
carries the ADDENDUM (append-only).  The empirical face's ledger is
fully decided.

## Ledger (open)

- Vol XIV's remaining work: THE PRINTING (the unification figure,
  the PDF, the QA/VLM gates).
- The grind: rule-stopped (both arms) — re-commissioning is the
  user's call, not a standing order.
- No open empirical rows: every row closed by experiment or banked
  as measured (the hallucination zone: the narrowed CI).

## Recovery pointers

- worklog Tasks 46/47 (both copies); `scripts/seed_dose_results.json`
  + `seed_dose_runs.jsonl` + `download/seed_dose_preregistration.md`;
  `download/The_Resolution_Programme_XIV_Ch{1,2,3,4,5,6,7}_*.md` (Ch4
  with the addendum); the outline's three post-execution notes.

## Hygiene notes

- venv: `python-flint` must be present for the engines (the env
  restore drops it — `pip install python-flint`); the seed batteries
  need only numpy.
- Always push to the mirror after every commit (origin
  MIKEAA2020/master.git, branch `main`).
