# State Management

- Cubit owns state transitions; UI side effects belong in a listener and must fire once per transition.
- Decide Cubit lifecycle from the complete navigation flow; the selected profile defines registration and provider patterns.
- After `await`, verify `context.mounted` before context-dependent work.
- Prefer `ValueNotifier<T>` and `ValueListenableBuilder<T>` for simple screen-local state; dispose screen-owned notifiers/controllers.

## Pagination

- Use `infinite_scroll_pagination` with Cubit. Prevent duplicate next-page fetches; append new pages; reset to page 1 for refresh/filter changes; retain content during refresh and next-page loading.
- Every paginated view must set `newPageProgressIndicatorBuilder`, `firstPageProgressIndicatorBuilder`, `firstPageErrorIndicatorBuilder`, and `noItemsFoundIndicatorBuilder`; never use the package defaults for those states.
- Every paginated list uses `PagedListView.separated`, and it must provide all four required indicator builders.
- Every aligned paginated grid uses `PagedAlignedGridView.count`, and it must provide all four required indicator builders. Do not use `.separated` for `PagedAlignedGridView.count`.
- Every paginated list follows the project's pull-to-refresh convention.
- Provide shared `PaginationFAB` after the screen-defined scroll threshold, driven by a screen-owned `ScrollController` and `ValueNotifier<bool>`. Its action animates to offset `0`; dispose both objects with the screen lifecycle. Do not replace another existing FAB—compose it with the existing floating action layout.
