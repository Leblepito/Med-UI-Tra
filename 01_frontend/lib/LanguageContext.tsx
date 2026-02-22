"use client";

/**
 * AntiGravity ThaiTurk — Language Context
 * Provides global language state with localStorage persistence.
 * Updates <html lang> and dir attributes automatically.
 */

import {
    createContext,
    useContext,
    useState,
    useEffect,
    useCallback,
    type ReactNode,
} from "react";
import { type Language, LANGUAGES, translations, getDir, t as translate } from "./i18n";
export type { Language };

// ─────────────────────────────────────────────────────────────────────────────
const STORAGE_KEY = "thaiturk_lang";
const DEFAULT_LANG: Language = "en";

// ─────────────────────────────────────────────────────────────────────────────
interface LanguageContextValue {
    lang: Language;
    setLang: (lang: Language) => void;
    t: (key: Parameters<typeof translate>[1]) => string;
    dir: "ltr" | "rtl";
}

const LanguageContext = createContext<LanguageContextValue | null>(null);

// ─────────────────────────────────────────────────────────────────────────────
// Provider
// ─────────────────────────────────────────────────────────────────────────────
export function LanguageProvider({ children }: { children: ReactNode }) {
    const [lang, setLangState] = useState<Language>(DEFAULT_LANG);
    const [mounted, setMounted] = useState(false);

    // Hydrate from localStorage after mount
    useEffect(() => {
        const stored = localStorage.getItem(STORAGE_KEY) as Language | null;
        if (stored && stored in LANGUAGES) {
            // Intentional: hydrate from localStorage on mount — runs once, not cascading
            // eslint-disable-next-line react-hooks/set-state-in-effect
            setLangState(stored);
        }
        setMounted(true);
    }, []);

    // Sync <html lang> and dir on language change
    useEffect(() => {
        if (!mounted) return;
        const dir = getDir(lang);
        document.documentElement.lang = lang;
        document.documentElement.dir = dir;
    }, [lang, mounted]);

    const setLang = useCallback((newLang: Language) => {
        if (!(newLang in LANGUAGES)) return;
        setLangState(newLang);
        localStorage.setItem(STORAGE_KEY, newLang);
    }, []);

    const tFn = useCallback(
        (key: Parameters<typeof translate>[1]) => translate(lang, key),
        [lang]
    );

    const value: LanguageContextValue = {
        lang,
        setLang,
        t: tFn,
        dir: getDir(lang),
    };

    return (
        <LanguageContext.Provider value={value}>
            {children}
        </LanguageContext.Provider>
    );
}

// ─────────────────────────────────────────────────────────────────────────────
// Hook
// ─────────────────────────────────────────────────────────────────────────────
export function useLanguage(): LanguageContextValue {
    const ctx = useContext(LanguageContext);
    if (!ctx) throw new Error("useLanguage must be used inside <LanguageProvider>");
    return ctx;
}

// Re-export for convenience
export { LANGUAGES, translations };
