"use client";

import { useState, useRef, useCallback, useEffect } from "react";
import Link from "next/link";
import Navbar from "../../../components/Navbar";
import { useLanguage } from "../../../lib/LanguageContext";
import {
    getVisualizationQuestions,
    startVisualization,
    checkVisualizationStatus,
    submitPostOpPhoto,
} from "../../../lib/api";
import type { VizQuestion } from "../../../lib/api";
import type { Language } from "../../../lib/i18n";

// ─── Procedure Categories ────────────────────────────────────────────────────
const PROCEDURES = [
    { id: "hair_transplant", icon: "💆", color: "from-sky-500 to-cyan-400" },
    { id: "rhinoplasty", icon: "👃", color: "from-rose-500 to-pink-400" },
    { id: "dental", icon: "🦷", color: "from-emerald-500 to-teal-400" },
    { id: "breast_augmentation", icon: "🩺", color: "from-purple-500 to-violet-400" },
    { id: "facelift", icon: "✨", color: "from-amber-500 to-orange-400" },
    { id: "liposuction", icon: "🏋️", color: "from-indigo-500 to-blue-400" },
    { id: "bbl", icon: "🍑", color: "from-pink-500 to-rose-400" },
    { id: "bichectomy", icon: "💎", color: "from-teal-500 to-cyan-400" },
] as const;

// ─── Question Language Helper ─────────────────────────────────────────────────
function getQuestionText(q: VizQuestion, lang: Language): string {
    const key = `question_${lang}` as keyof VizQuestion;
    return (q[key] as string) || q.question_en;
}

// ─── Image Resize Helper ─────────────────────────────────────────────────────
function resizeImage(file: File, maxSize: number): Promise<string> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement("canvas");
                let { width, height } = img;
                if (width > maxSize || height > maxSize) {
                    if (width > height) {
                        height = (height / width) * maxSize;
                        width = maxSize;
                    } else {
                        width = (width / height) * maxSize;
                        height = maxSize;
                    }
                }
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext("2d");
                if (!ctx) return reject(new Error("Canvas not supported"));
                ctx.drawImage(img, 0, 0, width, height);
                resolve(canvas.toDataURL("image/jpeg", 0.85));
            };
            img.onerror = reject;
            img.src = e.target?.result as string;
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// ─── Before/After Slider Component ───────────────────────────────────────────
function BeforeAfterSlider({ beforeSrc, afterSrc }: { beforeSrc: string; afterSrc: string }) {
    const [position, setPosition] = useState(50);
    const containerRef = useRef<HTMLDivElement>(null);
    const isDragging = useRef(false);

    const handleMove = useCallback((clientX: number) => {
        if (!containerRef.current || !isDragging.current) return;
        const rect = containerRef.current.getBoundingClientRect();
        const x = Math.max(0, Math.min(clientX - rect.left, rect.width));
        setPosition((x / rect.width) * 100);
    }, []);

    useEffect(() => {
        const onUp = () => { isDragging.current = false; };
        const onMove = (e: MouseEvent) => handleMove(e.clientX);
        const onTouchMove = (e: TouchEvent) => handleMove(e.touches[0].clientX);
        window.addEventListener("mouseup", onUp);
        window.addEventListener("mousemove", onMove);
        window.addEventListener("touchend", onUp);
        window.addEventListener("touchmove", onTouchMove);
        return () => {
            window.removeEventListener("mouseup", onUp);
            window.removeEventListener("mousemove", onMove);
            window.removeEventListener("touchend", onUp);
            window.removeEventListener("touchmove", onTouchMove);
        };
    }, [handleMove]);

    return (
        <div
            ref={containerRef}
            className="relative w-full aspect-square max-w-md mx-auto rounded-2xl overflow-hidden shadow-xl cursor-col-resize select-none"
            onMouseDown={() => { isDragging.current = true; }}
            onTouchStart={() => { isDragging.current = true; }}
        >
            {/* After image (full background) */}
            <img src={afterSrc} alt="After" className="absolute inset-0 w-full h-full object-cover" draggable={false} />
            {/* Before image (clipped) */}
            <div className="absolute inset-0 overflow-hidden" style={{ width: `${position}%` }}>
                <img src={beforeSrc} alt="Before" className="absolute inset-0 w-full h-full object-cover" style={{ minWidth: containerRef.current ? `${containerRef.current.offsetWidth}px` : "100%" }} draggable={false} />
            </div>
            {/* Slider line + handle */}
            <div className="absolute top-0 bottom-0 w-0.5 bg-white shadow-lg" style={{ left: `${position}%` }}>
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-white shadow-xl flex items-center justify-center">
                    <svg className="w-5 h-5 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l4-4 4 4M8 15l4 4 4-4" />
                    </svg>
                </div>
            </div>
            {/* Labels */}
            <div className="absolute top-3 left-3 bg-black/60 text-white text-xs font-bold px-2.5 py-1 rounded-full">BEFORE</div>
            <div className="absolute top-3 right-3 bg-cyan-600/80 text-white text-xs font-bold px-2.5 py-1 rounded-full">AFTER (AI)</div>
        </div>
    );
}

