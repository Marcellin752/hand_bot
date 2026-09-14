from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

import cv2
import mediapipe as mp
import numpy as np

from hand_bot.config import Settings
from hand_bot.vision.angles import calculate_angle, to_servo_angle
from hand_bot.vision.landmarks import FINGER_LANDMARKS, FINGER_ORDER

HandLandmarks = Any


@dataclass(frozen=True)
class FingerAngles:
    values: dict[str, float]

    def as_ordered_list(self, order: tuple[str, ...] = FINGER_ORDER) -> list[float]:
        return [self.values[name] for name in order]

    def as_ordered_dict(self, order: tuple[str, ...] = FINGER_ORDER) -> dict[str, float]:
        return {name: self.values[name] for name in order}


class HandTracker:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._mp_hands = mp.solutions.hands
        self._mp_draw = mp.solutions.drawing_utils
        self._hands = self._mp_hands.Hands(
            max_num_hands=settings.max_num_hands,
            min_detection_confidence=settings.min_detection_confidence,
            min_tracking_confidence=settings.min_tracking_confidence,
        )
        self._last_results: Any = None

    def close(self) -> None:
        self._hands.close()

    def __enter__(self) -> "HandTracker":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def process(self, frame_bgr: Any) -> Iterator[FingerAngles]:
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        self._last_results = self._hands.process(rgb)
        if not self._last_results.multi_hand_landmarks:
            return iter(())
        for hand_landmarks in self._last_results.multi_hand_landmarks:
            yield self._extract(hand_landmarks)

    def draw_all(self, frame_bgr: Any) -> None:
        if not self._last_results or not self._last_results.multi_hand_landmarks:
            return
        for hand_landmarks in self._last_results.multi_hand_landmarks:
            self.draw(frame_bgr, hand_landmarks)

    def draw(self, frame_bgr: Any, hand_landmarks: HandLandmarks) -> None:
        self._mp_draw.draw_landmarks(
            frame_bgr,
            hand_landmarks,
            self._mp_hands.HAND_CONNECTIONS,
        )

    def _extract(self, hand_landmarks: HandLandmarks) -> FingerAngles:
        lm = hand_landmarks.landmark
        values: dict[str, float] = {}
        for name, (a, b, c) in FINGER_LANDMARKS.items():
            p1 = np.asarray([lm[a].x, lm[a].y], dtype=np.float64)
            p2 = np.asarray([lm[b].x, lm[b].y], dtype=np.float64)
            p3 = np.asarray([lm[c].x, lm[c].y], dtype=np.float64)
            raw = calculate_angle(p1, p2, p3)
            values[name] = to_servo_angle(raw)
        return FingerAngles(values=values)
