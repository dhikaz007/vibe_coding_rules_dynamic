# Network and API

- Read the consuming project's endpoint mapping and API specification before API integration; never infer paths, methods, fields, headers, pagination, or business behavior.
- Presentation and Cubit do not call transport clients/datasources directly. Keep transport and error mapping behind repository boundaries.
- Reuse the selected profile/project's approved client and response/error conventions; do not introduce a parallel client stack.
- Keep API error details safe for users and logs. Map failures before they reach presentation.
