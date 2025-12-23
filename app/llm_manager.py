"""
llm_manager.py
Cloud Gemini wrapper for two-model setup:
- ask_gemini_standard: fast/short answers (gemini-1.5-flash or your choosing)
- ask_gemini_reasoning: deep reasoning (gemini-2.0-flash-thinking or your choosing)
Uses google.generativeai client if available.
"""

import asyncio
import os
from typing import Optional
from app.config import GEMINI_KEY
from app.utils_cleaner import clean_text

# Safe import block
GEMINI_AVAILABLE = False
try:
    import google.generativeai as genai  # pip package: google-generativeai
    genai.configure(api_key=GEMINI_KEY)
    GEMINI_AVAILABLE = bool(GEMINI_KEY)
except Exception:
    GEMINI_AVAILABLE = False

# Default model names (you can override in .env/config)
STANDARD_MODEL = os.getenv("GEMINI_STANDARD_MODEL", "models/text-bison-001")  # quick chat
REASONING_MODEL = os.getenv("GEMINI_REASON_MODEL", "models/text-bison-001")    # replace with reasoning model if available

async def ask_gemini_standard(prompt: str, max_tokens: int = 512) -> str:
    """
    Short/fast answer using the standard Gemini model.
    """
    if not GEMINI_AVAILABLE:
        return "[Gemini unavailable] Please set GEMINI_API_KEY in .env"
    try:
        # Use genai.generate_text or genai.Model.generate depending on package version
        response = genai.generate_text(model=STANDARD_MODEL, input=prompt, max_output_tokens=max_tokens)
        # response shape may differ by version. Try common fields:
        text = getattr(response, "text", None) or (response.get("candidates")[0].get("content") if isinstance(response, dict) and response.get("candidates") else str(response))
        return clean_text(text)
    except Exception as e:
        return f"[Gemini standard error] {e}"

async def ask_gemini_reasoning(prompt: str, max_tokens: int = 1024) -> str:
    """
    Longer, chain-of-thought style generation using the reasoning model.
    """
    if not GEMINI_AVAILABLE:
        return "[Gemini unavailable] Please set GEMINI_API_KEY in .env"
    try:
        response = genai.generate_text(model=REASONING_MODEL, input=prompt, max_output_tokens=max_tokens)
        text = getattr(response, "text", None) or (response.get("candidates")[0].get("content") if isinstance(response, dict) and response.get("candidates") else str(response))
        return clean_text(text)
    except Exception as e:
        return f"[Gemini reasoning error] {e}"

# Optional helper that tries reasoning first, falls back to standard.
async def ask_gemini(prompt: str, reasoning: bool = False) -> str:
    if reasoning:
        return await ask_gemini_reasoning(prompt)
    return await ask_gemini_standard(prompt)
