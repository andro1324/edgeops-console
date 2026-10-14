import { Activity, CircleCheckBig, Gauge, Server, Cpu, MemoryStick, HardDrive } from 'lucide-react';
import { api } from '../../api/client';
import { useApiQuery } from '../../hooks/useApiQuery';
import { formatLatency, formatNumber, formatPercent } from '../../lib/format';
import ErrorState from '../../components/ErrorState';
import LoadingState from '../../components/LoadingState';
import MetricCard from '../../components/MetricCard';
import PageHeader from '../../components/PageHeader';
import Panel from '../../components/Panel';
import TrafficChart from './TrafficChart';
import RegionHealth from './RegionHealth';

export default function DashboardPage() {
  const { data, isLoading, error, refetch } = useApiQuery(['overview'], api.getOverview, { refetchInterval: 30_000 });
  const { data: system, isLoading: systemLoading, error: systemError, refetch: refreshSystem } = useApiQuery(['system-metrics'], api.getSystemMetrics, { refetchInterval: 15_000, retry: 0 });
  return (
    <>
      <PageHeader eyebrow="Network Operations" title="Global overview" description="Real-time health, capacity and traffic signals across the edge network." action={<button className="primary-button" onClick={() => refetch()}>Refresh metrics</button>} />
      {isLoading ? <LoadingState rows={7} /> : error ? <ErrorState message={error.message} onRetry={refetch} /> : (
        <>
          <div className="metric-grid">
            <MetricCard icon={CircleCheckBig} label="Global uptime" value={formatPercent(data.uptime, 2)} delta="+0.03%" helper="vs last 30d" tone="success" />
            <MetricCard icon={Server} label="Healthy nodes" value={`${data.healthy_nodes}/${data.total_nodes}`} delta="+2" helper="this week" tone="info" />
            <MetricCard icon={Activity} label="Requests / min" value={formatNumber(data.requests_per_minute)} delta="+8.4%" helper="vs last hour" tone="accent" />
            <MetricCard icon={Gauge} label="P95 latency" value={formatLatency(data.p95_latency_ms)} delta="-11ms" helper="improvement" tone="warning" />
          </div>
          <Panel title="Host system metrics" subtitle={system?.note || 'Live metrics from the environment running the API'}>
            {systemLoading ? <LoadingState rows={2} /> : systemError ? <ErrorState message={systemError.message} onRetry={refreshSystem} /> : (
              <div className="metric-grid system-metric-grid">
                <MetricCard icon={Cpu} label="CPU usage" value={system.cpu_percent == null ? 'N/A' : `${system.cpu_percent}%`} helper="Linux /proc/stat" tone="accent" />
                <MetricCard icon={MemoryStick} label="Memory usage" value={system.memory ? `${system.memory.used_percent}%` : 'N/A'} helper={system.memory ? `${system.memory.used_mb} / ${system.memory.total_mb} MB` : 'Not available'} tone="info" />
                <MetricCard icon={HardDrive} label="Disk usage" value={system.disk ? `${system.disk.used_percent}%` : 'N/A'} helper={system.disk ? `${system.disk.free_gb} GB free` : 'Not available'} tone="warning" />
                <MetricCard icon={Activity} label="Load average" value={system.load_average ? system.load_average.join(' / ') : 'N/A'} helper="1 / 5 / 15 minutes" tone="success" />
              </div>
            )}
          </Panel>
          <div className="dashboard-grid">
            <Panel title="Traffic trend" subtitle="Requests served across all regions in the last 24 hours" className="span-2"><TrafficChart points={data.traffic_series} /></Panel>
            <Panel title="Regional health" subtitle="Live availability by point of presence"><RegionHealth regions={data.regions} /></Panel>
          </div>
        </>
      )}
    </>
  );
}