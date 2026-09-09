from datetime import datetime, timezone, timedelta

NODES = [
    {"id": 1, "hostname": "fra-edge-01", "region": "Frankfurt", "ip": "10.40.1.11", "status": "healthy", "os": "Ubuntu 24.04", "uptime": "143d 8h", "cpu": 42, "memory": 61, "disk": 38},
    {"id": 2, "hostname": "fra-edge-02", "region": "Frankfurt", "ip": "10.40.1.12", "status": "healthy", "os": "Ubuntu 24.04", "uptime": "87d 2h", "cpu": 58, "memory": 67, "disk": 51},
    {"id": 3, "hostname": "ams-edge-04", "region": "Amsterdam", "ip": "10.41.4.14", "status": "healthy", "os": "Debian 12", "uptime": "201d 4h", "cpu": 36, "memory": 54, "disk": 45},
    {"id": 4, "hostname": "iad-edge-03", "region": "Virginia", "ip": "10.52.3.13", "status": "degraded", "os": "Ubuntu 24.04", "uptime": "61d 19h", "cpu": 86, "memory": 78, "disk": 63},
    {"id": 5, "hostname": "sfo-edge-02", "region": "California", "ip": "10.54.2.12", "status": "healthy", "os": "Rocky Linux 9", "uptime": "119d 5h", "cpu": 49, "memory": 58, "disk": 41},
    {"id": 6, "hostname": "sin-edge-05", "region": "Singapore", "ip": "10.67.5.15", "status": "healthy", "os": "Debian 12", "uptime": "98d 11h", "cpu": 63, "memory": 71, "disk": 57},
]

INCIDENTS = [
    {"id": 1003, "title": "Elevated origin latency", "summary": "Increased origin response time affecting a subset of EU-CENTRAL cache misses. Traffic remains served while origin routing is being optimized.", "severity": "medium", "region": "EU-CENTRAL", "status": "monitoring", "owner": "Network SRE", "started_at": datetime.now(timezone.utc) - timedelta(hours=2, minutes=18)},
    {"id": 1002, "title": "Packet loss on transit provider", "summary": "Automated routing shifted traffic away from a degraded upstream path in US-EAST. Customer impact has cleared.", "severity": "high", "region": "US-EAST", "status": "resolved", "owner": "Edge Operations", "started_at": datetime.now(timezone.utc) - timedelta(days=1, hours=4)},
    {"id": 1001, "title": "Cache purge queue delay", "summary": "Purge propagation briefly exceeded the internal SLO during a high-volume deployment window.", "severity": "low", "region": "GLOBAL", "status": "resolved", "owner": "Platform", "started_at": datetime.now(timezone.utc) - timedelta(days=3, hours=7)},
]
