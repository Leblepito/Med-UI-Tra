/**
 * AntiGravity ThaiTurk — Frontend API Helper
 * All backend requests go through /api/* (proxied to FastAPI via next.config.ts)
 */

const BASE = "/api";

// ──────────────────────────────────────────────────
// Types
// ──────────────────────────────────────────────────

export interface ClassifyRequest {
    message: string;
    language?: string;
}

export interface ClassifyResult {
    sector: string;
    confidence: number;
    keywords_matched: string[];
    reasoning: string;
}

export interface MedicalIntakeBody {
    full_name: string;
    phone: string;
    language: "ru" | "en" | "tr" | "th";
    procedure_interest: string;
    urgency: "routine" | "soon" | "urgent" | "emergency";
    budget_usd?: number | null;
    notes?: string;
    referral_source?: string;
    phuket_arrival_date?: string;
}

export interface TravelRequestBody {
    full_name: string;
    phone: string;
    language?: string;
    destination?: string;
    check_in?: string;
    check_out?: string;
    guests?: number;
    notes?: string;
}

// ──────────────────────────────────────────────────
// Core fetch helper
// ──────────────────────────────────────────────────

async function apiFetch<T>(
    path: string,
    options?: RequestInit
): Promise<T> {
    const res = await fetch(`${BASE}${path}`, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(`API error ${res.status}: ${text}`);
    }
    return res.json() as Promise<T>;
}

// ──────────────────────────────────────────────────
// Endpoints
// ──────────────────────────────────────────────────

/** Health check */
export const healthCheck = () =>
    apiFetch<{ status: string; version: string }>("/health".replace("/api", ""));

/** Classify incoming request text → sector */
export const classifyRequest = (body: ClassifyRequest) =>
    apiFetch<ClassifyResult>("/classify", {
        method: "POST",
        body: JSON.stringify(body),
    });

/** Submit medical patient intake form */
export const submitMedicalIntake = (body: MedicalIntakeBody) =>
    apiFetch<Record<string, unknown>>("/medical/intake", {
        method: "POST",
        body: JSON.stringify(body),
    });

/** Get partner hospitals */
export const getHospitals = () =>
    apiFetch<{ total: number; hospitals: unknown[] }>("/medical/hospitals");

/** Get procedure categories + pricing */
export const getProcedures = () =>
    apiFetch<{ categories: unknown[] }>("/medical/procedures");

/** Get commission pipeline summary */
export const getCommissionSummary = () =>
    apiFetch<Record<string, unknown>>("/medical/commission/summary");

/** Submit travel planning request */
export const submitTravelRequest = (body: TravelRequestBody) =>
    apiFetch<Record<string, unknown>>("/travel/options", {
        method: "POST",
        body: JSON.stringify(body),
    });
