# Persistent User Preferences

These instructions persist across sessions and rollbacks. Read this file FIRST in every new session.
A mirror copy lives in the GitHub repo MIKEAA2020/master (PREFERENCES.md) so the rules also
persist on the remote. The worklog banner repeats the language rule.

## Language

- **ALWAYS respond in English, never in Chinese. PERMANENT COMMAND. Do not ask again. Do not revert.**
  This was ordered twice (2026-09-27 and 2026-09-28) after a Chinese-language violation.
  Applies to: every chat response, every generated document, every figure label, every filename,
  every summary, every commit message. No exceptions for any future session, model, or rollback.
- If any internal note or log is drafted in another language, translate it to English before delivery.

## Session Behavior

- When the user says "read and wait": read the material fully, confirm completion in one line, then WAIT.
  Do not summarize, analyze, advise, or offer next steps unless explicitly asked.

## Credentials and Repository Protocol (2026-09-28)

- GitHub PAT for MIKEAA2020 is stored persistently at:
  `/home/z/my-project/.secrets/github_pat.txt` (0600),
  `~/.git-credentials` (git credential helper store), and `~/.bashrc` (`$GITHUB_PAT`).
- **All creations from every round (documents, figures, scripts, results) must be committed and
  pushed to the MIKEAA2020/master repository at the end of each session.**
  Never commit the PAT or any credential anywhere.
- Before committing, sweep deliverables for credential leakage (`rg github_pat_`).

## Honesty Discipline

- Distinguish rigorously: (i) results already in the manuscripts (cite file + version),
  (ii) results derived in-session (give the computation/proof), (iii) conjectures (label as open).
  Never overstate novelty; never present a repackaged theorem as a new theory.
