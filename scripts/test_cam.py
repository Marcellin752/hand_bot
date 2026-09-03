from hand_bot.capture.camera import CameraCapture
from hand_bot.config import Settings


def main() -> None:
    import cv2

    settings = Settings()
    with CameraCapture(settings).frames() as camera:
        while camera.is_open:
            ok, frame = camera.read()
            if not ok:
                print("No frame received.")
                break
            cv2.imshow(settings.window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord(settings.quit_key):
                break


if __name__ == "__main__":
    main()
