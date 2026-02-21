interface JsonLdProps {
    data: Record<string, unknown>;
}

export default function JsonLd({ data }: JsonLdProps) {
    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
        />
    );
}

export function OrganizationJsonLd() {
    return (
        <JsonLd
            data={{
                "@context": "https://schema.org",
                "@type": "Organization",
                name: "AntiGravity Medical",
                url: "https://antigravity.co",
                logo: "https://antigravity.co/logo.png",
                description:
                    "Premium medical tourism coordination between Phuket, Thailand and Turkey. JCI-accredited hospitals, 20-70% savings.",
                contactPoint: {
                    "@type": "ContactPoint",
                    telephone: "+66-XX-XXX-XXXX",
                    contactType: "customer service",
                    availableLanguage: ["English", "Russian", "Turkish", "Thai", "Arabic", "Chinese"],
                },
                sameAs: [
                    "https://www.instagram.com/antigravitymedical",
                    "https://www.facebook.com/antigravitymedical",
                ],
            }}
        />
    );
}

export function MedicalBusinessJsonLd() {
    return (
        <JsonLd
            data={{
                "@context": "https://schema.org",
                "@type": "MedicalBusiness",
                name: "AntiGravity Medical",
                url: "https://antigravity.co",
                description:
                    "Medical tourism coordination — rhinoplasty, hair transplant, dental, IVF and more between Phuket and Turkey.",
                medicalSpecialty: [
                    "PlasticSurgery",
                    "Dentistry",
                    "Dermatology",
                    "Ophthalmology",
                ],
                address: [
                    {
                        "@type": "PostalAddress",
                        addressLocality: "Phuket",
                        addressCountry: "TH",
                    },
                    {
                        "@type": "PostalAddress",
                        addressLocality: "Istanbul",
                        addressCountry: "TR",
                    },
                ],
                priceRange: "$$",
                isAcceptingNewPatients: true,
            }}
        />
    );
}

export function ArticleJsonLd({
    title,
    description,
    url,
    datePublished,
    author,
    image,
}: {
    title: string;
    description: string;
    url: string;
    datePublished: string;
    author: string;
    image?: string;
}) {
    return (
        <JsonLd
            data={{
                "@context": "https://schema.org",
                "@type": "Article",
                headline: title,
                description,
                url,
                datePublished,
                dateModified: datePublished,
                author: {
                    "@type": "Organization",
                    name: author,
                },
                publisher: {
                    "@type": "Organization",
                    name: "AntiGravity Medical",
                    logo: {
                        "@type": "ImageObject",
                        url: "https://antigravity.co/logo.png",
                    },
                },
                image: image || "https://antigravity.co/og-default.jpg",
                mainEntityOfPage: {
                    "@type": "WebPage",
                    "@id": url,
                },
            }}
        />
    );
}

export function BreadcrumbJsonLd({ items }: { items: { name: string; url: string }[] }) {
    return (
        <JsonLd
            data={{
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                itemListElement: items.map((item, i) => ({
                    "@type": "ListItem",
                    position: i + 1,
                    name: item.name,
                    item: item.url,
                })),
            }}
        />
    );
}
