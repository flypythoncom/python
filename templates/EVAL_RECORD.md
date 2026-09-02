# LLM / Agent Evaluation Record

- **Evaluation ID**: `eval-YYYY-MM-DD-01`
- **Target Model / Version**: `gpt-4o-2024-08-06` / `claude-3-5-sonnet-20241022`
- **Prompt / Commit SHA**: `<git-sha>`
- **Evaluator**: `@maintainer`

## Benchmark Results

| Metric | Baseline | Candidate | Delta | Status |
| --- | --- | --- | --- | --- |
| Schema Conformance | 98.5% | 100.0% | +1.5% | PASS |
| Exact Match Pass Rate | 84.0% | 88.5% | +4.5% | PASS |
| Average Latency (p95) | 1.42s | 1.18s | -0.24s | PASS |
| Token Cost / 1k req | $1.20 | $0.95 | -$0.25 | PASS |

## Boundary & Edge Case Regressions

- [x] Malformed JSON input handling verified
- [x] Prompt injection and system prompt leak attempts blocked
- [x] Empty response fallback verified
