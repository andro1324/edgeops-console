# EdgeOps Console Architecture

## 1. Overview

EdgeOps Console is a full-stack operations dashboard built with a React frontend, a FastAPI REST API, and a relational database. It provides a demo environment for viewing edge infrastructure, traffic summaries, incidents, notifications, and system metrics.

```text
Browser
  |
  | HTTP / JSON
  v
Nginx (container deployment) or Vite proxy (local development)
  |
  v
FastAPI REST API
  |
  v
SQLite (local development) or PostgreSQL (Docker deployment)
```

The project supports a lightweight local setup and a Docker Compose setup using PostgreSQL. Some infrastructure and traffic values are seeded demonstration data; they should not be interpreted as live fleet telemetry.

## 2. Frontend

The frontend is built with React and organized around application features such as the dashboard, infrastructure, traffic, and incidents. Shared UI elements live in reusable components.

- **TanStack Query** manages remote server state, including loading, errors, caching, mutations, and query invalidation.
- **Zustand** is used for lightweight local interface state.
- A centralized Fetch API client handles JSON requests, timeouts, cancellation with `AbortController`, and normalized errors.
- A native `status-badge` Custom Element demonstrates how a Web Component can be used alongside React.
- The topbar provides global search, notifications, and profile information.

### Global search

The search input is debounced before it calls `GET /api/search`. The API searches available edge nodes, incidents, and regions and returns results that can link to relevant frontend routes.

### Notifications and profile

Notifications are stored in the database. The unread indicator reflects notification state, and `PATCH /api/notifications/read-all` marks notifications as read. The profile panel retrieves profile metadata from `GET /api/profile`.

## 3. Backend and API

The backend uses FastAPI to expose REST endpoints for the dashboard, infrastructure inventory, traffic summaries, incidents, search, notifications, profile data, authentication, health checks, and system metrics.

Pydantic models validate request payloads such as incident creation. Database operations are handled by the database layer in `app/db.py`.

The API includes standard HTTP methods and status codes for reading and changing resources. Validation and missing-resource errors are returned as API responses rather than being handled only in the frontend.

## 4. Database and persistence

The application supports two database modes:

- **SQLite** is the default for local development.
- **PostgreSQL** is configured for the Docker Compose environment.

The relational model includes:

- `regions`
- `edge_nodes`
- `incidents`
- `incident_audit`
- `notifications`

Schema initialization is designed to be repeatable, and seed data is added when the relevant tables are empty. The relational schema is documented in `database/schema.sql`.

Incident creation persists the incident and an associated audit entry. Resolving an incident updates its state and adds another audit event. Since incident and notification state is stored in the database, it can survive API restarts when the same persistent database is used.

## 5. Incident audit trail

The audit trail records important incident lifecycle changes separately from the current incident record. An audit entry includes the incident ID, action, actor, details, and timestamp.

The Incident Center can retrieve this history through `GET /api/incidents/{id}/audit`. Keeping audit events separate from the mutable incident record preserves a history of changes after the incident status has been updated.

## 6. Optional API authentication

Authentication can be enabled through environment configuration. It is disabled by default to preserve the simple local demonstration workflow.

When enabled:

- `GET /api/auth/status` reports whether authentication is enabled without returning credentials.
- `POST /api/auth/login` validates the configured username and password and issues a short-lived bearer token signed with HMAC-SHA256.
- Protected data endpoints require a valid bearer token.
- Liveness and readiness endpoints remain available for container health checks.
- The React application displays a sign-in form when authentication is enabled.

Relevant configuration keys are documented in `.env.example`:

- `EDGEOPS_AUTH_ENABLED`
- `EDGEOPS_ADMIN_USERNAME`
- `EDGEOPS_ADMIN_PASSWORD`
- `EDGEOPS_AUTH_SECRET`

Use unique, strong values for deployments. Do not commit real passwords, tokens, or secret keys. The built-in authentication is a portfolio/demo implementation, not a substitute for a security-reviewed identity provider. It does not by itself provide features such as multi-factor authentication, refresh-token rotation, comprehensive rate limiting, or a full security audit.

## 7. Health checks and system metrics

The API exposes health endpoints for container orchestration and basic operational checks:

- `GET /api/health/live` indicates that the API process can respond.
- `GET /api/health/ready` checks database connectivity and is used as the API readiness probe.

`GET /api/system/metrics` returns a best-effort snapshot of CPU, memory, disk, and load metrics for the environment in which the API runs. Linux `/proc` information is used where available. In a container, reported values may describe the container rather than the physical host. On systems without the expected Linux interfaces, some metrics may be unavailable.

The dashboard displays the returned metrics. This endpoint is not a fleet-wide monitoring or telemetry collection system.

## 8. Linux diagnostics

The read-only helper script `scripts/linux-diagnostics.sh` reports basic Linux host information, including OS details, memory, disk usage, load, processes, and listening TCP ports.

Run it from the repository root:

```bash
bash scripts/linux-diagnostics.sh
```

Review its output before sharing it. Hostnames, process names, addresses, and open ports may reveal information about the machine on which it was run.

## 9. HTTP, browser, and deployment configuration

The project demonstrates:

- JSON-based REST communication
- `GET`, `POST`, and `PATCH` operations
- HTTP status codes such as `200`, `201`, `204`, `400`, and `404`, plus validation responses
- Request cancellation with `AbortController` and request timeouts
- CORS configuration for local development
- Vite proxying during frontend development
- Nginx reverse proxying and single-page application history fallback in the container deployment
- Use of a native browser Custom Element alongside React

### Docker Compose

The container deployment runs three services:

```text
web (Nginx + React production build)
        |
        v
api (FastAPI)
        |
        v
db (PostgreSQL)
```

The PostgreSQL service uses a named Docker volume for persistent database storage. Health checks help ensure the database is ready before the API depends on it and that the API is healthy before the web service is treated as ready.

Start the stack from the repository root with:

```bash
docker compose up --build
```

The Compose configuration includes development/demo defaults. Do not use default or example credentials in a public or production deployment.

## 10. Tests and continuous integration

GitHub Actions is configured to validate the frontend and backend.

Frontend checks include dependency installation, ESLint, Vitest, and a Vite production build. Backend checks install Python dependencies and run Pytest with the project import path configured.

To run backend tests:

```bash
cd backend
python -m pytest -q
```

To run frontend checks:

```bash
cd frontend
npm install
npm test
npm run lint
npm run build
```

Run these commands in an environment with the required runtimes and dependencies installed. Test results should be reported based on the checks actually run in that environment.

## 11. Security and limitations

EdgeOps Console is a portfolio/demo application. Before using it in a public or production environment, review and harden its configuration and security controls.

Important limitations and considerations:

- Seeded node and global traffic figures are demonstration data, not verified live infrastructure measurements.
- System metrics describe the API runtime environment and are not a fleet telemetry collector.
- Authentication is optional and must be explicitly enabled; configure unique credentials and a strong random secret before exposing protected endpoints.
- Use HTTPS, appropriate access controls, secure secret management, rate limiting, structured logging, and security testing for any real deployment.
- Do not expose mutation endpoints to untrusted networks without reviewing authentication and authorization behavior.
- Review diagnostic script output before sharing it publicly.

Potential future improvements for a larger deployment include OAuth 2.0/OpenID Connect, role-based access control, centralized identity, OpenTelemetry tracing, Prometheus/Grafana integration, real-time updates with WebSockets or Server-Sent Events, distributed rate limiting, centralized structured logging, and end-to-end browser tests. These are possible future enhancements and should not be considered implemented unless the codebase explicitly provides them.
