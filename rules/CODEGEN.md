# Codegen

Load only when generated artifacts, routes, DI registrations, models, assets, or localization generation are affected.

## Commands

Analyze before completion:

```bash
flutter analyze
```

Codegen always cleans first:

```bash
dart run build_runner clean
dart run build_runner build --delete-conflicting-outputs
```

Watch mode:

```bash
dart run build_runner clean
dart run build_runner watch --delete-conflicting-outputs
```

Run after changes to Freezed/json_serializable, Injectable registration, typed GoRouter routes, or project asset generation.

Localization generation (TEMPLATE-PROJECT: keep only commands used by the project):

```bash
dart run easy_localization:generate -S assets/translations -O lib/translations
dart run easy_localization:generate -S assets/translations -O lib/translations -o locale_keys.g.dart -f keys
```

Testing command policy is in `TESTING.md`: exactly one test file per invocation.

## Startup order

TEMPLATE-PROJECT default:

```text
dotenv
→ EasyLocalization
→ async/preResolve storage
→ configureDependencies()
→ observers
→ runApp
```

Adjust only to documented project requirements.

## Generated files

Never manually edit generated output, including:

```text
*.freezed.dart
*.g.dart
*.gr.dart
injection.config.dart
locale_keys.g.dart
assets.gen.dart
```

Fix source/configuration and regenerate.
