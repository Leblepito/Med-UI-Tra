"use client";

import Link from "next/link";
import { useState } from "react";
import Navbar from "../../components/Navbar";
import { useLanguage } from "../../lib/LanguageContext";

const FEATURES = [
    { icon: "👗", label: "Textile / Apparel" },
    { icon: "🧵", label: "Custom Manufacturing" },
    { icon: "📦", label: "Bulk Export" },
    { icon: "🤝", label: "B2B Contracts" },
    { icon: "🇹🇷", label: "Turkey Sourcing" },
    { icon: "🇹🇭", label: "Thailand Sourcing" },
];

export default function FactoryPage() {
    const { t, dir } = useLanguage();
    const [phone, setPhone] = useState("");
    const [submitted, setSubmitted] = useState(false);

    return (
        <div className="min-h-screen bg-white text-slate-800" dir={dir}>
            <Navbar />

            {/* Hero — coming soon */}
            <section className="section-padding bg-gradient-to-b from-slate-900 to-slate-800 text-white relative overflow-hidden">
                <div className="absolute inset-0 pointer-events-none opacity-10"
                    style={{ backgroundImage: "repeating-linear-gradient(45deg, #f59e0b 0, #f59e0b 1px, transparent 0, transparent 50%)", backgroundSize: "20px 20px" }} />
                <div className="container-main relative text-center animate-fade-up">
                    <div className="inline-flex items-center gap-2 rounded-full border border-amber-500/40 bg-amber-500/10 px-4 py-1.5 mb-8">
                        <span className="h-2 w-2 rounded-full bg-amber-400 animate-pulse" />
                        <span className="text-xs font-bold text-amber-300 tracking-widest uppercase">{t("factoryBadge")}</span>
                    </div>
                    <h1 className="font-display text-4xl sm:text-5xl font-bold text-white mb-5">{t("factoryTitle")}</h1>
                    <p className="text-slate-300 text-lg max-w-xl mx-auto leading-relaxed">{t("factorySub")}</p>

                    {/* Feature chips */}
                    <div className="mt-10 flex flex-wrap justify-center gap-3">
                        {FEATURES.map((f) => (
                            <span key={f.label} className="flex items-center gap-1.5 px-4 py-2 rounded-full bg-white/10 border border-white/10 text-slate-300 text-sm backdrop-blur-sm">
                                {f.icon} {f.label}
                            </span>
                        ))}
                    </div>

                    {/* Notify form */}
                    <div className="mt-12 max-w-md mx-auto rounded-2xl border border-amber-500/20 bg-white/5 backdrop-blur-sm p-6">
                        <h2 className="text-base font-bold text-white mb-1">{t("factoryNotifyTitle")}</h2>
                        {submitted ? (
                            <p className="text-amber-300 font-semibold text-sm mt-3">✅ {t("factoryNotifyThanks")}</p>
                        ) : (
                            <>
                                <p className="text-sm text-slate-400 mb-4">{t("factoryNotifySub")}</p>
                                <div className="flex gap-2">
                                    <input
                                        type="text"
                                        aria-label="Phone or email for notifications"
                                        placeholder={t("factoryNotifyPlaceholder")}
                                        value={phone}
                                        onChange={(e) => setPhone(e.target.value)}
                                        className="flex-1 rounded-xl bg-white/10 border border-white/20 px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-amber-400 transition-all"
                                    />
                                    <button onClick={() => { if (phone.trim()) setSubmitted(true); }}
                                        className="px-4 py-2.5 rounded-xl bg-amber-500 text-white text-sm font-bold hover:bg-amber-400 transition-colors shrink-0">
                                        {t("factoryNotifyBtn")}
                                    </button>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="border-t border-slate-100 bg-slate-50 py-8">
                <div className="container-main text-center text-xs text-slate-400">
                    <span>AntiGravity Factory · B2B · Turkey & Thailand</span>
                    <span className="mx-3">·</span>
                    <Link href="/" className="hover:text-amber-600 transition-colors">{t("btnBack")}</Link>
                </div>
            </footer>
        </div>
    );
}
