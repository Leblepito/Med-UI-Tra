import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "Factory & B2B — Turkey & Thailand Sourcing",
    description:
        "B2B manufacturing and sourcing from Turkey and Thailand. Textile, apparel, custom manufacturing, and bulk export services.",
    openGraph: {
        title: "Factory & B2B — AntiGravity",
        description: "B2B manufacturing and sourcing from Turkey and Thailand.",
        type: "website",
    },
};

export default function FactoryLayout({ children }: { children: React.ReactNode }) {
    return children;
}
