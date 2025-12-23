import cv2
import mediapipe as mp
from ultralytics import YOLO

class VisionProcessor:
    """
    Vision system for TARS
    - OpenCV: camera handling
    - MediaPipe: hand detection
    - YOLO (hook): object detection (on demand)
    """

    def __init__(self, yolo_model_path="yolov8n.pt", enable_yolo=False):
        # MediaPipe (hands)
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        self.drawer = mp.solutions.drawing_utils

        # YOLO
        self.enable_yolo = enable_yolo
        self.yolo = YOLO(yolo_model_path) if enable_yolo else None

    def process_frame(self, frame):
        """
        Normal frame processing (hands only)
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                self.drawer.draw_landmarks(
                    frame,
                    hand,
                    mp.solutions.hands.HAND_CONNECTIONS
                )
        return frame

    def detect_objects(self, frame):
        """
        🟡 YOLO HOOK
        Detect objects only when this function is called
        """
        if not self.enable_yolo or self.yolo is None:
            return []

        results = self.yolo(frame, verbose=False)
        detections = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.yolo.names[cls_id]
                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    "label": label,
                    "confidence": round(conf, 2),
                    "bbox": [x1, y1, x2, y2]
                })

                # draw box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        return detections
