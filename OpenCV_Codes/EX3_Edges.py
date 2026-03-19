import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Convert to grayscale (Canny works on single channel)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Optional: Blur to reduce noise (improves edge quality)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # ----------- Different Threshold Variants ------

    # 1. Very sensitive (detects almost everything, including noise)
    edges_low = cv2.Canny(blur, 30, 80)

    # 2. Very strict (only strong edges)
    edges_high = cv2.Canny(blur, 200, 400)

    # ----------- Display all outputs -----------

    cv2.imshow("Original", frame)
    cv2.imshow("Low Threshold (Noisy)", edges_low)
    cv2.imshow("Very High (Minimal)", edges_high)

    # Press 'q' to exit
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()