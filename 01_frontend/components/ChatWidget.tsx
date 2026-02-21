"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { useLanguage } from "../lib/LanguageContext";

// ──────────────────────────────────────────────────────────────────────────
// Types
// ──────────────────────────────────────────────────────────────────────────

interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
    timestamp: string;
}

interface SessionResponse {
    session_id: string;
    greeting: string;
    language: string;
}

interface MessageResponse {
    session_id: string;
    message_id: string;
    response: string;
    tool_results: Record<string, unknown>[];
    tokens_used: { input: number; output: number };
    timestamp: string;
}

// ──────────────────────────────────────────────────────────────────────────
// API helpers (inline to avoid circular imports)
// ──────────────────────────────────────────────────────────────────────────

async function chatStartSession(language: string): Promise<SessionResponse> {
    const res = await fetch("/api/chat/session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language }),
    });
    if (!res.ok) throw new Error(`API ${res.status}`);
    return res.json();
}

async function chatSendMessage(
    session_id: string,
    message: string,
    language: string,
): Promise<MessageResponse> {
    const res = await fetch("/api/chat/message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id, message, language }),
    });
    if (!res.ok) throw new Error(`API ${res.status}`);
    return res.json();
}

// ──────────────────────────────────────────────────────────────────────────
// Component
// ──────────────────────────────────────────────────────────────────────────

