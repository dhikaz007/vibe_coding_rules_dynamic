# Dependency Injection: Flutter Modular

- Register dependencies with the application's Modular bind pattern.
- Page-owned Cubits use a fresh bind/provider lifecycle; intentionally reused instances use the established lazy/singleton Modular pattern only when the navigation flow requires it.
- Keep module binds near their feature/application ownership and reuse existing binds.
- Do not add `get_it`/`injectable` registrations or duplicate global state.
