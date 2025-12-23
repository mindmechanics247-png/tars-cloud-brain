# agent/reasoning.py
"""
reasoning.py
Simple wrapper class for calling Gemini models:
- chat(prompt) -> quick response (standard model)
- reason(prompt) -> longer/step-by-step response (reasoning model)
"""

import os
import asyncio
from typing import Optional

from app.utils_cleaner import clean_text  # reuse utils from app
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_STANDARD_MODEL = os.getenv("GEMINI_STANDARD_MODEL", "gemini-1.5-flash")
GEMINI_REASON_MODEL = os.getenv("GEMINI_REASON_MODEL", "gemini-2.0-flash-thinking")

# try import google generative ai
GEMINI_AVAILABLE = False
try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_KEY)
    GEMINI_AVAILABLE = bool(GEMINI_KEY)
except Exception:
    GEMINI_AVAILABLE = False

class ReasoningEngine:
    def __init__(self, standard_model: Optional[str] = None, reason_model: Optional[str] = None):
        self.standard = standard_model or GEMINI_STANDARD_MODEL
        self.reason = reason_model or GEMINI_REASON_MODEL

    async def _call_gemini(self, model: str, prompt: str, max_output_tokens: int = 512) -> str:
        if not GEMINI_AVAILABLE:
            return "[Gemini not available: check GOOGLE_API_KEY]"
        try:
            # adapt to common genai shapes
            resp = genai.generate_text(model=model, input=prompt, max_output_tokens=max_output_tokens)
            # attempt to extract text
            out = getattr(resp, "text", None)
            if out:
                return clean_text(out)
            # older versions: dict with candidates
            if isinstance(resp, dict):
                cands = resp.get("candidates")
                if cands and isinstance(cands, list):
                    return clean_text(cands[0].get("content") or cands[0].get("message") or str(cands[0]))
            return clean_text(str(resp))
        except Exception as e:
            return f"[Gemini error] {e}"

    def chat(self, prompt: str) -> str:
        """
        Synchronous-friendly wrapper for a short reply.
        Note: it's safe to call from async or sync contexts; we run event loop if needed.
        """
        coro = self._call_gemini(self.standard, prompt, max_output_tokens=300)
        try:
            return asyncio.get_event_loop().run_until_complete(coro)
        except RuntimeError:
            # if called inside running loop (e.g., agent runtime), return coroutine to be awaited by caller
            return coro

    def reason(self, prompt: str) -> str:
        """
        Use reasoning model for step-by-step output.
        """
        p = f"Reason step-by-step and return clear plan + final answer.\nUser: {prompt}\n\nSteps:"
        coro = self._call_gemini(self.reason, p, max_output_tokens=800)
        try:
            return asyncio.get_event_loop().run_until_complete(coro)
        except RuntimeError:
            return coro
