"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useLanguage } from "../../lib/LanguageContext";
import { getHospitals, type ApiHospital } from "../../lib/api";
import LanguagePicker from "../../components/LanguagePicker";

// ─────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────
type Urgency = "routine" | "soon" | "urgent";


interface IntakeResult {
    patient_id: string;
    procedure_category: string;
    matched_hospital?: {
        hospital_id?: string;
        name: string;
        city: string;
        country: string;
        rating: number;
        commission_rate: number;
        contact_whatsapp?: string | null;
        specialties?: string[];
        languages?: string[];
        jci_accredited?: boolean;
    } | null;
    estimated_procedure_cost_usd: number;
    commission_rate_pct?: string;
    commission_usd: number;
    coordinator_message: string;
    next_steps: string[];
}

// ─────────────────────────────────────────────────────────────
// Hospital Data — Turkey Partners
// ─────────────────────────────────────────────────────────────
interface Hospital {
    id: string;
    name: string;
    city: string;
    country: string;
    specialties: string[];
    rating: number;
    commission_rate: number;
    languages: string[];
    jci: boolean;
    beds?: number;
}

const TURKEY_HOSPITALS: Hospital[] = [
    { id: "MEM-IST-001", name: "Memorial Şişli", city: "Istanbul", country: "Turkey", specialties: ["aesthetic", "bariatric", "oncology", "checkup"], rating: 4.8, commission_rate: 0.22, languages: ["tr", "ru", "en"], jci: true, beds: 252 },
    { id: "ACI-IST-002", name: "Acıbadem Maslak", city: "Istanbul", country: "Turkey", specialties: ["aesthetic", "ophthalmology", "ivf", "checkup", "oncology"], rating: 4.9, commission_rate: 0.20, languages: ["tr", "en", "ar"], jci: true, beds: 300 },
    { id: "EST-ANT-003", name: "EsteNove Clinic", city: "Antalya", country: "Turkey", specialties: ["aesthetic", "hair", "dental", "dermatology"], rating: 4.7, commission_rate: 0.25, languages: ["tr", "ru", "en", "ar"], jci: false },
    { id: "DNT-IST-004", name: "DentGroup Istanbul", city: "Istanbul", country: "Turkey", specialties: ["dental"], rating: 4.5, commission_rate: 0.22, languages: ["tr", "en", "de"], jci: false },
    { id: "HCR-IST-005", name: "HairCure Istanbul", city: "Istanbul", country: "Turkey", specialties: ["hair", "dermatology"], rating: 4.6, commission_rate: 0.25, languages: ["tr", "ru", "en"], jci: false },
];

// ─────────────────────────────────────────────────────────────
// Hospital Data — Thailand / Phuket Coordination Centers
// ─────────────────────────────────────────────────────────────
const THAI_HOSPITALS: Hospital[] = [
    { id: "BKK-PHK-001", name: "Bangkok Hospital Phuket", city: "Phuket", country: "Thailand", specialties: ["checkup", "aesthetic", "ophthalmology", "dental"], rating: 4.7, commission_rate: 0.15, languages: ["th", "en", "ru"], jci: true, beds: 195 },
    { id: "SRJ-PHK-002", name: "Siriroj International Hospital", city: "Phuket", country: "Thailand", specialties: ["checkup", "aesthetic", "dermatology"], rating: 4.4, commission_rate: 0.15, languages: ["th", "en", "ru"], jci: false, beds: 100 },
    { id: "PHK-INT-003", name: "Phuket International Hospital", city: "Phuket", country: "Thailand", specialties: ["checkup", "dental", "aesthetic"], rating: 4.3, commission_rate: 0.15, languages: ["th", "en"], jci: false, beds: 100 },
    { id: "BMR-BKK-004", name: "Bumrungrad International", city: "Bangkok", country: "Thailand", specialties: ["oncology", "checkup", "ivf", "bariatric", "ophthalmology"], rating: 4.9, commission_rate: 0.12, languages: ["th", "en", "ar", "ru"], jci: true, beds: 580 },
];



// ─────────────────────────────────────────────────────────────
// Procedures, referral sources & specialty labels (all 6 languages)

// 6-language procedure lists
const PROCEDURES: Record<string, string[]> = {
    ru: ["Ринопластика", "Пересадка волос", "Стоматология / Виниры", "Липосакция", "Подтяжка живота", "Офтальмология (Lasik)", "Общий осмотр", "Онкология", "ЭКО / IVF", "Другое"],
    en: ["Rhinoplasty", "Hair Transplant", "Dental / Veneers", "Liposuction", "Abdominoplasty", "Eye Surgery (Lasik)", "Health Check-up", "Oncology", "IVF", "Other"],
    tr: ["Rinoplasti", "Saç Ekimi", "Diş / Veneer", "Liposuction", "Karın Germe", "Göz Ameliyatı (Lasik)", "Check-Up", "Onkoloji", "Tüp Bebek (IVF)", "Diğer"],
    th: ["เสริมจมูก", "ปลูกผม", "ทันตกรรม / วีเนียร์", "ดูดไขมัน", "กระชับหน้าท้อง", "ผ่าตัดตา (Lasik)", "ตรวจสุขภาพ", "มะเร็งวิทยา", "IVF", "อื่นๆ"],
    ar: ["رينوبلاستي", "زراعة الشعر", "طب الأسنان / القشرة", "شفط الدهون", "شد البطن", "جراحة العيون (Lasik)", "الفحص الطبي", "الأورام", "IVF", "أخرى"],
    zh: ["鼻整形", "植发", "牙科 / 贴面", "吸脂", "腹部整形", "眼科手术 (Lasik)", "健康检查", "肿瘤科", "IVF", "其他"],
};


const REFERRAL_SOURCES: Record<string, string[]> = {
    ru: ["Instagram", "Telegram", "Друзья / семья", "Google", "TikTok", "Другое"],
    en: ["Instagram", "Telegram", "Friends / Family", "Google", "TikTok", "Other"],
    tr: ["Instagram", "Telegram", "Arkadaş / Aile", "Google", "TikTok", "Diğer"],
    th: ["Instagram", "Telegram", "เพื่อน / ครอบครัว", "Google", "TikTok", "อื่นๆ"],
    ar: ["Instagram", "Telegram", "أصدقاء / عائلة", "Google", "TikTok", "أخرى"],
    zh: ["Instagram", "Telegram", "朋友 / 家人", "Google", "TikTok", "其他"],
};

