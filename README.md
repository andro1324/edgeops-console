# EdgeOps Console

**Enterprise Network & Cloud Operations Dashboard**

EdgeOps Console is a full-stack infrastructure monitoring and incident-management application built to demonstrate modern JavaScript frontend engineering in an enterprise operations environment.

The project combines a responsive React interface with a FastAPI backend, persistent SQL storage, PostgreSQL support, search, notifications, incident audit history, REST APIs, Docker, Nginx, automated tests and GitHub Actions CI.

## Highlights

- Global network operations dashboard with uptime, edge-node health, request volume and latency metrics
- Infrastructure monitoring for server CPU, memory, disk, operating system and availability
- CDN and traffic intelligence with regional request distribution and HTTP protocol analytics
- Persistent incident creation and resolution workflow
- Persistent incident audit trail
- Functional global search for nodes, incidents and regions
- Functional notifications panel with unread state and mark-all-read action
- Functional user profile panel backed by the API
- React Query server-state caching and mutation invalidation
- Zustand for lightweight local UI state
- Native Web Component integration
- FastAPI REST backend with Pydantic validation
- SQLite persistence for simple local development
- PostgreSQL persistence automatically enabled through Docker Compose
- Dockerized API and frontend
- Nginx reverse proxy and SPA fallback
- Pytest backend tests and Vitest frontend utility tests
- GitHub Actions CI for linting, tests and production builds

## Technology Stack

### Frontend

- React 18
- JavaScript / ES Modules
- Vite
- React Router
- TanStack Query
- Zustand
- Recharts
- Lucide React
- Fetch API
- Web Components / Custom Elements
- HTML5
- Responsive CSS

### Backend

- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- REST / JSON APIs

### Data

- PostgreSQL 16 for Docker-based deployments
- SQLite fallback for zero-configuration local development
- Relational SQL schema
- Persistent incidents, notifications and incident audit history

### DevOps & Quality

- Docker
- Docker Compose
- Nginx
- GitHub Actions
- Pytest
- Vitest
- ESLint

## Application Modules

### Global Overview

The dashboard provides a concise operations view of:

- Global uptime
- Healthy vs total edge nodes
- Requests per minute
- P95 latency
- 24-hour traffic trend
- Regional availability
- Regional health status

### Infrastructure

The infrastructure view displays operational information for edge nodes, including:

- Hostname
- Region
- IP address
- Operating system
- Uptime
- CPU utilization
- Memory utilization
- Disk utilization
- Health state

### Traffic Intelligence

Traffic analytics include:

- 24-hour request volume
- CDN cache-hit ratio
- TLS 1.3 adoption
- Countries served
- Top delivery regions
- HTTP/1.1, HTTP/2 and HTTP/3 share
- QUIC transport
- IPv6 traffic

### Incident Center

The incident workflow supports:

- Listing current and resolved incidents
- Creating incidents
- Severity and region classification
- Resolving active incidents
- Persistent database storage
- Persistent incident audit history
- Notifications generated for newly created incidents

## Functional Topbar

The application topbar is fully interactive.

### Search

The global search field queries the backend after a short debounce and returns matching:

- Edge nodes
- Incidents
- Regions

Selecting a result navigates directly to the relevant application section.

### Notifications

The notification bell loads persistent notifications from the backend. Users can:

- View unread notifications
- Open the related application section
- Mark all notifications as read

### Profile

The profile control opens a live profile panel populated by the API with role, email, location, availability and timezone information.

## REST API

FastAPI exposes the following endpoints:

```text
GET   /api/health
GET   /api/overview
GET   /api/nodes
GET   /api/traffic
GET   /api/incidents
POST  /api/incidents
PATCH /api/incidents/{id}/resolve
GET   /api/incidents/{id}/audit
GET   /api/search?q={query}
GET   /api/notifications
PATCH /api/notifications/read-all
GET   /api/profile
```

Interactive API documentation is available at:

```text
http://localhost:8000/api/docs
```

## Persistence Model

The backend no longer stores incidents only in Python memory.

For regular local development, the API automatically creates and uses a persistent SQLite database:

```text
backend/edgeops.db
```

For the containerized environment, Docker Compose automatically provisions PostgreSQL and configures the API to use it.

The relational schema includes:

