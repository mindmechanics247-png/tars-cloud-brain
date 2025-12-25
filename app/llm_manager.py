# app/llm_manager.py
"""
LLaMA (Groq) wrapper
- standard: fast replies
- reasoning: deep reasoning
"""

import os
from groq import Groq
from app.utils_cleaner import clean_text

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")

STANDARD_MODEL = os.getenv("LLAMA_STANDARD_MODEL", "llama3-8b-8192")
REASON_MODEL = os.getenv("LLAMA_REASON_MODEL", "llama3-8b-8192")

client = Groq(api_key=GROQ_API_KEY)


async def ask_llama(prompt: str, reasoning: bool = False) -> str:
    model = REASON_MODEL if reasoning else STANDARD_MODEL

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are TARS, a confident AI assistant designed by ANANT."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
            max_tokens=600,
        )

        text = response.choices[0].message.content
        return clean_text(text)

    except Exception as e:
        return f"[LLaMA error] {e}"