const SPECIALTY_LABELS: Record<string, Record<string, string>> = {
    aesthetic: { ru: "Эстетика", en: "Aesthetic", tr: "Estetik", th: "ศัลยกรรมความงาม", ar: "تجميل", zh: "美容" },
    hair: { ru: "Волосы", en: "Hair", tr: "Saç", th: "ผม", ar: "شعر", zh: "植发" },
    dental: { ru: "Стоматология", en: "Dental", tr: "Diş", th: "ทันตกรรม", ar: "أسنان", zh: "牙科" },
    bariatric: { ru: "Бариатрия", en: "Bariatric", tr: "Obezite", th: "โรคอ้วน", ar: "بدانة", zh: "减重手术" },
    oncology: { ru: "Онкология", en: "Oncology", tr: "Onkoloji", th: "มะเร็ง", ar: "أورام", zh: "肿瘤" },
    checkup: { ru: "Осмотр", en: "Check-up", tr: "Check-Up", th: "ตรวจสุขภาพ", ar: "فحص", zh: "体检" },
    ophthalmology: { ru: "Офтальмология", en: "Eye", tr: "Göz", th: "ตา", ar: "عيون", zh: "眼科" },
    ivf: { ru: "ЭКО", en: "IVF", tr: "Tüp Bebek", th: "ทำเด็กหลอดแก้ว", ar: "IVF", zh: "试管婴儿" },
    dermatology: { ru: "Дерматология", en: "Dermatology", tr: "Dermatoloji", th: "ผิวหนัง", ar: "جلدية", zh: "皮肤科" },
};


// Treatment cards with pricing
const TREATMENT_DATA = [
    { key: "aesthetic", icon: "👃", pricesTR: 4500, pricesTH: 5200, pricesUK: 7500, pricesUS: 12000 },
    { key: "hair", icon: "💆", pricesTR: 3000, pricesTH: 4000, pricesUK: 8000, pricesUS: 15000 },
    { key: "dental", icon: "🦷", pricesTR: 2000, pricesTH: 2800, pricesUK: 5000, pricesUS: 8000 },
    { key: "checkup", icon: "🩺", pricesTR: 600, pricesTH: 800, pricesUK: 2000, pricesUS: 3500 },
    { key: "ophthalmology", icon: "👁", pricesTR: 2500, pricesTH: 3200, pricesUK: 5500, pricesUS: 6000 },
    { key: "bariatric", icon: "⚕️", pricesTR: 7500, pricesTH: 9000, pricesUK: 12000, pricesUS: 23000 },
    { key: "ivf", icon: "🍼", pricesTR: 4500, pricesTH: 5500, pricesUK: 8000, pricesUS: 20000 },
    { key: "oncology", icon: "🔬", pricesTR: 8000, pricesTH: 10000, pricesUK: 15000, pricesUS: 25000 },
];

// ─────────────────────────────────────────────────────────────
// Shared Input Styles
// ─────────────────────────────────────────────────────────────
const inputClass =
    "w-full rounded-xl bg-slate-50 border border-slate-200 px-4 py-3 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:border-cyan-500 focus:bg-white focus:ring-2 focus:ring-cyan-500/20 transition-all duration-300";
const selectClass =
    "w-full rounded-xl bg-slate-50 border border-slate-200 px-4 py-3 text-sm text-slate-800 focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 transition-all duration-300 cursor-pointer";
const labelClass =
    "block text-xs text-slate-500 mb-1.5 font-medium tracking-wide";

// ─────────────────────────────────────────────────────────────
// SVG Icons
// ─────────────────────────────────────────────────────────────
function MedicalCrossIcon({ className }: { className?: string }) {
    return (
        <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2v20M2 12h20" />
            <circle cx="12" cy="12" r="9" opacity={0.3} />
        </svg>
    );
}

function CheckIcon({ className }: { className?: string }) {
    return (
        <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round">
            <path d="M5 13l4 4L19 7" />
        </svg>
    );
}

function WhatsAppIcon({ className }: { className?: string }) {
    return (
        <svg className={className} fill="currentColor" viewBox="0 0 24 24">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z" />
            <path d="M12 2C6.477 2 2 6.477 2 12c0 1.89.525 3.66 1.438 5.168L2 22l4.832-1.438A9.955 9.955 0 0012 22c5.523 0 10-4.477 10-10S17.523 2 12 2zm0 18a8 8 0 01-4.076-1.104l-.292-.174-3.024.793.808-2.951-.19-.302A8 8 0 1112 20z" />
        </svg>
    );
}

function StarIcon({ className, filled }: { className?: string; filled?: boolean }) {
    return filled ? (
        <svg className={className} viewBox="0 0 20 20" fill="currentColor"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
    ) : (
        <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
    );
}

// ─────────────────────────────────────────────────────────────
// Components
// ─────────────────────────────────────────────────────────────

function TrustBadge({ value, label, icon }: { value: string; label: string; icon: string }) {
    return (
        <div className="flex flex-col items-center gap-1 px-4 py-3">
            <span className="text-2xl">{icon}</span>
            <span className="text-2xl sm:text-3xl font-bold text-cyan-700 font-display">{value}</span>
            <span className="text-[11px] text-slate-500 text-center font-medium tracking-wide">{label}</span>
        </div>
    );
}

function StepCard({ number, title, description, icon }: { number: number; title: string; description: string; icon: string }) {
    return (
        <div className="group relative flex flex-col items-center text-center p-6 rounded-2xl bg-white border border-slate-100 shadow-sm hover:shadow-xl hover:shadow-cyan-500/5 hover:border-cyan-200 transition-all duration-500">
            <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-cyan-600 text-white text-sm font-bold flex items-center justify-center shadow-lg shadow-cyan-500/30">
                {number}
            </div>
            <span className="text-4xl mt-2 mb-4 group-hover:scale-110 transition-transform duration-300">{icon}</span>
            <h3 className="text-base font-semibold text-slate-800 mb-2 font-display">{title}</h3>
            <p className="text-sm text-slate-500 leading-relaxed">{description}</p>
        </div>
    );
}

function TreatmentCard({ name, icon, priceTR, onClick }: { name: string; icon: string; priceTR: number; onClick?: () => void }) {
    return (
        <button
            type="button"
            onClick={onClick}
            className="group relative flex flex-col items-center text-center p-5 rounded-2xl bg-white border border-slate-100 shadow-sm hover:shadow-xl hover:shadow-cyan-500/5 hover:border-cyan-200 transition-all duration-500 cursor-pointer"
        >
            <span className="text-4xl mb-3 group-hover:scale-110 group-hover:-translate-y-1 transition-transform duration-500">{icon}</span>
            <h3 className="text-sm font-semibold text-slate-800 mb-1">{name}</h3>
            <div className="text-xs text-cyan-600 font-semibold font-mono">
                ${priceTR.toLocaleString()}
                <span className="text-slate-400 font-normal ml-1">USD</span>
            </div>
        </button>
    );
}

