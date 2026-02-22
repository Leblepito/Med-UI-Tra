"use client";

import { useState } from "react";
import Link from "next/link";
import Navbar from "../../../components/Navbar";
import { useLanguage } from "../../../lib/LanguageContext";

// ─── Procedure Gallery Data ───────────────────────────────────────────────────
const GALLERY_CASES = [
    {
        id: 1,
        category: "hair",
        procedure: "Hair Transplant",
        hospital: "HairCure Istanbul",
        country: "Turkey",
        cases: 2400,
        rating: 4.8,
        beforeGrad: "from-amber-100 via-orange-100 to-amber-200",
        afterGrad: "from-slate-900 via-slate-800 to-slate-700",
        icon: "💆",
        beforeLabel: "Thinning crown, receding hairline",
        afterLabel: "Full density, natural hairline restored",
        stats: ["3500 grafts", "9h procedure", "12 months result"],
        savings: "72%",
        priceRange: "$1,800–$3,500",
    },
    {
        id: 2,
        category: "rhinoplasty",
        procedure: "Rhinoplasty",
        hospital: "Memorial Şişli",
        country: "Turkey",
        cases: 1800,
        rating: 4.9,
        beforeGrad: "from-rose-100 via-pink-100 to-rose-200",
        afterGrad: "from-rose-900 via-rose-800 to-pink-900",
        icon: "👃",
        beforeLabel: "Dorsal hump, wide nasal bridge",
        afterLabel: "Refined profile, balanced harmony",
        stats: ["General anesthesia", "10-day recovery", "Final result 6–12mo"],
        savings: "65%",
        priceRange: "$3,500–$6,000",
    },
    {
        id: 3,
        category: "dental",
        procedure: "Dental Veneers",
        hospital: "DentGroup Istanbul",
        country: "Turkey",
        cases: 3100,
        rating: 4.7,
        beforeGrad: "from-yellow-100 via-amber-100 to-yellow-200",
        afterGrad: "from-emerald-800 via-teal-800 to-emerald-900",
        icon: "🦷",
        beforeLabel: "Stained, uneven, chipped enamel",
        afterLabel: "Hollywood smile, perfect symmetry",
        stats: ["E-max porcelain", "2 sessions", "15yr lifespan"],
        savings: "70%",
        priceRange: "$200–$400 / tooth",
    },
    {
        id: 4,
        category: "face",
        procedure: "Facelift",
        hospital: "Acıbadem Maslak",
        country: "Turkey",
        cases: 950,
        rating: 4.9,
        beforeGrad: "from-purple-100 via-violet-100 to-purple-200",
        afterGrad: "from-purple-900 via-violet-900 to-indigo-900",
        icon: "✨",
        beforeLabel: "Sagging skin, deep nasolabial folds",
        afterLabel: "Lifted, refreshed, 10–15 year rejuvenation",
        stats: ["5–6h procedure", "2w recovery", "Results 10–15yr"],
        savings: "60%",
        priceRange: "$6,000–$10,000",
    },
    {
        id: 5,
        category: "body",
        procedure: "Liposuction",
        hospital: "Bangkok Hospital Phuket",
        country: "Thailand",
        cases: 2200,
        rating: 4.7,
        beforeGrad: "from-indigo-100 via-blue-100 to-indigo-200",
        afterGrad: "from-indigo-900 via-blue-900 to-slate-900",
        icon: "🏋️",
        beforeLabel: "Stubborn fat deposits, uneven contour",
        afterLabel: "Sculpted silhouette, defined contours",
        stats: ["VASER technology", "3–5 day recovery", "Long-lasting"],
        savings: "58%",
        priceRange: "$2,500–$5,000",
    },
    {
        id: 6,
        category: "hair",
        procedure: "FUE Hair Transplant",
        hospital: "EsteNove Clinic",
        country: "Turkey",
        cases: 1600,
        rating: 4.8,
        beforeGrad: "from-sky-100 via-cyan-100 to-sky-200",
        afterGrad: "from-sky-900 via-cyan-900 to-slate-800",
        icon: "💆",
        beforeLabel: "Type 4 baldness, visible scalp",
        afterLabel: "Dense coverage, undetectable extraction",
        stats: ["FUE method", "4500 grafts", "8mo to full result"],
        savings: "74%",
        priceRange: "$2,000–$4,200",
    },
];

const FILTERS = [
    { key: "all", labelKey: "galAll" as const },
    { key: "hair", labelKey: "galFilterHair" as const },
    { key: "rhinoplasty", labelKey: "galFilterRhino" as const },
    { key: "dental", labelKey: "galFilterDental" as const },
    { key: "face", labelKey: "galFilterFace" as const },
    { key: "body", labelKey: "galFilterBody" as const },
] as const;

