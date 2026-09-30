# session_summaries/ — the persistent home for session-reset summaries

## Purpose

Every time the conversation context is exhausted or the environment resets,
a compact summary of the session's state is written here BEFORE the reset
(or immediately after recovery).  This directory is the durable,
version-controlled answer to the recurring question "where do the reset
summaries live?" — so that a fresh session can bootstrap from the REPO
instead of re-deriving state from chat history (the token-saving protocol).

## The protocol

1. **At the end of every session** (or at the start of the next one, if the
   reset hit first), append a file `NNNN_<short-slug>.md` where `NNNN` is
   the zero-padded sequence number and the slug identifies the session's
   dominant task(s).
2. Each file follows the house template (below): the state of the ledger,
   the last task ID, the HEAD commit, the open orders, the recovery
   pointers (which worklog entries / results JSONs carry the detail).
3. The file stays SHORT (one screen): the detail lives in the worklog and
   the results JSONs — this directory is an INDEX, not an archive of
   transcripts.
4. Never edit older entries except to append a one-line correction marker
   (`> CORRECTION (NNNN): ...`) — the history must stay append-only, the
   same discipline as the worklog.

## The house template

```markdown
# Session NNNN — <one-line description>

- **Date**: YYYY-MM-DD
- **HEAD at end**: <commit> (<one-line subject>)
- **Last Task ID**: <n>
- **Ledger (open)**: <the open items, one line each>
- **Closed this session**: <one line each>
- **Open orders / next steps**: <the standing instructions>
- **Recovery pointers**: worklog Task <n>; scripts/<file>.py +
  <file>_results.json; download/<volume>.pdf
- **Hygiene notes**: PAT persisted at .secrets (root, gitignored) +
  scripts/restore_pat.sh; venv = `pip install --break-system-packages
  python-flint` + numpy/scipy/matplotlib after a reset.
```

## Index

- `0001_pre_task32_recovery.md` — the backfilled pre-Task-32 state
  (reconstructed after the context loss that followed Task 31/Volume XIII;
  written at Task 32 recovery time from the repo + the transferred
  summary; carries the 0002 correction marker).
- `0002_task32_class_level.md` — Task 32: the class-level adjudication
  (the escape retracted; the structural x^4 law; the kappa sign
  resolved; the p-convexity; the V-cone).
