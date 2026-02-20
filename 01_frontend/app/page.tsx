"use client";

import Link from "next/link";
import { useState } from "react";
import Navbar from "../components/Navbar";
import LanguagePicker from "../components/LanguagePicker";
import { useLanguage } from "../lib/LanguageContext";
import type { Language } from "../lib/i18n";

// ─── Language Selection Screen ───────────────────────────────────────────────
function LanguageSelectScreen({ onSelect }: { onSelect: (lang: Language) => void }) {
    return (
        <div className="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-sky-900 p-6">
            {/* Background mesh */}
            <div className="absolute inset-0 opacity-10"
                style={{ backgroundImage: "radial-gradient(circle at 20% 50%, #0ea5e9 0%, transparent 50%), radial-gradient(circle at 80% 20%, #6366f1 0%, transparent 50%)" }}
            />

            <div className="relative z-10 w-full max-w-lg text-center">
                {/* Logo */}
                <div className="flex justify-center mb-6">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-sky-500 to-cyan-400 flex items-center justify-center shadow-2xl shadow-sky-500/40">
                        <span className="text-3xl">✈️</span>
                    </div>
                </div>

                <h1 className="text-3xl font-bold text-white mb-2">AntiGravity Medical</h1>
                <p className="text-sky-300 text-sm mb-8 font-medium tracking-wide">
                    Phuket ↔ Turkey · Medical · Travel · B2B
                </p>

                {/* Prompt */}
                <p className="text-slate-300 text-base mb-2 font-semibold">Choose your language</p>
                <p className="text-slate-500 text-xs mb-6">Выберите язык · Dil seçin · เลือกภาษา · اختر لغتك · 选择语言</p>

                {/* Language cards */}
                <LanguagePicker
                    variant="full"
                    onPick={(l) => onSelect(l)}
                    className="mb-6"
                />

                <p className="text-slate-600 text-xs mt-4">
                    You can change the language anytime from the top bar
                </p>
            </div>
        </div>
    );
}

// ─── Stats Bar ───────────────────────────────────────────────────────────────
const STATS = [
    { key: "statsPatients", value: "1,800+" },
    { key: "statsCountries", value: "32" },
    { key: "statsClinics", value: "18" },
    { key: "statsSaving", value: "70%" },
] as const;

// ─── Sector Cards ────────────────────────────────────────────────────────────
const SECTORS = [
    {
        icon: "🏥",
        color: "from-sky-500 to-cyan-400",
        shadow: "shadow-sky-500/20",
        href: "/medical",
        titleKey: "secMedTitle",
        descKey: "secMedDesc",
        btnKey: "secMedBtn",
        badge: "JCI ✓",
        badgeCls: "bg-sky-100 text-sky-700",
        soon: false,
    },
    {
        icon: "🏖️",
        color: "from-teal-500 to-emerald-400",
        shadow: "shadow-teal-500/20",
        href: "/travel",
        titleKey: "secTravelTitle",
        descKey: "secTravelDesc",
        btnKey: "secTravelBtn",
        badge: "Phuket",
        badgeCls: "bg-teal-100 text-teal-700",
        soon: false,
    },
    {
        icon: "🏭",
        color: "from-amber-500 to-orange-400",
        shadow: "shadow-amber-500/20",
        href: "/factory",
        titleKey: "secFactoryTitle",
        descKey: "secFactoryDesc",
        btnKey: "navComingSoon",
        badge: "B2B",
        badgeCls: "bg-amber-100 text-amber-700",
        soon: true,
    },
] as const;

