import os
from pathlib import Path

TEST_DB = Path(__file__).parent / 'edgeops-test.db'
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ['DATABASE_URL'] = f'sqlite:///{TEST_DB}'

from fastapi.testclient import TestClient
from app.main import app


def test_overview_contract():
    with TestClient(app) as client:
        response = client.get('/api/overview')
        assert response.status_code == 200
        body = response.json()
        assert body['uptime'] > 99
        assert body['total_nodes'] >= body['healthy_nodes']


def test_incident_lifecycle_and_audit():
    with TestClient(app) as client:
        created = client.post('/api/incidents', json={
            'title': 'Synthetic test incident',
            'summary': 'Created by automated API contract test.',
            'severity': 'low',
            'region': 'EU-CENTRAL',
        })
        assert created.status_code == 201
        incident_id = created.json()['id']

        audit = client.get(f'/api/incidents/{incident_id}/audit')
        assert audit.status_code == 200
        assert audit.json()[0]['action'] == 'created'

        resolved = client.patch(f'/api/incidents/{incident_id}/resolve')
        assert resolved.status_code == 200
        assert resolved.json()['status'] == 'resolved'

        audit_after = client.get(f'/api/incidents/{incident_id}/audit')
        actions = [entry['action'] for entry in audit_after.json()]
        assert 'created' in actions and 'resolved' in actions


def test_search_notifications_and_profile():
    with TestClient(app) as client:
        search = client.get('/api/search', params={'q': 'Frankfurt'})
        assert search.status_code == 200
        assert len(search.json()['nodes']) >= 1

        notifications = client.get('/api/notifications')
        assert notifications.status_code == 200
        assert len(notifications.json()) >= 1

        marked = client.patch('/api/notifications/read-all')
        assert marked.status_code == 200
        assert all(item['is_read'] for item in marked.json())

        profile = client.get('/api/profile')
        assert profile.status_code == 200
        assert profile.json()['name'] == 'Andrej Pecirep'
