import { Bell, ChevronRight, Menu, Search, UserRound, X } from 'lucide-react';
import { useEffect, useMemo, useRef, useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { useApiQuery } from '../hooks/useApiQuery';
import { useUIStore } from '../store/uiStore';

function useOutsideClose(ref, close) {
  useEffect(() => {
    const handler = (event) => {
      if (ref.current && !ref.current.contains(event.target)) close();
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [ref, close]);
}

export default function Topbar() {
  const toggle = useUIStore((s) => s.toggleSidebar);
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [query, setQuery] = useState('');
  const [debounced, setDebounced] = useState('');
  const [panel, setPanel] = useState(null);
  const rootRef = useRef(null);

  useOutsideClose(rootRef, () => setPanel(null));

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(query.trim()), 250);
    return () => clearTimeout(timer);
  }, [query]);

  const searchQuery = useApiQuery(['search', debounced], () => api.search(debounced), {
    enabled: debounced.length >= 2,
    staleTime: 10_000,
  });
  const notifications = useApiQuery(['notifications'], api.getNotifications, { refetchInterval: 30_000 });
  const profile = useApiQuery(['profile'], api.getProfile, { staleTime: 300_000 });
  const markRead = useMutation({
    mutationFn: api.markNotificationsRead,
    onSuccess: (data) => queryClient.setQueryData(['notifications'], data),
  });

  const results = useMemo(() => {
    const data = searchQuery.data;
    if (!data) return [];
    return [...data.nodes, ...data.incidents, ...data.regions];
  }, [searchQuery.data]);

  const unread = (notifications.data || []).filter((item) => !item.is_read).length;
  const goTo = (path) => {
    navigate(path);
    setPanel(null);
    setQuery('');
  };

  return (
    <header className="topbar" ref={rootRef}>
      <button className="icon-button mobile-only" onClick={toggle} aria-label="Open navigation"><Menu size={20} /></button>

      <div className="topbar-search-wrap">
        <div className="search-box">
          <Search size={17} />
          <input
            aria-label="Search"
            value={query}
            onFocus={() => setPanel('search')}
            onChange={(event) => { setQuery(event.target.value); setPanel('search'); }}
            placeholder="Search nodes, incidents, regions…"
          />
          {query && <button className="search-clear" onClick={() => setQuery('')} aria-label="Clear search"><X size={14} /></button>}
        </div>
        {panel === 'search' && query.length > 0 && (
          <div className="topbar-popover search-popover">
            {query.trim().length < 2 ? <p className="popover-empty">Type at least 2 characters.</p> : searchQuery.isLoading ? <p className="popover-empty">Searching…</p> : results.length === 0 ? <p className="popover-empty">No matching nodes, incidents or regions.</p> : (
              <div className="search-results">
                {results.map((item) => (
                  <button key={`${item.type}-${item.id}`} className="search-result" onClick={() => goTo(item.path)}>
                    <span className={`result-type result-${item.type}`}>{item.type}</span>
                    <span className="result-copy">
                      <strong>{item.hostname || item.title || item.name}</strong>
                      <small>{item.region || item.code || item.status}</small>
                    </span>
                    <ChevronRight size={15} />
                  </button>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      <div className="topbar-actions">
        <div className="topbar-control-wrap">
          <button className="icon-button" aria-label="Notifications" onClick={() => setPanel(panel === 'notifications' ? null : 'notifications')}>
            <Bell size={19} />
            {unread > 0 && <span className="notification-dot" />}
          </button>
          {panel === 'notifications' && (
            <div className="topbar-popover notifications-popover">
              <div className="popover-header">
                <div><strong>Notifications</strong><span>{unread} unread</span></div>
                {unread > 0 && <button className="text-button" onClick={() => markRead.mutate()}>Mark all read</button>}
              </div>
              <div className="notification-list">
                {(notifications.data || []).map((item) => (
                  <button key={item.id} className={`notification-item ${item.is_read ? 'is-read' : ''}`} onClick={() => goTo(item.target_path)}>
                    <span className={`notification-level level-${item.level}`} />
                    <span><strong>{item.title}</strong><small>{item.message}</small></span>
                  </button>
                ))}
                {!notifications.isLoading && (notifications.data || []).length === 0 && <p className="popover-empty">No notifications.</p>}
              </div>
            </div>
          )}
        </div>

        <div className="topbar-control-wrap">
          <button className="profile profile-button" onClick={() => setPanel(panel === 'profile' ? null : 'profile')} aria-label="Open profile menu">
            <div className="avatar">{profile.data?.initials || 'AP'}</div>
            <div className="profile-copy"><strong>{profile.data?.name || 'Andrej Pecirep'}</strong><span>{profile.data?.role || 'Platform Engineer'}</span></div>
          </button>
          {panel === 'profile' && (
            <div className="topbar-popover profile-popover">
              <div className="profile-card-head"><div className="avatar avatar-large">{profile.data?.initials || 'AP'}</div><div><strong>{profile.data?.name}</strong><span>{profile.data?.role}</span></div></div>
              <div className="profile-details">
                <span><UserRound size={14}/> {profile.data?.email}</span>
                <span>{profile.data?.location}</span>
                <span>{profile.data?.timezone}</span>
              </div>
              <div className="profile-status"><span className="live-dot"/><strong>{profile.data?.status || 'Available'}</strong></div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
