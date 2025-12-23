"""
mcp_client.py
Lightweight MCP client stub to send events to an MCP-compatible server (e.g., N8N).
This is a simple HTTP POST helper — your N8N workflow should expose a webhook to receive events.
"""

import requests
import os
from app.config import SERP_KEY  # reuse config for any keys; change variable if needed

# Example: set N8N webhook URL in .env as N8N_WEBHOOK_URL
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")

def send_to_n8n(event_name: str, payload: dict):
    """
    POST to N8N webhook (if configured).
    """
    if not N8N_WEBHOOK_URL:
        return {"sent": False, "reason": "N8N_WEBHOOK_URL not set"}
    try:
        r = requests.post(N8N_WEBHOOK_URL, json={"event": event_name, "payload": payload}, timeout=8)
        return {"sent": True, "status_code": r.status_code, "resp": r.text}
    except Exception as e:
        return {"sent": False, "error": str(e)}
