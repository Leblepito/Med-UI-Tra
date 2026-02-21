"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Navbar from "../../../components/Navbar";
import ShareButtons from "../../../components/ShareButtons";
import { useLanguage } from "../../../lib/LanguageContext";
import { getBlogPost, getBlogFeatured, type BlogPostItem } from "../../../lib/api";
import { useParams } from "next/navigation";

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

function renderMarkdown(md: string): string {
    let html = md;
    // H2
    html = html.replace(/^## (.+)$/gm, '<h2 class="text-xl font-bold text-slate-800 mt-8 mb-4">$1</h2>');
    // H3
    html = html.replace(/^### (.+)$/gm, '<h3 class="text-lg font-bold text-slate-800 mt-6 mb-3">$1</h3>');
    // Bold
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold text-slate-800">$1</strong>');
    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-cyan-600 hover:text-cyan-700 underline underline-offset-2">$1</a>');
    // Unordered list
    html = html.replace(/^- (.+)$/gm, '<li class="ml-4 text-slate-600 leading-relaxed">$1</li>');
    html = html.replace(/(<li[^>]*>.*<\/li>\n?)+/g, '<ul class="list-disc pl-4 mb-4 space-y-1">$&</ul>');
    // Ordered list
    html = html.replace(/^\d+\. (.+)$/gm, '<li class="ml-4 text-slate-600 leading-relaxed">$1</li>');
    // Tables
    html = html.replace(/\|(.+)\|\n\|[-| ]+\|\n((?:\|.+\|\n?)*)/g, (_match, header: string, body: string) => {
        const headers = header.split('|').map((h: string) => h.trim()).filter(Boolean);
        const rows = body.trim().split('\n').map((row: string) =>
            row.split('|').map((c: string) => c.trim()).filter(Boolean)
        );
        return `<div class="overflow-x-auto mb-6"><table class="w-full text-sm border-collapse"><thead><tr>${headers.map((h: string) => `<th class="text-left p-3 bg-slate-50 border-b border-slate-200 font-semibold text-slate-700">${h}</th>`).join('')}</tr></thead><tbody>${rows.map((row: string[]) => `<tr>${row.map((c: string) => `<td class="p-3 border-b border-slate-100 text-slate-600">${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    });
    // Paragraphs (lines not yet wrapped)
    html = html.replace(/^(?!<[huldtoa])(.+)$/gm, '<p class="text-slate-600 leading-relaxed mb-4">$1</p>');
    // Clean up empty paragraphs
    html = html.replace(/<p[^>]*>\s*<\/p>/g, '');
    return html;
}

export default function BlogDetailPage() {
    const { t, lang } = useLanguage();
    const params = useParams();
    const slug = params?.slug as string;
    const [post, setPost] = useState<BlogPostItem | null>(null);
    const [related, setRelated] = useState<BlogPostItem[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!slug) return;
        Promise.all([
            getBlogPost(slug, lang),
            getBlogFeatured(lang, 3),
        ]).then(([postData, featuredData]) => {
            setPost(postData.post);
            setRelated(featuredData.posts.filter((p) => p.slug !== slug).slice(0, 2));
            setLoading(false);
        }).catch(() => setLoading(false));
    }, [slug, lang]);

    const getCategoryLabel = (catId: string) => {
        return CATEGORY_LABELS[catId]?.[lang] || CATEGORY_LABELS[catId]?.en || catId;
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-white">
                <Navbar />
                <div className="container-main py-16">
                    <div className="max-w-3xl mx-auto animate-pulse space-y-4">
                        <div className="h-6 bg-slate-100 rounded w-1/3" />
                        <div className="h-10 bg-slate-100 rounded w-3/4" />
                        <div className="h-4 bg-slate-100 rounded w-1/2" />
                        <div className="h-64 bg-slate-100 rounded mt-8" />
                    </div>
                </div>
            </div>
        );
    }

    if (!post) {
        return (
            <div className="min-h-screen bg-white">
                <Navbar />
                <div className="container-main py-16 text-center">
                    <h1 className="text-2xl font-bold text-slate-800 mb-4">Post not found</h1>
                    <Link href="/blog" className="text-cyan-600 hover:text-cyan-700 font-semibold">
                        {t("blogBack")}
                    </Link>
                </div>
            </div>
        );
    }

    const currentUrl = typeof window !== "undefined" ? window.location.href : "";

    return (
        <div className="min-h-screen bg-white text-slate-800" dir={lang === "ar" ? "rtl" : "ltr"}>
            <Navbar />

            {/* Breadcrumb */}
            <div className="bg-slate-50 border-b border-slate-100">
                <div className="container-main py-3">
                    <nav className="flex items-center gap-2 text-sm text-slate-400">
                        <Link href="/" className="hover:text-slate-600 transition-colors">Home</Link>
                        <span>/</span>
                        <Link href="/blog" className="hover:text-slate-600 transition-colors">{t("blogNavLabel")}</Link>
                        <span>/</span>
                        <span className="text-slate-600 truncate max-w-xs">{post.title}</span>
                    </nav>
                </div>
            </div>

            {/* Article */}
            <div className="container-main py-10">
                <div className="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-10">
                    {/* Main content */}
                    <article className="max-w-none">
                        {/* Meta */}
                        <div className="mb-6">
                            <span className="inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-cyan-100 text-cyan-700 mb-4">
                                {getCategoryLabel(post.category)}
                            </span>
                            <h1 className="font-display text-3xl sm:text-4xl font-bold text-slate-900 leading-tight mb-4">
                                {post.title}
                            </h1>
                            <div className="flex flex-wrap items-center gap-4 text-sm text-slate-400 mb-6">
                                <span>{post.author}</span>
                                <span>|</span>
                                <span>{new Date(post.date).toLocaleDateString()}</span>
                                <span>|</span>
                                <span>{post.read_time} {t("blogReadTime")}</span>
                            </div>
                            <ShareButtons url={currentUrl} title={post.title} />
                        </div>

                        {/* Body */}
                        <div
                            className="prose-custom"
                            dangerouslySetInnerHTML={{ __html: renderMarkdown(post.body || "") }}
                        />

                        {/* Tags */}
                        <div className="mt-10 pt-6 border-t border-slate-100">
                            <div className="flex flex-wrap gap-2">
                                {post.tags.map((tag) => (
                                    <span key={tag} className="px-3 py-1 rounded-full bg-slate-100 text-slate-500 text-xs font-medium">
                                        #{tag}
                                    </span>
                                ))}
                            </div>
                        </div>

                        {/* Bottom share */}
                        <div className="mt-6 flex items-center gap-3">
                            <span className="text-sm font-semibold text-slate-500">{t("blogShareTitle")}:</span>
                            <ShareButtons url={currentUrl} title={post.title} />
                        </div>
                    </article>

                    {/* Sidebar */}
                    <aside className="space-y-6">
                        {/* CTA */}
                        <div className="rounded-2xl bg-gradient-to-br from-cyan-500 to-sky-600 p-6 text-white shadow-lg">
                            <h3 className="font-bold text-lg mb-2">{t("blogCta")}</h3>
                            <p className="text-cyan-100 text-sm mb-4 leading-relaxed">
                                {t("medFormSub")}
                            </p>
                            <Link
                                href="/medical"
                                className="inline-block w-full text-center px-4 py-2.5 rounded-xl bg-white text-cyan-700 font-bold text-sm hover:bg-cyan-50 transition-colors"
                            >
                                {t("btnConsultation")}
                            </Link>
                        </div>

                        {/* Related */}
                        {related.length > 0 && (
                            <div className="rounded-2xl border border-slate-200 p-5">
                                <h3 className="font-bold text-slate-800 mb-4">{t("blogRelated")}</h3>
                                <div className="space-y-4">
                                    {related.map((r) => (
                                        <Link
                                            key={r.id}
                                            href={`/blog/${r.slug}`}
                                            className="block group"
                                        >
                                            <h4 className="text-sm font-semibold text-slate-700 group-hover:text-cyan-600 transition-colors line-clamp-2">
                                                {r.title}
                                            </h4>
                                            <p className="text-xs text-slate-400 mt-1">
                                                {r.read_time} {t("blogReadTime")}
                                            </p>
                                        </Link>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Back */}
                        <Link
                            href="/blog"
                            className="block text-center px-4 py-2.5 rounded-xl border border-slate-200 text-slate-600 font-semibold text-sm hover:bg-slate-50 transition-colors"
                        >
                            {t("blogBack")}
                        </Link>
                    </aside>
                </div>
            </div>
        </div>
    );
}
