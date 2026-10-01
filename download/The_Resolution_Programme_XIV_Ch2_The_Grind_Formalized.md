# The Resolution Programme, Volume XIV
# Chapter 2 — The Grind, Formalized: the Termination Structure

**Status**: record (the continuation protocol stated as mathematics —
and, as of this session, as a MEASURED STOPPING RULE that has fired).
**Date**: 2026-10-02 (session 0012).  **The batteries**:
`tail_law.py` + `gradient_split_ab.py` (existing, consolidated — Task
38 / Task 39) + the projection instrument, which is the census
(`grind_census.py`, Task 44, round 4 this session).  **The chapter's
claim, updated by the census**: the grind is not open mathematics; it
is scheduled computation with a measured cost law — and, as of round
4, a measured stopping rule, which the frontier's own dynamics have
now exercised.

---

## 2.1  The race law (the termination guarantee)

Every far-out conversion is a RADIUS race: the box must shrink (by
bisection) until its interval certificate closes.  The law (Task 38,
n = 35 conversions measured): the depth d* = ceil(log2(eps0)/rate),
where eps0 = rad/value at the tag (median 5.41) and rate is the
per-level relative-radius decay — median 0.135 bits per level.
Predicted vs. actual median error: 1.0 level.  The swamp is a radius
problem, not a value problem: the VALUES are certifiable from the
first probe (the fuel law below); the width of the interval at the
census boxes is what the levels buy off, one bisection at a time.

The law is the termination guarantee it was banked as: no conversion
is stuck, every one finishes at its predicted depth, and the depth is
computable in advance from the tag's own numbers.  What the census
added this volume: the frontier's DEPTH STRUCTURE is also why the
branch count does not close — the LIFO stack replenishes exactly
because the deep conversions split new entries faster than the
shallow ones close (the oscillation band 24–32 over 4.5M calls, the
net trend OPENING at −2 branches/M over the deciding window).

## 2.2  The fuel law (the divergence never binds)

The far-out population is 81.3% of the ROOT; the centers' margins are
100% positive, with m ~ ρ^{31.46} (R² 0.974): the divergence is the
certificate's FUEL, and it never binds — the values run 1e9 to 1e33
over λ* across the whole far-out census.  The fuel law is why the
completion face can be bookkeeping (Chapter 3): the far field's
mathematical content is carried by the growth laws (Task 41's
s^4 window quartic, the ρ^{3.666} excited growth) and the sound
shells (FF-4: 6/6 one-shot strict-sound), not by the grind's
leaf-count.

## 2.3  The N* law and the censored 21

Every measured conversion wins at N* = 2 — the degree-8 form of the
divergence certificates carries the whole far-out tail; the high-N
rungs of the ladder never bind.  The censored 21 (the honest census's
remainder beyond the 26-level probe cap) are predicted slow, not
stuck: d* ∈ [28, 54].  The census's round 4 adds the cover-side
mirror: the 1246 first stall leaves of the cover4d arc, whose measured
center margins (min +11.25, median +107 above λ*) are the same
reading on the other engine — the values are in, the intervals at
depth are the width artifact, and the residue is priced as refinement,
not as mathematics.

## 2.4  The width-first optimality, and the A/B that guarded it

The gradient-prioritized split corollary (Task 38's banked
"actionable" 2x drain) was REFUTED by controlled A/B BEFORE any engine
edit (Task 39): the stock width-first split12 converts 0.4998 e45/call
with zero stalls; the gradient arm 0.4185 with 324 cap-hit stalls —
0.84x, the static prior over-splitting the stale carriers (the TL-3b
profile was a TRANSIENT of the then-current stack; the live profile is
flat, and at the flat profile the measured 0.135 bits/level is already
at the informed-split optimum: halving the top-18% term gives
log2(100/91) ≈ 0.137 bits).  The width-first rule stays, validated
near-optimal on the live frontier — the A/B-before-edit rule paying
for itself exactly as designed.

## 2.5  The stopping rule (stated first, measured after)

The census's commissioning line was the user's: the grind "needs a
stopping rule and an expected endpoint."  The rule was stated FIRST
(Chapter 1 quotes it verbatim) and then evaluated from the parsed
round series — the discipline the whole corpus practices, applied to
the corpus's own continuation protocol:

- **COVER4D**: CONTINUE while frontier > 0 AND the trailing-3 net
  closure ≥ 1 branch per 20M calls (the diminishing-return floor).
  COMPLETE at frontier = 0 — the completion certificate.  HOLD (report
  the structure, spend no more compute) when the trailing rate sits
  below the floor for 3 consecutive rounds.
- **WALL**: CONTINUE while the trailing-3 net stack reduction > 0.
  STOP when the stack trend is non-descending — the far-out refinement
  REPLENISHES the stack; exhaustion is not this arm's endpoint, and
  the completion face is Task 42's bookkeeping.

**The measured verdicts**: the wall arm STOPPED (the oscillation 39–45,
net +4/window).  The cover4d arm caught its own projection error —
the census's first reading ("near exhaustion, 3M calls to zero" from
the trailing window 32→30→24) was a windowing artifact, reversed by
the next three census-driven slices (24→26→28→30, the LIFO
replenishment), and the fourth round completed the third consecutive
below-floor window — **HOLD fired**.  One slice decided it; the rule's
own text ("spend no more compute") made the second slice
unnecessary.  The grind is now fully rule-stopped.

## 2.6  What the grind's mathematics is

The chapter's closing statement, in the corpus's own terms: the grind
contributed three things to the ledger, and none of them is a leaf
count.  First, the LAWS (the race, the fuel, N*, the width-first
optimality) — measured, replicated across two engines, portable to any
interval-certification programme.  Second, the CERTIFICATED REGION
(29.92M leaves on the cover side, 346,400 on the wall side, zero
stalls across the whole arc until the rule-stopping round, whose
stalls are margin-positive residue) — the ground truth the theorem's
statement stands on.  Third, the STOPPING RULE itself — the
instrument that converts an open-ended compute order into a decided,
priced, bounded commitment.  The continuation protocol of the first
thirteen volumes ("re-run the driver") is hereby SUPERSEDED by its own
measurement: the certificates stand, the completion is bookkeeping,
and the compute stops.
