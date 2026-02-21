"use client";

import Link from "next/link";
import { useState } from "react";
import Navbar from "../../components/Navbar";
import { useLanguage } from "../../lib/LanguageContext";
import type { TravelResponse } from "../../lib/api";

const DESTINATIONS: Record<string, string[]> = {
    en: ["Phuket — Patong Beach", "Phuket — Kamala", "Phuket — Kata", "Koh Samui", "Krabi"],
    ru: ["Пхукет — Патонг-Бич", "Пхукет — Камала", "Пхукет — Ката", "Ко Самуи", "Краби"],
    tr: ["Phuket — Patong Plajı", "Phuket — Kamala", "Phuket — Kata", "Koh Samui", "Krabi"],
    th: ["ภูเก็ต — หาดป่าตอง", "ภูเก็ต — กมลา", "ภูเก็ต — กะตะ", "เกาะสมุย", "กระบี่"],
    ar: ["بوكيت — شاطئ باتونج", "بوكيت — كامالا", "بوكيت — كاتا", "كو ساموي", "كرابي"],
    zh: ["普吉岛 — 芭东海滩", "普吉岛 — 卡马拉", "普吉岛 — 卡塔", "苏梅岛", "甲米"],
};

const WHY_ICONS = ["🧑‍💼", "💰", "🚗", "🏝️"] as const;
const WHY_KEYS = [
    ["travelWhy1", "travelWhy1d"],
    ["travelWhy2", "travelWhy2d"],
    ["travelWhy3", "travelWhy3d"],
    ["travelWhy4", "travelWhy4d"],
] as const;

