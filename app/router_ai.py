from fastapi import APIRouter, Body
from typing import Dict

from app.utils_cleaner import clean_text
from app.memory import append_conversation, save_memory_item
from app.reasoning_engine import generate_response
from app.tools_docstrings import TOOLS

router = APIRouter()


@router.post("/chat")
async def chat_api(payload: Dict = Body(...)):
    """
    REST chat endpoint for TARS (used by Android app or curl).
    """
    user_text = clean_text(payload.get("message", ""))
    explicit_flag = bool(payload.get("use_reasoning", False))

    if not user_text:
        return {"reply": "Please say something.", "used_reasoning": False}

    # Save user message
    append_conversation({"role": "user", "text": user_text})

    # Generate response
    reply, used_reasoning = await generate_response(
        user_text,
        explicit_reasoning=explicit_flag,
    )

    # Save assistant reply
    save_memory_item({
        "text": reply,
        "meta": {"used_reasoning": used_reasoning},
    })
    append_conversation({"role": "assistant", "text": reply})

    return {
        "reply": reply,
        "used_reasoning": used_reasoning,
        "tools": TOOLS,
    }
