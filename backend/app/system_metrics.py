"""Read host metrics on Linux without requiring privileged system APIs.

Values are best-effort snapshots for a portfolio/demo environment, not a
replacement for a production monitoring agent.
"""
from __future__ import annotations

import os
import shutil
import time
from pathlib import Path


def _read_cpu_counters() -> tuple[int, int] | None:
    try:
        fields = Path('/proc/stat').read_text(encoding='utf-8').splitlines()[0].split()[1:]
        values = [int(value) for value in fields]
        idle = values[3] + (values[4] if len(values) > 4 else 0)
        return sum(values), idle
    except (OSError, ValueError, IndexError):
        return None


def _cpu_percent() -> float | None:
    first = _read_cpu_counters()
    if first is None:
        return None
    time.sleep(0.08)
    second = _read_cpu_counters()
    if second is None:
        return None
    total_delta = second[0] - first[0]
    idle_delta = second[1] - first[1]
    if total_delta <= 0:
        return 0.0
    return round(max(0.0, min(100.0, (1 - idle_delta / total_delta) * 100)), 2)


def _memory() -> dict[str, int] | None:
    try:
        values: dict[str, int] = {}
        for line in Path('/proc/meminfo').read_text(encoding='utf-8').splitlines():
            key, value = line.split(':', 1)
            if key in {'MemTotal', 'MemAvailable'}:
                values[key] = int(value.strip().split()[0])
        total = values['MemTotal']
        available = values['MemAvailable']
        used = total - available
        return {
            'total_mb': round(total / 1024),
            'used_mb': round(used / 1024),
            'used_percent': round((used / total) * 100, 2) if total else 0,
        }
    except (OSError, ValueError, KeyError, IndexError):
        return None


def get_system_metrics() -> dict:
    """Return best-effort metrics for the process/container environment."""
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.08)
        mem = psutil.virtual_memory()
        memory = {'total_mb': round(mem.total / (1024 ** 2)), 'used_mb': round(mem.used / (1024 ** 2)), 'used_percent': round(mem.percent, 2)}
        disk_usage = psutil.disk_usage('/')
        disk = type('DiskUsage', (), {'total': disk_usage.total, 'used': disk_usage.used, 'free': disk_usage.free})()
    except ImportError:
        cpu = _cpu_percent() if Path('/proc/stat').exists() else None
        memory = _memory() if Path('/proc/meminfo').exists() else None
        disk = shutil.disk_usage('/')
    try:
        load = os.getloadavg()
        load_average = [round(value, 2) for value in load]
    except (AttributeError, OSError):
        load_average = None

    return {
        'source': 'host',
        'platform': os.name,
        'cpu_percent': cpu,
        'memory': memory,
        'disk': {
            'total_gb': round(disk.total / (1024 ** 3), 2),
            'used_gb': round(disk.used / (1024 ** 3), 2),
            'free_gb': round(disk.free / (1024 ** 3), 2),
            'used_percent': round((disk.used / disk.total) * 100, 2) if disk.total else 0,
        },
        'load_average': load_average,
        'note': 'Container metrics describe the container environment, not necessarily the physical host.' if Path('/.dockerenv').exists() else None,
    }
