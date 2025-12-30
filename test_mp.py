#!/usr/bin/env python3
##
## EPITECH PROJECT, 2025
## Handbot
## File description:
## test cam
##

import cv2
import mediapipe as mp
import numpy as np

def calcul_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    v_ba = a - b
    v_bc = c - b

    cos_angle = np.dot(v_ba, v_bc) / (np.linalg.norm(v_ba) * np.linalg.norm(v_bc))
    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    angle = np.arccos(cos_angle)
    return np.degrees(angle)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No access to the camera")
    exit()

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        print("Error: No flux")
        break
    h, w, _ = frame.shape
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            doigts_points = {
                "Pouce": (2, 3, 4),
                "Index": (5, 6, 7),
                "Majeur": (9, 10, 11),
                "Annul": (13, 14, 15),
                "Auri": (17, 18, 19)
                }
            for i, (nom, pts) in enumerate(doigts_points.items()):
                p1 = [lm[pts[0]].x, lm[pts[0]].y]
                p2 = [lm[pts[1]].x, lm[pts[1]].y]
                p3 = [lm[pts[2]].x, lm[pts[2]].y]

                angle = calcul_angle(p1, p2, p3)
                pos_txt = (int(lm[pts[1]].x * w), int(lm[pts[1]].y * h) - 10)
                cv2.putText(frame, f"{angle} deg", pos_txt,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
