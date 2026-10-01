# Session Summary 0012 — Task 45

## The HOLD watch resolved; Chapter 4 written around the decided experiment

The user's order: *"run 1–2 cover4d slices + census to resolve the HOLD
watch; then Vol XIV Chapter 4 writes itself around a decided experiment
rather than a design — with the token-coverage-matched dose-response
pool as the one remaining nameable upgrade."*

- **Date**: 2026-10-02
- **HEAD at end**: (this session's commit — Task 45, the census HOLD
  resolution + the Vol XIV Chapter 4 record)
- **Last Task ID**: 45

## What happened

1. **The census round 4** (one cover4d-only slice, per the amended
   protocol — the rule itself decided one slice was enough): 60.0M
   calls, 29,924,011 leaves certified (BDC 10,840,150 e0 + 8,324,792
   e4 + 10,759,069 e5), frontier 30.  The series 24→26→28→30→30 gives
   the THIRD consecutive below-floor window (closure −2.0 branches/M
   against the +0.05 floor; projection NO-CLOSURE, the trend opens).
   **THE RULE FIRES HOLD — both arms of the grind are now rule-stopped**
   (the wall arm stopped in Task 44).  No second slice spent (the rule
   says spend no more compute once HOLD fires).
2. **The arc's first stall leaves**, in the deciding round: 1246, with
   every measured center margin ≥ +11.25 above λ* (median +107,
   n=1099 with values) — interval-width effects at the frontier's
   depth (the wall's far-out pattern), not mathematical obstructions.
   Banked as residue with the margins.
3. **Vol XIV Chapter 4 WRITTEN** as a record:
   `download/The_Resolution_Programme_XIV_Ch4_The_Seed_Level_Boundary.md`
   — the decided experiment's full account (the pre-registration, the
   bit-identical gate, H1's law with all numbers, H2's honest
   correction and the coherence-tier law, H3's negative, H4's power
   diagnosis, the secondary endpoint, the boundary's scoped statement,
   the census resolution §4.9, and §4.10 the token-coverage-matched
   dose-response pool as the ONE remaining nameable upgrade — named,
   priced, uncommissioned).
4. Records: README (item 14 update + the grind_census row's
   resolution), the outline's second post-execution note, this
   summary, worklog Task 45 (both copies), commit + push.

## Ledger (open)

- The grind: DECIDED — HOLD by rule, both arms stopped; the completion
  face is Task 42's bookkeeping.  The continuation protocol is
  SUPERSEDED: no further drain rounds unless the user re-commissions.
- The seed-level boundary: DECIDED — the scope law (Task 44).
- The empirical face's one open item: the token-coverage-matched
  dose-response pool (sizes 44–48) — named and priced in Ch.4 §4.10,
  NOT commissioned.
- Vol XIV's remaining build: chapters 1–3, 5–7 + the printings (the
  chapter-4 record is the volume's first written chapter).

## Recovery pointers

- worklog Task 45 (both copies); `scripts/grind_census_results.json`
  (both copies) — the HOLD verdict + the stall margins;
  `download/The_Resolution_Programme_XIV_Ch4_The_Seed_Level_Boundary.md`
  (both copies); `scripts/seed_boundary_results.json` (Task 44's data).
- The venv lost `python-flint` in the environment restore — reinstalled
  (`pip install python-flint`); check it after any reset before running
  the engines.

## Hygiene notes

- PAT: the mirror remote carries the embedded token (push worked this
  session); `.secrets/` at the project root (gitignored) is the
  three-layer fallback if the remote URL ever breaks.
- Always push to the mirror (`github_repos/master`, origin
  MIKEAA2020/master.git) after every commit.
