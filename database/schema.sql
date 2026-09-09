CREATE TABLE regions (
  id INTEGER PRIMARY KEY,
  code VARCHAR(16) NOT NULL UNIQUE,
  name VARCHAR(80) NOT NULL,
  continent VARCHAR(32) NOT NULL
);

CREATE TABLE edge_nodes (
  id INTEGER PRIMARY KEY,
  hostname VARCHAR(120) NOT NULL UNIQUE,
  region_id INTEGER NOT NULL REFERENCES regions(id),
  ip_address VARCHAR(45) NOT NULL,
  status VARCHAR(20) NOT NULL CHECK (status IN ('healthy','degraded','offline')),
  os_name VARCHAR(80) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE incidents (
  id INTEGER PRIMARY KEY,
  title VARCHAR(120) NOT NULL,
  summary TEXT NOT NULL,
  severity VARCHAR(20) NOT NULL CHECK (severity IN ('low','medium','high','critical')),
  status VARCHAR(20) NOT NULL CHECK (status IN ('investigating','monitoring','resolved')),
  region_id INTEGER REFERENCES regions(id),
  owner VARCHAR(120) NOT NULL,
  started_at TIMESTAMP NOT NULL,
  resolved_at TIMESTAMP NULL
);

CREATE INDEX idx_incidents_status_started ON incidents(status, started_at DESC);
CREATE INDEX idx_nodes_region_status ON edge_nodes(region_id, status);
