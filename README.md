# Vibe Coding Rules Dynamic

[![Validation](https://github.com/dhikaz007/vibe_coding_rules_dynamic/actions/workflows/validate-ruleset.yml/badge.svg)](https://github.com/dhikaz007/vibe_coding_rules_dynamic/actions/workflows/validate-ruleset.yml)
[![Release](https://github.com/dhikaz007/vibe_coding_rules_dynamic/actions/workflows/release.yml/badge.svg)](https://github.com/dhikaz007/vibe_coding_rules_dynamic/actions/workflows/release.yml)

One reusable Flutter rule set with selectable architecture profiles.

## Available profiles

- `go_router_get_it` — `go_router`, `go_router_builder`, `get_it`, and `injectable`.
- `flutter_modular_v5` — legacy `Module`, `ChildRoute`/`ModuleRoute`, `Bind`, and `RouteGuard`.
- `flutter_modular_v6` — `routes(r)`, `r.child`/`r.module`, module imports, and `exportedBinds`.
- `flutter_modular_v7` — `createModule`, `ModularApp.routerConfigOf`, function guards, and v7 bind APIs.

## Use in an application

Copy [templates/PROJECT_PROFILE.md](templates/PROJECT_PROFILE.md) to the root of the Flutter application and select exactly one profile. Configure the application's agent entrypoint to read this repository's `AGENTS.md` before implementation.

```md
profile: go_router_get_it
```

Universal rules are under `rules/` and include the complete state-management,
pagination, UI, code-generation, network, security, testing, and workflow
contracts. Stack-specific routing, DI, architecture, and folder conventions
are under `profiles/<profile>/`. Do not combine profile documents in a single
application.

Each profile includes `profile.yaml` metadata so Flutter Agents CLI can create a preset and determine its architecture, routing, DI, and compatible dependencies.

## Release

Push a version tag after validation succeeds to create a GitHub Release with generated notes:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Continuous validation

Every push and pull request to `main` runs `agents ruleset validate` through GitHub Actions. The check rejects missing required profile documents or metadata before the rules are merged. A profile smoke test also initializes a temporary project with each available profile and confirms its generated dynamic rule files.
