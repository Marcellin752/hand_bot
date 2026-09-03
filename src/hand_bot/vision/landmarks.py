from typing import Final

FINGER_LANDMARKS: Final[dict[str, tuple[int, int, int]]] = {
    "thumb": (2, 3, 4),
    "index": (5, 6, 7),
    "middle": (9, 10, 11),
    "ring": (13, 14, 15),
    "pinky": (17, 18, 19),
}

FINGER_ORDER: Final[tuple[str, ...]] = ("thumb", "index", "middle", "ring", "pinky")
