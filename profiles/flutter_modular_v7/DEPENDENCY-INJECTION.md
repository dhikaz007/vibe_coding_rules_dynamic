# Dependency Injection: Flutter Modular v7

Register dependencies with `..add`, `..addSingleton`, and `..addLazySingleton` in `createModule`. Resolve with `inject<T>()`. Page-owned Cubits are registered with the established v7 lifetime and provided with `BlocProvider(create:)`; shared instances are reused only when their navigation lifecycle requires it.
