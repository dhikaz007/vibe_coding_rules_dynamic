# Dynamic Flutter Coding Rules

This repository provides reusable Flutter coding rules. A consuming project selects **one** stack profile in its own `PROJECT_PROFILE.md`.

## 1. Select the profile first

Before any code change:

1. Read the consuming project's `PROJECT_PROFILE.md`.
2. Accept only one of these values:
   - `go_router_get_it`
   - `flutter_modular_v5`
   - `flutter_modular_v6`
   - `flutter_modular_v7`
3. Read `rules/CORE.md`, then the selected profile's `ARCHITECTURE.md`, `ROUTING.md`, `DEPENDENCY-INJECTION.md`, and `FOLDER-STRUCTURE.md` only when the task touches that concern.
4. Read the relevant universal rule under `rules/` only when its concern is touched.

Never load or mix both profiles. If `PROJECT_PROFILE.md` is missing or invalid, stop and ask for the profile; do not infer it from dependencies.

## 2. Universal rule router

| Concern | Rule |
|---|---|
| UI, widget extraction, localization, assets | `rules/UI.md` |
| Cubit, async state, pagination, local state | `rules/STATE-MANAGEMENT.md` |
| API contract, transport, repository/error behavior | `rules/NETWORK.md` |
| Tokens, secrets, storage, mutations, telemetry | `rules/SECURITY.md` |
| Freezed, JSON, routing/assets/localization generation | `rules/CODEGEN.md` |
| Tests | `rules/TESTING.md` |
| Substantial feature, migration, refactor | `rules/WORKFLOW.md` |

## 3. Rules always in effect

- Inspect the nearest comparable implementation before adding code.
- Never invent product requirements or API contracts.
- Presentation never calls a datasource/API client directly.
- Cubits own state transitions, never navigation/dialog/snackbar side effects.
- Use the selected profile for routing, DI, and source-tree decisions.
- Never manually edit generated files, hardcode secrets, commit, or push unless explicitly requested.
- Run the applicable focused checks and `flutter analyze` before completing a code change.
