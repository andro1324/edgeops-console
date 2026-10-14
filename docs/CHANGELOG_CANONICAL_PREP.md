# Canonical preparation changes

This document records the portfolio improvements added for study and interview preparation.

## 1. Optional API authentication

- `GET /api/auth/status` reports whether authentication is enabled without revealing credentials.
- `POST /api/auth/login` checks the configured username/password and returns a short-lived HMAC-SHA256 signed bearer token.
- Protected data endpoints require a valid bearer token when `EDGEOPS_AUTH_ENABLED=true`.
- Liveness/readiness endpoints remain public for container probes.
- The React app shows a sign-in form when authentication is enabled.

Configuration is in `.env.example`. Authentication is disabled by default for local demo compatibility. Before a public deployment, enable it and set unique, strong credentials and a random secret of at least 32 characters. This is a portfolio implementation; it is not a replacement for a security-reviewed identity provider, rate limiting, MFA, refresh-token rotation, HTTPS, or a security audit.

## 2. Live system metrics

- `GET /api/system/metrics` reads best-effort CPU, memory, disk, and load-average values from the environment running the API.
- The dashboard now displays those values.
- In a container, the reported values can describe the container environment rather than the physical host.
- Some operating systems do not expose Linux `/proc` metrics; those values may be `null`/not available.

## 3. Health checks

- `/api/health/live` indicates that the API process is responding.
- `/api/health/ready` verifies database connectivity.
- Docker Compose uses readiness to gate dependent services.

## 4. Linux diagnostics

`scripts/linux-diagnostics.sh` reports OS details, memory, disk, load, processes, and listening TCP ports. Run it locally with:

```bash
bash scripts/linux-diagnostics.sh
```

Review its output before sharing it because hostnames, process names, and ports can be sensitive.

## 5. Tests and validation

Run backend tests from the backend directory:

```bash
cd backend
python -m pytest -q
```

Run frontend checks where Node.js dependencies are installed:

```bash
cd frontend
npm install
npm test
npm run lint
npm run build
```

The backend test suite passed in the build environment. The frontend build/lint was not run in this environment because dependencies were not installed and external package downloads were unavailable.
