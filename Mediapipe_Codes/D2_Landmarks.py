import cv2
import mediapipe as mp

# mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# default webcam
cap = cv2.VideoCapture(0)

# Hand detection
with mp_hands.Hands() as hands:

    while True:
        status, frame = cap.read() # read frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # BGR to RGB

        results = hands.process(rgb) # calling mediapipe

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:
                # draw landmarks
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                id = 0
                for lm in hand_landmarks.landmark:
                    id += 1
                    h, w, c = frame.shape
                    x, y = int(lm.x*w), int(lm.y*h)
                    print(id, x, y)
                    
        frame = cv2.flip(frame,1)
        cv2.imshow("Hand", frame)

        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()