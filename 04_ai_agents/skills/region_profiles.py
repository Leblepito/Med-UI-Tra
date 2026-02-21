"""
AntiGravity ThaiTurk — Region Profiles & Platform Specs
Adapted from Seo-Ads cultural intelligence layer for medical tourism.
"""
from __future__ import annotations

REGION_PROFILES: dict[str, dict] = {
    "turkey": {
        "code": "tr",
        "tone": "warm, professional, reassuring",
        "style": "direct with empathy, testimonial-driven",
        "preferred_ctas": [
            "Ucretsiz danismanlik alin",
            "Hemen randevu alin",
            "WhatsApp ile iletisime gecin",
        ],
        "taboos": ["aggressive pricing language", "comparing Turkish clinics negatively"],
        "currency": "USD",
        "trust_signals": ["JCI accreditation", "TURSAB membership", "before/after gallery", "real patient reviews"],
        "holidays": ["Ramadan", "Republic Day (Oct 29)", "Victory Day (Aug 30)"],
        "content_preferences": {
            "formality": "medium",
            "humor": "light",
            "visuals": "before/after photos, clinic interiors, city landmarks",
            "social_proof": "patient count, country count, star ratings",
        },
        "seo_keywords": [
            "sac ekimi turkiye", "dis tedavisi istanbul", "rinoplasti fiyatlari",
            "medikal turizm turkiye", "estetik cerrahi antalya",
        ],
    },
    "russia": {
        "code": "ru",
        "tone": "authoritative, factual, trustworthy",
        "style": "data-driven, comparison-focused, detailed pricing",
        "preferred_ctas": [
            "Besplatnaya konsultatsiya",
            "Uznat stoimost",
            "Napisat v WhatsApp",
        ],
        "taboos": ["overly casual tone", "ignoring visa concerns"],
        "currency": "USD",
        "trust_signals": ["JCI certification", "Russian-speaking coordinator", "price comparison tables", "visa assistance mention"],
        "holidays": ["New Year (Jan 1-8)", "Women's Day (Mar 8)", "Victory Day (May 9)"],
        "content_preferences": {
            "formality": "high",
            "humor": "minimal",
            "visuals": "infographics, comparison charts, medical certificates",
            "social_proof": "detailed testimonials with full story, savings percentages",
        },
        "seo_keywords": [
            "peresadka volos turtsiya", "stomatologiya stambul", "rinoplastika tsena",
            "meditsinskiy turizm", "lechenie v turtsii",
        ],
    },
    "uae": {
        "code": "ar",
        "tone": "respectful, luxury-oriented, discreet",
        "style": "premium positioning, privacy emphasis, VIP experience",
        "preferred_ctas": [
            "Istishara majaniya",
            "Tawasal abar WhatsApp",
            "Ihsul ala ard sir",
        ],
        "taboos": ["pork/alcohol imagery", "revealing before/after photos", "Ramadan insensitivity"],
        "currency": "USD",
        "trust_signals": ["VIP packages", "private rooms", "halal options", "Arabic-speaking staff", "luxury hotel partners"],
        "holidays": ["Ramadan", "Eid al-Fitr", "Eid al-Adha", "UAE National Day (Dec 2)"],
        "content_preferences": {
            "formality": "very high",
            "humor": "none",
            "visuals": "luxury interiors, VIP suites, premium branding",
            "social_proof": "celebrity endorsements, premium testimonials",
        },
        "seo_keywords": [
            "زراعة الشعر تركيا", "تجميل الانف اسطنبول", "علاج الاسنان تركيا",
            "سياحة طبية", "عمليات تجميل تركيا",
        ],
    },
    "europe": {
        "code": "en",
        "tone": "professional, evidence-based, transparent",
        "style": "comparison with EU/UK prices, regulatory compliance, outcome data",
        "preferred_ctas": [
            "Get a free quote",
            "Book free consultation",
            "Compare prices now",
        ],
        "taboos": ["medical claims without evidence", "misleading savings percentages"],
        "currency": "EUR",
        "trust_signals": ["JCI accreditation", "EU-equivalent standards", "NHS price comparison", "surgeon credentials"],
        "holidays": ["Christmas", "Easter", "August holidays"],
        "content_preferences": {
            "formality": "medium-high",
            "humor": "subtle",
            "visuals": "clean infographics, surgeon profiles, facility certifications",
            "social_proof": "Trustpilot reviews, verified patient stories, outcome statistics",
        },
        "seo_keywords": [
            "hair transplant turkey cost", "dental treatment istanbul", "rhinoplasty turkey price",
            "medical tourism turkey", "cosmetic surgery abroad",
        ],
    },
    "asia": {
        "code": "zh",
        "tone": "informative, respectful, community-oriented",
        "style": "educational, step-by-step guides, visa info prominent",
        "preferred_ctas": [
            "免费咨询",
            "获取报价",
            "WhatsApp联系我们",
        ],
        "taboos": ["assuming one Asian culture", "ignoring dietary preferences"],
        "currency": "USD",
        "trust_signals": ["international accreditation", "multilingual staff", "travel assistance", "post-op follow-up in region"],
        "holidays": ["Chinese New Year", "Golden Week", "Mid-Autumn Festival"],
        "content_preferences": {
            "formality": "high",
            "humor": "minimal",
            "visuals": "step-by-step process graphics, comparison tables, testimonials with photos",
            "social_proof": "patient numbers, country diversity, detailed reviews",
        },
        "seo_keywords": [
            "土耳其植发", "伊斯坦布尔牙科", "土耳其整形手术",
            "医疗旅游土耳其", "土耳其美容手术费用",
        ],
    },
    "thailand": {
        "code": "th",
        "tone": "friendly, caring, service-oriented",
        "style": "personal touch, coordinator emphasis, convenience focused",
        "preferred_ctas": [
            "ปรึกษาฟรี",
            "ติดต่อผ่าน WhatsApp",
            "ดูราคาเปรียบเทียบ",
        ],
        "taboos": ["disrespecting monarchy", "insensitive Buddhist references"],
        "currency": "THB",
        "trust_signals": ["Phuket follow-up clinic", "Thai-speaking coordinator", "dual-country care model", "airport transfer included"],
        "holidays": ["Songkran (Apr 13-15)", "King's Birthday (Jul 28)", "Loy Krathong"],
        "content_preferences": {
            "formality": "medium",
            "humor": "light, friendly",
            "visuals": "friendly staff photos, clinic interiors, Phuket scenery",
            "social_proof": "Thai patient stories, local partner clinic credentials",
        },
        "seo_keywords": [
            "ปลูกผมตุรกี", "ทำฟันอิสตันบูล", "เสริมจมูกตุรกี",
            "ท่องเที่ยวเชิงการแพทย์", "ศัลยกรรมตุรกีราคา",
        ],
    },
}

