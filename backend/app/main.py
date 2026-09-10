from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Response
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


@app.get('/api/health', status_code=204)
def health() -> Response:
    return Response(status_code=204)


@app.get('/api/overview')
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


@app.get('/api/nodes')
def nodes():
    return get_nodes()


@app.get('/api/traffic')
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


@app.get('/api/incidents', response_model=list[Incident])
def incidents():
    return get_incidents()


@app.post('/api/incidents', response_model=Incident, status_code=201)
def create_incident(payload: IncidentCreate):
    try:
        return create_incident_record(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.patch('/api/incidents/{incident_id}/resolve', response_model=Incident)
def resolve_incident(incident_id: int):
    incident = resolve_incident_record(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail='Incident not found')
    return incident


@app.get('/api/incidents/{incident_id}/audit')
def incident_audit(incident_id: int):
    return get_incident_audit(incident_id)


@app.get('/api/search')
def search(q: str = Query(min_length=2, max_length=80)):
    return search_everything(q.strip())


@app.get('/api/notifications')
def notifications():
    return get_notifications()


@app.patch('/api/notifications/read-all')
def read_all_notifications():
    return mark_notifications_read()


@app.get('/api/profile')
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
