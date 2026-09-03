import numpy as np
import pytest

from hand_bot.vision.angles import calculate_angle, to_servo_angle


class TestCalculateAngle:
    def test_straight_angle_returns_180(self):
        a = np.array([0.0, 0.0])
        b = np.array([1.0, 0.0])
        c = np.array([2.0, 0.0])
        angle = calculate_angle(a, b, c)
        assert angle == pytest.approx(180.0, abs=1e-6)

    def test_right_angle(self):
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 0.0])
        c = np.array([0.0, 1.0])
        angle = calculate_angle(a, b, c)
        assert angle == pytest.approx(90.0, abs=1e-6)

    def test_colinear_points(self):
        a = np.array([0.0, 0.0, 0.0])
        b = np.array([1.0, 0.0, 0.0])
        c = np.array([2.0, 0.0, 0.0])
        angle = calculate_angle(a, b, c)
        assert angle == pytest.approx(180.0, abs=1e-6)

    def test_60_degree(self):
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 0.0])
        c = np.array([0.5, np.sqrt(3) / 2])
        angle = calculate_angle(a, b, c)
        assert angle == pytest.approx(60.0, abs=1e-6)

    def test_zero_vector_a_returns_zero(self):
        a = np.array([0.0, 0.0])
        b = np.array([0.0, 0.0])
        c = np.array([1.0, 0.0])
        angle = calculate_angle(a, b, c)
        assert angle == 0.0


class TestToServoAngle:
    def test_straight_returns_zero(self):
        assert to_servo_angle(180.0) == pytest.approx(0.0)

    def test_bent_returns_high(self):
        assert to_servo_angle(0.0) == pytest.approx(180.0)

    def test_mid_bent(self):
        result = to_servo_angle(90.0)
        assert result == pytest.approx(90.0)

    def test_clamp_above_180(self):
        assert to_servo_angle(200.0) == pytest.approx(0.0)

    def test_clamp_below_zero(self):
        assert to_servo_angle(-10.0) == pytest.approx(180.0)
