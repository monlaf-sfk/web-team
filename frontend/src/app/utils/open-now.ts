export function isCafeOpenNow(opensAt: string, closesAt: string): boolean {
  const now = new Date();
  const current = now.getHours() * 60 + now.getMinutes();
  const opens = toMinutes(opensAt);
  const closes = toMinutes(closesAt);
  if (opens <= closes) {
    return current >= opens && current <= closes;
  }
  return current >= opens || current <= closes;
}

function toMinutes(time: string): number {
  const [h, m] = time.split(':').map(Number);
  return h * 60 + (m || 0);
}
