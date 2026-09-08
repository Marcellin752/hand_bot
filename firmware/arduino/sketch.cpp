#include <Arduino.h>
#include <Servo.h>

const int NUM_SERVOS = 5;
const int SERVO_PINS[NUM_SERVOS] = {5, 6, 9, 10, 11};
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 180;

Servo servos[NUM_SERVOS];

void setup() {
    Serial.begin(9600);
    while (!Serial) {
        delay(100);
    }

    for (int i = 0; i < NUM_SERVOS; i++) {
        servos[i].attach(SERVO_PINS[i]);
        servos[i].write(90);
    }

    delay(1000);
}

void loop() {
    if (Serial.available() < 5) {
        return;
    }

    String line = Serial.readStringUntil('\n');
    line.trim();

    int angles[NUM_SERVOS];
    int count = parseAngles(line, angles);

    if (count == NUM_SERVOS) {
        for (int i = 0; i < NUM_SERVOS; i++) {
            angles[i] = constrain(angles[i], MIN_ANGLE, MAX_ANGLE);
            servos[i].write(angles[i]);
        }
    }
}

int parseAngles(String line, int angles[5]) {
    int index = 0;
    int start = 0;
    int end = line.indexOf(',');

    while (end != -1 && index < NUM_SERVOS) {
        String token = line.substring(start, end);
        angles[index] = token.toInt();
        index++;
        start = end + 1;
        end = line.indexOf(',', start);
    }

    if (index < NUM_SERVOS) {
        String token = line.substring(start);
        angles[index] = token.toInt();
        index++;
    }

    return index;
}