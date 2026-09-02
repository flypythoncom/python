---
id: integrate-an-external-api
type: playbook
title: Integrate an External API
summary: Wrap a third-party API behind a typed boundary with safe credentials, timeouts, retries, and deterministic tests.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Integrate an External API

1. Document the provider, endpoint, data sent, credential owner, cost limit,
   rate limit, and allowed side effects.
2. Put provider code behind a small typed interface. Validate every response;
   model output is untrusted data too.
3. Keep credentials outside source control and redact them from logs and errors.
4. Set connect and response timeouts. Retry only transient, idempotent work with
   bounded backoff; never retry an irreversible action blindly.
5. Test with a deterministic fake transport, including timeout, malformed data,
   rate limit, and partial failure. Keep live tests opt-in.
6. Verify cost, latency, logs, and the user-visible fallback in a controlled
   environment before enabling production traffic.
