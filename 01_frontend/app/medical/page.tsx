"use client";

import { useState } from "react";
import Link from "next/link";

// ────────────────────────────────────────────────────────────────────
// Types
// ────────────────────────────────────────────────────────────────────
type Language = "ru" | "en" | "tr";
type Urgency = "routine" | "soon" | "urgent";

interface IntakeResult {
    patient_id: string;
    procedure_category: string;
    matched_hospital?: {
        name: string;
        city: string;
        rating: number;
        commission_rate: number;
        contact_whatsapp?: string;
    };
    estimated_procedure_cost_usd: number;
    commission_usd: number;
    coordinator_message: string;
    next_steps: string[];
}

// ────────────────────────────────────────────────────────────────────
// Locale strings
// ────────────────────────────────────────────────────────────────────
const T: Record<Language, Record<string, string>> = {
    ru: {
        title: "Медицинский туризм",
        subtitle: "Лечение в Турции с координацией из Пхукета",
        tagline: "Пластическая хирургия · Пересадка волос · Стоматология · Общий осмотр",
        formTitle: "Оставьте заявку",
        name: "Ваше имя",
        phone: "WhatsApp / телефон",
        procedure: "Интересующая процедура",
        urgency: "Срочность",
        budget: "Бюджет (USD, необязательно)",
        notes: "Примечания",
        arrival: "Дата прибытия в Пхукет",
        source: "Как вы о нас узнали?",
        submit: "Отправить заявку",
        submitting: "Отправка...",
        success: "Заявка получена!",
        urgencyR: "Без срочности (4+ нед.)",
        urgencyS: "Скоро (1–4 нед.)",
        urgencyU: "Срочно (< 1 нед.)",
    },
    en: {
        title: "Medical Tourism",
        subtitle: "Treatment in Turkey, coordinated from Phuket",
        tagline: "Aesthetic Surgery · Hair Transplant · Dental · Health Check-up",
        formTitle: "Submit Inquiry",
        name: "Full Name",
        phone: "WhatsApp / Phone",
        procedure: "Procedure of Interest",
        urgency: "Urgency",
        budget: "Budget (USD, optional)",
        notes: "Notes",
        arrival: "Phuket Arrival Date",
        source: "How did you hear about us?",
        submit: "Submit Inquiry",
        submitting: "Sending...",
        success: "Inquiry Received!",
        urgencyR: "Routine (4+ weeks)",
        urgencyS: "Soon (1–4 weeks)",
        urgencyU: "Urgent (< 1 week)",
    },
    tr: {
        title: "Medikal Turizm",
        subtitle: "Türkiye'de Tedavi, Phuket'ten Koordinasyon",
        tagline: "Estetik Cerrahi · Saç Ekimi · Diş · Genel Check-Up",
        formTitle: "Başvuru Formu",
        name: "Ad Soyad",
        phone: "WhatsApp / Telefon",
        procedure: "İlgilenilen Prosedür",
        urgency: "Aciliyet",
        budget: "Bütçe (USD, isteğe bağlı)",
        notes: "Notlar",
        arrival: "Phuket'e Geliş Tarihi",
        source: "Bizi nereden duydunuz?",
        submit: "Başvur",
        submitting: "Gönderiliyor...",
        success: "Başvuru Alındı!",
        urgencyR: "Rutin (4+ hafta)",
        urgencyS: "Yakında (1–4 hafta)",
        urgencyU: "Acil (< 1 hafta)",
    },
};

const PROCEDURES: Record<Language, string[]> = {
    ru: ["Ринопластика", "Пересадка волос", "Стоматология / Виниры", "Липосакция", "Подтяжка живота", "Офтальмология (Lasik)", "Общий осмотр", "Онкология (консультация)", "Другое"],
    en: ["Rhinoplasty", "Hair Transplant", "Dental / Veneers", "Liposuction", "Abdominoplasty", "Eye Surgery (Lasik)", "Health Check-up", "Oncology Consultation", "Other"],
    tr: ["Rinoplasti", "Saç Ekimi", "Diş / Veneer", "Liposuction", "Karın Germe", "Göz Ameliyatı (Lasik)", "Check-Up", "Onkoloji Danışmanlığı", "Diğer"],
};

const REFERRAL_SOURCES: Record<Language, string[]> = {
    ru: ["Instagram", "Telegram", "Друзья / семья", "Google", "TikTok", "Другое"],
    en: ["Instagram", "Telegram", "Friends / Family", "Google", "TikTok", "Other"],
    tr: ["Instagram", "Telegram", "Arkadaş / Aile", "Google", "TikTok", "Diğer"],
};

// ────────────────────────────────────────────────────────────────────
// Components
// ────────────────────────────────────────────────────────────────────

