# Routing: Flutter Modular

- Use `flutter_modular` route declarations, modules, guards, and navigation patterns already established by the application.
- Route and module ownership remains in the feature/app routing structure; do not add `go_router` routes or generated typed-route code.
- A destination mutation returns its result through the established Modular flow; the originating screen refreshes its own Cubit/state.
- Never navigate directly from a Cubit.
