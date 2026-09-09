export const formatPercent = (value, digits = 1) => `${Number(value).toFixed(digits)}%`;
export const formatNumber = (value) => new Intl.NumberFormat('en-US', { notation: value > 999999 ? 'compact' : 'standard', maximumFractionDigits: 1 }).format(value);
export const formatLatency = (value) => `${Math.round(value)} ms`;
export const formatDateTime = (value) => new Intl.DateTimeFormat('en-GB', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value));
export const clamp = (value, min, max) => Math.min(Math.max(value, min), max);