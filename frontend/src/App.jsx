import { Navigate, Route, Routes } from 'react-router-dom';
import AppShell from './components/AppShell';
import DashboardPage from './features/dashboard/DashboardPage';
import InfrastructurePage from './features/infrastructure/InfrastructurePage';
import IncidentsPage from './features/incidents/IncidentsPage';
import AuthGate from './components/AuthGate';
import TrafficPage from './features/traffic/TrafficPage';

export default function App() {
  return (
    <AuthGate><Routes>
      <Route element={<AppShell />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/infrastructure" element={<InfrastructurePage />} />
        <Route path="/traffic" element={<TrafficPage />} />
        <Route path="/incidents" element={<IncidentsPage />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Route>
    </Routes></AuthGate>
  );
}