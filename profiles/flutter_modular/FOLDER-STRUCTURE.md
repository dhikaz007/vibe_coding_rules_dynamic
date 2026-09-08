# Folder Structure: Flutter Modular

- Follow the existing Modular feature structure: feature config/module files, Cubit, domain, screens, and screen components.
- Shared cross-feature UI belongs in `shared/` only after real cross-feature reuse; screen-specific UI remains in its feature.
- Use the application's existing `services/`, `routes/`, `helpers/`, `storage/`, and generated-reference locations; do not create a parallel `core/` tree unless the project already uses it.
