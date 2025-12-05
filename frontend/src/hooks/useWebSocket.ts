import { useEffect, useRef, useState, useCallback } from 'react';
import type {
    Prediction,
    WebSocketMessage,
    ConnectionStatus,
    LogEntry,
    Toast,
} from '../utils/types';
import {
    WS_URL,
    RECONNECT_DELAY_MS,
    OUTBREAK_PROB_THRESHOLD,
    generateId,
} from '../utils/constants';

interface UseWebSocketReturn {
    connectionStatus: ConnectionStatus;
    predictions: Map<string, Prediction>;
    logs: LogEntry[];
    toasts: Toast[];
    lastUpdate: string | null;
    dismissToast: (id: string) => void;
    clearLogs: () => void;
}

export function useWebSocket(): UseWebSocketReturn {
    const wsRef = useRef<WebSocket | null>(null);
    const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('disconnected');
    const [predictions, setPredictions] = useState<Map<string, Prediction>>(new Map());
    const [logs, setLogs] = useState<LogEntry[]>([]);
    const [toasts, setToasts] = useState<Toast[]>([]);
    const [lastUpdate, setLastUpdate] = useState<string | null>(null);

    const dismissToast = useCallback((id: string) => {
        setToasts((prev) => prev.filter((toast) => toast.id !== id));
    }, []);

    const clearLogs = useCallback(() => {
        setLogs([]);
    }, []);

    const addToast = useCallback((toast: Omit<Toast, 'id'>) => {
        const newToast: Toast = { ...toast, id: generateId() };
        setToasts((prev) => [...prev.slice(-4), newToast]); // Keep max 5 toasts
    }, []);

    const addLogEntry = useCallback((prediction: Prediction) => {
        const logEntry: LogEntry = {
            id: generateId(),
            timestamp: prediction.ts,
            district: prediction.district,
            cases: prediction.predicted_cases_rounded,
            outbreak: prediction.outbreak_flag,
            probability: prediction.outbreak_prob,
        };
        setLogs((prev) => [logEntry, ...prev].slice(0, 100)); // Keep last 100 entries
    }, []);

    const handlePredictions = useCallback(
        (items: Prediction[]) => {
            setPredictions((prev) => {
                const newMap = new Map(prev);
                items.forEach((prediction) => {
                    newMap.set(prediction.district, prediction);
                    addLogEntry(prediction);

                    // Trigger toast for outbreaks
                    if (prediction.outbreak_flag || prediction.outbreak_prob > OUTBREAK_PROB_THRESHOLD) {
                        addToast({
                            type: 'danger',
                            title: '🚨 Outbreak Alert',
                            message: `${prediction.district.toUpperCase()}: ${prediction.predicted_cases_rounded} predicted cases (${(prediction.outbreak_prob * 100).toFixed(0)}% probability)`,
                            district: prediction.district,
                        });
                    }
                });
                return newMap;
            });

            if (items.length > 0) {
                setLastUpdate(items[0].ts);
            }
        },
        [addLogEntry, addToast]
    );

    const connect = useCallback(() => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            return;
        }

        setConnectionStatus('connecting');

        try {
            const ws = new WebSocket(WS_URL);

            ws.onopen = () => {
                console.log('WebSocket connected');
                setConnectionStatus('connected');
            };

            ws.onmessage = (event) => {
                try {
                    const message: WebSocketMessage = JSON.parse(event.data);

                    switch (message.type) {
                        case 'batch_prediction':
                            handlePredictions(message.items);
                            break;
                        case 'connection_established':
                            console.log('Connection established:', message.message);
                            break;
                        case 'pong':
                            console.log('Pong received');
                            break;
                        default:
                            console.log('Unknown message type:', message);
                    }
                } catch (error) {
                    console.error('Failed to parse WebSocket message:', error);
                }
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            ws.onclose = () => {
                console.log('WebSocket disconnected');
                setConnectionStatus('disconnected');
                wsRef.current = null;

                // Auto-reconnect
                reconnectTimeoutRef.current = setTimeout(() => {
                    console.log('Attempting to reconnect...');
                    connect();
                }, RECONNECT_DELAY_MS);
            };

            wsRef.current = ws;
        } catch (error) {
            console.error('Failed to create WebSocket:', error);
            setConnectionStatus('disconnected');
        }
    }, [handlePredictions]);

    useEffect(() => {
        connect();

        return () => {
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
            }
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, [connect]);

    return {
        connectionStatus,
        predictions,
        logs,
        toasts,
        lastUpdate,
        dismissToast,
        clearLogs,
    };
}
