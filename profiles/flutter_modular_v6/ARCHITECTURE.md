# Architecture: Flutter Modular v6

Use `class XxxModule extends Module`. App and feature modules define routes with `routes(r)`, import dependencies through `List<Module> get imports`, and expose feature dependencies through the appropriate bind module. Preserve the existing `feature/<name>/config`, `cubit`, `domain`, and `screens` boundaries.