function HospitalCard({ hospital, lang, onSelect }: { hospital: Hospital; lang: string; onSelect?: () => void }) {
    const countryFlag = hospital.country === "Turkey" ? "🇹🇷" : "🇹🇭";
    return (
        <div className="group rounded-2xl border border-slate-100 bg-white p-5 shadow-sm hover:shadow-xl hover:shadow-cyan-500/5 hover:border-cyan-200 transition-all duration-500">
            <div className="flex items-start justify-between mb-3">
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                        <span className="text-lg">{countryFlag}</span>
                        <h3 className="text-sm font-semibold text-slate-800 group-hover:text-cyan-700 transition-colors truncate">{hospital.name}</h3>
                    </div>
                    <div className="text-xs text-slate-500">{hospital.city}, {hospital.country}</div>
                </div>
                <div className="flex items-center gap-1 ml-2 shrink-0">
                    <StarIcon className="w-3.5 h-3.5 text-amber-400" filled />
                    <span className="text-xs font-semibold text-slate-700">{hospital.rating}</span>
                </div>
            </div>

            <div className="flex flex-wrap gap-1.5 mb-3">
                {hospital.jci && (
                    <span className="text-[9px] px-2 py-0.5 rounded-md bg-cyan-50 border border-cyan-200 text-cyan-700 uppercase tracking-wider font-bold">
                        JCI
                    </span>
                )}
                {hospital.specialties.slice(0, 3).map((s) => (
                    <span key={s} className="text-[9px] px-2 py-0.5 rounded-md bg-slate-50 border border-slate-200 text-slate-600 uppercase tracking-wider font-medium">
                        {SPECIALTY_LABELS[s]?.[lang] ?? s}
                    </span>
                ))}
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-slate-100">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider font-medium">
                    {hospital.languages.join(" · ").toUpperCase()}
                </span>
                <button
                    type="button"
                    onClick={onSelect}
                    className="text-xs text-cyan-600 hover:text-cyan-800 font-semibold transition-colors duration-300"
                >
                    {lang === "ru" ? "Записаться" : lang === "tr" ? "Başvur" : lang === "ar" ? "استفسر" : lang === "zh" ? "咨询" : lang === "th" ? "สอบถาม" : "Inquire"} →
                </button>
            </div>
        </div>
    );
}

function SectionHeader({ title, subtitle }: { title: string; subtitle?: string }) {
    return (
        <div className="text-center mb-12">
            <h2 className="text-2xl sm:text-3xl font-display font-bold text-slate-800">{title}</h2>
            {subtitle && <p className="mt-3 text-slate-500 max-w-2xl mx-auto">{subtitle}</p>}
            <div className="mt-4 mx-auto w-16 h-1 rounded-full bg-gradient-to-r from-cyan-500 to-teal-500" />
        </div>
    );
}

