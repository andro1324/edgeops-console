import { History, X } from 'lucide-react';
import { api } from '../../api/client';
import { useApiQuery } from '../../hooks/useApiQuery';
import { formatDateTime } from '../../lib/format';
import LoadingState from '../../components/LoadingState';
import ErrorState from '../../components/ErrorState';

export default function IncidentAuditModal({ incident, onClose }) {
  const { data, isLoading, error, refetch } = useApiQuery(['incident-audit', incident.id], () => api.getIncidentAudit(incident.id));
  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={onClose}>
      <div className="modal audit-modal" role="dialog" aria-modal="true" aria-labelledby="audit-title" onMouseDown={(event) => event.stopPropagation()}>
        <header>
          <div><span className="eyebrow">Audit trail</span><h2 id="audit-title">Incident #{incident.id}</h2></div>
          <button className="icon-button" onClick={onClose} aria-label="Close"><X size={19}/></button>
        </header>
        <div className="audit-body">
          <div className="audit-summary"><History size={17}/><div><strong>{incident.title}</strong><span>Persistent operational history</span></div></div>
          {isLoading ? <LoadingState rows={3}/> : error ? <ErrorState message={error.message} onRetry={refetch}/> : (
            <div className="audit-list">
              {data.map((entry) => <div className="audit-entry" key={entry.id}><span className="audit-marker"/><div><strong>{entry.action}</strong><p>{entry.details}</p><small>{entry.actor} · {formatDateTime(entry.created_at)}</small></div></div>)}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
