import cv2  # OpenCV library for image processing

# Load face detector (pre-trained Haar Cascade model)
face = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Load sunglasses image with transparency (alpha channel)
# IMREAD_UNCHANGED ensures we get 4 channels (B, G, R, Alpha)
glass = cv2.imread("Learning/Robotics/Mediapipe_Codes/Sunglasses.png",cv2.IMREAD_UNCHANGED)

# Start webcam (0 = default camera)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from webcam
    ret, img = cap.read()

    # Flip image horizontally (mirror effect like selfie)
    img = cv2.flip(img, 1)

    # Convert frame to grayscale (face detection works better)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    # (image, scaleFactor, minNeighbors)
    faces = face.detectMultiScale(gray, 1.3, 5)

    # Loop through all detected faces
    for (x, y, w, h) in faces:

        # Resize sunglasses to match face width
        # Height is adjusted proportionally (40% of face height)
        g = cv2.resize(glass, (w, int(h * 0.4)))

        # Loop through each pixel of the sunglasses image
        for i in range(g.shape[0]):      # rows (height)
            for j in range(g.shape[1]):  # columns (width)

                # Check alpha channel (transparency)
                # g[i, j][3] → alpha value (0 = fully transparent)
                if g[i, j][3] != 0:  # only place non-transparent pixels

                    # Place pixel on face region
                    # y + offset moves it slightly down to eye level
                    img[y + int(h * 0.25) + i, x + j] = g[i, j][:3]
                    # [:3] → take only BGR, ignore alpha

    # Show output window
    cv2.imshow("Filter 😎", img)

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Release camera and close all windows
cap.release()
cv2.destroyAllWindows()