---
id: setup-structured-logging
type: playbook
title: Set Up Production Structured Logging
summary: Configure structured JSON logging with context propagation, sensitive data redaction, and environment isolation.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Set Up Production Structured Logging

1. Choose JSON-formatted structured output for production and colorized readable
   text for local development; avoid ad-hoc `print()` and unstructured string concatenation.
2. Propagate a unique `request_id` or `trace_id` through every incoming HTTP request,
   background job, and downstream service call using Python `contextvars`.
3. Standardize log event schemas: include timestamp (ISO 8601), log level, logger name,
   event name, trace identifiers, and structured payload fields.
4. Implement automatic redaction filters for sensitive fields (e.g. `password`, `token`,
   `authorization`, `api_key`, and personally identifiable information).
5. Capture full exception stack traces with `exc_info=True` only at service boundaries;
   do not log redundant raw tracebacks across multiple nested catch blocks.
6. Verify log generation under test by asserting structured dictionary fields
   rather than brittle substring matches.
