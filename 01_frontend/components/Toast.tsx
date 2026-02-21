"use client";

import { useState, useEffect, useCallback, createContext, useContext } from "react";

type ToastType = "success" | "error" | "info";

interface ToastItem {
    id: string;
    message: string;
    type: ToastType;
}

interface ToastContextValue {
    showToast: (message: string, type?: ToastType) => void;
}

const ToastContext = createContext<ToastContextValue>({
    showToast: () => {},
});

export function useToast() {
    return useContext(ToastContext);
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
    const [toasts, setToasts] = useState<ToastItem[]>([]);

    const showToast = useCallback((message: string, type: ToastType = "info") => {
        const id = `toast-${Date.now()}`;
        setToasts((prev) => [...prev, { id, message, type }]);
    }, []);

    const removeToast = useCallback((id: string) => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
    }, []);

    return (
        <ToastContext.Provider value={{ showToast }}>
            {children}
            {/* Toast container */}
            <div className="fixed top-4 right-4 z-[200] flex flex-col gap-2 pointer-events-none">
                {toasts.map((toast) => (
                    <ToastMessage key={toast.id} toast={toast} onDismiss={removeToast} />
                ))}
            </div>
        </ToastContext.Provider>
    );
}

function ToastMessage({ toast, onDismiss }: { toast: ToastItem; onDismiss: (id: string) => void }) {
    useEffect(() => {
        const timer = setTimeout(() => onDismiss(toast.id), 4000);
        return () => clearTimeout(timer);
    }, [toast.id, onDismiss]);

    const colors = {
        success: "bg-emerald-50 border-emerald-200 text-emerald-800",
        error: "bg-red-50 border-red-200 text-red-800",
        info: "bg-cyan-50 border-cyan-200 text-cyan-800",
    };

    const icons = {
        success: (
            <svg className="w-4 h-4 text-emerald-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
        ),
        error: (
            <svg className="w-4 h-4 text-red-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
        ),
        info: (
            <svg className="w-4 h-4 text-cyan-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        ),
    };

    return (
        <div
            className={`pointer-events-auto flex items-center gap-2 rounded-xl border px-4 py-3 shadow-lg text-sm font-medium animate-slide-right ${colors[toast.type]}`}
            role="alert"
        >
            {icons[toast.type]}
            <span>{toast.message}</span>
            <button
                onClick={() => onDismiss(toast.id)}
                className="ml-2 opacity-50 hover:opacity-100 transition-opacity"
                aria-label="Dismiss"
            >
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
    );
}
