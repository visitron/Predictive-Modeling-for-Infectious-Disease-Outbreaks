/**
 * Application constants
 */

// WebSocket configuration
export const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8001/ws';
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

// Outbreak thresholds
export const OUTBREAK_PROB_THRESHOLD = 0.6;
export const OUTBREAK_CASE_THRESHOLD = 10;

// UI configuration
export const MAX_LOG_ENTRIES = 100;
export const TOAST_AUTO_DISMISS_MS = 5000;
export const RECONNECT_DELAY_MS = 3000;

// Probability bar colors
export const getProbabilityColor = (prob: number): string => {
    if (prob >= 0.8) return '#dc2626'; // Red
    if (prob >= 0.6) return '#f59e0b'; // Orange/warning
    if (prob >= 0.4) return '#eab308'; // Yellow
    return '#10b981'; // Green
};

// Format helpers
export const formatNumber = (num: number, decimals = 2): string => {
    return num.toLocaleString('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
    });
};

export const formatTimestamp = (isoString: string): string => {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
    });
};

export const formatDate = (isoString: string): string => {
    const date = new Date(isoString);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
    });
};

export const capitalizeDistrict = (district: string): string => {
    return district
        .split('_')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
};

// Generate unique IDs
export const generateId = (): string => {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};
