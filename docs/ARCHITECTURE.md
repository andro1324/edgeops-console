# EdgeOps Architecture

## Frontend
The React client is organized by feature, with shared presentation components separated from HTTP access and global UI state. TanStack Query owns server state, caching and refresh behavior; Zustand is intentionally limited to local UI state. Native `fetch` is wrapped by a timeout-aware HTTP client that normalizes non-2xx responses.

A native Web Component (`<status-badge>`) demonstrates standards-based custom elements interoperability with React. The dashboard uses responsive, semantic layouts and accessible controls. CSS uses design tokens, progressive responsive breakpoints and no framework-specific utility dependency.

## Backend
FastAPI exposes a compact demo API with typed validation through Pydantic. Endpoints model operational overview, infrastructure inventory, delivery analytics and incident lifecycle actions. This backend exists to make the frontend genuinely dynamic rather than a collection of static mocks.

## HTTP and browser engineering
- JSON content negotiation and explicit `Accept`/`Content-Type` headers.
- Correct status codes: 200, 201, 204, 404 and validation errors.
- Request cancellation via `AbortController`.
- CORS configured for local development.
- Nginx reverse proxy example with HTTP/1.1 forwarding and security headers.
- SPA history fallback using `try_files`.

## Quality
Frontend lint/build and backend tests run in GitHub Actions. Backend tests cover a read contract and an incident create/resolve lifecycle. Components expose semantic labels and the responsive sidebar is keyboard-addressable.

## Production evolution
For a real deployment, we need to replace in-memory demo data with PostgreSQL using the included relational schema, add OAuth/OIDC authentication, role-based authorization, OpenTelemetry traces, Prometheus metrics, a WebSocket/SSE event channel, rate limiting and a persistent incident audit trail.
