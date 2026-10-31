# Project Conventions Discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `rules/` resolve project-local symbols and paths through a per-project `PROJECT-CONVENTIONS.md` instead of hardcoding `core/widgets`, `AppButton`, and friends.

**Architecture:** A scan-once, self-healing conventions file sits at `docs/dynamic-rules/PROJECT-CONVENTIONS.md`. Rules reference fixed role names (`text`, `button`, `text_field`, `svg`, `spacing`, `feedback`, `date_formatter`, `pagination_fab`), never project symbol names. Fresh projects short-circuit to `mode: fresh` and use profile defaults.

**Tech Stack:** Markdown rule set. No code. Verification is `agents ruleset validate` plus grep guards in CI.

## Global Constraints

- Do not commit or push. Repo `AGENTS.md` forbids commits without an explicit request. Every "commit" step below runs only if the user explicitly asks.
- Review `README.md` for GitHub-facing impact in the same change as any user-facing rule/profile/wiring change.
- Never edit generated files, hardcode secrets, or rename symbols that are not part of this plan.
- Role names are the fixed vocabulary: `text`, `button`, `text_field`, `svg`, `spacing`, `feedback`, `date_formatter`, `pagination_fab`. No other roles.
- `kind` ∈ {`class`, `static-class`, `extension`, `function`, `none`}; `source` ∈ {`observed`, `profile-default`, `none`}.

---

### Task 1: Create the conventions template

**Files:**
- Create: `templates/PROJECT-CONVENTIONS.md`

**Interfaces:**
- Produces: the file every consuming project's agent copies or regenerates. Later tasks reference its section names verbatim.

- [ ] **Step 1: Write the template**

```md
# Project conventions (observed)
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
```

- [ ] **Step 2: Verify the shape**

Run: `grep -c '^|' templates/PROJECT-CONVENTIONS.md`
Expected: `8` (eight role rows).

Run: `grep -nE '## Unresolved|mode: fresh' templates/PROJECT-CONVENTIONS.md`
Expected: both lines present.

- [ ] **Step 3: Commit (only if requested)**

```bash
git add templates/PROJECT-CONVENTIONS.md
git commit -m "feat: add PROJECT-CONVENTIONS.md template"
```

---

### Task 2: Rewrite CORE.md convention resolution

**Files:**
- Modify: `rules/CORE.md:10-13`

**Interfaces:**
- Produces: the authority order and role vocabulary every other rule defers to.

- [ ] **Step 1: Replace the "Project-specific convention resolution" section**

Old:

```md
## Project-specific convention resolution

- “Existing”, “established”, “approved”, and “project convention” always mean the nearest comparable implementation first, then the consuming project's documented rule.
- If neither source defines the required convention, do not invent one: report the gap and ask for direction before changing architecture, routing, DI lifetime, transport, storage, or security behavior.
```

New:

```md
## Project-specific convention resolution

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
```

- [ ] **Step 2: Verify no leftover path literal**

Run: `grep -n 'core/widgets\|AppButton\|AppText' rules/CORE.md`
Expected: no output.

- [ ] **Step 3: Commit (only if requested)**

```bash
git add rules/CORE.md
git commit -m "feat: CORE.md resolves conventions through PROJECT-CONVENTIONS.md"
```

---

### Task 3: Rewrite UI.md role references

**Files:**
- Modify: `rules/UI.md:13-32`, `rules/UI.md:37`, `rules/UI.md:38`, `rules/UI.md:40`

**Interfaces:**
- Consumes: role vocabulary from `CORE.md` (Task 2).
- Produces: `UI.md` that names no project-local symbol.

- [ ] **Step 1: Replace the "Core-widget first" section (lines 13-32)**

New:

```md
## Core-widget first

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
```

- [ ] **Step 2: Replace the date/time line (line 37)**

Old:

```md
- Date/time: TEMPLATE-PROJECT `<DEFAULT_TIMEZONE>`, `<DATE_FORMAT>`, `<DEFAULT_LOCALE_CODE>` through shared `AppDateFormatter`; do not instantiate DateFormat repeatedly in features.
```

New:

```md
- Date/time: TEMPLATE-PROJECT `<DEFAULT_TIMEZONE>`, `<DATE_FORMAT>`, `<DEFAULT_LOCALE_CODE>` through the `date_formatter` role; do not instantiate `DateFormat` repeatedly in features.
```

- [ ] **Step 3: Replace the pagination FAB line (line 38)**

Old:

```md
- Paginated-list back-to-top uses the shared `PaginationFAB`. When it shares a screen with other floating actions, preserve the existing primary action and follow the screen's established FAB hierarchy, spacing, and layout.
```

