"""
vision_engine.py
Hybrid vision: OpenCV preprocessing -> MediaPipe hands -> YOLO fallback.
Provides analyze_frame_bytes(frame_bytes) for endpoints and tools.
Safe: no face identification, only presence/gesture and object labels.
"""

import cv2
import numpy as np
import base64
import os
from typing import Dict, Any
from app.config import YOLO_MODEL_PATH
from app.utils_cleaner import clean_text

# MediaPipe setup (fast hand detection)
try:
    import mediapipe as mp
    mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils
except Exception:
    mp_hands = None
    mp_draw = None

# YOLO (ultralytics) optional
YoloModel = None
try:
    from ultralytics import YOLO
    # If provided model path exists use it, else let ultralytics fetch default
    if YOLO_MODEL_PATH and os.path.exists(YOLO_MODEL_PATH):
        YoloModel = YOLO(YOLO_MODEL_PATH)
    else:
        YoloModel = YOLO("yolov8n.pt")
except Exception:
    YoloModel = None

def _bytes_to_image(frame_bytes: bytes):
    nparr = np.frombuffer(frame_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def _mediapipe_hands_summary(img) -> Dict[str, Any]:
    """Return hand detection summary using MediaPipe (landmarks count, handedness if available)."""
    if mp_hands is None:
        return {"hands": [], "hands_count": 0}
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = mp_hands.process(rgb)
    hands = []
    if res.multi_hand_landmarks:
        for idx, lm in enumerate(res.multi_hand_landmarks):
            hands.append({"landmarks_count": len(lm.landmark)})
    return {"hands": hands, "hands_count": len(hands)}

def _yolo_objects_summary(img) -> Dict[str, Any]:
    """Return YOLO detections: name + confidence list. If YOLO not available, return []."""
    dets = []
    if YoloModel is None:
        return {"objects": []}
    try:
        results = YoloModel(img, verbose=False)
        for r in results:
            boxes = getattr(r, "boxes", None)
            if boxes:
                for b in boxes:
                    try:
                        cls_idx = int(b.cls[0].item())
                        name = r.names.get(cls_idx, str(cls_idx))
                        conf = float(b.conf[0].item())
                        dets.append({"name": clean_text(name), "confidence": round(conf, 3)})
                    except Exception:
                        continue
    except Exception:
        return {"objects": []}
    return {"objects": dets}

def analyze_frame_bytes(frame_bytes: bytes) -> Dict[str, Any]:
    """
    Full analysis entrypoint.
    Returns:
      - gesture token (simple)
      - hands_count
      - objects (from YOLO)
      - image_preview_b64 (small)
    """
    img = _bytes_to_image(frame_bytes)
    if img is None:
        return {"error": "could not decode image"}

    # Resize for speed (maintain aspect ratio)
    h, w = img.shape[:2]
    scale = 640 / max(w, h) if max(w, h) > 640 else 1.0
    small = cv2.resize(img, None, fx=scale, fy=scale)

    # MediaPipe simple hand detection
    hands_info = _mediapipe_hands_summary(small)
    gesture_token = "none"
    if hands_info["hands_count"] > 0:
        gesture_token = "hand_detected"

    # YOLO objects fallback
    yolo_info = _yolo_objects_summary(small)
    objects = yolo_info.get("objects", [])

    # Create base64 preview for UI (small JPEG)
    _, buf = cv2.imencode(".jpg", small, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
    preview_b64 = base64.b64encode(buf).decode("ascii")

    return {
        "gesture": gesture_token,
        "hands_count": hands_info["hands_count"],
        "objects": objects,
        "image_preview_b64": preview_b64
    }
