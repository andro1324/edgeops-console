import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';
import { useUIStore } from '../store/uiStore';

export default function AppShell() {
  const density = useUIStore((state) => state.density);
  return (
    <div className={`app-shell density-${density}`}>
      <Sidebar />
      <div className="workspace">
        <Topbar />
        <main className="page-container"><Outlet /></main>
      </div>
    </div>
  );
}