import cv2

# read image
img = cv2.imread("Learning/Robotics/Test_Codes/image.png")

print("Shape:", img.shape)
print("Height:", img.shape[0])
print("Width:", img.shape[1])
print("Channels:", img.shape[2])

# print(img)
# print(type(img))

