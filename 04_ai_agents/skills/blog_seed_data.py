"""
AntiGravity ThaiTurk — Blog Seed Data
10 blog posts x 6 languages for the medical tourism blog.
"""
from __future__ import annotations

BLOG_CATEGORIES = [
    {"id": "hair_transplant", "icon": "💆"},
    {"id": "rhinoplasty", "icon": "👃"},
    {"id": "dental", "icon": "🦷"},
    {"id": "ivf", "icon": "🍼"},
    {"id": "eye_surgery", "icon": "👁️"},
    {"id": "bbl", "icon": "🍑"},
    {"id": "breast", "icon": "🎀"},
    {"id": "bariatric", "icon": "⚖️"},
    {"id": "facelift", "icon": "✨"},
    {"id": "medical_tourism_guide", "icon": "🌍"},
]

BLOG_POSTS: list[dict] = [
    {
        "id": "hair-transplant-turkey-guide",
        "category": "hair_transplant",
        "featured": True,
        "author": "Dr. AntiGravity Medical",
        "date": "2026-02-15",
        "read_time": 8,
        "image": "/images/blog/hair-transplant.jpg",
        "tags": ["hair transplant", "FUE", "Turkey", "Istanbul"],
        "translations": {
            "en": {
                "title": "Hair Transplant in Turkey: The Complete 2026 Guide",
                "slug": "hair-transplant-turkey-guide",
                "excerpt": "Turkey performs over 500,000 hair transplants annually. Learn about FUE techniques, costs, top clinics, and what to expect from your journey.",
                "body": """## Why Turkey for Hair Transplant?

Turkey has become the world capital of hair transplantation, performing over 500,000 procedures annually. The combination of world-class surgeons, cutting-edge technology, and prices 60-70% lower than Europe or the US makes it an unbeatable destination.

Istanbul alone has over 350 licensed clinics specializing in hair restoration. The competition drives quality up and prices down, benefiting patients from around the world.

## FUE vs DHI: Which Technique Is Right for You?

**Follicular Unit Extraction (FUE)** is the gold standard. Individual follicles are extracted and implanted one by one, leaving no linear scar. Recovery is fast — most patients return to work within a week.

**Direct Hair Implantation (DHI)** uses a Choi pen for even more precise placement. It's ideal for patients who want maximum density in the hairline area.

Both techniques are available at our [partner hospitals in Turkey](/medical), with surgeons who have performed thousands of successful procedures.

## Cost Comparison

| Location | Average Cost | Grafts Included |
|----------|-------------|-----------------|
| Turkey | $2,000–$4,000 | 3,000–5,000 |
| UK | $8,000–$15,000 | 2,000–3,000 |
| USA | $10,000–$20,000 | 2,000–3,000 |

## What's Included in Your Package

At AntiGravity Medical, your hair transplant package includes:
- **VIP airport transfer** — met at arrivals, private car to hotel
- **4-star hotel** — 3 nights accommodation near the clinic
- **The procedure** — including PRP treatment and medications
- **Translator** — available throughout your stay
- **Post-op care kit** — shampoo, medications, pillow
- **Phuket follow-up** — post-operative check at our partner clinic

## Recovery Timeline

- **Day 1-3**: Mild swelling, rest recommended
- **Day 7**: Scabs fall off naturally
- **Week 2-4**: Transplanted hair sheds (normal!)
- **Month 3-4**: New growth begins
- **Month 8-12**: Full results visible

## Book Your Free Consultation

Ready to start your hair restoration journey? [Get a free consultation](/medical) — our coordinator will contact you via WhatsApp within 5 minutes.""",
            },
            "ru": {
                "title": "Пересадка волос в Турции: Полное руководство 2026",
                "slug": "peresadka-volos-turtsiya",
                "excerpt": "Турция проводит более 500 000 пересадок волос ежегодно. Узнайте о методах FUE, стоимости, лучших клиниках и чего ожидать.",
                "body": """## Почему Турция для пересадки волос?

Турция стала мировой столицей трансплантации волос — более 500 000 процедур ежегодно. Сочетание хирургов мирового класса, передовых технологий и цен на 60-70% ниже, чем в Европе или США, делает её непревзойдённым направлением.

Только в Стамбуле более 350 лицензированных клиник, специализирующихся на восстановлении волос.

## FUE vs DHI: Какая техника подходит вам?

**Экстракция фолликулярных единиц (FUE)** — золотой стандарт. Фолликулы извлекаются и пересаживаются по одному, не оставляя линейного рубца. Восстановление быстрое — большинство пациентов возвращаются к работе в течение недели.

**Прямая имплантация волос (DHI)** использует ручку Choi для ещё более точной посадки. Идеально для максимальной густоты в зоне линии роста.

Обе техники доступны в наших [партнёрских клиниках в Турции](/medical).

## Сравнение цен

| Страна | Средняя цена | Графтов |
|--------|-------------|---------|
| Турция | $2,000–$4,000 | 3,000–5,000 |
| Великобритания | $8,000–$15,000 | 2,000–3,000 |
| США | $10,000–$20,000 | 2,000–3,000 |

## Что включено в пакет

В AntiGravity Medical пакет пересадки волос включает:
- **VIP-трансфер из аэропорта**
- **Отель 4 звезды** — 3 ночи рядом с клиникой
- **Процедура** — включая PRP и медикаменты
- **Переводчик** — на весь период пребывания
- **Набор для ухода** — шампунь, медикаменты, подушка
- **Наблюдение на Пхукете** — контроль в партнёрской клинике

## Запишитесь на бесплатную консультацию

Готовы начать? [Получите бесплатную консультацию](/medical) — координатор свяжется через WhatsApp за 5 минут.""",
            },
            "tr": {
                "title": "Turkiye'de Sac Ekimi: 2026 Komple Rehber",
                "slug": "turkiyede-sac-ekimi-rehberi",
                "excerpt": "Turkiye yillik 500.000'den fazla sac ekimi yapmaktadir. FUE teknikleri, maliyetler, en iyi klinikler ve surecten ne beklemeniz gerektigini ogrenin.",
                "body": """## Neden Sac Ekimi Icin Turkiye?

Turkiye, yillik 500.000'den fazla islemle sac ekiminin dunya baskenti haline gelmistir. Dunya sinifi cerrahlar, son teknoloji ve Avrupa veya ABD'den %60-70 daha dusuk fiyatlarin bilesimi onu rakipsiz bir destinasyon yapar.

Sadece Istanbul'da sac restorasyonunda uzmanlasan 350'den fazla lisansli klinik bulunmaktadir.

## FUE vs DHI: Hangi Teknik Size Uygun?

**Folikuler Unit Ekstraksiyon (FUE)** altin standarttir. Bireysel folikuller tek tek cikarilir ve implante edilir, lineer iz birakmaz. Iyilesme hizlidir — cogu hasta bir hafta icinde ise doner.

**Direkt Sac Implantasyonu (DHI)** daha hassas yerlestirme icin Choi kalemi kullanir. Sac cizgisi bolgesinde maksimum yogunluk isteyenler icin idealdir.

Her iki teknik de [Turkiye'deki partner hastanelerimizde](/medical) mevcuttur.

## Fiyat Karsilastirmasi

| Ulke | Ortalama Maliyet | Greft |
|------|-----------------|-------|
| Turkiye | $2,000–$4,000 | 3,000–5,000 |
| Ingiltere | $8,000–$15,000 | 2,000–3,000 |
| ABD | $10,000–$20,000 | 2,000–3,000 |

## Paketinize Neler Dahil

AntiGravity Medical sac ekimi paketiniz:
- **VIP havaalani transferi**
- **4 yildizli otel** — klinigin yakininda 3 gece konaklama
- **Islem** — PRP tedavisi ve ilaclar dahil
- **Tercuman** — konaklamaniz boyunca
- **Bakim kiti** — sampuan, ilaclar, yastik
- **Phuket'te takip** — partner klinikte ameliyat sonrasi kontrol

## Ucretsiz Danismanlik Alin

Baslamaya hazir misiniz? [Ucretsiz danismanlik alin](/medical) — koordinatorumuz 5 dakika icinde WhatsApp'tan iletisime gececek.""",
            },
            "th": {
                "title": "ปลูกผมที่ตุรกี: คู่มือฉบับสมบูรณ์ 2026",
                "slug": "plook-pom-turkey-guide",
                "excerpt": "ตุรกีทำการปลูกผมมากกว่า 500,000 ครั้งต่อปี เรียนรู้เกี่ยวกับเทคนิค FUE ค่าใช้จ่าย คลินิกชั้นนำ และสิ่งที่คาดหวัง",
                "body": """## ทำไมต้องปลูกผมที่ตุรกี?

ตุรกีกลายเป็นเมืองหลวงของโลกในเรื่องการปลูกผม ด้วยจำนวนมากกว่า 500,000 ครั้งต่อปี การผสมผสานของศัลยแพทย์ระดับโลก เทคโนโลยีล้ำสมัย และราคาที่ถูกกว่ายุโรปหรือสหรัฐ 60-70%

อิสตันบูลมีคลินิกที่ได้รับอนุญาตมากกว่า 350 แห่ง

## FUE vs DHI: เทคนิคไหนเหมาะกับคุณ?

**FUE** เป็นมาตรฐานทองคำ รากผมถูกสกัดและปลูกทีละเส้น ไม่ทิ้งแผลเป็นเส้นตรง ฟื้นตัวเร็ว ผู้ป่วยส่วนใหญ่กลับไปทำงานได้ภายในหนึ่งสัปดาห์

**DHI** ใช้ปากกา Choi สำหรับการวางที่แม่นยำยิ่งขึ้น เหมาะสำหรับความหนาแน่นสูงสุดบริเวณแนวผม

ทั้งสองเทคนิคมีให้บริการที่[โรงพยาบาลพาร์ทเนอร์ในตุรกี](/medical)

## เปรียบเทียบราคา

| ประเทศ | ราคาเฉลี่ย | กราฟท์ |
|--------|-----------|--------|
| ตุรกี | $2,000–$4,000 | 3,000–5,000 |
| อังกฤษ | $8,000–$15,000 | 2,000–3,000 |
| สหรัฐ | $10,000–$20,000 | 2,000–3,000 |

## แพ็คเกจรวมอะไรบ้าง

- **รถรับส่ง VIP จากสนามบิน**
- **โรงแรม 4 ดาว** — 3 คืน
- **การรักษา** — รวม PRP และยา
- **ล่าม** — ตลอดการเข้าพัก
- **ชุดดูแลหลังผ่าตัด**
- **ติดตามผลที่ภูเก็ต**

## จองปรึกษาฟรี

พร้อมเริ่มต้นแล้วหรือยัง? [รับคำปรึกษาฟรี](/medical) — ผู้ประสานงานจะติดต่อผ่าน WhatsApp ภายใน 5 นาที""",
            },
            "ar": {
                "title": "زراعة الشعر في تركيا: الدليل الشامل 2026",
                "slug": "ziraat-shaar-turkiya",
                "excerpt": "تجري تركيا أكثر من 500,000 عملية زراعة شعر سنوياً. تعرف على تقنيات FUE والتكاليف وأفضل العيادات.",
                "body": """## لماذا تركيا لزراعة الشعر؟

أصبحت تركيا عاصمة العالم لزراعة الشعر، بأكثر من 500,000 عملية سنوياً. مزيج من الجراحين العالميين والتكنولوجيا المتقدمة وأسعار أقل بنسبة 60-70% من أوروبا أو أمريكا.

إسطنبول وحدها تضم أكثر من 350 عيادة مرخصة.

## FUE مقابل DHI: أي تقنية تناسبك؟

**استخراج الوحدات البصيلية (FUE)** هو المعيار الذهبي. يتم استخراج البصيلات وزرعها واحدة تلو الأخرى بدون ندبة خطية. التعافي سريع.

**زراعة الشعر المباشرة (DHI)** تستخدم قلم تشوي لزراعة أكثر دقة.

كلا التقنيتين متاحتان في [مستشفياتنا الشريكة في تركيا](/medical).

## مقارنة الأسعار

| الموقع | متوسط التكلفة | البصيلات |
|--------|--------------|----------|
| تركيا | $2,000–$4,000 | 3,000–5,000 |
| بريطانيا | $8,000–$15,000 | 2,000–3,000 |
| أمريكا | $10,000–$20,000 | 2,000–3,000 |

## ماذا يشمل الباقة

- **نقل VIP من المطار**
- **فندق 4 نجوم** — 3 ليالٍ
- **العملية** — شاملة PRP والأدوية
- **مترجم** — طوال إقامتك
- **مجموعة العناية بعد العملية**
- **متابعة في بوكيت**

## احجز استشارتك المجانية

[احصل على استشارة مجانية](/medical) — سيتواصل المنسق عبر واتساب خلال 5 دقائق.""",
            },
            "zh": {
                "title": "土耳其植发：2026年完整指南",
                "slug": "turkey-hair-transplant-guide-zh",
                "excerpt": "土耳其每年进行超过50万例植发手术。了解FUE技术、费用、顶级诊所以及您的旅程。",
                "body": """## 为什么选择土耳其植发？

土耳其已成为全球植发之都，每年进行超过50万例手术。世界级外科医生、尖端技术和比欧美低60-70%的价格完美结合。

仅伊斯坦布尔就有350多家专业植发诊所。

## FUE vs DHI：哪种技术适合您？

**毛囊单位提取（FUE）**是黄金标准。逐个提取和种植毛囊，不留线性疤痕。恢复快速——大多数患者一周内可恢复工作。

**直接植发（DHI）**使用Choi笔进行更精确的种植。

两种技术均可在我们的[土耳其合作医院](/medical)获得。

## 价格对比

| 地点 | 平均费用 | 毛囊数 |
|------|---------|--------|
| 土耳其 | $2,000–$4,000 | 3,000–5,000 |
| 英国 | $8,000–$15,000 | 2,000–3,000 |
| 美国 | $10,000–$20,000 | 2,000–3,000 |

## 套餐包含

- **VIP机场接送**
- **四星级酒店** — 3晚
- **手术** — 包括PRP和药物
- **翻译** — 全程服务
- **术后护理套装**
- **普吉岛随访**

## 预约免费咨询

准备开始了吗？[获取免费咨询](/medical) — 协调员将在5分钟内通过WhatsApp联系您。""",
            },
        },
    },
    {
        "id": "rhinoplasty-istanbul-antalya",
        "category": "rhinoplasty",
        "featured": True,
        "author": "Dr. AntiGravity Medical",
        "date": "2026-02-10",
        "read_time": 7,
        "image": "/images/blog/rhinoplasty.jpg",
        "tags": ["rhinoplasty", "nose job", "Istanbul", "Antalya"],
        "translations": {
            "en": {
                "title": "Rhinoplasty in Turkey: Istanbul vs Antalya Clinics",
                "slug": "rhinoplasty-istanbul-antalya",
                "excerpt": "Comparing top rhinoplasty clinics in Istanbul and Antalya. Costs, surgeon expertise, recovery, and why Turkey leads in nose surgery.",
                "body": """## Turkey: The Rhinoplasty Capital

Turkey performs more rhinoplasty procedures than almost any country in the world. With costs starting from $3,500 — compared to $8,000-$15,000 in Europe — it's no wonder patients travel from 50+ countries.

## Istanbul vs Antalya: Which City?

**Istanbul** offers the largest selection of surgeons and clinics. Major hospitals like Memorial, Acibadem, and Liv Hospital have dedicated rhinoplasty departments.

**Antalya** combines your procedure with a recovery holiday on the Mediterranean coast. Smaller, boutique clinics offer a more personalized experience.

Both cities have JCI-accredited facilities available through our [clinic matching system](/medical).

## What to Expect

- **Consultation**: Virtual or in-person assessment with your surgeon
- **Day of surgery**: 2-3 hour procedure under general anesthesia
- **Day 1-2**: Rest at your hotel with our coordinator checking in
- **Day 7**: Cast removal and final check-up
- **Return home**: Most patients fly home after 7-10 days

## Cost Breakdown

| Item | Turkey | UK |
|------|--------|-----|
| Surgeon fee | $2,500–$4,000 | $5,000–$10,000 |
| Hospital | Included | $2,000–$5,000 |
| Hotel (5 nights) | $300–$600 | N/A |
| Total | $3,500–$5,000 | $8,000–$15,000 |

## Recovery Tips

After your rhinoplasty, you'll want to:
- Sleep elevated for the first 2 weeks
- Avoid strenuous exercise for 4-6 weeks
- Protect your nose from sun exposure
- Attend follow-up appointments (available in [Phuket](/medical))

## Start Your Journey

[Book a free consultation](/medical) and our coordinator will match you with the ideal surgeon for your goals.""",
            },
            "ru": {
                "title": "Ринопластика в Турции: клиники Стамбула и Антальи",
                "slug": "rinoplastika-stambul-antalya",
                "excerpt": "Сравнение лучших клиник ринопластики в Стамбуле и Анталье. Стоимость, опыт хирургов, восстановление.",
                "body": """## Турция — столица ринопластики

Турция проводит больше операций ринопластики, чем почти любая другая страна. Стоимость от $3,500 по сравнению с $8,000-$15,000 в Европе.

## Стамбул vs Анталья

**Стамбул** предлагает самый большой выбор хирургов. Крупные больницы — Memorial, Acibadem, Liv Hospital.

**Анталья** сочетает процедуру с отдыхом на Средиземноморском побережье.

Обе города имеют JCI-аккредитованные клиники в нашей [системе подбора](/medical).

## Чего ожидать

- **Консультация**: виртуальная или очная оценка
- **День операции**: 2-3 часа под общей анестезией
- **День 1-2**: отдых в отеле
- **День 7**: снятие гипса и финальный осмотр
- **Возвращение**: большинство пациентов летят домой через 7-10 дней

## Стоимость

| Пункт | Турция | Великобритания |
|-------|--------|---------------|
| Хирург | $2,500–$4,000 | $5,000–$10,000 |
| Клиника | Включено | $2,000–$5,000 |
| Отель | $300–$600 | — |
| Итого | $3,500–$5,000 | $8,000–$15,000 |

## Начните

[Запишитесь на бесплатную консультацию](/medical) — координатор подберёт идеального хирурга.""",
            },
            "tr": {
                "title": "Turkiye'de Rinoplasti: Istanbul ve Antalya Klinikleri",
                "slug": "turkiyede-rinoplasti",
                "excerpt": "Istanbul ve Antalya'daki en iyi rinoplasti kliniklerinin karsilastirmasi. Maliyet, uzmanlik ve neden Turkiye burun estetiginde lider.",
                "body": """## Turkiye: Rinoplasti Baskenti

Turkiye dunyanin en cok rinoplasti yapilan ulkelerinden biridir. $3,500'dan baslayan fiyatlarla Avrupa'daki $8,000-$15,000'a kiyasla inanilmaz avantaj saglar.

## Istanbul vs Antalya

**Istanbul** en genis cerrah ve klinik secenegini sunar. Memorial, Acibadem, Liv Hospital gibi buyuk hastaneler ozel rinoplasti bolumlere sahiptir.

**Antalya** isleminizi Akdeniz kiyisinda bir tatille birlestirir.

Her iki sehirde de [klinik eslestirme sistemimiz](/medical) uzerinden JCI akrediteli tesisler mevcuttur.

## Surecten Ne Beklenmeli

- **Danismanlik**: Cerrahinizla sanal veya yuz yuze degerlendirme
- **Ameliyat gunu**: Genel anestezi altinda 2-3 saatlik islem
- **1-2. gun**: Otelde dinlenme
- **7. gun**: Alci cikarma ve son kontrol
- **Eve donus**: Cogu hasta 7-10 gun sonra ucar

## Ucretsiz Danismanlik

[Ucretsiz danismanlik alin](/medical) — koordinatorumuz sizin icin ideal cerrahi bulacak.""",
            },
            "th": {
                "title": "เสริมจมูกที่ตุรกี: คลินิกอิสตันบูล vs อันตัลยา",
                "slug": "serm-jamook-turkey",
                "excerpt": "เปรียบเทียบคลินิกเสริมจมูกชั้นนำในอิสตันบูลและอันตัลยา ค่าใช้จ่าย ความเชี่ยวชาญ การฟื้นตัว",
                "body": """## ตุรกี: เมืองหลวงของการเสริมจมูก

ตุรกีทำการเสริมจมูกมากที่สุดในโลก ราคาเริ่มต้นจาก $3,500 เทียบกับ $8,000-$15,000 ในยุโรป

## อิสตันบูล vs อันตัลยา

**อิสตันบูล** มีศัลยแพทย์และคลินิกให้เลือกมากที่สุด

**อันตัลยา** ผสมผสานการรักษากับวันหยุดพักผ่อนริมทะเลเมดิเตอร์เรเนียน

ทั้งสองเมืองมีสถานพยาบาลที่ได้รับการรับรอง JCI ผ่าน[ระบบจับคู่คลินิก](/medical)

## สิ่งที่คาดหวัง

- **ปรึกษา**: ประเมินออนไลน์หรือพบตัว
- **วันผ่าตัด**: 2-3 ชั่วโมงภายใต้การดมยาสลบ
- **วันที่ 7**: ถอดเฝือกและตรวจสุดท้าย
- **กลับบ้าน**: ส่วนใหญ่บินกลับหลัง 7-10 วัน

## จองปรึกษาฟรี

[รับคำปรึกษาฟรี](/medical) — ผู้ประสานงานจะจับคู่ศัลยแพทย์ที่เหมาะกับคุณ""",
            },
            "ar": {
                "title": "تجميل الأنف في تركيا: عيادات إسطنبول مقابل أنطاليا",
                "slug": "tajmeel-anf-turkiya",
                "excerpt": "مقارنة أفضل عيادات تجميل الأنف في إسطنبول وأنطاليا. التكاليف والخبرة والتعافي.",
                "body": """## تركيا: عاصمة تجميل الأنف

تجري تركيا عمليات تجميل أنف أكثر من أي دولة تقريباً. بتكلفة تبدأ من $3,500 مقارنة بـ $8,000-$15,000 في أوروبا.

## إسطنبول مقابل أنطاليا

**إسطنبول** تقدم أكبر مجموعة من الجراحين. مستشفيات كبرى مثل ميموريال وأجيبادم.

**أنطاليا** تجمع بين العملية وعطلة على ساحل البحر المتوسط.

كلتا المدينتين لديها مرافق معتمدة JCI عبر [نظام المطابقة](/medical).

## ماذا تتوقع

- **الاستشارة**: تقييم افتراضي أو شخصي
- **يوم العملية**: 2-3 ساعات تحت التخدير العام
- **اليوم 7**: إزالة الجبيرة والفحص النهائي

## احجز استشارة مجانية

[احصل على استشارة مجانية](/medical) — سيجد المنسق الجراح المثالي لك.""",
            },
            "zh": {
                "title": "土耳其隆鼻：伊斯坦布尔与安塔利亚诊所对比",
                "slug": "turkey-rhinoplasty-guide-zh",
                "excerpt": "对比伊斯坦布尔和安塔利亚顶级隆鼻诊所。费用、医生专业水平、恢复期。",
                "body": """## 土耳其：隆鼻之都

土耳其是全球隆鼻手术量最大的国家之一。价格从$3,500起，而欧洲为$8,000-$15,000。

## 伊斯坦布尔 vs 安塔利亚

**伊斯坦布尔**提供最多的外科医生和诊所选择。

**安塔利亚**将手术与地中海海岸度假相结合。

两个城市都有JCI认证设施，可通过我们的[诊所匹配系统](/medical)获取。

## 费用对比

| 项目 | 土耳其 | 英国 |
|------|--------|------|
| 外科医生 | $2,500–$4,000 | $5,000–$10,000 |
| 医院 | 已包含 | $2,000–$5,000 |
| 酒店 | $300–$600 | — |
| 总计 | $3,500–$5,000 | $8,000–$15,000 |

## 开始您的旅程

[预约免费咨询](/medical) — 协调员将为您匹配理想的外科医生。""",
            },
        },
    },
    {
        "id": "dental-veneers-turkey",
        "category": "dental",
        "featured": True,
        "author": "Dr. AntiGravity Medical",
        "date": "2026-02-05",
        "read_time": 6,
        "image": "/images/blog/dental.jpg",
        "tags": ["dental", "veneers", "crowns", "Turkey"],
        "translations": {
            "en": {
                "title": "Dental Veneers & Crowns in Turkey: Save Up to 70%",
                "slug": "dental-veneers-turkey",
                "excerpt": "Why thousands choose Turkey for dental veneers and crowns. E-max, zirconia, costs, and the Hollywood smile treatment explained.",
                "body": """## The Dental Tourism Boom

Turkey has become Europe's dental chair, with over 200,000 international patients choosing Turkish dental clinics each year. The savings are dramatic — up to 70% compared to UK or US prices.

## Types of Dental Veneers

**E-max Veneers**: Premium porcelain with a natural translucency. Minimal tooth preparation required. Last 15-20 years.

**Zirconia Crowns**: Stronger option for back teeth. Excellent durability with natural aesthetics.

**Composite Veneers**: Budget-friendly option. Can be done in a single visit but less durable (5-7 years).

## Cost Comparison (per tooth)

| Type | Turkey | UK | USA |
|------|--------|-----|-----|
| E-max Veneer | $250–$400 | $800–$1,200 | $1,000–$2,000 |
| Zirconia Crown | $200–$350 | $600–$1,000 | $800–$1,500 |
| Composite | $100–$150 | $300–$500 | $400–$800 |

## The Hollywood Smile Package

Most patients opt for a full set of 20 veneers — the "Hollywood Smile." In Turkey, this costs $5,000-$8,000. The same treatment in the UK runs $16,000-$24,000.

Your [AntiGravity dental package](/medical) includes:
- 3D digital scan and design preview
- All dental work with premium materials
- Hotel accommodation (5-7 nights)
- Airport transfers
- Follow-up check in Phuket

## Timeline

- **Day 1**: Consultation, 3D scan, tooth preparation
- **Day 2-5**: Lab creates your custom veneers
- **Day 5-7**: Fitting, adjustments, final polish
- **Day 8**: Final check and departure

## Book Your Smile Makeover

[Get a free consultation](/medical) — see your new smile in a 3D preview before committing.""",
            },
            "ru": {
                "title": "Виниры и коронки в Турции: экономия до 70%",
                "slug": "viniry-koronki-turtsiya",
                "excerpt": "Почему тысячи выбирают Турцию для виниров. E-max, цирконий, стоимость и голливудская улыбка.",
                "body": """## Бум стоматологического туризма

Турция стала стоматологическим кабинетом Европы — более 200 000 международных пациентов ежегодно. Экономия до 70%.

## Типы виниров

**E-max виниры**: Премиальный фарфор с натуральной прозрачностью. Минимальная препарация зубов. Срок службы 15-20 лет.

**Циркониевые коронки**: Прочнее для жевательных зубов. Отличная эстетика.

**Композитные виниры**: Бюджетный вариант. За одно посещение, но менее долговечны (5-7 лет).

## Стоимость (за зуб)

| Тип | Турция | Великобритания | США |
|-----|--------|---------------|-----|
| E-max | $250–$400 | $800–$1,200 | $1,000–$2,000 |
| Цирконий | $200–$350 | $600–$1,000 | $800–$1,500 |

## Голливудская улыбка

Полный комплект из 20 виниров в Турции: $5,000-$8,000. В Великобритании: $16,000-$24,000.

Ваш [пакет AntiGravity](/medical) включает: 3D-сканирование, все работы, отель, трансферы, наблюдение на Пхукете.

## Запишитесь

[Бесплатная консультация](/medical) — увидьте свою новую улыбку в 3D-превью.""",
            },
            "tr": {
                "title": "Turkiye'de Dis Kaplama ve Kronlar: %70'e Kadar Tasarruf",
                "slug": "turkiyede-dis-kaplama",
                "excerpt": "Binlerce kisi neden dis kaplamalari icin Turkiye'yi seciyor. E-max, zirkonyum, maliyetler ve Hollywood gulumse tedavisi.",
                "body": """## Dis Turizmi Patlamasi

Turkiye, yillik 200.000'den fazla uluslararasi hastayla Avrupa'nin dis koltugu haline gelmistir. Tasarruf dramatik — Ingiltere veya ABD fiyatlarina gore %70'e kadar.

## Dis Kaplama Turleri

**E-max Kaplamalar**: Dogal gecirgenlige sahip premium porselen. 15-20 yil dayanir.

**Zirkonyum Kronlar**: Arka disler icin daha guclu secenek.

## Fiyat Karsilastirmasi (dis basina)

| Tur | Turkiye | Ingiltere |
|-----|---------|-----------|
| E-max | $250–$400 | $800–$1,200 |
| Zirkonyum | $200–$350 | $600–$1,000 |

## Hollywood Gulus Paketi

20 kaplamadan olusan tam set Turkiye'de $5,000-$8,000. Ingiltere'de $16,000-$24,000.

[AntiGravity dis paketiniz](/medical): 3D tarama, tum islemler, otel, transfer, Phuket'te takip.

## Randevu Alin

[Ucretsiz danismanlik alin](/medical) — 3D ongoru ile yeni gulusunuzu gorun.""",
            },
            "th": {
                "title": "วีเนียร์และครอบฟันที่ตุรกี: ประหยัดสูงสุด 70%",
                "slug": "veneer-crown-turkey",
                "excerpt": "ทำไมหลายพันคนเลือกตุรกีสำหรับวีเนียร์ E-max เซอร์โคเนีย ค่าใช้จ่าย และ Hollywood Smile",
                "body": """## การท่องเที่ยวเชิงทันตกรรม

ตุรกีรับผู้ป่วยต่างชาติมากกว่า 200,000 คนต่อปีสำหรับทันตกรรม ประหยัดสูงสุด 70%

## ประเภทวีเนียร์

**E-max**: พอร์ซเลนพรีเมียมความโปร่งแสงธรรมชาติ อายุ 15-20 ปี

**เซอร์โคเนียคราวน์**: แข็งแรงกว่าสำหรับฟันกราม

## เปรียบเทียบราคา (ต่อซี่)

| ประเภท | ตุรกี | อังกฤษ |
|--------|-------|--------|
| E-max | $250–$400 | $800–$1,200 |
| เซอร์โคเนีย | $200–$350 | $600–$1,000 |

## แพ็คเกจ Hollywood Smile

ครบเซ็ต 20 ซี่ในตุรกี $5,000-$8,000 vs อังกฤษ $16,000-$24,000

[แพ็คเกจ AntiGravity](/medical) รวม: สแกน 3D, งานทันตกรรมทั้งหมด, โรงแรม, รถรับส่ง, ติดตามผลที่ภูเก็ต

## จองปรึกษาฟรี

[รับคำปรึกษาฟรี](/medical)""",
            },
            "ar": {
                "title": "قشور وتيجان الأسنان في تركيا: وفر حتى 70%",
                "slug": "qushur-asnan-turkiya",
                "excerpt": "لماذا يختار الآلاف تركيا لقشور الأسنان. E-max والزركونيا والتكاليف وابتسامة هوليوود.",
                "body": """## طفرة سياحة الأسنان

أصبحت تركيا كرسي طبيب أسنان أوروبا بأكثر من 200,000 مريض دولي سنوياً. التوفير يصل إلى 70%.

## أنواع القشور

**E-max**: بورسلين فاخر بشفافية طبيعية. يدوم 15-20 سنة.

**تيجان الزركونيا**: أقوى للأسنان الخلفية.

## ابتسامة هوليوود

مجموعة كاملة من 20 قشرة في تركيا: $5,000-$8,000 مقابل $16,000-$24,000 في بريطانيا.

[باقة AntiGravity](/medical) تشمل: مسح 3D، جميع الأعمال، فندق، نقل، متابعة في بوكيت.

## احجز استشارة مجانية

[استشارة مجانية](/medical)""",
            },
            "zh": {
                "title": "土耳其牙贴面和牙冠：节省高达70%",
                "slug": "dental-veneers-turkey-zh",
                "excerpt": "为什么数千人选择土耳其做牙贴面。E-max、氧化锆、费用和好莱坞微笑。",
                "body": """## 牙科旅游热潮

土耳其每年接待超过20万名国际牙科患者。节省高达70%。

## 贴面类型

**E-max贴面**：天然通透感的优质瓷贴面，使用寿命15-20年。

**氧化锆牙冠**：后牙的更强选择。

## 好莱坞微笑套餐

全套20颗贴面在土耳其$5,000-$8,000，英国$16,000-$24,000。

[AntiGravity套餐](/medical)包括：3D扫描、所有牙科工作、酒店、接送、普吉岛随访。

## 预约免费咨询

[获取免费咨询](/medical)""",
            },
        },
    },
    {
        "id": "ivf-turkey-success-rates",
        "category": "ivf",
        "featured": False,
        "author": "Dr. AntiGravity Medical",
        "date": "2026-01-28",
        "read_time": 9,
        "image": "/images/blog/ivf.jpg",
        "tags": ["IVF", "fertility", "Turkey", "success rates"],
        "translations": {
            "en": {
                "title": "IVF in Turkey: Success Rates, Costs & What to Expect",
                "slug": "ivf-turkey-success-rates",
                "excerpt": "Turkey's IVF success rates rival the best in Europe. Complete guide to fertility treatment costs, clinics, and the patient journey.",
                "body": """## Why Choose Turkey for IVF?

Turkey's IVF clinics achieve success rates of 50-60% for women under 35, comparable to the best European centers. With costs 50-65% lower, it's a compelling option for couples worldwide.

## Success Rates by Age

| Age Group | Turkey | UK | USA |
|-----------|--------|-----|-----|
| Under 35 | 50-60% | 45-55% | 50-55% |
| 35-37 | 40-50% | 35-45% | 40-45% |
| 38-40 | 30-40% | 25-35% | 30-35% |
| Over 40 | 15-25% | 15-20% | 15-25% |

## Cost Comparison

| Treatment | Turkey | UK | USA |
|-----------|--------|-----|-----|
| Standard IVF | $3,500–$5,000 | $7,000–$12,000 | $12,000–$20,000 |
| IVF + ICSI | $4,000–$5,500 | $8,000–$14,000 | $15,000–$25,000 |
| Egg freezing | $2,000–$3,000 | $4,000–$7,000 | $6,000–$10,000 |

## Top IVF Clinics in Turkey

Our [partner network](/medical) includes leading fertility centers in Istanbul with:
- State-of-the-art embryology labs
- Genetic screening (PGT-A) capabilities
- Multilingual medical teams
- Dedicated fertility coordinators

## The IVF Journey

1. **Initial consultation** (virtual): Medical history review, treatment plan
2. **Stimulation phase**: 10-12 days of hormone treatment
3. **Egg retrieval**: Outpatient procedure, 15-20 minutes
4. **Fertilization**: Embryo culture for 3-5 days
5. **Transfer**: Quick, painless procedure
6. **The wait**: Pregnancy test after 12-14 days
7. **Follow-up**: Monitoring available at our [Phuket partner clinic](/medical)

## Book Your Consultation

[Start your fertility journey](/medical) — compassionate, confidential support from day one.""",
            },
            "ru": {
                "title": "ЭКО в Турции: успешность, стоимость и процесс",
                "slug": "eko-turtsiya-uspeshnost",
                "excerpt": "Показатели успешности ЭКО в Турции конкурируют с лучшими в Европе. Полное руководство по стоимости и клиникам.",
                "body": """## Почему Турция для ЭКО?

Клиники ЭКО в Турции достигают показателей 50-60% для женщин до 35 лет. При стоимости на 50-65% ниже — отличный вариант.

## Стоимость

| Процедура | Турция | Великобритания |
|-----------|--------|---------------|
| Стандартное ЭКО | $3,500–$5,000 | $7,000–$12,000 |
| ЭКО + ICSI | $4,000–$5,500 | $8,000–$14,000 |

## Путь ЭКО

1. **Консультация**: обзор истории, план лечения
2. **Стимуляция**: 10-12 дней гормональной терапии
3. **Забор яйцеклеток**: амбулаторная процедура
4. **Оплодотворение**: культивация эмбрионов 3-5 дней
5. **Перенос**: быстрая безболезненная процедура
6. **Тест на беременность**: через 12-14 дней
7. **Наблюдение**: в [партнёрской клинике на Пхукете](/medical)

## Запишитесь

[Начните путь к материнству](/medical) — конфиденциальная поддержка с первого дня.""",
            },
            "tr": { "title": "Turkiye'de Tup Bebek: Basari Oranlari ve Maliyetler", "slug": "turkiyede-tup-bebek", "excerpt": "Turkiye'nin tup bebek basari oranlari Avrupa'nin en iyileriyle yarisiyor.", "body": """## Neden Turkiye'de Tup Bebek?\n\nTurkiye'nin IVF klinikleri 35 yas alti kadinlarda %50-60 basari orani elde etmektedir.\n\n## Maliyet Karsilastirmasi\n\n| Tedavi | Turkiye | Ingiltere |\n|--------|---------|----------|\n| Standart IVF | $3,500–$5,000 | $7,000–$12,000 |\n| IVF + ICSI | $4,000–$5,500 | $8,000–$14,000 |\n\n## Surecimiz\n\n1. Danismanlik ve plan\n2. 10-12 gunluk stimulasyon\n3. Yumurta toplama\n4. Dollenme ve embriyo kulturu\n5. Transfer\n6. Gebelik testi\n7. [Phuket'te takip](/medical)\n\n[Ucretsiz danismanlik alin](/medical)""" },
            "th": { "title": "IVF ที่ตุรกี: อัตราความสำเร็จ ค่าใช้จ่าย และสิ่งที่คาดหวัง", "slug": "ivf-turkey-th", "excerpt": "อัตราความสำเร็จ IVF ของตุรกีแข่งขันกับศูนย์ชั้นนำของยุโรป", "body": """## ทำไมเลือกตุรกีสำหรับ IVF?\n\nคลินิก IVF ในตุรกีมีอัตราความสำเร็จ 50-60% สำหรับผู้หญิงอายุต่ำกว่า 35 ปี ค่าใช้จ่ายต่ำกว่า 50-65%\n\n## ค่าใช้จ่าย\n\n| การรักษา | ตุรกี | อังกฤษ |\n|----------|-------|--------|\n| IVF | $3,500–$5,000 | $7,000–$12,000 |\n| IVF + ICSI | $4,000–$5,500 | $8,000–$14,000 |\n\n## ขั้นตอน\n\n1. ปรึกษาและวางแผน\n2. กระตุ้นไข่ 10-12 วัน\n3. เก็บไข่\n4. ปฏิสนธิ\n5. ย้ายตัวอ่อน\n6. ตรวจตั้งครรภ์\n7. [ติดตามผลที่ภูเก็ต](/medical)\n\n[จองปรึกษาฟรี](/medical)""" },
            "ar": { "title": "أطفال الأنابيب في تركيا: نسب النجاح والتكاليف", "slug": "ivf-turkiya", "excerpt": "معدلات نجاح أطفال الأنابيب في تركيا تنافس أفضل المراكز الأوروبية.", "body": """## لماذا تركيا لأطفال الأنابيب؟\n\nتحقق عيادات تركيا معدلات 50-60% للنساء تحت 35 سنة.\n\n## التكاليف\n\n| العلاج | تركيا | بريطانيا |\n|--------|-------|----------|\n| IVF | $3,500–$5,000 | $7,000–$12,000 |\n\n## الرحلة\n\n1. الاستشارة\n2. التحفيز 10-12 يوم\n3. سحب البويضات\n4. التخصيب\n5. النقل\n6. اختبار الحمل\n7. [متابعة في بوكيت](/medical)\n\n[احجز استشارة مجانية](/medical)""" },
            "zh": { "title": "土耳其试管婴儿：成功率、费用和流程", "slug": "ivf-turkey-zh", "excerpt": "土耳其IVF成功率媲美欧洲顶级中心。完整指南。", "body": """## 为什么选择土耳其做IVF？\n\n土耳其IVF诊所35岁以下女性成功率达50-60%。费用低50-65%。\n\n## 费用对比\n\n| 治疗 | 土耳其 | 英国 |\n|------|--------|------|\n| IVF | $3,500–$5,000 | $7,000–$12,000 |\n\n## 流程\n\n1. 初诊咨询\n2. 促排卵10-12天\n3. 取卵\n4. 受精培养\n5. 胚胎移植\n6. 验孕\n7. [普吉岛随访](/medical)\n\n[预约免费咨询](/medical)""" },
        },
    },
    {
        "id": "eye-surgery-lasik-turkey",
        "category": "eye_surgery",
        "featured": False,
        "author": "Dr. AntiGravity Medical",
        "date": "2026-01-20",
        "read_time": 5,
        "image": "/images/blog/eye-surgery.jpg",
        "tags": ["LASIK", "eye surgery", "vision", "Turkey"],
        "translations": {
            "en": { "title": "LASIK Eye Surgery in Turkey: Clear Vision for Less", "slug": "lasik-eye-surgery-turkey", "excerpt": "LASIK in Turkey costs $1,000-$2,000 for both eyes — a fraction of Western prices. Learn about the procedure and top eye clinics.", "body": """## Why Turkey for LASIK?\n\nTurkey's eye surgery clinics use the latest excimer laser technology at a fraction of Western costs. LASIK for both eyes: $1,000-$2,000 vs $4,000-$6,000 in the UK.\n\n## Types of Laser Eye Surgery\n\n**LASIK**: The most popular. A thin flap is created, the cornea reshaped by laser, and the flap replaced. Vision improves within hours.\n\n**PRK/LASEK**: Surface treatment without a flap. Better for thin corneas. Slightly longer recovery.\n\n**SMILE**: Minimally invasive, small incision technique. Fastest recovery.\n\n## Cost Comparison (both eyes)\n\n| Procedure | Turkey | UK | USA |\n|-----------|--------|-----|-----|\n| LASIK | $1,000–$2,000 | $4,000–$6,000 | $4,000–$8,000 |\n| PRK | $800–$1,500 | $3,000–$5,000 | $3,000–$6,000 |\n\n## The Process\n\n1. **Pre-op assessment**: Comprehensive eye exam\n2. **Procedure**: 15-20 minutes, painless\n3. **Recovery**: Rest for 24 hours, vision improves rapidly\n4. **Follow-up**: Next day check, then 1 week, then 1 month\n\nFollow-up available at our [Phuket partner clinic](/medical).\n\n## Book Your Consultation\n\n[Get a free eye surgery consultation](/medical)""" },
            "ru": { "title": "LASIK в Турции: четкое зрение по доступной цене", "slug": "lasik-turtsiya", "excerpt": "LASIK в Турции стоит $1,000-$2,000 за оба глаза. Узнайте о процедуре и клиниках.", "body": """## Почему Турция для LASIK?\n\nТурецкие клиники используют новейшие лазерные технологии по доступным ценам. LASIK: $1,000-$2,000 vs $4,000-$6,000 в Великобритании.\n\n## Типы лазерной коррекции\n\n**LASIK**: Самый популярный метод. Зрение улучшается в течение часов.\n\n**PRK/LASEK**: Поверхностная обработка без лоскута.\n\n**SMILE**: Минимально инвазивная техника.\n\n## Стоимость (оба глаза)\n\n| Процедура | Турция | Великобритания |\n|-----------|--------|---------------|\n| LASIK | $1,000–$2,000 | $4,000–$6,000 |\n\n## Процесс\n\n1. Обследование глаз\n2. Процедура: 15-20 минут\n3. Восстановление: 24 часа\n4. Наблюдение в [клинике на Пхукете](/medical)\n\n[Запишитесь](/medical)""" },
            "tr": { "title": "Turkiye'de LASIK Goz Ameliyati", "slug": "turkiyede-lasik", "excerpt": "Turkiye'de LASIK iki goz icin $1,000-$2,000. Bati fiyatlarinin bir kismina.", "body": """## Neden Turkiye'de LASIK?\n\nTurkiye'nin goz klinikleri en son lazer teknolojisini kullaniyor. Her iki goz LASIK: $1,000-$2,000 vs Ingiltere'de $4,000-$6,000.\n\n## Turler\n\n**LASIK**: En populer yontem.\n**PRK/LASEK**: Ince kornea icin.\n**SMILE**: Minimum invaziv.\n\n## Fiyat (iki goz)\n\n| Islem | Turkiye | Ingiltere |\n|-------|---------|----------|\n| LASIK | $1,000–$2,000 | $4,000–$6,000 |\n\n[Ucretsiz danismanlik alin](/medical)""" },
            "th": { "title": "ทำเลสิกที่ตุรกี: มองเห็นชัดในราคาคุ้ม", "slug": "lasik-turkey-th", "excerpt": "เลสิกที่ตุรกี $1,000-$2,000 ทั้งสองข้าง เทียบกับราคาตะวันตก", "body": """## ทำไมเลสิกที่ตุรกี?\n\nคลินิกตาในตุรกีใช้เทคโนโลยีเลเซอร์ล่าสุด ราคา $1,000-$2,000 vs อังกฤษ $4,000-$6,000\n\n## ประเภท\n\n**LASIK**: ยอดนิยม\n**PRK**: สำหรับกระจกตาบาง\n**SMILE**: รุกรานน้อยที่สุด\n\n[จองปรึกษาฟรี](/medical)""" },
            "ar": { "title": "جراحة العيون بالليزك في تركيا", "slug": "lasik-turkiya", "excerpt": "الليزك في تركيا $1,000-$2,000 للعينين. جزء من الأسعار الغربية.", "body": """## لماذا تركيا للعيون؟\n\nتستخدم عيادات تركيا أحدث تقنيات الليزر. الليزك: $1,000-$2,000 مقابل $4,000-$6,000 في بريطانيا.\n\n## الأنواع\n\n**LASIK**: الأكثر شيوعاً\n**PRK**: للقرنية الرقيقة\n**SMILE**: أقل تدخل\n\n[احجز استشارة مجانية](/medical)""" },
            "zh": { "title": "土耳其LASIK激光眼科手术", "slug": "lasik-turkey-zh", "excerpt": "土耳其LASIK双眼$1,000-$2,000，仅为西方价格的一小部分。", "body": """## 为什么选择土耳其LASIK？\n\n土耳其眼科诊所使用最新激光技术。双眼LASIK：$1,000-$2,000 vs 英国$4,000-$6,000。\n\n## 类型\n\n**LASIK**：最受欢迎\n**PRK**：适合薄角膜\n**SMILE**：微创\n\n[预约免费咨询](/medical)""" },
        },
    },
    {
        "id": "bbl-turkey-safety",
        "category": "bbl",
        "featured": False,
        "author": "Dr. AntiGravity Medical",
        "date": "2026-01-15",
        "read_time": 7,
        "image": "/images/blog/bbl.jpg",
        "tags": ["BBL", "body contouring", "safety", "Turkey"],
        "translations": {
            "en": { "title": "BBL in Turkey: Safety, Costs & Choosing the Right Clinic", "slug": "bbl-turkey-safety", "excerpt": "Brazilian Butt Lift in Turkey: what you need to know about safety standards, costs ($4,000-$7,000), and finding a qualified surgeon.", "body": """## BBL in Turkey: The Facts\n\nThe Brazilian Butt Lift has become one of Turkey's most requested procedures. While demand is high, choosing the right clinic is crucial for safety.\n\n## Safety First\n\nAt AntiGravity Medical, we only partner with clinics that follow strict safety protocols:\n- Board-certified plastic surgeons with BBL specialization\n- Modern operating theaters with proper monitoring\n- Fat injection below the muscle fascia (safer technique)\n- Overnight hospital stay included\n\n## Cost Comparison\n\n| Location | Cost |\n|----------|------|\n| Turkey | $4,000–$7,000 |\n| UK | $8,000–$15,000 |\n| USA | $10,000–$20,000 |\n\n## What's Included\n\n- Pre-operative tests and consultation\n- The BBL procedure with liposuction\n- Compression garment\n- 1-night hospital stay\n- 5 nights hotel\n- VIP transfers\n- [Phuket follow-up](/medical)\n\n## Recovery\n\n- Week 1-2: No sitting directly on buttocks\n- Week 3-4: Light activities resume\n- Month 2-3: Full results visible\n- 6 months: Final shape settled\n\n[Book a free consultation](/medical)""" },
            "ru": { "title": "BBL в Турции: безопасность, стоимость и выбор клиники", "slug": "bbl-turtsiya", "excerpt": "Бразильская подтяжка ягодиц: безопасность, стоимость $4,000-$7,000 и выбор хирурга.", "body": """## BBL в Турции\n\nBBL — одна из самых востребованных процедур. Выбор правильной клиники критически важен.\n\n## Безопасность\n\nМы работаем только с клиниками с строгими протоколами безопасности.\n\n## Стоимость\n\n| Страна | Цена |\n|--------|------|\n| Турция | $4,000–$7,000 |\n| Великобритания | $8,000–$15,000 |\n\n## Что включено\n\n- Предоперационные тесты\n- BBL с липосакцией\n- Компрессионное бельё\n- 1 ночь в клинике, 5 ночей отель\n- Трансферы\n- [Наблюдение на Пхукете](/medical)\n\n[Запишитесь](/medical)""" },
            "tr": { "title": "Turkiye'de BBL: Guvenlik, Maliyetler ve Dogru Klinik Secimi", "slug": "turkiyede-bbl", "excerpt": "Turkiye'de BBL: guvenlik standartlari, maliyet $4,000-$7,000 ve nitelikli cerrah bulma.", "body": """## Turkiye'de BBL\n\nBBL en cok talep edilen islemlerden biri. Dogru klinigin secimi guvenlik icin kritik.\n\n## Guvenlik\n\nSadece siki guvenlik protokollerine uyan kliniklerle calisiyoruz.\n\n## Maliyet\n\n| Ulke | Maliyet |\n|------|--------|\n| Turkiye | $4,000–$7,000 |\n| Ingiltere | $8,000–$15,000 |\n\n[Ucretsiz danismanlik alin](/medical)""" },
            "th": { "title": "BBL ที่ตุรกี: ความปลอดภัย ค่าใช้จ่าย และเลือกคลินิก", "slug": "bbl-turkey-th", "excerpt": "BBL ในตุรกี: มาตรฐานความปลอดภัย ค่าใช้จ่าย $4,000-$7,000", "body": """## BBL ที่ตุรกี\n\nBBL เป็นหนึ่งในขั้นตอนที่ได้รับความนิยมสูงสุด การเลือกคลินิกที่เหมาะสมเป็นสิ่งสำคัญ\n\n## ค่าใช้จ่าย\n\n| ประเทศ | ราคา |\n|--------|------|\n| ตุรกี | $4,000–$7,000 |\n| อังกฤษ | $8,000–$15,000 |\n\n[จองปรึกษาฟรี](/medical)""" },
            "ar": { "title": "BBL في تركيا: السلامة والتكاليف", "slug": "bbl-turkiya", "excerpt": "رفع المؤخرة البرازيلي: السلامة والتكاليف $4,000-$7,000.", "body": """## BBL في تركيا\n\nBBL من أكثر العمليات طلباً. اختيار العيادة المناسبة أمر حاسم.\n\n## التكاليف\n\n| الموقع | التكلفة |\n|--------|--------|\n| تركيا | $4,000–$7,000 |\n| بريطانيا | $8,000–$15,000 |\n\n[احجز استشارة مجانية](/medical)""" },
            "zh": { "title": "土耳其BBL：安全性、费用和选择诊所", "slug": "bbl-turkey-zh", "excerpt": "巴西臀部提升术：安全标准、费用$4,000-$7,000。", "body": """## 土耳其BBL\n\nBBL是最受欢迎的手术之一。选择合适的诊所至关重要。\n\n## 费用\n\n| 地点 | 费用 |\n|------|------|\n| 土耳其 | $4,000–$7,000 |\n| 英国 | $8,000–$15,000 |\n\n[预约免费咨询](/medical)""" },
        },
    },
    {
        "id": "breast-augmentation-turkey",
        "category": "breast",
        "featured": False,
        "author": "Dr. AntiGravity Medical",
        "date": "2026-01-10",
        "read_time": 6,
        "image": "/images/blog/breast.jpg",
        "tags": ["breast augmentation", "implants", "Turkey"],
        "translations": {
            "en": { "title": "Breast Augmentation in Turkey: Implants, Costs & Recovery", "slug": "breast-augmentation-turkey", "excerpt": "Breast augmentation in Turkey from $3,000 with Motiva or Mentor implants. Complete guide to the procedure, recovery, and results.", "body": """## Breast Surgery in Turkey\n\nTurkey offers premium breast augmentation with top-brand implants (Motiva, Mentor, Allergan) at 50-65% less than UK/US prices.\n\n## Cost Comparison\n\n| Procedure | Turkey | UK |\n|-----------|--------|-----|\n| Augmentation | $3,000–$5,000 | $6,000–$10,000 |\n| Lift + Augmentation | $4,000–$6,000 | $8,000–$14,000 |\n| Reduction | $3,500–$5,500 | $7,000–$12,000 |\n\n## What's Included\n\n- Consultation with board-certified surgeon\n- Premium implants of your choice\n- 1-night hospital stay\n- Compression bra\n- Hotel + transfers\n- [Phuket follow-up](/medical)\n\n## Recovery\n\n- Week 1: Rest, light movement\n- Week 2-4: Gradual return to activities\n- Month 3: Implants settle, final shape\n- 6 months: Scars fade significantly\n\n[Book a free consultation](/medical)""" },
            "ru": { "title": "Увеличение груди в Турции: импланты, стоимость и восстановление", "slug": "uvelichenie-grudi-turtsiya", "excerpt": "Увеличение груди в Турции от $3,000 с имплантами Motiva или Mentor.", "body": """## Маммопластика в Турции\n\nПремиальные импланты (Motiva, Mentor, Allergan) на 50-65% дешевле.\n\n## Стоимость\n\n| Процедура | Турция | Великобритания |\n|-----------|--------|---------------|\n| Увеличение | $3,000–$5,000 | $6,000–$10,000 |\n| Подтяжка + увеличение | $4,000–$6,000 | $8,000–$14,000 |\n\n## Что включено\n\nКонсультация, импланты, 1 ночь в клинике, компрессионное бельё, отель, трансферы, [наблюдение на Пхукете](/medical).\n\n[Запишитесь](/medical)""" },
            "tr": { "title": "Turkiye'de Gogus Buyutme: Implantlar ve Maliyetler", "slug": "turkiyede-gogus-buyutme", "excerpt": "Turkiye'de gogus buyutme Motiva veya Mentor implantlarla $3,000'dan.", "body": """## Turkiye'de Gogus Cerrahisi\n\nPremium implantlar %50-65 daha dusuk fiyatla.\n\n## Maliyet\n\n| Islem | Turkiye | Ingiltere |\n|-------|---------|----------|\n| Buyutme | $3,000–$5,000 | $6,000–$10,000 |\n\n[Ucretsiz danismanlik alin](/medical)""" },
            "th": { "title": "เสริมหน้าอกที่ตุรกี: ซิลิโคน ค่าใช้จ่าย และการฟื้นตัว", "slug": "serm-na-ok-turkey", "excerpt": "เสริมหน้าอกที่ตุรกีเริ่มต้น $3,000 พร้อมซิลิโคน Motiva หรือ Mentor", "body": """## ศัลยกรรมเต้านมในตุรกี\n\nซิลิโคนพรีเมียมราคาถูกกว่า 50-65%\n\n## ค่าใช้จ่าย\n\n| ขั้นตอน | ตุรกี | อังกฤษ |\n|---------|-------|--------|\n| เสริม | $3,000–$5,000 | $6,000–$10,000 |\n\n[จองปรึกษาฟรี](/medical)""" },
            "ar": { "title": "تكبير الثدي في تركيا: الزرعات والتكاليف", "slug": "takbeer-sader-turkiya", "excerpt": "تكبير الثدي في تركيا من $3,000 بزرعات Motiva أو Mentor.", "body": """## جراحة الثدي في تركيا\n\nزرعات فاخرة بأسعار أقل 50-65%.\n\n## التكاليف\n\n| العملية | تركيا | بريطانيا |\n|---------|-------|----------|\n| تكبير | $3,000–$5,000 | $6,000–$10,000 |\n\n[احجز استشارة مجانية](/medical)""" },
            "zh": { "title": "土耳其隆胸：假体、费用和恢复", "slug": "breast-augmentation-turkey-zh", "excerpt": "土耳其隆胸$3,000起，使用Motiva或Mentor假体。", "body": """## 土耳其胸部手术\n\n优质假体价格低50-65%。\n\n## 费用\n\n| 项目 | 土耳其 | 英国 |\n|------|--------|------|\n| 隆胸 | $3,000–$5,000 | $6,000–$10,000 |\n\n[预约免费咨询](/medical)""" },
        },
    },
    {
        "id": "bariatric-surgery-turkey",
        "category": "bariatric",
        "featured": False,
        "author": "Dr. AntiGravity Medical",
        "date": "2026-01-05",
        "read_time": 8,
        "image": "/images/blog/bariatric.jpg",
        "tags": ["bariatric", "gastric sleeve", "weight loss", "Turkey"],
        "translations": {
            "en": { "title": "Gastric Sleeve Surgery in Turkey: Transform Your Life", "slug": "bariatric-surgery-turkey", "excerpt": "Gastric sleeve in Turkey from $4,500 — with JCI-accredited hospitals, experienced surgeons, and comprehensive aftercare.", "body": """## Why Turkey for Bariatric Surgery?\n\nTurkey has become a leading destination for weight loss surgery. Gastric sleeve costs $4,500-$7,000, compared to $15,000-$25,000 in the US.\n\n## Types of Bariatric Surgery\n\n**Gastric Sleeve**: Most popular. Removes 80% of the stomach. Average weight loss: 60-70% of excess weight.\n\n**Gastric Bypass**: For higher BMI patients. Average weight loss: 70-80% of excess weight.\n\n**Gastric Balloon**: Non-surgical option. Temporary (6-12 months).\n\n## Cost Comparison\n\n| Surgery | Turkey | UK | USA |\n|---------|--------|-----|-----|\n| Sleeve | $4,500–$7,000 | $8,000–$15,000 | $15,000–$25,000 |\n| Bypass | $5,500–$8,000 | $10,000–$18,000 | $20,000–$35,000 |\n| Balloon | $2,000–$3,500 | $5,000–$8,000 | $6,000–$10,000 |\n\n## What's Included\n\n- Pre-op blood tests and assessment\n- The procedure at a JCI hospital\n- 3-night hospital stay\n- Dietitian consultation\n- 12-month post-op nutrition plan\n- Hotel + VIP transfers\n- [Phuket follow-up](/medical)\n\n[Start your weight loss journey](/medical)""" },
            "ru": { "title": "Бариатрическая хирургия в Турции: измените свою жизнь", "slug": "bariatricheskaya-hirurgiya-turtsiya", "excerpt": "Рукавная резекция желудка в Турции от $4,500 — JCI-клиники и опытные хирурги.", "body": """## Почему Турция?\n\nТурция — ведущее направление для бариатрической хирургии. Стоимость $4,500-$7,000 vs $15,000-$25,000 в США.\n\n## Виды\n\n**Рукавная резекция**: Самая популярная. Потеря 60-70% избыточного веса.\n\n**Шунтирование**: Для высокого ИМТ. Потеря 70-80%.\n\n## Стоимость\n\n| Операция | Турция | США |\n|----------|--------|-----|\n| Резекция | $4,500–$7,000 | $15,000–$25,000 |\n\n[Запишитесь](/medical)""" },
            "tr": { "title": "Turkiye'de Tup Mide Ameliyati", "slug": "turkiyede-tup-mide", "excerpt": "Turkiye'de tup mide $4,500'dan. JCI akrediteli hastaneler ve deneyimli cerrahlar.", "body": """## Neden Turkiye?\n\nTurkiye obezite cerrahisinde lider. Maliyet $4,500-$7,000 vs ABD'de $15,000-$25,000.\n\n## Turler\n\n**Tup Mide**: En populer. Fazla kilonun %60-70'ini kaybedersiniz.\n\n**Gastrik Bypass**: Yuksek BMI icin.\n\n[Ucretsiz danismanlik alin](/medical)""" },
            "th": { "title": "ผ่าตัดลดน้ำหนักที่ตุรกี", "slug": "bariatric-turkey-th", "excerpt": "Gastric Sleeve ที่ตุรกีเริ่มต้น $4,500 พร้อมโรงพยาบาล JCI", "body": """## ทำไมตุรกี?\n\nตุรกีเป็นจุดหมายชั้นนำสำหรับผ่าตัดลดน้ำหนัก ค่าใช้จ่าย $4,500-$7,000 vs สหรัฐ $15,000-$25,000\n\n[จองปรึกษาฟรี](/medical)""" },
            "ar": { "title": "جراحة تكميم المعدة في تركيا", "slug": "takeem-maida-turkiya", "excerpt": "تكميم المعدة في تركيا من $4,500 — مستشفيات JCI وجراحون ذوو خبرة.", "body": """## لماذا تركيا؟\n\nتركيا وجهة رائدة لجراحة السمنة. التكلفة $4,500-$7,000 مقابل $15,000-$25,000 في أمريكا.\n\n[احجز استشارة مجانية](/medical)""" },
            "zh": { "title": "土耳其胃袖状切除术", "slug": "bariatric-turkey-zh", "excerpt": "土耳其胃袖状切除术$4,500起——JCI认证医院和经验丰富的外科医生。", "body": """## 为什么选择土耳其？\n\n土耳其是减重手术的领先目的地。费用$4,500-$7,000 vs 美国$15,000-$25,000。\n\n[预约免费咨询](/medical)""" },
        },
    },
    {
        "id": "facelift-turkey-rejuvenation",
        "category": "facelift",
        "featured": False,
        "author": "Dr. AntiGravity Medical",
        "date": "2025-12-28",
        "read_time": 6,
        "image": "/images/blog/facelift.jpg",
        "tags": ["facelift", "rejuvenation", "anti-aging", "Turkey"],
        "translations": {
            "en": { "title": "Facelift in Turkey: Turn Back the Clock", "slug": "facelift-turkey-rejuvenation", "excerpt": "Facelift surgery in Turkey from $4,000 — natural results with experienced surgeons. Full face, mini facelift, and neck lift options.", "body": """## Facelift Options in Turkey\n\nTurkey's aesthetic surgeons specialize in natural-looking rejuvenation. Prices start from $4,000, compared to $10,000-$20,000 in the West.\n\n## Types\n\n**Full Facelift**: Addresses entire face. Lasts 10-15 years. $5,000-$8,000.\n\n**Mini Facelift**: Lower face focus. Less downtime. $4,000-$6,000.\n\n**Neck Lift**: Targets sagging neck skin. Often combined with facelift. $3,500-$5,500.\n\n## What's Included\n\n- Surgeon consultation and 3D simulation\n- The procedure\n- 1-night hospital stay\n- Recovery hotel (5-7 nights)\n- All transfers\n- [Phuket follow-up](/medical)\n\n## Recovery\n\n- Week 1: Bandages, mild swelling\n- Week 2: Stitches removed, bruising fades\n- Month 1: Social activities resume\n- Month 3: Final results visible\n\n[Book your consultation](/medical)""" },
            "ru": { "title": "Подтяжка лица в Турции: верните молодость", "slug": "podtyazhka-litsa-turtsiya", "excerpt": "Подтяжка лица в Турции от $4,000 — натуральные результаты с опытными хирургами.", "body": """## Варианты подтяжки лица\n\nТурецкие хирурги специализируются на естественном омоложении. Цены от $4,000 vs $10,000-$20,000 на Западе.\n\n## Типы\n\n**Полная подтяжка**: $5,000-$8,000\n**Мини-подтяжка**: $4,000-$6,000\n**Подтяжка шеи**: $3,500-$5,500\n\n[Запишитесь](/medical)""" },
            "tr": { "title": "Turkiye'de Yuz Germe: Gencliginizi Geri Kazanin", "slug": "turkiyede-yuz-germe", "excerpt": "Turkiye'de yuz germe $4,000'dan. Dogal sonuclar ve deneyimli cerrahlar.", "body": """## Turkiye'de Yuz Germe Secenekleri\n\nTurk estetik cerrahlar dogal gorunumlu germe islemi konusunda uzmandir. Fiyatlar $4,000'dan baslar.\n\n## Turler\n\n**Tam Yuz Germe**: $5,000-$8,000\n**Mini Yuz Germe**: $4,000-$6,000\n**Boyun Germe**: $3,500-$5,500\n\n[Ucretsiz danismanlik alin](/medical)""" },
            "th": { "title": "ดึงหน้าที่ตุรกี: ย้อนเวลากลับ", "slug": "facelift-turkey-th", "excerpt": "ศัลยกรรมดึงหน้าที่ตุรกีเริ่มต้น $4,000", "body": """## ตัวเลือกดึงหน้าในตุรกี\n\nศัลยแพทย์ตุรกีเชี่ยวชาญการทำให้ดูเป็นธรรมชาติ เริ่มต้น $4,000\n\n[จองปรึกษาฟรี](/medical)""" },
            "ar": { "title": "شد الوجه في تركيا: استعد شبابك", "slug": "shad-wajh-turkiya", "excerpt": "شد الوجه في تركيا من $4,000 — نتائج طبيعية مع جراحين ذوي خبرة.", "body": """## خيارات شد الوجه\n\nيتخصص جراحو تركيا في التجديد الطبيعي. الأسعار من $4,000.\n\n[احجز استشارة مجانية](/medical)""" },
            "zh": { "title": "土耳其面部提升：逆转时光", "slug": "facelift-turkey-zh", "excerpt": "土耳其面部提升手术$4,000起——自然效果，经验丰富的外科医生。", "body": """## 土耳其面部提升选择\n\n土耳其美容外科医生擅长自然效果。价格从$4,000起。\n\n[预约免费咨询](/medical)""" },
        },
    },
    {
        "id": "medical-tourism-guide-phuket-turkey",
        "category": "medical_tourism_guide",
        "featured": True,
        "author": "AntiGravity Medical Team",
        "date": "2026-02-18",
        "read_time": 10,
        "image": "/images/blog/medical-tourism.jpg",
        "tags": ["medical tourism", "guide", "Phuket", "Turkey", "planning"],
        "translations": {
            "en": { "title": "Medical Tourism Guide: Phuket to Turkey & Back", "slug": "medical-tourism-guide-phuket-turkey", "excerpt": "The complete guide to medical tourism between Phuket and Turkey. Planning, flights, visas, what to pack, and how our dual-country model works.", "body": """## The Dual-Country Advantage\n\nAntiGravity Medical pioneered the Phuket-Turkey health corridor. Pre-consultation in Phuket, treatment in Turkey, follow-up back in Phuket — seamless, safe, and cost-effective.\n\n## Step-by-Step Planning\n\n### 1. Initial Consultation (Phuket or Virtual)\nYour coordinator assesses your needs, matches you with the ideal clinic, and creates a personalized treatment plan.\n\n### 2. Travel Arrangements\n- **Flights**: Direct Phuket-Istanbul (6-7 hours) or via Dubai/Singapore\n- **Visa**: Most nationalities get Turkey e-visa online in minutes\n- **Insurance**: We recommend travel medical insurance\n\n### 3. Treatment in Turkey\n- VIP airport pickup\n- Hotel accommodation near clinic\n- Personal translator\n- The procedure itself\n- Post-op monitoring at the clinic\n\n### 4. Recovery\n- Hotel recovery with coordinator check-ins\n- Sightseeing opportunities (for suitable recovery periods)\n- Final check-up before departure\n\n### 5. Follow-up in Phuket\n- Post-operative monitoring at our partner clinic\n- Ongoing coordinator support\n- Results documentation\n\n## What to Pack\n\n- Comfortable, loose-fitting clothing\n- Medications list (with generic names)\n- Medical records and imaging\n- Passport and visa documents\n- Compression garments (if advised)\n\n## Cost Savings\n\nPatients save 40-70% on average compared to UK/US prices. With flights and hotel included, the total cost is still significantly less.\n\n| Procedure | All-Inclusive Turkey | UK Price Only |\n|-----------|---------------------|---------------|\n| Hair Transplant | $3,500–$5,000 | $8,000–$15,000 |\n| Rhinoplasty | $4,500–$6,000 | $8,000–$15,000 |\n| Dental (20 veneers) | $6,000–$9,000 | $16,000–$24,000 |\n\n## Start Your Journey\n\n[Book a free consultation](/medical) — your personal coordinator will guide you through every step.""" },
            "ru": { "title": "Гид по медицинскому туризму: Пхукет ↔ Турция", "slug": "gid-meditsinskiy-turizm-phuket-turtsiya", "excerpt": "Полное руководство по медицинскому туризму между Пхукетом и Турцией. Планирование, перелёты, визы и модель двух стран.", "body": """## Преимущество двух стран\n\nAntiGravity Medical — пионер коридора Пхукет-Турция. Пред-консультация на Пхукете, лечение в Турции, наблюдение снова на Пхукете.\n\n## Планирование шаг за шагом\n\n### 1. Консультация\nКоординатор оценит ваши потребности и подберёт идеальную клинику.\n\n### 2. Организация поездки\n- Прямые рейсы Пхукет-Стамбул (6-7 часов)\n- Электронная виза\n- Рекомендуем страховку\n\n### 3. Лечение в Турции\n- VIP-встреча в аэропорту\n- Отель рядом с клиникой\n- Переводчик\n\n### 4. Наблюдение на Пхукете\nПостоперационный контроль в партнёрской клинике.\n\n## Экономия\n\nПациенты экономят 40-70% по сравнению с ценами Великобритании/США.\n\n[Запишитесь на бесплатную консультацию](/medical)""" },
            "tr": { "title": "Medikal Turizm Rehberi: Phuket ↔ Turkiye", "slug": "medikal-turizm-rehberi", "excerpt": "Phuket ve Turkiye arasinda medikal turizm icin komple rehber. Planlama, ucuslar, vizeler ve cift ulke modelimiz.", "body": """## Cift Ulke Avantaji\n\nAntiGravity Medical Phuket-Turkiye saglik koridorunun oncusudur. Phuket'te on danismanlik, Turkiye'de tedavi, Phuket'te takip.\n\n## Adim Adim Planlama\n\n### 1. Danismanlik\nKoordinatorunuz ihtiyaclarinizi degerlendirir.\n\n### 2. Seyahat Duzenlemeleri\n- Phuket-Istanbul direkt ucuslar (6-7 saat)\n- E-vize\n\n### 3. Turkiye'de Tedavi\n- VIP transfer, otel, tercuman\n\n### 4. Phuket'te Takip\n\n## Tasarruf\n\nHastalar ortalama %40-70 tasarruf eder.\n\n[Ucretsiz danismanlik alin](/medical)""" },
            "th": { "title": "คู่มือการท่องเที่ยวเชิงการแพทย์: ภูเก็ต ↔ ตุรกี", "slug": "medical-tourism-guide-th", "excerpt": "คู่มือสมบูรณ์สำหรับการท่องเที่ยวเชิงการแพทย์ระหว่างภูเก็ตและตุรกี", "body": """## ข้อได้เปรียบสองประเทศ\n\nAntiGravity Medical บุกเบิกเส้นทางสุขภาพภูเก็ต-ตุรกี ปรึกษาเบื้องต้นที่ภูเก็ต รักษาที่ตุรกี ติดตามผลกลับที่ภูเก็ต\n\n## วางแผนทีละขั้น\n\n1. ปรึกษาเบื้องต้น\n2. จัดเตรียมการเดินทาง\n3. รักษาในตุรกี\n4. ติดตามผลที่ภูเก็ต\n\n## ประหยัด 40-70%\n\n[จองปรึกษาฟรี](/medical)""" },
            "ar": { "title": "دليل السياحة الطبية: بوكيت ↔ تركيا", "slug": "daleel-siyaha-tibbiya", "excerpt": "الدليل الشامل للسياحة الطبية بين بوكيت وتركيا.", "body": """## ميزة البلدين\n\nAntiGravity Medical رائدة ممر بوكيت-تركيا الصحي.\n\n## التخطيط خطوة بخطوة\n\n1. الاستشارة الأولية\n2. ترتيبات السفر\n3. العلاج في تركيا\n4. المتابعة في بوكيت\n\n## التوفير 40-70%\n\n[احجز استشارة مجانية](/medical)""" },
            "zh": { "title": "医疗旅游指南：普吉岛 ↔ 土耳其", "slug": "medical-tourism-guide-zh", "excerpt": "普吉岛和土耳其之间医疗旅游的完整指南。", "body": """## 双国优势\n\nAntiGravity Medical开创了普吉岛-土耳其健康走廊。\n\n## 分步规划\n\n1. 初次咨询\n2. 旅行安排\n3. 土耳其治疗\n4. 普吉岛随访\n\n## 节省40-70%\n\n[预约免费咨询](/medical)""" },
        },
    },
]


