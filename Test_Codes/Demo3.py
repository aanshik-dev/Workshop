import cv2

# read image
img = cv2.imread("Learning/Robotics/Test_Codes/image.png")

cv2.line(img, (540,360), (680, 180), (0, 0, 255), 3)
cv2.line(img,(680,180),(720,180),(0,0,255),3)

cv2.rectangle(img,(720,140),(1000,260),(0,255,255),-1)

cv2.circle(img,(420,140),130,(0,0,0),2)

cv2.putText(img,"Kingfisher",(740,200),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)

cv2.imshow("Line",img)
cv2.waitKey(0)
cv2.destroyAllWindows()