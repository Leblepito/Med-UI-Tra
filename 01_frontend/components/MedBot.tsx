"use client";

import { useState, useRef, useEffect, useCallback, useMemo } from "react";
import Link from "next/link";
import { useLanguage } from "../lib/LanguageContext";

// ─── Types ────────────────────────────────────────────────────────────────────
interface Message {
    id: string;
    role: "user" | "bot";
    content: string;
    timestamp: Date;
    isEscalation?: boolean;
}

// ─── Hardcoded FAQ Knowledge Base ────────────────────────────────────────────
const FAQ: Record<string, Record<string, string>> = {
    en: {
        hair: "💆 **Hair Transplant** in Turkey:\n- FUE method: **$1,800–$3,500**\n- 2,000–5,000 grafts per session\n- 9–10 hour procedure\n- Results visible in 8–12 months\n\nWe partner with HairCure Istanbul & EsteNove Clinic (both JCI). Includes airport transfer + hotel. Shall I connect you with a coordinator?",
        rhinoplasty: "👃 **Rhinoplasty (Nose Job)** in Turkey:\n- Cost: **$3,500–$6,000** (vs. $12,000+ in UK/USA)\n- General anesthesia, 2–3h procedure\n- 10–14 day recovery\n- Final result: 6–12 months\n\nPartner hospitals: Memorial Şişli, Acıbadem Maslak (both JCI-accredited). Shall I book a free consultation?",
        dental: "🦷 **Dental Veneers / Smile Design**:\n- E-max porcelain veneers: **$200–$400 per tooth**\n- Full smile (10 teeth): ~$2,000–$4,000\n- 2 sessions over 5–7 days\n- 15-year lifespan\n\nPartner: DentGroup Istanbul. Package includes hotel + transfer. Want to see before/after examples?",
        hospitals: "🏥 **Our Partner Hospitals:**\n\n**Turkey (Istanbul/Antalya):**\n- Memorial Şişli ⭐ 4.8 (JCI)\n- Acıbadem Maslak ⭐ 4.9 (JCI)\n- EsteNove Antalya ⭐ 4.7\n- DentGroup Istanbul ⭐ 4.5\n- HairCure Istanbul ⭐ 4.6\n\n**Thailand (Phuket):**\n- Bangkok Hospital Phuket ⭐ 4.7 (JCI)\n- Siriroj International ⭐ 4.4\n\nAll packages include VIP transfer + personal coordinator.",
        booking: "📅 **How to Book:**\n1. Fill free consultation form on /medical\n2. Coordinator contacts you via WhatsApp in **5 minutes**\n3. We match you to the ideal clinic & create a care plan\n4. Book flights — we arrange hotel + transfers\n5. Treatment in Turkey/Thailand 🏥\n6. Follow-up in Phuket 🌴\n\nFirst consultation is **100% free**. Ready to start?",
        price: "💰 **Price Comparison (vs. Western clinics):**\n- Hair Transplant: $2,500 vs $15,000 → **Save 83%**\n- Rhinoplasty: $5,000 vs $14,000 → **Save 65%**\n- Dental Veneers: $300/tooth vs $1,500 → **Save 80%**\n- Facelift: $8,000 vs $20,000 → **Save 60%**\n- IVF: $3,500 vs $12,000 → **Save 71%**\n\nAll-inclusive packages available. Which procedure interests you?",
    },
    ru: {
        hair: "💆 **Трансплантация волос** в Турции:\n- Метод FUE: **$1,800–$3,500**\n- 2,000–5,000 графтов за сеанс\n- Процедура 9–10 часов\n- Результат через 8–12 месяцев\n\nПартнёры: HairCure Istanbul & EsteNove. Включает трансфер + отель. Хотите записаться?",
        price: "💰 **Сравнение цен (vs. Западные клиники):**\n- Трансплантация волос: $2,500 vs $15,000 → **экономия 83%**\n- Ринопластика: $5,000 vs $14,000 → **65%**\n- Виниры: $300/зуб vs $1,500 → **80%**\n- Подтяжка лица: $8,000 vs $20,000 → **60%**\n\nВсе пакеты «всё включено». Какая процедура интересует?",
        booking: "📅 **Как записаться:**\n1. Заполните форму консультации\n2. Координатор пишет в WhatsApp за **5 минут**\n3. Подбираем клинику и план лечения\n4. Организуем отель и трансфер\n5. Лечение в Турции/Таиланде 🏥\n\nКонсультация **бесплатная**.",
    },
    tr: {
        hair: "💆 **Saç Ekimi** Türkiye'de:\n- FUE yöntemi: **$1,800–$3,500**\n- Oturum başına 2.000–5.000 greft\n- 9–10 saatlik işlem\n- 8–12 ayda sonuç\n\nPartner klinikler: HairCure Istanbul & EsteNove. Havalimanı transferi + otel dahil. Randevu alalım mı?",
        price: "💰 **Fiyat Karşılaştırması:**\n- Saç Ekimi: $2.500 vs $15.000 → **%83 tasarruf**\n- Rinoplasti: $5.000 vs $14.000 → **%65**\n- Veneer: $300/diş vs $1.500 → **%80**\n- Yüz Germe: $8.000 vs $20.000 → **%60**\n\nHangi prosedür ilginizi çekiyor?",
        booking: "📅 **Nasıl Rezervasyon Yapılır:**\n1. /medical formunu doldurun\n2. Koordinatör **5 dakikada** WhatsApp'tan yazar\n3. Ideal kliniği buluruz\n4. Otel + transfer ayarlarız\n\nİlk konsültasyon **ücretsiz**.",
    },
};

