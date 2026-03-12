import cv2

# read image
img = cv2.imread("Learning/Robotics/Test_Codes/image.png")

# show image
cv2.imshow("My Image", img)

# wait until key pressed
cv2.waitKey(0)

# close window
cv2.destroyAllWindows()