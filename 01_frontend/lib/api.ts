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

/** Hospital object returned by GET /api/medical/hospitals */
export interface ApiHospital {
    hospital_id: string;
    name: string;
    city: string;
    country: string;
    specialties: string[];
    commission_rate: number;
    contact_whatsapp?: string | null;
    avg_procedure_cost_usd?: number | null;
    rating: number;
    languages: string[];
    jci_accredited?: boolean;
    active?: boolean;
}

/** Full intake response from POST /api/medical/intake */
export interface IntakeResponse {
    success: boolean;
    patient_id: string;
    procedure_category: string;
    message: string;
    matched_hospital: ApiHospital | null;
    estimated_procedure_cost_usd: number;
    commission_rate_pct: string;
    commission_usd: number;
    next_steps: string[];
    coordinator_message: string;
    record?: Record<string, unknown>;
}

/** Hotel suggestion inside TravelResponse */
export interface TravelSuggestion {
    name: string;
    stars: number;
    price_night_usd: number;
    highlight: string;
}

/** Full travel response from POST /api/travel/options */
export interface TravelResponse {
    request_id: string;
    status: string;
    coordinator_message: string;
    suggestions: TravelSuggestion[];
    next_steps: string[];
}

/** Destination object from GET /api/travel/destinations */
export interface Destination {
    id: string;
    name: string;
    country: string;
    flag: string;
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
    apiFetch<IntakeResponse>("/medical/intake", {
        method: "POST",
        body: JSON.stringify(body),
    });

/** Get partner hospitals */
export const getHospitals = () =>
    apiFetch<{ total: number; hospitals: ApiHospital[] }>("/medical/hospitals");

/** Get procedure categories + pricing */
export const getProcedures = () =>
    apiFetch<{ categories: unknown[] }>("/medical/procedures");

/** Get commission pipeline summary */
export const getCommissionSummary = () =>
    apiFetch<Record<string, unknown>>("/medical/commission/summary");

/** Submit travel planning request */
export const submitTravelRequest = (body: TravelRequestBody) =>
    apiFetch<TravelResponse>("/travel/options", {
        method: "POST",
        body: JSON.stringify(body),
    });

/** Get available travel destinations */
export const getDestinations = () =>
    apiFetch<{ destinations: Destination[] }>("/travel/destinations");
