<div style= "width: 100%; background-image: linear-gradient(90deg,rgb(20, 0, 36),rgb(31, 0, 56),rgb(66, 13, 94)); background-size: contain;">
<div style= "backdrop-filter: blur(15px) brightness(150%); padding: 25px" >

# 🐦‍🔥🔥 **OPEN-CV Notes** 🔥🐦‍🔥

- By Aanshik-dev

<br>

## 🐦‍🔥 What is OpenCV?

OpenCV (Open Source Computer Vision Library) is a library used for:

- Image processing
- Video processing
- Object detection
- Face recognition
- Gesture detection
- Robotics vision

It allows computers to see and understand images or videos.
Projects use OpenCV to:

- Capture video from webcam
- Process frames
- Draw landmarks
- Display the result

### 🔥 Installing OpenCV

```bash
pip install opencv-python
```

⚡ Test installation:

```py
import cv2
print(cv2.**version**)
```

<br>

## 🐦‍🔥 How Images Work in OpenCV

An image is just a matrix of pixels.

- Example:
  `Image` = 720 x 1080 pixels
  Each pixel contains 3 values:
  `[B, G, R]`

- Pixel Example:
  [255,0,0] → Blue
  [0,255,0] → Green
  [0,0,255] → Red

> 📝 NOTE : OpenCV uses BGR instead of RGB.

<br>

## 🐦‍🔥 Reading and Displaying an Image

```py
import cv2

# read image
img = cv2.imread("image.jpg")

# show image
cv2.imshow("My Image", img)

# wait until key pressed
cv2.waitKey(0)

# close window
cv2.destroyAllWindows()
```

⚡ Explanation:

| Function                  | Purpose            |
| ------------------------- | ------------------ |
| `cv2.imread()`            | load image         |
| `cv2.imshow()`            | display image      |
| `cv2.waitKey()`           | wait for key press |
| `cv2.destroyAllWindows()` | close windows      |

waitKey(0) → Wait for any key to be pressed
waitKey(1000) → Wait for 1 second

<br>

## 🐦‍🔥 Accessing Image Properties

```py
import cv2

img = cv2.imread("image.jpg")

print("Shape:", img.shape)
print("Height:", img.shape[0])
print("Width:", img.shape[1])
print("Channels:", img.shape[2])
```

⚡ Example output:

Shape: (720,1080,3)

- Meaning:
  720 → height
  1080 → width
  3 → color channels (BGR)

> 📝 NOTE : The image object created is a 3D Numpy Array

<br>

## 🐦‍🔥 Drawing Shapes on Image

OpenCV allows drawing graphics on images for marking and visualizing the image.

### 🔥 Draw Line

```py
import cv2

img = cv2.imread("image.jpg")

cv2.line(img,(0,0),(300,300),(255,0,0),5)

cv2.imshow("Line",img)
cv2.waitKey(0)
```

⚡ Parameters:
`image, start_point, end_point, color, thickness`

### 🔥 Draw Rectangle

```py
cv2.rectangle(img,(100,100),(400,300),(0,255,0),3)
```

⚡ Parameters:
`image, top_left, bottom_right, color, thickness`
thickness = -1 for filled

### 🔥 Draw Circle

```
cv2.circle(img,(200,200),50,(0,0,255),-1)
```

⚡ Parameters:
`image, center, radius, color, thickness`

### 🔥 Write Text

```py
cv2.putText(img,
"Hello OpenCV",
(50,50),
cv2.FONT_HERSHEY_SIMPLEX,
1,
(255,255,255), 2)
```

⚡ Parameters:
`image, text, origin, font, scale, color, thickness`

Fonts:

- `cv2.FONT_HERSHEY_SIMPLEX`
- `cv2.FONT_HERSHEY_PLAIN`
- `cv2.FONT_HERSHEY_DUPLEX`
- `cv2.FONT_HERSHEY_COMPLEX`
- `cv2.FONT_HERSHEY_TRIPLEX`
- `cv2.FONT_HERSHEY_COMPLEX_SMALL`
- `cv2.FONT_HERSHEY_SCRIPT_SIMPLEX`
- `cv2.FONT_HERSHEY_SCRIPT_COMPLEX`