New:

```md
- Paginated-list back-to-top uses the `pagination_fab` role; if that role is `none observed`, skip the back-to-top affordance. When it shares a screen with other floating actions, preserve the existing primary action and follow the screen's established FAB hierarchy, spacing, and layout.
```

- [ ] **Step 4: Replace the widget-extraction line (line 40)**

Old:

```md
- Do not extract UI into `_buildXxx()` or other widget-returning methods. A meaningful extracted UI section is a public `XxxWidget` class in the owning feature's `presentation/widgets/` or `presentation/components/` folder and is exported through its barrel. Private widget classes (`_XxxWidget`) are forbidden.
```

New:

```md
- Do not extract UI into `_buildXxx()` or other widget-returning methods. A meaningful extracted UI section is a public `XxxWidget` class in the owning feature's widget folder (from the conventions file, else the profile default) and is exported through its barrel. Private widget classes (`_XxxWidget`) are forbidden.
```

- [ ] **Step 5: Verify no leftover symbols**

Run: `grep -nE 'AppButton|AppText|AppTextField|AppSvg|AppSpacing|AppDimensions|AppDateFormatter|PaginationFAB|core/widgets|presentation/widgets' rules/UI.md`
Expected: no output.

- [ ] **Step 6: Commit (only if requested)**

```bash
git add rules/UI.md
git commit -m "feat: UI.md resolves components through role map"
```

---

### Task 4: Rewrite STATE-MANAGEMENT.md pagination FAB

**Files:**
- Modify: `rules/STATE-MANAGEMENT.md:124-125`

**Interfaces:**
- Consumes: `pagination_fab` role and its none branch from `CORE.md`.

- [ ] **Step 1: Replace lines 124-125**

Old:

```md
- provide a shared `PaginationFAB` back-to-top action after the screen-defined scroll threshold, driven by a screen-owned `ScrollController` and `ValueNotifier<bool>`; dispose both with the screen lifecycle
- if another floating action already exists, preserve its primary purpose and compose/position `PaginationFAB` within that existing FAB layout rather than replacing it
```

New:

```md
- provide a shared back-to-top action after the screen-defined scroll threshold, driven by a screen-owned `ScrollController` and `ValueNotifier<bool>`; dispose both with the screen lifecycle. Resolve the widget from the `pagination_fab` role; if the role is `none observed`, skip the back-to-top affordance instead of creating one
- if another floating action already exists, preserve its primary purpose and compose/position the back-to-top action within that existing FAB layout rather than replacing it
```

- [ ] **Step 2: Verify**

Run: `grep -n 'PaginationFAB' rules/STATE-MANAGEMENT.md`
Expected: no output.

- [ ] **Step 3: Commit (only if requested)**

```bash
git add rules/STATE-MANAGEMENT.md
git commit -m "feat: STATE-MANAGEMENT resolves back-to-top via pagination_fab role"
```

---

### Task 5: Mark profile folder defaults as overridable

**Files:**
- Modify: `profiles/go_router_get_it/FOLDER-STRUCTURE.md:6`
- Modify: `profiles/flutter_modular_v5/FOLDER-STRUCTURE.md`
- Modify: `profiles/flutter_modular_v6/FOLDER-STRUCTURE.md`
- Modify: `profiles/flutter_modular_v7/FOLDER-STRUCTURE.md`

**Interfaces:**
- Produces: profiles that state the conventions file overrides their widget location/naming.

- [ ] **Step 1: go_router — replace line 6**

Old:

```md
- Shared app widgets use `core/widgets/app_<name>.dart`; one-screen widgets never move to `core` without real cross-feature reuse.
```

New:

```md
- Shared app widgets use `core/widgets/app_<name>.dart` (default when `docs/dynamic-rules/PROJECT-CONVENTIONS.md` is absent); one-screen widgets never move to `core` without real cross-feature reuse.
```

- [ ] **Step 2: modular_v5 — append one line**

Append after line 3:

```md
Shared-widget location and component names resolve from `docs/dynamic-rules/PROJECT-CONVENTIONS.md` when present; this structure is the default otherwise.
```

- [ ] **Step 3: modular_v6 — append one line**

Append after line 18:

```md
Shared-widget location and component names resolve from `docs/dynamic-rules/PROJECT-CONVENTIONS.md` when present; the `core/` layout above is the default otherwise.
```

- [ ] **Step 4: modular_v7 — append one line**

Append after line 3:

```md
Shared-widget location and component names resolve from `docs/dynamic-rules/PROJECT-CONVENTIONS.md` when present; this structure is the default otherwise.
```

- [ ] **Step 5: Verify**

