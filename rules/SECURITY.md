# Security

- Never hardcode or log credentials, tokens, raw authorization headers, or sensitive personal data.
- Follow the consuming project's approved secure-storage, TLS, authentication-refresh, and telemetry conventions.
- Mutations require duplicate-submit protection and the project's idempotency/mutation-safety convention.
- Do not weaken certificate, authorization, validation, or redaction behavior to make development easier.
