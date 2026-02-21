export default function Loading() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-white">
            <div className="text-center animate-fade-up">
                <div className="w-12 h-12 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-cyan-500 to-cyan-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 animate-pulse">
                    <svg className="w-6 h-6 text-white animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                </div>
                <p className="text-sm text-slate-400 font-medium">Loading...</p>
            </div>
        </div>
    );
}
