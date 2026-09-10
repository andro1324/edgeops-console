CREATE TABLE IF NOT EXISTS regions (
  id INTEGER PRIMARY KEY,
  code VARCHAR(16) NOT NULL UNIQUE,
  name VARCHAR(80) NOT NULL,
  continent VARCHAR(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS edge_nodes (
  id INTEGER PRIMARY KEY,
  hostname VARCHAR(120) NOT NULL UNIQUE,
  region_id INTEGER NOT NULL REFERENCES regions(id),
  ip_address VARCHAR(45) NOT NULL,
  status VARCHAR(20) NOT NULL CHECK (status IN ('healthy','degraded','offline')),
  os_name VARCHAR(80) NOT NULL,
  uptime_label VARCHAR(40) NOT NULL,
  cpu INTEGER NOT NULL CHECK (cpu BETWEEN 0 AND 100),
  memory INTEGER NOT NULL CHECK (memory BETWEEN 0 AND 100),
  disk INTEGER NOT NULL CHECK (disk BETWEEN 0 AND 100),
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS incidents (
  id INTEGER PRIMARY KEY,
  title VARCHAR(120) NOT NULL,
  summary TEXT NOT NULL,
  severity VARCHAR(20) NOT NULL CHECK (severity IN ('low','medium','high','critical')),
  status VARCHAR(20) NOT NULL CHECK (status IN ('investigating','monitoring','resolved')),
  region_id INTEGER REFERENCES regions(id),
  owner VARCHAR(120) NOT NULL,
  started_at TIMESTAMPTZ NOT NULL,
  resolved_at TIMESTAMPTZ NULL
);

CREATE TABLE IF NOT EXISTS incident_audit (
  id INTEGER PRIMARY KEY,
  incident_id INTEGER NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
  action VARCHAR(40) NOT NULL,
  actor VARCHAR(120) NOT NULL,
  details TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notifications (
  id INTEGER PRIMARY KEY,
  title VARCHAR(140) NOT NULL,
  message TEXT NOT NULL,
  level VARCHAR(20) NOT NULL,
  target_path VARCHAR(120) NOT NULL,
  is_read SMALLINT NOT NULL DEFAULT 0 CHECK (is_read IN (0,1)),
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_incidents_status_started ON incidents(status, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_nodes_region_status ON edge_nodes(region_id, status);
CREATE INDEX IF NOT EXISTS idx_audit_incident_created ON incident_audit(incident_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_notifications_read_created ON notifications(is_read, created_at DESC);
