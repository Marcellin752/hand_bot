import cv2

from hand_bot.capture.camera import CameraCapture
from hand_bot.control.mapper import AngleMapper
from hand_bot.control.smoother import AngleSmoother
from hand_bot.io.protocol import build_payload
from hand_bot.io.serial_link import SerialLink
from hand_bot.ui.overlay import OverlayRenderer
from hand_bot.vision.tracker import HandTracker


class ControlPipeline:
    def __init__(
        self,
        capture: CameraCapture,
        tracker: HandTracker,
        serial_link: SerialLink | None,
        smoother: AngleSmoother,
        mapper: AngleMapper,
        overlay: OverlayRenderer,
    ) -> None:
        self._capture = capture
        self._tracker = tracker
        self._serial = serial_link
        self._smoother = smoother
        self._mapper = mapper
        self._overlay = overlay

    def run(self, quit_key: str = "q") -> None:
        self._capture.open()
        try:
            while self._capture.is_open:
                ok, frame = self._capture.read()
                if not ok:
                    break
                for finger_angles in self._tracker.process(frame):
                    smoothed = self._smoother.smooth(finger_angles)
                    mapped = self._mapper.map(smoothed)
                    self._overlay.draw(frame, mapped)
                    payload = build_payload(mapped.as_ordered_list())
                    if self._serial:
                        self._serial.write(payload)
                self._tracker.draw_all(frame)
                cv2.imshow(self._overlay.window_name, frame)
                if cv2.waitKey(1) & 0xFF == ord(quit_key):
                    break
        finally:
            cv2.destroyAllWindows()
            self._capture.close()

    def close(self) -> None:
        if self._serial is not None:
            self._serial.close()
        self._tracker.close()
