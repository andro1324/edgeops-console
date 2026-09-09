const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export class ApiError extends Error {
  constructor(message, status, details = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.details = details;
  }
}

export async function request(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeout ?? 8000);
  try {
    const response = await fetch(`${BASE_URL}${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', Accept: 'application/json', ...options.headers },
      signal: controller.signal,
    });
    if (!response.ok) {
      let details = null;
      try { details = await response.json(); } catch { details = null; }
      throw new ApiError(details?.detail || `HTTP ${response.status}`, response.status, details);
    }
    if (response.status === 204) return null;
    return response.json();
  } catch (error) {
    if (error.name === 'AbortError') throw new ApiError('Request timed out', 408);
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

export const api = {
  getOverview: () => request('/overview'),
  getNodes: () => request('/nodes'),
  getTraffic: () => request('/traffic'),
  getIncidents: () => request('/incidents'),
  createIncident: (payload) => request('/incidents', { method: 'POST', body: JSON.stringify(payload) }),
  resolveIncident: (id) => request(`/incidents/${id}/resolve`, { method: 'PATCH' }),
};