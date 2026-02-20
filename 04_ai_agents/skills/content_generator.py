"""
AntiGravity Ventures — Marketing: Content Generator
Blog, reklam metni, sosyal medya postu, landing page ve email sablonlari.
"""
from __future__ import annotations

from typing import Any


# ---------------------------------------------------------------------------
# Platform format limitleri
# ---------------------------------------------------------------------------
PLATFORM_LIMITS: dict[str, dict[str, int]] = {
    "google_ads":    {"headline": 30, "description": 90, "headlines_count": 15},
    "meta_ads":      {"primary_text": 125, "headline": 40, "description": 30},
    "yandex_direct": {"title": 56, "text": 81, "sitelinks": 4},
    "vk_ads":        {"title": 33, "description": 70},
    "instagram":     {"caption": 2200, "hashtags": 30},
    "line":          {"message": 500},
}

# ---------------------------------------------------------------------------
# Procedure display names per language
# ---------------------------------------------------------------------------
PROCEDURE_NAMES: dict[str, dict[str, str]] = {
    "hair_transplant": {
        "tr": "Sac Ekimi", "en": "Hair Transplant", "ru": "Пересадка волос",
        "ar": "زراعة الشعر", "th": "ปลูกผม",
    },
    "dental": {
        "tr": "Dis Tedavisi", "en": "Dental Treatment", "ru": "Стоматология",
        "ar": "علاج الأسنان", "th": "ทันตกรรม",
    },
    "aesthetic": {
        "tr": "Estetik Cerrahi", "en": "Plastic Surgery", "ru": "Пластическая хирургия",
        "ar": "جراحة تجميل", "th": "ศัลยกรรมความงาม",
    },
    "bariatric": {
        "tr": "Obezite Cerrahisi", "en": "Bariatric Surgery", "ru": "Бариатрическая хирургия",
        "ar": "جراحة السمنة", "th": "ผ่าตัดลดน้ำหนัก",
    },
    "ivf": {
        "tr": "Tup Bebek", "en": "IVF Treatment", "ru": "ЭКО",
        "ar": "أطفال الأنابيب", "th": "เด็กหลอดแก้ว",
    },
    "ophthalmology": {
        "tr": "Goz Ameliyati", "en": "Eye Surgery", "ru": "Офтальмология",
        "ar": "جراحة العيون", "th": "ผ่าตัดตา",
    },
    "checkup": {
        "tr": "Check-up", "en": "Health Checkup", "ru": "Чекап",
        "ar": "فحص شامل", "th": "ตรวจสุขภาพ",
    },
    "dermatology": {
        "tr": "Dermatoloji", "en": "Dermatology", "ru": "Дерматология",
        "ar": "أمراض جلدية", "th": "ผิวหนัง",
    },
    "oncology": {
        "tr": "Onkoloji", "en": "Oncology", "ru": "Онкология",
        "ar": "علاج الأورام", "th": "มะเร็งวิทยา",
    },
}

# Region display names
REGION_NAMES: dict[str, dict[str, str]] = {
    "turkey": {"tr": "Turkiye", "en": "Turkey", "ru": "Турция", "ar": "تركيا", "th": "ตุรกี"},
    "russia": {"tr": "Rusya", "en": "Russia", "ru": "Россия", "ar": "روسيا", "th": "รัสเซีย"},
    "uae":    {"tr": "BAE", "en": "UAE", "ru": "ОАЭ", "ar": "الإمارات", "th": "สหรัฐอาหรับเอมิเรตส์"},
    "europe": {"tr": "Avrupa", "en": "Europe", "ru": "Европа", "ar": "أوروبا", "th": "ยุโรป"},
    "asia":   {"tr": "Asya", "en": "Asia", "ru": "Азия", "ar": "آسيا", "th": "เอเชีย"},
}

