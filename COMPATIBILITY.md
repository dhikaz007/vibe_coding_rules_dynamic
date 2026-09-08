# Profile Compatibility

| Profile | Required routing and DI package |
|---|---|
| `go_router_get_it` | `go_router`, `go_router_builder`, `get_it`, `injectable` |
| `flutter_modular_v5` | `flutter_modular: ^5.0.3` |
| `flutter_modular_v6` | `flutter_modular: ^6.4.1` |
| `flutter_modular_v7` | `flutter_modular: ^7.1.0` |

Use `agents dependency plan` before adding packages. Do not upgrade a Modular major version by changing only `pubspec.yaml`; select the matching ruleset profile and migrate source code separately.
