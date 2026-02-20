"""
AntiGravity Ventures — Marketing: SEO Engine
Keyword analizi, meta tag uretimi, icerik skorlama ve sitemap destegi.
"""
from __future__ import annotations

import re
from typing import Any


# ---------------------------------------------------------------------------
# Medikal turizm keyword havuzu (9 prosedur x 5 dil)
# ---------------------------------------------------------------------------
MEDICAL_KEYWORDS: dict[str, dict[str, list[str]]] = {
    "hair_transplant": {
        "tr": ["sac ekimi istanbul fiyat", "sac ekimi turkiye", "fue sac ekimi", "dhi sac ekimi", "sac ekimi sonuclari"],
        "ru": ["пересадка волос турция цена", "трансплантация волос стамбул", "fue пересадка", "dhi пересадка волос", "пересадка волос отзывы"],
        "en": ["hair transplant turkey cost", "hair transplant istanbul", "fue hair transplant", "dhi hair transplant", "best hair transplant clinic turkey"],
        "ar": ["زراعة الشعر تركيا", "تكلفة زراعة الشعر", "زراعة الشعر في اسطنبول", "أفضل مركز زراعة شعر", "زراعة الشعر بتقنية fue"],
        "th": ["ปลูกผมตุรกี", "ปลูกผมราคา", "ปลูกผมอิสตันบูล", "fue ปลูกผม", "ปลูกผมต่างประเทศ"],
    },
    "dental": {
        "tr": ["dis implant turkiye", "dis tedavisi istanbul", "zirkonyum dis kaplama", "dis beyazlatma", "hollywood smile turkiye"],
        "ru": ["стоматология турция цена", "имплантация зубов стамбул", "виниры турция", "голливудская улыбка турция", "лечение зубов турция"],
        "en": ["dental implants turkey", "dental treatment istanbul cost", "hollywood smile turkey", "veneers turkey price", "best dental clinic turkey"],
        "ar": ["زراعة الأسنان تركيا", "تكلفة علاج الأسنان", "ابتسامة هوليوود تركيا", "فينير تركيا", "أفضل عيادة أسنان"],
        "th": ["ทำฟันตุรกี", "รากฟันเทียมตุรกี", "วีเนียร์ตุรกี", "ฟอกสีฟันตุรกี", "ฮอลลีวูดสไมล์"],
    },
    "aesthetic": {
        "tr": ["estetik cerrahi turkiye", "rinoplasti istanbul fiyat", "yuz germe turkiye", "liposuction istanbul", "gogus estetigi"],
        "ru": ["пластическая хирургия турция", "ринопластика стамбул цена", "подтяжка лица турция", "липосакция стамбул", "маммопластика турция"],
        "en": ["plastic surgery turkey cost", "rhinoplasty istanbul price", "facelift turkey", "liposuction istanbul", "breast augmentation turkey"],
        "ar": ["جراحة تجميل تركيا", "عملية الأنف تركيا", "شفط الدهون اسطنبول", "تجميل الثدي تركيا", "شد الوجه تركيا"],
        "th": ["ศัลยกรรมตุรกี", "เสริมจมูกตุรกี", "ดูดไขมันตุรกี", "เสริมหน้าอกตุรกี", "ศัลยกรรมความงาม"],
    },
    "bariatric": {
        "tr": ["obezite cerrahisi turkiye", "gastrik sleeve istanbul", "mide kucultme fiyat", "tup mide ameliyati", "gastrik bypass turkiye"],
        "ru": ["бариатрическая хирургия турция", "рукавная гастрэктомия стамбул", "уменьшение желудка цена", "шунтирование желудка турция", "похудение операция турция"],
        "en": ["bariatric surgery turkey cost", "gastric sleeve istanbul", "weight loss surgery turkey", "gastric bypass turkey price", "obesity surgery turkey"],
        "ar": ["جراحة السمنة تركيا", "تكميم المعدة تركيا", "عملية تحويل المسار", "جراحة إنقاص الوزن", "أفضل جراح سمنة"],
        "th": ["ผ่าตัดลดน้ำหนักตุรกี", "ผ่าตัดกระเพาะตุรกี", "สลีฟตุรกี", "บายพาสตุรกี", "ลดน้ำหนักศัลยกรรม"],
    },
    "ivf": {
        "tr": ["tup bebek turkiye fiyat", "ivf tedavisi istanbul", "tup bebek merkezi", "yumurta dondurma", "ivf basari orani"],
        "ru": ["эко турция цена", "эко стамбул клиника", "искусственное оплодотворение турция", "заморозка яйцеклеток", "лучшая клиника эко"],
        "en": ["ivf turkey cost", "ivf treatment istanbul", "fertility clinic turkey", "egg freezing turkey", "ivf success rates turkey"],
        "ar": ["أطفال الأنابيب تركيا", "تكلفة التلقيح الصناعي", "علاج العقم تركيا", "تجميد البويضات تركيا", "أفضل مركز إخصاب"],
        "th": ["ทำเด็กหลอดแก้วตุรกี", "ivf ตุรกี", "รักษาภาวะมีบุตรยาก", "แช่แข็งไข่ตุรกี", "คลินิกเจริญพันธุ์"],
    },
    "ophthalmology": {
        "tr": ["goz ameliyati turkiye", "lasik istanbul fiyat", "katarakt ameliyati", "goz lazer tedavisi", "lens implantasyonu"],
        "ru": ["офтальмология турция", "лазерная коррекция стамбул", "операция на глаза турция", "ласик цена турция", "катаракта операция"],
        "en": ["eye surgery turkey cost", "lasik istanbul price", "cataract surgery turkey", "eye laser treatment", "lens implant turkey"],
        "ar": ["جراحة العيون تركيا", "عملية الليزك تركيا", "عملية الساد تركيا", "تصحيح النظر بالليزر", "زراعة العدسات"],
        "th": ["ผ่าตัดตาตุรกี", "เลสิคตุรกี", "ต้อกระจกตุรกี", "เลเซอร์ตาตุรกี", "เปลี่ยนเลนส์ตา"],
    },
    "checkup": {
        "tr": ["check-up turkiye", "genel saglik kontrolu istanbul", "executive check-up", "kanser taramasi turkiye", "kapsamli saglik kontrolu"],
        "ru": ["чекап турция", "медицинский осмотр стамбул", "полное обследование турция", "скрининг рака турция", "диагностика стамбул"],
        "en": ["health checkup turkey", "medical screening istanbul", "executive checkup turkey", "cancer screening turkey", "full body checkup cost"],
        "ar": ["فحص شامل تركيا", "فحص طبي اسطنبول", "فحص السرطان تركيا", "تشخيص طبي شامل", "فحص تنفيذي تركيا"],
        "th": ["ตรวจสุขภาพตุรกี", "ตรวจร่างกายอิสตันบูล", "แพ็คเกจตรวจสุขภาพ", "ตรวจมะเร็งตุรกี", "ตรวจสุขภาพต่างประเทศ"],
    },
    "dermatology": {
        "tr": ["dermatoloji turkiye", "cilt tedavisi istanbul", "akne tedavisi", "lazer epilasyon", "cilt genclestime"],
        "ru": ["дерматология турция", "лечение кожи стамбул", "лечение акне турция", "лазерная эпиляция", "омоложение кожи"],
        "en": ["dermatology turkey", "skin treatment istanbul", "acne treatment turkey", "laser hair removal turkey", "skin rejuvenation"],
        "ar": ["علاج البشرة تركيا", "أمراض جلدية اسطنبول", "علاج حب الشباب", "إزالة الشعر بالليزر", "تجديد البشرة"],
        "th": ["รักษาผิวตุรกี", "ผิวหนังตุรกี", "รักษาสิวตุรกี", "เลเซอร์กำจัดขน", "เยาว์วัยผิว"],
    },
    "oncology": {
        "tr": ["onkoloji turkiye", "kanser tedavisi istanbul", "kemoterapi turkiye", "radyoterapi merkezi", "ikinci gorus onkoloji"],
        "ru": ["онкология турция", "лечение рака стамбул", "химиотерапия турция", "лучевая терапия", "второе мнение онколог"],
        "en": ["oncology turkey", "cancer treatment istanbul", "chemotherapy turkey cost", "radiation therapy turkey", "second opinion oncology"],
        "ar": ["علاج السرطان تركيا", "أورام اسطنبول", "العلاج الكيميائي تركيا", "العلاج الإشعاعي", "رأي ثاني أورام"],
        "th": ["รักษามะเร็งตุรกี", "เคมีบำบัดตุรกี", "รังสีรักษาตุรกี", "มะเร็งอิสตันบูล", "ขอความเห็นที่สอง"],
    },
}

