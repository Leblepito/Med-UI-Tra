"use client";

/**
 * AntiGravity ThaiTurk — Language Picker Component
 *
 * variant="compact"  → Small flag+code buttons (used in Navbar / header)
 * variant="full"     → Large cards with flag, native name and English name
 *                       (used on entry / welcome screen)
 */

import { type Language, LANGUAGES } from "../lib/i18n";
import { useLanguage } from "../lib/LanguageContext";

// ─────────────────────────────────────────────────────────────────────────────
interface LanguagePickerProps {
    variant?: "compact" | "full";
    onPick?: (lang: Language) => void; // optional callback after selection
    className?: string;
}

export default function LanguagePicker({
    variant = "compact",
    onPick,
    className = "",
}: LanguagePickerProps) {
    const { lang, setLang } = useLanguage();

    const handleSelect = (l: Language) => {
        setLang(l);
        onPick?.(l);
    };

    // ── FULL MODE (entry screen) ─────────────────────────────────────────────
    if (variant === "full") {
        return (
            <div className={`grid grid-cols-2 sm:grid-cols-3 gap-3 ${className}`}>
                {(Object.entries(LANGUAGES) as [Language, (typeof LANGUAGES)[Language]][]).map(
                    ([code, meta]) => {
                        const active = lang === code;
                        return (
                            <button
                                key={code}
                                type="button"
                                onClick={() => handleSelect(code)}
                                className={`
                                    group flex flex-col items-center gap-2 rounded-2xl border-2 py-5 px-4
                                    transition-all duration-200 cursor-pointer select-none
                                    ${active
                                        ? "border-sky-500 bg-sky-500/10 shadow-lg shadow-sky-500/20 scale-[1.03]"
                                        : "border-white/10 bg-white/5 hover:border-white/25 hover:bg-white/10 hover:scale-[1.02]"
                                    }
                                `}
                            >
                                {/* Flag */}
                                <span className="text-4xl leading-none">{meta.flag}</span>

                                {/* Native name */}
                                <span
                                    className={`text-sm font-bold leading-tight text-center ${active ? "text-white" : "text-slate-200"}`}
                                    dir={meta.dir}
                                >
                                    {meta.native}
                                </span>

                                {/* English label */}
                                <span className={`text-[11px] uppercase tracking-widest font-semibold ${active ? "text-sky-300" : "text-slate-400"}`}>
                                    {meta.label}
                                </span>

                                {active && (
                                    <span className="mt-0.5 h-1.5 w-1.5 rounded-full bg-sky-400 animate-pulse" />
                                )}
                            </button>
                        );
                    }
                )}
            </div>
        );
    }

    // ── COMPACT MODE (header / navbar) ───────────────────────────────────────
    return (
        <div className={`flex items-center gap-0.5 bg-slate-50 dark:bg-white/5 rounded-lg p-0.5 border border-slate-200 dark:border-white/10 ${className}`}>
            {(Object.entries(LANGUAGES) as [Language, (typeof LANGUAGES)[Language]][]).map(
                ([code, meta]) => {
                    const active = lang === code;
                    return (
                        <button
                            key={code}
                            type="button"
                            title={meta.native}
                            onClick={() => handleSelect(code)}
                            className={`
                                px-2 py-1 rounded-md text-[11px] font-bold uppercase tracking-wider
                                transition-all duration-200 flex items-center gap-1
                                ${active
                                    ? "bg-white dark:bg-white/20 text-sky-700 dark:text-sky-300 shadow-sm border border-slate-200 dark:border-white/20"
                                    : "text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300"
                                }
                            `}
                        >
                            <span className="text-base leading-none">{meta.flag}</span>
                            <span className="hidden sm:inline">{code.toUpperCase()}</span>
                        </button>
                    );
                }
            )}
        </div>
    );
}
