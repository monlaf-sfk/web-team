import { HttpErrorResponse } from '@angular/common/http';

export function extractErrors(err: HttpErrorResponse): Record<string, string> {
  if (err.status === 401) {
    return { detail: 'You are not logged in.' };
  }
  if (err.status === 0) {
    return { detail: 'Network error. Is the server running?' };
  }
  const body = err.error;
  if (!body) {
    return { detail: `Request failed (HTTP ${err.status}).` };
  }
  if (typeof body === 'string') {
    return { detail: body };
  }
  const out: Record<string, string> = {};
  for (const key of Object.keys(body)) {
    const value = body[key];
    out[key] = Array.isArray(value) ? String(value[0]) : String(value);
  }
  return out;
}
