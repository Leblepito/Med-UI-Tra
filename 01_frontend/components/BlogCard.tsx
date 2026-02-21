import Link from "next/link";

const CATEGORY_COLORS: Record<string, string> = {
    hair_transplant: "bg-purple-100 text-purple-700",
    rhinoplasty: "bg-pink-100 text-pink-700",
    dental: "bg-blue-100 text-blue-700",
    ivf: "bg-rose-100 text-rose-700",
    eye_surgery: "bg-indigo-100 text-indigo-700",
    bbl: "bg-orange-100 text-orange-700",
    breast: "bg-fuchsia-100 text-fuchsia-700",
    bariatric: "bg-teal-100 text-teal-700",
    facelift: "bg-amber-100 text-amber-700",
    medical_tourism_guide: "bg-cyan-100 text-cyan-700",
};

const CATEGORY_ICONS: Record<string, string> = {
    hair_transplant: "💆",
    rhinoplasty: "👃",
    dental: "🦷",
    ivf: "🍼",
    eye_surgery: "👁️",
    bbl: "🍑",
    breast: "🎀",
    bariatric: "⚖️",
    facelift: "✨",
    medical_tourism_guide: "🌍",
};

interface BlogCardProps {
    title: string;
    slug: string;
    excerpt: string;
    category: string;
    categoryLabel: string;
    date: string;
    readTime: number;
    readTimeLabel: string;
    image?: string;
}

export default function BlogCard({
    title,
    slug,
    excerpt,
    category,
    categoryLabel,
    date,
    readTime,
    readTimeLabel,
    image,
}: BlogCardProps) {
    const colorCls = CATEGORY_COLORS[category] || "bg-slate-100 text-slate-700";
    const icon = CATEGORY_ICONS[category] || "📝";

    return (
        <Link
            href={`/blog/${slug}`}
            aria-label={`Read article: ${title}`}
            className="group flex flex-col rounded-2xl border border-slate-200 bg-white shadow-sm hover:shadow-xl hover:border-cyan-200 transition-all duration-300 hover:-translate-y-1 overflow-hidden"
        >
            {/* Image placeholder */}
            <div className="relative h-48 bg-gradient-to-br from-slate-100 to-slate-50 flex items-center justify-center overflow-hidden">
                <span className="text-5xl opacity-60 group-hover:scale-110 transition-transform duration-300">
                    {icon}
                </span>
                <div className="absolute top-3 left-3">
                    <span className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full ${colorCls}`}>
                        {categoryLabel}
                    </span>
                </div>
            </div>

            {/* Content */}
            <div className="flex flex-col flex-1 p-5">
                <h3 className="text-base font-bold text-slate-800 mb-2 line-clamp-2 group-hover:text-cyan-700 transition-colors">
                    {title}
                </h3>
                <p className="text-sm text-slate-500 leading-relaxed mb-4 line-clamp-3 flex-1">
                    {excerpt}
                </p>
                <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>{new Date(date).toLocaleDateString()}</span>
                    <span>{readTime} {readTimeLabel}</span>
                </div>
            </div>
        </Link>
    );
}
