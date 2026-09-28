# -*- coding: utf-8 -*-
"""vol5_content_b.py — The Remaining Open Links (Vol V): chapters 8-12 + tables."""

TABLES_B = {
    "bridges": {
        "caption": "Table 3 — The bridge ledger after this session: DeepSeek's six theorems, "
                   "the corpus corrections of Volume II, and the status now",
        "header": ["Bridge", "As DeepSeek stated it", "As corrected (Vol II)", "Status now"],
        "ratios": [0.13, 0.27, 0.32, 0.28],
        "font": 7.4,
        "rows": [
            ["A", "R(D) equals the minimum over sheaf-theoretic refinements of the "
             "obstruction datum",
             "ill-typed at full generality (a real-valued function cannot equal a "
             "class-valued invariant); the zero-distortion slice survives as a floor",
             "UNCHANGED: the zero-slice floor stands; the general statement remains "
             "ill-typed"],
            ["B", "Hankel singular values are exactly the dimensions of sheaf "
             "cohomology groups",
             "two-shadow discipline: rank as the integer shadow, singular values as "
             "the real shadow, one ladder relating them",
             "UNCHANGED, and now load-bearing: the floor-equality locus of the "
             "small-gain law is measured thin (0/200 random targets)"],
            ["C", "the determination index equals the slope of R(D) at the optimal "
             "point",
             "well-typed; corollary-candidate of BT2: the slope interpretation is "
             "what the sandwich would fix at the optimum",
             "STRENGTHENED: the sandwich's ceiling is now the trace identity, so C "
             "awaits only the floor side; and the index itself is now a measured "
             "object on RockSample (E3)"],
            ["BT1", "the obstruction datum is isomorphic to the viability curvature",
             "two-step chain: obstruction to Hankel structure [BT1a, open] to "
             "curvature [proved] to regulation [proved, with data]",
             "UNCHANGED at the full-statement level: BT1a is the programme's sole "
             "remaining deep open link"],
            ["BT2", "R(D) is the minimum per-optic Lipschitz constant of an optic "
             "implementing the transducer",
             "the sandwich: the AAK floor below, the optic-chain ceiling above; "
             "equality at the optimum is the graded small-gain law, the open core",
             "CLOSED AS FAR AS THE CORPUS ALLOWS: the ceiling is the guarded-trace "
             "identity; the gap law is exact (quadratic closed form); the equality "
             "locus is characterized; the floor inherits Open 7.13"],
            ["BT3", "the intercept principle is equivalent to non-existence of a fixed "
             "point of the homotopy fixed-point extension",
             "enrichment first: once the cost-enriched graded category is built, the "
             "intercept becomes fixed-point non-existence of the currying "
             "endomorphism",
             "DONE: the enrichment is built, the budget endomorphism is defined, and "
             "the intercept is PROVED as fixed-point non-existence (integer "
             "arithmetic), fused with the contraction side into the dichotomy law"],
        ],
    },
    "rocksample": {
        "caption": "Table 4 — The RockSample confrontation: the three experiments, their "
                   "predictions, and their verdicts",
        "header": ["Experiment", "Design", "Result", "Verdict"],
        "ratios": [0.15, 0.30, 0.30, 0.25],
        "font": 7.4,
        "rows": [
            ["E1: matched compute",
             "vanilla POMCP (random rollouts) at 100/300/800 simulations per decision "
             "vs the DI program (a closed-form policy from the determination-index "
             "calculus, no search) on a fixed 20-map RockSample[4,4] suite, "
             "eps = 0.9, gamma = 0.95",
             "vanilla POMCP 9.91 / 9.51 / 8.92; the DI program 13.78 +/- 1.05 at "
             "0.004 ms per decision (roughly 10,000x cheaper than the 300-sim "
             "baseline); POMCP with DI rollouts 5.30 (negative datapoint); "
             "clairvoyant bound 24.18",
             "the theory-derived policy beats the named baseline by ~45% at four "
             "orders of magnitude less decision compute; search-refinement "
             "underperforms and is reported as a negative result"],
            ["E2: compression",
             "the DI program on log-odds-quantized beliefs at widths q = 2..16 vs the "
             "exact posterior; the small-gain certificate with measured components "
             "(L_V = 91.8, Lambda = 0.95)",
             "q >= 5 recovers the exact value (14.0-15.9 vs 14.21); q = 4 partial "
             "(10.50); q = 3 breaks (3.40: the belief RESETS to the prior each read); "
             "q = 2 commits blind and survives (14.94); the certificate holds at "
             "every width",
             "the compression boundary sits at the band-resolution scale, as the "
             "determination-index calculus predicts; the q = 3 break is structural, "
             "not a distortion — a phase boundary, safe but not informative for "
             "the local bound"],
            ["E3: the sensor wall",
             "the DI program's checks-per-episode and reward against sensor "
             "efficiency eps from 0.55 to 1.0; the theory's near-wall form: the "
             "determination index ~ 2b/mu with mu = ln((1+theta)/(1-theta))",
             "checks saturate at the horizon cap (60/episode) below eps ~ 0.7 and "
             "plunge above it (59.96 to 4.00); reward collapses from 13.38 to 0.03 "
             "between eps = 0.9 and 0.55; the measured log-log slope -1.13 (flattened "
             "by the cap) against the near-wall theory's -1",
             "the wall is real and the reward collapses across it: the same "
             "first-order-pole family as the budget wall at L = 1 — the AI "
             "benchmark's own instance of the one-wall law"],
        ],
    },
}

