import { useState } from 'react';
import { useWebSocket } from './hooks';
import { Dashboard, NotificationSystem, LiveLogViewer } from './components';
import './index.css';

function App() {
  const {
    connectionStatus,
    predictions,
    logs,
    toasts,
    lastUpdate,
    dismissToast,
    clearLogs,
  } = useWebSocket();

  const [showLogs, setShowLogs] = useState(true);

  return (
    <div className="min-h-screen flex flex-col">
      {/* Notification System */}
      <NotificationSystem toasts={toasts} onDismiss={dismissToast} />

      {/* Main Content */}
      <div className="flex flex-col lg:flex-row flex-1 gap-0">
        {/* Dashboard Section */}
        <div className="flex-1 flex flex-col min-w-0">
          <Dashboard
            predictions={predictions}
            connectionStatus={connectionStatus}
            lastUpdate={lastUpdate}
          />
        </div>

        {/* Log Viewer Sidebar */}
        <div
          className={`lg:w-96 flex-shrink-0 border-t lg:border-t-0 lg:border-l border-gray-700/50 transition-all ${showLogs ? 'block' : 'hidden lg:block'
            }`}
        >
          <div className="p-4 h-full">
            <LiveLogViewer logs={logs} onClear={clearLogs} />
          </div>
        </div>
      </div>

      {/* Mobile Log Toggle */}
      <button
        onClick={() => setShowLogs(!showLogs)}
        className="lg:hidden fixed bottom-4 right-4 z-50 bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full shadow-lg transition-colors"
        aria-label="Toggle logs"
      >
        <svg
          className="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d={
              showLogs
                ? 'M6 18L18 6M6 6l12 12'
                : 'M4 6h16M4 12h16M4 18h16'
            }
          />
        </svg>
      </button>

      {/* Footer */}
      <footer className="glass py-3 px-6 text-center text-xs text-gray-500 border-t border-gray-700/50">
        <div className="flex flex-col sm:flex-row items-center justify-center gap-2 sm:gap-4">
          <span>Outbreak Prediction System v1.0.0</span>
          <span className="hidden sm:inline">•</span>
          <span>
            Powered by XGBoost &amp; FastAPI
          </span>
          <span className="hidden sm:inline">•</span>
          <span className="flex items-center gap-1">
            <span
              className={`status-dot ${connectionStatus === 'connected'
                  ? 'status-dot-connected'
                  : 'status-dot-disconnected'
                }`}
              style={{ width: '6px', height: '6px' }}
            />
            WebSocket {connectionStatus}
          </span>
        </div>
      </footer>
    </div>
  );
}

export default App;
