"""
llm_manager.py
Correct Gemini wrapper (2024+ compatible)
"""

import os
from app.utils_cleaner import clean_text
from app.config import GEMINI_KEY

import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

STANDARD_MODEL = os.getenv("GEMINI_STANDARD_MODEL", "gemini-1.5-pro")
REASONING_MODEL = os.getenv("GEMINI_REASON_MODEL", "gemini-1.5-pro")

# ---------------- STANDARD ---------------- #

async def ask_gemini_standard(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(STANDARD_MODEL)
        response = model.generate_content(prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"[Gemini standard error] {e}"

# ---------------- REASONING ---------------- #

async def ask_gemini_reasoning(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(REASONING_MODEL)
        response = model.generate_content(prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"[Gemini reasoning error] {e}"

# ---------------- AUTO ---------------- #

async def ask_gemini(prompt: str, reasoning: bool = False) -> str:
    if reasoning:
        return await ask_gemini_reasoning(prompt)
    return await ask_gemini_standard(prompt)
