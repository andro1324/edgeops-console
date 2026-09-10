# EdgeOps Console

**Enterprise Network & Cloud Operations Dashboard**

EdgeOps Console is a full-stack network and infrastructure monitoring application designed to demonstrate modern frontend engineering practices in an enterprise-oriented environment.

The platform provides a centralized interface for monitoring global edge infrastructure, CDN traffic, server health, regional availability, network protocols, and operational incidents.

The project combines a modern **React frontend** with a lightweight **FastAPI backend**, RESTful communication, reusable UI architecture, responsive design, SQL modeling, Docker-based deployment, Nginx configuration, automated testing, and continuous integration.

---

## Overview

Modern infrastructure teams need a clear view of network health, server utilization, traffic distribution, regional availability, and active incidents.

EdgeOps Console models such an operational environment through four primary modules:

- **Global Overview** — high-level infrastructure and network metrics
- **Infrastructure** — edge node and server resource monitoring
- **Traffic Intelligence** — CDN, protocol, and regional traffic analytics
- **Incident Center** — incident creation, tracking, and resolution

Unlike a static dashboard mockup, the frontend communicates with a real HTTP API and handles loading states, errors, queries, mutations, and cache invalidation.

---

## Key Features

### Global Operations Dashboard

The main dashboard provides an immediate overview of the network infrastructure, including:

- Global uptime
- Healthy and total edge nodes
- Requests per minute
- P95 response latency
- 24-hour traffic visualization
- Regional availability
- Regional operational status

The dashboard is designed to provide infrastructure operators with the most important system information at a glance.

---

### Infrastructure Monitoring

The infrastructure module provides detailed information about individual edge nodes and servers.

Available information includes:

- Server hostname
- IP address
- Operating system
- Region
- Current status
- CPU utilization
- Memory utilization
- Disk utilization
- System uptime

Reusable UI components and status indicators make it easy to identify degraded or unhealthy infrastructure.

---

### Traffic Intelligence

The Traffic Intelligence module provides insight into CDN delivery and network protocol usage.

Metrics include:

- Total requests over the last 24 hours
- CDN cache-hit ratio
- TLS 1.3 adoption
- Countries served
- Regional request distribution
- HTTP/1.1 usage
- HTTP/2 usage
- HTTP/3 usage
- QUIC transport
- IPv6 traffic share

This module demonstrates how infrastructure telemetry can be transformed into an operationally useful user interface.

---

### Incident Management

EdgeOps Console includes a functional incident management workflow backed by the FastAPI service.

Users can:

- View current and historical incidents
- Inspect incident severity
- Track incident status
- View affected regions
- Identify assigned owners
- Create new incidents
- Resolve active incidents

Incident actions use real HTTP requests rather than local frontend-only state.

TanStack Query handles mutation state and cache invalidation after changes.

---

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
- Native Fetch API
- Web Components
- HTML5
- Custom responsive CSS

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- REST API
- CORS middleware

### Database Design

- SQL
- Relational schema
- Primary and foreign keys
- Constraints
- Indexes

The current portfolio implementation uses in-memory demo data while a relational schema is included for future PostgreSQL persistence.

### Infrastructure & DevOps

- Docker
- Docker Compose
- Nginx
- GitHub Actions
- Linux-compatible container environment

### Testing & Quality

- ESLint
- Pytest
- Vitest-ready frontend configuration
- Automated GitHub Actions CI workflow

---

## Architecture

The project follows a feature-oriented architecture that separates UI components, application state, HTTP communication, business features, and backend services.

