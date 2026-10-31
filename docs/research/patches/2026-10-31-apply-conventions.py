#!/usr/bin/env python3
"""Apply the PROJECT-CONVENTIONS wiring edits (plan Tasks 1-8).

Dry-run by default: prints OK/MISSING per replacement.
Run with --apply to write the files.

Exact-string replace. Every 'old' must appear exactly once.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

TEMPLATE = """# Project conventions (observed)
<!-- verified: YYYY-MM-DD -->
<!-- mode: fresh -->

## Role map
| role | kind | source | default | alternates | path |
|---|---|---|---|---|---|
| text | none | none | none observed | - | - |
| button | none | none | none observed | - | - |
| text_field | none | none | none observed | - | - |
| svg | none | none | none observed | - | - |
| feedback | none | none | none observed | - | - |
| date_formatter | none | none | none observed | - | - |
| spacing | none | none | none observed | - | - |
| pagination_fab | none | none | none observed | - | - |

## Layout
shared_widget_dir: core/widgets
feature_dir: lib/feature
feature_subdirs: data, domain, presentation
feature_component_dir: presentation/components
barrel_policy: none

## Localization
status: absent
translations_dir: assets/translations
default_locale: en
key_access: none

## Assets
dir: assets/
generated_refs: none

## Icons
library: none
fallback: -

## Design authority
design_doc: none

## Unresolved
- none
"""

CORE_OLD = """## Project-specific convention resolution

- “Existing”, “established”, “approved”, and “project convention” always mean the nearest comparable implementation first, then the consuming project's documented rule.
- If neither source defines the required convention, do not invent one: report the gap and ask for direction before changing architecture, routing, DI lifetime, transport, storage, or security behavior.
"""

CORE_NEW = """## Project-specific convention resolution

Authority order, highest first:

1. user instruction
2. nearest comparable implementation in code
3. `docs/dynamic-rules/PROJECT-CONVENTIONS.md`
4. the selected profile's documents
5. the universal rules

- “Existing”, “established”, “approved”, and “project convention” always mean the nearest comparable implementation first, then the conventions file, then the consuming project's documented rule.
- Read `docs/dynamic-rules/PROJECT-CONVENTIONS.md` when present. It records observed symbols, paths, and layout; when absent, fall back to the profile default.
- The conventions file is a cache of observation, not a source of truth. Verify only the concern the task touches: one narrow lookup in the recorded directory or for the recorded symbol. On mismatch, use the code and update the file.
- Resolve roles by role name, never by symbol name. The role map holds `default` and `alternates`; a role mapped to `none observed` means the project has no such symbol, and the consuming rule's none branch applies.
- If neither code nor the file defines the required convention, do not invent one: report the gap and ask for direction before changing architecture, routing, DI lifetime, transport, storage, or security behavior.

## Convention discovery

Run once, only when `docs/dynamic-rules/PROJECT-CONVENTIONS.md` does not exist:

1. Locate the shared widget directory: glob `**/widgets`, `**/shared`, `**/components` at bounded depth; prefer the one containing widget classes.
2. Classify widget roles by shape, not name. For each `class ... extends StatelessWidget|StatefulWidget` there, inspect the Flutter primitive it wraps: `Text`/`RichText` → `text`; `ElevatedButton`/`FilledButton`/`TextButton` → `button`; `TextFormField`/`TextField` → `text_field`; `SvgPicture` → `svg`.
3. Search `DateFormat(` inside a `class` or `extension` for `date_formatter`; a `Flushbar`/`showSnackBar`/`showDialog` wrapper for `feedback`; a class or const set of doubles for `spacing`; a back-to-top floating action for `pagination_fab`.
4. Record feature layout from one representative `feature/<name>` directory, the barrel policy, localization/asset/icon dependencies from `pubspec.yaml`, and `DESIGN.md` presence.
5. If a role has several candidates of the same specificity, rank by usage count (`grep -c`), then the nearest comparable screen; only then ask and record in `## Unresolved`. Never guess.
6. If the project has no shared widget directory and no role candidates, write `mode: fresh` with every role `none` and the profile-default layout; ask nothing.
"""

UI_CORE_OLD = """## Core-widget first

Prefer existing core components:
- Button → `AppButton`
- Text → `AppText`
- TextField → `AppTextField`
- SVG → `AppSvg`
- Spacing → project `AppSpacing`/`AppDimensions`, not raw spacing widgets in screens
- Feedback → project flushbar helper, not `ScaffoldMessenger.showSnackBar`

Before creating a component, search existing `core/widgets` and feature widgets/components.

Interaction conventions:
- Chip-like control → Flutter Chip family first; use transparent side if project theme otherwise adds unwanted border.
- Tabs/segments → `TabBar` + `TabBarView` first; TEMPLATE-PROJECT default: no swipe (`NeverScrollableScrollPhysics`).
- Button-like actions → `TextButton`/`IconButton`/`TextButton.icon`, not `GestureDetector`.
- `GestureDetector`/`InkWell` is for non-button tappable surfaces.
- Icons → Figma-exported SVG/generated asset first; fallback to `<ICON_LIBRARY>` only when no asset exists. Do not use default `Icons.*` if project policy chooses a dedicated icon library.
- Rich inline text → `Text.rich(...)`.
- App-wide missing reusable primitive → create once in `core/widgets` with `app_` prefix.
"""

UI_CORE_NEW = """## Core-widget first

