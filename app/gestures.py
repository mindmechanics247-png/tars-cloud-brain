"""
gestures.py
Map vision tokens and hand landmarks to high-level gestures/actions.
This is intentionally simple: use MediaPipe landmarks later to refine gestures.
"""

from typing import Dict

# Basic mapping: token -> action
TOKEN_ACTION_MAP = {
    "hand_detected": "ACTIVATE_LISTENING",
    "none": "NO_ACTION"
}

def map_gesture_token(token: str) -> str:
    return TOKEN_ACTION_MAP.get(token, "NO_ACTION")

# Expand later: parse landmark arrays to detect pinch, point, swipe, etc.
def landmark_to_gesture(landmarks) -> Dict:
    """
    Placeholder for landmark->gesture detection logic.
    landmarks: list of normalized landmarks from MediaPipe.
    Returns example:
      {"gesture": "pinch", "confidence":0.92}
    """
    # For now return None (not implemented). We keep placeholder for future upgrade.
    return {"gesture": None, "confidence": 0.0}
