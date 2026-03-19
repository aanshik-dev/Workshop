import cv2
import mediapipe as mp
import numpy as np
import math
import screen_brightness_control as sbc

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

# Brightness range
min_brightness = 0
max_brightness = 100

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror image

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_img)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []

            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))

            # Thumb tip = 4, Index tip = 8
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            # Draw points
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), -1)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), -1)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # Distance
            length = math.hypot(x2 - x1, y2 - y1)

            # Map distance to brightness
            brightness = np.interp(length, [20, 200], [min_brightness, max_brightness])
            sbc.set_brightness(int(brightness))

            # Display brightness
            cv2.putText(img, f'Brightness: {int(brightness)}%', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Brightness Control", img)

    if cv2.waitKey(1) == ord('q'):  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()