# agent/tools_n8n.py
"""
tools_n8n.py
Sends an event (payload) to an N8N webhook. The webhook triggers your no-code flows.
"""

import os
import requests
from typing import Dict

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")

def trigger_n8n(event_name: str, payload: Dict) -> Dict:
    """
    Send event to N8N webhook. Returns {sent: bool, status_code/int or error}
    """
    if not N8N_WEBHOOK_URL:
        return {"sent": False, "error": "N8N_WEBHOOK_URL not configured"}
    try:
        body = {"event": event_name, "payload": payload}
        r = requests.post(N8N_WEBHOOK_URL, json=body, timeout=10)
        return {"sent": True, "status_code": r.status_code, "response": r.text}
    except Exception as e:
        return {"sent": False, "error": str(e)}
