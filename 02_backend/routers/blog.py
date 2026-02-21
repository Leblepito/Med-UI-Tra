"""
AntiGravity ThaiTurk — Blog API Router
Endpoints for blog posts, categories, and AI-generated content.
"""
from __future__ import annotations

import sys
from pathlib import Path
from fastapi import APIRouter, Query
from pydantic import BaseModel

# Ensure skills are importable
_skills_path = Path(__file__).parent.parent.parent / "04_ai_agents" / "skills"
if str(_skills_path) not in sys.path:
    sys.path.insert(0, str(_skills_path))

from blog_seed_data import (
    get_all_posts,
    get_post_by_slug,
    get_featured_posts,
    get_posts_by_category,
    get_all_slugs,
    BLOG_CATEGORIES,
)

router = APIRouter(prefix="/api/blog", tags=["Blog"])


@router.get("/posts")
def list_posts(
    language: str = Query("en", description="Language code: en, ru, tr, th, ar, zh"),
    category: str | None = Query(None, description="Filter by category slug"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
) -> dict:
    """List blog posts with optional category filter and pagination."""
    if category:
        posts = get_posts_by_category(category, language)
    else:
        posts = get_all_posts(language)

    total = len(posts)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = posts[start:end]

    return {
        "posts": paginated,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page,
    }


@router.get("/posts/{slug}")
def get_post(slug: str, language: str = Query("en")) -> dict:
    """Get a single blog post by slug."""
    post = get_post_by_slug(slug, language)
    if not post:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Blog post '{slug}' not found")
    return {"post": post}


@router.get("/categories")
def list_categories() -> dict:
    """List all blog categories."""
    return {"categories": BLOG_CATEGORIES}


@router.get("/featured")
def featured_posts(language: str = Query("en"), limit: int = Query(3, ge=1, le=10)) -> dict:
    """Get featured/latest blog posts."""
    posts = get_featured_posts(language, limit)
    return {"posts": posts}


@router.get("/slugs")
def all_slugs() -> dict:
    """Get all post slugs (for sitemap generation)."""
    return {"slugs": get_all_slugs()}


class GenerateBlogRequest(BaseModel):
    topic: str
    language: str = "en"
    region: str = "europe"


@router.post("/generate")
def generate_blog(req: GenerateBlogRequest) -> dict:
    """AI-generate a new blog post (admin endpoint). Placeholder for future AI integration."""
    return {
        "status": "planned",
        "message": "AI blog generation will be available in the next release.",
        "topic": req.topic,
        "language": req.language,
        "region": req.region,
    }
