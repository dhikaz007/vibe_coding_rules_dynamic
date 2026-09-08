# Testing

- Test behavior at the lowest useful level: unit, Cubit/state, widget, then integration.
- Pagination tests cover first page, next page, last page, failure, refresh/filter reset, and preserved content.
- Test state transitions and observable outcomes, not widget internals.
- Run focused tests for changed behavior and `flutter analyze` before completion.
