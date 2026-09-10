import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./edgeops.db')


def _is_postgres():
    return DATABASE_URL.startswith('postgresql://') or DATABASE_URL.startswith('postgres://')


@contextmanager
def connection():
    if _is_postgres():
        import psycopg
        from psycopg.rows import dict_row
        conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    else:
        path = DATABASE_URL.removeprefix('sqlite:///')
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def _execute(conn, sql, params=()):
    if _is_postgres():
        sql = sql.replace('?', '%s')
    return conn.execute(sql, params)


def _scalar(conn, sql, params=()):
    row = _execute(conn, sql, params).fetchone()
    if row is None:
        return None
    return list(dict(row).values())[0]


def init_db():
    statements = [
        """CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY,
            code VARCHAR(16) NOT NULL UNIQUE,
            name VARCHAR(80) NOT NULL,
            continent VARCHAR(32) NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS edge_nodes (
            id INTEGER PRIMARY KEY,
            hostname VARCHAR(120) NOT NULL UNIQUE,
            region_id INTEGER NOT NULL REFERENCES regions(id),
            ip_address VARCHAR(45) NOT NULL,
            status VARCHAR(20) NOT NULL CHECK (status IN ('healthy','degraded','offline')),
            os_name VARCHAR(80) NOT NULL,
            uptime_label VARCHAR(40) NOT NULL,
            cpu INTEGER NOT NULL,
            memory INTEGER NOT NULL,
            disk INTEGER NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY,
            title VARCHAR(120) NOT NULL,
            summary TEXT NOT NULL,
            severity VARCHAR(20) NOT NULL CHECK (severity IN ('low','medium','high','critical')),
            status VARCHAR(20) NOT NULL CHECK (status IN ('investigating','monitoring','resolved')),
            region_id INTEGER REFERENCES regions(id),
            owner VARCHAR(120) NOT NULL,
            started_at TIMESTAMP NOT NULL,
            resolved_at TIMESTAMP NULL
        )""",
        """CREATE TABLE IF NOT EXISTS incident_audit (
            id INTEGER PRIMARY KEY,
            incident_id INTEGER NOT NULL REFERENCES incidents(id),
            action VARCHAR(40) NOT NULL,
            actor VARCHAR(120) NOT NULL,
            details TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY,
            title VARCHAR(140) NOT NULL,
            message TEXT NOT NULL,
            level VARCHAR(20) NOT NULL,
            target_path VARCHAR(120) NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""",
    ]
    with connection() as conn:
        for stmt in statements:
            _execute(conn, stmt)
        _seed(conn)


