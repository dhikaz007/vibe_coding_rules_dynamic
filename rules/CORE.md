# Core Rules

- Requirements and visual design supplied by the consuming project are authoritative.
- Use feature-first Pragmatic Clean Architecture; keep feature-specific code out of shared application infrastructure.
- Reuse the nearest valid pattern and make the smallest complete change.
- Do not create speculative abstractions, empty layers, packages, or unrelated refactors.
- A mutation must prevent duplicate submission in both state logic and UI.
- Preserve existing list content while refreshing or loading another page.

## Project-specific convention resolution

- “Existing”, “established”, “approved”, and “project convention” always mean the nearest comparable implementation first, then the consuming project's documented rule.
- If neither source defines the required convention, do not invent one: report the gap and ask for direction before changing architecture, routing, DI lifetime, transport, storage, or security behavior.
