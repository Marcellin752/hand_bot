def build_payload(values: list[float], terminator: str = "\n") -> str:
    return ",".join(str(int(round(v))) for v in values) + terminator


def parse_payload(payload: str) -> list[int]:
    cleaned = payload.strip()
    if not cleaned:
        return []
    return [int(part) for part in cleaned.split(",")]
