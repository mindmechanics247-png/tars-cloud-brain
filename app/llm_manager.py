"""
llm_manager.py
Gemini wrapper (SDK ≥ 0.7.x compatible)
"""

import os
from app.config import GEMINI_KEY
from app.utils_cleaner import clean_text

import google.generativeai as genai

genai.configure(api_key=GEMINI_KEY)

STANDARD_MODEL = os.getenv("GEMINI_STANDARD_MODEL", "gemini-1.5-flash")
REASONING_MODEL = os.getenv("GEMINI_REASON_MODEL", "gemini-1.5-pro")


async def _ask(model_name: str, prompt: str, max_tokens: int):
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": 0.6,
            },
        )
        return clean_text(response.text)
    except Exception as e:
        return f"[Gemini error] {e}"


async def ask_gemini_standard(prompt: str, max_tokens: int = 512):
    return await _ask(STANDARD_MODEL, prompt, max_tokens)


async def ask_gemini_reasoning(prompt: str, max_tokens: int = 1024):
    return await _ask(REASONING_MODEL, prompt, max_tokens)


async def ask_gemini(prompt: str, reasoning: bool = False):
    return await (
        ask_gemini_reasoning(prompt)
        if reasoning
        else ask_gemini_standard(prompt)
    )