function PatientJourney({ lang }: { lang: string }) {
    const steps: Record<string, string[]> = {
        ru: ["Заявка", "Подбор клиники", "Консültация", "Лечение"],
        en: ["Inquiry", "Clinic Match", "Consultation", "Treatment"],
        tr: ["Başvuru", "Klinik Eşleşme", "Konsültasyon", "Tedavi"],
        th: ["ส่งคำขอ", "จับคู่คลินิค", "ปรึกษา", "รักษา"],
        ar: ["الاستفسار", "مطابقة العيادة", "الاستشارة", "العلاج"],
        zh: ["提交申请", "匹配诊所", "咨询", "治疗"],
    };
    return (
        <div className="flex items-center justify-between gap-2 mb-6">
            {steps[lang].map((step, i) => (
                <div key={i} className="flex items-center gap-2 flex-1">
                    <div className="flex items-center gap-2 flex-1">
                        <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${i === 0
                            ? "bg-cyan-600 text-white shadow-md shadow-cyan-500/30"
                            : "bg-slate-100 text-slate-400 border border-slate-200"
                            }`}>
                            {i === 0 ? <CheckIcon className="w-3.5 h-3.5" /> : i + 1}
                        </div>
                        <span className={`text-xs tracking-wide ${i === 0 ? "text-cyan-700 font-semibold" : "text-slate-400"}`}>
                            {step}
                        </span>
                    </div>
                    {i < steps[lang].length - 1 && (
                        <div className={`w-6 h-px shrink-0 ${i === 0 ? "bg-cyan-300" : "bg-slate-200"}`} />
                    )}
                </div>
            ))}
        </div>
    );
}

// ─────────────────────────────────────────────────────────────
// Main Page
// ─────────────────────────────────────────────────────────────

export default function MedicalPage() {
    const { lang, t } = useLanguage();
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<IntakeResult | null>(null);
    const [hospitalTab, setHospitalTab] = useState<"turkey" | "thailand">("turkey");
    const [hospitals, setHospitals] = useState<Hospital[]>([]);
    const [hospitalsLoading, setHospitalsLoading] = useState(true);
    const [form, setForm] = useState({
        full_name: "",
        phone: "",
        procedure_interest: "",
        urgency: "routine" as Urgency,
        budget_usd: "",
        notes: "",
        referral_source: "",
        phuket_arrival_date: "",
    });

    useEffect(() => {
        getHospitals()
            .then((data) => {
                const mapped: Hospital[] = data.hospitals.map((h: ApiHospital) => ({
                    id: h.hospital_id,
                    name: h.name,
                    city: h.city,
                    country: h.country,
                    specialties: h.specialties,
                    rating: h.rating,
                    commission_rate: h.commission_rate,
                    languages: h.languages,
                    jci: h.jci_accredited ?? false,
                }));
                setHospitals(mapped);
            })
            .catch(() => {
                setHospitals([...TURKEY_HOSPITALS, ...THAI_HOSPITALS]);
            })
            .finally(() => setHospitalsLoading(false));
    }, []);


    const buildCoordinatorMessage = (patientId: string, hospitalName: string, cost: number): string => {
        const templates: Record<string, string> = {
            ru: `Здравствуйте! 🏥\n\nВаша заявка получена в AntiGravity Medical.\nНаш координатор свяжется с вами в течение 5 минут через WhatsApp.\n\n📋 Заявка: #${patientId}\n🏨 Рекомендуемая клиника: ${hospitalName}\n💰 Предварительная стоимость: $${cost.toLocaleString()} USD`,
            en: `Hello! 🏥\n\nYour inquiry has been received by AntiGravity Medical.\nOur coordinator will contact you via WhatsApp within 5 minutes.\n\n📋 Inquiry: #${patientId}\n🏨 Matched clinic: ${hospitalName}\n💰 Estimated cost: $${cost.toLocaleString()} USD`,
            tr: `Merhaba! 🏥\n\nBaşvurunuz AntiGravity Medical tarafından alındı.\nKoordinatörümüz 5 dakika içinde WhatsApp üzerinden iletişime geçecek.\n\n📋 Başvuru: #${patientId}\n🏨 Eşleşen klinik: ${hospitalName}\n💰 Tahmini maliyet: $${cost.toLocaleString()} USD`,
            th: `สวัสดี! 🏥\n\nคำขอของคุณได้รับแล้วจาก AntiGravity Medical\nผู้ประสานงานจะติดต่อผ่าน WhatsApp ภายใน 5 นาที\n\n📋 คำขอ: #${patientId}\n🏨 คลินิกที่จับคู่: ${hospitalName}\n💰 ค่าใช้จ่ายโดยประมาณ: $${cost.toLocaleString()} USD`,
            ar: `مرحباً! 🏥\n\nتم استلام استفسارك من AntiGravity Medical.\nسيتواصل منسقنا معك عبر واتساب خلال 5 دقائق.\n\n📋 الاستفسار: #${patientId}\n🏨 العيادة المقترنة: ${hospitalName}\n💰 التكلفة التقديرية: $${cost.toLocaleString()} USD`,
            zh: `您好! 🏥\n\nAntiGravity Medical已收到您的咨询。\n协调员将在5分钟内通过WhatsApp联系您。\n\n📋 咨询编号: #${patientId}\n🏨 匹配诊所: ${hospitalName}\n💰 预计费用: $${cost.toLocaleString()} USD`,
        };
        return templates[lang] ?? templates.en;
    };

    const buildNextSteps = (city: string): string[] => {
        const steps: Record<string, string[]> = {
            ru: [
                "📱 Координатор свяжется через WhatsApp (5 мин)",
                "📋 Пре-консультация на Пхукете",
                "🩺 Подготовка медицинских документов",
                `✈️ Организация трансфера в ${city}`,
                "💰 Окончательное ценовое предложение",
            ],
            en: [
                "📱 Coordinator contacts via WhatsApp (5 min)",
                "📋 Pre-consultation in Phuket",
                "🩺 Medical documents preparation",
                `✈️ Transfer to ${city} organized`,
                "💰 Final price quote & payment plan",
            ],
            tr: [
                "📱 Koordinatör WhatsApp'tan iletişime geçecek (5 dk)",
                "📋 Phuket'te ön konsültasyon",
                "🩺 Tıbbi belgeler hazırlanacak",
                `✈️ ${city} transferi organize edilecek`,
                "💰 Kesin fiyat teklifi ve ödeme planı",
            ],
            th: [
                `📱 ผู้ประสานงานจะติดต่อผ่าน WhatsApp (5 นาที)`,
                "📋 ปรึกษาเบื้องต้นที่ภูเก็ต",
                "🩺 เตรียมเอกสารทางการแพทย์",
                `✈️ จัดการรถรับส่งไป ${city}`,
                "💰 ใบเสนอราคาและแผนการชำระเงิน",
            ],
            ar: [
                "📱 سيتواصل المنسق عبر واتساب (5 دقائق)",
                "📋 استشارة أولية في بوكيت",
                "🩺 إعداد الوثائق الطبية",
                `✈️ تنظيم النقل إلى ${city}`,
                "💰 عرض السعر النهائي وخطة الدفع",
            ],
            zh: [
                "📱 协调员将通过WhatsApp联系您（5分钟内）",
                "📋 普吉岛预咨询",
                "🩺 准备医疗文件",
                `✈️ 安排前往${city}的交通`,
                "💰 最终报价和付款计划",
            ],
        };
        if (form.phuket_arrival_date) {
            const dateLine: Record<string, string> = {
                ru: `📅 Дата прибытия: ${form.phuket_arrival_date}`,
                en: `📅 Arrival date: ${form.phuket_arrival_date}`,
                tr: `📅 Geliş tarihi: ${form.phuket_arrival_date}`,
                th: `📅 วันที่เดินทางมาถึง: ${form.phuket_arrival_date}`,
                ar: `📅 تاريخ الوصول: ${form.phuket_arrival_date}`,
                zh: `📅 到达日期: ${form.phuket_arrival_date}`,
            };
            (steps[lang] ?? steps.en).push(dateLine[lang] ?? dateLine.en);
        }
        return steps[lang] ?? steps.en;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await fetch("/api/medical/intake", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    ...form,
                    language: lang,
                    budget_usd: form.budget_usd ? parseFloat(form.budget_usd) : null,
                }),
            });
            if (!res.ok) throw new Error(await res.text());
            const data: IntakeResult = await res.json();
            setResult(data);
        } catch {
            const demoHospital = TURKEY_HOSPITALS[2];
            const patientId = `MED-${new Date().toISOString().slice(0, 10).replace(/-/g, "")}-${Math.random().toString(36).slice(2, 8).toUpperCase()}`;
            setResult({
                patient_id: patientId,
                procedure_category: "aesthetic",
                matched_hospital: {
                    name: demoHospital.name,
                    city: demoHospital.city,
                    country: demoHospital.country,
                    rating: demoHospital.rating,
                    commission_rate: demoHospital.commission_rate,
                    contact_whatsapp: "+905003456789",
                    specialties: demoHospital.specialties,
                    languages: demoHospital.languages,
                },
                estimated_procedure_cost_usd: 4500,
                commission_usd: 4500 * demoHospital.commission_rate,
                coordinator_message: buildCoordinatorMessage(patientId, demoHospital.name, 4500),
                next_steps: buildNextSteps(demoHospital.city),
            });
        } finally {
            setLoading(false);
        }
    };

    const selectProcedure = (procedureValue: string) => {
        setForm({ ...form, procedure_interest: procedureValue });
        document.getElementById("intake-form")?.scrollIntoView({ behavior: "smooth" });
    };

    const scrollToForm = () => {
        document.getElementById("intake-form")?.scrollIntoView({ behavior: "smooth" });
    };

    const turkeyHospitals = hospitals.length > 0
        ? hospitals.filter(h => h.country === "Turkey")
        : TURKEY_HOSPITALS;
    const thaiHospitals = hospitals.length > 0
        ? hospitals.filter(h => h.country === "Thailand")
        : THAI_HOSPITALS;
    const displayHospitals = hospitalTab === "turkey" ? turkeyHospitals : thaiHospitals;

    return (
        <div className="min-h-screen bg-white text-slate-800 selection:bg-cyan-100 selection:text-cyan-900">

            {/* ══════════ Header ══════════ */}
            <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-xl border-b border-slate-100 shadow-sm">
                <div className="container-main h-16 flex items-center justify-between">
                    <Link href="/" className="flex items-center gap-2.5">
                        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-500 to-teal-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
                            <MedicalCrossIcon className="w-5 h-5 text-white" />
                        </div>
                        <div className="hidden sm:block">
                            <span className="text-sm font-bold text-slate-800 tracking-tight">AntiGravity</span>
                            <span className="text-sm font-bold text-cyan-600 ml-1">Medical</span>
                        </div>
                    </Link>

                    <nav className="hidden md:flex items-center gap-6 text-sm text-slate-600">
                        <a href="#treatments" className="hover:text-cyan-600 transition-colors">{t("medTreatmentsTitle")}</a>
                        <a href="#hospitals" className="hover:text-cyan-600 transition-colors">{t("medHospitalsTitle")}</a>
                        <a href="#pricing" className="hover:text-cyan-600 transition-colors">{t("medPriceTitle")}</a>
                    </nav>

                    <div className="flex items-center gap-3">
                        <LanguagePicker />

                        <button
                            type="button"
                            onClick={scrollToForm}
                            className="hidden sm:inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-cyan-600 text-white text-sm font-semibold shadow-lg shadow-cyan-500/20 hover:bg-cyan-700 transition-all duration-300"
                        >
                            {t("medHeroBtn")}
                        </button>
                    </div>
                </div>
            </header>

            {/* ══════════ Hero Section ══════════ */}
            <section className="relative overflow-hidden bg-gradient-to-b from-slate-50 to-white pt-16 sm:pt-24 pb-8 sm:pb-16">
                {/* Decorative blobs */}
                <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-100/40 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3 pointer-events-none" />
                <div className="absolute bottom-0 left-0 w-72 h-72 bg-teal-100/30 rounded-full blur-3xl translate-y-1/3 -translate-x-1/4 pointer-events-none" />

                <div className="container-main relative">
                    <div className="max-w-3xl mx-auto text-center animate-fade-up">
                        <div className="inline-flex items-center gap-2 rounded-full border border-cyan-200 bg-cyan-50 px-4 py-1.5 mb-6">
                            <span className="h-2 w-2 rounded-full bg-cyan-500 animate-pulse" />
                            <span className="text-xs font-semibold text-cyan-700 tracking-wide">
                                {t("medBadge")}
                            </span>
                        </div>

                        <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-900 leading-tight">
                            {t("medTitle")}
                        </h1>

                        <p className="mt-5 text-slate-500 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
                            {t("medSubtitle")}
                        </p>

                        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
                            <a
                                href="#intake-form"
                                className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-gradient-to-r from-cyan-600 to-teal-600 text-white text-sm font-semibold shadow-xl shadow-cyan-500/25 hover:from-cyan-500 hover:to-teal-500 hover:shadow-cyan-500/35 transition-all duration-300"
                            >
                                {t("medHeroBtn")}
                                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                                </svg>
                            </a>
                            <a
                                href="#pricing"
                                className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl border-2 border-slate-200 text-slate-600 text-sm font-semibold hover:border-cyan-300 hover:text-cyan-700 transition-all duration-300"
                            >
                                {t("medHeroBtnAlt")}
                            </a>
                        </div>
                    </div>
                </div>
            </section>

            {/* ══════════ Trust Bar ══════════ */}
            <section className="border-y border-slate-100 bg-white">
                <div className="container-main py-6">
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 divide-x divide-slate-100">
                        <TrustBadge icon="👥" value="2,500+" label={t("medTrustPatients")} />
                        <TrustBadge icon="🌍" value="45+" label={t("medTrustCountries")} />
                        <TrustBadge icon="🏥" value="9" label={t("medTrustClinics")} />
                        <TrustBadge icon="💰" value="70%" label={t("medTrustSavings")} />
                    </div>
                </div>
            </section>

            {/* ══════════ How It Works ══════════ */}
            <section className="section-padding bg-slate-50/50">
                <div className="container-main">
                    <SectionHeader title={t("medHowTitle")} />
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 pt-4">
                        <div className="animate-fade-up stagger-1">
                            <StepCard number={1} title={t("medStep1")} description={t("medStep1d")} icon="📝" />
                        </div>
                        <div className="animate-fade-up stagger-2">
                            <StepCard number={2} title={t("medStep2")} description={t("medStep2d")} icon="🤖" />
                        </div>
                        <div className="animate-fade-up stagger-3">
                            <StepCard number={3} title={t("medStep3")} description={t("medStep3d")} icon="🏥" />
                        </div>
                        <div className="animate-fade-up stagger-4">
                            <StepCard number={4} title={t("medStep4")} description={t("medStep4d")} icon="🩺" />
                        </div>
                    </div>
                </div>
            </section>

            {/* ══════════ Treatments ══════════ */}
            <section id="treatments" className="section-padding bg-white scroll-mt-20">
                <div className="container-main">
                    <SectionHeader title={t("medTreatmentsTitle")} />
                    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                        {TREATMENT_DATA.map((item, i) => (
                            <div key={item.key} className={`animate-fade-up stagger-${i + 1}`}>
                                <TreatmentCard
                                    name={SPECIALTY_LABELS[item.key]?.[lang] ?? item.key}
                                    icon={item.icon}
                                    priceTR={item.pricesTR}
                                    onClick={() => {
                                        const procedureIdx = ["aesthetic", "hair", "dental", "checkup", "ophthalmology", "bariatric", "ivf", "oncology"].indexOf(item.key);
                                        const mapping = [0, 1, 2, 6, 5, 3, 8, 7];
                                        if (procedureIdx >= 0 && mapping[procedureIdx] !== undefined) {
                                            selectProcedure(PROCEDURES[lang][mapping[procedureIdx]]);
                                        }
                                    }}
                                />
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ══════════ Price Comparison ══════════ */}
            <section id="pricing" className="section-padding bg-gradient-to-b from-slate-900 to-slate-800 text-white scroll-mt-20">
                <div className="container-main">
                    <div className="text-center mb-12">
                        <h2 className="text-2xl sm:text-3xl font-display font-bold text-white">{t("medPriceTitle")}</h2>
                        <div className="mt-4 mx-auto w-16 h-1 rounded-full bg-gradient-to-r from-cyan-400 to-teal-400" />
                    </div>

                    <div className="overflow-x-auto rounded-2xl border border-slate-700">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="bg-slate-800/80 border-b border-slate-700">
                                    <th className="text-left px-5 py-4 text-xs uppercase tracking-wider text-slate-400 font-semibold">{t("medPriceProc")}</th>
                                    <th className="text-center px-5 py-4 text-xs uppercase tracking-wider text-cyan-400 font-bold">🇹🇷 {t("medPriceTurkey")}</th>
                                    <th className="text-center px-5 py-4 text-xs uppercase tracking-wider text-teal-400 font-bold">🇹🇭 {t("medPriceThailand")}</th>
                                    <th className="text-center px-5 py-4 text-xs uppercase tracking-wider text-slate-400 font-semibold">🇬🇧 {t("medPriceUK")}</th>
                                    <th className="text-center px-5 py-4 text-xs uppercase tracking-wider text-slate-400 font-semibold">🇺🇸 {t("medPriceUSA")}</th>
                                    <th className="text-center px-5 py-4 text-xs uppercase tracking-wider text-emerald-400 font-bold">{t("medPriceSave")}</th>
                                </tr>
                            </thead>
                            <tbody>
                                {TREATMENT_DATA.map((item, i) => {
                                    const savings = Math.round((1 - item.pricesTR / item.pricesUS) * 100);
                                    return (
                                        <tr key={item.key} className={`border-b border-slate-700/50 ${i % 2 === 0 ? "bg-slate-800/30" : "bg-slate-800/10"} hover:bg-slate-700/30 transition-colors`}>
                                            <td className="px-5 py-4 font-medium text-slate-200">
                                                <span className="mr-2">{item.icon}</span>
                                                {SPECIALTY_LABELS[item.key]?.[lang] ?? item.key}
                                            </td>
                                            <td className="text-center px-5 py-4 text-cyan-300 font-bold font-mono">${item.pricesTR.toLocaleString()}</td>
                                            <td className="text-center px-5 py-4 text-teal-300 font-mono">${item.pricesTH.toLocaleString()}</td>
                                            <td className="text-center px-5 py-4 text-slate-400 font-mono">${item.pricesUK.toLocaleString()}</td>
                                            <td className="text-center px-5 py-4 text-slate-400 font-mono">${item.pricesUS.toLocaleString()}</td>
                                            <td className="text-center px-5 py-4">
                                                <span className="inline-flex px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold">
                                                    {savings}%
                                                </span>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                    <p className="text-center text-xs text-slate-500 mt-4">
                        * {lang === "ru" ? "Ориентировочные цены. Точная стоимость определяется после консультации." : lang === "tr" ? "Tahmini fiyatlar. Kesin fiyat konsültasyon sonrası belirlenir." : "Approximate prices. Final cost determined after consultation."}
                    </p>
                </div>
            </section>

            {/* ══════════ Partner Hospitals ══════════ */}
            <section id="hospitals" className="section-padding bg-white scroll-mt-20">
                <div className="container-main">
                    <SectionHeader title={t("medHospitalsTitle")} />

                    {/* Tabs */}
                    <div className="flex items-center justify-center gap-2 mb-8">
                        <button
                            type="button"
                            onClick={() => setHospitalTab("turkey")}
                            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300 ${hospitalTab === "turkey"
                                ? "bg-cyan-600 text-white shadow-lg shadow-cyan-500/20"
                                : "bg-slate-50 text-slate-500 border border-slate-200 hover:border-cyan-200 hover:text-cyan-600"
                                }`}
                        >
                            🇹🇷 {t("medHospitalsTurkey")}
                        </button>
                        <button
                            type="button"
                            onClick={() => setHospitalTab("thailand")}
                            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300 ${hospitalTab === "thailand"
                                ? "bg-teal-600 text-white shadow-lg shadow-teal-500/20"
                                : "bg-slate-50 text-slate-500 border border-slate-200 hover:border-teal-200 hover:text-teal-600"
                                }`}
                        >
                            🇹🇭 {t("medHospitalsThailand")}
                        </button>
                    </div>

                    {hospitalsLoading ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                            {[1, 2, 3].map((i) => (
                                <div key={i} className="rounded-2xl border border-slate-100 bg-white p-5 animate-pulse">
                                    <div className="h-4 bg-slate-200 rounded w-3/4 mb-3" />
                                    <div className="h-3 bg-slate-100 rounded w-1/2 mb-4" />
                                    <div className="flex gap-2 mb-4">
                                        <div className="h-5 bg-slate-100 rounded w-12" />
                                        <div className="h-5 bg-slate-100 rounded w-16" />
                                    </div>
                                    <div className="h-3 bg-slate-100 rounded w-full" />
                                </div>
                            ))}
                            <p className="col-span-full text-center text-sm text-slate-400 mt-2">{t("medLoadingHospitals")}</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                            {displayHospitals.map((h) => (
                                <HospitalCard key={h.id} hospital={h} lang={lang} onSelect={scrollToForm} />
                            ))}
                        </div>
                    )}
                </div>
            </section>

            {/* ══════════ Why Choose Us ══════════ */}
            <section className="section-padding bg-slate-50/50">
                <div className="container-main">
                    <SectionHeader title={t("medWhyTitle")} />
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {[
                            { icon: "🏅", title: t("medWhy1"), desc: t("medWhy1d") },
                            { icon: "🗣️", title: t("medWhy2"), desc: t("medWhy2d") },
                            { icon: "💎", title: t("medWhy3"), desc: t("medWhy3d") },
                            { icon: "✈️", title: t("medWhy4"), desc: t("medWhy4d") },
                            { icon: "🤖", title: t("medWhy5"), desc: t("medWhy5d") },
                            { icon: "🌏", title: t("medWhy6"), desc: t("medWhy6d") },
                        ].map((item, i) => (
                            <div key={i} className={`flex gap-4 p-5 rounded-2xl bg-white border border-slate-100 shadow-sm hover:shadow-md hover:border-cyan-200 transition-all duration-500 animate-fade-up stagger-${i + 1}`}>
                                <span className="text-3xl shrink-0">{item.icon}</span>
                                <div>
                                    <h3 className="text-sm font-semibold text-slate-800 mb-1">{item.title}</h3>
                                    <p className="text-xs text-slate-500 leading-relaxed">{item.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ══════════ Intake Form / Result ══════════ */}
            <section id="intake-form" className="section-padding bg-white scroll-mt-20">
                <div className="max-w-2xl mx-auto px-4 sm:px-6">
                    {!result ? (
                        <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-10 shadow-xl shadow-slate-200/50 animate-fade-up">
                            <div className="flex items-center gap-3 mb-8">
                                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-cyan-500 to-teal-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
                                    <MedicalCrossIcon className="w-6 h-6 text-white" />
                                </div>
                                <div>
                                    <h2 className="text-xl font-display font-bold text-slate-800">{t("medFormTitle")}</h2>
                                    <p className="text-xs text-slate-500 mt-0.5">{t("medFormSub")}</p>
                                </div>
                            </div>

                            <form onSubmit={handleSubmit} className="space-y-5">
                                {/* Name + Phone */}
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                    <div>
                                        <label htmlFor="intake-name" className={labelClass}>{t.name} *</label>
                                        <input id="intake-name" required value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} className={inputClass} placeholder="John Doe" />
                                    </div>
                                    <div>
                                        <label htmlFor="intake-phone" className={labelClass}>{t("fieldPhone")} *</label>
                                        <input id="intake-phone" required value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} className={inputClass} placeholder="+66 xxx xxx xxxx" />
                                    </div>
                                </div>

                                {/* Procedure */}
                                <div>
                                    <label htmlFor="intake-procedure" className={labelClass}>{t("medFieldProcedure")} *</label>
                                    <select id="intake-procedure" required value={form.procedure_interest} onChange={(e) => setForm({ ...form, procedure_interest: e.target.value })} className={selectClass}>
                                        <option value="">—</option>
                                        {PROCEDURES[lang].map((p) => <option key={p} value={p}>{p}</option>)}
                                    </select>
                                </div>

                                {/* Urgency + Budget */}
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label htmlFor="intake-urgency" className={labelClass}>{t("medFieldUrgency")}</label>
                                        <select id="intake-urgency" value={form.urgency} onChange={(e) => setForm({ ...form, urgency: e.target.value as Urgency })} className={selectClass}>
                                            <option value="routine">{t("medUrgencyR")}</option>
                                            <option value="soon">{t("medUrgencyS")}</option>
                                            <option value="urgent">{t("medUrgencyU")}</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label htmlFor="intake-budget" className={labelClass}>{t("medFieldBudget")}</label>
                                        <input id="intake-budget" type="number" min={0} value={form.budget_usd} onChange={(e) => setForm({ ...form, budget_usd: e.target.value })} className={inputClass} placeholder="5000" />
                                    </div>
                                </div>

                                {/* Arrival + Source */}
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label htmlFor="intake-arrival" className={labelClass}>{t("medFieldArrival")}</label>
                                        <input id="intake-arrival" type="date" value={form.phuket_arrival_date} onChange={(e) => setForm({ ...form, phuket_arrival_date: e.target.value })} className={inputClass} />
                                    </div>
                                    <div>
                                        <label htmlFor="intake-source" className={labelClass}>{t("medFieldReferral")}</label>
                                        <select id="intake-source" value={form.referral_source} onChange={(e) => setForm({ ...form, referral_source: e.target.value })} className={selectClass}>
                                            <option value="">—</option>
                                            {REFERRAL_SOURCES[lang].map((s) => <option key={s} value={s}>{s}</option>)}
                                        </select>
                                    </div>
                                </div>

                                {/* Notes */}
                                <div>
                                    <label htmlFor="intake-notes" className={labelClass}>{t("fieldNotes")}</label>
                                    <textarea id="intake-notes" rows={3} value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} className={`${inputClass} resize-none`} />
                                </div>

                                <button
                                    id="intake-submit"
                                    type="submit"
                                    disabled={loading}
                                    className="group relative w-full rounded-xl py-3.5 text-sm font-semibold text-white overflow-hidden transition-all duration-300 disabled:opacity-50 cursor-pointer"
                                >
                                    <div className="absolute inset-0 bg-gradient-to-r from-cyan-600 to-teal-600 transition-all duration-300 group-hover:from-cyan-500 group-hover:to-teal-500" />
                                    <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 shadow-[0_8px_32px_rgba(6,182,212,0.3)]" />
                                    <span className="relative flex items-center justify-center gap-2">
                                        {loading ? (
                                            <>
                                                <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
                                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                                </svg>
                                                {t("btnSubmitting")}
                                            </>
                                        ) : t("btnSubmit")}
                                    </span>
                                </button>
                            </form>
                        </div>
                    ) : (
                        /* ── Success Card ── */
                        <div className="rounded-3xl border border-cyan-200 bg-gradient-to-b from-cyan-50 to-white p-6 sm:p-10 shadow-xl shadow-cyan-100/50 animate-fade-up">
                            <div className="flex items-center gap-4 mb-6">
                                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-500 to-teal-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
                                    <CheckIcon className="w-7 h-7 text-white" />
                                </div>
                                <div>
                                    <h2 className="text-xl font-display font-bold text-slate-800">{t("medSuccess")}</h2>
                                    <div className="text-xs text-cyan-600 font-mono mt-0.5 font-semibold tracking-wide">{result.patient_id}</div>
                                </div>
                            </div>

                            <PatientJourney lang={lang} />

                            {/* Coordinator message */}
                            <div className="rounded-2xl border border-cyan-200 bg-cyan-50/50 p-4 mb-6">
                                <div className="flex items-center gap-2 mb-2">
                                    <span className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse" />
                                    <span className="text-[11px] text-cyan-700 uppercase tracking-wider font-semibold">{t("medCoordMsg")}</span>
                                </div>
                                <pre className="text-xs text-slate-600 leading-relaxed whitespace-pre-wrap font-body">
                                    {result.coordinator_message}
                                </pre>
                            </div>

                            {/* Matched hospital */}
                            {result.matched_hospital && (
                                <div className="rounded-2xl border border-slate-200 bg-white p-5 mb-6 shadow-sm">
                                    <div className="text-[10px] text-slate-400 uppercase tracking-widest mb-3 font-semibold">{t("medMatchedClinic")}</div>
                                    <h3 className="text-lg font-display font-bold text-slate-800">{result.matched_hospital.name}</h3>
                                    <div className="text-sm text-slate-500 mt-1 flex items-center gap-2">
                                        <span>{result.matched_hospital.city}, {result.matched_hospital.country || "Turkey"}</span>
                                        <span className="w-1 h-1 rounded-full bg-slate-300" />
                                        <span className="flex items-center gap-1 text-amber-500">
                                            <StarIcon className="w-3.5 h-3.5" filled />
                                            {result.matched_hospital.rating}
                                        </span>
                                    </div>

                                    {result.matched_hospital.specialties && (
                                        <div className="flex flex-wrap gap-1.5 mt-3">
                                            {result.matched_hospital.specialties.map((s) => (
                                                <span key={s} className="text-[9px] px-2 py-0.5 rounded-md bg-slate-50 border border-slate-200 text-slate-600 uppercase tracking-wider font-medium">
                                                    {SPECIALTY_LABELS[s]?.[lang] ?? s}
                                                </span>
                                            ))}
                                        </div>
                                    )}

                                    <div className="grid grid-cols-2 gap-3 mt-4 pt-4 border-t border-slate-100">
                                        <div>
                                            <div className="text-[10px] text-slate-400 uppercase tracking-wider mb-1">{t("medCostEstimate")}</div>
                                            <div className="text-lg text-slate-800 font-mono font-bold">${result.estimated_procedure_cost_usd.toLocaleString()}</div>
                                        </div>
                                        <div>
                                            <div className="text-[10px] text-slate-400 uppercase tracking-wider mb-1">{t("medCommission")}</div>
                                            <div className="text-lg text-cyan-600 font-mono font-bold">
                                                ${result.commission_usd.toLocaleString()} <span className="text-sm text-slate-400">({result.commission_rate_pct ?? `${(result.matched_hospital.commission_rate * 100).toFixed(0)}%`})</span>
                                            </div>
                                        </div>
                                    </div>

                                    {result.matched_hospital.contact_whatsapp && (
                                        <a
                                            href={`https://wa.me/${result.matched_hospital.contact_whatsapp.replace("+", "")}`}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            id="whatsapp-link"
                                            className="mt-4 inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#25D366] text-white text-sm font-semibold hover:bg-[#20BD5A] shadow-lg shadow-green-500/20 transition-all duration-300"
                                        >
                                            <WhatsAppIcon className="w-4 h-4" />
                                            WhatsApp
                                        </a>
                                    )}
                                </div>
                            )}

                            {/* Next Steps */}
                            <div className="space-y-3 mb-8">
                                <div className="text-[10px] text-slate-400 uppercase tracking-widest font-semibold mb-3">
                                    {lang === "ru" ? "Следующие шаги" : lang === "en" ? "Next Steps" : "Sonraki Adımlar"}
                                </div>
                                {result.next_steps.map((step, i) => (
                                    <div key={i} className="flex gap-3 items-start">
                                        <span className="shrink-0 w-7 h-7 rounded-lg bg-cyan-50 border border-cyan-200 flex items-center justify-center text-xs font-bold text-cyan-700 mt-0.5">
                                            {i + 1}
                                        </span>
                                        <span className="text-sm text-slate-600 leading-relaxed">{step}</span>
                                    </div>
                                ))}
                            </div>

                            <button
                                id="new-intake-btn"
                                type="button"
                                onClick={() => setResult(null)}
                                className="w-full rounded-xl border-2 border-slate-200 bg-white py-3 text-sm text-slate-500 font-semibold hover:text-cyan-700 hover:bg-cyan-50 hover:border-cyan-300 transition-all duration-300"
                            >
                                {t("btnNewRequest")}
                            </button>
                        </div>
                    )}
                </div>
            </section>

            {/* ══════════ Footer ══════════ */}
            <footer className="bg-slate-900 text-white pt-16 pb-8">
                <div className="container-main">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mb-10">
                        {/* Brand */}
                        <div>
                            <div className="flex items-center gap-2.5 mb-4">
                                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-500 to-teal-600 flex items-center justify-center">
                                    <MedicalCrossIcon className="w-5 h-5 text-white" />
                                </div>
                                <div>
                                    <span className="text-sm font-bold text-white">AntiGravity</span>
                                    <span className="text-sm font-bold text-cyan-400 ml-1">Medical</span>
                                </div>
                            </div>
                            <p className="text-sm text-slate-400 leading-relaxed max-w-xs">{t("medFooterTagline")}</p>
                            <div className="flex items-center gap-3 mt-5">
                                <span className="text-[9px] px-2.5 py-1 rounded bg-cyan-900/50 border border-cyan-700/30 text-cyan-400 uppercase tracking-wider font-bold">JCI Partner</span>
                                <span className="text-[9px] px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-slate-400 uppercase tracking-wider font-bold">TURSAB</span>
                            </div>
                        </div>

                        {/* Quick Links */}
                        <div>
                            <h4 className="text-xs text-slate-500 uppercase tracking-widest font-semibold mb-4">{t("medTreatmentsTitle")}</h4>
                            <div className="grid grid-cols-2 gap-2 text-sm text-slate-400">
                                {PROCEDURES[lang].slice(0, 8).map((p) => (
                                    <a key={p} href="#intake-form" className="hover:text-cyan-400 transition-colors">{p}</a>
                                ))}
                            </div>
                        </div>

                        {/* Contact */}
                        <div>
                            <h4 className="text-xs text-slate-500 uppercase tracking-widest font-semibold mb-4">{t("medFooterContact")}</h4>
                            <div className="space-y-3 text-sm text-slate-400">
                                <div className="flex items-center gap-2">
                                    <span>📍</span>
                                    <span>Phuket, Thailand</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <span>📍</span>
                                    <span>Istanbul & Antalya, Turkey</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <WhatsAppIcon className="w-4 h-4 text-green-400" />
                                    <span>+66 XX XXX XXXX</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <span>📧</span>
                                    <span>medical@antigravity.co</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="border-t border-slate-800 pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-600">
                        <span>&copy; {new Date().getFullYear()} AntiGravity Ventures. All rights reserved.</span>
                        <span className="flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse" />
                            Medical coordination active — Phuket & Turkey
                        </span>
                    </div>
                </div>
            </footer>

            {/* ══════════ Floating WhatsApp Button ══════════ */}
            <a
                href="https://wa.me/66XXXXXXXXX"
                target="_blank"
                rel="noopener noreferrer"
                className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-[#25D366] text-white flex items-center justify-center shadow-2xl shadow-green-500/30 hover:bg-[#20BD5A] hover:scale-110 transition-all duration-300 whatsapp-pulse"
                aria-label="WhatsApp"
            >
                <WhatsAppIcon className="w-7 h-7" />
            </a>
        </div>
    );
}
