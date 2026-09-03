# hand-bot

Vision-driven robotic hand controller using MediaPipe Hands and serial communication.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

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
camera → vision (angles) → control (smoothing, mapping) → io (serial) → arduino
```

## Configuration

Edit `src/hand_bot/config.py` to change serial port, camera index, and smoothing parameters.