```text
edgeops-console/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── data.py
│   │   ├── main.py
│   │   └── models.py
│   │
│   ├── tests/
│   │   └── test_api.py
│   │
│   └── requirements.txt
│
├── database/
│   └── schema.sql
│
├── docs/
│   └── ARCHITECTURE.md
│
├── frontend/
│   ├── public/
│   │
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js
│   │   │
│   │   ├── components/
│   │   │   ├── AppShell.jsx
│   │   │   ├── ErrorState.jsx
│   │   │   ├── LoadingState.jsx
│   │   │   ├── MetricCard.jsx
│   │   │   ├── PageHeader.jsx
│   │   │   ├── Panel.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── Topbar.jsx
│   │   │
│   │   ├── features/
│   │   │   ├── dashboard/
│   │   │   ├── incidents/
│   │   │   ├── infrastructure/
│   │   │   └── traffic/
│   │   │
│   │   ├── hooks/
│   │   │   └── useApiQuery.js
│   │   │
│   │   ├── lib/
│   │   │   └── format.js
│   │   │
│   │   ├── store/
│   │   │   └── uiStore.js
│   │   │
│   │   ├── styles/
│   │   │   └── global.css
│   │   │
│   │   ├── web-components/
│   │   │   └── status-badge.js
│   │   │
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── nginx/
│   └── default.conf
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Frontend Architecture

The frontend is organized around domain features rather than placing all components in a single directory.

Major application domains are located under:

```text
frontend/src/features/
```

and include:

```text
dashboard/
infrastructure/
traffic/
incidents/
```

Shared presentation components remain separate under:

```text
frontend/src/components/
```

This approach improves maintainability and makes the application easier to extend as new operational modules are introduced.

---

## State Management

EdgeOps Console separates **server state** from **client UI state**.

### TanStack Query

TanStack Query manages data received from the backend, including:

- API requests
- Loading states
- Error states
- Caching
- Refetching
- Mutations
- Cache invalidation

### Zustand

Zustand is used only for lightweight client-side presentation state.

This prevents remote API data from being unnecessarily duplicated inside a global frontend store.

---

## HTTP Layer

Frontend components do not communicate with the Fetch API directly.

HTTP communication is centralized in:

```text
frontend/src/api/client.js
```

The request layer handles:

- Base API configuration
- JSON communication
- HTTP headers
- Request timeouts
- AbortController cancellation
- Error normalization
- GET requests
- POST requests
- PATCH requests

This creates a consistent boundary between frontend components and backend services.

---

## Web Components

The project contains a native browser Web Component:

```text
frontend/src/web-components/status-badge.js
```

The custom element demonstrates interoperability between React and browser-native Custom Elements.

It is used for displaying operational status information without relying exclusively on React components.

---

## REST API

The backend exposes the following API routes.

### Health Check

```http
GET /api/health
```

Returns:

```text
204 No Content
```

Used to verify API availability.

---

### Operations Overview

```http
GET /api/overview
```

Returns global infrastructure information such as:

- uptime
- healthy node count
- requests per minute
- latency
- traffic history
- regional availability

---

### Infrastructure Nodes

```http
GET /api/nodes
```

Returns the available edge infrastructure nodes and their current utilization metrics.

---

### Traffic Analytics

```http
GET /api/traffic
```

Returns:

- request volume
- cache-hit ratio
- TLS adoption
- geographic traffic
- HTTP protocol distribution
- IPv6 usage

---

### List Incidents

```http
GET /api/incidents
```

Returns operational incidents ordered by start time.

---

### Create Incident

```http
POST /api/incidents
```

Creates a new operational incident.

The backend validates the request payload using Pydantic models and returns:

```text
201 Created
```

---

### Resolve Incident

```http
PATCH /api/incidents/{incident_id}/resolve
```

Marks an existing incident as resolved.

If the incident does not exist, the API returns:

```text
404 Not Found
```

---

## HTTP & Browser Engineering

The application demonstrates practical HTTP and browser concepts rather than abstracting everything behind third-party libraries.

Implemented concepts include:

- RESTful endpoint design
- JSON request and response bodies
- `Accept` headers
- `Content-Type` headers
- HTTP status codes
- CORS
- Fetch API
- AbortController
- Request cancellation
- API timeout handling
- Error normalization
- Reverse proxying
- SPA routing fallback

The backend uses appropriate HTTP response codes including:

```text
200 OK
201 Created
204 No Content
404 Not Found
```

Validation errors are handled automatically through FastAPI and Pydantic.

---

## Responsive UI

The user interface is built using custom CSS rather than a UI framework.

The styling architecture includes:

- CSS design tokens
- Responsive breakpoints
- Grid layouts
- Flexible dashboard cards
- Responsive navigation
- Accessible buttons and controls
- Mobile-friendly layouts
- Consistent spacing and typography
- Operational status indicators

The interface is intended to resemble a modern network operations or infrastructure management platform.

---

## Local Development

### Prerequisites

Make sure the following tools are installed:

- Node.js 20+
- npm
- Python 3.11+
- pip
- Git

Docker is optional for containerized execution.

---

## Run the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/api/docs
```

OpenAPI specification:

```text
http://localhost:8000/api/openapi.json
```

---

## Run the Frontend

Open another terminal and navigate to:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

During development, Vite proxies frontend `/api` requests to the FastAPI backend.

---

## Frontend Commands

