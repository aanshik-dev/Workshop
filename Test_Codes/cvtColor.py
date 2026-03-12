import cv2

# read image
img = cv2.imread("Learning/Robotics/Test_Codes/image.png")
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


cv2.imshow("Kingfisher", img)
cv2.waitKey(0)
cv2.destroyAllWindows()