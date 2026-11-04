# Maintainer run-through record

## 2026-10-11 — authored from official documentation (mechanical verification only)

- Course authored against the VS Code GitHub Copilot documentation at
  code.visualstudio.com/docs/copilot, fetched 2026-10-11 (pages: local
  agents and session controls, custom instructions, review and revert
  agent changes, Agent Skills), and the shared `report-tool` core.
  `TASK.md`, `tests/`, `scenario/`, `starter/`, `solution/` are
  byte-identical to the Claude Code / Codex / Cursor course cores —
  enforced by the `core-group` check in `tools/verify_courses.py`.
- Version reference: VS Code 1.134 with the Copilot harness on the Agent
  Host, as the documentation describes it on that date. No VS Code build
  was installed for this record.
- Documented behaviors the lessons depend on (sourced, not observed):
  - Chat input controls: Session Target (Copilot), Agent role
    (Agent / Plan / Ask), Permissions (Manual permissions / Allow all),
    Code isolation (Folder / New Worktree; worktree sessions are always
    Allow all; the isolation choice exists only in the Agents window).
  - In Agent Host sessions edits are saved directly with no pending
    Keep/Undo state; review happens in the diff view and Source Control;
    Restore Checkpoint restores files and chat history but does not
    reverse completed terminal commands.
  - `chat.checkpoints.showFileChanges` and the
    `chat.tools.edits.autoApprove` glob setting for sensitive-file
    approval.
  - `.github/copilot-instructions.md` / `AGENTS.md` as always-on project
    instructions; `.github/instructions/*.instructions.md` attached by
    `applyTo` when the agent creates or modifies a matching file;
    References in the response show which instructions were used.
  - Agent Skills discovered from `.github/skills/<name>/SKILL.md`, where
    `<name>` must equal the skill's `name` field. Lesson 1 therefore
    installs the live FlyPython Skill (name `flypython-challenges`) at
    `.github/skills/flypython-challenges/SKILL.md`.
- Commands and results (Linux, Python 3.12):
  - `python verify.py starter --expect-failure` — exit 0; the seven
    expected failures reproduced.
  - `python verify.py solution` — exit 0; 9/9 tests pass.
  - `python verify.py` — exit 1 on the shipped starter; l03/l04 `[open]`,
    l01/l02/l05 `[pending]`.
  - `python tools/verify_courses.py` — contract satisfied, core identical
    with the other `report-tool` members.
- **Not done:** any run inside VS Code with Copilot. No Copilot account was
  used; every Copilot behavior described in the lessons is sourced from
  official documentation, not observed.

## Pending before this course can be called taught-in-tool

- One full agent-taught run-through with GitHub Copilot in VS Code
  ("start lesson 1" through the Lesson 5 checkpoint) on a current build,
  recording observed deviations from `COURSE.md` here — in particular
  whether Manual permissions prompts before the Skill URL fetch, and
  whether the `applyTo` file shows up in References as Lesson 2 expects.
- Whether the Copilot Free plan's monthly chat request allowance lasts the
  whole course is unverified.

## 2026-11-04 — claim-instruction accuracy fix (mechanical re-verify)

- Lesson and hint text corrected to match the shipped verifier: the default
  `python verify.py` prints no claim code for reflection checkpoints
  (l01/l02/l05); the code appears only after the explicit
  `--attest ID` flag for a completed reflection. L02/L05 checkpoints now
  name the command; L01 hint 3 no longer promises a code from the default
  run; evidence sections keep both command transcripts.
- Verification: clean-copy runs of `verify.py check --json` with partial
  and full `--attest` sets reproduced the documented states; repository
  gates (`make check`) green at this change. No live GitHub Copilot agent run —
  the pending live run-through below still stands.

## Deviation log

(none yet — no live run has happened)
