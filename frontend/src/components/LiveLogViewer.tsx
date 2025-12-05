import React, { useRef, useEffect } from 'react';
import type { LogEntry } from '../utils/types';
import { formatTimestamp, capitalizeDistrict, formatNumber } from '../utils/constants';

interface LiveLogViewerProps {
    logs: LogEntry[];
    onClear: () => void;
}

export const LiveLogViewer: React.FC<LiveLogViewerProps> = ({ logs, onClear }) => {
    const scrollRef = useRef<HTMLDivElement>(null);
    const [autoScroll, setAutoScroll] = React.useState(true);

    useEffect(() => {
        if (autoScroll && scrollRef.current) {
            scrollRef.current.scrollTop = 0;
        }
    }, [logs, autoScroll]);

    const handleScroll = () => {
        if (scrollRef.current) {
            const { scrollTop } = scrollRef.current;
            setAutoScroll(scrollTop < 50);
        }
    };

    return (
        <div className="glass rounded-xl overflow-hidden">
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-700/50">
                <div className="flex items-center gap-2">
                    <span className="text-lg">📋</span>
                    <h3 className="font-semibold text-white">Live Log</h3>
                    <span className="text-xs text-gray-500 bg-gray-700/50 px-2 py-0.5 rounded-full">
                        {logs.length} entries
                    </span>
                </div>
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => setAutoScroll(!autoScroll)}
                        className={`text-xs px-2 py-1 rounded transition-colors ${autoScroll
                            ? 'bg-blue-600/20 text-blue-400'
                            : 'bg-gray-700/50 text-gray-400 hover:text-white'
                            }`}
                    >
                        {autoScroll ? '⏸ Auto-scroll ON' : '▶ Auto-scroll OFF'}
                    </button>
                    <button
                        onClick={onClear}
                        className="text-xs px-2 py-1 rounded bg-gray-700/50 text-gray-400 hover:text-white hover:bg-gray-600/50 transition-colors"
                    >
                        Clear
                    </button>
                </div>
            </div>

            {/* Log Entries */}
            <div
                ref={scrollRef}
                onScroll={handleScroll}
                className="log-container"
            >
                {logs.length === 0 ? (
                    <div className="p-8 text-center text-gray-500">
                        <div className="text-3xl mb-2">📭</div>
                        <div>No log entries yet</div>
                    </div>
                ) : (
                    logs.map((entry) => (
                        <div
                            key={entry.id}
                            className={`log-entry ${entry.outbreak ? 'log-entry-outbreak' : ''}`}
                        >
                            <div className="flex items-center justify-between gap-4">
                                <div className="flex items-center gap-3 min-w-0">
                                    <span className="text-gray-500 text-xs whitespace-nowrap">
                                        {formatTimestamp(entry.timestamp)}
                                    </span>
                                    <span
                                        className={`font-medium truncate ${entry.outbreak ? 'text-red-400' : 'text-gray-300'
                                            }`}
                                    >
                                        {capitalizeDistrict(entry.district)}
                                    </span>
                                </div>
                                <div className="flex items-center gap-3 flex-shrink-0">
                                    <span
                                        className={`font-mono font-bold ${entry.outbreak ? 'text-red-400' : 'text-blue-400'
                                            }`}
                                    >
                                        {entry.cases} cases
                                    </span>
                                    <span
                                        className={`text-xs px-2 py-0.5 rounded ${entry.probability >= 0.6
                                            ? 'bg-red-600/20 text-red-400'
                                            : entry.probability >= 0.4
                                                ? 'bg-yellow-600/20 text-yellow-400'
                                                : 'bg-green-600/20 text-green-400'
                                            }`}
                                    >
                                        {formatNumber(entry.probability * 100, 0)}%
                                    </span>
                                    {entry.outbreak && (
                                        <span className="text-xs text-red-400 animate-pulse">
                                            ⚠️
                                        </span>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};