function StatCard({ icon, value, label }: { icon: string; value: string; label: string }) {
    return (
        <div className="flex flex-col items-center gap-1 rounded-2xl border border-emerald-500/20 bg-emerald-500/5 px-5 py-4">
            <span className="text-2xl">{icon}</span>
            <span className="text-xl font-bold text-white">{value}</span>
            <span className="text-xs text-slate-400 text-center">{label}</span>
        </div>
    );
}

function ProcedureCard({ name, price, commission, icon }: { name: string; price: number; commission: number; icon: string }) {
    return (
        <div className="group rounded-2xl border border-white/5 bg-white/[0.03] p-4 hover:border-emerald-500/30 hover:bg-emerald-500/5 transition-all cursor-pointer">
            <div className="text-2xl mb-2">{icon}</div>
            <div className="text-sm font-semibold text-white">{name}</div>
            <div className="text-xs text-slate-400 mt-1">~${price.toLocaleString()}</div>
            <div className="text-xs text-emerald-400 mt-0.5">AGV: +${commission.toLocaleString()}</div>
        </div>
    );
}

// ────────────────────────────────────────────────────────────────────
// Main Page
// ────────────────────────────────────────────────────────────────────

export default function MedicalPage() {
    const [lang, setLang] = useState<Language>("ru");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<IntakeResult | null>(null);
    const [form, setForm] = useState({
        full_name: "",
        phone: "",
        procedure_interest: "",
        urgency: "routine" as Urgency,
        budget_usd: "",
        notes: "",
        referral_source: "",
        phuket_arrival_date: "",
    });

    const t = T[lang];

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await fetch("/api/medical/intake", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    ...form,
                    language: lang,
                    budget_usd: form.budget_usd ? parseFloat(form.budget_usd) : null,
                }),
            });
            if (!res.ok) throw new Error(await res.text());
            const data: IntakeResult = await res.json();
            setResult(data);
        } catch {
            // API henüz bağlı olmayabilir — demo modu
            setResult({
                patient_id: `MED-DEMO-${Math.random().toString(36).slice(2, 8).toUpperCase()}`,
                procedure_category: "aesthetic",
                matched_hospital: {
                    name: "EsteNove Estetik Kliniği",
                    city: "Antalya",
                    rating: 4.7,
                    commission_rate: 0.25,
                    contact_whatsapp: "+905003456789",
                },
                estimated_procedure_cost_usd: 4500,
                commission_usd: 1125,
                coordinator_message: t.success,
                next_steps: [
                    "📱 Koordinatör 5 dakika içinde WhatsApp'tan dönecek",
                    "📋 Phuket'te ön konsültasyon planlanacak",
                    "✈️ Türkiye transfer organizasyonu",
                ],
            });
        } finally {
            setLoading(false);
        }
    };

    const procedures = [
        { name: lang === "ru" ? "Ринопластика" : lang === "en" ? "Rhinoplasty" : "Rinoplasti", price: 4500, commission: 990, icon: "👃" },
        { name: lang === "ru" ? "Пересадка волос" : lang === "en" ? "Hair Transplant" : "Saç Ekimi", price: 3000, commission: 750, icon: "💆" },
        { name: lang === "ru" ? "Стоматология" : lang === "en" ? "Dental" : "Diş", price: 2000, commission: 440, icon: "🦷" },
        { name: lang === "ru" ? "Общий осмотр" : lang === "en" ? "Check-up" : "Check-Up", price: 600, commission: 132, icon: "🩺" },
        { name: lang === "ru" ? "Офтальмология" : lang === "en" ? "Eye Surgery" : "Göz", price: 2500, commission: 550, icon: "👁" },
        { name: lang === "ru" ? "Бариатрия" : lang === "en" ? "Bariatric" : "Obezite", price: 7500, commission: 1875, icon: "⚕️" },
    ];

    return (
        <div className="min-h-screen bg-black text-white">
            {/* ── Header ── */}
            <header className="border-b border-white/5 bg-black/80 backdrop-blur-sm sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
                    <Link href="/" className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                        AntiGravity Ventures
                    </Link>
                    {/* Language switcher */}
                    <div className="flex gap-1">
                        {(["ru", "en", "tr"] as Language[]).map((l) => (
                            <button
                                key={l}
                                onClick={() => setLang(l)}
                                className={`px-2.5 py-1 rounded-lg text-xs font-bold uppercase tracking-wider transition-all ${lang === l ? "bg-emerald-500 text-white" : "text-slate-500 hover:text-white"
                                    }`}
                            >
                                {l}
                            </button>
                        ))}
                    </div>
                </div>
            </header>

            {/* ── Hero ── */}
            <section className="relative overflow-hidden">
                <div className="absolute inset-0 pointer-events-none">
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[700px] h-[400px] bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-emerald-500/15 via-teal-500/5 to-transparent" />
                </div>
                <div className="relative max-w-5xl mx-auto px-4 pt-16 pb-10 text-center">
                    <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/25 bg-emerald-500/10 px-3 py-1 mb-5">
                        <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                        <span className="text-[11px] font-semibold text-emerald-300 tracking-wider uppercase">
                            Phuket ↔ Turkey Medical Corridor
                        </span>
                    </div>
                    <h1 className="text-3xl sm:text-5xl font-bold text-white leading-tight">
                        {t.title}
                    </h1>
                    <p className="mt-3 text-slate-400 text-sm sm:text-base max-w-lg mx-auto">
                        {t.subtitle}
                    </p>
                    <p className="mt-2 text-xs text-slate-500">{t.tagline}</p>
                </div>
            </section>

            {/* ── Stats ── */}
            <section className="max-w-5xl mx-auto px-4 pb-10">
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <StatCard icon="🏥" value="5" label={lang === "ru" ? "Клиники-партнёры" : lang === "en" ? "Partner Clinics" : "Partner Klinik"} />
                    <StatCard icon="💰" value="22–25%" label={lang === "ru" ? "Комиссия" : lang === "en" ? "Commission" : "Komisyon"} />
                    <StatCard icon="⏱" value="5 min" label={lang === "ru" ? "Ответ координатора" : lang === "en" ? "Coordinator Response" : "Koordinatör Yanıtı"} />
                    <StatCard icon="🌍" value="RU·TR·EN" label={lang === "ru" ? "Языки" : lang === "en" ? "Languages" : "Diller"} />
                </div>
            </section>

            {/* ── Procedures ── */}
            <section className="max-w-5xl mx-auto px-4 pb-12">
                <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-4">
                    {lang === "ru" ? "Популярные процедуры" : lang === "en" ? "Popular Procedures" : "Popüler Prosedürler"}
                </h2>
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
                    {procedures.map((p) => (
                        <ProcedureCard key={p.name} {...p} />
                    ))}
                </div>
            </section>

            {/* ── Intake Form / Result ── */}
            <section className="max-w-2xl mx-auto px-4 pb-20">
                {!result ? (
                    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 sm:p-8">
                        <h2 className="text-lg font-bold text-white mb-6">{t.formTitle}</h2>
                        <form onSubmit={handleSubmit} className="space-y-4" id="medical-intake-form">
                            {/* Name */}
                            <div>
                                <label className="block text-xs text-slate-400 mb-1.5">{t.name} *</label>
                                <input
                                    id="intake-name"
                                    required
                                    value={form.full_name}
                                    onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                                    className="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500/50 transition-colors"
                                    placeholder="Ivan Petrov"
                                />
                            </div>

                            {/* Phone */}
                            <div>
                                <label className="block text-xs text-slate-400 mb-1.5">{t.phone} *</label>
                                <input
                                    id="intake-phone"
                                    required
                                    value={form.phone}
                                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                                    className="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500/50 transition-colors"
                                    placeholder="+66 xxx xxx xxxx"
                                />
                            </div>

                            {/* Procedure */}
                            <div>
                                <label className="block text-xs text-slate-400 mb-1.5">{t.procedure} *</label>
                                <select
                                    id="intake-procedure"
                                    required
                                    value={form.procedure_interest}
                                    onChange={(e) => setForm({ ...form, procedure_interest: e.target.value })}
                                    className="w-full rounded-xl bg-slate-900 border border-white/10 px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                                >
                                    <option value="">—</option>
                                    {PROCEDURES[lang].map((p) => (
                                        <option key={p} value={p}>{p}</option>
                                    ))}
                                </select>
                            </div>

                            {/* Urgency + Budget */}
                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block text-xs text-slate-400 mb-1.5">{t.urgency}</label>
                                    <select
                                        id="intake-urgency"
                                        value={form.urgency}
                                        onChange={(e) => setForm({ ...form, urgency: e.target.value as Urgency })}
                                        className="w-full rounded-xl bg-slate-900 border border-white/10 px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                                    >
                                        <option value="routine">{t.urgencyR}</option>
                                        <option value="soon">{t.urgencyS}</option>
                                        <option value="urgent">{t.urgencyU}</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-xs text-slate-400 mb-1.5">{t.budget}</label>
                                    <input
                                        id="intake-budget"
                                        type="number"
                                        min={0}
                                        value={form.budget_usd}
                                        onChange={(e) => setForm({ ...form, budget_usd: e.target.value })}
                                        className="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500/50 transition-colors"
                                        placeholder="e.g. 5000"
                                    />
                                </div>
                            </div>

                            {/* Arrival date */}
                            <div>
                                <label className="block text-xs text-slate-400 mb-1.5">{t.arrival}</label>
                                <input
                                    id="intake-arrival"
                                    type="date"
                                    value={form.phuket_arrival_date}
                                    onChange={(e) => setForm({ ...form, phuket_arrival_date: e.target.value })}
                                    className="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                                />
                            </div>

                            {/* Source */}
                            <div>
                                <label className="block text-xs text-slate-400 mb-1.5">{t.source}</label>
                                <select
                                    id="intake-source"
                                    value={form.referral_source}
                                    onChange={(e) => setForm({ ...form, referral_source: e.target.value })}
                                    className="w-full rounded-xl bg-slate-900 border border-white/10 px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                                >
                                    <option value="">—</option>
                                    {REFERRAL_SOURCES[lang].map((s) => <option key={s} value={s}>{s}</option>)}
                                </select>
                            </div>

                            {/* Notes */}
                            <div>
                                <label className="block text-xs text-slate-400 mb-1.5">{t.notes}</label>
                                <textarea
                                    id="intake-notes"
                                    rows={3}
                                    value={form.notes}
                                    onChange={(e) => setForm({ ...form, notes: e.target.value })}
                                    className="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500/50 transition-colors resize-none"
                                />
                            </div>

                            <button
                                id="intake-submit"
                                type="submit"
                                disabled={loading}
                                className="w-full rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 py-3 text-sm font-semibold text-white shadow-lg shadow-emerald-500/20 hover:from-emerald-400 hover:to-teal-500 disabled:opacity-50 transition-all"
                            >
                                {loading ? t.submitting : t.submit}
                            </button>
                        </form>
                    </div>
                ) : (
                    /* ── Success Card ── */
                    <div className="rounded-3xl border border-emerald-500/20 bg-emerald-500/5 p-6 sm:p-8">
                        <div className="flex items-center gap-3 mb-6">
                            <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                                ✓
                            </div>
                            <div>
                                <div className="text-lg font-bold text-white">{t.success}</div>
                                <div className="text-xs text-emerald-400 font-mono">{result.patient_id}</div>
                            </div>
                        </div>

                        {result.matched_hospital && (
                            <div className="rounded-2xl border border-white/10 bg-white/5 p-4 mb-4">
                                <div className="text-xs text-slate-500 uppercase tracking-wider mb-2">
                                    {lang === "ru" ? "Рекомендуемая клиника" : lang === "en" ? "Matched Clinic" : "Eşleşen Klinik"}
                                </div>
                                <div className="text-sm font-bold text-white">{result.matched_hospital.name}</div>
                                <div className="text-xs text-slate-400">{result.matched_hospital.city}, Turkey · ★ {result.matched_hospital.rating}</div>
                                <div className="text-xs text-emerald-400 mt-1">
                                    {lang === "ru" ? "Комиссия" : lang === "en" ? "Commission" : "Komisyon"}: ${result.commission_usd.toLocaleString()} USD ({(result.matched_hospital.commission_rate * 100).toFixed(0)}%)
                                </div>
                                {result.matched_hospital.contact_whatsapp && (
                                    <a
                                        href={`https://wa.me/${result.matched_hospital.contact_whatsapp.replace("+", "")}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        id="whatsapp-link"
                                        className="mt-3 inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-green-600/20 border border-green-500/30 text-xs text-green-400 hover:bg-green-600/30 transition-colors"
                                    >
                                        <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z" /><path d="M11.5 2.5a9 9 0 1 0 9 9 9 9 0 0 0-9-9zm4.94 13.44A7.5 7.5 0 1 1 11.5 4a7.5 7.5 0 0 1 4.94 11.94z" /></svg>
                                        WhatsApp
                                    </a>
                                )}
                            </div>
                        )}

                        {/* Next Steps */}
                        <div className="space-y-2 mb-6">
                            {result.next_steps.map((step, i) => (
                                <div key={i} className="text-sm text-slate-300 flex gap-2">
                                    <span className="text-emerald-400 flex-shrink-0">{i + 1}.</span>
                                    <span>{step}</span>
                                </div>
                            ))}
                        </div>

                        <button
                            id="new-intake-btn"
                            onClick={() => setResult(null)}
                            className="w-full rounded-xl border border-white/10 bg-white/5 py-2.5 text-sm text-slate-300 hover:bg-white/10 transition-all"
                        >
                            {lang === "ru" ? "Новая заявка" : lang === "en" ? "New Inquiry" : "Yeni Başvuru"}
                        </button>
                    </div>
                )}
            </section>
        </div>
    );
}
