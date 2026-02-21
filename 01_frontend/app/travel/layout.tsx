import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "Travel & Accommodation — Phuket Recovery Coordination",
    description:
        "Post-treatment recovery coordination in Phuket, Thailand. Hotel bookings, airport transfers, and local guides for medical tourists. Patong, Kamala, Kata and more.",
    openGraph: {
        title: "Travel & Accommodation — AntiGravity Medical",
        description:
            "Recovery-focused travel coordination in Phuket, Thailand. Hotel bookings, transfers, and concierge services.",
        type: "website",
    },
};

export default function TravelLayout({ children }: { children: React.ReactNode }) {
    return children;
}
