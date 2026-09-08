# Workflow

- For substantial features, migrations, and cross-domain refactors: inspect the comparable implementation, requirements/design, selected profile, and only the applicable universal rules before editing.
- Implement the smallest complete vertical slice; add routes, DI, code generation, and tests only when the change actually requires them.
- Before completion: inspect the diff, verify boundaries and selected-profile compliance, run applicable tests/generation, then run `flutter analyze`.
- Do not commit or push unless the user explicitly requests it.
