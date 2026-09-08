# Dependency Injection: Flutter Modular v6

Use a dedicated bind `Module` when the feature exposes dependencies. Register with `exportedBinds(Injector i)` and the existing `i.add`/`i.addLazySingleton` lifetime pattern. Compose Bloc ownership with the project's `modularBloc<T>()` and `modularValueBloc<T>()` helpers; do not introduce v5 `Bind` lists or v7 global `inject` conventions.
