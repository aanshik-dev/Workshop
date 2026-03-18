import cv2

cap = cv2.VideoCapture(0) # 0 for default camera

while True:
  status, frame = cap.read()
  frame = cv2.flip(frame,1)

  cv2.imshow("Webcam", frame)
  if cv2.waitKey(1) == ord('q'):
    break
    # press q to quit
    # waitKey(1) = 1 ms  
    # ord('q') = 113

cap.release() # close camera
cv2.destroyAllWindows()