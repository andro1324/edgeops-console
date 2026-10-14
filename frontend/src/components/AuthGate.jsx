import { useEffect, useState } from 'react';
import { api } from '../api/client';

export default function AuthGate({ children }) {
  const [mode, setMode] = useState('checking');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let active = true;
    fetch(`${import.meta.env.VITE_API_BASE_URL || '/api'}/auth/status`)
      .then((response) => response.json())
      .then((data) => { if (active) setMode(data.enabled ? (localStorage.getItem('edgeops_token') ? 'app' : 'login') : 'app'); })
      .catch(() => { if (active) setMode('app'); });
    return () => { active = false; };
  }, []);

  async function submit(event) {
    event.preventDefault(); setBusy(true); setError('');
    try { const result = await api.login(username, password); localStorage.setItem('edgeops_token', result.access_token); setMode('app'); }
    catch (err) { setError(err.message || 'Sign-in failed'); }
    finally { setBusy(false); }
  }

  if (mode === 'checking') return <div className="auth-screen"><p>Checking authentication configuration…</p></div>;
  if (mode === 'login') return (
    <main className="auth-screen"><form className="auth-card" onSubmit={submit}>
      <div className="brand-mark auth-mark">EO</div><p className="eyebrow">EDGEOPS CONSOLE</p><h1>Sign in</h1><p className="auth-description">Use the administrator credentials configured for this deployment.</p>
      <label>Username<input autoComplete="username" value={username} onChange={(e) => setUsername(e.target.value)} required /></label>
      <label>Password<input type="password" autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} required /></label>
      {error && <p className="form-error" role="alert">{error}</p>}<button className="primary-button" type="submit" disabled={busy}>{busy ? 'Signing in…' : 'Sign in'}</button>
    </form></main>
  );
  return children;
}
