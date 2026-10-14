from app.system_metrics import get_system_metrics


def test_system_metrics_has_documented_shape():
    result = get_system_metrics()
    assert result['source'] == 'host'
    assert 'cpu_percent' in result
    assert 'memory' in result
    assert {'total_gb', 'used_gb', 'free_gb', 'used_percent'} <= set(result['disk'])
    if result['cpu_percent'] is not None:
        assert 0 <= result['cpu_percent'] <= 100
    if result['memory'] is not None:
        assert 0 <= result['memory']['used_percent'] <= 100


def test_disk_values_are_non_negative():
    disk = get_system_metrics()['disk']
    assert disk['total_gb'] >= 0
    assert disk['used_gb'] >= 0
    assert disk['free_gb'] >= 0