// ─── Main Page ───────────────────────────────────────────────────────────────
export default function HomePage() {
    const { t, lang } = useLanguage();
    // Show language select screen for first-time visitors
    const [langChosen, setLangChosen] = useState(() => {
        if (typeof window === "undefined") return true; // SSR: skip
        return Boolean(localStorage.getItem("thaiturk_lang"));
    });

    if (!langChosen) {
        return (
            <LanguageSelectScreen
                onSelect={(l) => {
                    setLangChosen(true);
                }}
            />
        );
    }

    return (
        <div className="min-h-screen bg-white text-slate-800" dir={lang === "ar" ? "rtl" : "ltr"}>
            <Navbar />

            {/* ── HERO ─────────────────────────────────────────────────────── */}
            <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-sky-900 py-20 sm:py-28">
                {/* Bokeh blobs */}
                <div className="pointer-events-none absolute inset-0">
                    <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-sky-500/10 blur-3xl" />
                    <div className="absolute bottom-[-20%] right-[-5%] w-[45%] h-[55%] rounded-full bg-indigo-500/10 blur-3xl" />
                </div>

                <div className="container-main relative z-10 text-center animate-fade-up">
                    <div className="inline-flex items-center gap-2 rounded-full border border-sky-500/30 bg-sky-500/10 px-4 py-1.5 mb-8">
                        <span className="h-2 w-2 rounded-full bg-sky-400 animate-pulse" />
                        <span className="text-xs font-bold text-sky-300 tracking-widest uppercase">
                            Phuket ↔ Turkey ↔ AI
                        </span>
                    </div>

                    <h1 className="font-display text-4xl sm:text-6xl font-bold text-white leading-tight mb-4">
                        {t("heroTitle")}
                    </h1>
                    <p className="text-slate-300 text-lg sm:text-xl max-w-2xl mx-auto leading-relaxed mb-8">
                        {t("heroSub")}
                    </p>

                    <div className="flex flex-wrap justify-center gap-3 mb-10">
                        <Link href="/medical"
                            className="px-7 py-3.5 rounded-xl bg-sky-500 text-white font-bold hover:bg-sky-400 transition-all duration-200 shadow-lg shadow-sky-500/30 hover:scale-105">
                            {t("heroBtn")}
                        </Link>
                        <Link href="/travel"
                            className="px-7 py-3.5 rounded-xl border border-white/20 text-white font-semibold hover:bg-white/10 transition-all duration-200">
                            {t("secTravelBtn")}
                        </Link>
                    </div>

                    {/* Inline language switcher for visibility */}
                    <div className="flex justify-center">
                        <LanguagePicker variant="compact" />
                    </div>
                </div>
            </section>

            {/* ── STATS BAR ────────────────────────────────────────────────── */}
            <section className="bg-white border-b border-slate-100">
                <div className="container-main py-6 grid grid-cols-2 sm:grid-cols-4 gap-4 sm:gap-0 sm:divide-x divide-slate-100">
                    {STATS.map(({ key, value }) => (
                        <div key={key} className="text-center px-4">
                            <p className="text-2xl font-bold text-sky-600">{value}</p>
                            <p className="text-xs text-slate-500 mt-0.5">{t(key as Parameters<typeof t>[0])}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* ── SECTORS ──────────────────────────────────────────────────── */}
            <section className="section-padding bg-slate-50">
                <div className="container-main">
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                        {SECTORS.map((s, i) => (
                            <div
                                key={s.href}
                                className={`group relative rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1 stagger-${i + 1}`}
                            >
                                {/* Icon */}
                                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${s.color} flex items-center justify-center shadow-lg ${s.shadow} mb-4`}>
                                    <span className="text-2xl">{s.icon}</span>
                                </div>
                                <span className={`text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${s.badgeCls}`}>{s.badge}</span>

                                <h2 className="mt-3 text-lg font-bold text-slate-800">{t(s.titleKey as Parameters<typeof t>[0])}</h2>
                                <p className="text-sm text-slate-500 mt-2 leading-relaxed">{t(s.descKey as Parameters<typeof t>[0])}</p>

                                <div className="mt-5">
                                    {s.soon ? (
                                        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-amber-200 text-amber-600 text-sm font-semibold">
                                            🔒 {t("navComingSoon")}
                                        </span>
                                    ) : (
                                        <Link href={s.href}
                                            className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-gradient-to-r ${s.color} text-white text-sm font-bold shadow-md transition-all duration-200 hover:scale-105`}>
                                            {t(s.btnKey as Parameters<typeof t>[0])} →
                                        </Link>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── FOOTER ───────────────────────────────────────────────────── */}
            <footer className="border-t border-slate-100 bg-white py-8">
                <div className="container-main flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-slate-400">
                    <span>© 2026 AntiGravity Ventures · {t("footerTagline")}</span>
                    <div className="flex gap-4">
                        <Link href="/medical" className="hover:text-sky-600 transition-colors">{t("navMedical")}</Link>
                        <Link href="/travel" className="hover:text-sky-600 transition-colors">{t("navTravel")}</Link>
                        <Link href="/factory" className="hover:text-sky-600 transition-colors">{t("navFactory")}</Link>
                    </div>
                </div>
            </footer>
        </div>
    );
}
