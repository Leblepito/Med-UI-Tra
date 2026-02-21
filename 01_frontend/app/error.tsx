"use client";

import { useEffect } from "react";

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    useEffect(() => {
        console.error("Global error:", error);
    }, [error]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-white px-4">
            <div className="max-w-md text-center animate-fade-up">
                <div className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-red-50 flex items-center justify-center">
                    <svg className="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                </div>
                <h1 className="font-display text-2xl font-bold text-slate-800 mb-2">Something went wrong</h1>
                <p className="text-slate-500 text-sm mb-6 leading-relaxed">
                    An unexpected error occurred. Please try again or contact our support team if the issue persists.
                </p>
                <div className="flex gap-3 justify-center">
                    <button
                        onClick={reset}
                        className="px-5 py-2.5 rounded-xl bg-cyan-600 text-white text-sm font-semibold hover:bg-cyan-700 transition-colors"
                    >
                        Try Again
                    </button>
                    <a
                        href="/"
                        className="px-5 py-2.5 rounded-xl border border-slate-200 text-slate-600 text-sm font-semibold hover:bg-slate-50 transition-colors"
                    >
                        Go Home
                    </a>
                </div>
                {error.digest && (
                    <p className="mt-4 text-xs text-slate-400 font-mono">Error ID: {error.digest}</p>
                )}
            </div>
        </div>
    );
}
