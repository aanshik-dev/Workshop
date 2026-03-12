import cv2
cap = cv2.VideoCapture(0)

while True:
    status, frame = cap.read()

    h,w,c = frame.shape
    cv2.circle(frame,(w//2,h//2),50,(0,255,0),3)
    cv2.putText(frame,"OpenCV Demo",
                (50,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,255),
                2)

    cv2.imshow("OpenCV Camera",frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()