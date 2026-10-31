# Project Conventions Discovery Design (v3)

Date: 2026-10-31
Status: approved, pending implementation plan
Supersedes: v2 of the same file
Evidence: `docs/research/evidence/2026-10-31-conventions-evidence.md`

## Problem

The rule set installs one profile per project, but several rules name concrete
paths and symbols that only hold for the reference project:

- `rules/UI.md:16-20` names `AppButton`, `AppText`, `AppTextField`, `AppSvg`,
  `AppSpacing`/`AppDimensions`.
- `rules/UI.md:21` names a project flushbar helper without a path.
- `rules/UI.md:37` names `AppDateFormatter`.
- `rules/UI.md:38` names `PaginationFAB`.
- `rules/UI.md:40` names `presentation/widgets/` and `presentation/components/`.
- `profiles/*/FOLDER-STRUCTURE.md` names `core/widgets/app_<name>.dart`.
- `templates/PROJECT_PROFILE.md` carries only `profile:`.

Evidence from four projects shows symbol names, kinds, and folder layouts
diverge at rename level. Naming families do not overlap: `App*`, `Custom*`,
`*App`. A rule that names a symbol is wrong in at least three of the four.

`rules/CORE.md:12` already makes the nearest comparable implementation the first
source of convention truth. What is missing is a durable place to record what
the scan found, so discovery is paid once.

## Decision model

The conventions file is a cache of observation, not a source of truth. Authority
order:

1. user instruction
2. nearest comparable implementation in code (`CORE.md:12`)
3. `docs/dynamic-rules/PROJECT-CONVENTIONS.md`
4. `profiles/<selected>/*` — defaults
5. `rules/*.md` — universal contracts

The file overrides profile defaults for paths, symbols, and layout only. It never
overrides profile decisions about routing, DI lifetime, layering, or feature
boundaries.

The conventions layer is profile-independent: one file serves
`go_router_get_it`, `flutter_modular_v5`, `v6`, and `v7`.

## File schema

Path: `docs/dynamic-rules/PROJECT-CONVENTIONS.md`.

```md
# Project conventions (observed)
<!-- verified: YYYY-MM-DD -->
<!-- mode: adopted -->

## Role map
| role | kind | source | default | alternates | path |
|---|---|---|---|---|---|
| text | class | observed | CustomText | - | lib/core/shared/text.dart |
| button | class | observed | CustomButton | - | lib/core/shared/button.dart |
| text_field | class | observed | CustomTextField | - | lib/core/shared/text_field.dart |
| svg | class | observed | SvgWidget | - | lib/core/shared/svg.dart |
| feedback | static-class | observed | AppNotifier | - | lib/core/notification/app_notifier.dart |
| date_formatter | extension | observed | DateTimeStringX | - | lib/core/extensions/string_datetime.dart |
| spacing | none | none | none observed | - | - |
| pagination_fab | none | none | none observed | - | - |

## Layout
shared_widget_dir: lib/core/shared
feature_dir: lib/feature
feature_subdirs: screens, config, cubit, domain
feature_component_dir: screens/components
barrel_policy: part-barrel in extensions, none in shared

## Localization
status: absent | easy_localization | arb
translations_dir: assets/translations
default_locale: id
key_access: LocaleKeys

## Assets
dir: assets/
generated_refs: flutter_gen

## Icons
library: figma svg assets
fallback: -

## Design authority
design_doc: DESIGN.md | none

## Unresolved
- spacing: no shared token found; task must ask before adding one
```

### Content rules

- Role names are fixed by the catalog below. A project never invents a role.
- `kind` is one of `class`, `static-class`, `extension`, `function`, `none`.
- `source` is one of `observed`, `profile-default`, `none`.
- `default` is the symbol to use. `alternates` lists other valid symbols for the
  same role with comparable usage.
- A role can map to several symbols. That is normal, not ambiguity.
- An absent role is `kind: none`, `source: none`, `default: none observed`.
  Never omit the row.
- `## Unresolved` is mandatory and lists anything the scan could not settle.
- `mode: adopted` for a scanned project, `mode: fresh` for a new one.
- No package versions, state management, or storage facts. Those belong to
  `pubspec.yaml`.
- No field that no rule consumes. The catalog holds only roles a rule actually
  reuses, plus the layout, localization, asset, icon, and design-authority
  sections that rules reference.

### Role catalog

Eight roles, one per reuse directive in `rules/`:

| Role | Rule that consumes it |
|---|---|
| `text` | `UI.md:17` text component |
| `button` | `UI.md:16` button component |
| `text_field` | `UI.md:18` text field component |
| `svg` | `UI.md:19` SVG component |
| `spacing` | `UI.md:20` `AppSpacing`/`AppDimensions` |
| `feedback` | `UI.md:21` flushbar helper |
| `date_formatter` | `UI.md:37` `AppDateFormatter` |
| `pagination_fab` | `UI.md:38`, `STATE-MANAGEMENT.md:124` |

The button role is one role, not two. `UI.md:16` says "Button", and projects that
offer primary and secondary variants express them as `default` plus `alternates`
(revamp: `ButtonPrimary` + `ButtonSecondary`; dms: `AppPrimaryButton` +
`AppSecondaryButton`; LMS-ECampus: one `CustomButton` for both).

Roles are not a widget inventory. `dialog`, `bottom_sheet`, and
`loading_overlay` exist in several projects but no rule directs the agent to
reuse a specific symbol for them (`STATE-MANAGEMENT.md:61` only forbids a Cubit
from showing them), so they have no row. Add a role only when a rule begins to
consume it.

### None branches

When a role is `none observed`, the consuming rule degrades instead of forcing
the agent to invent a symbol:

- `spacing: none` → raw spacing is allowed; do not create `AppSpacing`.
- `pagination_fab: none` → skip the back-to-top affordance; do not create
  `PaginationFAB`.
- `feedback: none` → fall back to `ScaffoldMessenger`; record in `## Unresolved`
  only if the project needs consistent styling.

Without these branches, the `UI.md` rewrite would still push the agent to create
symbols the project does not have.

## Fresh-project path

When the scan finds no shared widget directory and no role candidates:

1. Write the file with `mode: fresh`, every role `kind: none`, `source: none`,
   layout copied from the selected profile.
2. Do not ask questions.
3. Profile defaults apply. The first task that needs a symbol uses the profile
   default path and name.

This is the no-adaptation path for greenfield projects. It also gives the next
session a place to record the first observed symbol.

## Discovery procedure

Runs only when the file does not exist.

1. Locate the shared widget directory: `glob` for `**/widgets`, `**/shared`,
   `**/components` at bounded depth. Prefer the one containing widget classes.
2. Classify widget roles by shape, not name. For each `class ... extends
   StatelessWidget|StatefulWidget` in that directory, inspect the Flutter
   primitive it wraps:
   - `Text`, `RichText` → `text`
   - `ElevatedButton`, `FilledButton`, `TextButton` → `button`
   - `TextFormField`, `TextField` → `text_field`
   - `SvgPicture` → `svg`
3. Extensions and helpers: search `DateFormat(` inside a `class` or `extension`
   for `date_formatter`; a `Flushbar`, `showSnackBar`, or `showDialog` wrapper
   for `feedback`; a class or const set of doubles for `spacing`.
4. Feature layout: list one representative `feature/<name>` directory and record
   its subdirectory names.
5. Barrel policy: treat a file whose body is only `export`/`part` lines as a
   barrel; record where it exists.
6. Read `pubspec.yaml` for localization, asset, and icon dependencies.
7. Look for `DESIGN.md` and record its presence under `design_doc`.
8. Write the file and report five lines: chosen directories, roles found, roles
   absent, rejected candidates.

Ambiguity: two candidates of the same role and the same specificity with no
usage evidence. Resolution order is usage count (`grep -c`), then the nearest
comparable screen, then ask and record in `## Unresolved`. Never guess.

## Self-heal per task

- Only the role or layout field touched by the task is verified.
- One narrow lookup: glob inside the recorded directory, or grep the recorded
  symbol name.
- Match: proceed.
- Mismatch, rename, or missing path: use the code, update that row and
  `verified:`, report one line.
- If the role was `none` and the project now has a candidate, record it.
- No broad rescan. No updates outside the touched concern.

## Wiring

New file:

- `templates/PROJECT-CONVENTIONS.md` — the skeleton above with empty values.

Changed files:

- `AGENTS.md` — after validating `PROJECT_PROFILE.md`, read the conventions file
  when present; skip when absent.
- `rules/CORE.md` — authority order, role vocabulary, ambiguity gate, self-heal.
- `rules/UI.md` — replace every symbol and path literal with a role reference,
  falling back to the profile default when the file is absent. This covers
  `:16-21`, `:37`, `:38`, `:40`, and the none branches above.
- `rules/STATE-MANAGEMENT.md` — replace the `PaginationFAB` literal at `:124`
  with the `pagination_fab` role and its none branch.
- `profiles/*/FOLDER-STRUCTURE.md` (4 files) — mark `core/widgets/app_<name>.dart`
  as the default used only when the conventions file is absent.
- `.github/workflows/validate-ruleset.yml` — deny project-local identifiers
  inside `rules/`; verify the template carries 8 role rows and
  `## Unresolved`.
- `README.md` — quick start, fresh mode, installed-files list.

No new rule file. `CORE.md` already owns convention resolution, so the router is
unchanged.

## Validation

CI additions in `.github/workflows/validate-ruleset.yml`:

- deny list inside `rules/`: `AppButton`, `AppText`, `AppTextField`, `AppSvg`,
  `AppSpacing`, `AppDimensions`, `AppDateFormatter`, `PaginationFAB`,
  `core/widgets`, `presentation/widgets`;
- template check: 8 role rows present, `## Unresolved` present, `mode` comment
  present;
- existing profile smoke test unchanged.

## Acceptance criteria

1. `LMS-ECampus` scan yields `lib/core/shared`, `CustomText`, `CustomButton`,
   `SvgWidget`, `AppNotifier`, `DateTimeStringX`, `spacing: none`,
   `pagination_fab: none`.
2. `dms_mobile` scan yields `lib/core/widgets`, `AppText`, `AppPrimaryButton`
   with `AppSecondaryButton` as alternate, `AppSvg`, `AppFlushbar`,
   `AppDateFormatter` as `class`.
3. `fire_todo` scan yields `lib/core/widgets`, `TextApp`, `ButtonPrimary`,
   `SvgApp`, `SnackbarApp`, `DateExtension` as `extension`,
   `localization: absent`.
4. A fresh project with no widget directory produces `mode: fresh`, all roles
   `none`, and the agent proceeds without asking.
5. A second session performs no directory-wide scan, only narrow verification.
6. CI fails when a project-local symbol or concrete widget path reappears in
   `rules/`.

## Risks

- A role with several valid symbols can be used inconsistently within one
  project. Mitigation: `default` is explicit, alternates require usage evidence.
- Folder refactors leave the file stale until the role is touched. Mitigation:
  self-heal on first use.
- Two branches editing the file concurrently can conflict. Impact is small.

## Out of scope

- Installing the conventions file through the CLI.
- Recording package versions, state management, or storage choices.
- Auto-refactoring a project to match a profile default.
- Normalizing a project's naming to one family.
- Inventorying widgets that no rule reuses.