# Tone templates
TONE_CTA: dict[str, dict[str, str]] = {
    "professional": {
        "tr": "Ucretsiz konsultasyon icin hemen iletisime gecin.",
        "en": "Contact us today for a free consultation.",
        "ru": "Свяжитесь с нами для бесплатной консультации.",
        "ar": "تواصل معنا اليوم للحصول على استشارة مجانية.",
        "th": "ติดต่อเราวันนี้เพื่อรับคำปรึกษาฟรี",
    },
    "casual": {
        "tr": "Merak ettiginiz her seyi sorun — size yardimci olalim!",
        "en": "Got questions? We're here to help!",
        "ru": "Есть вопросы? Мы здесь, чтобы помочь!",
        "ar": "هل لديك أسئلة؟ نحن هنا للمساعدة!",
        "th": "มีคำถามไหม? เราพร้อมช่วยเหลือ!",
    },
    "urgent": {
        "tr": "Sinirli kontenjan — hemen yerinizi ayirtin!",
        "en": "Limited slots available — book now!",
        "ru": "Ограниченное количество мест — бронируйте сейчас!",
        "ar": "أماكن محدودة — احجز الآن!",
        "th": "จำนวนจำกัด — จองเลย!",
    },
    "luxury": {
        "tr": "Premium saglik deneyiminizi baslatmak icin ozel danismaninizla gorusun.",
        "en": "Begin your premium healthcare journey with a personal advisor.",
        "ru": "Начните ваш путь к здоровью с персональным консультантом.",
        "ar": "ابدأ رحلتك الصحية الفاخرة مع مستشارك الشخصي.",
        "th": "เริ่มต้นการดูแลสุขภาพระดับพรีเมียมกับที่ปรึกษาส่วนตัว",
    },
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_blog_post(procedure: str, region: str, lang: str, tone: str = "professional") -> dict[str, Any]:
    """Blog yazisi uretir: baslik + govde + meta + CTA."""
    proc_key = procedure.lower().replace(" ", "_").replace("-", "_")
    proc_name = PROCEDURE_NAMES.get(proc_key, {}).get(lang, procedure.title())
    region_name = REGION_NAMES.get(region, {}).get(lang, region.title())
    cta = TONE_CTA.get(tone, TONE_CTA["professional"]).get(lang, TONE_CTA["professional"]["en"])

    templates = {
        "en": {
            "title": f"{proc_name} in {region_name}: Complete Guide & Costs 2026",
            "body": (
                f"## Why Choose {region_name} for {proc_name}?\n\n"
                f"{region_name} has become one of the top destinations for {proc_name.lower()}, "
                f"offering world-class medical facilities at competitive prices. Thousands of "
                f"international patients travel here each year for high-quality procedures.\n\n"
                f"## What to Expect\n\n"
                f"The {proc_name.lower()} process typically includes an initial consultation, "
                f"pre-operative assessments, the procedure itself, and follow-up care. Most clinics "
                f"offer all-inclusive packages covering accommodation and transfers.\n\n"
                f"## Cost Comparison\n\n"
                f"Patients can save 50-70% compared to prices in Western Europe or the US, "
                f"without compromising on quality. All partner hospitals are JCI-accredited.\n\n"
                f"## How to Get Started\n\n{cta}"
            ),
        },
        "tr": {
            "title": f"{region_name}'de {proc_name}: 2026 Rehberi ve Fiyatlari",
            "body": (
                f"## Neden {region_name}'de {proc_name}?\n\n"
                f"{region_name}, {proc_name.lower()} icin dunyanin en populer destinasyonlarindan biridir. "
                f"Her yil binlerce uluslararasi hasta kaliteli tedavi icin buraya gelmektedir.\n\n"
                f"## Surec Nasil Isler?\n\n"
                f"Ilk konsultasyon, ameliyat oncesi tetkikler, islem ve takip bakimi "
                f"standart surecin parcasidir. Kliniklerin cogu konaklama ve transferi "
                f"iceren paket fiyatlar sunmaktadir.\n\n"
                f"## Fiyat Karsilastirmasi\n\n"
                f"Bati Avrupa veya ABD fiyatlarina kiyasla %50-70 tasarruf saglanabilir. "
                f"Tum partner hastaneler JCI akreditasyonuna sahiptir.\n\n"
                f"## Nasil Baslayabilirsiniz?\n\n{cta}"
            ),
        },
        "ru": {
            "title": f"{proc_name} в {_ru_locative(region_name)}: Полное руководство 2026",
            "body": (
                f"## Почему {region_name} для {proc_name.lower()}?\n\n"
                f"{region_name} стала одним из лучших направлений для {proc_name.lower()}. "
                f"Тысячи пациентов ежегодно приезжают сюда за качественными процедурами.\n\n"
                f"## Чего ожидать\n\n"
                f"Процесс включает первичную консультацию, предоперационные обследования, "
                f"саму процедуру и последующее наблюдение.\n\n"
                f"## Сравнение цен\n\n"
                f"Экономия составляет 50-70% по сравнению с ценами в Западной Европе. "
                f"Все партнёрские клиники имеют аккредитацию JCI.\n\n"
                f"## Как начать?\n\n{cta}"
            ),
        },
        "ar": {
            "title": f"{proc_name} في {region_name}: الدليل الشامل 2026",
            "body": (
                f"## لماذا {region_name} لـ{proc_name}؟\n\n"
                f"أصبحت {region_name} من أفضل الوجهات لـ{proc_name}. "
                f"يسافر آلاف المرضى سنوياً للحصول على إجراءات عالية الجودة.\n\n"
                f"## ماذا تتوقع\n\n"
                f"تشمل العملية الاستشارة الأولية والفحوصات والإجراء والمتابعة.\n\n"
                f"## مقارنة الأسعار\n\n"
                f"يمكن توفير 50-70% مقارنة بأسعار أوروبا الغربية.\n\n"
                f"## كيف تبدأ؟\n\n{cta}"
            ),
        },
        "th": {
            "title": f"{proc_name}ใน{region_name}: คู่มือฉบับสมบูรณ์ 2026",
            "body": (
                f"## ทำไมต้อง{region_name}สำหรับ{proc_name}?\n\n"
                f"{region_name}กลายเป็นจุดหมายปลายทางชั้นนำสำหรับ{proc_name} "
                f"ผู้ป่วยนานาชาติหลายพันคนเดินทางมาทุกปี\n\n"
                f"## สิ่งที่คาดหวังได้\n\n"
                f"กระบวนการรวมถึงการปรึกษาเบื้องต้น การตรวจก่อนผ่าตัด หัตถการ และการติดตามผล\n\n"
                f"## เปรียบเทียบราคา\n\n"
                f"ประหยัดได้ 50-70% เมื่อเทียบกับยุโรปตะวันตก\n\n"
                f"## เริ่มต้นอย่างไร?\n\n{cta}"
            ),
        },
    }

    t = templates.get(lang, templates["en"])
    return {
        "content_type": "blog",
        "title": t["title"],
        "body": t["body"],
        "meta": {
            "description": t["title"],
            "keywords": f"{proc_name}, {region_name}, medical tourism, 2026",
        },
        "cta": cta,
        "lang": lang,
        "region": region,
    }


def generate_ad_copy(procedure: str, platform: str, region: str, lang: str) -> dict[str, Any]:
    """Reklam metni uretir — platform format limitlerini uygular."""
    proc_key = procedure.lower().replace(" ", "_").replace("-", "_")
    proc_name = PROCEDURE_NAMES.get(proc_key, {}).get(lang, procedure.title())
    region_name = REGION_NAMES.get(region, {}).get(lang, region.title())

    # Base copy
    headlines = {
        "en": [f"{proc_name} in {region_name}", "Save 50-70%", "JCI Accredited", "Free Consultation"],
        "tr": [f"{region_name}'de {proc_name}", "%50-70 Tasarruf", "JCI Akredite", "Ucretsiz Danismanlik"],
        "ru": [f"{proc_name} в {_ru_locative(region_name)}", "Экономия 50-70%", "Аккредитация JCI", "Бесплатная консультация"],
        "ar": [f"{proc_name} في {region_name}", "وفّر 50-70%", "معتمدة JCI", "استشارة مجانية"],
        "th": [f"{proc_name}ที่{region_name}", "ประหยัด 50-70%", "JCI รับรอง", "ปรึกษาฟรี"],
    }
    descriptions = {
        "en": f"World-class {proc_name.lower()} at affordable prices. All-inclusive packages with accommodation and transfers.",
        "tr": f"Dunya standartlarinda {proc_name.lower()} uygun fiyatlarla. Konaklama ve transfer dahil paketler.",
        "ru": f"Мировой уровень {proc_name.lower()} по доступным ценам. Пакеты всё включено.",
        "ar": f"{proc_name} بمستوى عالمي وأسعار معقولة. باقات شاملة مع الإقامة والنقل.",
        "th": f"{proc_name}ระดับโลกในราคาที่เข้าถึงได้ แพ็คเกจรวมที่พักและรถรับส่ง",
    }

    h = headlines.get(lang, headlines["en"])
    d = descriptions.get(lang, descriptions["en"])

    # Apply platform limits
    plat_key = _normalize_platform_key(platform)
    limits = PLATFORM_LIMITS.get(plat_key, {})

    formatted = {"platform": platform}
    if plat_key == "google_ads":
        formatted["headlines"] = [hl[:limits.get("headline", 30)] for hl in h]
        formatted["description"] = d[:limits.get("description", 90)]
    elif plat_key == "meta_ads":
        formatted["primary_text"] = d[:limits.get("primary_text", 125)]
        formatted["headline"] = h[0][:limits.get("headline", 40)]
    elif plat_key == "yandex_direct":
        formatted["title"] = h[0][:limits.get("title", 56)]
        formatted["text"] = d[:limits.get("text", 81)]
    elif plat_key == "vk_ads":
        formatted["title"] = h[0][:limits.get("title", 33)]
        formatted["description"] = d[:limits.get("description", 70)]
    else:
        formatted["headline"] = h[0]
        formatted["description"] = d

    return {
        "content_type": "ad_copy",
        "title": h[0],
        "body": d,
        "cta": TONE_CTA["urgent"].get(lang, "Book now!"),
        "platform_formatted": formatted,
        "lang": lang,
        "region": region,
    }


def generate_social_post(procedure: str, platform: str, region: str, lang: str) -> dict[str, Any]:
    """Sosyal medya postu uretir — hashtag ve emoji ile."""
    proc_key = procedure.lower().replace(" ", "_").replace("-", "_")
    proc_name = PROCEDURE_NAMES.get(proc_key, {}).get(lang, procedure.title())
    region_name = REGION_NAMES.get(region, {}).get(lang, region.title())

    hashtags_map = {
        "en": [f"#{proc_key}", "#MedicalTourism", f"#{region.title()}Healthcare", "#AntiGravity", "#HealthTravel"],
        "tr": [f"#{proc_key}", "#SaglikTurizmi", "#TurkiyeTedavi", "#AntiGravity", "#SaglikSeyahati"],
        "ru": [f"#{proc_key}", "#МедицинскийТуризм", "#ЛечениеЗаГраницей", "#AntiGravity", "#Здоровье"],
    }

    captions = {
        "en": f"Transform your life with {proc_name.lower()} in {region_name}! World-class care, incredible savings. Your journey starts here.",
        "tr": f"{region_name}'de {proc_name.lower()} ile hayatinizi degistirin! Dunya standartlarinda bakim, inanilmaz tasarruf.",
        "ru": f"Измените свою жизнь с {proc_name.lower()} в {_ru_locative(region_name)}! Мировой уровень, невероятная экономия.",
        "ar": f"غيّر حياتك مع {proc_name} في {region_name}! رعاية عالمية وتوفير مذهل.",
        "th": f"เปลี่ยนชีวิตด้วย{proc_name}ที่{region_name}! การดูแลระดับโลก ประหยัดอย่างน่าทึ่ง",
    }

    caption = captions.get(lang, captions["en"])
    hashtags = hashtags_map.get(lang, hashtags_map["en"])

    return {
        "content_type": "social",
        "title": f"{proc_name} — {region_name}",
        "body": caption,
        "cta": TONE_CTA["casual"].get(lang, "DM us!"),
        "platform_formatted": {
            "platform": platform,
            "caption": caption,
            "hashtags": hashtags,
        },
        "lang": lang,
        "region": region,
    }


def generate_landing_page_copy(procedure: str, region: str, lang: str) -> dict[str, Any]:
    """Landing page icerigi uretir: hero + benefits + testimonial + CTA."""
    proc_key = procedure.lower().replace(" ", "_").replace("-", "_")
    proc_name = PROCEDURE_NAMES.get(proc_key, {}).get(lang, procedure.title())
    region_name = REGION_NAMES.get(region, {}).get(lang, region.title())

    lp = {
        "en": {
            "hero": f"Premium {proc_name} in {region_name} — Save Up to 70%",
            "benefits": [
                "JCI-accredited partner hospitals",
                "All-inclusive packages (flight, hotel, transfers)",
                "Multilingual patient coordinators",
                "Post-procedure follow-up care",
                "Transparent pricing — no hidden fees",
            ],
            "testimonial_template": '"I had my {procedure} in {region} and saved thousands. The care was exceptional!" — Patient',
        },
        "tr": {
            "hero": f"{region_name}'de Premium {proc_name} — %70'e Kadar Tasarruf",
            "benefits": [
                "JCI akrediteli partner hastaneler",
                "Her sey dahil paketler (ucus, otel, transfer)",
                "Cok dilli hasta koordinatorleri",
                "Islem sonrasi takip bakimi",
                "Seffaf fiyatlandirma — gizli ucret yok",
            ],
            "testimonial_template": '"{procedure} icin {region}\'a geldim ve binlerce dolar tasarruf ettim. Bakim muhtesamdi!" — Hasta',
        },
        "ru": {
            "hero": f"Премиум {proc_name} в {_ru_locative(region_name)} — Экономия до 70%",
            "benefits": [
                "Партнёрские клиники с аккредитацией JCI",
                "Пакеты всё включено (перелёт, отель, трансфер)",
                "Многоязычные координаторы",
                "Послеоперационное наблюдение",
                "Прозрачные цены — без скрытых платежей",
            ],
            "testimonial_template": '"Я прошёл {procedure} в {region} и сэкономил тысячи. Обслуживание было отличным!" — Пациент',
        },
    }

    template = lp.get(lang, lp["en"])
    return {
        "content_type": "landing_page",
        "title": template["hero"],
        "body": "\n".join(f"- {b}" for b in template["benefits"]),
        "meta": {"testimonial_template": template["testimonial_template"]},
        "cta": TONE_CTA["luxury"].get(lang, TONE_CTA["luxury"]["en"]),
        "lang": lang,
        "region": region,
    }


def generate_email_template(campaign_type: str, region: str, lang: str) -> dict[str, Any]:
    """Email sablonu uretir: subject + body + CTA."""
    region_name = REGION_NAMES.get(region, {}).get(lang, region.title())

    subjects = {
        "en": f"Your Health Journey to {region_name} Starts Here",
        "tr": f"{region_name} Saglik Yolculugunuz Basliyor",
        "ru": f"Ваш путь к здоровью в {_ru_locative(region_name)} начинается здесь",
    }
    bodies = {
        "en": (
            f"Dear Patient,\n\n"
            f"Thank you for your interest in medical tourism to {region_name}. "
            f"We offer premium healthcare packages with savings of up to 70%.\n\n"
            f"What's included:\n"
            f"- Free initial consultation\n"
            f"- All-inclusive treatment packages\n"
            f"- Dedicated patient coordinator\n"
            f"- Airport transfers and accommodation\n\n"
            f"Reply to this email or contact us via WhatsApp to get started."
        ),
        "tr": (
            f"Degerli Hasta,\n\n"
            f"{region_name} saglik turizmine gosterdiginiz ilgi icin tesekkurler. "
            f"%70'e kadar tasarruflu premium saglik paketleri sunuyoruz.\n\n"
            f"Paketimize dahil olanlar:\n"
            f"- Ucretsiz ilk konsultasyon\n"
            f"- Her sey dahil tedavi paketleri\n"
            f"- Ozel hasta koordinatoru\n"
            f"- Havalimani transferi ve konaklama\n\n"
            f"Baslamak icin bu e-postaya yanit verin veya WhatsApp'tan bize ulasin."
        ),
        "ru": (
            f"Уважаемый пациент,\n\n"
            f"Благодарим за интерес к медицинскому туризму в {_ru_locative(region_name)}. "
            f"Мы предлагаем премиальные пакеты с экономией до 70%.\n\n"
            f"Что включено:\n"
            f"- Бесплатная первичная консультация\n"
            f"- Пакеты всё включено\n"
            f"- Персональный координатор\n"
            f"- Трансфер и проживание\n\n"
            f"Ответьте на это письмо или свяжитесь через WhatsApp."
        ),
    }

    return {
        "content_type": "email",
        "title": subjects.get(lang, subjects["en"]),
        "body": bodies.get(lang, bodies["en"]),
        "cta": TONE_CTA["professional"].get(lang, TONE_CTA["professional"]["en"]),
        "lang": lang,
        "region": region,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ru_locative(name: str) -> str:
    """Basic Russian locative form helper."""
    if name.endswith("ия"):
        return name[:-2] + "ии"
    if name.endswith("а"):
        return name[:-1] + "е"
    return name + "е" if name and name[-1].isalpha() else name


def _normalize_platform_key(platform: str) -> str:
    """Platform adini PLATFORM_LIMITS key formatina donusturur."""
    mapping = {
        "google": "google_ads",
        "google_ads": "google_ads",
        "meta": "meta_ads",
        "meta_ads": "meta_ads",
        "facebook": "meta_ads",
        "yandex": "yandex_direct",
        "yandex_direct": "yandex_direct",
        "vk": "vk_ads",
        "vk_ads": "vk_ads",
        "instagram": "instagram",
        "line": "line",
    }
    return mapping.get(platform.lower(), platform.lower())
