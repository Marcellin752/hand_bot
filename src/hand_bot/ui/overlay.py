from typing import Any

import cv2

from hand_bot.config import Settings
from hand_bot.vision.tracker import FingerAngles


class OverlayRenderer:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

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
