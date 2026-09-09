from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from .data import NODES, INCIDENTS
from .models import Incident, IncidentCreate

app = FastAPI(title='EdgeOps API', version='1.0.0', docs_url='/api/docs', openapi_url='/api/openapi.json')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.get('/api/health', status_code=204)
def health() -> Response:
    return Response(status_code=204)

@app.get('/api/overview')
def overview():
    traffic = [
        {"time": "00:00", "requests": 72}, {"time": "03:00", "requests": 58}, {"time": "06:00", "requests": 84},
        {"time": "09:00", "requests": 131}, {"time": "12:00", "requests": 148}, {"time": "15:00", "requests": 139},
        {"time": "18:00", "requests": 163}, {"time": "21:00", "requests": 122}, {"time": "Now", "requests": 151},
    ]
    return {
        'uptime': 99.987, 'healthy_nodes': 143, 'total_nodes': 146, 'requests_per_minute': 1843200, 'p95_latency_ms': 84,
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
def nodes(): return NODES

@app.get('/api/traffic')
def traffic():
    return {
        'requests_24h': 2_583_941_220, 'cache_hit_ratio': 93.7, 'tls13_share': 88.4, 'countries_served': 187,
        'top_regions': [
            {'region': 'EU Central', 'requests': 784_231_441, 'share': 30.4}, {'region': 'US East', 'requests': 641_029_981, 'share': 24.8},
            {'region': 'EU West', 'requests': 487_310_440, 'share': 18.9}, {'region': 'US West', 'requests': 356_718_927, 'share': 13.8},
            {'region': 'AP South', 'requests': 201_440_872, 'share': 7.8},
        ],
        'protocols': [
            {'name': 'HTTP/3', 'share': 42, 'description': 'QUIC transport'}, {'name': 'HTTP/2', 'share': 51, 'description': 'Multiplexed TCP'},
            {'name': 'HTTP/1.1', 'share': 7, 'description': 'Legacy compatible'}, {'name': 'IPv6', 'share': 39, 'description': 'Dual-stack traffic'},
        ],
    }

@app.get('/api/incidents', response_model=list[Incident])
def incidents(): return sorted(INCIDENTS, key=lambda i: i['started_at'], reverse=True)

@app.post('/api/incidents', response_model=Incident, status_code=201)
def create_incident(payload: IncidentCreate):
    incident = {**payload.model_dump(), 'id': max(i['id'] for i in INCIDENTS) + 1, 'status': 'investigating', 'owner': 'Frontend Demo', 'started_at': datetime.now(timezone.utc)}
    INCIDENTS.append(incident)
    return incident

@app.patch('/api/incidents/{incident_id}/resolve', response_model=Incident)
def resolve_incident(incident_id: int):
    for incident in INCIDENTS:
        if incident['id'] == incident_id:
            incident['status'] = 'resolved'
            return incident
    raise HTTPException(status_code=404, detail='Incident not found')
