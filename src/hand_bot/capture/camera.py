from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import cv2

from hand_bot.config import Settings


class CameraCapture:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._capture: cv2.VideoCapture | None = None

    def open(self) -> None:
        if self._capture is not None:
            return
        cap = cv2.VideoCapture(self._settings.camera_index)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera index {self._settings.camera_index}")
        self._capture = cap

    def close(self) -> None:
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def read(self) -> tuple[bool, Any]:
        if self._capture is None:
            raise RuntimeError("Camera is not open")
        ok, frame = self._capture.read()
        if not ok:
            return False, frame
        if self._settings.frame_mirror:
            frame = cv2.flip(frame, 1)
        return True, frame

    @property
    def is_open(self) -> bool:
        return self._capture is not None and self._capture.isOpened()

    def __enter__(self) -> "CameraCapture":
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @contextmanager
    def frames(self) -> Iterator["CameraCapture"]:
        self.open()
        try:
            yield self
        finally:
            self.close()