def _seed(conn):
    if (_scalar(conn, 'SELECT COUNT(*) FROM regions') or 0) == 0:
        regions = [
            (1, 'EU-CENTRAL', 'Frankfurt', 'Europe'),
            (2, 'EU-WEST', 'Amsterdam', 'Europe'),
            (3, 'US-EAST', 'Virginia', 'North America'),
            (4, 'US-WEST', 'California', 'North America'),
            (5, 'AP-SOUTH', 'Singapore', 'Asia'),
            (6, 'GLOBAL', 'Global', 'Global'),
        ]
        for row in regions:
            _execute(conn, 'INSERT INTO regions (id, code, name, continent) VALUES (?, ?, ?, ?)', row)

    if (_scalar(conn, 'SELECT COUNT(*) FROM edge_nodes') or 0) == 0:
        nodes = [
            (1, 'fra-edge-01', 1, '10.40.1.11', 'healthy', 'Ubuntu 24.04', '143d 8h', 42, 61, 38),
            (2, 'fra-edge-02', 1, '10.40.1.12', 'healthy', 'Ubuntu 24.04', '87d 2h', 58, 67, 51),
            (3, 'ams-edge-04', 2, '10.41.4.14', 'healthy', 'Debian 12', '201d 4h', 36, 54, 45),
            (4, 'iad-edge-03', 3, '10.52.3.13', 'degraded', 'Ubuntu 24.04', '61d 19h', 86, 78, 63),
            (5, 'sfo-edge-02', 4, '10.54.2.12', 'healthy', 'Rocky Linux 9', '119d 5h', 49, 58, 41),
            (6, 'sin-edge-05', 5, '10.67.5.15', 'healthy', 'Debian 12', '98d 11h', 63, 71, 57),
        ]
        for row in nodes:
            _execute(conn, '''INSERT INTO edge_nodes
                (id, hostname, region_id, ip_address, status, os_name, uptime_label, cpu, memory, disk)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

    if (_scalar(conn, 'SELECT COUNT(*) FROM incidents') or 0) == 0:
        now = datetime.now(timezone.utc)
        incidents = [
            (1003, 'Elevated origin latency', 'Increased origin response time affecting a subset of EU-CENTRAL cache misses. Traffic remains served while origin routing is being optimized.', 'medium', 'monitoring', 1, 'Network SRE', (now - timedelta(hours=2, minutes=18)).isoformat(), None),
            (1002, 'Packet loss on transit provider', 'Automated routing shifted traffic away from a degraded upstream path in US-EAST. Customer impact has cleared.', 'high', 'resolved', 3, 'Edge Operations', (now - timedelta(days=1, hours=4)).isoformat(), (now - timedelta(days=1, hours=2)).isoformat()),
            (1001, 'Cache purge queue delay', 'Purge propagation briefly exceeded the internal SLO during a high-volume deployment window.', 'low', 'resolved', 6, 'Platform', (now - timedelta(days=3, hours=7)).isoformat(), (now - timedelta(days=3, hours=6)).isoformat()),
        ]
        for row in incidents:
            _execute(conn, '''INSERT INTO incidents
                (id, title, summary, severity, status, region_id, owner, started_at, resolved_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)
            audit_id = (_scalar(conn, 'SELECT COALESCE(MAX(id), 0) + 1 FROM incident_audit') or 1)
            _execute(conn, 'INSERT INTO incident_audit (id, incident_id, action, actor, details) VALUES (?, ?, ?, ?, ?)', (audit_id, row[0], 'created', row[6], 'Seeded operational incident'))

    if (_scalar(conn, 'SELECT COUNT(*) FROM notifications') or 0) == 0:
        notifications = [
            (1, 'Node degradation detected', 'iad-edge-03 is reporting elevated CPU utilization.', 'warning', '/infrastructure', 0),
            (2, 'Incident requires monitoring', 'Elevated origin latency remains under active observation.', 'info', '/incidents', 0),
            (3, 'Traffic milestone', 'HTTP/3 traffic share reached 42% across the edge network.', 'success', '/traffic', 0),
        ]
        for row in notifications:
            _execute(conn, 'INSERT INTO notifications (id, title, message, level, target_path, is_read) VALUES (?, ?, ?, ?, ?, ?)', row)


def get_nodes():
    with connection() as conn:
        rows = _execute(conn, '''SELECT n.id, n.hostname, r.name AS region, n.ip_address AS ip,
            n.status, n.os_name AS os, n.uptime_label AS uptime, n.cpu, n.memory, n.disk
            FROM edge_nodes n JOIN regions r ON r.id = n.region_id ORDER BY n.id''').fetchall()
        return [dict(r) for r in rows]


def get_incidents():
    with connection() as conn:
        rows = _execute(conn, '''SELECT i.id, i.title, i.summary, i.severity, i.status,
            r.code AS region, i.owner, i.started_at, i.resolved_at
            FROM incidents i LEFT JOIN regions r ON r.id = i.region_id
            ORDER BY i.started_at DESC''').fetchall()
        return [dict(r) for r in rows]


def create_incident_record(payload):
    with connection() as conn:
        region_id = _scalar(conn, 'SELECT id FROM regions WHERE code = ?', (payload.region,))
        if region_id is None:
            raise ValueError('Unknown region')
        next_id = (_scalar(conn, 'SELECT COALESCE(MAX(id), 1000) + 1 FROM incidents') or 1001)
        started_at = datetime.now(timezone.utc).isoformat()
        owner = 'Platform Operations'
        _execute(conn, '''INSERT INTO incidents
            (id, title, summary, severity, status, region_id, owner, started_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (next_id, payload.title, payload.summary, payload.severity, 'investigating', region_id, owner, started_at))
        audit_id = (_scalar(conn, 'SELECT COALESCE(MAX(id), 0) + 1 FROM incident_audit') or 1)
        _execute(conn, 'INSERT INTO incident_audit (id, incident_id, action, actor, details) VALUES (?, ?, ?, ?, ?)',
                 (audit_id, next_id, 'created', owner, 'Incident created from EdgeOps Console'))
        notification_id = (_scalar(conn, 'SELECT COALESCE(MAX(id), 0) + 1 FROM notifications') or 1)
        _execute(conn, '''INSERT INTO notifications
            (id, title, message, level, target_path, is_read)
            VALUES (?, ?, ?, ?, ?, 0)''',
            (notification_id, 'New incident created', payload.title, payload.severity, '/incidents'))
    return get_incident(next_id)


def get_incident(incident_id):
    with connection() as conn:
        row = _execute(conn, '''SELECT i.id, i.title, i.summary, i.severity, i.status,
            r.code AS region, i.owner, i.started_at, i.resolved_at
            FROM incidents i LEFT JOIN regions r ON r.id = i.region_id WHERE i.id = ?''', (incident_id,)).fetchone()
        return dict(row) if row else None


def resolve_incident_record(incident_id):
    with connection() as conn:
        exists = _scalar(conn, 'SELECT COUNT(*) FROM incidents WHERE id = ?', (incident_id,))
        if not exists:
            return None
        resolved_at = datetime.now(timezone.utc).isoformat()
        _execute(conn, "UPDATE incidents SET status = 'resolved', resolved_at = ? WHERE id = ?", (resolved_at, incident_id))
        audit_id = (_scalar(conn, 'SELECT COALESCE(MAX(id), 0) + 1 FROM incident_audit') or 1)
        _execute(conn, 'INSERT INTO incident_audit (id, incident_id, action, actor, details) VALUES (?, ?, ?, ?, ?)',
                 (audit_id, incident_id, 'resolved', 'Platform Operations', 'Incident marked as resolved'))
    return get_incident(incident_id)


def get_incident_audit(incident_id):
    with connection() as conn:
        rows = _execute(conn, 'SELECT id, incident_id, action, actor, details, created_at FROM incident_audit WHERE incident_id = ? ORDER BY created_at DESC', (incident_id,)).fetchall()
        return [dict(r) for r in rows]


def get_notifications():
    with connection() as conn:
        rows = _execute(conn, 'SELECT id, title, message, level, target_path, is_read, created_at FROM notifications ORDER BY created_at DESC, id DESC LIMIT 12').fetchall()
        result = [dict(r) for r in rows]
        for item in result:
            item['is_read'] = bool(item['is_read'])
        return result


def mark_notifications_read():
    with connection() as conn:
        _execute(conn, 'UPDATE notifications SET is_read = 1 WHERE is_read = 0')
    return get_notifications()


def search_everything(query):
    q = f"%{query.lower()}%"
    with connection() as conn:
        node_rows = _execute(conn, '''SELECT n.id, n.hostname, r.name AS region, n.status
            FROM edge_nodes n JOIN regions r ON r.id = n.region_id
            WHERE LOWER(n.hostname) LIKE ? OR LOWER(r.name) LIKE ? OR LOWER(n.ip_address) LIKE ?
            LIMIT 6''', (q, q, q)).fetchall()
        incident_rows = _execute(conn, '''SELECT i.id, i.title, i.severity, i.status, r.code AS region
            FROM incidents i LEFT JOIN regions r ON r.id = i.region_id
            WHERE LOWER(i.title) LIKE ? OR LOWER(i.summary) LIKE ? OR LOWER(r.code) LIKE ?
            LIMIT 6''', (q, q, q)).fetchall()
        region_rows = _execute(conn, '''SELECT id, code, name FROM regions
            WHERE LOWER(code) LIKE ? OR LOWER(name) LIKE ? LIMIT 6''', (q, q)).fetchall()
    return {
        'nodes': [{**dict(r), 'path': '/infrastructure', 'type': 'node'} for r in node_rows],
        'incidents': [{**dict(r), 'path': '/incidents', 'type': 'incident'} for r in incident_rows],
        'regions': [{**dict(r), 'path': '/dashboard', 'type': 'region'} for r in region_rows],
    }
