
from hand_bot.vision.tracker import FingerAngles


class TestFingerAngles:
    def test_as_ordered_list(self):
        angles = FingerAngles(
            values={"thumb": 0.0, "index": 45.0, "middle": 90.0, "ring": 135.0, "pinky": 180.0},
        )
        result = angles.as_ordered_list()
        assert result == [0.0, 45.0, 90.0, 135.0, 180.0]

    def test_as_ordered_dict(self):
        angles = FingerAngles(
            values={"thumb": 0.0, "index": 45.0, "middle": 90.0, "ring": 135.0, "pinky": 180.0},
        )
        result = angles.as_ordered_dict()
        assert list(result.keys()) == ["thumb", "index", "middle", "ring", "pinky"]
        assert result["index"] == 45.0
