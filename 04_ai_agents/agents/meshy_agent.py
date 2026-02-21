"""
AntiGravity Ventures — Meshy Agent
Before/After visualization using Meshy.ai Image-to-Image API.

Responsibilities:
  1. Generate procedure-specific questions
  2. Build optimized prompts for Meshy.ai
  3. Call Meshy.ai image-to-image API
  4. Poll task status
"""
from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger("MeshyAgent")

MESHY_API_KEY = os.getenv("MESHY_API_KEY", "")
MESHY_BASE_URL = "https://api.meshy.ai/openapi/v1/image-to-image"

# ---------------------------------------------------------------------------
# Procedure Questions
# ---------------------------------------------------------------------------

PROCEDURE_QUESTIONS: dict[str, list[dict[str, str]]] = {
    "hair_transplant": [
        {"id": "grafts", "question_en": "How many grafts are you considering?", "question_tr": "Kac graft dusunuyorsunuz?", "question_ru": "Сколько графтов вы рассматриваете?", "type": "select", "options": "1500-2000,2000-3000,3000-4000,4000-5000,5000+"},
        {"id": "method", "question_en": "FUE or FUT method?", "question_tr": "FUE mi FUT mu?", "question_ru": "Метод FUE или FUT?", "type": "select", "options": "FUE,FUT,DHI"},
        {"id": "area", "question_en": "Which area needs treatment?", "question_tr": "Hangi bolge tedavi edilecek?", "question_ru": "Какая зона нуждается в лечении?", "type": "select", "options": "Hairline,Crown,Temple,Full coverage"},
    ],
    "rhinoplasty": [
        {"id": "nose_type", "question_en": "What is your current nose shape?", "question_tr": "Mevcut burun seklliniz?", "question_ru": "Какая у вас форма носа?", "type": "select", "options": "Wide,Hooked,Bulbous,Asymmetric,Long"},
        {"id": "change", "question_en": "What change do you want?", "question_tr": "Istediginiz degisiklik?", "question_ru": "Какое изменение хотите?", "type": "select", "options": "Smaller tip,Straighter bridge,Narrower nostrils,Overall refinement"},
        {"id": "breathing", "question_en": "Any breathing issues?", "question_tr": "Nefes problemi var mi?", "question_ru": "Есть проблемы с дыханием?", "type": "select", "options": "No,Yes - mild,Yes - severe"},
    ],
    "dental": [
        {"id": "treatment_type", "question_en": "What dental treatment?", "question_tr": "Hangi dis tedavisi?", "question_ru": "Какое стоматологическое лечение?", "type": "select", "options": "Veneers,Implants,Crowns,Full smile makeover"},
        {"id": "teeth_count", "question_en": "How many teeth?", "question_tr": "Kac dis?", "question_ru": "Сколько зубов?", "type": "select", "options": "1-4,5-8,8-12,Full arch (12-16),Both arches"},
        {"id": "shade", "question_en": "Preferred shade?", "question_tr": "Renk tercihi?", "question_ru": "Предпочтительный оттенок?", "type": "select", "options": "Natural white,Hollywood white,Match existing teeth"},
    ],
    "breast_augmentation": [
        {"id": "goal", "question_en": "What is your goal?", "question_tr": "Hedefiniz nedir?", "question_ru": "Какова ваша цель?", "type": "select", "options": "Increase size,Lift,Lift + augmentation,Reduction"},
        {"id": "size", "question_en": "Desired size change?", "question_tr": "Istenen beden degisikligi?", "question_ru": "Желаемое изменение размера?", "type": "select", "options": "1 cup,2 cups,3+ cups,Natural enhancement"},
        {"id": "implant_type", "question_en": "Implant preference?", "question_tr": "Implant tercihi?", "question_ru": "Предпочтение имплантов?", "type": "select", "options": "Silicone,Saline,Fat transfer,Not sure yet"},
    ],
    "facelift": [
        {"id": "concern", "question_en": "Primary concern?", "question_tr": "Birincil endise?", "question_ru": "Основная проблема?", "type": "select", "options": "Sagging jawline,Nasolabial folds,Neck laxity,Overall aging"},
        {"id": "extent", "question_en": "Desired extent?", "question_tr": "Istenen kapsam?", "question_ru": "Желаемый объём?", "type": "select", "options": "Mini facelift,Full facelift,Lower facelift,Mid-face lift"},
    ],
    "liposuction": [
        {"id": "area", "question_en": "Target area?", "question_tr": "Hedef bolge?", "question_ru": "Целевая зона?", "type": "select", "options": "Abdomen,Love handles,Thighs,Arms,Chin,Multiple areas"},
        {"id": "amount", "question_en": "How much fat to remove?", "question_tr": "Ne kadar yag alinacak?", "question_ru": "Сколько жира удалить?", "type": "select", "options": "Small amount (contouring),Moderate,Significant"},
    ],
    "bbl": [
        {"id": "goal", "question_en": "Desired outcome?", "question_tr": "Istenen sonuc?", "question_ru": "Желаемый результат?", "type": "select", "options": "Natural enhancement,Moderate augmentation,Dramatic change"},
        {"id": "donor", "question_en": "Fat donor areas?", "question_tr": "Yag alim bolgeleri?", "question_ru": "Донорские зоны жира?", "type": "select", "options": "Abdomen,Back,Thighs,Multiple areas"},
    ],
    "bichectomy": [
        {"id": "goal", "question_en": "Desired face shape?", "question_tr": "Istenen yuz sekli?", "question_ru": "Желаемая форма лица?", "type": "select", "options": "Subtle slimming,V-line contour,Defined cheekbones"},
    ],
}

