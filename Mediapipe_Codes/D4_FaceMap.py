import cv2
import mediapipe as mp

# mediapipe setup
mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

# webcam
cap = cv2.VideoCapture(0)

# FaceMesh model
with mp_face.FaceMesh(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_faces=1) as face_mesh:

    while cap.isOpened():

        status, frame = cap.read()

        if not status:
            break

        # convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect face landmarks
        results = face_mesh.process(rgb)

        # check if face is detected
        if results.multi_face_landmarks:

            for face_landmarks in results.multi_face_landmarks:
              # Total 468 landmarks
                # draw face landmarks
                mp_draw.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face.FACEMESH_TESSELATION
                )

        # mirror image
        frame = cv2.flip(frame, 1)

        # show output
        cv2.imshow("Face Landmarks", frame)

        if cv2.waitKey(1) == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()