# Keyword difficulty & volume estimates per procedure
KEYWORD_METRICS: dict[str, dict[str, Any]] = {
    "hair_transplant":  {"avg_volume": "high",   "difficulty": "medium", "avg_cpc": 1.20},
    "dental":           {"avg_volume": "high",   "difficulty": "medium", "avg_cpc": 0.95},
    "aesthetic":        {"avg_volume": "high",   "difficulty": "high",   "avg_cpc": 1.80},
    "bariatric":        {"avg_volume": "medium", "difficulty": "medium", "avg_cpc": 1.50},
    "ivf":              {"avg_volume": "medium", "difficulty": "high",   "avg_cpc": 2.10},
    "ophthalmology":    {"avg_volume": "medium", "difficulty": "low",    "avg_cpc": 0.80},
    "checkup":          {"avg_volume": "low",    "difficulty": "low",    "avg_cpc": 0.45},
    "dermatology":      {"avg_volume": "medium", "difficulty": "low",    "avg_cpc": 0.65},
    "oncology":         {"avg_volume": "low",    "difficulty": "high",   "avg_cpc": 2.50},
}

VOLUME_MAP = {"high": "10K-50K/mo", "medium": "1K-10K/mo", "low": "100-1K/mo"}
DIFFICULTY_MAP = {"high": "hard", "medium": "moderate", "low": "easy"}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_keywords(procedure: str, region: str, lang: str) -> dict[str, Any]:
    """Keyword analizi: liste + hacim tahmini + zorluk skoru."""
    proc_key = procedure.lower().replace(" ", "_").replace("-", "_")
    proc_data = MEDICAL_KEYWORDS.get(proc_key, {})
    kw_list = proc_data.get(lang, proc_data.get("en", []))
    metrics = KEYWORD_METRICS.get(proc_key, {"avg_volume": "low", "difficulty": "medium", "avg_cpc": 1.0})

    keywords = []
    for kw in kw_list:
        keywords.append({
            "keyword": kw,
            "search_volume_estimate": VOLUME_MAP.get(metrics["avg_volume"], "unknown"),
            "difficulty": DIFFICULTY_MAP.get(metrics["difficulty"], "moderate"),
            "cpc_estimate": metrics["avg_cpc"],
        })

    return {
        "procedure": proc_key,
        "region": region,
        "lang": lang,
        "keywords": keywords,
        "total_keywords": len(keywords),
    }


