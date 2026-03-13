import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands() as hands:

    while cap.isOpened():
        status, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            # finger tips index array
            tips = [4,8,12,16,20]
            # for each hand
            for hand_landmarks in results.multi_hand_landmarks:
                # for each landmark
                for id,lm in enumerate(hand_landmarks.landmark):
                  h,w,c = frame.shape
                  x,y = int(lm.x*w), int(lm.y*h)

                  if id in tips: # if tip then draw circle
                        cv2.circle(frame,(x,y),10,(0,255,0),-1)

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("Finger Tips",frame)
        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
