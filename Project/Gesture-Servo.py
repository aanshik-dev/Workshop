import cv2
import mediapipe as mp
import math
import numpy as np
import serial
import time

ser = serial.Serial("COM10", 115200)
time.sleep(2)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

def dist(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def angle_cal(a, b, c):
    bc = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]))
    ba = math.degrees(math.atan2(a[1] - b[1], a[0] - b[0]))
    angle = bc - ba
    if angle < 0:
        angle = -angle
    if angle > 180:
        angle = 360 - angle
    return angle


def servo_control(finger_len, b2w, t2w, factor, delta, angle):
    if delta > 55:
        if t2w < b2w:
            return 0
        elif t2w > b2w:
            value = np.interp(finger_len, [5, b2w * factor], [0, 180])
            value = min(max(value, 0), 180)
            return value
        else:
            return 180
    else:
        value = np.interp(angle, [65, 175], [0, 180])
        return value


def draw_mode_text(image, delta):
    if delta > 55:
        color = (130, 0, 255)
        text = "DISTANCE MODE"
    else:
        color = (0, 180, 0)
        text = "ANGLE MODE"

    cv2.circle(image, (40, 40), 15, color, cv2.FILLED)
    cv2.putText(image, text, (70, 50),
                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)

with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=1) as hands:

    while cap.isOpened():

        success, image = cap.read()
        if not success:
            continue
        image = cv2.flip(image, 1)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = hands.process(rgb)
        rgb.flags.writeable = True
        image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                ls = []
                depth = []
                h, w, c = image.shape

                for lm in hand_landmarks.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    z = lm.z * 1000
                    ls.append((x, y))
                    depth.append(z)

                if len(ls) >= 9:
                    wrist = ls[0]

                    idx_base = ls[5]
                    idx_mid = ls[6]
                    idx_tip = ls[8]

                    idx_b2w = dist(idx_base, wrist)
                    idx_t2w = dist(idx_tip, wrist)
                    idx_len = dist(idx_base, idx_tip)

                    index_angle = angle_cal(idx_base, idx_mid, idx_tip)

                    if len(depth) > 17:

                        diff = depth[5] - depth[17]
                        if diff == 0:
                            diff = 0.001
                        delta = abs((dist(ls[9], wrist) / diff) * 10)
                    else:
                        delta = 0

                    draw_mode_text(image, delta)

                    index_val = servo_control(
                        idx_len,
                        idx_b2w,
                        idx_t2w,
                        0.85,
                        delta,
                        index_angle
                    )

                    index_val = int(index_val)

                    # SEND TO ARDUINO
                    ser.write((str(index_val) + "\n").encode())

                    cv2.putText(
                        image,
                        f"Servo: {index_val}",
                        (20, 100),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1,
                        (255, 0, 255),
                        2
                    )

                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

        cv2.imshow("Index Finger Servo Control", image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
ser.close()