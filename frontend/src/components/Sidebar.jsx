import { Activity, Gauge, Network, ShieldAlert, Server, X } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { useUIStore } from '../store/uiStore';

const links = [
  { to: '/dashboard', label: 'Overview', icon: Gauge },
  { to: '/infrastructure', label: 'Infrastructure', icon: Server },
  { to: '/traffic', label: 'Traffic', icon: Activity },
  { to: '/incidents', label: 'Incidents', icon: ShieldAlert },
];

export default function Sidebar() {
  const open = useUIStore((s) => s.sidebarOpen);
  const close = useUIStore((s) => s.closeSidebar);
  return (
    <>
      {open && <button className="sidebar-scrim" aria-label="Close navigation" onClick={close} />}
      <aside className={`sidebar ${open ? 'is-open' : ''}`}>
        <div className="brand-row">
          <div className="brand-mark"><Network size={22} /></div>
          <div><strong>EdgeOps</strong><span>Control Plane</span></div>
          <button className="icon-button mobile-only" aria-label="Close menu" onClick={close}><X size={20} /></button>
        </div>
        <nav aria-label="Primary navigation">
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink key={to} to={to} onClick={close} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              <Icon size={18} /><span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <span className="live-dot" />
          <div><strong>Global network</strong><small>All systems monitored</small></div>
        </div>
      </aside>
    </>
  );
}