CHAPTERS_B = [
    {"title": "The RockSample Confrontation",
     "blocks": [
        ("p", "DeepSeek's Risk 3 was a demand with a named test attached: the "
              "framework's empirical validation was biological — metabolic networks, "
              "the Keio collection, autopoiesis closure — and for an AI-facing "
              "contribution, in DeepSeek's words, you would need to show that the "
              "framework yields better policies or more efficient learning on "
              "standard benchmarks, against POMCP, DESPOT, and point-based value "
              "iteration, on RockSample, Tiger, and Hallway. This session implements "
              "the demand's first instance: RockSample[n, k] in the original "
              "Smith-Simmons formulation, on a fixed twenty-map suite at n = 4, k = "
              "4, sensor efficiency 0.9, discount 0.95; a faithful POMCP with exact "
              "posterior tracking — a strictly stronger variant than the particle "
              "version, since the belief is a product of per-rock Bernoullis and the "
              "observation-conditioned tree can carry exact posteriors — as the "
              "named baseline; and the theory's instruments as the contender."),
        ("p", "The unified pipeline, instantiated, has three moving parts, each of "
              "which is a corpus instrument rather than an ad hoc heuristic. The "
              "belief compression is the interface-width budget of the transduction "
              "corpus: the per-rock posterior quantized to a log-odds grid, the "
              "width q the analogue of the memory budget M. The determination index "
              "is the corpus's own object — the number of observations needed to "
              "determine the action — instantiated by the sensor's information rate: "
              "the log-odds random walk of repeated checks has drift mu equal to "
              "twice the log-likelihood ratio at the current distance, and the "
              "expected number of checks to exit the action band is the band width "
              "over the drift, exactly the Wald quantity. The DI program is the "
              "closed-form policy this calculus dictates: check the rock with the "
              "best information rate per approach step, commit when the belief exits "
              "the band, walk to determined-good rocks and sample them, exit when "
              "nothing remains determined-good, and never check a rock already "
              "outside the band — a dominated action in the calculus's own terms, "
              "whose admission turns out to matter enormously."),
        ("p", "The headline comparison is honest about what matched means. Vanilla "
              "POMCP with random rollouts scores 9.91, 9.51, and 8.92 mean "
              "discounted reward at 100, 300, and 800 simulations per decision; the "
              "DI program scores 13.78 with a 95% confidence interval of plus or "
              "minus 1.05 — a 45% margin over the baseline at its best budget — "
              "while spending 0.004 milliseconds per decision against the "
              "baseline's tens of milliseconds: roughly four orders of magnitude "
              "less decision compute. The clairvoyant bound, the same program "
              "reading the true rock states instead of the belief, sits at 24.18: "
              "the DI program realizes about 57% of the perfect-information value, "
              "the baseline about 37%. And the one negative result is reported with "
              "the same care: POMCP with the DI program as its rollout policy "
              "scores 5.30, worse than random rollouts — at these small budgets "
              "the tree's exploration re-introduces exactly the commitment "
              "pathology the program's band discipline exists to solve, a known "
              "small-budget effect of strong default policies, and a genuine "
              "warning against reading the 45% margin as a search-level claim. It "
              "is a policy-level result, and it is stated as one."),
        ("p", "One methodological confession belongs in the record, because the "
              "anchor discipline caught it and because it became a measurement. "
              "The session's first headline number was 23.4, not 13.8, and the "
              "number was a bug: an argument-order swap in the policy wrapper "
              "passed the true rock states where the belief belonged, silently "
              "converting the DI program into an oracle that sampled exactly the "
              "good rocks and never needed to check. The tell was E3's check "
              "counter reading zero — a policy that scores 23 without a single "
              "sensor reading is not a policy — and the discrepancy between the "
              "E1 and E2 baselines, which ran the same code through different "
              "call paths, is what forced the audit. The oracle is kept, "
              "relabeled as the clairvoyant bound, because a perfect-information "
              "reference is genuinely useful; but the honest headline is the "
              "corrected one, and the episode is the anchor-first rule earning "
              "its keep for the fourth time in the programme's history."),
        ("figure", "rock"),
     ]},

    {"title": "The Compression Kink and the Sensor Wall",
     "blocks": [
        ("p", "The compression scan answers the question the certificate exists "
              "for: how much belief resolution does the program actually need? "
              "The exact-posterior program scores 14.21; the compressed program "
              "recovers that value at every width from five levels upward "
              "(13.98 to 15.93 across q = 5, 6, 8, 10, 16, all within the "
              "confidence band), is partially degraded at four levels (10.50), "
              "and breaks catastrophically at three (3.40). The break is "
              "structural, not gradual: with three levels spanning the log-odds "
              "range, the middle level sits exactly at the prior, and every "
              "sensor reading rounds a moderately confident belief back to "
              "uninformed — the belief resets on every observation, the program "
              "never commits, and the episode is consumed by checking. Two "
              "levels survive for the opposite reason: the grid is so coarse "
              "that one reading throws every belief to a band edge, and the "
              "program becomes a one-reading commitment heuristic that happens "
              "to be viable at this sensor efficiency. The boundary the theory "
              "predicts — the cell size must resolve the action band, roughly "
              "2.2 log-odds — falls between the four-level cell (4.7) and the "
              "six-level cell (2.8), and the measured recovery tracks it."),
        ("p", "The certificate check is reported with its components measured and "
              "its slack admitted. The bound has the small-gain form — the "
              "deficit at most the measured value Lipschitz constant times the "
              "measured quantization distortion over one minus the sensor's "
              "loop gain — and with the worst-case measured components (L_V = "
              "91.8 from belief-perturbation experiments, Lambda capped at "
              "0.95) it holds at every width, including the structural break: "
              "the q = 3 deficit of 10.81 sits an order of magnitude below its "
              "bound of 544. The honest reading is that the certificate is safe "
              "everywhere and informative in the continuous regime: for q at or "
              "above five, the deficits (at most 0.23) sit inside bounds that "
              "are themselves within a factor of a few of the deficits' scale, "
              "while at the break the bound certifies nothing that the phase "
              "diagram does not already say. A local bound crossing a phase "
              "boundary is exactly the situation the p-scan taught the "
              "programme to expect: the Onsager law holds inside its window "
              "and the kink lives outside it."),
        ("p", "The sensor wall is the third experiment and the one that closes "
              "the loop with the enrichment's mathematics. As the sensor "
              "efficiency falls toward uninformative at one half, the "
              "information rate mu falls to zero and the determination index "
              "diverges as its reciprocal — a first-order pole at the wall, "
              "the same functional family as the budget wall at L = 1. The "
              "measurement shows both faces of the divergence: below efficiency "
              "0.7 the program's checks saturate at the episode horizon (60 "
              "checks per episode, the belief walk too slow to exit the band in "
              "any episode, the reward collapsing from 13.38 at 0.9 to 0.03 at "
              "0.55 — the determination index has exceeded the horizon, and "
              "the observer is on the wrong side of the wall), and above 0.8 "
              "the check count plunges as the theory's reciprocal (59.96 down "
              "to 4.00, measured log-log slope -1.13, flattened toward the "
              "near-wall theory's -1 by the horizon cap). The reward boundary "
              "between collapse and competence is the AI benchmark's own "
              "instance of the one-wall law, and it is measured, not "
              "asserted."),
        ("stats", [("13.78 vs 9.51", "the DI program vs the best POMCP baseline "
                                     "(45% margin, ~10^4x less decision compute)"),
                   ("q >= 5", "the compression width where the program recovers its "
                              "exact-posterior value: the band-resolution scale"),
                   ("0.03 vs 13.38", "reward below vs above the sensor wall "
                                     "(eps = 0.55 vs 0.9): the determination index "
                                     "exceeds the horizon")]),
     ]},

    {"title": "The Verdict on Risk 3",
     "blocks": [
        ("p", "The adjudication proceeds clause by clause, because DeepSeek's "
              "criterion had two clauses and the benchmark meets them unevenly. "
              "The first clause — show that the framework yields better policies "
              "on standard benchmarks — is met in its policy-performance sense: "
              "the determination-index program, a closed-form policy derived "
              "from the corpus's own calculus with no search, no learning, and "
              "no tuning beyond the band constant the theory fixes, beats a "
              "faithful POMCP implementation by 45% at matched simulation "
              "budgets and by four orders of magnitude in decision compute, on "
              "the exact benchmark DeepSeek named, in the standard formulation, "
              "with the reference points (clairvoyant bound, negative search "
              "datapoint) that make the margin interpretable rather than "
              "promotional."),
        ("p", "The second clause — or more efficient learning — is not met, and "
              "the volume says so plainly. Nothing here learns: the DI program "
              "is computed, not trained, and the search-refinement variant that "
              "would carry a learning-efficiency claim underperformed at the "
              "budgets the sandbox could afford. Three further limits are "
              "recorded with the same plainness: the comparison is against this "
              "session's own POMCP implementation, not production C++ solvers, "
              "so no wall-clock fairness claim is made — the compute claim is "
              "per-decision simulation count, which is implementation-"
              "independent; the instance is RockSample[4,4] alone, with Tiger "
              "and Hallway named by DeepSeek but not run; and the episode "
              "population is 60-160 episodes per configuration, adequate for "
              "the margins reported but not for a benchmark paper's error "
              "discipline. Each limit is a bounded extension, none is a "
              "conceptual obstacle, and the negative search result is the one "
              "that would most change the picture if reversed at production "
              "budgets."),
        ("p", "Against the risk as written, the verdict is partial retirement, "
              "achieved and honestly bounded. The biological-only validation "
              "objection is answered: the framework's instruments — the "
              "determination index as a policy, the compression width as a "
              "resource dial, the small-gain certificate as a guarantee shape, "
              "and the wall as a phase prediction — now have measured lives "
              "on a standard AI benchmark, and the theory's predictions were "
              "run before they were read. What remains open under Risk 3 is "
              "the learning-efficiency clause and the production-solver "
              "comparison; what is closed is the claim that the framework has "
              "nothing to say to the AI side. DeepSeek's staged path placed "
              "the algorithmic paper third, after the bridge paper and the "
              "monograph, benchmarked for ICML, NeurIPS, or CAV; this "
              "confrontation is that stage's first data point, and it is on "
              "the board."),
        ("quote", "The theory-derived program beat the named baseline by 45% "
                  "at four orders of magnitude less compute — a policy-level "
                  "result, reported with its negative datapoint attached and "
                  "its learning-efficiency clause left open."),
     ]},

    {"title": "The Bridge Ledgers, Updated",
     "blocks": [
        ("p", "The programme's bookkeeping is part of its honesty, and the "
              "ledgers change materially this session. The bridge ledger "
              "first: of DeepSeek's six theorems, Theorem A remains ill-typed "
              "at full generality with its zero-distortion floor intact; "
              "Theorem B's two-shadow discipline is unchanged and newly "
              "load-bearing, because the floor-equality locus it governs is "
              "now a measured thin set; Theorem C is strengthened, since the "
              "sandwich's ceiling side is now an identity and the "
              "determination index itself has been measured on an AI "
              "benchmark. BT1 stands where Volume II left it: the two proved "
              "links of the chain are proved, BT1a is open, and it is now the "
              "programme's only deep open link. BT2 is closed as far as the "
              "corpus's own conditional floor allows — the ceiling is the "
              "trace identity, the gap law is exact, the equality locus is "
              "characterized, and the floor side inherits Open 7.13's status "
              "honestly. BT3 is done: built, retyped, and proved."),
        ("p", "The risk ledger changes more. Risk 1 — the curvature may be "
              "formal rather than substantive — is untouched by this session: "
              "the refinement-resolution and small-loop holonomy links stand "
              "on their own evidence. Risk 2 — the quantitative gap, the "
              "enrichment that DeepSeek said might require new mathematics — "
              "is retired by construction: the cost-enriched graded category "
              "exists, its algebra's failures are exhibited and turned into "
              "design decisions, and the guarded trace carries the distortion "
              "accounting Volume II demanded. Risk 3 is partially retired, on "
              "the RockSample numbers of the previous two chapters. Risk 4 — "
              "community reception — remains unmet by construction, because "
              "reception is not something the programme can compute; what it "
              "can compute is readiness, and the readiness changed: the "
              "fifteen-to-twenty-page bridge paper that DeepSeek's first "
              "stage specified — the definitions, the two-step chain, the "
              "sandwich, the retyped transfer theorem, the continuations as "
              "applications — now has its definitions and its law written, "
              "in the form of this volume's mathematical core."),
        ("p", "The staged path, read against the corpus as Volume II read it, "
              "now has a different shape of urgency. The individual lines are "
              "public; the identification that binds them is not; and the "
              "sharper risk Volume II named — that the juxtaposition is done "
              "for the author, wrongly, by the first reader who notices the "
              "pattern — stands closer now, because the pattern is more "
              "complete: a cost algebra, a budget dichotomy with a wall, an "
              "exact gap law, and a benchmark confrontation are a "
              "recognizable programme to anyone who has seen one. The bridge "
              "paper's skeleton is this volume's chapters two through five "
              "plus Volume II's adjudication tables; the monograph's "
              "compositional-home chapter has its category; and the "
              "algorithmic paper has its first table. What none of them have "
              "yet is a reader, and that is the one thing the programme "
              "cannot manufacture for itself."),
        ("table", "bridges"),
     ]},

    {"title": "What Remains",
     "blocks": [
        ("p", "The record should close the way the audits have closed "
              "throughout: with the open items named, sized, and sequenced. "
              "The deep one is BT1a — the dictionary-plus-recovery theorem "
              "between the extensional diagnostics of causal descent and the "
              "operator structure of the Hankel theory: distinct rows as "
              "fibre conflicts, rank as interface size, the rank filtration "
              "as the nested-space ladder. Volume II called it the deep one "
              "because no existing template proves it, and nothing this "
              "session changes that; what this session changes is its "
              "isolation. With BT3 built and BT2 closed to the corpus's own "
              "conditional ceiling, BT1a is no longer one of three open "
              "links but the one, and the enrichment now exists to state it "
              "in: the obstruction datum is a section of the budget lattice's "
              "failure sheaf, and its identification with Hankel structure "
              "is a morphism problem in a category that finally has both "
              "sides."),
        ("p", "The bounded ones are the floor and the benchmark's extensions. "
              "Open 7.13 — the intrinsic multiletter characterization of when "
              "the AAK floor is attainable — is now measured from the "
              "equality-locus side: the scan says the locus is thin, which "
              "is evidence about the characterization's shape but not the "
              "characterization. The unconditional small-gain law therefore "
              "still runs on the corpus's conditional floor, and says so "
              "wherever it is stated. On the benchmark side, the three "
              "bounded extensions carry their own sizes: Tiger and Hallway "
              "are small instances a single session can add; the "
              "production-solver comparison needs a machine with more than "
              "two cores and a C++ baseline; and the learning-efficiency "
              "clause needs the search-refinement result reversed at "
              "budgets two orders of magnitude up, which is where the "
              "literature says POMCP's tree stops depending on its default "
              "policy. The n = 4 scan's L = 10 leg, left to the manuscript's "
              "own computation in Volume IV's honest gaps, also still "
              "belongs on this list."),
        ("p", "And the one that is not a theorem at all: the programme's "
              "unsubmitted state. Risk 4 was never a mathematical risk, and "
              "the session's work does not touch it; what it does is remove "
              "the last internal excuse on the two stages that precede it. "
              "The bridge paper's mathematics is written; the definitions "
              "exist; the law has its closed form and its measured walls; "
              "the benchmark has its first table and its honest negative "
              "datapoint. The order the user fixed for this session is "
              "executed in full — the enrichment built, the equality closed "
              "to its corpus-bounded ceiling, the benchmark confronted — "
              "and what the programme owes next is either BT1a's proof or "
              "the submission decision, whichever the author calls first. "
              "The mathematics will wait; the priority clock will not."),
        ("stats", [("1", "deep open link remaining: BT1a, the obstruction-to-Hankel "
                        "dictionary-plus-recovery theorem"),
                   ("3", "bounded extensions: Tiger and Hallway; the "
                         "production-solver comparison; the learning-efficiency clause"),
                   ("0", "internal excuses left on the bridge paper's mathematical "
                         "readiness")]),
     ]},
]

# merge into the content namespace used by the engine (content_a's TABLES is
# the shared dict; updating it here makes 'bridges' and 'rocksample' resolvable)
from vol5_content_a import TABLES as _SHARED_TABLES
_SHARED_TABLES.update(TABLES_B)