export default function TravelPage() {
    const { t, lang, dir } = useLanguage();
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [travelResult, setTravelResult] = useState<TravelResponse | null>(null);
    const [errorMsg, setErrorMsg] = useState("");
    const [form, setForm] = useState({
        full_name: "", phone: "", destination: "", check_in: "", check_out: "",
        guests: "2", notes: "",
    });

    const destOptions = DESTINATIONS[lang] ?? DESTINATIONS.en;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErrorMsg("");

        // Date validation: check_out must be after check_in
        if (form.check_in && form.check_out && form.check_out <= form.check_in) {
            setErrorMsg(t("travelDateError") || "Check-out date must be after check-in date.");
            return;
        }

        setLoading(true);
        try {
            const res = await fetch("/api/travel/options", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ...form, language: lang }),
            });
            if (!res.ok) {
                const err = await res.json().catch(() => null);
                throw new Error(err?.detail || "API error");
            }
            const data: TravelResponse = await res.json();
            setTravelResult(data);
        } catch (err) {
            setTravelResult(null);
            setErrorMsg(err instanceof Error ? err.message : "An unexpected error occurred. Please try again.");
        } finally {
            setLoading(false);
            setSubmitted(true);
        }
    };

    return (
        <div className="min-h-screen bg-white text-slate-800" dir={dir}>
            <Navbar />

            {/* ── HERO ─────────────────────────────────────────────────────── */}
            <section className="relative overflow-hidden bg-gradient-to-br from-teal-900 via-slate-800 to-emerald-900 py-20 sm:py-28">
                <div className="pointer-events-none absolute inset-0">
                    <div className="absolute -top-20 -left-20 w-96 h-96 rounded-full bg-teal-500/10 blur-3xl" />
                    <div className="absolute -bottom-20 -right-20 w-96 h-96 rounded-full bg-emerald-500/10 blur-3xl" />
                </div>
                <div className="container-main relative z-10 text-center animate-fade-up">
                    <div className="inline-flex items-center gap-2 rounded-full border border-teal-400/30 bg-teal-400/10 px-4 py-1.5 mb-6">
                        <span className="h-2 w-2 rounded-full bg-teal-400 animate-pulse" />
                        <span className="text-xs font-bold text-teal-300 uppercase tracking-widest">{t("travelBadge")}</span>
                    </div>
                    <h1 className="font-display text-4xl sm:text-6xl font-bold text-white mb-4">{t("travelTitle")}</h1>
                    <p className="text-slate-300 text-lg max-w-xl mx-auto leading-relaxed">{t("travelSubtitle")}</p>
                </div>
            </section>

            {/* ── WHY ──────────────────────────────────────────────────────── */}
            <section className="section-padding bg-slate-50">
                <div className="container-main grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                    {WHY_KEYS.map(([titleKey, descKey], i) => (
                        <div key={i} className="bg-white rounded-2xl border border-slate-100 p-5 shadow-sm hover:shadow-md transition-shadow">
                            <div className="w-10 h-10 rounded-xl bg-teal-50 flex items-center justify-center text-xl mb-3">{WHY_ICONS[i]}</div>
                            <h3 className="font-bold text-slate-800 mb-1">{t(titleKey)}</h3>
                            <p className="text-sm text-slate-500 leading-relaxed">{t(descKey)}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* ── BOOKING FORM ─────────────────────────────────────────────── */}
            <section className="section-padding bg-white">
                <div className="container-main max-w-xl">
                    <h2 className="font-display text-2xl font-bold text-slate-800 text-center mb-2">{t("travelFormTitle")}</h2>
                    <p className="text-center text-slate-500 text-sm mb-8">{t("travelFormSub")}</p>

                    {submitted ? (
                        travelResult ? (
                            <div className="rounded-2xl border border-teal-200 bg-gradient-to-b from-teal-50 to-white p-8 animate-fade-up">
                                <div className="flex items-center gap-3 mb-6">
                                    <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-teal-500 to-emerald-600 flex items-center justify-center text-white text-xl shadow-lg shadow-teal-500/20">
                                        🏖️
                                    </div>
                                    <div>
                                        <h3 className="text-xl font-bold text-teal-800">{t("travelSuccess")}</h3>
                                        <div className="text-xs text-teal-600 font-mono font-semibold">
                                            {t("travelRefNo")}: {travelResult.request_id}
                                        </div>
                                    </div>
                                </div>

                                {/* Coordinator message */}
                                <div className="rounded-xl border border-teal-200 bg-teal-50/50 p-4 mb-6">
                                    <p className="text-sm text-slate-700 leading-relaxed">{travelResult.coordinator_message}</p>
                                </div>

                                {/* Hotel suggestions */}
                                {travelResult.suggestions.length > 0 && (
                                    <div className="mb-6">
                                        <h4 className="text-xs text-slate-400 uppercase tracking-widest font-semibold mb-3">{t("travelHotelSuggestions")}</h4>
                                        <div className="space-y-3">
                                            {travelResult.suggestions.map((s, i) => (
                                                <div key={i} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                                                    <div className="flex items-center justify-between mb-1">
                                                        <h5 className="font-semibold text-slate-800">{s.name}</h5>
                                                        <div className="flex items-center gap-0.5">
                                                            {Array.from({ length: s.stars }).map((_, j) => (
                                                                <span key={j} className="text-amber-400 text-xs">&#9733;</span>
                                                            ))}
                                                        </div>
                                                    </div>
                                                    <p className="text-xs text-slate-500 mb-2">{s.highlight}</p>
                                                    <div className="text-sm font-mono font-bold text-teal-600">
                                                        ${s.price_night_usd} <span className="text-slate-400 font-normal text-xs">{t("travelPerNight")}</span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Next steps */}
                                {travelResult.next_steps.length > 0 && (
                                    <div className="mb-6">
                                        <h4 className="text-xs text-slate-400 uppercase tracking-widest font-semibold mb-3">{t("travelNextSteps")}</h4>
                                        <div className="space-y-2">
                                            {travelResult.next_steps.map((step, i) => (
                                                <div key={i} className="flex gap-3 items-start">
                                                    <span className="shrink-0 w-6 h-6 rounded-lg bg-teal-50 border border-teal-200 flex items-center justify-center text-xs font-bold text-teal-700">
                                                        {i + 1}
                                                    </span>
                                                    <span className="text-sm text-slate-600">{step}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                <button onClick={() => { setSubmitted(false); setTravelResult(null); }}
                                    className="w-full py-3 rounded-xl border-2 border-slate-200 bg-white text-sm text-slate-500 font-semibold hover:text-teal-700 hover:bg-teal-50 hover:border-teal-300 transition-all duration-300">
                                    {t("btnNewRequest")}
                                </button>
                            </div>
                        ) : (
                            <div className="rounded-2xl border border-red-200 bg-red-50 p-8 text-center animate-fade-up">
                                <div className="w-12 h-12 mx-auto mb-3 rounded-2xl bg-red-100 flex items-center justify-center">
                                    <svg className="w-6 h-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                                    </svg>
                                </div>
                                <h3 className="text-lg font-bold text-red-800 mb-2">{t("formErrorTitle") || "Something went wrong"}</h3>
                                <p className="text-red-600 text-sm mb-5">{errorMsg || t("formErrorGeneric") || "Please try again later."}</p>
                                <button onClick={() => { setSubmitted(false); setErrorMsg(""); }}
                                    className="px-5 py-2 rounded-xl bg-teal-600 text-white text-sm font-bold hover:bg-teal-500 transition-colors">
                                    {t("btnTryAgain") || "Try Again"}
                                </button>
                            </div>
                        )
                    ) : (
                        <form onSubmit={handleSubmit} className="space-y-4">
                            {errorMsg && (
                                <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700" role="alert">
                                    {errorMsg}
                                </div>
                            )}
                            <div>
                                <label htmlFor="travel-name" className="block text-xs font-semibold text-slate-500 mb-1">{t("fieldName")}</label>
                                <input id="travel-name" required placeholder={t("fieldName")} value={form.full_name}
                                    onChange={e => setForm({ ...form, full_name: e.target.value })}
                                    className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:outline-none focus:border-teal-400 transition-colors" />
                            </div>
                            <div>
                                <label htmlFor="travel-phone" className="block text-xs font-semibold text-slate-500 mb-1">{t("fieldPhone")}</label>
                                <input id="travel-phone" required placeholder="+7 (999) 123-4567" value={form.phone}
                                    onChange={e => setForm({ ...form, phone: e.target.value })}
                                    className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:outline-none focus:border-teal-400 transition-colors" />
                            </div>

                            <div>
                                <label htmlFor="travel-dest" className="block text-xs font-semibold text-slate-500 mb-1">{t("travelFieldDest")}</label>
                            <select id="travel-dest" value={form.destination} onChange={e => setForm({ ...form, destination: e.target.value })}
                                className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm text-slate-700 focus:outline-none focus:border-teal-400 transition-colors">
                                <option value="">{t("travelFieldDest")}</option>
                                {destOptions.map(d => <option key={d} value={d}>{d}</option>)}
                            </select>
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label htmlFor="travel-checkin" className="text-xs text-slate-500 mb-1 block">{t("travelFieldCheckin")}</label>
                                    <input id="travel-checkin" type="date" value={form.check_in}
                                        onChange={e => setForm({ ...form, check_in: e.target.value })}
                                        className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:outline-none focus:border-teal-400" />
                                </div>
                                <div>
                                    <label htmlFor="travel-checkout" className="text-xs text-slate-500 mb-1 block">{t("travelFieldCheckout")}</label>
                                    <input id="travel-checkout" type="date" value={form.check_out}
                                        onChange={e => setForm({ ...form, check_out: e.target.value })}
                                        className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:outline-none focus:border-teal-400" />
                                </div>
                            </div>

                            <div className="flex items-center gap-3">
                                <label htmlFor="travel-guests" className="text-sm text-slate-600 shrink-0">{t("travelFieldGuests")}:</label>
                                <input id="travel-guests" type="number" min="1" max="20" value={form.guests}
                                    onChange={e => setForm({ ...form, guests: e.target.value })}
                                    className="w-24 rounded-xl border border-slate-200 px-4 py-3 text-sm focus:outline-none focus:border-teal-400" />
                            </div>

                            <textarea aria-label="Notes" placeholder={t("fieldNotes")} rows={3} value={form.notes}
                                onChange={e => setForm({ ...form, notes: e.target.value })}
                                className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:outline-none focus:border-teal-400 resize-none transition-colors" />

                            <button type="submit" disabled={loading}
                                className="w-full py-3.5 rounded-xl bg-teal-600 text-white font-bold hover:bg-teal-500 disabled:opacity-60 transition-all duration-200 hover:scale-[1.01]">
                                {loading ? t("btnSubmitting") : t("btnSubmit")}
                            </button>
                        </form>
                    )}
                </div>
            </section>

            {/* ── FOOTER ───────────────────────────────────────────────────── */}
            <footer className="border-t border-slate-100 bg-slate-50 py-8">
                <div className="container-main text-center text-xs text-slate-400">
                    <span>AntiGravity Travel · Phuket · {t("footerTagline")}</span>
                    <span className="mx-3">·</span>
                    <Link href="/" className="hover:text-teal-600 transition-colors">{t("btnBack")}</Link>
                </div>
            </footer>
        </div>
    );
}