def get_all_posts(language: str = "en") -> list[dict]:
    """Get all blog posts for a specific language."""
    result = []
    for post in BLOG_POSTS:
        trans = post["translations"].get(language, post["translations"].get("en"))
        if trans:
            result.append({
                "id": post["id"],
                "slug": trans["slug"],
                "title": trans["title"],
                "excerpt": trans["excerpt"],
                "body": trans["body"],
                "category": post["category"],
                "featured": post["featured"],
                "author": post["author"],
                "date": post["date"],
                "read_time": post["read_time"],
                "image": post["image"],
                "tags": post["tags"],
            })
    return result


def get_post_by_slug(slug: str, language: str = "en") -> dict | None:
    """Find a post by slug in any language."""
    for post in BLOG_POSTS:
        for lang_code, trans in post["translations"].items():
            if trans["slug"] == slug:
                target = post["translations"].get(language, trans)
                return {
                    "id": post["id"],
                    "slug": target["slug"],
                    "title": target["title"],
                    "excerpt": target["excerpt"],
                    "body": target["body"],
                    "category": post["category"],
                    "featured": post["featured"],
                    "author": post["author"],
                    "date": post["date"],
                    "read_time": post["read_time"],
                    "image": post["image"],
                    "tags": post["tags"],
                    "original_slug": slug,
                }
    return None


def get_featured_posts(language: str = "en", limit: int = 3) -> list[dict]:
    """Get featured blog posts."""
    posts = get_all_posts(language)
    featured = [p for p in posts if p["featured"]]
    return featured[:limit]


def get_posts_by_category(category: str, language: str = "en") -> list[dict]:
    """Get posts filtered by category."""
    posts = get_all_posts(language)
    return [p for p in posts if p["category"] == category]


def get_all_slugs() -> list[dict[str, str]]:
    """Get all slugs for sitemap generation."""
    slugs = []
    for post in BLOG_POSTS:
        for lang_code, trans in post["translations"].items():
            slugs.append({"slug": trans["slug"], "language": lang_code, "date": post["date"]})
    return slugs
