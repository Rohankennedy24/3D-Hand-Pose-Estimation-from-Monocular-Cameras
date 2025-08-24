# backend.py
import cv2
import mediapipe as mp
from flask import Flask, jsonify

app = Flask(__name__)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

def landmark_to_3d(landmarks):
    result = []
    for lm in landmarks:
        result.append({
            'x': lm.x,
            'y': lm.y,
            'z': lm.z  # relative depth (negative means closer to camera)
        })
    return result

@app.route('/hand_landmarks')
def hand_landmarks():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        return jsonify({'error': 'Failed to capture image from camera'})
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    data = []
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            data.append(landmark_to_3d(hand_landmarks.landmark))
    cap.release()
    return jsonify({'hands': data})

if __name__ == '__main__':
    app.run(debug=True)
