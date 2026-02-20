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

// ─── Featured Treatments (top 4 from medical page data) ─────────────────────
type LangMap = Partial<Record<Language, string>>;
const FEATURED_TREATMENTS: { icon: string; name: LangMap & { en: string }; priceTR: number; priceUS: number }[] = [
    {
        icon: "👃", priceTR: 4500, priceUS: 12000,
        name: { en: "Rhinoplasty", ru: "Ринопластика", tr: "Rinoplasti", th: "เสริมจมูก", ar: "تجميل الأنف", zh: "鼻整形" },
    },
    {
        icon: "💆", priceTR: 3000, priceUS: 15000,
        name: { en: "Hair Transplant", ru: "Пересадка волос", tr: "Saç Ekimi", th: "ปลูกผม", ar: "زراعة الشعر", zh: "植发" },
    },
    {
        icon: "🦷", priceTR: 2000, priceUS: 8000,
        name: { en: "Dental Veneers", ru: "Виниры", tr: "Diş Veneerleri", th: "วีเนียร์", ar: "القشرة السنية", zh: "牙贴面" },
    },
    {
        icon: "🍼", priceTR: 4500, priceUS: 20000,
        name: { en: "IVF", ru: "ЭКО / IVF", tr: "Tüp Bebek", th: "IVF", ar: "أطفال الأنابيب", zh: "试管婴儿" },
    },
];

// ─── Trust Items ─────────────────────────────────────────────────────────────
const TRUST_ITEMS = [
    { icon: "🏅", titleKey: "homeWhy1", descKey: "homeWhy1d" },
    { icon: "🗣️", titleKey: "homeWhy2", descKey: "homeWhy2d" },
    { icon: "💎", titleKey: "homeWhy3", descKey: "homeWhy3d" },
    { icon: "🌏", titleKey: "homeWhy4", descKey: "homeWhy4d" },
];

