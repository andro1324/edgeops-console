import { TriangleAlert } from 'lucide-react';
export default function ErrorState({ message = 'Unable to load data.', onRetry }) {
  return <div className="error-state"><TriangleAlert size={22} /><div><strong>Something went wrong</strong><p>{message}</p>{onRetry && <button className="text-button" onClick={onRetry}>Try again</button>}</div></div>;
}