export function CardSkeleton() {
    return (
        <div className="rounded-2xl border border-slate-100 bg-white p-6 animate-pulse">
            <div className="h-10 w-10 rounded-xl bg-slate-100 mb-4" />
            <div className="h-4 w-3/4 rounded bg-slate-100 mb-2" />
            <div className="h-3 w-full rounded bg-slate-50 mb-1" />
            <div className="h-3 w-2/3 rounded bg-slate-50" />
        </div>
    );
}

export function FormSkeleton() {
    return (
        <div className="max-w-xl mx-auto space-y-4 animate-pulse">
            <div className="h-6 w-1/2 mx-auto rounded bg-slate-100 mb-6" />
            {[1, 2, 3, 4].map((i) => (
                <div key={i} className="space-y-1.5">
                    <div className="h-3 w-20 rounded bg-slate-100" />
                    <div className="h-11 w-full rounded-xl bg-slate-50 border border-slate-100" />
                </div>
            ))}
            <div className="h-11 w-full rounded-xl bg-slate-100 mt-6" />
        </div>
    );
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
    return (
        <div className="space-y-3 animate-pulse">
            <div className="grid grid-cols-4 gap-4 px-4 py-2">
                {[1, 2, 3, 4].map((i) => (
                    <div key={i} className="h-3 rounded bg-slate-100" />
                ))}
            </div>
            {Array.from({ length: rows }).map((_, i) => (
                <div key={i} className="grid grid-cols-4 gap-4 px-4 py-3 rounded-xl bg-slate-50/50">
                    {[1, 2, 3, 4].map((j) => (
                        <div key={j} className="h-3 rounded bg-slate-100" />
                    ))}
                </div>
            ))}
        </div>
    );
}
