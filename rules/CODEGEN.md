# Code Generation

- Never manually edit generated artifacts.
- When changing Freezed, JSON serialization, DI, generated routes, assets, or localization, run the project-required generation command before verification.
- Keep source declarations and generated references in sync; do not commit stale generated output.
- For `go_router_builder`, keep route declarations, their matching `part '<source>.g.dart';`, and generated typed-route helpers together. Add `build_runner` and `go_router_builder` as dev dependencies, then run `dart run build_runner build --delete-conflicting-outputs` after route changes.
- For `injectable`, keep `injectable_generator` and `build_runner` in dev dependencies; run the same project-approved generator after registration changes.
