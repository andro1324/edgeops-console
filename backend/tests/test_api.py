from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_overview_contract():
    response = client.get('/api/overview')
    assert response.status_code == 200
    body = response.json()
    assert body['uptime'] > 99
    assert body['total_nodes'] >= body['healthy_nodes']

def test_incident_lifecycle():
    created = client.post('/api/incidents', json={'title':'Synthetic test incident','summary':'Created by automated API contract test.','severity':'low','region':'EU-CENTRAL'})
    assert created.status_code == 201
    incident_id = created.json()['id']
    resolved = client.patch(f'/api/incidents/{incident_id}/resolve')
    assert resolved.status_code == 200
    assert resolved.json()['status'] == 'resolved'
