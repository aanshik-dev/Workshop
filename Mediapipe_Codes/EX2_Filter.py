import cv2
import numpy as np

# Load face detector
face = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Load filters (with alpha channel)
glass = cv2.imread("Learning/Robotics/Mediapipe_Codes/Filter_Glasses.png", cv2.IMREAD_UNCHANGED)
cat = cv2.imread("Learning/Robotics/Mediapipe_Codes/Filter_Cat.png", cv2.IMREAD_UNCHANGED)

cap = cv2.VideoCapture(0)

mode = 1  # 0 = no filter, 1 = glasses, 2 = cat mask

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        # ---------------- GLASSES ----------------
        if mode == 1:
            g = cv2.resize(glass, (w, int(h * 0.4)))

            for i in range(g.shape[0]):
                for j in range(g.shape[1]):
                    if g[i, j][3] != 0:
                        if y + int(h * 0.25) + i < img.shape[0] and x + j < img.shape[1]:
                            img[y + int(h * 0.25) + i, x + j] = g[i, j][:3]

        # ---------------- CAT MASK ----------------
        elif mode == 2:
            c = cv2.resize(cat, (int(1.1*w), int(1.1*h)))

            for i in range(c.shape[0]):  # shape[0] = height
                for j in range(c.shape[1]):  # shape[1] = width
                    if c[i, j][3] != 0:
                        if (y - int(h * 0.3)) + i < img.shape[0] and (x - int(w * 0.1)) + j < img.shape[1]:
                            img[y - int(h * 0.3) + i, x - int(w * 0.1) + j] = c[i, j][:3]

    cv2.imshow("Filter 😎", img)

    key = cv2.waitKey(1)

    # Key controls
    if key == ord('1'):
        mode = 1
    elif key == ord('2'):
        mode = 2
    elif key == ord('0'):
        mode = 0  # remove filter
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()