Prefer existing project components by role. Resolve each role from `docs/dynamic-rules/PROJECT-CONVENTIONS.md` when present, then the selected profile's default:

- button role → button component
- text role → text component
- text_field role → text field component
- svg role → SVG component
- spacing role → project spacing/dimension tokens, not raw spacing widgets in screens
- feedback role → project feedback helper, not `ScaffoldMessenger.showSnackBar`

None branches: `spacing: none` allows raw spacing; `feedback: none` falls back to `ScaffoldMessenger`.

Before creating a component, search the recorded shared-widget directory and feature widgets/components.

Interaction conventions:
- Chip-like control → Flutter Chip family first; use transparent side if project theme otherwise adds unwanted border.
- Tabs/segments → `TabBar` + `TabBarView` first; TEMPLATE-PROJECT default: no swipe (`NeverScrollableScrollPhysics`).
- Button-like actions → `TextButton`/`IconButton`/`TextButton.icon`, not `GestureDetector`.
- `GestureDetector`/`InkWell` is for non-button tappable surfaces.
- Icons → Figma-exported SVG/generated asset first; fallback to the icon library recorded in the conventions file only when no asset exists. Do not use default `Icons.*` if project policy chooses a dedicated icon library.
- Rich inline text → `Text.rich(...)`.
- App-wide missing reusable primitive → create once in the recorded shared-widget directory, following the project's naming family.
"""

UI_DATE_OLD = """- Date/time: TEMPLATE-PROJECT `<DEFAULT_TIMEZONE>`, `<DATE_FORMAT>`, `<DEFAULT_LOCALE_CODE>` through shared `AppDateFormatter`; do not instantiate DateFormat repeatedly in features."""
UI_DATE_NEW = """- Date/time: TEMPLATE-PROJECT `<DEFAULT_TIMEZONE>`, `<DATE_FORMAT>`, `<DEFAULT_LOCALE_CODE>` through the `date_formatter` role; do not instantiate `DateFormat` repeatedly in features."""

UI_FAB_OLD = """- Paginated-list back-to-top uses the shared `PaginationFAB`. When it shares a screen with other floating actions, preserve the existing primary action and follow the screen's established FAB hierarchy, spacing, and layout."""
UI_FAB_NEW = """- Paginated-list back-to-top uses the `pagination_fab` role; if that role is `none observed`, skip the back-to-top affordance. When it shares a screen with other floating actions, preserve the existing primary action and follow the screen's established FAB hierarchy, spacing, and layout."""

UI_EXTRACT_OLD = """- Do not extract UI into `_buildXxx()` or other widget-returning methods. A meaningful extracted UI section is a public `XxxWidget` class in the owning feature's `presentation/widgets/` or `presentation/components/` folder and is exported through its barrel. Private widget classes (`_XxxWidget`) are forbidden."""
UI_EXTRACT_NEW = """- Do not extract UI into `_buildXxx()` or other widget-returning methods. A meaningful extracted UI section is a public `XxxWidget` class in the owning feature's widget folder (from the conventions file, else the profile default) and is exported through its barrel. Private widget classes (`_XxxWidget`) are forbidden."""

STATE_OLD = """- provide a shared `PaginationFAB` back-to-top action after the screen-defined scroll threshold, driven by a screen-owned `ScrollController` and `ValueNotifier<bool>`; dispose both with the screen lifecycle
- if another floating action already exists, preserve its primary purpose and compose/position `PaginationFAB` within that existing FAB layout rather than replacing it"""
STATE_NEW = """- provide a shared back-to-top action after the screen-defined scroll threshold, driven by a screen-owned `ScrollController` and `ValueNotifier<bool>`; dispose both with the screen lifecycle. Resolve the widget from the `pagination_fab` role; if the role is `none observed`, skip the back-to-top affordance instead of creating one
- if another floating action already exists, preserve its primary purpose and compose/position the back-to-top action within that existing FAB layout rather than replacing it"""

GO_ROUTER_OLD = "- Shared app widgets use `core/widgets/app_<name>.dart`; one-screen widgets never move to `core` without real cross-feature reuse."
GO_ROUTER_NEW = "- Shared app widgets use `core/widgets/app_<name>.dart` (default when `docs/dynamic-rules/PROJECT-CONVENTIONS.md` is absent); one-screen widgets never move to `core` without real cross-feature reuse."

V5_OLD = "Each route-domain module remains near `lib/routes/`; do not introduce v6 feature `config/` modules or v7 `createModule` files."
V5_NEW = V5_OLD + "\nShared-widget location and component names resolve from `docs/dynamic-rules/PROJECT-CONVENTIONS.md` when present; this structure is the default otherwise."

V6_OLD = "Every folder keeps a barrel named after the folder; import through barrels, never deep-file paths.\n"
V6_NEW = V6_OLD + "Shared-widget location and component names resolve from `docs/dynamic-rules/PROJECT-CONVENTIONS.md` when present; the `core/` layout above is the default otherwise.\n"

