import { Bell, Menu, Search } from 'lucide-react';
import { useUIStore } from '../store/uiStore';

export default function Topbar() {
  const toggle = useUIStore((s) => s.toggleSidebar);
  return (
    <header className="topbar">
      <button className="icon-button mobile-only" onClick={toggle} aria-label="Open navigation"><Menu size={20} /></button>
      <div className="search-box"><Search size={17} /><input aria-label="Search" placeholder="Search nodes, incidents, regions…" /></div>
      <div className="topbar-actions">
        <button className="icon-button" aria-label="Notifications"><Bell size={19} /><span className="notification-dot" /></button>
        <div className="profile"><div className="avatar">AP</div><div className="profile-copy"><strong>Andrej P.</strong><span>Platform Engineer</span></div></div>
      </div>
    </header>
  );
}