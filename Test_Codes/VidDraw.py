import cv2

cap = cv2.VideoCapture(0)

while True:
  status, frame = cap.read()
  frame = cv2.flip(frame,1)

  cv2.rectangle(frame,(30,30),(300,100),(0,255,0),3)
  cv2.putText(frame,
              "Camera Active",
              (40,70),
              cv2.FONT_HERSHEY_SIMPLEX,
              1,
              (255,255,255),
              2)

  cv2.imshow("Demo",frame)
  if cv2.waitKey(1) == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()