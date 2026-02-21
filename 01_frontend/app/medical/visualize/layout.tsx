import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "AI Visualization — Before & After | AntiGravity Medical",
    description:
        "Upload your photo and see a realistic AI-powered preview of your medical procedure results. Hair transplant, rhinoplasty, dental, and more.",
    openGraph: {
        title: "AI Before & After Visualization | AntiGravity Medical",
        description:
            "See how you could look after your procedure with AI-powered visualization. Upload your photo for a personalized preview.",
    },
};

export default function VisualizeLayout({ children }: { children: React.ReactNode }) {
    return <>{children}</>;
}
