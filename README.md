# Vibe Coding Rules Dynamic

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

Universal rules are under `rules/`. Stack-specific rules are under `profiles/<profile>/`. Do not combine profile documents in a single application.
