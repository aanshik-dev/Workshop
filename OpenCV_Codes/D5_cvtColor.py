import cv2

# read image
img = cv2.imread("Learning/Robotics/OpenCV_Codes/image.png")
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

negative = 255 - img

cv2.imshow("Kingfisher", img)
cv2.imshow("Negative", negative)
cv2.waitKey(0)
cv2.destroyAllWindows()