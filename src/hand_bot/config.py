from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    camera_index: int = 0
    max_num_hands: int = 1
    min_detection_confidence: float = 0.75
    min_tracking_confidence: float = 0.6
    smoothing_alpha: float = 0.6
    window_name: str = "Robotic Hand Control"
    quit_key: str = "q"
    frame_mirror: bool = True


@dataclass(frozen=True)
class SerialSettings:
    port: str = "/dev/ttyUSB0"
    baudrate: int = 9600
    timeout: float = 0.1
    open_delay: float = 2.0