V7_OLD = "Keep a feature's path constants and module declaration together; do not introduce legacy `lib/routes/` module lists."
V7_NEW = V7_OLD + "\nShared-widget location and component names resolve from `docs/dynamic-rules/PROJECT-CONVENTIONS.md` when present; this structure is the default otherwise."

AGENTS_OLD = "5. Read only the matching universal rule under `rules/`; do not preload unrelated profile or universal rules.\n"
AGENTS_NEW = AGENTS_OLD + "6. Read `docs/dynamic-rules/PROJECT-CONVENTIONS.md` if present; skip if absent. Resolve shared widgets, helpers, and layout from it before falling back to the profile default.\n"

README_INTRO_OLD = "After that, ask the agent for the work. It reads `PROJECT_PROFILE.md` and loads only the rules for the concerns your task actually touches.\n"
README_INTRO_NEW = README_INTRO_OLD + """On the first task that needs a shared widget or helper, the agent scans the
project once and writes `docs/dynamic-rules/PROJECT-CONVENTIONS.md`, recording
the real widget folder, component names, formatters, and layout. A fresh
project with nothing to scan gets `mode: fresh` and uses the profile defaults
with no questions. Later sessions read the file and never rescan.
"""

README_INSTALLED_OLD = "docs/dynamic-rules/rules/*.md\ndocs/RULES-MAP.md\n```"
README_INSTALLED_NEW = "docs/dynamic-rules/rules/*.md\ndocs/RULES-MAP.md\ndocs/dynamic-rules/PROJECT-CONVENTIONS.md   (created by the agent, not the CLI)\n```"

WF_ANCHOR = """            exit 1
          fi

  profile-smoke-test:"""

WF_NEW = """            exit 1
          fi

      - name: Guard universal rules against project-local symbols
        run: |
          if grep -nE 'AppButton|AppText|AppTextField|AppSvg|AppSpacing|AppDimensions|AppDateFormatter|PaginationFAB|core/widgets|presentation/widgets' rules/*.md; then
            echo "::error::rules/*.md must resolve symbols and paths via docs/dynamic-rules/PROJECT-CONVENTIONS.md, not hardcode project-local names."
            exit 1
          fi

      - name: Verify conventions template shape
        run: |
          tpl=templates/PROJECT-CONVENTIONS.md
          for role in text button text_field svg feedback date_formatter spacing pagination_fab; do
            grep -q "| $role |" "$tpl" || { echo "::error::template missing role $role"; exit 1; }
          done
          grep -q "## Unresolved" "$tpl" || { echo "::error::template missing ## Unresolved"; exit 1; }
          grep -q "mode:" "$tpl" || { echo "::error::template missing mode comment"; exit 1; }

  profile-smoke-test:"""

REPLACEMENTS = [
    ("rules/CORE.md", CORE_OLD, CORE_NEW),
    ("rules/UI.md", UI_CORE_OLD, UI_CORE_NEW),
    ("rules/UI.md", UI_DATE_OLD, UI_DATE_NEW),
    ("rules/UI.md", UI_FAB_OLD, UI_FAB_NEW),
    ("rules/UI.md", UI_EXTRACT_OLD, UI_EXTRACT_NEW),
    ("rules/STATE-MANAGEMENT.md", STATE_OLD, STATE_NEW),
    ("profiles/go_router_get_it/FOLDER-STRUCTURE.md", GO_ROUTER_OLD, GO_ROUTER_NEW),
    ("profiles/flutter_modular_v5/FOLDER-STRUCTURE.md", V5_OLD, V5_NEW),
    ("profiles/flutter_modular_v6/FOLDER-STRUCTURE.md", V6_OLD, V6_NEW),
    ("profiles/flutter_modular_v7/FOLDER-STRUCTURE.md", V7_OLD, V7_NEW),
    ("AGENTS.md", AGENTS_OLD, AGENTS_NEW),
    ("README.md", README_INTRO_OLD, README_INTRO_NEW),
    ("README.md", README_INSTALLED_OLD, README_INSTALLED_NEW),
    (".github/workflows/validate-ruleset.yml", WF_ANCHOR, WF_NEW),
]

CREATE = [("templates/PROJECT-CONVENTIONS.md", TEMPLATE)]

apply_mode = "--apply" in sys.argv
failed = False

for rel, content in CREATE:
    p = ROOT / rel
    if p.exists():
        print(f"SKIP exists: {rel}")
    else:
        if apply_mode:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
        print(f"{'WROTE' if apply_mode else 'CREATE'}: {rel}")

for rel, old, new in REPLACEMENTS:
    p = ROOT / rel
    text = p.read_text()
    n = text.count(old)
    if n != 1:
        print(f"MISSING ({n}x): {rel}")
        failed = True
        continue
    if apply_mode:
        p.write_text(text.replace(old, new))
    print(f"{'WROTE' if apply_mode else 'OK'}: {rel}")

print("DRY-RUN only" if not apply_mode else "APPLIED")
sys.exit(1 if failed else 0)
