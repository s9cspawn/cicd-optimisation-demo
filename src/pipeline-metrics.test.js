import { describe, expect, it } from 'vitest';
import { formatDuration, percentageChange, statusLabel } from './pipeline-metrics.js';

describe('formatDuration', () => {
  it('formats a measured duration as minutes and seconds', () => {
    expect(formatDuration(125.4)).toBe('2m 5s');
  });

  it.each([0, -1, Number.NaN, Number.POSITIVE_INFINITY])(
    'returns Pending for an unavailable duration (%s)',
    (duration) => {
      expect(formatDuration(duration)).toBe('Pending');
    },
  );
});

describe('percentageChange', () => {
  it('reports a reduction as a negative percentage', () => {
    expect(percentageChange(100, 72)).toBe('-28.0%');
  });

  it('reports an increase with an explicit positive sign', () => {
    expect(percentageChange(100, 110)).toBe('+10.0%');
  });

  it('does not calculate a percentage without a valid baseline', () => {
    expect(percentageChange(0, 20)).toBe('Pending');
  });
});

describe('statusLabel', () => {
  it('tracks remaining benchmark runs', () => {
    expect(statusLabel(2)).toBe('3 runs remaining');
  });

  it('marks a five-run sample as complete', () => {
    expect(statusLabel(5)).toBe('Sample complete');
  });

  it('marks an untouched benchmark as awaiting data', () => {
    expect(statusLabel(0)).toBe('Awaiting benchmark');
  });
});
