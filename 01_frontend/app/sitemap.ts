import type { MetadataRoute } from "next";

const baseUrl = "https://leblepito.com";

const BLOG_SLUGS = [
    "hair-transplant-turkey-guide",
    "rhinoplasty-istanbul-antalya",
    "dental-veneers-turkey",
    "ivf-turkey-success-rates",
    "lasik-eye-surgery-turkey",
    "bbl-turkey-safety",
    "breast-augmentation-turkey",
    "bariatric-surgery-turkey",
    "facelift-turkey-rejuvenation",
    "medical-tourism-guide-phuket-turkey",
];

export default function sitemap(): MetadataRoute.Sitemap {
    const now = new Date();

    const staticPages: MetadataRoute.Sitemap = [
        {
            url: baseUrl,
            lastModified: now,
            changeFrequency: "weekly",
            priority: 1,
        },
        {
            url: `${baseUrl}/medical`,
            lastModified: now,
            changeFrequency: "weekly",
            priority: 0.9,
        },
        {
            url: `${baseUrl}/travel`,
            lastModified: now,
            changeFrequency: "weekly",
            priority: 0.8,
        },
        {
            url: `${baseUrl}/blog`,
            lastModified: now,
            changeFrequency: "weekly",
            priority: 0.8,
        },
        {
            url: `${baseUrl}/factory`,
            lastModified: now,
            changeFrequency: "monthly",
            priority: 0.5,
        },
    ];

    const blogPages: MetadataRoute.Sitemap = BLOG_SLUGS.map((slug) => ({
        url: `${baseUrl}/blog/${slug}`,
        lastModified: now,
        changeFrequency: "monthly" as const,
        priority: 0.7,
    }));

    return [...staticPages, ...blogPages];
}
