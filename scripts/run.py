from hand_bot.capture.camera import CameraCapture
from hand_bot.config import SerialSettings, Settings
from hand_bot.control.mapper import AngleMapper
from hand_bot.control.pipeline import ControlPipeline
from hand_bot.control.smoother import AngleSmoother
from hand_bot.io.serial_link import SerialLink
from hand_bot.ui.overlay import OverlayRenderer
from hand_bot.vision.tracker import HandTracker


def build_pipeline(
    settings: Settings | None = None,
    serial_settings: SerialSettings | None = None,
) -> ControlPipeline:
    cfg = settings or Settings()
    serial_cfg = serial_settings or SerialSettings()
    serial_link = SerialLink(serial_cfg)
    serial_link.open()
    return ControlPipeline(
        capture=CameraCapture(cfg),
        tracker=HandTracker(cfg),
        serial_link=serial_link if serial_link.is_open else None,
        smoother=AngleSmoother(alpha=cfg.smoothing_alpha),
        mapper=AngleMapper(),
        overlay=OverlayRenderer(cfg),
    )


def main() -> None:
    pipeline = build_pipeline()
    try:
        pipeline.run()
    finally:
        pipeline._tracker.close()


if __name__ == "__main__":
    main()
