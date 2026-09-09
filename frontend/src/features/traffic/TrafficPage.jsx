import { Activity, Globe2, ShieldCheck, Zap } from 'lucide-react';
import { api } from '../../api/client';
import { useApiQuery } from '../../hooks/useApiQuery';
import { formatNumber, formatPercent } from '../../lib/format';
import ErrorState from '../../components/ErrorState';
import LoadingState from '../../components/LoadingState';
import MetricCard from '../../components/MetricCard';
import PageHeader from '../../components/PageHeader';
import Panel from '../../components/Panel';

export default function TrafficPage() {
  const { data, isLoading, error, refetch } = useApiQuery(['traffic'], api.getTraffic);
  return <><PageHeader eyebrow="Traffic Intelligence" title="Delivery analytics" description="Observe request volume, cache efficiency, protocols and top delivery regions." />{isLoading ? <LoadingState rows={6}/> : error ? <ErrorState message={error.message} onRetry={refetch}/> : <><div className="metric-grid"><MetricCard icon={Activity} label="24h requests" value={formatNumber(data.requests_24h)} delta="+12.1%" helper="day over day" tone="accent"/><MetricCard icon={Zap} label="Cache hit ratio" value={formatPercent(data.cache_hit_ratio)} delta="+1.8%" helper="optimized" tone="success"/><MetricCard icon={ShieldCheck} label="TLS 1.3" value={formatPercent(data.tls13_share)} delta="+3.2%" helper="adoption" tone="info"/><MetricCard icon={Globe2} label="Countries served" value={data.countries_served} delta="+4" helper="this quarter" tone="warning"/></div><div className="dashboard-grid"><Panel title="Top regions" subtitle="Share of global request volume"><div className="rank-list">{data.top_regions.map((r, i) => <div className="rank-row" key={r.region}><span className="rank">{String(i+1).padStart(2,'0')}</span><div><strong>{r.region}</strong><span>{formatNumber(r.requests)} requests</span></div><div className="share-bar"><span style={{width:`${r.share}%`}}/></div><strong>{r.share}%</strong></div>)}</div></Panel><Panel title="Protocol mix" subtitle="HTTP versions negotiated with clients"><div className="protocol-grid">{data.protocols.map((p) => <div className="protocol-card" key={p.name}><span>{p.name}</span><strong>{p.share}%</strong><small>{p.description}</small></div>)}</div></Panel></div></>}</>;
}