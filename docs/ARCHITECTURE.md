# EdgeOps Console Architecture

## 1. System Overview

EdgeOps Console is a three-tier full-stack application composed of a React client, FastAPI service and persistent relational database.

```text
Browser
  |
  | HTTP / JSON
  v
Nginx / Vite proxy
  |
  v
FastAPI REST API
  |
  v
SQLite (local) or PostgreSQL (Docker)
```

The application is intentionally designed so the same API contract works with a zero-configuration local database and a production-like PostgreSQL deployment.

## 2. Frontend Architecture

The React client follows a feature-oriented structure. Domain-specific code is grouped into dashboard, infrastructure, traffic and incident modules, while reusable presentation primitives remain under `components/`.

TanStack Query owns remote server state, including loading, error, caching, mutation and invalidation behavior. Zustand is intentionally limited to lightweight local interface state such as sidebar behavior.

The Fetch API is wrapped by a centralized client that provides JSON headers, request timeout handling, AbortController cancellation and normalized errors.

A native `<status-badge>` Custom Element demonstrates interoperability between React and standards-based Web Components.

## 3. Interactive Topbar

The topbar is application functionality rather than static decoration.

### Global Search

Search input is debounced before querying `GET /api/search`. The backend searches edge nodes, incidents and regions. Search results include a destination route so selecting an item navigates to the relevant module.

### Notifications

The notification menu uses persistent records from the database. Unread state is reflected by the notification indicator and can be cleared through `PATCH /api/notifications/read-all`.

### Profile

The profile control loads current profile metadata from `GET /api/profile` and exposes it through an accessible interactive panel.

## 4. Backend Architecture

FastAPI exposes typed REST endpoints for operational metrics, infrastructure inventory, traffic analytics, incidents, search, notifications and profile data.

Pydantic validates incident creation payloads. API routes delegate persistence work to `app/db.py` rather than directly manipulating in-memory Python collections.

The database layer supports two runtime modes:

- **SQLite** — default for local development
- **PostgreSQL** — automatically configured by Docker Compose

Schema initialization is idempotent and seed data is inserted only when the relevant tables are empty.

## 5. Persistence

The relational model includes:

- `regions`
- `edge_nodes`
- `incidents`
- `incident_audit`
- `notifications`

Incident creation writes a persistent incident plus a corresponding audit entry. Incident resolution updates the record and appends another audit event.

Because state is stored in the database, newly created incidents and notification read state survive API restarts.

The canonical relational schema is documented in `database/schema.sql`.

## 6. Incident Audit Trail

Every important incident lifecycle transition writes an append-only audit entry containing:

- Incident ID
- Action
- Actor
- Details
- Timestamp

The frontend exposes this history through the Incident Center using `GET /api/incidents/{id}/audit`.

This is deliberately separate from the mutable incident record so operational history remains available after status changes.

## 7. HTTP & Browser Engineering

The application demonstrates:

- JSON content negotiation
- RESTful GET, POST and PATCH operations
- HTTP status codes including 200, 201, 204, 400, 404 and validation responses
- Request cancellation through AbortController
- Request timeout behavior
- CORS for local development
- Vite development proxying
- Nginx API reverse proxying
- SPA history fallback through `try_files`
- Native browser Custom Elements

## 8. Container Architecture

`docker compose up --build` starts three services:

```text
web (Nginx + React build)
        |
        v
api (FastAPI)
        |
        v
db (PostgreSQL 16)
```

The database service uses a named Docker volume for durable PostgreSQL storage. Health checks ensure PostgreSQL is ready before the API starts and the API is healthy before the web service is treated as ready.

## 9. Quality & CI

GitHub Actions validates both application layers.

Frontend CI runs:

- npm dependency installation
- ESLint
- Vitest
- Vite production build

Backend CI runs:

- Python dependency installation
- Pytest with `PYTHONPATH=.`

Backend tests cover the overview contract, incident lifecycle, persistent audit history, search, notifications and profile data.

## 10. Security & Production Evolution

The repository now includes persistent database storage, PostgreSQL support, a persistent incident audit trail, interactive search and notifications, container deployment and CI.

For a larger production environment, the next architectural enhancements would typically include:

- OAuth 2.0 / OpenID Connect authentication
- Role-based authorization
- Centralized identity and SSO
- OpenTelemetry distributed tracing
- Prometheus metrics
- Grafana visualization
- WebSocket or Server-Sent Events for real-time telemetry
- Distributed API rate limiting
- Secrets management
- Centralized structured logging
- End-to-end browser testing

These items are documented as future enhancements and are not claimed as implemented in the current project.
