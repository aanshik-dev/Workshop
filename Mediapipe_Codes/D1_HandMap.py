import cv2
import mediapipe as mp

# mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# webcam
cap = cv2.VideoCapture(0)

with mp_hands.Hands() as hands:

    while True:
        status, frame = cap.read()
        # convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect hands
        results = hands.process(rgb)

        # check if hands are detected
        if results.multi_hand_landmarks:
            print(results.multi_hand_landmarks)

            for hand_landmarks in results.multi_hand_landmarks:
                # draw landmarks
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )
        frame = cv2.flip(frame,1)
        cv2.imshow("Hand Detection", frame)

        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
