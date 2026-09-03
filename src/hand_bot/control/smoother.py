from collections import deque

from hand_bot.vision.tracker import FingerAngles


class AngleSmoother:
    def __init__(self, alpha: float = 0.6) -> None:
        self._alpha = alpha
        self._prev: dict[str, float] | None = None

    def smooth(self, angles: FingerAngles) -> FingerAngles:
        if self._prev is None:
            self._prev = dict(angles.values)
            return angles
        smoothed: dict[str, float] = {}
        for name, value in angles.values.items():
            prev = self._prev[name]
            smoothed[name] = self._alpha * value + (1.0 - self._alpha) * prev
        self._prev = smoothed
        return FingerAngles(values=smoothed)

    def reset(self) -> None:
        self._prev = None


class MovingAverageSmoother:
    def __init__(self, window_size: int = 5) -> None:
        self._window_size = window_size
        self._buffers: dict[str, deque[float]] | None = None

    def smooth(self, angles: FingerAngles) -> FingerAngles:
        if self._buffers is None:
            self._buffers = {name: deque(maxlen=self._window_size) for name in angles.values}
        for name, value in angles.values.items():
            self._buffers[name].append(value)
        return FingerAngles(values={name: sum(buf) / len(buf) for name, buf in self._buffers.items()})

    def reset(self) -> None:
        self._buffers = None
