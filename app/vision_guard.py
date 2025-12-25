import os

VISION_ENABLED = os.getenv("ENABLE_VISION", "false").lower() == "true"

def vision_allowed():
    return VISION_ENABLED
