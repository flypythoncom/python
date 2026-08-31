# Security policy

## Supported versions

Security fixes apply to the default branch and the currently deployed
`python.flypython.com` site. Historical commits, forks, and archived catalog
entries are not supported releases.

## Report a vulnerability privately

Do not open a public issue for a security vulnerability. Use
[GitHub's private vulnerability reporting](https://github.com/flypythoncom/python/security/advisories/new).
If that form is unavailable, email hello@flypython.com with the subject
`FlyPython security report`.

Include:

- The affected URL, file, workflow, or commit
- Clear reproduction steps and impact
- Any proof of concept needed to confirm the issue
- Whether the issue is already public
- A safe way to contact you

Remove credentials and personal data that are not required to reproduce the
issue. We will acknowledge reports on a best-effort basis, investigate, and
coordinate disclosure after a fix is available.

## In scope

Examples include:

- Script injection or unsafe rendered catalog content
- A link-checking path that can reach private, loopback, or metadata services
- Workflow permission escalation or untrusted-code execution
- Exposed credentials, DNS takeover, or custom-domain control issues
- Dependency or build-chain compromise with a demonstrated impact

Broken links, outdated descriptions, ordinary 403/429 responses, and resource
quality disagreements are not security vulnerabilities. Use the broken-link or
resource-proposal issue form for those reports.

## Safe harbor

Make a good-faith effort to avoid privacy violations, service disruption, data
destruction, and access beyond what is needed to demonstrate the issue. Do not
perform denial-of-service testing or interact with third-party resources beyond
their published policies. We will not pursue action against good-faith research
that follows this policy.
