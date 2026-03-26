import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:

    while cap.isOpened():
        status, frame = cap.read()
        if not status:
            break

        # Mirror the frame for natural movement
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        # Convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            # Finger tips indices: Thumb(4), Index(8), Middle(12), Ring(16), Pinky(20)
            tips = [4, 8, 12, 16, 20]
            tip_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
            
            for hand_landmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    # Convert normalized coordinates to pixel coordinates
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cz = lm.z  # Z is relative to the wrist

                    if id in tips:
                        # Find the index in our tip names list
                        name = tip_names[tips.index(id)]
                        # 1. Print to terminal
                        print(f"{name} Tip -> X: {cx}, Y: {cy}, Z: {cz:.4f}")
                        # 2. Draw a circle on the tip
                        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
                        # 3. Put coordinate text on the frame
                        cv2.putText(frame, f"{cz:.2f}", (cx -30, cy - 15),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 50, 0), 1)

                # Draw the full hand skeleton
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("Finger Tips Coordinates", frame)
        
        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()