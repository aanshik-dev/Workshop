import cv2
import mediapipe as mp
import numpy as np

class EyeBlinkCounter:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True, # Critical for iris and fine eyelid tracking
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Optimized indices for EAR calculation (6 points per eye)
        self.L_EYE_EAR = [362, 385, 387, 263, 373, 380]
        self.R_EYE_EAR = [33, 160, 158, 133, 153, 144]
        
        # Full contour indices for "marking" (The fancy lines)
        self.L_EYE_FULL = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.R_EYE_FULL = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

        self.EAR_THRESH = 0.22
        self.CONSEC_FRAMES = 3
        
        # Counters
        self.l_blink_count = 0
        self.r_blink_count = 0
        self.l_frames = 0
        self.r_frames = 0

    def calculate_ear(self, eye_indices, landmarks, w, h):
        # Extract points as (x, y) pixels
        pts = []
        for idx in eye_indices:
            lm = landmarks.landmark[idx]
            pts.append(np.array([lm.x * w, lm.y * h]))
        
        # Vertical distances
        v1 = np.linalg.norm(pts[1] - pts[5])
        v2 = np.linalg.norm(pts[2] - pts[4])
        # Horizontal distance
        h_dist = np.linalg.norm(pts[0] - pts[3])
        
        return (v1 + v2) / (2.0 * h_dist)

    def draw_eye_marking(self, frame, eye_indices, landmarks, w, h, color):
        # Create a list of points for the contour
        pts = []
        for idx in eye_indices:
            lm = landmarks.landmark[idx]
            pts.append((int(lm.x * w), int(lm.y * h)))
        
        # Draw the "marking" edges using a hull for smoothness
        hull = cv2.convexHull(np.array(pts))
        cv2.polylines(frame, [hull], True, color, 1, cv2.LINE_AA)
        
        # Draw subtle dots on landmarks
        for p in pts:
            cv2.circle(frame, p, 1, (0, 0 , 255), -1)

    def process_frame(self, frame):
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face_lms in results.multi_face_landmarks:
                # 1. Calculate EAR
                l_ear = self.calculate_ear(self.L_EYE_EAR, face_lms, w, h)
                r_ear = self.calculate_ear(self.R_EYE_EAR, face_lms, w, h)

                # 2. Logic for Blinks
                # Left Eye
                if l_ear < self.EAR_THRESH:
                    self.l_frames += 1
                else:
                    if self.l_frames >= self.CONSEC_FRAMES:
                        self.l_blink_count += 1
                    self.l_frames = 0

                # Right Eye
                if r_ear < self.EAR_THRESH:
                    self.r_frames += 1
                else:
                    if self.r_frames >= self.CONSEC_FRAMES:
                        self.r_blink_count += 1
                    self.r_frames = 0

                # 3. Draw Geometry Markings
                # Use Cyan if open, Red if blinking
                l_color = (0, 200, 255) if l_ear > self.EAR_THRESH else (0, 0, 255)
                r_color = (0, 200, 255) if r_ear > self.EAR_THRESH else (0, 0, 255)

                self.draw_eye_marking(frame, self.L_EYE_FULL, face_lms, w, h, l_color)
                self.draw_eye_marking(frame, self.R_EYE_FULL, face_lms, w, h, r_color)

                # 4. Display Stats
                cv2.putText(frame, f"L Blinks: {self.l_blink_count}", (20, 40), 1, 1.5, (255, 50, 0), 2)
                cv2.putText(frame, f"R Blinks: {self.r_blink_count}", (20, 80), 1, 1.5, (255, 50, 0), 2)

        return frame

    def run(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, frame = cap.read()
            if not success: break
            
            frame = cv2.flip(frame, 1)
            frame = self.process_frame(frame)
            
            cv2.imshow("Geometry Blink Counter", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
            
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    counter = EyeBlinkCounter()
    counter.run()