import { Activity, CircleCheckBig, Gauge, Server } from 'lucide-react';
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
          <div className="dashboard-grid">
            <Panel title="Traffic trend" subtitle="Requests served across all regions in the last 24 hours" className="span-2"><TrafficChart points={data.traffic_series} /></Panel>
            <Panel title="Regional health" subtitle="Live availability by point of presence"><RegionHealth regions={data.regions} /></Panel>
          </div>
        </>
      )}
    </>
  );
}