#!/usr/bin/env python3
##
## EPITECH PROJECT, 2025
## Handbot
## File description:
## tests
##

import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No access to the camera")
    exit()

print("It is Ok, Camera activated")

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        print("Error: No flux")
        break
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