export default function ChatWidget() {
    const { t, lang, dir } = useLanguage();
    const [isOpen, setIsOpen] = useState(false);
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputText, setInputText] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isLoading]);

    // Focus input when opened
    useEffect(() => {
        if (isOpen && inputRef.current) {
            setTimeout(() => inputRef.current?.focus(), 200);
        }
    }, [isOpen]);

    // Start session when widget opens
    const handleOpen = useCallback(async () => {
        setIsOpen(true);
        if (!sessionId) {
            try {
                const res = await chatStartSession(lang);
                setSessionId(res.session_id);
                setMessages([
                    {
                        id: "greeting",
                        role: "assistant",
                        content: res.greeting,
                        timestamp: new Date().toISOString(),
                    },
                ]);
            } catch {
                setMessages([
                    {
                        id: "err-init",
                        role: "assistant",
                        content: t("chatError"),
                        timestamp: new Date().toISOString(),
                    },
                ]);
            }
        }
    }, [sessionId, lang, t]);

    // Send message
    const handleSend = useCallback(async () => {
        const text = inputText.trim();
        if (!text || !sessionId || isLoading) return;

        const userMsg: Message = {
            id: `usr-${Date.now()}`,
            role: "user",
            content: text,
            timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, userMsg]);
        setInputText("");
        setIsLoading(true);

        try {
            const res = await chatSendMessage(sessionId, text, lang);
            setMessages((prev) => [
                ...prev,
                {
                    id: res.message_id,
                    role: "assistant",
                    content: res.response,
                    timestamp: res.timestamp,
                },
            ]);
        } catch {
            setMessages((prev) => [
                ...prev,
                {
                    id: `err-${Date.now()}`,
                    role: "assistant",
                    content: t("chatError"),
                    timestamp: new Date().toISOString(),
                },
            ]);
        } finally {
            setIsLoading(false);
        }
    }, [inputText, sessionId, isLoading, lang, t]);

    // Quick action
    const handleQuickAction = useCallback(
        (value: string) => {
            if (!sessionId || isLoading) return;
            setInputText(value);
        },
        [sessionId, isLoading],
    );

    // Quick actions data
    const quickActions = [
        { label: t("chatQuickPricing"), value: t("chatQuickPricingValue") },
        { label: t("chatQuickHospitals"), value: t("chatQuickHospitalsValue") },
        { label: t("chatQuickBooking"), value: t("chatQuickBookingValue") },
    ];

    // ── RENDER ─────────────────────────────────────────────────────────────

    return (
        <>
            {/* ─── Floating Bubble ─── */}
            {!isOpen && (
                <button
                    onClick={handleOpen}
                    className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center
                               rounded-full bg-gradient-to-br from-cyan-500 to-cyan-600
                               text-white shadow-lg shadow-cyan-500/30
                               transition-all duration-300
                               hover:scale-105 hover:shadow-xl hover:shadow-cyan-500/40"
                    aria-label={t("chatOpen")}
                >
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                        />
                    </svg>
                </button>
            )}

            {/* ─── Chat Panel ─── */}
            {isOpen && (
                <div
                    className={`fixed bottom-0 z-50 flex h-[100dvh] w-full flex-col overflow-hidden
                               border border-slate-200 bg-white shadow-2xl shadow-slate-900/10
                               sm:bottom-6 sm:h-[600px] sm:max-h-[80vh] sm:w-[400px] sm:rounded-2xl
                               ${dir === "rtl" ? "left-0 sm:left-6" : "right-0 sm:right-6"}`}
                    dir={dir}
                >
                    {/* ── Header ── */}
                    <div className="flex items-center justify-between bg-gradient-to-r from-cyan-600 to-cyan-500 px-4 py-3 text-white">
                        <div className="flex items-center gap-3">
                            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-white/20">
                                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                                    />
                                </svg>
                            </div>
                            <div>
                                <div className="text-sm font-bold">{t("chatTitle")}</div>
                                <div className="flex items-center gap-1 text-[11px] text-cyan-100">
                                    <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-green-400" />
                                    {t("chatOnline")}
                                </div>
                            </div>
                        </div>
                        <button
                            onClick={() => setIsOpen(false)}
                            className="rounded-lg p-1.5 transition-colors hover:bg-white/20"
                            aria-label="Close chat"
                        >
                            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    {/* ── Messages ── */}
                    <div className="flex-1 space-y-3 overflow-y-auto bg-slate-50/50 px-4 py-3">
                        {messages.map((msg) => (
                            <div key={msg.id} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                                <div
                                    className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
                                        msg.role === "user"
                                            ? "rounded-br-md bg-cyan-600 text-white"
                                            : "rounded-bl-md border border-slate-100 bg-white text-slate-700 shadow-sm"
                                    }`}
                                >
                                    <div className="whitespace-pre-wrap">{msg.content}</div>
                                    <div className={`mt-1 text-[10px] ${msg.role === "user" ? "text-cyan-200" : "text-slate-400"}`}>
                                        {new Date(msg.timestamp).toLocaleTimeString([], {
                                            hour: "2-digit",
                                            minute: "2-digit",
                                        })}
                                    </div>
                                </div>
                            </div>
                        ))}

                        {/* Typing indicator */}
                        {isLoading && (
                            <div className="flex justify-start">
                                <div className="rounded-2xl rounded-bl-md border border-slate-100 bg-white px-4 py-3 shadow-sm">
                                    <div className="flex gap-1.5">
                                        <span className="h-2 w-2 animate-bounce rounded-full bg-slate-300" style={{ animationDelay: "0ms" }} />
                                        <span className="h-2 w-2 animate-bounce rounded-full bg-slate-300" style={{ animationDelay: "150ms" }} />
                                        <span className="h-2 w-2 animate-bounce rounded-full bg-slate-300" style={{ animationDelay: "300ms" }} />
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* ── Quick Actions (shown at start) ── */}
                    {messages.length <= 1 && !isLoading && (
                        <div className="flex gap-2 overflow-x-auto border-t border-slate-100 bg-white px-4 py-2">
                            {quickActions.map(({ label, value }) => (
                                <button
                                    key={label}
                                    onClick={() => handleQuickAction(value)}
                                    className="shrink-0 rounded-full border border-cyan-200 bg-cyan-50 px-3 py-1.5
                                               text-xs font-semibold text-cyan-700
                                               transition-colors hover:border-cyan-300 hover:bg-cyan-100"
                                >
                                    {label}
                                </button>
                            ))}
                        </div>
                    )}

                    {/* ── Input ── */}
                    <form
                        onSubmit={(e) => {
                            e.preventDefault();
                            handleSend();
                        }}
                        className="flex items-center gap-2 border-t border-slate-100 bg-white px-4 py-3"
                    >
                        <input
                            ref={inputRef}
                            type="text"
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === "Enter" && !e.shiftKey) {
                                    e.preventDefault();
                                    handleSend();
                                }
                            }}
                            placeholder={t("chatPlaceholder")}
                            disabled={isLoading || !sessionId}
                            className="flex-1 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5
                                       text-sm text-slate-800 placeholder:text-slate-400
                                       transition-all focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/20
                                       disabled:opacity-50"
                            dir={dir}
                        />
                        <button
                            type="submit"
                            disabled={!inputText.trim() || isLoading || !sessionId}
                            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl
                                       bg-cyan-600 text-white transition-all
                                       hover:bg-cyan-700 disabled:opacity-40"
                        >
                            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d={dir === "rtl" ? "M10 19l-7-7m0 0l7-7m-7 7h18" : "M14 5l7 7m0 0l-7 7m7-7H3"}
                                />
                            </svg>
                        </button>
                    </form>
                </div>
            )}
        </>
    );
}