PLATFORM_SPECS: dict[str, dict] = {
    "blog": {
        "title_max": 70,
        "meta_description_max": 160,
        "body_min_words": 500,
        "body_max_words": 1500,
        "h2_recommended": 3,
        "image_alt_required": True,
        "internal_links_min": 2,
        "keyword_density_pct": (1.0, 2.5),
    },
    "instagram": {
        "caption_max": 2200,
        "hashtags_max": 30,
        "recommended_hashtags": 15,
        "image_ratio": "1:1 or 4:5",
        "story_duration_sec": 15,
        "cta_style": "soft, link-in-bio",
    },
    "facebook": {
        "post_max": 63206,
        "optimal_length": 250,
        "link_preview": True,
        "image_ratio": "1.91:1",
        "cta_style": "direct link",
    },
    "google_ads": {
        "headline_max": 30,
        "headlines_count": 15,
        "description_max": 90,
        "descriptions_count": 4,
        "display_url_max": 15,
        "cta_style": "action-oriented",
    },
    "twitter": {
        "tweet_max": 280,
        "thread_max": 25,
        "hashtags_recommended": 3,
        "image_ratio": "16:9",
        "cta_style": "concise with link",
    },
    "linkedin": {
        "post_max": 3000,
        "optimal_length": 600,
        "article_max": 120000,
        "hashtags_recommended": 5,
        "cta_style": "professional, industry-focused",
    },
}


def get_region_profile(region: str) -> dict | None:
    """Get profile for a region (case-insensitive)."""
    return REGION_PROFILES.get(region.lower())


def get_platform_spec(platform: str) -> dict | None:
    """Get spec for a platform (case-insensitive)."""
    return PLATFORM_SPECS.get(platform.lower())


def get_region_by_language(lang_code: str) -> dict | None:
    """Look up region profile by language code (tr, ru, en, th, ar, zh)."""
    for profile in REGION_PROFILES.values():
        if profile["code"] == lang_code:
            return profile
    return None