// ─── Animated Slider Card ─────────────────────────────────────────────────────
function GalleryCard({ item }: { item: typeof GALLERY_CASES[0] }) {
    const [hovered, setHovered] = useState(false);

    return (
        <div
            className="group relative rounded-2xl overflow-hidden border border-slate-200 bg-white shadow-md hover:shadow-2xl transition-all duration-500 hover:-translate-y-1"
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
        >
            {/* Image comparison area */}
            <div className="relative h-56 overflow-hidden">
                {/* Before side */}
                <div
                    className={`absolute inset-0 bg-gradient-to-br ${item.beforeGrad} flex flex-col items-center justify-center transition-all duration-700`}
                    style={{ clipPath: hovered ? "inset(0 60% 0 0)" : "inset(0 0% 0 0)" }}
                >
                    <span className="text-5xl mb-2 grayscale opacity-70">{item.icon}</span>
                    <div className="text-center px-3">
                        <div className="inline-block bg-black/60 text-white text-[10px] font-bold px-2 py-0.5 rounded-full mb-1">BEFORE</div>
                        <p className="text-xs text-slate-600 leading-tight">{item.beforeLabel}</p>
                    </div>
                </div>
                {/* After side */}
                <div
                    className={`absolute inset-0 bg-gradient-to-br ${item.afterGrad} flex flex-col items-center justify-center transition-all duration-700`}
                    style={{ clipPath: hovered ? "inset(0 0% 0 40%)" : "inset(0 0% 0 100%)" }}
                >
                    <span className="text-5xl mb-2 brightness-200">{item.icon}</span>
                    <div className="text-center px-3">
                        <div className="inline-block bg-cyan-500/80 text-white text-[10px] font-bold px-2 py-0.5 rounded-full mb-1">AFTER (AI)</div>
                        <p className="text-xs text-white/80 leading-tight">{item.afterLabel}</p>
                    </div>
                </div>

                {/* Divider line */}
                <div
                    className="absolute top-0 bottom-0 w-0.5 bg-white shadow-lg transition-all duration-700 z-10"
                    style={{ left: hovered ? "40%" : "100%" }}
                >
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-white shadow-xl flex items-center justify-center text-slate-600 text-xs font-bold">
                        ↔
                    </div>
                </div>

                {/* Hover hint */}
                {!hovered && (
                    <div className="absolute inset-0 flex items-center justify-center z-20">
                        <div className="bg-black/40 backdrop-blur-sm text-white text-xs font-semibold px-3 py-1.5 rounded-full flex items-center gap-1.5 animate-pulse">
                            <span>↔</span> Hover to reveal
                        </div>
                    </div>
                )}

                {/* Savings badge */}
                <div className="absolute top-3 right-3 z-30 bg-emerald-500 text-white text-xs font-bold px-2.5 py-1 rounded-full shadow-lg">
                    Save {item.savings}
                </div>
            </div>

            {/* Card info */}
            <div className="p-4">
                <div className="flex items-start justify-between mb-2">
                    <div>
                        <h3 className="font-bold text-slate-800 text-sm">{item.procedure}</h3>
                        <p className="text-xs text-slate-500">{item.hospital} · {item.country}</p>
                    </div>
                    <div className="text-right">
                        <div className="text-xs font-bold text-cyan-600">{item.priceRange}</div>
                        <div className="text-[11px] text-slate-400">from</div>
                    </div>
                </div>

                {/* Stats pills */}
                <div className="flex flex-wrap gap-1.5 mb-3">
                    {item.stats.map((s) => (
                        <span key={s} className="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full font-medium">
                            {s}
                        </span>
                    ))}
                </div>

                {/* Rating + cases */}
                <div className="flex items-center justify-between text-xs text-slate-500 border-t border-slate-100 pt-2.5">
                    <span className="flex items-center gap-1">
                        <span className="text-amber-400">★</span>
                        <span className="font-semibold text-slate-700">{item.rating}</span>
                    </span>
                    <span>{item.cases.toLocaleString()} cases</span>
                </div>
            </div>
        </div>
    );
}