Run: `grep -rn 'PROJECT-CONVENTIONS.md' profiles/`
Expected: four matches (one per profile).

- [ ] **Step 6: Commit (only if requested)**

```bash
git add profiles/
git commit -m "feat: profiles mark widget location as overridable by conventions"
```

---

### Task 6: Wire AGENTS.md to read the conventions file

**Files:**
- Modify: `AGENTS.md` (section "1. Select the profile first", after step 5)

**Interfaces:**
- Produces: the agent reads the conventions file before concern rules.

- [ ] **Step 1: Add step 6**

Append to the numbered list under "1. Select the profile first":

```md
6. Read `docs/dynamic-rules/PROJECT-CONVENTIONS.md` if present; skip if absent. Resolve shared widgets, helpers, and layout from it before falling back to the profile default.
```

- [ ] **Step 2: Verify**

Run: `grep -n 'PROJECT-CONVENTIONS.md' AGENTS.md`
Expected: the step above appears.

- [ ] **Step 3: Commit (only if requested)**

```bash
git add AGENTS.md
git commit -m "feat: AGENTS.md reads PROJECT-CONVENTIONS.md after profile"
```

---

### Task 7: Update README.md

**Files:**
- Modify: `README.md`

**Interfaces:**
- Produces: user-facing docs for the conventions file, fresh mode, and installed files.

- [ ] **Step 1: Add a conventions note to Quick start**

After the "After that, ask the agent for the work..." paragraph (line 42), add:

```md
On the first task that needs a shared widget or helper, the agent scans the
project once and writes `docs/dynamic-rules/PROJECT-CONVENTIONS.md`, recording
the real widget folder, component names, formatters, and layout. A fresh
project with nothing to scan gets `mode: fresh` and uses the profile defaults
with no questions. Later sessions read the file and never rescan.
```

- [ ] **Step 2: Update "What gets installed"**

Add to the code block in "What gets installed" (lines 55-63), after `docs/RULES-MAP.md`:

```text
docs/dynamic-rules/PROJECT-CONVENTIONS.md   (created by the agent, not the CLI)
```

- [ ] **Step 3: Verify**

Run: `grep -n 'PROJECT-CONVENTIONS' README.md`
Expected: two or more matches.

- [ ] **Step 4: Commit (only if requested)**

```bash
git add README.md
git commit -m "docs: document PROJECT-CONVENTIONS.md and fresh mode"
```

---

### Task 8: Add CI guards

**Files:**
- Modify: `.github/workflows/validate-ruleset.yml`

**Interfaces:**
- Consumes: the 8 role names and deny list fixed in the spec.

- [ ] **Step 1: Add the symbol deny guard**

After the "Guard universal rules against stack-specific APIs" step (line 40-45), add:

```yaml
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
```

- [ ] **Step 2: Verify locally**

Run: `grep -nE 'AppButton|AppText|AppTextField|AppSvg|AppSpacing|AppDimensions|AppDateFormatter|PaginationFAB|core/widgets|presentation/widgets' rules/*.md`
Expected: no output (the CI guard must pass against the edited rules).

Run: `bash -n` on a locally copied script is not applicable; instead run the template loop manually:

```bash
for role in text button text_field svg feedback date_formatter spacing pagination_fab; do grep -q "| $role |" templates/PROJECT-CONVENTIONS.md || echo "missing $role"; done
```
Expected: no output.

- [ ] **Step 3: Commit (only if requested)**

```bash
git add .github/workflows/validate-ruleset.yml
git commit -m "ci: deny project-local symbols and verify conventions template"
```

---

### Task 9: End-to-end verification

**Files:**
- None (read-only checks).

- [ ] **Step 1: Run the local grep deny list**

Run: `grep -nE 'AppButton|AppText|AppTextField|AppSvg|AppSpacing|AppDimensions|AppDateFormatter|PaginationFAB|core/widgets|presentation/widgets' rules/*.md`
Expected: no output.

- [ ] **Step 2: Confirm no rule names a role it does not consume**

Run: `grep -rn 'none observed\|role' rules/*.md | sort`
Expected: role references appear only in `CORE.md`, `UI.md`, `STATE-MANAGEMENT.md`.

- [ ] **Step 3: Run the ruleset validator (if the CLI is present)**

Run: `agents ruleset validate vibe-coding-rules`
Expected: exit 0.

- [ ] **Step 4: README review**

Confirm `README.md` mentions the conventions file and fresh mode (repo `AGENTS.md` requires README review on user-facing changes).

- [ ] **Step 5: Stop**

Do not commit unless the user explicitly asks. Report the files changed and the verification output.
