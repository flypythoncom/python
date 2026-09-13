# Learning paths

Paths sequence challenge courses into badge routes. Each path lives in its
own folder with a machine-checked `path.json` contract plus bilingual module
and challenge documents.

- [Agent tools foundation](foundation/) — drive a coding agent (Claude
  Code, Codex, Cursor, DeepSeek Harness, Kimi Code, or ZCode — pick one),
  write a single-source rules file, and verify agent output by hand.
  Modules: the pick-one tool courses, the rules and verification courses,
  and a dual-agent route challenge (200 points). The orientation module is
  optional extra credit (10 points) — not required for the badge.
- [Data analysis with an agent](data-analysis/) — clean, explore, visualize,
  and report on a real dataset. Modules: the `da-eda`, `da-visualization`,
  and `da-report` courses plus an end-to-end capstone (200 points).

## Conventions

- `path.json` is the contract: module order, course references, points, and
  badge definitions; `optional: true` marks extra-credit modules that do not
  count toward the badge. `python tools/verify_paths.py` checks every path
  against the courses that actually exist in `courses/`.
- Module documents (`modules/*.md`) always ship with a `_cn.md` pair in the
  same change.
- Route capstones carry their own `TASK.md`/`TASK_cn.md`, starter inputs, a
  reviewed `solution/`, and a `verify.py` that gates the route badge.
- Points come only from checkpoints verified by `verify.py` and recorded
  with claim codes; badges are self-reported local evidence, never
  certificates.

Continue the guided experience on [flypython.com](https://flypython.com/).
