from hand_bot.config import SerialSettings

try:
    import serial
except ImportError:  # pragma: no cover
    serial = None  # type: ignore[assignment]


class SerialLink:
    def __init__(self, settings: SerialSettings) -> None:
        self._settings = settings
        self._handle = None

    def open(self) -> bool:
        if serial is None:
            print("pyserial not installed; serial link disabled.")
            return False
        try:
            self._handle = serial.Serial(
                port=self._settings.port,
                baudrate=self._settings.baudrate,
                timeout=self._settings.timeout,
            )
            import time
            time.sleep(self._settings.open_delay)
            print(f"Serial connection established on {self._settings.port}")
            return True
        except Exception as exc:
            print(f"Serial connection error: {exc}")
            self._handle = None
            return False

    def close(self) -> None:
        if self._handle is not None:
            try:
                self._handle.close()
            except Exception:
                pass
            self._handle = None

    def write(self, payload: str) -> bool:
        if self._handle is None:
            return False
        try:
            self._handle.write(payload.encode("utf-8"))
            return True
        except Exception as exc:
            print(f"Serial write error: {exc}")
            return False

    @property
    def is_open(self) -> bool:
        return self._handle is not None

    def __enter__(self) -> "SerialLink":
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
