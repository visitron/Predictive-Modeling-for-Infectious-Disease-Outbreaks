import React, { useEffect } from 'react';
import type { Toast } from '../utils/types';
import { TOAST_AUTO_DISMISS_MS, capitalizeDistrict } from '../utils/constants';

interface NotificationSystemProps {
    toasts: Toast[];
    onDismiss: (id: string) => void;
}

export const NotificationSystem: React.FC<NotificationSystemProps> = ({
    toasts,
    onDismiss,
}) => {
    return (
        <div className="toast-container">
            {toasts.map((toast) => (
                <ToastItem key={toast.id} toast={toast} onDismiss={onDismiss} />
            ))}
        </div>
    );
};

interface ToastItemProps {
    toast: Toast;
    onDismiss: (id: string) => void;
}

const ToastItem: React.FC<ToastItemProps> = ({ toast, onDismiss }) => {
    useEffect(() => {
        const timer = setTimeout(() => {
            onDismiss(toast.id);
        }, TOAST_AUTO_DISMISS_MS);

        return () => clearTimeout(timer);
    }, [toast.id, onDismiss]);

    return (
        <div
            className={`toast ${toast.type === 'danger'
                ? 'toast-danger'
                : toast.type === 'warning'
                    ? 'toast-warning'
                    : 'glass'
                }`}
        >
            {/* Icon */}
            <div className="flex-shrink-0 text-2xl">
                {toast.type === 'danger' ? '🚨' : toast.type === 'warning' ? '⚠️' : 'ℹ️'}
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0">
                <div className="font-semibold text-white">{toast.title}</div>
                <div className="text-sm text-white/80 truncate">{toast.message}</div>
                {toast.district && (
                    <div className="text-xs text-white/60 mt-1">
                        District: {capitalizeDistrict(toast.district)}
                    </div>
                )}
            </div>

            {/* Dismiss Button */}
            <button
                onClick={() => onDismiss(toast.id)}
                className="flex-shrink-0 ml-2 p-1 rounded-full hover:bg-white/10 transition-colors"
                aria-label="Dismiss notification"
            >
                <svg
                    className="w-5 h-5 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                    />
                </svg>
            </button>

            {/* Progress Bar */}
            <div className="absolute bottom-0 left-0 right-0 h-1 bg-white/20 rounded-b-xl overflow-hidden">
                <div
                    className="h-full bg-white/40 animate-[shrink_5s_linear_forwards]"
                    style={{
                        animation: `shrink ${TOAST_AUTO_DISMISS_MS}ms linear forwards`,
                    }}
                />
            </div>
        </div>
    );
};

// Add keyframes for shrink animation
const style = document.createElement('style');
style.textContent = `
  @keyframes shrink {
    from { width: 100%; }
    to { width: 0%; }
  }
`;
document.head.appendChild(style);
