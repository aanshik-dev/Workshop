import cv2

cap = cv2.VideoCapture(0)

# Read first two frames
ret, frame1 = cap.read()
ret, frame2 = cap.read()

# Flip BOTH frames initially (mirror effect)
frame1 = cv2.flip(frame1, 1)
frame2 = cv2.flip(frame2, 1)

while cap.isOpened():
    
    # Compute difference between two consecutive frames
    diff = cv2.absdiff(frame1, frame2)
    
    # Convert to grayscale (simplifies processing)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # Blur to reduce noise (small random changes)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Convert to binary image (motion areas become white)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    
    # Dilate to make white regions bigger (fill gaps)
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find contours (moving regions)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        # Ignore small movements (like noise)
        if cv2.contourArea(c) < 2000:
            continue

        # Get bounding box around motion
        x, y, w, h = cv2.boundingRect(c)
        
        # Draw rectangle around motion
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)
        
        # Show motion text
        cv2.putText(frame1, "Motion Detected", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # Show the processed frame (already flipped)
    cv2.imshow("Motion Detector", frame1)

    # Move frames forward
    frame1 = frame2
    ret, frame2 = cap.read()

    if not ret:
        break

    # IMPORTANT: Flip the new frame also
    frame2 = cv2.flip(frame2, 1)

    # Press 'q' to exit
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()