def generate_meta_tags(title: str, description: str, keywords: list[str], lang: str) -> dict[str, str]:
    """SEO meta tag seti uretir (title, description, OG tags)."""
    title_tag = title[:60] if len(title) > 60 else title
    meta_desc = description[:160] if len(description) > 160 else description
    kw_str = ", ".join(keywords[:10])

    return {
        "title_tag": title_tag,
        "meta_description": meta_desc,
        "meta_keywords": kw_str,
        "og_title": title_tag,
        "og_description": meta_desc,
        "og_type": "website",
        "og_locale": _lang_to_locale(lang),
        "twitter_card": "summary_large_image",
        "twitter_title": title_tag,
        "twitter_description": meta_desc,
    }


def score_content(text: str, target_keywords: list[str]) -> dict[str, Any]:
    """Metnin SEO skorunu hesaplar (0-100)."""
    if not text or not target_keywords:
        return {"seo_score": 0, "suggestions": ["Metin ve hedef keyword listesi gerekli."]}

    text_lower = text.lower()
    word_count = len(text.split())
    suggestions = []
    score = 50  # base

    # Keyword density check
    found = 0
    for kw in target_keywords:
        if kw.lower() in text_lower:
            found += 1
    keyword_ratio = found / max(len(target_keywords), 1)
    score += int(keyword_ratio * 20)

    if keyword_ratio < 0.3:
        suggestions.append("Hedef keyword'lerin cogu icerik icinde kullanilmamis. Daha fazla keyword entegre edin.")

    # Length check
    if word_count < 300:
        suggestions.append("Icerik 300 kelimeden kisa. SEO icin en az 800+ kelime onerilir.")
        score -= 10
    elif word_count >= 800:
        score += 10
    elif word_count >= 1500:
        score += 15

    # Heading check (basic)
    if "##" in text or "<h2" in text.lower():
        score += 5
    else:
        suggestions.append("Alt basliklar (H2/H3) ekleyin — yapisi daha iyi SEO skoru saglar.")

    # CTA check
    cta_patterns = ["contact", "book", "iletisim", "randevu", "связаться", "записаться", "احجز", "จอง"]
    if any(p in text_lower for p in cta_patterns):
        score += 5
    else:
        suggestions.append("Call-to-action (CTA) ekleyin — donusum oranini arttirir.")

    score = max(0, min(100, score))

    return {
        "seo_score": score,
        "word_count": word_count,
        "keywords_found": found,
        "keywords_total": len(target_keywords),
        "keyword_density_percent": round(keyword_ratio * 100, 1),
        "suggestions": suggestions if suggestions else ["Icerik iyi optimize edilmis."],
    }


def generate_sitemap_entry(page_url: str, priority: float = 0.8, changefreq: str = "weekly") -> str:
    """XML sitemap satiri uretir."""
    return (
        f"  <url>\n"
        f"    <loc>{page_url}</loc>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        f"  </url>"
    )


def competitor_keyword_gaps(our_keywords: list[str], competitor_keywords: list[str]) -> dict[str, Any]:
    """Rakip keyword analizi — eksik keyword firsatlarini bulur."""
    our_set = {kw.lower() for kw in our_keywords}
    comp_set = {kw.lower() for kw in competitor_keywords}

    missing = sorted(comp_set - our_set)
    shared = sorted(our_set & comp_set)
    unique = sorted(our_set - comp_set)

    return {
        "missing_opportunities": missing,
        "shared_keywords": shared,
        "our_unique": unique,
        "gap_count": len(missing),
        "overlap_count": len(shared),
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _lang_to_locale(lang: str) -> str:
    return {
        "tr": "tr_TR",
        "ru": "ru_RU",
        "en": "en_US",
        "ar": "ar_AE",
        "th": "th_TH",
    }.get(lang, "en_US")
