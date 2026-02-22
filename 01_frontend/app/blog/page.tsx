"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Navbar from "../../components/Navbar";
import BlogCard from "../../components/BlogCard";
import { useLanguage } from "../../lib/LanguageContext";
import { getBlogPosts, getBlogCategories, type BlogPostItem } from "../../lib/api";

const CATEGORY_LABELS: Record<string, Record<string, string>> = {
    hair_transplant: { en: "Hair Transplant", ru: "Пересадка волос", tr: "Sac Ekimi", th: "ปลูกผม", ar: "زراعة الشعر", zh: "植发" },
    rhinoplasty: { en: "Rhinoplasty", ru: "Ринопластика", tr: "Rinoplasti", th: "เสริมจมูก", ar: "تجميل الأنف", zh: "鼻整形" },
    dental: { en: "Dental", ru: "Стоматология", tr: "Dis", th: "ทันตกรรม", ar: "طب الأسنان", zh: "牙科" },
    ivf: { en: "IVF", ru: "ЭКО", tr: "Tup Bebek", th: "IVF", ar: "أطفال الأنابيب", zh: "试管婴儿" },
    eye_surgery: { en: "Eye Surgery", ru: "Офтальмология", tr: "Goz Ameliyati", th: "ผ่าตัดตา", ar: "جراحة العيون", zh: "眼科手术" },
    bbl: { en: "BBL", ru: "BBL", tr: "BBL", th: "BBL", ar: "BBL", zh: "BBL" },
    breast: { en: "Breast", ru: "Маммопластика", tr: "Gogus", th: "เต้านม", ar: "الثدي", zh: "胸部" },
    bariatric: { en: "Bariatric", ru: "Бариатрия", tr: "Obezite", th: "ลดน้ำหนัก", ar: "السمنة", zh: "减重" },
    facelift: { en: "Facelift", ru: "Подтяжка лица", tr: "Yuz Germe", th: "ดึงหน้า", ar: "شد الوجه", zh: "面部提升" },
    medical_tourism_guide: { en: "Guide", ru: "Руководство", tr: "Rehber", th: "คู่มือ", ar: "دليل", zh: "指南" },
};

export default function BlogPage() {
    const { t, lang } = useLanguage();
    const [posts, setPosts] = useState<BlogPostItem[]>([]);
    const [categories, setCategories] = useState<{ id: string; icon: string }[]>([]);
    const [activeCategory, setActiveCategory] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        let cancelled = false;
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setLoading(true);
        Promise.all([
            getBlogPosts(lang, activeCategory ?? undefined),
            getBlogCategories(),
        ]).then(([postsData, catsData]) => {
            if (cancelled) return;
            setPosts(postsData.posts);
            setCategories(catsData.categories);
            setError(false);
            setLoading(false);
        }).catch(() => {
            if (cancelled) return;
            setError(true);
            setLoading(false);
        });
        return () => { cancelled = true; };
    }, [lang, activeCategory]);

    const getCategoryLabel = (catId: string) => {
        return CATEGORY_LABELS[catId]?.[lang] || CATEGORY_LABELS[catId]?.en || catId;
    };

    return (
        <div className="min-h-screen bg-white text-slate-800" dir={lang === "ar" ? "rtl" : "ltr"}>
            <Navbar />

            {/* Hero */}
            <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-sky-900 py-16 sm:py-20">
                <div className="pointer-events-none absolute inset-0">
                    <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-sky-500/10 blur-3xl" />
                    <div className="absolute bottom-[-20%] right-[-5%] w-[45%] h-[55%] rounded-full bg-indigo-500/10 blur-3xl" />
                </div>
                <div className="container-main relative z-10 text-center">
                    <div className="inline-flex items-center gap-2 rounded-full border border-sky-500/30 bg-sky-500/10 px-4 py-1.5 mb-6">
                        <span className="text-xs font-bold text-sky-300 tracking-widest uppercase">
                            {t("blogNavLabel")}
                        </span>
                    </div>
                    <h1 className="font-display text-3xl sm:text-5xl font-bold text-white leading-tight mb-4">
                        {t("blogTitle")}
                    </h1>
                    <p className="text-slate-300 text-lg max-w-2xl mx-auto leading-relaxed">
                        {t("blogSubtitle")}
                    </p>
                </div>
            </section>

            {/* Category Filter */}
            <section className="bg-white border-b border-slate-100 sticky top-16 z-40">
                <div className="container-main py-4">
                    <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-hide">
                        <button
                            onClick={() => setActiveCategory(null)}
                            className={`shrink-0 px-4 py-2 rounded-full text-sm font-semibold transition-all duration-200 ${
                                !activeCategory
                                    ? "bg-cyan-600 text-white shadow-md"
                                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                            }`}
                        >
                            {t("blogAllCategories")}
                        </button>
                        {categories.map((cat) => (
                            <button
                                key={cat.id}
                                onClick={() => setActiveCategory(cat.id)}
                                className={`shrink-0 px-4 py-2 rounded-full text-sm font-semibold transition-all duration-200 ${
                                    activeCategory === cat.id
                                        ? "bg-cyan-600 text-white shadow-md"
                                        : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                                }`}
                            >
                                {cat.icon} {getCategoryLabel(cat.id)}
                            </button>
                        ))}
                    </div>
                </div>
            </section>

            {/* Blog Grid */}
            <section className="section-padding bg-slate-50">
                <div className="container-main">
                    {error ? (
                        <div className="text-center py-16">
                            <p className="text-slate-800 text-lg font-semibold mb-2">Something went wrong</p>
                            <p className="text-slate-400 mb-4">Could not load blog posts. Please try again later.</p>
                            <button
                                onClick={() => { setLoading(true); setError(false); }}
                                className="px-5 py-2 rounded-xl bg-cyan-600 text-white font-semibold hover:bg-cyan-500 transition-colors"
                            >
                                Try Again
                            </button>
                        </div>
                    ) : loading ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                            {[1, 2, 3, 4, 5, 6].map((i) => (
                                <div key={i} className="rounded-2xl bg-white border border-slate-200 overflow-hidden animate-pulse">
                                    <div className="h-48 bg-slate-100" />
                                    <div className="p-5 space-y-3">
                                        <div className="h-4 bg-slate-100 rounded w-3/4" />
                                        <div className="h-3 bg-slate-100 rounded w-full" />
                                        <div className="h-3 bg-slate-100 rounded w-2/3" />
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : posts.length === 0 ? (
                        <div className="text-center py-16">
                            <p className="text-slate-400 text-lg">No posts found</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                            {posts.map((post) => (
                                <BlogCard
                                    key={post.id}
                                    title={post.title}
                                    slug={post.slug}
                                    excerpt={post.excerpt}
                                    category={post.category}
                                    categoryLabel={getCategoryLabel(post.category)}
                                    date={post.date}
                                    readTime={post.read_time}
                                    readTimeLabel={t("blogReadTime")}
                                    image={post.image}
                                />
                            ))}
                        </div>
                    )}
                </div>
            </section>

            {/* Footer CTA */}
            <section className="section-padding bg-white">
                <div className="container-main text-center">
                    <h2 className="text-2xl font-display font-bold text-slate-800 mb-4">
                        {t("blogCta")}
                    </h2>
                    <Link
                        href="/medical"
                        className="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl bg-sky-500 text-white font-bold hover:bg-sky-400 transition-all duration-200 shadow-lg shadow-sky-500/30 hover:scale-105"
                    >
                        {t("btnConsultation")}
                    </Link>
                </div>
            </section>
        </div>
    );
}
