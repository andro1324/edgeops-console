import { describe, expect, it } from 'vitest';
import { clamp, formatLatency, formatPercent } from './format';

describe('format utilities', () => {
  it('formats percentages and latency values', () => {
    expect(formatPercent(99.987, 2)).toBe('99.99%');
    expect(formatLatency(83.6)).toBe('84 ms');
  });

  it('clamps values to a safe range', () => {
    expect(clamp(120, 0, 100)).toBe(100);
    expect(clamp(-5, 0, 100)).toBe(0);
  });
});
