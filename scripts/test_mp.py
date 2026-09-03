from hand_bot.capture.camera import CameraCapture
from hand_bot.config import Settings
from hand_bot.vision.tracker import HandTracker


def main() -> None:
    import cv2

    settings = Settings()
    with CameraCapture(settings).frames() as camera, HandTracker(settings) as tracker:
        while camera.is_open:
            ok, frame = camera.read()
            if not ok:
                break
            for angles in tracker.process(frame):
                h, w = frame.shape[:2]
                for name, value in angles.values.items():
                    cv2.putText(
                        frame,
                        f"{int(round(value))}",
                        (10, 20 + 20 * list(angles.values).index(name)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                    )
            cv2.imshow(settings.window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord(settings.quit_key):
                break


if __name__ == "__main__":
    main()
