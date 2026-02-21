import type { Metadata, Viewport } from "next";
import { Lora, Manrope, Noto_Sans_Thai, Noto_Kufi_Arabic, Noto_Sans_SC } from "next/font/google";
import "./globals.css";
import { LanguageProvider } from "../lib/LanguageContext";
import ChatWidget from "../components/ChatWidget";

const lora = Lora({
    subsets: ["latin", "cyrillic", "latin-ext"],
    variable: "--font-lora",
    display: "swap",
});

const manrope = Manrope({
    subsets: ["latin", "cyrillic", "latin-ext"],
    variable: "--font-manrope",
    display: "swap",
});

const notoThai = Noto_Sans_Thai({
    subsets: ["thai"],
    variable: "--font-thai",
    display: "swap",
    weight: ["400", "600", "700"],
});

const notoArabic = Noto_Kufi_Arabic({
    subsets: ["arabic"],
    variable: "--font-arabic",
    display: "swap",
    weight: ["400", "600", "700"],
});

const notoChinese = Noto_Sans_SC({
    subsets: ["latin"],
    variable: "--font-chinese",
    display: "swap",
    weight: ["400", "700"],
});

export const metadata: Metadata = {
    title: {
        default: "AntiGravity Medical — Phuket & Turkey Health Corridor",
        template: "%s | AntiGravity Medical",
    },
    description:
        "Premium medical tourism coordination between Phuket, Thailand and Turkey. JCI-accredited hospitals, 20-70% savings. Aesthetic surgery, hair transplant, dental, IVF and more.",
};

export const viewport: Viewport = {
    width: "device-width",
    initialScale: 1,
    themeColor: "#0891B2",
    colorScheme: "light",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body
                className={`${lora.variable} ${manrope.variable} ${notoThai.variable} ${notoArabic.variable} ${notoChinese.variable} font-body bg-white text-slate-800 antialiased`}
            >
                <LanguageProvider>
                    {children}
                    <ChatWidget />
                </LanguageProvider>
            </body>
        </html>
    );
}
