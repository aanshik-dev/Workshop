import cv2
import mediapipe as mp

# -----------------------------
# Setup
# -----------------------------
mp_face = mp.solutions.face_mesh
cap = cv2.VideoCapture(0)

# Colors (B, G, R)
COLOR_POINTS = (255, 255, 0)  # Cyan/Yellowish highlight
COLOR_LINES = (255, 255, 255) # Pure White for custom geometry
COLOR_EDGES = (0, 255, 255)   # Neon Yellow/Cyan for features

# Custom geometric connections (Outer Face Oval)
connections = [
    (10, 338), (338, 297), (297, 332), (332, 284),
    (284, 251), (251, 389), (389, 356), (356, 454),
    (454, 323), (323, 361), (361, 288), (288, 397),
    (397, 365), (365, 379), (379, 378), (378, 400),
    (400, 377), (377, 152),
    (152, 148), (148, 176), (176, 149), (149, 150),
    (150, 136), (136, 172), (172, 58), (58, 132),
    (132, 93), (93, 234), (234, 127), (127, 162),
    (162, 21), (21, 54), (54, 103), (103, 67), (67, 109),
    (109, 10)
]

# Feature Edges (Indices for eyes and lips)
L_EYE = [33, 160, 158, 133, 153, 144]
R_EYE = [362, 385, 387, 263, 373, 380]
LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 185]

with mp_face.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                points = []
                for lm in face_landmarks.landmark:
                    points.append((int(lm.x * w), int(lm.y * h)))

                # 1. Draw "Edge" Contours for features (Eyes and Lips)
                def draw_contour(indices, color, thickness=1):
                    for i in range(len(indices)):
                        p1 = points[indices[i]]
                        p2 = points[indices[(i + 1) % len(indices)]]
                        cv2.line(frame, p1, p2, color, thickness)

                draw_contour(L_EYE, COLOR_EDGES, 1)
                draw_contour(R_EYE, COLOR_EDGES, 1)
                draw_contour(LIPS, COLOR_EDGES, 1)

                # 2. Draw custom connections (Geometric Oval)
                for start, end in connections:
                    cv2.line(frame, points[start], points[end], COLOR_LINES, 1)

                # 3. Draw small landmark points (Subtle)
                for point in points:
                    cv2.circle(frame, point, 1, COLOR_POINTS, -1)

        cv2.imshow("Advanced Face Geometry", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()