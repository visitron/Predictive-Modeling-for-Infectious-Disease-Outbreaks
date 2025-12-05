import React from 'react';
import type { Prediction } from '../utils/types';
import {
    capitalizeDistrict,
    formatTimestamp,
    formatNumber,
    getProbabilityColor,
} from '../utils/constants';

interface DistrictCardProps {
    prediction: Prediction;
}

export const DistrictCard: React.FC<DistrictCardProps> = ({ prediction }) => {
    const {
        district,
        predicted_cases_rounded,
        outbreak_prob,
        outbreak_flag,
        ts,
        predicted_log,
    } = prediction;

    const probColor = getProbabilityColor(outbreak_prob);
    const probPercent = (outbreak_prob * 100).toFixed(0);

    return (
        <div
            className={`card p-6 animate-fade-in ${outbreak_flag ? 'card-outbreak' : ''
                }`}
        >
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">
                    {capitalizeDistrict(district)}
                </h3>
                {outbreak_flag && (
                    <span className="px-3 py-1 text-xs font-bold text-white bg-red-600 rounded-full animate-pulse">
                        OUTBREAK
                    </span>
                )}
            </div>

            {/* Predicted Cases */}
            <div className="mb-4">
                <div className="text-sm text-gray-400 mb-1">Predicted Cases</div>
                <div className="flex items-baseline gap-2">
                    <span
                        className={`text-4xl font-bold ${outbreak_flag ? 'text-red-400' : 'text-blue-400'
                            }`}
                    >
                        {predicted_cases_rounded}
                    </span>
                    <span className="text-sm text-gray-500">
                        (log: {formatNumber(predicted_log, 3)})
                    </span>
                </div>
            </div>

            {/* Outbreak Probability */}
            <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-400">Outbreak Probability</span>
                    <span
                        className="text-sm font-semibold"
                        style={{ color: probColor }}
                    >
                        {probPercent}%
                    </span>
                </div>
                <div className="prob-bar">
                    <div
                        className="prob-bar-fill"
                        style={{
                            width: `${Math.min(outbreak_prob * 100, 100)}%`,
                            backgroundColor: probColor,
                        }}
                    />
                </div>
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-700">
                <span className="text-xs text-gray-500">Last updated</span>
                <span className="text-xs text-gray-400">{formatTimestamp(ts)}</span>
            </div>
        </div>
    );
};
