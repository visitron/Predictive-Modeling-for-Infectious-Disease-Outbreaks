import React from 'react';
import type { Prediction, ConnectionStatus } from '../utils/types';
import { DistrictCard } from './DistrictCard';
import { formatTimestamp, formatDate } from '../utils/constants';

interface DashboardProps {
    predictions: Map<string, Prediction>;
    connectionStatus: ConnectionStatus;
    lastUpdate: string | null;
}

export const Dashboard: React.FC<DashboardProps> = ({
    predictions,
    connectionStatus,
    lastUpdate,
}) => {
    const sortedPredictions = Array.from(predictions.values()).sort((a, b) => {
        // Sort by outbreak flag first, then by probability
        if (a.outbreak_flag !== b.outbreak_flag) {
            return a.outbreak_flag ? -1 : 1;
        }
        return b.outbreak_prob - a.outbreak_prob;
    });

    const outbreakCount = sortedPredictions.filter((p) => p.outbreak_flag).length;

    return (
        <div className="flex-1 overflow-auto">
            {/* Header */}
            <header className="glass sticky top-0 z-10 px-6 py-4 mb-6">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                    <div>
                        <h1 className="text-2xl md:text-3xl font-bold text-white flex items-center gap-3">
                            <span className="text-3xl">🦠</span>
                            Outbreak Prediction Dashboard
                        </h1>
                        <p className="text-gray-400 text-sm mt-1">
                            Real-time disease outbreak monitoring system
                        </p>
                    </div>

                    <div className="flex items-center gap-6">
                        {/* Connection Status */}
                        <div className="flex items-center gap-2">
                            <span
                                className={`status-dot ${connectionStatus === 'connected'
                                    ? 'status-dot-connected'
                                    : connectionStatus === 'connecting'
                                        ? 'status-dot-connecting'
                                        : 'status-dot-disconnected'
                                    }`}
                            />
                            <span
                                className={`text-sm font-medium ${connectionStatus === 'connected'
                                    ? 'status-connected'
                                    : connectionStatus === 'connecting'
                                        ? 'status-connecting'
                                        : 'status-disconnected'
                                    }`}
                            >
                                {connectionStatus === 'connected'
                                    ? 'Connected'
                                    : connectionStatus === 'connecting'
                                        ? 'Connecting...'
                                        : 'Disconnected'}
                            </span>
                        </div>

                        {/* Last Update */}
                        {lastUpdate && (
                            <div className="text-right">
                                <div className="text-xs text-gray-500">Last Update</div>
                                <div className="text-sm text-gray-300">
                                    {formatTimestamp(lastUpdate)}
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Stats Bar */}
                <div className="flex flex-wrap items-center gap-4 mt-4 pt-4 border-t border-gray-700/50">
                    <div className="flex items-center gap-2">
                        <span className="text-gray-400 text-sm">Districts:</span>
                        <span className="text-white font-semibold">{predictions.size}</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <span className="text-gray-400 text-sm">Active Outbreaks:</span>
                        <span
                            className={`font-semibold ${outbreakCount > 0 ? 'text-red-400' : 'text-green-400'
                                }`}
                        >
                            {outbreakCount}
                        </span>
                    </div>
                    {lastUpdate && (
                        <div className="flex items-center gap-2">
                            <span className="text-gray-400 text-sm">Date:</span>
                            <span className="text-white">{formatDate(lastUpdate)}</span>
                        </div>
                    )}
                </div>
            </header>

            {/* Cards Grid */}
            {predictions.size === 0 ? (
                <div className="flex flex-col items-center justify-center py-20">
                    <div className="text-6xl mb-4">📡</div>
                    <h2 className="text-xl font-semibold text-gray-300 mb-2">
                        Waiting for Data
                    </h2>
                    <p className="text-gray-500 text-center max-w-md">
                        {connectionStatus === 'connected'
                            ? 'Connected to server. Predictions will appear shortly...'
                            : connectionStatus === 'connecting'
                                ? 'Establishing connection to the prediction server...'
                                : 'Unable to connect. Please ensure the backend server is running.'}
                    </p>
                </div>
            ) : (
                <div className="dashboard-grid">
                    {sortedPredictions.map((prediction) => (
                        <DistrictCard key={prediction.district} prediction={prediction} />
                    ))}
                </div>
            )}
        </div>
    );
};
