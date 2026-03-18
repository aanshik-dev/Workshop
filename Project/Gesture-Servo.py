import cv2
import mediapipe as mp
import math
import pyfirmata2
import numpy as np
import time

# Arduino / NodeMCU connection
PORT = "COM5"
board = pyfirmata2.Arduino(PORT)
time.sleep(3)


iterator = pyfirmata2.util.Iterator(board)
iterator.start()

# Only ONE servo (Index Finger)
index_pin = 5
servo_index = board.get_pin(f"d:{index_pin}:s")
servo_index.mode = pyfirmata2.SERVO

# Mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)


def angle_cal(a, b, c):

    bc = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]))
    ba = math.degrees(math.atan2(a[1]-b[1], a[0]-b[0]))

    angle = bc - ba

    if angle < 0:
        angle = -angle

    if angle > 180:
        angle = 360 - angle

    return angle


def servo_control(length, b2w, t2w, factor, delta, angle):

    if delta > 55:

        if t2w < b2w:
            return 0

        elif t2w > b2w:

            value = np.interp(length, [5, b2w*factor], [0,180])
            value = min(max(value,0),180)

            return value

        else:
            return 180

    else:

        value = np.interp(angle, [65,175], [0,180])

        return value


with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1
) as hands:

    while cap.isOpened():

        success, image = cap.read()

        if not success:
            continue

        image = cv2.flip(image,1)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False

        results = hands.process(image)

        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                ls=[]
                depth=[]

                for idx,lm in enumerate(hand_landmarks.landmark):

                    h,w,c = image.shape

                    x,y = int(lm.x*w), int(lm.y*h)
                    z = lm.z*1000

                    ls.append((x,y))
                    depth.append(z)

                if len(ls) > 8:

                    wrist = ls[0]

                    thumb_base = ls[2]
                    thumb_mid = ls[3]
                    thumb_tip = ls[4]

                    idx_base = ls[5]
                    idx_mid = ls[6]
                    idx_tip = ls[8]

                    mid_base = ls[9]
                    mid_mid = ls[10]
                    mid_tip = ls[12]

                    ring_base = ls[13]
                    ring_mid = ls[14]
                    ring_tip = ls[16]

                    lit_base = ls[17]
                    lit_mid = ls[18]
                    lit_tip = ls[20]


                    # distances
                    idx_b2w = dist(idx_base, wrist)
                    idx_t2w = dist(idx_tip, wrist)
                    idx_len = dist(idx_base, idx_tip)

                    mid_b2w = dist(mid_base, wrist)
                    mid_t2w = dist(mid_tip, wrist)
                    mid_len = dist(mid_base, mid_tip)

                    ring_b2w = dist(ring_base, wrist)
                    ring_t2w = dist(ring_tip, wrist)
                    ring_len = dist(ring_base, ring_tip)

                    lit_b2w = dist(lit_base, wrist)
                    lit_t2w = dist(lit_tip, wrist)
                    lit_len = dist(lit_base, lit_tip)


                    # angles
                    thumb_angle = angle_cal(thumb_base, thumb_mid, thumb_tip)
                    index_angle = angle_cal(idx_base, idx_mid, idx_tip)
                    middle_angle = angle_cal(mid_base, mid_mid, mid_tip)
                    ring_angle = angle_cal(ring_base, ring_mid, ring_tip)
                    little_angle = angle_cal(lit_base, lit_mid, lit_tip)


                    # palm tilt
                    diff = depth[5] - depth[17]

                    delta = abs(mid_b2w/diff)*10


                    # servo value only for INDEX
                    index_val = servo_control(
                        idx_len,
                        idx_b2w,
                        idx_t2w,
                        0.85,
                        delta,
                        index_angle
                    )


                    # move servo
                    servo_index.write(180-index_val)


                    # PRINT ALL FINGER VALUES
                    print(
                        f"Thumb:{thumb_angle:.1f} | "
                        f"Index:{index_val:.1f} | "
                        f"Middle:{middle_angle:.1f} | "
                        f"Ring:{ring_angle:.1f} | "
                        f"Little:{little_angle:.1f}"
                    )


                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )


        cv2.imshow("Hand Tracking",image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


cap.release()
cv2.destroyAllWindows()
board.exit()