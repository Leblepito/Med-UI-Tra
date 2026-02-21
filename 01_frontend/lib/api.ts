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
    language: "ru" | "en" | "tr" | "th" | "ar" | "zh";
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

/** Health check — backend exposes /health (not under /api) */
export const healthCheck = async () => {
    const res = await fetch("/health", { headers: { "Content-Type": "application/json" } });
    if (!res.ok) throw new Error(`API error ${res.status}`);
    return res.json() as Promise<{ status: string; version: string }>;
};

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

// ──────────────────────────────────────────────────
// Chat
// ──────────────────────────────────────────────────

export interface ChatStartSessionBody {
    language: string;
    user_name?: string;
}

export interface ChatStartSessionResponse {
    session_id: string;
    greeting: string;
    language: string;
}

export interface ChatSendMessageBody {
    session_id: string;
    message: string;
    language?: string;
}

export interface ChatMessageResponse {
    session_id: string;
    message_id: string;
    response: string;
    tool_results: Record<string, unknown>[];
    tokens_used: { input: number; output: number };
    timestamp: string;
}

/** Start a new chat session */
export const chatStartSession = (body: ChatStartSessionBody) =>
    apiFetch<ChatStartSessionResponse>("/chat/session", {
        method: "POST",
        body: JSON.stringify(body),
    });

/** Send a chat message and get AI response */
export const chatSendMessage = (body: ChatSendMessageBody) =>
    apiFetch<ChatMessageResponse>("/chat/message", {
        method: "POST",
        body: JSON.stringify(body),
    });

/** Get chat history for a session */
export const chatGetHistory = (sessionId: string) =>
    apiFetch<{ session_id: string; messages: Record<string, unknown>[]; total: number }>(
        `/chat/history/${sessionId}`,
    );

// ──────────────────────────────────────────────────
// Blog
// ──────────────────────────────────────────────────

export interface BlogPostItem {
    id: string;
    slug: string;
    title: string;
    excerpt: string;
    body?: string;
    category: string;
    featured: boolean;
    author: string;
    date: string;
    read_time: number;
    image: string;
    tags: string[];
}

/** Get blog posts (paginated, filterable) */
export const getBlogPosts = (language = "en", category?: string, page = 1, perPage = 10) => {
    const params = new URLSearchParams({ language, page: String(page), per_page: String(perPage) });
    if (category) params.set("category", category);
    return apiFetch<{ posts: BlogPostItem[]; total: number; page: number; per_page: number; total_pages: number }>(
        `/blog/posts?${params}`,
    );
};

/** Get a single blog post by slug */
export const getBlogPost = (slug: string, language = "en") =>
    apiFetch<{ post: BlogPostItem }>(`/blog/posts/${slug}?language=${language}`);

/** Get blog categories */
export const getBlogCategories = () =>
    apiFetch<{ categories: { id: string; icon: string }[] }>("/blog/categories");

/** Get featured blog posts */
export const getBlogFeatured = (language = "en", limit = 3) =>
    apiFetch<{ posts: BlogPostItem[] }>(`/blog/featured?language=${language}&limit=${limit}`);

// ──────────────────────────────────────────────────
// Meshy Visualization
// ──────────────────────────────────────────────────

export interface VizQuestion {
    id: string;
    question_en: string;
    question_tr: string;
    question_ru: string;
    type: string;
    options: string;
}

export interface VizQuestionsResponse {
    category: string;
    questions: VizQuestion[];
}

export interface VizStartResponse {
    viz_id: string;
    meshy_task_id: string;
    status: string;
    message: string;
}

export interface VizStatusResponse {
    viz_id: string;
    status: string;
    output_image_url: string | null;
    procedure_category: string;
}

export interface VizPostOpResponse {
    viz_id: string;
    similarity_score: number;
    message: string;
}

/** Get visualization questions for a procedure category */
export const getVisualizationQuestions = (category: string) =>
    apiFetch<VizQuestionsResponse>("/meshy/questions", {
        method: "POST",
        body: JSON.stringify({ category }),
    });

/** Start a new visualization job */
export const startVisualization = (image_base64: string, procedure_category: string, answers: Record<string, string>) =>
    apiFetch<VizStartResponse>("/meshy/visualize", {
        method: "POST",
        body: JSON.stringify({ image_base64, procedure_category, answers }),
    });

/** Check visualization status */
export const checkVisualizationStatus = (vizId: string) =>
    apiFetch<VizStatusResponse>(`/meshy/status/${vizId}`);

/** Submit post-op photo for comparison */
export const submitPostOpPhoto = (vizId: string, image_base64: string) =>
    apiFetch<VizPostOpResponse>("/meshy/post-op", {
        method: "POST",
        body: JSON.stringify({ viz_id: vizId, image_base64 }),
    });
