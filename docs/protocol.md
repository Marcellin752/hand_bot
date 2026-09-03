# Serial Protocol

## Payload Format

```
thumb_angle,index_angle,middle_angle,ring_angle,pinky_angle\n
```

- Angles are integers in range `[0, 180]`
- Terminator: `\n` (LF)
- Baudrate: 9600

## Example

```
0,45,90,135,180
```

- `0` — thumb fully extended
- `45` — index half bent
- `90` — middle at 90°
- `135` — ring significantly bent
- `180` — pinky fully closed