// ─── Main Wizard ──────────────────────────────────────────────────────────────
export default function VisualizePage() {
    const { t, lang } = useLanguage();

    // Wizard state
    const [step, setStep] = useState(1);
    const [selectedProcedure, setSelectedProcedure] = useState("");
    const [questions, setQuestions] = useState<VizQuestion[]>([]);
    const [answers, setAnswers] = useState<Record<string, string>>({});
    const [imageBase64, setImageBase64] = useState("");
    const [imagePreview, setImagePreview] = useState("");
    const [vizId, setVizId] = useState("");
    const [resultUrl, setResultUrl] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [postOpScore, setPostOpScore] = useState<number | null>(null);

    const fileInputRef = useRef<HTMLInputElement>(null);

    // Step 1 → 2: Select procedure → fetch questions
    const handleProcedureSelect = async (procId: string) => {
        setSelectedProcedure(procId);
        setError("");
        try {
            const data = await getVisualizationQuestions(procId);
            setQuestions(data.questions);
            setAnswers({});
            setStep(2);
        } catch (err) {
            setError(t("vizError"));
        }
    };

    // Step 2 → 3: Answer questions → photo upload
    const handleQuestionsSubmit = () => {
        setStep(3);
    };

    // Step 3: File upload + resize
    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;
        setError("");

        if (file.size > 10 * 1024 * 1024) {
            setError(t("vizFileTooLarge"));
            return;
        }
        if (!file.type.startsWith("image/")) {
            setError(t("vizInvalidFormat"));
            return;
        }

        try {
            const resized = await resizeImage(file, 1024);
            setImageBase64(resized);
            setImagePreview(resized);
        } catch {
            setError(t("vizError"));
        }
    };

    // Step 3 → 4: Submit → start visualization
    const handleStartVisualization = async () => {
        if (!imageBase64) return;
        setLoading(true);
        setError("");
        setStep(4);

        try {
            const resp = await startVisualization(imageBase64, selectedProcedure, answers);
            setVizId(resp.viz_id);

            // Start polling
            pollStatus(resp.viz_id);
        } catch (err: unknown) {
            const msg = err instanceof Error ? err.message : String(err);
            if (msg.includes("429")) {
                setError(t("vizDailyLimit"));
            } else {
                setError(t("vizError"));
            }
            setStep(3);
            setLoading(false);
        }
    };

    // Polling
    const pollStatus = async (id: string) => {
        let attempts = 0;
        const maxAttempts = 60; // 3 minutes max

        const poll = async () => {
            attempts++;
            try {
                const status = await checkVisualizationStatus(id);
                if (status.status === "succeeded" && status.output_image_url) {
                    setResultUrl(status.output_image_url);
                    setLoading(false);
                    setStep(5);
                } else if (status.status === "failed") {
                    setError(t("vizError"));
                    setLoading(false);
                    setStep(3);
                } else if (attempts < maxAttempts) {
                    setTimeout(poll, 3000);
                } else {
                    setError(t("vizTimeout"));
                    setLoading(false);
                    setStep(3);
                }
            } catch {
                if (attempts < maxAttempts) {
                    setTimeout(poll, 3000);
                } else {
                    setError(t("vizError"));
                    setLoading(false);
                    setStep(3);
                }
            }
        };

        setTimeout(poll, 3000);
    };

    // Step 6: Post-op upload
    const handlePostOpUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;
        try {
            const resized = await resizeImage(file, 1024);
            const resp = await submitPostOpPhoto(vizId, resized);
            setPostOpScore(resp.similarity_score);
        } catch {
            setError(t("vizError"));
        }
    };

    // Reset
    const handleReset = () => {
        setStep(1);
        setSelectedProcedure("");
        setQuestions([]);
        setAnswers({});
        setImageBase64("");
        setImagePreview("");
        setVizId("");
        setResultUrl("");
        setError("");
        setLoading(false);
        setPostOpScore(null);
    };

    return (
        <div className="min-h-screen bg-white text-slate-800" dir={lang === "ar" ? "rtl" : "ltr"}>
            <Navbar />

            {/* Hero */}
            <section className="relative bg-gradient-to-br from-slate-900 via-slate-800 to-sky-900 py-16 sm:py-20">
                <div className="pointer-events-none absolute inset-0">
                    <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-cyan-500/10 blur-3xl" />
                    <div className="absolute bottom-[-20%] right-[-5%] w-[40%] h-[50%] rounded-full bg-indigo-500/10 blur-3xl" />
                </div>
                <div className="container-main relative z-10 text-center">
                    <div className="inline-flex items-center gap-2 rounded-full border border-cyan-500/30 bg-cyan-500/10 px-4 py-1.5 mb-6">
                        <span className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse" />
                        <span className="text-xs font-bold text-cyan-300 tracking-widest uppercase">AI Powered</span>
                    </div>
                    <h1 className="font-display text-3xl sm:text-5xl font-bold text-white leading-tight mb-4">
                        {t("vizTitle")}
                    </h1>
                    <p className="text-slate-300 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
                        {t("vizSubtitle")}
                    </p>
                </div>
            </section>

            {/* Progress Steps */}
            <section className="bg-white border-b border-slate-100">
                <div className="container-main py-4">
                    <div className="flex items-center justify-center gap-2 sm:gap-4">
                        {[1, 2, 3, 4, 5].map((s) => (
                            <div key={s} className="flex items-center gap-2">
                                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all ${
                                    s === step
                                        ? "bg-cyan-600 text-white shadow-lg shadow-cyan-500/30"
                                        : s < step
                                            ? "bg-cyan-100 text-cyan-700"
                                            : "bg-slate-100 text-slate-400"
                                }`}>
                                    {s < step ? "✓" : s}
                                </div>
                                {s < 5 && <div className={`hidden sm:block w-8 h-0.5 ${s < step ? "bg-cyan-300" : "bg-slate-200"}`} />}
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Error Display */}
            {error && (
                <div className="container-main mt-6">
                    <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center">
                        <p className="text-sm text-red-700 font-medium">{error}</p>
                        {error === t("vizDailyLimit") && (
                            <p className="text-xs text-red-500 mt-1">{t("vizDailyLimitSub")}</p>
                        )}
                    </div>
                </div>
            )}

            {/* Wizard Content */}
            <section className="section-padding">
                <div className="container-main max-w-3xl mx-auto">

                    {/* ── STEP 1: Procedure Selection ────────────────────── */}
                    {step === 1 && (
                        <div className="animate-fade-up">
                            <h2 className="text-xl font-bold text-slate-800 text-center mb-2">{t("vizStep1Title")}</h2>
                            <p className="text-sm text-slate-500 text-center mb-8">{t("vizStep1Sub")}</p>
                            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                                {PROCEDURES.map((proc) => (
                                    <button
                                        key={proc.id}
                                        onClick={() => handleProcedureSelect(proc.id)}
                                        className="group rounded-2xl border border-slate-200 bg-white p-5 text-center shadow-sm hover:shadow-lg hover:border-cyan-300 transition-all duration-300 hover:-translate-y-1"
                                    >
                                        <div className={`w-12 h-12 mx-auto rounded-xl bg-gradient-to-br ${proc.color} flex items-center justify-center shadow-lg mb-3`}>
                                            <span className="text-2xl">{proc.icon}</span>
                                        </div>
                                        <span className="text-xs font-bold text-slate-700">
                                            {t(`vizProc_${proc.id}` as Parameters<typeof t>[0])}
                                        </span>
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* ── STEP 2: AI Questions ──────────────────────────── */}
                    {step === 2 && (
                        <div className="animate-fade-up">
                            <h2 className="text-xl font-bold text-slate-800 text-center mb-2">{t("vizStep2Title")}</h2>
                            <p className="text-sm text-slate-500 text-center mb-8">{t("vizStep2Sub")}</p>
                            <div className="space-y-5">
                                {questions.map((q) => (
                                    <div key={q.id} className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
                                        <label className="block text-sm font-semibold text-slate-700 mb-3">
                                            {getQuestionText(q, lang)}
                                        </label>
                                        <div className="flex flex-wrap gap-2">
                                            {q.options.split(",").map((opt) => (
                                                <button
                                                    key={opt}
                                                    onClick={() => setAnswers((prev) => ({ ...prev, [q.id]: opt.trim() }))}
                                                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                                                        answers[q.id] === opt.trim()
                                                            ? "bg-cyan-600 text-white shadow-md"
                                                            : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                                                    }`}
                                                >
                                                    {opt.trim()}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <div className="flex justify-between mt-8">
                                <button
                                    onClick={() => setStep(1)}
                                    className="px-5 py-2.5 rounded-xl border border-slate-200 text-slate-600 text-sm font-semibold hover:bg-slate-50 transition-colors"
                                >
                                    {t("btnBack")}
                                </button>
                                <button
                                    onClick={handleQuestionsSubmit}
                                    disabled={Object.keys(answers).length === 0}
                                    className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-cyan-400 text-white text-sm font-bold shadow-md hover:scale-105 transition-all disabled:opacity-50 disabled:hover:scale-100"
                                >
                                    {t("vizNext")}
                                </button>
                            </div>
                        </div>
                    )}

                    {/* ── STEP 3: Photo Upload ────────────────────────────── */}
                    {step === 3 && (
                        <div className="animate-fade-up">
                            <h2 className="text-xl font-bold text-slate-800 text-center mb-2">{t("vizStep3Title")}</h2>
                            <p className="text-sm text-slate-500 text-center mb-8">{t("vizStep3Sub")}</p>

                            {!imagePreview ? (
                                <div
                                    onClick={() => fileInputRef.current?.click()}
                                    className="border-2 border-dashed border-slate-300 rounded-2xl p-12 text-center cursor-pointer hover:border-cyan-400 hover:bg-cyan-50/30 transition-all"
                                >
                                    <div className="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-sky-500 to-cyan-400 flex items-center justify-center shadow-lg mb-4">
                                        <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                        </svg>
                                    </div>
                                    <p className="text-sm font-semibold text-slate-700 mb-1">{t("vizUploadTitle")}</p>
                                    <p className="text-xs text-slate-400">{t("vizUploadSub")}</p>
                                </div>
                            ) : (
                                <div className="text-center">
                                    <div className="relative inline-block">
                                        <img
                                            src={imagePreview}
                                            alt="Preview"
                                            className="max-w-xs rounded-2xl shadow-xl border-4 border-white"
                                        />
                                        <button
                                            onClick={() => { setImageBase64(""); setImagePreview(""); }}
                                            className="absolute -top-2 -right-2 w-7 h-7 rounded-full bg-red-500 text-white text-sm flex items-center justify-center shadow-lg hover:bg-red-600"
                                        >
                                            x
                                        </button>
                                    </div>
                                </div>
                            )}

                            <input
                                ref={fileInputRef}
                                type="file"
                                accept="image/*"
                                onChange={handleFileChange}
                                className="hidden"
                            />

                            <div className="flex justify-between mt-8">
                                <button
                                    onClick={() => setStep(2)}
                                    className="px-5 py-2.5 rounded-xl border border-slate-200 text-slate-600 text-sm font-semibold hover:bg-slate-50 transition-colors"
                                >
                                    {t("btnBack")}
                                </button>
                                <button
                                    onClick={handleStartVisualization}
                                    disabled={!imageBase64}
                                    className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-cyan-400 text-white text-sm font-bold shadow-md hover:scale-105 transition-all disabled:opacity-50 disabled:hover:scale-100"
                                >
                                    {t("vizGenerate")}
                                </button>
                            </div>
                        </div>
                    )}

                    {/* ── STEP 4: Processing ──────────────────────────────── */}
                    {step === 4 && (
                        <div className="animate-fade-up text-center py-12">
                            <div className="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-sky-500 to-cyan-400 flex items-center justify-center shadow-2xl shadow-cyan-500/30 mb-6 animate-pulse">
                                <svg className="w-10 h-10 text-white animate-spin" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                </svg>
                            </div>
                            <h2 className="text-xl font-bold text-slate-800 mb-2">{t("vizProcessing")}</h2>
                            <p className="text-sm text-slate-500 mb-6">{t("vizProcessingSub")}</p>

                            {/* Animated progress bar */}
                            <div className="w-64 mx-auto h-2 bg-slate-100 rounded-full overflow-hidden">
                                <div className="h-full bg-gradient-to-r from-sky-500 to-cyan-400 rounded-full animate-[progress_3s_ease-in-out_infinite]"
                                    style={{ width: "70%", animation: "progress 3s ease-in-out infinite" }}
                                />
                            </div>
                            <style>{`
                                @keyframes progress {
                                    0% { width: 10%; }
                                    50% { width: 80%; }
                                    100% { width: 10%; }
                                }
                            `}</style>
                        </div>
                    )}

                    {/* ── STEP 5: Result ──────────────────────────────────── */}
                    {step === 5 && (
                        <div className="animate-fade-up">
                            <h2 className="text-xl font-bold text-slate-800 text-center mb-2">{t("vizResultTitle")}</h2>
                            <p className="text-sm text-slate-500 text-center mb-8">{t("vizResultSub")}</p>

                            {/* Before/After Slider */}
                            <BeforeAfterSlider
                                beforeSrc={imagePreview}
                                afterSrc={resultUrl}
                            />

                            {/* Disclaimer */}
                            <div className="mt-6 bg-amber-50 border border-amber-200 rounded-xl p-4">
                                <p className="text-xs text-amber-700 text-center leading-relaxed">
                                    {t("vizDisclaimer")}
                                </p>
                            </div>

                            {/* Post-op upload section */}
                            <div className="mt-8 rounded-2xl border border-slate-200 bg-slate-50 p-6 text-center">
                                <h3 className="text-sm font-bold text-slate-700 mb-2">{t("vizPostOpTitle")}</h3>
                                <p className="text-xs text-slate-500 mb-4">{t("vizPostOpSub")}</p>

                                {postOpScore !== null ? (
                                    <div className="inline-flex items-center gap-3 bg-white rounded-xl border border-cyan-200 px-6 py-3">
                                        <span className="text-2xl font-bold text-cyan-600">{postOpScore}%</span>
                                        <span className="text-xs text-slate-500">{t("vizSimilarity")}</span>
                                    </div>
                                ) : (
                                    <label className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl border border-slate-300 text-slate-600 text-sm font-semibold cursor-pointer hover:bg-white transition-colors">
                                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                                        </svg>
                                        {t("vizUploadPostOp")}
                                        <input type="file" accept="image/*" onChange={handlePostOpUpload} className="hidden" />
                                    </label>
                                )}
                            </div>

                            {/* Actions */}
                            <div className="flex flex-wrap justify-center gap-3 mt-8">
                                <button
                                    onClick={handleReset}
                                    className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-cyan-400 text-white text-sm font-bold shadow-md hover:scale-105 transition-all"
                                >
                                    {t("vizNewVisualization")}
                                </button>
                                <Link
                                    href="/medical"
                                    className="px-6 py-2.5 rounded-xl border border-slate-200 text-slate-600 text-sm font-semibold hover:bg-slate-50 transition-colors"
                                >
                                    {t("vizBookProcedure")}
                                </Link>
                            </div>
                        </div>
                    )}
                </div>
            </section>

            {/* CTA Section */}
            <section className="section-padding bg-gradient-to-br from-slate-900 via-slate-800 to-sky-900">
                <div className="container-main text-center">
                    <h2 className="text-2xl font-display font-bold text-white mb-4">{t("vizCtaTitle")}</h2>
                    <p className="text-slate-300 text-sm mb-6 max-w-lg mx-auto">{t("vizCtaSub")}</p>
                    <Link
                        href="/medical"
                        className="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl bg-sky-500 text-white font-bold hover:bg-sky-400 transition-all shadow-lg shadow-sky-500/30 hover:scale-105"
                    >
                        {t("btnConsultation")}
                    </Link>
                </div>
            </section>
        </div>
    );
}
