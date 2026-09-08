# UI

- Reuse the consuming project's shared/core widgets, tokens, localization, and generated assets before creating a new component.
- All user-facing text uses the project's localization system and generated keys; do not hardcode user-facing strings.
- Use the project date formatter and theme values; support system text scaling and safe-area ownership.
- Use semantic button widgets for button-like actions, Flutter `TabBar`/`TabBarView` for tabs, and generated SVG assets before icon-library fallbacks.
- Every function declares an explicit return type. Use `void` for actions without a result. For several related return values, use a typed record, for example `(String statusText, Color backgroundColor, Color textColor) getStatus()`.
- Do not extract UI into `_buildXxx()` or other widget-returning methods. A meaningful extracted section is a public `XxxWidget` in the owning feature's widget/component folder and is exported through its barrel.
- Private widget classes such as `_XxxWidget extends StatelessWidget` or `StatefulWidget` are forbidden.
- Keep page-specific UI inline in the screen by default.
- Extract a public `XxxWidget` only when the section is reused, independently stateful, materially improves readability, or is large enough to obscure the screen flow.
- Do not extract simple layout wrappers, one-off `Padding`, `Row`, `Column`, `PreferredSize`, `InputDecoration`, list-item callbacks, or short inline builders merely to reduce line count.
- Prefer one screen file while its visual flow remains readable.
- Every Dart source folder has a barrel file with no exception, even when it contains only one Dart file. Name it after the folder, import public types through it, and export every public file in the same change.
- Paginated-list back-to-top uses the shared `PaginationFAB`. When other floating actions exist, preserve their primary action and compose the FAB layout, hierarchy, and spacing to match the screen.
