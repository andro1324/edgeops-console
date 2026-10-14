from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Response, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import base64, hashlib, hmac, json, os, time
from fastapi.middleware.cors import CORSMiddleware

from .db import (
    create_incident_record,
    get_incident_audit,
    get_incidents,
    get_nodes,
    get_notifications,
    init_db,
    mark_notifications_read,
    resolve_incident_record,
    search_everything,
)
from .models import Incident, IncidentCreate
from .system_metrics import get_system_metrics

# Optional bearer-token authentication. Enable in deployments with EDGEOPS_AUTH_ENABLED=true.
security = HTTPBearer(auto_error=False)
AUTH_ENABLED = os.getenv("EDGEOPS_AUTH_ENABLED", "false").lower() == "true"
AUTH_USERNAME = os.getenv("EDGEOPS_ADMIN_USERNAME", "admin")
AUTH_PASSWORD = os.getenv("EDGEOPS_ADMIN_PASSWORD", "")
AUTH_SECRET = os.getenv("EDGEOPS_AUTH_SECRET", "")

def _b64(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")

def _issue_token(username: str) -> str:
    now = int(time.time())
    header = _b64(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    payload = _b64(json.dumps({"sub": username, "iat": now, "exp": now + 3600}, separators=(",", ":")).encode())
    body = f"{header}.{payload}"
    signature = _b64(hmac.new(AUTH_SECRET.encode(), body.encode(), hashlib.sha256).digest())
    return f"{body}.{signature}"

def _valid_token(token: str) -> str | None:
    try:
        header, payload, signature = token.split(".")
        header_data = json.loads(base64.urlsafe_b64decode(header + "=" * (-len(header) % 4)))
        if header_data.get("alg") != "HS256":
            return None
        body = f"{header}.{payload}"
        expected = _b64(hmac.new(AUTH_SECRET.encode(), body.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(signature, expected):
            return None
        data = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        if int(data.get("exp", 0)) < int(time.time()):
            return None
        return str(data["sub"])
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        return None

def require_auth(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> str | None:
    if not AUTH_ENABLED:
        return None
    if not AUTH_SECRET or not AUTH_PASSWORD:
        raise HTTPException(status_code=503, detail="Authentication is enabled but secrets are not configured")
    username = _valid_token(credentials.credentials) if credentials else None
    if not username:
        raise HTTPException(status_code=401, detail="Authentication required", headers={"WWW-Authenticate": "Bearer"})
    return username


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title='EdgeOps API',
    version='2.0.0',
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://localhost:8080'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/api/auth/status')
def auth_status():
    return {'enabled': AUTH_ENABLED}


@app.post('/api/auth/login')
def login(payload: dict):
    if not AUTH_ENABLED:
        raise HTTPException(status_code=404, detail='Authentication is disabled')
    if not AUTH_SECRET or not AUTH_PASSWORD:
        raise HTTPException(status_code=503, detail='Authentication secrets are not configured')
    username = str(payload.get('username', ''))
    password = str(payload.get('password', ''))
    if not hmac.compare_digest(username, AUTH_USERNAME) or not hmac.compare_digest(password, AUTH_PASSWORD):
        raise HTTPException(status_code=401, detail='Invalid username or password')
    return {'access_token': _issue_token(username), 'token_type': 'bearer', 'expires_in': 3600}


@app.get('/api/health/live')
def liveness() -> dict:
    return {'status': 'ok'}


@app.get('/api/health/ready')
def readiness() -> dict:
    # A lightweight database check makes this suitable for container readiness probes.
    from .db import connection
    try:
        with connection() as conn:
            conn.execute('SELECT 1')
    except Exception as exc:
        raise HTTPException(status_code=503, detail='Database is unavailable') from exc
    return {'status': 'ready', 'database': 'ok'}


@app.get('/api/health', status_code=204)
def health() -> Response:
    return Response(status_code=204)


@app.get('/api/system/metrics', dependencies=[Depends(require_auth)])
def system_metrics():
    """Return a best-effort snapshot of the environment running the API."""
    return get_system_metrics()


@app.get('/api/overview', dependencies=[Depends(require_auth)])
def overview():
    traffic = [
        {'time': '00:00', 'requests': 72}, {'time': '03:00', 'requests': 58}, {'time': '06:00', 'requests': 84},
        {'time': '09:00', 'requests': 131}, {'time': '12:00', 'requests': 148}, {'time': '15:00', 'requests': 139},
        {'time': '18:00', 'requests': 163}, {'time': '21:00', 'requests': 122}, {'time': 'Now', 'requests': 151},
    ]
    nodes = get_nodes()
    healthy = sum(1 for node in nodes if node['status'] == 'healthy')
    return {
        'uptime': 99.987,
        'healthy_nodes': 143 if len(nodes) == 6 else healthy,
        'total_nodes': 146 if len(nodes) == 6 else len(nodes),
        'requests_per_minute': 1_843_200,
        'p95_latency_ms': 84,
        'traffic_series': traffic,
        'regions': [
            {'code': 'FRA', 'name': 'Frankfurt', 'nodes': 28, 'status': 'operational', 'availability': 99.99},
            {'code': 'AMS', 'name': 'Amsterdam', 'nodes': 22, 'status': 'operational', 'availability': 100.0},
            {'code': 'IAD', 'name': 'Virginia', 'nodes': 31, 'status': 'degraded', 'availability': 99.71},
            {'code': 'SFO', 'name': 'California', 'nodes': 24, 'status': 'operational', 'availability': 99.98},
            {'code': 'SIN', 'name': 'Singapore', 'nodes': 18, 'status': 'operational', 'availability': 99.96},
        ],
    }


@app.get('/api/nodes', dependencies=[Depends(require_auth)])
def nodes():
    return get_nodes()


@app.get('/api/traffic', dependencies=[Depends(require_auth)])
def traffic():
    return {
        'requests_24h': 2_583_941_220,
        'cache_hit_ratio': 93.7,
        'tls13_share': 88.4,
        'countries_served': 187,
        'top_regions': [
            {'region': 'EU Central', 'requests': 784_231_441, 'share': 30.4},
            {'region': 'US East', 'requests': 641_029_981, 'share': 24.8},
            {'region': 'EU West', 'requests': 487_310_440, 'share': 18.9},
            {'region': 'US West', 'requests': 356_718_927, 'share': 13.8},
            {'region': 'AP South', 'requests': 201_440_872, 'share': 7.8},
        ],
        'protocols': [
            {'name': 'HTTP/3', 'share': 42, 'description': 'QUIC transport'},
            {'name': 'HTTP/2', 'share': 51, 'description': 'Multiplexed TCP'},
            {'name': 'HTTP/1.1', 'share': 7, 'description': 'Legacy compatible'},
            {'name': 'IPv6', 'share': 39, 'description': 'Dual-stack traffic'},
        ],
    }


@app.get('/api/incidents', response_model=list[Incident], dependencies=[Depends(require_auth)])
def incidents():
    return get_incidents()


@app.post('/api/incidents', response_model=Incident, status_code=201, dependencies=[Depends(require_auth)])
def create_incident(payload: IncidentCreate):
    try:
        return create_incident_record(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.patch('/api/incidents/{incident_id}/resolve', response_model=Incident, dependencies=[Depends(require_auth)])
def resolve_incident(incident_id: int):
    incident = resolve_incident_record(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail='Incident not found')
    return incident


@app.get('/api/incidents/{incident_id}/audit', dependencies=[Depends(require_auth)])
def incident_audit(incident_id: int):
    return get_incident_audit(incident_id)


@app.get('/api/search', dependencies=[Depends(require_auth)])
def search(q: str = Query(min_length=2, max_length=80)):
    return search_everything(q.strip())


@app.get('/api/notifications', dependencies=[Depends(require_auth)])
def notifications():
    return get_notifications()


@app.patch('/api/notifications/read-all', dependencies=[Depends(require_auth)])
def read_all_notifications():
    return mark_notifications_read()


@app.get('/api/profile', dependencies=[Depends(require_auth)])
def profile():
    return {
        'name': 'Andrej Pecirep',
        'initials': 'AP',
        'role': 'Platform Engineer',
        'email': 'pecirepandrej6@gmail.com',
        'location': 'Kiseljak, Bosnia and Herzegovina',
        'status': 'Available',
        'timezone': 'Europe/Sarajevo',
    }
