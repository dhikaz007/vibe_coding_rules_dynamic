# Network and API

- Read the consuming project's endpoint mapping and API specification before API integration; never infer paths, methods, fields, headers, pagination, or business behavior.
- Presentation and Cubit do not call transport clients/datasources directly. Keep transport and error mapping behind repository boundaries.
- Reuse the client and response/error convention from the nearest comparable feature; if it is not documented or observable, ask before introducing a client or error-mapping pattern. Do not introduce a parallel client stack.
- Keep API error details safe for users and logs. Map failures before they reach presentation.
