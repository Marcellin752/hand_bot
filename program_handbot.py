#!/usr/bin/env python3
##
## EPITECH PROJECT, 2025
## HANDBOT
## File description:
## HANDBOT
##

import cv2
import mediapipe as mp
import numpy as np
import serial
import time

# --- BLUETOOTH CONFIGURATION ---
try:
    #'COM10' à remplacer par le port Bluetooth série sortant du PC
    bluetooth_port = 'COM10' 
    arduino = serial.Serial(port=bluetooth_port, baudrate=9600, timeout=0.1)
    time.sleep(2) # Attente de l'initialisation du module
    print(f"Connexion établie sur {bluetooth_port}")
except Exception as e:
    arduino = None
    print(f"Erreur de connexion Bluetooth : {e}")

# --- ANGLE CALCULATION FUNCTION ---
def calculate_angle(a, b, c):
    """Calcule l'angle au sommet 'b' à partir de trois points a, b, c"""
    a, b, c = np.array(a), np.array(b), np.array(c)
    vector_ba = a - b
    vector_bc = c - b
    # Produit scalaire pour obtenir le cosinus
    cosine_angle = np.dot(vector_ba, vector_bc) / (np.linalg.norm(vector_ba) * np.linalg.norm(vector_bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

# --- MEDIAPIPE INITIALIZATION ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

# --- CAMERA CAPTURE ---
video_capture = cv2.VideoCapture(0)

# Dictionnaire des articulations : (Base, Milieu, Bout)
finger_landmarks = {
    "Thumb": (2, 3, 4), "Index": (5, 6, 7), "Middle": (9, 10, 11),
    "Ring": (13, 14, 15), "Pinky": (17, 18, 19)
}

while video_capture.isOpened():
    success, frame = video_capture.read()
    if not success: break
    
    # Prétraitement de l'image
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    img_h, img_w, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            servo_angles = []

            for name, points in finger_landmarks.items():
                # Extraction des coordonnées x, y
                p1 = [landmarks[points[0]].x, landmarks[points[0]].y]
                p2 = [landmarks[points[1]].x, landmarks[points[1]].y]
                p3 = [landmarks[points[2]].x, landmarks[points[2]].y]

                # Calcul et adaptation (180-angle pour que 0 = doigt tendu)
                raw_angle = calculate_angle(p1, p2, p3)
                final_angle = int(np.clip(180 - raw_angle, 0, 180))
                servo_angles.append(final_angle)

                # Affichage des angles sur l'image
                text_pos = (int(p2[0] * img_w), int(p2[1] * img_h) - 10)
                cv2.putText(frame, str(final_angle), text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Envoi des données via Bluetooth : "A,B,C,D,E\n"
            data_payload = ",".join(map(str, servo_angles)) + "\n"
            if arduino:
                arduino.write(bytes(data_payload, 'utf-8'))
            print(f"Sent: {data_payload.strip()}")

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Robotic Hand Control', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

video_capture.release()
if arduino: arduino.close()
cv2.destroyAllWindows()