Scale can be any number including fractions.

<br>

## 🐦‍🔥 Capturing Video from Webcam

This is the most important part which is used in most of the projects.

```py
import cv2

cap = cv2.VideoCapture(0) # 0 for default camera

while True:
  status, frame = cap.read()

  cv2.imshow("Webcam", frame)
  if cv2.waitKey(1) == ord('q'):
    break
    # press q to quit
    # waitKey(1) = 1 ms
    # ord('q') = 113

cap.release() # close camera
cv2.destroyAllWindows()
```

⚡ Explanation:

- `VideoCapture(0)` open default webcam
- Loop infinitely to capture video
- `cap.read()` capture frame from camera, returns status & frame
- `status` is true if frame is captured
- `frame` is a 3D Numpy array
- `cv2.imshow()` display frame
- `cv2.waitKey(1)` wait for key press for 1 ms
- `ord('q')` = 113 = q key

<br>

## 🐦‍🔥 Flipping Camera

Often webcams are mirrored, this is how to fix it.

```py
frame = cv2.flip(frame,1)
```

Flip types:
`0` : vertical
`1` : horizontal
`-1` : both

image = cv2.flip(image, 1)

<br>

## 🐦‍🔥 Color Conversion

OpenCV uses BGR but many ML models use RGB.

```py
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

MediaPipe requires RGB, so we need to convert.

OpenCV → BGR
MediaPipe → RGB

| Conversion  | Code                  |
| ----------- | --------------------- |
| BGR → Gray  | `cv2.COLOR_BGR2GRAY`  |
| Gray → BGR  | `cv2.COLOR_GRAY2BGR`  |
| BGR → RGB   | `cv2.COLOR_BGR2RGB`   |
| RGB → BGR   | `cv2.COLOR_RGB2BGR`   |
| BGR → HSV   | `cv2.COLOR_BGR2HSV`   |
| HSV → BGR   | `cv2.COLOR_HSV2BGR`   |
| BGR → LAB   | `cv2.COLOR_BGR2LAB`   |
| BGR → YCrCb | `cv2.COLOR_BGR2YCrCb` |

⚡ To convert to negative image

```py
negative = 255 - img
```

This subtract each pixel value from 255 of the original 3D image array

<br>

## 🐦‍🔥 Drawing Graphics on Video

```py
import cv2

cap = cv2.VideoCapture(0)

while True:
ret, frame = cap.read()
    #Creating a UI panel on the frame
    cv2.rectangle(frame,(50,50),(300,200),(0,255,0),3)
    cv2.putText(frame,"Camera Active",(60,90),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

    cv2.imshow("Demo",frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

<br>

## 🐦‍🔥  Frame Processing Concept

Camera → Frames → Process Frame → Show Frame

Example flow:

Webcam
↓
Frame captured
↓
OpenCV modifies frame
↓
MediaPipe detects hand
↓
Servo angles calculated
↓
Frame displayed

 Demo Before MediaPipe (Recommended)

Show this before hand tracking.

Demo Code 5 – Simple Motion Demo

```py
import cv2
cap = cv2.VideoCapture(0)

while True:
ret, frame = cap.read()

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
```
This teaches:

frame dimensions
drawing shapes
text overlay
real-time processing

1️⃣4️⃣ How This Connects to Your Final Project

Explain this transition:

OpenCV → Camera frames
↓
MediaPipe → Detect hand landmarks
↓
Math → calculate finger angles
↓
PyFirmata → send servo signal
↓
Arduino → move robotic hand
1️⃣5️⃣ Simple Visual Pipeline for Students

Show them this diagram:

Camera
│
OpenCV
│
Frame Processing
│
MediaPipe Hand Detection
│
Finger Angle Calculation
│
Servo Angle Mapping
│
Arduino Control
│
Robotic Hand Movement

<br>