function getLocalizedFaq(lang: string): Record<string, string> {
    return { ...FAQ.en, ...((FAQ[lang]) || {}) };
}

// Simple keyword matcher
function matchFaq(text: string, faq: Record<string, string>): string | null {
    const lower = text.toLowerCase();
    if (/hair|saç|волос|шевелюр|植发|شعر|ผม/.test(lower)) return faq.hair ?? null;
    if (/rhino|nose|nase|鼻|أنف|จมูก|ринопластик|burun/.test(lower)) return faq.rhinoplasty ?? null;
    if (/dent|teeth|veneer|smile|зуб|diş|牙|أسنان|ฟัน/.test(lower)) return faq.dental ?? null;
    if (/hospit|clinic|больниц|hastane|医院|مستشفى|โรงพยาบาล/.test(lower)) return faq.hospitals ?? null;
    if (/book|appoint|reserv|записат|randevu|预约|حجز|นัด/.test(lower)) return faq.booking ?? null;
    if (/pric|cost|price|сколько|стоит|fiyat|цена|价格|سعر|ราคา|how much/.test(lower)) return faq.price ?? null;
    return null;
}

function renderMarkdown(text: string): string {
    return text
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/^- (.+)$/gm, '<li class="ml-3 list-disc">$1</li>')
        .replace(/^\d+\. (.+)$/gm, '<li class="ml-3 list-decimal">$1</li>')
        .replace(/\n/g, "<br />");
}

