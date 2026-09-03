import numpy as np
from numpy.typing import NDArray


def calculate_angle(
    a: NDArray[np.float64],
    b: NDArray[np.float64],
    c: NDArray[np.float64],
) -> float:
    ba = a - b
    bc = c - b
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    if norm_ba == 0 or norm_bc == 0:
        return 0.0
    cosine = np.dot(ba, bc) / (norm_ba * norm_bc)
    cosine = float(np.clip(cosine, -1.0, 1.0))
    return float(np.degrees(np.arccos(cosine)))


def to_servo_angle(raw_angle: float) -> float:
    clamped = float(np.clip(raw_angle, 0.0, 180.0))
    return float(np.clip(180.0 - clamped, 0.0, 180.0))
