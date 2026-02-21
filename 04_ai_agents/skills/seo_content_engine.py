"""
AntiGravity ThaiTurk — SEO Content Engine
Merges seo_engine + content_generator with region-aware content generation.
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from .region_profiles import get_region_by_language, get_platform_spec, PLATFORM_SPECS


def generate_meta_tags(title: str, description: str, language: str = "en") -> dict[str, str]:
    """Generate SEO meta tags for a page."""
    spec = get_platform_spec("blog") or {}
    title_max = spec.get("title_max", 70)
    desc_max = spec.get("meta_description_max", 160)

    return {
        "title": title[:title_max],
        "description": description[:desc_max],
        "og:title": title[:title_max],
        "og:description": description[:desc_max],
        "og:type": "article",
        "og:locale": _lang_to_locale(language),
        "twitter:card": "summary_large_image",
        "twitter:title": title[:title_max],
        "twitter:description": description[:desc_max],
    }


def generate_social_posts(blog_title: str, blog_excerpt: str, blog_url: str, platforms: list[str] | None = None) -> dict[str, str]:
    """Generate social media posts from blog content."""
    if platforms is None:
        platforms = ["twitter", "facebook", "linkedin"]

    posts: dict[str, str] = {}

    for platform in platforms:
        spec = get_platform_spec(platform)
        if not spec:
            continue

        if platform == "twitter":
            max_len = spec.get("tweet_max", 280)
            url_len = 23  # t.co short link
            available = max_len - url_len - 2
            text = f"{blog_title}: {blog_excerpt}"
            posts["twitter"] = f"{text[:available]} {blog_url}"
        elif platform == "facebook":
            posts["facebook"] = f"{blog_title}\n\n{blog_excerpt}\n\n{blog_url}"
        elif platform == "linkedin":
            posts["linkedin"] = f"{blog_title}\n\n{blog_excerpt}\n\nRead more: {blog_url}"

    return posts


def calculate_seo_score(content: str, keywords: list[str]) -> dict[str, Any]:
    """Score content for SEO quality."""
    words = content.split()
    word_count = len(words)
    content_lower = content.lower()

    keyword_counts: dict[str, int] = {}
    for kw in keywords:
        count = content_lower.count(kw.lower())
        keyword_counts[kw] = count

    total_kw_occurrences = sum(keyword_counts.values())
    density = (total_kw_occurrences / word_count * 100) if word_count > 0 else 0

    spec = get_platform_spec("blog") or {}
    min_words = spec.get("body_min_words", 500)
    max_words = spec.get("body_max_words", 1500)
    density_range = spec.get("keyword_density_pct", (1.0, 2.5))

    score = 100
    issues: list[str] = []

    if word_count < min_words:
        score -= 20
        issues.append(f"Content too short: {word_count} words (min {min_words})")
    elif word_count > max_words:
        score -= 5
        issues.append(f"Content may be too long: {word_count} words")

    if density < density_range[0]:
        score -= 15
        issues.append(f"Keyword density too low: {density:.1f}% (target {density_range[0]}-{density_range[1]}%)")
    elif density > density_range[1]:
        score -= 10
        issues.append(f"Keyword density too high: {density:.1f}% (target {density_range[0]}-{density_range[1]}%)")

    h2_count = len(re.findall(r"^## ", content, re.MULTILINE))
    h2_recommended = spec.get("h2_recommended", 3)
    if h2_count < h2_recommended:
        score -= 10
        issues.append(f"Only {h2_count} H2 headings (recommended {h2_recommended}+)")

    has_internal_links = bool(re.findall(r"\[.*?\]\(/.*?\)", content))
    if not has_internal_links:
        score -= 5
        issues.append("No internal links found")

    return {
        "score": max(0, score),
        "word_count": word_count,
        "keyword_density_pct": round(density, 2),
        "keyword_counts": keyword_counts,
        "h2_count": h2_count,
        "has_internal_links": has_internal_links,
        "issues": issues,
    }


def _lang_to_locale(lang: str) -> str:
    """Convert language code to locale string."""
    mapping = {
        "en": "en_US",
        "tr": "tr_TR",
        "ru": "ru_RU",
        "th": "th_TH",
        "ar": "ar_SA",
        "zh": "zh_CN",
    }
    return mapping.get(lang, "en_US")
