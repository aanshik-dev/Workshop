import cv2
# read image
img = cv2.imread("Learning/Robotics/OpenCV_Codes/image.png", 0)
# 1 for color and 0 for grayscale

img.flags.writeable = False # makes image read only

print(img.ndim)

# show image
cv2.imshow("Kingfisher", img)

# wait until key pressed
cv2.waitKey(0)

# close window
cv2.destroyAllWindows()


