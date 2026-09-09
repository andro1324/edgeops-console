export default function LoadingState({ rows = 4 }) {
  return <div className="skeleton-stack" aria-label="Loading">{Array.from({ length: rows }, (_, i) => <div className="skeleton" key={i} />)}</div>;
}