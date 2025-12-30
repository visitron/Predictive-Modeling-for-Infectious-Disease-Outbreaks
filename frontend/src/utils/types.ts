/**
 * Type definitions for the Outbreak Prediction System
 */

export interface Prediction {
    ts: string;
    district: string;
    disease: string;
    predicted_log: number;
    predicted_cases: number;
    predicted_cases_rounded: number;
    outbreak_prob: number;
    outbreak_flag: boolean;
    input_features: Record<string, number>;
    model_version: string;
}

export interface BatchPrediction {
    type: 'batch_prediction';
    items: Prediction[];
}

export interface ConnectionMessage {
    type: 'connection_established';
    message: string;
    refresh_interval: number;
}

export interface PongMessage {
    type: 'pong';
}

export type WebSocketMessage = BatchPrediction | ConnectionMessage | PongMessage;

export interface Metadata {
    feature_list: string[];
    model_version: string;
    refresh_interval: number;
    model_loaded: boolean;
    districts: string[];
    active_connections: number;
}

export interface LogEntry {
    id: string;
    timestamp: string;
    district: string;
    cases: number;
    outbreak: boolean;
    probability: number;
}

export interface Toast {
    id: string;
    type: 'danger' | 'warning' | 'info';
    title: string;
    message: string;
    district?: string;
}

export type ConnectionStatus = 'connected' | 'disconnected' | 'connecting';
