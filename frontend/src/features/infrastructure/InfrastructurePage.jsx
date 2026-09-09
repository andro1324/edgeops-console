import { Cpu, HardDrive, MemoryStick, Server } from 'lucide-react';
import { api } from '../../api/client';
import { useApiQuery } from '../../hooks/useApiQuery';
import { formatPercent } from '../../lib/format';
import ErrorState from '../../components/ErrorState';
import LoadingState from '../../components/LoadingState';
import PageHeader from '../../components/PageHeader';

const ResourceBar = ({ label, value, icon: Icon }) => <div className="resource"><div className="resource-top"><span><Icon size={15}/>{label}</span><strong>{formatPercent(value, 0)}</strong></div><div className="progress"><span style={{ width: `${Math.min(value, 100)}%` }} /></div></div>;

export default function InfrastructurePage() {
  const { data, isLoading, error, refetch } = useApiQuery(['nodes'], api.getNodes);
  return <><PageHeader eyebrow="Infrastructure" title="Edge nodes" description="Capacity and runtime status for globally distributed compute nodes." />{isLoading ? <LoadingState rows={8}/> : error ? <ErrorState message={error.message} onRetry={refetch}/> : <div className="node-grid">{data.map((node) => <article className="node-card" key={node.id}><header><div className="node-icon"><Server size={20}/></div><div><strong>{node.hostname}</strong><span>{node.region} · {node.ip}</span></div><status-badge status={node.status}>{node.status}</status-badge></header><div className="node-meta"><span>OS <strong>{node.os}</strong></span><span>Uptime <strong>{node.uptime}</strong></span></div><ResourceBar label="CPU" value={node.cpu} icon={Cpu}/><ResourceBar label="Memory" value={node.memory} icon={MemoryStick}/><ResourceBar label="Disk" value={node.disk} icon={HardDrive}/></article>)}</div>}</>;
}