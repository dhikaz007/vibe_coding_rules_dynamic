# Profile Compatibility

| Profile | Required routing and DI package |
|---|---|
| `go_router_get_it` | `go_router`, `go_router_builder`, `get_it`, `injectable` |
| `flutter_modular_v5` | `flutter_modular: ^5.0.3` |
| `flutter_modular_v6` | `flutter_modular: ^6.4.1` |
| `flutter_modular_v7` | `flutter_modular: ^7.1.0` |

Use `agents dependency plan` before adding packages. Do not upgrade a Modular major version by changing only `pubspec.yaml`; select the matching ruleset profile and migrate source code separately.

## SDK and codegen compatibility

- Before selecting or upgrading a profile, verify the consuming project's `environment.sdk`, Flutter SDK, and resolved package constraints with `flutter pub get`; do not infer compatibility from the profile name alone.
- `go_router_get_it` requires Dart `>=3.3.0 <4.0.0`. Its route and DI generators are dev dependencies: `build_runner`, `go_router_builder`, and `injectable_generator`.
- Flutter Modular v5/v6/v7 retain `dart: project-verified` because their supported SDK range must be read from the exact package version resolved by the consuming project's lockfile before changing a legacy project.
