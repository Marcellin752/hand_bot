# Wiring

## ESP32 DevKit + Servos

### GPIO Pins

| Finger | GPIO |
|---|---|
| Thumb | 18 |
| Index | 19 |
| Middle | 21 |
| Ring | 22 |
| Pinky | 23 |

> Note: GPIO 6–11 are wired to the ESP32 internal SPI flash and must not be
> used as servo outputs.

### Connections

- ESP32 DevKit → Servo signal (orange/yellow) → GPIO pins above
- ESP32 5V → Servo VCC (red)
- ESP32 GND → Servo GND (brown)

### Baudrate

9600 baud, 8N1.

## Serial Protocol

```
thumb,index,middle,ring,pinky\n
```

Example: `0,45,90,135,180`