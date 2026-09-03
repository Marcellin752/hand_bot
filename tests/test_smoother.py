import pytest

from hand_bot.control.smoother import AngleSmoother, MovingAverageSmoother
from hand_bot.vision.tracker import FingerAngles


class TestAngleSmoother:
    def test_first_frame_no_smoothing(self):
        smoother = AngleSmoother(alpha=0.6)
        angles = FingerAngles(values={"index": 90.0, "middle": 45.0})
        result = smoother.smooth(angles)
        assert result.values["index"] == 90.0

    def test_smoothing_applied(self):
        smoother = AngleSmoother(alpha=0.5)
        angles1 = FingerAngles(values={"index": 0.0})
        angles2 = FingerAngles(values={"index": 100.0})
        smoother.smooth(angles1)
        result = smoother.smooth(angles2)
        assert 25.0 < result.values["index"] < 75.0

    def test_reset(self):
        smoother = AngleSmoother(alpha=0.6)
        smoother.smooth(FingerAngles(values={"index": 50.0}))
        smoother.reset()
        assert smoother._prev is None


class TestMovingAverageSmoother:
    def test_single_value(self):
        smoother = MovingAverageSmoother(window_size=3)
        angles = FingerAngles(values={"index": 50.0})
        result = smoother.smooth(angles)
        assert result.values["index"] == 50.0

    def test_average_window(self):
        smoother = MovingAverageSmoother(window_size=3)
        smoother.smooth(FingerAngles(values={"index": 0.0}))
        smoother.smooth(FingerAngles(values={"index": 60.0}))
        result = smoother.smooth(FingerAngles(values={"index": 120.0}))
        assert result.values["index"] == pytest.approx(60.0)
