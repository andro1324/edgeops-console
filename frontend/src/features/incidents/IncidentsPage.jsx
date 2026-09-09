import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { CheckCircle2, Plus } from 'lucide-react';
import { api } from '../../api/client';
import { useApiQuery } from '../../hooks/useApiQuery';
import { formatDateTime } from '../../lib/format';
import ErrorState from '../../components/ErrorState';
import LoadingState from '../../components/LoadingState';
import PageHeader from '../../components/PageHeader';
import IncidentModal from './IncidentModal';

export default function IncidentsPage() {
  const [open, setOpen] = useState(false);
  const queryClient = useQueryClient();
  const { data, isLoading, error, refetch } = useApiQuery(['incidents'], api.getIncidents);
  const resolve = useMutation({ mutationFn: api.resolveIncident, onSuccess: () => queryClient.invalidateQueries({ queryKey: ['incidents'] }) });
  return <><PageHeader eyebrow="Reliability" title="Incident center" description="Track operational events from detection through mitigation and resolution." action={<button className="primary-button" onClick={()=>setOpen(true)}><Plus size={17}/>New incident</button>}/>{isLoading ? <LoadingState rows={7}/> : error ? <ErrorState message={error.message} onRetry={refetch}/> : <div className="incident-list">{data.map((incident)=><article className="incident-card" key={incident.id}><div className={`severity severity-${incident.severity}`}>{incident.severity.toUpperCase()}</div><div className="incident-main"><div className="incident-title-row"><h2>{incident.title}</h2><status-badge status={incident.status}>{incident.status}</status-badge></div><p>{incident.summary}</p><div className="incident-meta"><span>{incident.region}</span><span>Started {formatDateTime(incident.started_at)}</span><span>Owner: {incident.owner}</span></div></div>{incident.status !== 'resolved' && <button className="secondary-button" disabled={resolve.isPending} onClick={()=>resolve.mutate(incident.id)}><CheckCircle2 size={16}/>Resolve</button>}</article>)}</div>}{open && <IncidentModal onClose={()=>setOpen(false)}/>}</>;
}