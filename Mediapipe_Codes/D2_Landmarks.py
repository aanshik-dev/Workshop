import cv2
import mediapipe as mp

# mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# default webcam
cap = cv2.VideoCapture(0)

# Hand detection
with mp_hands.Hands() as hands:

  while cap.isOpened():
    status, frame = cap.read() # read frame
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # BGR to RGB

    results = hands.process(rgb) # calling mediapipe

    if results.multi_hand_landmarks: # check if hands are detected

      # for each hand detedcted
      for hand_landmarks in results.multi_hand_landmarks:
        # draw landmarks
        mp_draw.draw_landmarks(
          frame,
          hand_landmarks, # passing array of 21 landmarks
          mp_hands.HAND_CONNECTIONS
        )
        # for each landmark(x,y,z)
        for idx, lm in enumerate(hand_landmarks.landmark):
          h, w, c = frame.shape  # height, width, channels
          x, y, z = int(lm.x*w), int(lm.y*h), int(lm.z*w)  # x, y, z in px
          print(f"[{idx}] = {x}, {y}, {z}")

    frame = cv2.flip(frame,1)  # flip frame
    cv2.imshow("Hand", frame)

    if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()