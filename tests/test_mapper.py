
from hand_bot.control.mapper import AngleMapper, PerFingerMapper
from hand_bot.vision.tracker import FingerAngles


class TestAngleMapper:
    def test_identity(self):
        mapper = AngleMapper(raw_min=0.0, raw_max=180.0, servo_min=0.0, servo_max=180.0)
        angles = FingerAngles(values={"index": 90.0})
        result = mapper.map(angles)
        assert result.values["index"] == 90.0

    def test_scaling(self):
        mapper = AngleMapper(raw_min=0.0, raw_max=180.0, servo_min=0.0, servo_max=90.0)
        angles = FingerAngles(values={"index": 90.0})
        result = mapper.map(angles)
        assert result.values["index"] == 45.0

    def test_offset(self):
        mapper = AngleMapper(raw_min=0.0, raw_max=180.0, servo_min=10.0, servo_max=170.0)
        angles = FingerAngles(values={"index": 90.0})
        result = mapper.map(angles)
        assert result.values["index"] == 90.0


class TestPerFingerMapper:
    def test_per_finger_config(self):
        mapper = PerFingerMapper(finger_configs={"index": (20.0, 160.0)})
        angles = FingerAngles(values={"index": 90.0})
        result = mapper.map(angles)
        assert 0.0 <= result.values["index"] <= 180.0

    def test_unknown_finger_default(self):
        mapper = PerFingerMapper(finger_configs={})
        angles = FingerAngles(values={"index": 90.0})
        result = mapper.map(angles)
        assert result.values["index"] == 90.0
