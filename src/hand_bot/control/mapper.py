from hand_bot.vision.tracker import FingerAngles


class AngleMapper:
    def __init__(
        self,
        raw_min: float = 0.0,
        raw_max: float = 180.0,
        servo_min: float = 0.0,
        servo_max: float = 180.0,
    ) -> None:
        self._raw_min = raw_min
        self._raw_max = raw_max
        self._servo_min = servo_min
        self._servo_max = servo_max

    def map(self, angles: FingerAngles) -> FingerAngles:
        factor = (self._servo_max - self._servo_min) / (self._raw_max - self._raw_min)
        mapped = {
            name: self._servo_min + (val - self._raw_min) * factor
            for name, val in angles.values.items()
        }
        return FingerAngles(values=mapped)


class PerFingerMapper:
    def __init__(self, finger_configs: dict[str, tuple[float, float]]) -> None:
        self._configs = finger_configs

    def map(self, angles: FingerAngles) -> FingerAngles:
        mapped: dict[str, float] = {}
        for name, val in angles.values.items():
            raw_min, raw_max = self._configs.get(name, (0.0, 180.0))
            factor = 180.0 / (raw_max - raw_min)
            mapped[name] = max(0.0, min(180.0, (val - raw_min) * factor))
        return FingerAngles(values=mapped)