- `regions`
- `edge_nodes`
- `incidents`
- `incident_audit`
- `notifications`

The source schema is available in:

```text
database/schema.sql
```

## Project Structure

```text
edgeops-console/
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── main.py
│   │   └── models.py
│   ├── tests/
│   │   └── test_api.py
│   └── requirements.txt
├── database/
│   └── schema.sql
├── docs/
│   └── ARCHITECTURE.md
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── dashboard/
│   │   │   ├── incidents/
│   │   │   ├── infrastructure/
│   │   │   └── traffic/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── store/
│   │   ├── styles/
│   │   └── web-components/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.js
├── nginx/
│   └── default.conf
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Local Development

### Prerequisites

- Node.js 20+
- npm
- Python 3.12+
- pip

### Backend

```bash
cd backend
python -m venv .venv
```

Activate the environment.

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Install dependencies and start the API:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at:

```text
http://localhost:8000
```

When `DATABASE_URL` is not provided, the backend automatically uses persistent SQLite storage.

### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

Vite automatically proxies `/api` traffic to the FastAPI development server.

## Docker Compose

The complete production-like environment can be started with one command:

```bash
docker compose up --build
```

Docker Compose starts:

1. PostgreSQL 16
2. FastAPI backend
3. React production build served by Nginx

Open the application at:

```text
http://localhost:8080
```

The API is also exposed at:

```text
http://localhost:8000
```

PostgreSQL data is stored in a named Docker volume, so incidents, notifications and audit entries survive container restarts.

To remove containers and the database volume completely:

```bash
docker compose down -v
```

## Testing

### Backend

```bash
cd backend
PYTHONPATH=. pytest -q
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH="."
pytest -q
```

The backend test suite covers:

- Operations overview contract
- Incident creation
- Incident resolution
- Persistent incident audit entries
- Global search
- Notifications
- Mark-all-read behavior
- Profile endpoint

### Frontend

```bash
cd frontend
npm run test
```

### Code Quality

```bash
cd frontend
npm run lint
npm run build
```

## Continuous Integration

GitHub Actions runs automatically for pushes to `main` and pull requests.

The CI workflow performs:

### Frontend

- Dependency installation
- ESLint validation
- Vitest tests
- Production Vite build

### Backend

- Python dependency installation
- Pytest test suite with the correct module path

The workflow is located at:

```text
.github/workflows/ci.yml
```

## HTTP & Browser Engineering

The project demonstrates practical web-platform knowledge through:

- RESTful resource design
- JSON content negotiation
- GET, POST and PATCH requests
- Correct HTTP response codes
- Fetch API
- AbortController request cancellation
- Request timeout handling
- CORS
- SPA routing
- Nginx reverse proxying
- Native Custom Elements
- Responsive semantic UI components

## Architecture Decisions

The frontend is organized by business feature rather than as a single flat component directory. Shared UI primitives remain separate from domain-specific functionality.

TanStack Query owns server state, while Zustand is limited to local UI state. HTTP logic is centralized in a reusable API client so components do not duplicate networking concerns.

The backend uses a lightweight database abstraction that supports SQLite for easy development and PostgreSQL for containerized deployment. Database initialization is idempotent and seeds realistic operational demo data only when tables are empty.

Incident mutations write to both the incident record and a persistent audit trail. Notification state is persisted rather than being recreated only on the frontend.

More detail is available in `docs/ARCHITECTURE.md`.

## Production Evolution

The current project already includes persistent PostgreSQL support, an audit trail, Docker deployment, CI and functional operational interactions.

For a larger real-world deployment, logical next steps would include:

- OAuth 2.0 / OpenID Connect authentication
- Role-based authorization
- WebSocket or Server-Sent Events for real-time telemetry
- OpenTelemetry traces
- Prometheus metrics and Grafana dashboards
- Distributed rate limiting
- Centralized secrets management
- Horizontal API scaling
- End-to-end Playwright tests
- Production identity-provider integration

These are future scalability and security enhancements and are not presented as currently implemented features.

## Author

**Andrej Pecirep**  
Bachelor of Electrical Engineering — Computing and Informatics  
Kiseljak, Bosnia and Herzegovina

GitHub: `https://github.com/andro1324`

## License

This project is intended for portfolio, educational and technical demonstration purposes.
