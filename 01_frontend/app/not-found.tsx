import Link from "next/link";

export default function NotFound() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-white px-4">
            <div className="max-w-md text-center animate-fade-up">
                <div className="text-8xl font-bold text-slate-100 mb-4 font-display">404</div>
                <h1 className="font-display text-2xl font-bold text-slate-800 mb-2">Page Not Found</h1>
                <p className="text-slate-500 text-sm mb-8 leading-relaxed">
                    The page you&apos;re looking for doesn&apos;t exist or has been moved.
                </p>
                <div className="flex gap-3 justify-center">
                    <Link
                        href="/"
                        className="px-5 py-2.5 rounded-xl bg-cyan-600 text-white text-sm font-semibold hover:bg-cyan-700 transition-colors"
                    >
                        Go Home
                    </Link>
                    <Link
                        href="/medical"
                        className="px-5 py-2.5 rounded-xl border border-slate-200 text-slate-600 text-sm font-semibold hover:bg-slate-50 transition-colors"
                    >
                        Medical Services
                    </Link>
                </div>
            </div>
        </div>
    );
}
