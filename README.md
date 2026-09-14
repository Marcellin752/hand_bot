# hand-bot

Vision-driven robotic hand controller using MediaPipe Hands and serial communication.
Project developed as part of the TEKBOT EPITECH association.

## Setup

### Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### ESP32 Firmware (PlatformIO)

```bash
cd firmware
platformio run
platformio device monitor --baud 9600
# or with Arduino IDE:
# Open firmware/arduino/sketch.cpp → select "ESP32 Dev Module" → upload
```

### Documentation

- [Wiring diagram](docs/wiring.md) - GPIO pinout and connections
- [Serial protocol](docs/protocol.md) - Data format and examples

## Usage

```bash
python scripts/run.py
```

## Scripts

| Script | Description |
|---|---|
| `scripts/run.py` | Main controller (camera → tracker → serial) |
| `scripts/test_cam.py` | Camera access test |
| `scripts/test_mp.py` | MediaPipe hand tracking test |

## Architecture

```
camera → vision (angles) → control (smoothing, mapping) → io (serial) → ESP32 → servos
```

## Configuration

Edit `src/hand_bot/config.py` to change serial port, camera index, and smoothing parameters.