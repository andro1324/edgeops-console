export default function MetricCard({ icon: Icon, label, value, delta, tone = 'neutral', helper }) {
  return (
    <article className="metric-card">
      <div className={`metric-icon tone-${tone}`}><Icon size={20} /></div>
      <div className="metric-content"><span>{label}</span><strong>{value}</strong><small className={delta?.startsWith('+') ? 'positive' : delta?.startsWith('-') ? 'negative' : ''}>{delta} {helper}</small></div>
    </article>
  );
}