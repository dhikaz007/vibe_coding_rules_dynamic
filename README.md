# Vibe Coding Rules Dynamic

[![Validation](https://github.com/dhikaz007/vibe_coding_rules_dynamic/actions/workflows/validate-ruleset.yml/badge.svg)](https://github.com/dhikaz007/vibe_coding_rules_dynamic/actions/workflows/validate-ruleset.yml)
[![Release](https://github.com/dhikaz007/vibe_coding_rules_dynamic/actions/workflows/release.yml/badge.svg)](https://github.com/dhikaz007/vibe_coding_rules_dynamic/actions/workflows/release.yml)

One reusable Flutter rule set with selectable architecture profiles.

## What this is

Every Flutter project answers the same architecture questions: where does a Cubit get its dependencies, who is allowed to navigate, what happens when an API returns a field it never documented, which value is allowed to come from an environment variable. Answer them differently in two projects and you own two codebases.

This repository holds those answers once. A project selects **one** profile, and the universal rules plus that profile's documents are installed into it. Nothing is registered in code — the agent reads them before it writes.

## Quick start

From the root of a Flutter project, with the Flutter Agents CLI installed:

```bash
agents ruleset add vibe-coding-rules https://github.com/dhikaz007/vibe_coding_rules_dynamic
agents ruleset use vibe-coding-rules go_router_get_it
agents ruleset map --all
```

Replace `go_router_get_it` with one of the profiles listed below. The third command is the one people miss: `ruleset use` installs only the profile documents, so without `ruleset map --all` the universal rules never arrive.

Confirm it worked:

```bash
cat PROJECT_PROFILE.md
ls docs/dynamic-rules/rules/
```

```text
profile: go_router_get_it          ← the profile you selected

CODEGEN.md  CORE.md  ENVIRONMENT.md  NETWORK.md  SECURITY.md
STATE-MANAGEMENT.md  TESTING.md  UI.md  WORKFLOW.md
```

If `docs/dynamic-rules/rules/` is empty, `map --all` did not run. If `PROJECT_PROFILE.md` names a different profile than the one you want, run `ruleset use` again — a project holds exactly one profile.

After that, ask the agent for the work. It reads `PROJECT_PROFILE.md` and loads only the rules for the concerns your task actually touches.

## Available profiles

- `go_router_get_it` — `go_router`, `go_router_builder`, `get_it`, and `injectable`.
- `flutter_modular_v5` — legacy `Module`, `ChildRoute`/`ModuleRoute`, `Bind`, and `RouteGuard`.
- `flutter_modular_v6` — `routes(r)`, `r.child`/`r.module`, module imports, and `exportedBinds`.
- `flutter_modular_v7` — `createModule`, `ModularApp.routerConfigOf`, function guards, and v7 bind APIs.

A profile fixes routing, dependency injection, architecture, and folder conventions. The universal rules cover everything a profile cannot decide for you, and they never name a stack API — a universal rule states the decision and delegates the mechanism to the profile.

## What gets installed

```text
PROJECT_PROFILE.md
docs/dynamic-rules/profiles/<profile>/ARCHITECTURE.md
docs/dynamic-rules/profiles/<profile>/ROUTING.md
docs/dynamic-rules/profiles/<profile>/DEPENDENCY-INJECTION.md
docs/dynamic-rules/profiles/<profile>/FOLDER-STRUCTURE.md
docs/dynamic-rules/rules/*.md
docs/RULES-MAP.md
```

`docs/RULES-MAP.md` records which source is active per concern, so a project rule can override a dynamic one without deleting either.

Requires Flutter Agents CLI `2.7.0` or newer to install every rule in this repository. On `2.8.0` or newer a rule added here reaches projects without a CLI upgrade; below that, a newly added rule is skipped rather than installed.

Without the CLI, copy [templates/PROJECT_PROFILE.md](templates/PROJECT_PROFILE.md) to the application root and configure the agent entrypoint to read this repository's `AGENTS.md` before implementation:

```md
profile: go_router_get_it
```

## What the universal rules cover

`rules/` holds the state-management, pagination, UI, code-generation, JSON/serialization, environment, network, security, testing, and workflow contracts. The JSON contract covers `build.yaml` field renaming, enum fallbacks, and converters; the environment contract covers `AppConfig`, `.env.example` placeholders, flavors, and build-time defines. Those decisions are never repeated inside a profile, and a profile never restates a universal rule.

Each profile includes `profile.yaml` metadata so Flutter Agents CLI can create a preset and determine its architecture, routing, DI, and compatible dependencies. See [COMPATIBILITY.md](COMPATIBILITY.md) for the packages each profile requires.

## Release

Push a version tag after validation succeeds to create a GitHub Release with generated notes:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Continuous validation

Every push and pull request to `main` runs `agents ruleset validate` through GitHub Actions. The check rejects missing required profile documents or metadata before the rules are merged. A second check rejects any stack-specific API named inside `rules/`, because universal rules are copied into every profile and must delegate routing, DI, and folder decisions to `profiles/<selected>/`.

A profile smoke test also initializes a temporary project with each available profile and confirms that exactly one profile was installed and that every file in `rules/` was installed. Adding a universal rule that no concern can claim therefore fails CI instead of silently never reaching a project.
