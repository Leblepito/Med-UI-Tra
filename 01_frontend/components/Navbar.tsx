"use client";

import Link from "next/link";
import { useState } from "react";
import { usePathname } from "next/navigation";
import { useLanguage } from "../lib/LanguageContext";
import LanguagePicker from "./LanguagePicker";

export default function Navbar() {
    const { t } = useLanguage();
    const pathname = usePathname();
    const [mobileOpen, setMobileOpen] = useState(false);

    const links = [
        { href: "/", label: t("navHome"), icon: "🏠" },
        { href: "/medical", label: t("navMedical"), icon: "🏥" },
        { href: "/medical/visualize", label: t("navVisualize"), icon: "🔮" },
        { href: "/travel", label: t("navTravel"), icon: "🏖️" },
        { href: "/blog", label: t("blogNavLabel"), icon: "📝" },
        { href: "/factory", label: t("navFactory"), icon: "🏭", soon: true },
    ];

    return (
        <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-xl border-b border-slate-100 shadow-sm">
            <div className="container-main h-16 flex items-center justify-between gap-4">

                {/* Logo */}
                <Link href="/" className="flex items-center gap-2.5 shrink-0">
                    <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-sky-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-sky-500/20">
                        <span className="text-lg">✈️</span>
                    </div>
                    <div className="hidden sm:flex flex-col leading-none">
                        <span className="text-xs font-bold text-slate-400 tracking-widest uppercase">AntiGravity</span>
                        <span className="text-sm font-bold text-slate-800">Medical</span>
                    </div>
                </Link>

                {/* Desktop nav links */}
                <nav className="hidden md:flex items-center gap-1">
                    {links.map(({ href, label, soon }) => {
                        const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
                        return (
                            <Link
                                key={href}
                                href={href}
                                className={`relative flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${active
                                        ? "bg-sky-50 text-sky-700"
                                        : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                                    }`}
                            >
                                {label}
                                {soon && (
                                    <span className="text-[9px] font-bold text-amber-600 bg-amber-100 rounded-full px-1.5 py-0.5 leading-none uppercase tracking-wider">
                                        {t("navComingSoon")}
                                    </span>
                                )}
                                {active && (
                                    <span className="absolute bottom-0.5 left-1/2 -translate-x-1/2 h-0.5 w-4 rounded-full bg-sky-500" />
                                )}
                            </Link>
                        );
                    })}
                </nav>

                {/* Language picker + mobile toggle */}
                <div className="flex items-center gap-2">
                    <LanguagePicker variant="compact" />

                    {/* Mobile hamburger */}
                    <button
                        type="button"
                        className="md:hidden p-2 rounded-lg text-slate-500 hover:bg-slate-50 transition-colors"
                        onClick={() => setMobileOpen(!mobileOpen)}
                        aria-label="Toggle menu"
                        aria-expanded={mobileOpen}
                        aria-controls="mobile-nav"
                    >
                        {mobileOpen ? (
                            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                        ) : (
                            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>
                        )}
                    </button>
                </div>
            </div>

            {/* Mobile menu */}
            {mobileOpen && (
                <div id="mobile-nav" className="md:hidden border-t border-slate-100 bg-white/95 backdrop-blur-xl" role="navigation" aria-label="Mobile navigation">
                    <div className="container-main py-3 flex flex-col gap-1">
                        {links.map(({ href, label, icon, soon }) => {
                            const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
                            return (
                                <Link
                                    key={href}
                                    href={href}
                                    onClick={() => setMobileOpen(false)}
                                    className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-colors ${active ? "bg-sky-50 text-sky-700" : "text-slate-600 hover:bg-slate-50"
                                        }`}
                                >
                                    <span>{icon}</span>
                                    {label}
                                    {soon && (
                                        <span className="ml-auto text-[9px] font-bold text-amber-600 bg-amber-100 rounded-full px-1.5 py-0.5 uppercase tracking-wider">
                                            {t("navComingSoon")}
                                        </span>
                                    )}
                                </Link>
                            );
                        })}
                    </div>
                </div>
            )}
        </header>
    );
}
