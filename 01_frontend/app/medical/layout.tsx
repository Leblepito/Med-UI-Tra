import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "Medical Tourism — Rhinoplasty, Hair Transplant, Dental & More",
    description:
        "Premium medical tourism in Turkey & Thailand. JCI-accredited hospitals, 20-70% savings on rhinoplasty, hair transplant, dental veneers, LASIK, IVF. Free consultation in 6 languages.",
    openGraph: {
        title: "Medical Tourism — AntiGravity Medical",
        description:
            "Premium medical procedures in JCI-accredited hospitals. Turkey & Thailand health corridor with 20-70% savings.",
        type: "website",
    },
};

export default function MedicalLayout({ children }: { children: React.ReactNode }) {
    return children;
}
