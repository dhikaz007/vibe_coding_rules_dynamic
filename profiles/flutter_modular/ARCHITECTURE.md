# Architecture: Flutter Modular

Use the project's established Flutter Modular feature shape, for example:

```text
feature/<feature>/
├── config/
├── cubit/
├── domain/
└── screens/
    └── component/
```

Use the application's existing `services/`, `shared/`, routes, and storage boundaries. Presentation flows through Cubit → repository → approved service/transport layer. Do not introduce `get_it`, `injectable`, or `go_router` into this profile.