// ─── Component ────────────────────────────────────────────────────────────────
export default function MedBot() {
    const { t, lang, dir } = useLanguage();
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputText, setInputText] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const [msgCount, setMsgCount] = useState(0);
    const [showEscalation, setShowEscalation] = useState(false);
    const endRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    const faq = useMemo(() => getLocalizedFaq(lang), [lang]);

    // Auto-scroll
    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isTyping]);

    // Focus on open
    useEffect(() => {
        if (isOpen && inputRef.current) {
            setTimeout(() => inputRef.current?.focus(), 200);
        }
    }, [isOpen]);

    // Greeting on first open
    const handleOpen = useCallback(() => {
        setIsOpen(true);
        if (messages.length === 0) {
            setMessages([{
                id: "greeting",
                role: "bot",
                content: t("medBotGreeting"),
                timestamp: new Date(),
            }]);
        }
    }, [messages.length, t]);

    const addBotMessage = useCallback((content: string, extra?: Partial<Message>) => {
        setMessages((prev) => [...prev, {
            id: `bot-${Date.now()}`,
            role: "bot",
            content,
            timestamp: new Date(),
            ...extra,
        }]);
    }, []);

    const sendMessage = useCallback(async (text: string) => {
        if (!text.trim() || isTyping) return;

        const userMsg: Message = {
            id: `usr-${Date.now()}`,
            role: "user",
            content: text.trim(),
            timestamp: new Date(),
        };
        setMessages((prev) => [...prev, userMsg]);
        setInputText("");
        setIsTyping(true);

        const newCount = msgCount + 1;
        setMsgCount(newCount);

        // Simulate thinking delay
        await new Promise((r) => setTimeout(r, 800));

        // Try hardcoded FAQ first
        const matched = matchFaq(text, faq);
        if (matched) {
            addBotMessage(matched);
        } else {
            // Fall back to backend
            try {
                const res = await fetch("/api/chat/message", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: text.trim(), language: lang, session_id: "medbot" }),
                });
                if (res.ok) {
                    const data = await res.json();
                    addBotMessage(data.response || t("chatError"));
                } else {
                    addBotMessage("I'd be happy to help! For detailed answers, please use our consultation form or I can connect you with a coordinator. 😊");
                }
            } catch {
                addBotMessage("I'd be happy to help! For detailed answers, please use our consultation form or I can connect you with a coordinator. 😊");
            }
        }

        setIsTyping(false);

        // Show escalation after 2 exchanges
        if (newCount >= 2 && !showEscalation) {
            setShowEscalation(true);
        }
    }, [isTyping, msgCount, faq, lang, addBotMessage, t, showEscalation]);

    const quickActions = useMemo(() => [
        { label: t("medBotQuick1"), value: "hair transplant cost" },
        { label: t("medBotQuick2"), value: "rhinoplasty information" },
        { label: t("medBotQuick3"), value: "partner hospitals list" },
        { label: t("medBotQuick4"), value: "book a consultation" },
    ], [t]);

    if (!isOpen) {
        return (
            <button
                onClick={handleOpen}
                className="fixed bottom-6 right-6 z-50 group"
                aria-label={t("chatOpen")}
            >
                {/* Pulse ring */}
                <span className="absolute inset-0 rounded-full bg-cyan-400 opacity-30 animate-ping" />
                <div className="relative flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-cyan-500 to-sky-600 text-white shadow-xl shadow-cyan-500/40 transition-all duration-300 group-hover:scale-110 group-hover:shadow-2xl group-hover:shadow-cyan-500/50">
                    {/* Stethoscope icon */}
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                    {/* Badge */}
                    <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-emerald-400 border-2 border-white" />
                </div>
                {/* Tooltip */}
                <div className="absolute bottom-full right-0 mb-2 whitespace-nowrap rounded-lg bg-slate-900 text-white text-xs font-semibold px-3 py-1.5 opacity-0 group-hover:opacity-100 transition-opacity duration-200 shadow-lg">
                    {t("medBotName")} — {t("medBotTagline")}
                </div>
            </button>
        );
    }

    return (
        <div
            className={`fixed bottom-0 z-50 flex h-[100dvh] w-full flex-col overflow-hidden border border-slate-200 bg-white shadow-2xl shadow-slate-900/10 sm:bottom-6 sm:h-[620px] sm:max-h-[85vh] sm:w-[400px] sm:rounded-2xl ${dir === "rtl" ? "left-0 sm:left-6" : "right-0 sm:right-6"}`}
            dir={dir}
            role="dialog"
            aria-label={t("medBotName")}
        >
            {/* ── Header ── */}
            <div className="flex items-center justify-between bg-gradient-to-r from-cyan-700 via-cyan-600 to-sky-500 px-4 py-3 text-white">
                <div className="flex items-center gap-3">
                    {/* Avatar */}
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white/20 text-xl font-bold shadow-inner ring-2 ring-white/30">
                        👩‍⚕️
                    </div>
                    <div>
                        <div className="text-sm font-bold leading-tight">{t("medBotName")}</div>
                        <div className="flex items-center gap-1.5 text-[11px] text-cyan-100">
                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                            {t("medBotTagline")}
                        </div>
                    </div>
                </div>
                <div className="flex items-center gap-1">
                    {messages.length > 0 && (
                        <button
                            onClick={() => { setMessages([]); setMsgCount(0); setShowEscalation(false); }}
                            className="rounded-lg p-1.5 hover:bg-white/20 transition-colors"
                            title="Clear"
                        >
                            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                        </button>
                    )}
                    <button
                        onClick={() => setIsOpen(false)}
                        className="rounded-lg p-1.5 hover:bg-white/20 transition-colors"
                    >
                        <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            </div>

            {/* ── Messages ── */}
            <div className="flex-1 overflow-y-auto bg-gradient-to-b from-slate-50/80 to-white px-4 py-3 space-y-3" aria-live="polite">
                {messages.map((msg) => (
                    <div key={msg.id} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                        {msg.role === "bot" && (
                            <div className="mr-2 mt-1 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-cyan-500 to-sky-600 text-sm shadow-md">
                                👩‍⚕️
                            </div>
                        )}
                        <div
                            className={`max-w-[82%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${msg.role === "user"
                                    ? "rounded-br-md bg-gradient-to-br from-cyan-600 to-sky-600 text-white shadow-md"
                                    : "rounded-bl-md border border-slate-100 bg-white text-slate-700 shadow-sm"
                                }`}
                        >
                            {msg.role === "bot" ? (
                                <div
                                    className="whitespace-pre-wrap [&_strong]:font-bold [&_li]:text-sm"
                                    dangerouslySetInnerHTML={{ __html: renderMarkdown(msg.content) }}
                                />
                            ) : (
                                <div>{msg.content}</div>
                            )}
                            <div className={`mt-1 text-[10px] ${msg.role === "user" ? "text-cyan-200" : "text-slate-400"}`}>
                                {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                            </div>
                        </div>
                    </div>
                ))}

                {/* Typing indicator */}
                {isTyping && (
                    <div className="flex justify-start">
                        <div className="mr-2 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-cyan-500 to-sky-600 text-sm">👩‍⚕️</div>
                        <div className="rounded-2xl rounded-bl-md border border-slate-100 bg-white px-4 py-3 shadow-sm">
                            <div className="flex gap-1.5">
                                <span className="h-2 w-2 animate-bounce rounded-full bg-slate-300" style={{ animationDelay: "0ms" }} />
                                <span className="h-2 w-2 animate-bounce rounded-full bg-slate-300" style={{ animationDelay: "150ms" }} />
                                <span className="h-2 w-2 animate-bounce rounded-full bg-slate-300" style={{ animationDelay: "300ms" }} />
                            </div>
                        </div>
                    </div>
                )}

                {/* Escalation card */}
                {showEscalation && !isTyping && (
                    <div className="rounded-xl border border-cyan-200 bg-cyan-50 p-3 text-center">
                        <p className="text-xs text-slate-600 mb-2">{t("medBotEscalation")}</p>
                        <Link
                            href="/medical#consultation"
                            className="inline-flex items-center gap-1.5 rounded-lg bg-cyan-600 px-4 py-2 text-xs font-bold text-white hover:bg-cyan-700 transition-colors"
                        >
                            📞 {t("medBotEscalationBtn")}
                        </Link>
                    </div>
                )}

                <div ref={endRef} />
            </div>

            {/* ── Quick Actions ── */}
            {messages.length <= 1 && !isTyping && (
                <div className="border-t border-slate-100 bg-white px-3 py-2">
                    <p className="text-[10px] text-slate-400 uppercase font-semibold tracking-wider mb-1.5">Quick questions</p>
                    <div className="grid grid-cols-2 gap-1.5">
                        {quickActions.map(({ label, value }) => (
                            <button
                                key={label}
                                onClick={() => sendMessage(value)}
                                className="rounded-lg border border-cyan-200 bg-cyan-50 px-2.5 py-1.5 text-left text-[11px] font-semibold text-cyan-700 hover:bg-cyan-100 hover:border-cyan-300 transition-colors leading-tight"
                            >
                                {label}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* ── Input ── */}
            <form
                onSubmit={(e) => { e.preventDefault(); sendMessage(inputText); }}
                className="flex items-center gap-2 border-t border-slate-100 bg-white px-4 py-3"
            >
                <label htmlFor="medbot-input" className="sr-only">Message</label>
                <input
                    id="medbot-input"
                    ref={inputRef}
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder={t("chatPlaceholder")}
                    disabled={isTyping}
                    className="flex-1 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm text-slate-800 placeholder:text-slate-400 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/20 disabled:opacity-50 transition-all"
                    dir={dir}
                />
                <button
                    type="submit"
                    disabled={!inputText.trim() || isTyping}
                    className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-600 to-sky-600 text-white hover:scale-105 transition-all disabled:opacity-40 shadow-md shadow-cyan-500/20"
                >
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                    </svg>
                </button>
            </form>

            {/* Trust footer */}
            <div className="bg-slate-50 border-t border-slate-100 px-4 py-2 text-center">
                <p className="text-[10px] text-slate-400">🔒 Secure · 🏥 JCI Accredited Partners · 🌍 6 Languages</p>
            </div>
        </div>
    );
}
