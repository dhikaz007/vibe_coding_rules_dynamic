# Dynamic Flutter Coding Rules Design

## Goal

Provide one reusable rule repository for Flutter projects without copying a full rule set per routing/DI stack. Each consuming project selects exactly one architecture profile through `PROJECT_PROFILE.md`.

## Repository layout

```text
Vibe Coding Rules Dynamic/
├── AGENTS.md
├── README.md
├── rules/                         # stack-neutral rules
│   ├── UI.md
│   ├── STATE-MANAGEMENT.md
│   ├── SECURITY.md
│   ├── TESTING.md
│   ├── CODEGEN.md
│   └── WORKFLOW.md
└── profiles/
    ├── go_router_get_it/
    │   ├── ARCHITECTURE.md
    │   ├── ROUTING.md
    │   ├── DEPENDENCY-INJECTION.md
    │   └── FOLDER-STRUCTURE.md
    └── flutter_modular/
        ├── ARCHITECTURE.md
        ├── ROUTING.md
        ├── DEPENDENCY-INJECTION.md
        └── FOLDER-STRUCTURE.md
```

## Profile selection

Each Flutter application keeps a small `PROJECT_PROFILE.md` in its own repository:

```md
profile: go_router_get_it
```

or:

```md
profile: flutter_modular
```

`AGENTS.md` first reads this file, validates the selected profile, then loads only that profile's routing, DI, architecture, and folder-structure rules. A project never loads both profiles.

## Profile responsibilities

`go_router_get_it` owns `go_router`, `go_router_builder`, typed route generation, `get_it`, `injectable`, and the selected feature-first folder structure.

`flutter_modular` owns `flutter_modular`, Modular binds/routes, Modular lifecycle patterns, and the selected Modular folder structure.

## Universal rule responsibilities

Universal rules contain behavior that does not depend on routing or DI. This includes UI, localization, security, testing, code generation when applicable, workflow, pagination, and shared state conventions.

The following recently agreed conventions are universal:

- pagination status builders and explicit `PagedListView.separated` / `PagedAlignedGridView.count` selection
- adaptive `PaginationFAB`
- explicit function return types and named records for several related values
- public extracted widgets only; no `_buildXxx()` or private widget classes
- one barrel file per Dart source folder, including a folder with one file

## Migration

`Vibe Coding Rules - Token Optimized` supplies the initial `go_router_get_it` profile. `Vibe Coding Rules Modular - Token Optimized` supplies the initial `flutter_modular` profile. Equivalent stack-neutral content is consolidated into `rules/`; stack-specific content remains in its profile.

The original folders are retained unchanged. The new directory is a standalone repository candidate that can later be initialized and published to GitHub.

## Verification

- Both profile identifiers resolve from `PROJECT_PROFILE.md`.
- `AGENTS.md` directs agents to exactly one selected profile.
- No universal rule names a stack-specific API unless it is conditional and delegated to the selected profile.
- All agreed common rules appear once in `rules/`.
