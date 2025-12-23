from fastapi import APIRouter, Body
from typing import Dict
from app.utils_cleaner import clean_text
from app.memory import append_conversation, save_memory_item
from app.reasoning_engine import generate_response
from app.tools_docstrings import TOOLS

router = APIRouter()

@router.post("/chat")
async def chat_api(payload: Dict = Body(...)):
    q = clean_text(payload.get("query", ""))
    explicit_flag = bool(payload.get("use_reasoning", False))
    append_conversation({"role":"user", "text": q})

    reply, used_reasoning = await generate_response(q, explicit_reasoning=explicit_flag)

    # Attach suggested tools to response (the reasoning may suggest tools; this is a hint)
    # For simplicity: always include tools docstrings so frontend can display tool buttons
    save_memory_item({"text": reply, "meta": {"used_reasoning": used_reasoning}})
    append_conversation({"role":"assistant", "text": reply})

    return {"reply": reply, "used_reasoning": used_reasoning, "tools": TOOLS}
