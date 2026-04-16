import { getDb } from '../lib/database';
import { getSetting } from '../lib/database';

const API_BASE = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';

async function getToken(): Promise<string | null> {
  return getSetting('auth_token');
}

async function apiFetch(path: string, options: RequestInit = {}): Promise<Response> {
  const token = await getToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return fetch(`${API_BASE}${path}`, { ...options, headers });
}

export async function syncBatch(deviceId: string, records: unknown[]): Promise<{
  processed: number;
  synced: number;
  results: { clientId: string; status: string; reason?: string }[];
}> {
  const res = await apiFetch('/sync', {
    method: 'POST',
    body: JSON.stringify({ deviceId, records }),
  });
  if (!res.ok) throw new Error(`Sync failed: ${res.status}`);
  return res.json();
}

export async function fetchFacilities() {
  const res = await apiFetch('/facilities');
  if (!res.ok) throw new Error('Failed to fetch facilities');
  return res.json();
}

export async function postAlert(alertData: unknown) {
  const res = await apiFetch('/alerts', {
    method: 'POST',
    body: JSON.stringify(alertData),
  });
  if (!res.ok) throw new Error('Failed to post alert');
  return res.json();
}

export async function login(workerId: string, password: string) {
  const res = await apiFetch('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ workerId, password }),
  });
  if (!res.ok) throw new Error('Login failed');
  return res.json();
}
