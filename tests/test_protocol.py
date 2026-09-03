
from hand_bot.io.protocol import build_payload, parse_payload


class TestBuildPayload:
    def test_five_values(self):
        payload = build_payload([0, 45, 90, 135, 180])
        assert payload == "0,45,90,135,180\n"

    def test_integer_conversion(self):
        payload = build_payload([10.7, 89.4, 170.3])
        assert payload == "11,89,170\n"

    def test_custom_terminator(self):
        payload = build_payload([0, 90, 180], terminator="\r\n")
        assert payload == "0,90,180\r\n"


class TestParsePayload:
    def test_parse_valid(self):
        result = parse_payload("10,45,90,135,180\n")
        assert result == [10, 45, 90, 135, 180]

    def test_parse_with_spaces(self):
        result = parse_payload(" 10 , 45 , 90 ")
        assert result == [10, 45, 90]

    def test_parse_empty(self):
        assert parse_payload("") == []
        assert parse_payload("   \n") == []

    def test_roundtrip(self):
        original = [0, 90, 135, 180, 45]
        payload = build_payload(original)
        parsed = parse_payload(payload)
        assert parsed == original