// ─── Main Page ─────────────────────────────────────────────────────────────────
export default function GalleryPage() {
    const { t } = useLanguage();
    const [activeFilter, setActiveFilter] = useState("all");

    const filtered = activeFilter === "all"
        ? GALLERY_CASES
        : GALLERY_CASES.filter((c) => c.category === activeFilter);

    return (
        <div className="min-h-screen bg-white text-slate-800">
            <Navbar />

            {/* ── Hero ─────────────────────────────────────────────────── */}
            <section className="relative bg-gradient-to-br from-slate-900 via-slate-800 to-sky-900 py-16 sm:py-20 overflow-hidden">
                <div className="pointer-events-none absolute inset-0">
                    <div className="absolute top-[-15%] left-[-8%] w-[45%] h-[55%] rounded-full bg-cyan-500/10 blur-3xl" />
                    <div className="absolute bottom-[-20%] right-[-5%] w-[40%] h-[50%] rounded-full bg-violet-500/10 blur-3xl" />
                </div>
                <div className="container-main relative z-10 text-center">
                    <div className="inline-flex items-center gap-2 rounded-full border border-cyan-500/30 bg-cyan-500/10 px-4 py-1.5 mb-6">
                        <span className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse" />
                        <span className="text-xs font-bold text-cyan-300 tracking-widest uppercase">AI-Simulated Results</span>
                    </div>
                    <h1 className="font-display text-3xl sm:text-5xl font-bold text-white leading-tight mb-4">
                        {t("galTitle")}
                    </h1>
                    <p className="text-slate-300 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed mb-8">
                        {t("galSubtitle")}
                    </p>
                    <Link
                        href="/medical/visualize"
                        className="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 to-sky-500 text-white font-bold hover:scale-105 transition-all shadow-lg shadow-cyan-500/30"
                    >
                        ✨ {t("galCtaBtn")}
                    </Link>
                </div>
            </section>

            {/* ── Disclaimer Banner ────────────────────────────────────── */}
            <div className="bg-amber-50 border-b border-amber-200">
                <div className="container-main py-3 flex items-start gap-2">
                    <span className="text-amber-500 text-sm mt-0.5 shrink-0">⚠️</span>
                    <p className="text-xs text-amber-700 leading-relaxed">{t("galDisclaimer")}</p>
                </div>
            </div>

            {/* ── Filter Tabs ──────────────────────────────────────────── */}
            <section className="border-b border-slate-100 bg-white sticky top-0 z-20 shadow-sm">
                <div className="container-main py-3">
                    <div className="flex items-center gap-2 overflow-x-auto scrollbar-none pb-0.5">
                        {FILTERS.map((f) => (
                            <button
                                key={f.key}
                                onClick={() => setActiveFilter(f.key)}
                                className={`shrink-0 rounded-full px-4 py-1.5 text-xs font-semibold transition-all ${activeFilter === f.key
                                        ? "bg-cyan-600 text-white shadow-md shadow-cyan-500/30"
                                        : "border border-slate-200 text-slate-600 hover:border-cyan-300 hover:text-cyan-600"
                                    }`}
                            >
                                {t(f.labelKey)}
                            </button>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── Gallery Grid ─────────────────────────────────────────── */}
            <section className="section-padding">
                <div className="container-main">
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filtered.map((item) => (
                            <GalleryCard key={item.id} item={item} />
                        ))}
                    </div>

                    {filtered.length === 0 && (
                        <div className="text-center py-20 text-slate-400">
                            <div className="text-4xl mb-3">🔍</div>
                            <p className="text-sm font-medium">No results for this filter</p>
                        </div>
                    )}
                </div>
            </section>

            {/* ── Stats Strip ──────────────────────────────────────────── */}
            <section className="bg-slate-50 border-y border-slate-100 py-10">
                <div className="container-main">
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 text-center">
                        {[
                            { value: "12,000+", label: t("galCases") },
                            { value: "98%", label: "Satisfaction Rate" },
                            { value: "40+", label: "Partner Clinics" },
                            { value: "4.8★", label: t("galRating") },
                        ].map((s) => (
                            <div key={s.label}>
                                <div className="text-2xl font-display font-bold text-cyan-600">{s.value}</div>
                                <div className="text-xs text-slate-500 mt-0.5 font-medium">{s.label}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── CTA ─────────────────────────────────────────────────── */}
            <section className="section-padding bg-gradient-to-br from-slate-900 via-slate-800 to-sky-900">
                <div className="container-main text-center">
                    <h2 className="text-2xl sm:text-3xl font-display font-bold text-white mb-3">
                        {t("galCtaTitle")}
                    </h2>
                    <p className="text-slate-300 text-sm mb-8 max-w-lg mx-auto leading-relaxed">{t("galCtaSub")}</p>
                    <div className="flex flex-wrap justify-center gap-4">
                        <Link
                            href="/medical/visualize"
                            className="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 to-sky-500 text-white font-bold hover:scale-105 transition-all shadow-lg shadow-cyan-500/30"
                        >
                            🤖 {t("galCtaBtn")}
                        </Link>
                        <Link
                            href="/medical"
                            className="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl border border-white/20 text-white font-semibold hover:bg-white/10 transition-all"
                        >
                            📋 {t("btnConsultation")}
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    );
}