# ---------------------------------------------------------------------------
# Prompt Generation
# ---------------------------------------------------------------------------

def _build_prompt(procedure: str, answers: dict[str, str]) -> str:
    """Build a Meshy.ai-optimized prompt from procedure type and answers."""
    base = "Professional medical photography, realistic medical outcome, high quality clinical result photo"

    prompts: dict[str, str] = {
        "hair_transplant": f"post hair transplant result, natural hairline, {answers.get('grafts', '3000')} grafts {answers.get('method', 'FUE')}, {answers.get('area', 'hairline')} area restored, dense natural growth, male patient",
        "rhinoplasty": f"post rhinoplasty result, refined nose shape, {answers.get('change', 'overall refinement')}, natural proportions, healed result, facial harmony",
        "dental": f"post dental {answers.get('treatment_type', 'veneers')} result, {answers.get('teeth_count', '8')} teeth, {answers.get('shade', 'natural white')} shade, perfect smile, natural looking teeth",
        "breast_augmentation": f"post breast {answers.get('goal', 'augmentation')} result, {answers.get('size', 'natural enhancement')}, {answers.get('implant_type', 'silicone')}, natural proportions, healed clinical result",
        "facelift": f"post facelift result, {answers.get('concern', 'overall aging')} addressed, {answers.get('extent', 'full facelift')}, rejuvenated appearance, natural result",
        "liposuction": f"post liposuction result, {answers.get('area', 'abdomen')} area contoured, {answers.get('amount', 'moderate')} fat removal, toned appearance",
        "bbl": f"post BBL result, {answers.get('goal', 'natural enhancement')}, fat transfer from {answers.get('donor', 'abdomen')}, natural curves, proportional result",
        "bichectomy": f"post bichectomy result, {answers.get('goal', 'subtle slimming')}, refined facial contour, healed clinical result",
    }

    procedure_prompt = prompts.get(procedure, f"post {procedure} medical procedure result, realistic outcome")
    return f"{base}, {procedure_prompt}"


# ---------------------------------------------------------------------------
# Meshy API Calls
# ---------------------------------------------------------------------------

async def get_procedure_questions(category: str) -> list[dict[str, str]]:
    """Return the question set for a procedure category."""
    return PROCEDURE_QUESTIONS.get(category, [])


async def create_visualization(image_base64: str, procedure: str, answers: dict[str, str]) -> dict[str, Any]:
    """Call Meshy.ai image-to-image API to generate visualization."""
    if not MESHY_API_KEY:
        logger.warning("MESHY_API_KEY not set — returning mock response")
        return {
            "result": "mock_task_12345",
            "status": "pending",
            "mock": True,
        }

    prompt = _build_prompt(procedure, answers)

    # Ensure proper data URI prefix
    if not image_base64.startswith("data:"):
        image_base64 = f"data:image/jpeg;base64,{image_base64}"

    payload = {
        "ai_model": "nano-banana-pro",
        "prompt": prompt,
        "reference_image_urls": [image_base64],
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            MESHY_BASE_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {MESHY_API_KEY}",
                "Content-Type": "application/json",
            },
        )
        resp.raise_for_status()
        data = resp.json()

    return data


async def check_status(meshy_task_id: str) -> dict[str, Any]:
    """Poll Meshy.ai for task status."""
    if not MESHY_API_KEY:
        return {
            "id": meshy_task_id,
            "status": "SUCCEEDED",
            "output_urls": ["https://placehold.co/512x512/0891b2/white?text=AI+Result"],
            "mock": True,
        }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(
            f"{MESHY_BASE_URL}/{meshy_task_id}",
            headers={"Authorization": f"Bearer {MESHY_API_KEY}"},
        )
        resp.raise_for_status()
        return resp.json()
