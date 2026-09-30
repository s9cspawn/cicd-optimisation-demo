export function formatDuration(seconds) {
  if (!Number.isFinite(seconds) || seconds <= 0) return 'Pending';

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.round(seconds % 60);
  return `${minutes}m ${remainingSeconds}s`;
}

export function percentageChange(before, after) {
  if (!Number.isFinite(before) || !Number.isFinite(after) || before <= 0) return 'Pending';

  const change = ((after - before) / before) * 100;
  return `${change > 0 ? '+' : ''}${change.toFixed(1)}%`;
}

export function statusLabel(runCount) {
  if (runCount >= 5) return 'Sample complete';
  if (runCount > 0) return `${5 - runCount} runs remaining`;
  return 'Awaiting benchmark';
}