Start the development environment:

```bash
npm run dev
```

Create a production build:

```bash
npm run build
```

Run ESLint:

```bash
npm run lint
```

Preview the production build:

```bash
npm run preview
```

Run configured frontend tests:

```bash
npm run test
```

---

## Backend Tests

Navigate to:

```bash
cd backend
```

Run:

```bash
pytest -q
```

Backend tests cover core API behavior, including:

- API read operations
- Incident creation
- Incident resolution lifecycle

---

## Docker

A Docker configuration is included for containerized execution.

Build the application image:

```bash
docker build -t edgeops-console .
```

Run the container:

```bash
docker run --rm -p 8000:8000 edgeops-console
```

---

## Docker Compose & Nginx

The project also includes Docker Compose and Nginx configuration for a multi-service deployment example.

First create the frontend production build:

```bash
cd frontend
npm install
npm run build
```

Return to the project root and run:

```bash
docker compose up --build
```

The application can then be accessed at:

```text
http://localhost:8080
```

Nginx provides:

- Static frontend delivery
- Single-page application routing fallback
- API reverse proxying
- HTTP forwarding
- Basic production security headers

---

## Continuous Integration

The repository includes a GitHub Actions workflow located at:

```text
.github/workflows/ci.yml
```

The CI pipeline performs automated quality checks for the application.

This helps detect problems before changes are integrated into the main development branch.

The project includes tooling for:

- Frontend linting
- Frontend production builds
- Backend testing
- Automated repository validation

---

## Database Model

The relational database design is located at:

```text
database/schema.sql
```

The schema demonstrates a production-oriented relational model using:

- Tables
- Primary keys
- Foreign keys
- Constraints
- Indexes

The current application intentionally uses in-memory data to keep the portfolio project easy to run without requiring an external database server.

The provided SQL schema represents the persistence layer that can be used when evolving the application toward a production environment.

---

## Design Decisions

### Feature-Oriented Frontend

Application functionality is grouped around business domains instead of file types alone.

This keeps related components close to the functionality they support.

### Centralized API Layer

Components do not contain duplicated networking logic.

All HTTP communication is handled through the dedicated API layer.

### Server State vs. UI State

Remote API state is managed by TanStack Query, while lightweight interface state is managed independently through Zustand.

### Native Browser APIs

The application intentionally demonstrates knowledge beyond React by using:

- Fetch API
- AbortController
- Custom Elements
- HTTP semantics
- Semantic HTML
- Native CSS

### Real Backend Integration

The backend makes the frontend genuinely dynamic.

This enables realistic:

- loading flows
- error handling
- API queries
- mutations
- state synchronization
- cache invalidation

---

## Production Evolution

EdgeOps Console is currently designed as a portfolio and technical demonstration project.

A real production deployment could extend the architecture with:

- PostgreSQL persistence based on the included relational schema
- OAuth 2.0 / OpenID Connect authentication
- Single Sign-On
- Role-based access control
- Persistent user accounts
- Persistent incident history
- Incident audit trails
- WebSocket or Server-Sent Events for live telemetry
- Prometheus metrics
- Grafana dashboards
- OpenTelemetry distributed tracing
- API rate limiting
- Centralized logging
- Playwright end-to-end testing
- WCAG 2.2 accessibility auditing
- Content Security Policy
- Stricter production CORS policies
- Secrets management
- Horizontal service scaling

These are architectural evolution opportunities rather than features claimed as implemented in the current version.

---

## Engineering Concepts Demonstrated

This project demonstrates practical experience with:

- Modern JavaScript
- React application architecture
- Component-driven development
- REST APIs
- HTTP standards
- Responsive web design
- State management
- Server-state caching
- Browser APIs
- Web Components
- Python backend development
- API validation
- SQL data modeling
- Containerization
- Reverse proxy configuration
- Automated testing
- CI workflows
- Enterprise-oriented application architecture

---

## Project Purpose

EdgeOps Console was created as a portfolio project demonstrating how a modern frontend application can be designed for an infrastructure-heavy enterprise environment.

The focus is not only visual presentation but also maintainable architecture, HTTP communication, reusable components, backend integration, testing, deployment concepts, and production-oriented engineering decisions.

---

## Author

**Andrej Pecirep**

Electrical Engineering — Computing and Informatics

Software Developer focused on modern web applications, frontend engineering, backend integration, and enterprise-oriented software development.

---

## License

This project is intended for educational, portfolio, and demonstration purposes.