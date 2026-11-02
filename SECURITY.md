# Security policy

Verdict is an advisory classifier. It is not a sandbox, authorization mechanism, security boundary, or replacement for deterministic validation. Never let its output alone permit destructive operations or override authoritative environment-state checks.

Logs may contain secrets. Local inference makes no network requests, but callers are responsible for safe storage and handling of their inputs.

Report vulnerabilities privately through the contact information at https://balanov.pro/ rather than opening a public issue with sensitive logs.
