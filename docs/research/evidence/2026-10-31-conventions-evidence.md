# Conventions Evidence: Four Flutter Projects

Date: 2026-10-31
Purpose: measure how far `rules/` and `profiles/` assumptions match real
projects, and record what the conventions layer must store.

## Projects scanned

| Project | Path | Profile deps | i18n |
|---|---|---|---|
| dms_mobile | `Zegen/Mobile Dev Active/dms_mobile` | go_router 18, get_it 9, injectable 3 | easy_localization |
| LMS-ECampus | `Zegen/Mobile Dev Active/LMS-ECampus` | flutter_modular 6.4.1 | easy_localization |
| lms_mobile_revamp | `Zegen/Mobile Dev Active/lms_mobile_revamp` | flutter_modular 6.4.1 | easy_localization |
| fire_todo | `Andhika Development/My Project/fire_todo` | flutter_modular 7.1.0 | none found (flutter_gen only) |

`dms_mobile` is the project the current rules were written against. Its layout
matches `rules/` and `profiles/go_router_get_it/` almost one to one:
`lib/core/widgets/app_*.dart`, `AppText`, `AppSvg`, `PaginationFAB`,
`lib/core/utils/app_date_formatter.dart`, `lib/core/theme/app_theme.dart`,
`feature/<x>/presentation/{widgets,components}`, barrel `widgets.dart`.

## Role matrix

Verified by grep on `class`/`extension` declarations. `?` means not verified in
this pass, not absent.

| Role | dms (go_router) | LMS-ECampus (mod v6) | revamp (mod v6) | fire_todo (mod v7) |
|---|---|---|---|---|
| text | `AppText` | `CustomText` | `CustomText` | `TextApp` |
| button primary | `AppPrimaryButton` | `CustomButton` | `ButtonPrimary` | `ButtonPrimary` |
| button secondary | `AppSecondaryButton` | same `CustomButton` | `ButtonSecondary` | `ButtonSecondary` |
| text field | `AppInputField` | `CustomTextField` | `InputFormPrimary` | `TextFormFieldApp` |
| svg | `AppSvg` | `SvgWidget` | `SvgWidget` | `SvgApp` |
| feedback | `AppFlushbar` | `AppNotifier` (private `_showFlushbar`) | ? | `SnackbarApp` |
| dialog | `AppDialog` | `BaseAlertDialog`, `BaseGeneralDialog` | ? | ? |
| bottom sheet | ? | `BaseBottomSheet` | `RangeDateBottomSheet` | ? |
| pagination FAB | `PaginationFAB` | none | `PaginationFAB` | none |
| loading overlay | `AppLoaderOverlay` | `LoadingOverlay` | `DefaultLoadingOverlay` | `LoadingApp` |
| date formatter | `AppDateFormatter` (class) | `DateTimeStringX` (ext on String) | ? | `DateExtension` (ext on DateTime) |
| theme | `core/theme/app_theme.dart` | inline `main.dart:73` | ? | ? |
| spacing token | `AppSpacer` | none observed | ? | ? |
| colors | `core/colors/` | `core/constant/colors.dart` | `constants/` | ? |
| barrel | `core/widgets/widgets.dart` | none for `shared`; `extensions.dart` is a `part` barrel | ? | ? |
| feature layout | `presentation/{widgets,components}` + `data`/`domain` | `screens`, `config`, `cubit`, `domain` | `screens/components` | `presentation`, `module`, `data`, `domain` |
| shared widget dir | `lib/core/widgets` | `lib/core/shared` | `lib/shared` | `lib/core/widgets` |

## What this proves

1. Only the shared-widget directory and the button roles agree in two of four
   projects. Everything else is rename-level divergence.
2. Naming families do not overlap: `App*` (dms), `Custom*` (LMS, revamp),
   suffix form `*App` (fire_todo). A rule that names a symbol is wrong in at
   least three of the four projects.
3. A role can legitimately have several symbols in one project
   (`ButtonPrimary` + `ButtonSecondary` + `ButtonCustom` + `ButtonCustomAlt` in
   revamp; `CustomButton` serves both button roles in LMS-ECampus). A single
   `symbol` field is not enough; a role needs an ordered set.
4. The same role is a different kind across projects: date formatting is a
   class in dms, an extension on `String` in LMS-ECampus, an extension on
   `DateTime` in fire_todo. `kind` is mandatory.
5. Feature layout diverges: `presentation/` in dms and fire_todo, `screens/` in
   both LMS projects. This is a profile-default override, not a rule violation.
6. Localization is not universal: fire_todo has no localization package, so the
   `LocaleKeys` requirement from `rules/UI.md:8` would be a false rule there.
   Absence must be representable.
7. The conventions layer is profile-independent. Routing and DI stay with the
   profile; roles and paths live in one file shared by every profile.

## Design deltas required

D1. Role map is set-valued:

```
## Role map
| role | kind | default | alternates | path |
| text | class | CustomText | - | lib/core/shared/text.dart |
| button_primary | class | ButtonPrimary | ButtonCustom, ButtonCustomAlt | lib/shared/button_primary.dart |
| date_formatter | extension | DateTimeStringX | - | lib/core/extensions/string_datetime.dart |
| spacing | none | none observed | - | - |
```

D2. `kind` values: `class`, `extension`, `static-class`, `function`,
`none`. `static-class` covers `AppNotifier` and `SnackbarApp`.

D3. `source` per entry: `observed`, `profile-default`, `none`. A fresh project
writes no role entries and is marked `mode: fresh`; the agent then uses profile
defaults and never asks. This is the no-adaptation path.

D4. Ambiguity rule changes. Multiple symbols for one role are normal, not
ambiguous. Ambiguity is now: two candidates for the same role and same
specificity, with no usage evidence. Resolution order: usage count
(`grep -c`), then nearest comparable screen, then ask.

D5. Rules rewrite to roles only. `rules/UI.md` says "text widget role", never
`AppText`. CI denylist holds the project-local identifiers currently named in
`rules/`: `AppButton`, `AppText`, `AppTextField`, `AppSvg`, `AppSpacing`,
`AppDimensions`, `AppDateFormatter`, `PaginationFAB`.

D6. Scan by shape, not name:

- widget role: `class ... extends StatelessWidget|StatefulWidget` inside the
  shared widget dir, classified by the Flutter primitive it wraps
  (`Text`, `TextFormField`, `SvgPicture`, `ElevatedButton`/`OutlinedButton`).
- date formatter: `DateFormat(` inside a `class` or `extension`.
- feedback: `Flushbar`, `showSnackBar`, `showDialog` wrapper calls.
- theme: file containing `ThemeData`, or the `theme:` argument in `main.dart`.
- tokens: class or const set of doubles in theme/constants.
- barrel: a file whose body is only `export`/`part` lines.

D7. Fresh-project path: if the scan finds no shared widget dir and no role
candidates, write `mode: fresh` and stop. No questions, no invented symbols,
profile defaults apply.

## Open items

- Feedback, theme, and spacing in `lms_mobile_revamp` and `fire_todo` were not
  verified in this pass.
- Whether `rules/STATE-MANAGEMENT.md` naming (`withBloc`, `modularBloc`) holds
  for fire_todo's v7 module layout was not verified.