// ─── Homepage Testimonials ──────────────────────────────────────────────────
const HOME_TESTIMONIALS: { name: string; flag: string; procedure: LangMap & { en: string }; text: LangMap & { en: string } }[] = [
    {
        name: "Dmitry K.", flag: "🇷🇺",
        procedure: { en: "Hair Transplant, Istanbul", ru: "Пересадка волос, Стамбул", tr: "Saç Ekimi, İstanbul", th: "ปลูกผม, อิสตันบูล", ar: "زراعة الشعر، إسطنبول", zh: "植发，伊斯坦布尔" },
        text: {
            en: "The entire process was seamless. My coordinator handled everything from airport pickup to post-op care. Results exceeded my expectations.",
            ru: "Весь процесс прошёл безупречно. Координатор организовал всё — от трансфера из аэропорта до послеоперационного ухода. Результат превзошёл ожидания.",
            tr: "Tüm süreç kusursuzdu. Koordinatörüm havalimanı transferinden ameliyat sonrası bakıma kadar her şeyi organize etti. Sonuçlar beklentilerimi aştı.",
            th: "ทุกขั้นตอนราบรื่น ผู้ประสานงานดูแลทุกอย่างตั้งแต่รับสนามบินจนถึงดูแลหลังผ่าตัด ผลลัพธ์เกินความคาดหวัง",
            ar: "كانت العملية بأكملها سلسة. تولى المنسق كل شيء من استقبال المطار حتى الرعاية بعد العملية. النتائج فاقت توقعاتي.",
            zh: "整个过程非常顺畅。协调员从机场接送到术后护理全程处理。效果超出了我的预期。",
        },
    },
    {
        name: "Sarah M.", flag: "🇬🇧",
        procedure: { en: "Rhinoplasty, Antalya", ru: "Ринопластика, Анталья", tr: "Rinoplasti, Antalya", th: "เสริมจมูก, อันตัลยา", ar: "تجميل الأنف، أنطاليا", zh: "鼻整形，安塔利亚" },
        text: {
            en: "I saved over 60% compared to London prices. The clinic was world-class and my follow-up in Phuket was very reassuring.",
            ru: "Я сэкономила более 60% по сравнению с ценами в Лондоне. Клиника мирового уровня, а наблюдение на Пхукете добавило уверенности.",
            tr: "Londra fiyatlarına göre %60'tan fazla tasarruf ettim. Klinik dünya standartlarındaydı ve Phuket'teki takip çok güven vericiydi.",
            th: "ประหยัดกว่า 60% เมื่อเทียบกับราคาในลอนดอน คลินิกมาตรฐานระดับโลกและการติดตามผลที่ภูเก็ตน่าเชื่อถือมาก",
            ar: "وفرت أكثر من 60% مقارنة بأسعار لندن. العيادة كانت عالمية المستوى والمتابعة في بوكيت كانت مطمئنة جداً.",
            zh: "与伦敦价格相比节省了60%以上。诊所世界一流，在普吉岛的随访也很让人放心。",
        },
    },
    {
        name: "Yuki T.", flag: "🇹🇭",
        procedure: { en: "Dental Veneers, Istanbul", ru: "Виниры, Стамбул", tr: "Veneer, İstanbul", th: "วีเนียร์, อิสตันบูล", ar: "قشور الأسنان، إسطنبول", zh: "牙贴面，伊斯坦布尔" },
        text: {
            en: "Living in Phuket, the dual-country model was perfect. Pre-consultation here, treatment in Istanbul, and follow-up back home. Highly recommend!",
            ru: "Живя на Пхукете, модель двух стран оказалась идеальной. Пред-консультация здесь, лечение в Стамбуле, наблюдение дома. Очень рекомендую!",
            tr: "Phuket'te yaşayan biri olarak çift ülke modeli mükemmeldi. Burada ön konsültasyon, İstanbul'da tedavi ve evde takip. Kesinlikle tavsiye ederim!",
            th: "อาศัยอยู่ภูเก็ต โมเดลสองประเทศเหมาะมาก ปรึกษาเบื้องต้นที่นี่ รักษาที่อิสตันบูล ติดตามผลกลับบ้าน แนะนำเลย!",
            ar: "بما أنني أعيش في بوكيت، كان نموذج البلدين مثالياً. استشارة أولية هنا، علاج في إسطنبول، ومتابعة في المنزل. أنصح بشدة!",
            zh: "住在普吉岛，双国模式非常完美。这里初诊，伊斯坦布尔治疗，回家随访。强烈推荐！",
        },
    },
];

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

            {/* ── FEATURED TREATMENTS ─────────────────────────────────── */}
            <section className="section-padding bg-white">
                <div className="container-main">
                    <h2 className="text-2xl sm:text-3xl font-display font-bold text-slate-800 text-center mb-10">
                        {t("homeFeaturedTitle")}
                    </h2>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-5">
                        {FEATURED_TREATMENTS.map((tr) => {
                            const saving = Math.round((1 - tr.priceTR / tr.priceUS) * 100);
                            return (
                                <div key={tr.icon} className="group rounded-2xl border border-slate-100 bg-white p-5 text-center shadow-sm hover:shadow-lg hover:border-cyan-200 transition-all duration-300 hover:-translate-y-1">
                                    <span className="text-3xl block mb-3">{tr.icon}</span>
                                    <h3 className="text-sm font-bold text-slate-800 mb-1">{tr.name[lang] ?? tr.name.en}</h3>
                                    <p className="text-lg font-bold text-cyan-600">${tr.priceTR.toLocaleString()}</p>
                                    <span className="inline-block mt-1.5 text-[11px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full">
                                        -{saving}%
                                    </span>
                                </div>
                            );
                        })}
                    </div>
                    <div className="text-center mt-8">
                        <Link href="/medical"
                            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-sky-500 to-cyan-400 text-white font-bold shadow-md hover:scale-105 transition-all duration-200">
                            {t("homeFeaturedBtn")}
                        </Link>
                    </div>
                </div>
            </section>

            {/* ── TRUST / WHY CHOOSE US ──────────────────────────────── */}
            <section className="section-padding bg-slate-50">
                <div className="container-main">
                    <h2 className="text-2xl sm:text-3xl font-display font-bold text-slate-800 text-center mb-10">
                        {t("homeWhyTitle")}
                    </h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                        {TRUST_ITEMS.map((item, i) => (
                            <div key={i} className="rounded-2xl border border-slate-100 bg-white p-6 shadow-sm hover:shadow-md hover:border-cyan-200 transition-all duration-300">
                                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-sky-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 mb-4">
                                    <span className="text-2xl">{item.icon}</span>
                                </div>
                                <h3 className="text-sm font-bold text-slate-800 mb-2">{t(item.titleKey as Parameters<typeof t>[0])}</h3>
                                <p className="text-xs text-slate-500 leading-relaxed">{t(item.descKey as Parameters<typeof t>[0])}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── TESTIMONIALS ────────────────────────────────────────── */}
            <section className="section-padding bg-white">
                <div className="container-main">
                    <h2 className="text-2xl sm:text-3xl font-display font-bold text-slate-800 text-center mb-10">
                        {t("homeTestimonialsTitle")}
                    </h2>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                        {HOME_TESTIMONIALS.map((rev, i) => (
                            <div key={i} className="rounded-2xl border border-slate-100 bg-white p-6 shadow-sm hover:shadow-md transition-all duration-300">
                                <div className="flex items-center gap-1 mb-3 text-amber-400 text-sm">
                                    {"★★★★★"}
                                </div>
                                <p className="text-sm text-slate-600 leading-relaxed mb-4 italic">
                                    &ldquo;{rev.text[lang] ?? rev.text.en}&rdquo;
                                </p>
                                <div className="flex items-center gap-3">
                                    <div className="w-9 h-9 rounded-full bg-gradient-to-br from-cyan-500 to-sky-600 flex items-center justify-center text-white text-xs font-bold">
                                        {rev.name.charAt(0)}
                                    </div>
                                    <div>
                                        <p className="text-sm font-semibold text-slate-800">{rev.flag} {rev.name}</p>
                                        <p className="text-xs text-slate-400">{rev.procedure[lang] ?? rev.procedure.en}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── FOOTER ───────────────────────────────────────────────────── */}
            <footer className="bg-slate-900 text-white pt-16 pb-8">
                <div className="container-main">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mb-10">
                        {/* Brand */}
                        <div>
                            <div className="flex items-center gap-2.5 mb-4">
                                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-sky-500 to-cyan-400 flex items-center justify-center">
                                    <span className="text-lg">✈️</span>
                                </div>
                                <div>
                                    <span className="text-sm font-bold text-white">AntiGravity</span>
                                    <span className="text-sm font-bold text-cyan-400 ml-1">Medical</span>
                                </div>
                            </div>
                            <p className="text-sm text-slate-400 leading-relaxed max-w-xs">{t("footerTagline")}</p>
                            <div className="flex items-center gap-3 mt-5">
                                <span className="text-[9px] px-2.5 py-1 rounded bg-cyan-900/50 border border-cyan-700/30 text-cyan-400 uppercase tracking-wider font-bold">JCI Partner</span>
                                <span className="text-[9px] px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-slate-400 uppercase tracking-wider font-bold">TURSAB</span>
                            </div>
                        </div>

                        {/* Quick Links */}
                        <div>
                            <h4 className="text-xs text-slate-500 uppercase tracking-widest font-semibold mb-4">Links</h4>
                            <div className="space-y-2 text-sm text-slate-400">
                                <Link href="/medical" className="block hover:text-cyan-400 transition-colors">{t("navMedical")}</Link>
                                <Link href="/travel" className="block hover:text-cyan-400 transition-colors">{t("navTravel")}</Link>
                                <Link href="/factory" className="block hover:text-cyan-400 transition-colors">{t("navFactory")}</Link>
                            </div>
                        </div>

                        {/* Contact */}
                        <div>
                            <h4 className="text-xs text-slate-500 uppercase tracking-widest font-semibold mb-4">Contact</h4>
                            <div className="space-y-3 text-sm text-slate-400">
                                <div className="flex items-center gap-2"><span>📍</span><span>Phuket, Thailand</span></div>
                                <div className="flex items-center gap-2"><span>📍</span><span>Istanbul & Antalya, Turkey</span></div>
                                <div className="flex items-center gap-2"><span>💬</span><span>+66 XX XXX XXXX</span></div>
                                <div className="flex items-center gap-2"><span>📧</span><span>info@antigravity.co</span></div>
                            </div>
                        </div>
                    </div>

                    <div className="border-t border-slate-800 pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-600">
                        <span>&copy; {new Date().getFullYear()} AntiGravity Ventures. All rights reserved.</span>
                        <span className="flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse" />
                            Phuket &amp; Turkey — Active
                        </span>
                    </div>
                </div>
            </footer>
        </div>
    );
}
