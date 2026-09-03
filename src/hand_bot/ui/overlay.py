from typing import Any

import cv2

from hand_bot.config import Settings
from hand_bot.vision.tracker import FingerAngles


class OverlayRenderer:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._mp_hands = None
        try:
            import mediapipe as mp
            self._mp_hands = mp.solutions.hands
        except ImportError:
            pass

    @property
    def window_name(self) -> str:
        return self._settings.window_name

    def draw(self, frame: Any, angles: FingerAngles) -> None:
        h, w = frame.shape[:2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        for i, (name, value) in enumerate(angles.values.items()):
            x = int(0.02 * w)
            y = int((0.95 - i * 0.05) * h)
            cv2.putText(frame, f"{name}: {int(round(value))}", (x, y), font, 0.5, (0, 255, 0), 2)

    def draw_landmarks(self, frame: Any, hand_landmarks: object) -> None:
        if self._mp_hands is None:
            return
        mp_draw = self._mp_hands.solutions.drawing_utils  # type: ignore[attr-defined]
        mp_draw.draw_landmarks(frame, hand_landmarks, self._mp_hands.HAND_CONNECTIONS)
