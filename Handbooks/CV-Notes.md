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

<br>

## 🐦‍🔥 Capturing Video from Webcam

This is the most important part which is used in most of the projects.

Demo Code 3
import cv2

cap = cv2.VideoCapture(0)

while True:
ret, frame = cap.read()

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

Explanation:

Code Meaning
VideoCapture(0) open webcam
cap.read() capture frame
frame image from camera
while True continuous video
8️⃣ Flipping Camera

Often webcams are mirrored.

frame = cv2.flip(frame,1)

Flip types:

Value Meaning
0 vertical
1 horizontal
-1 both

Your project uses:

image = cv2.flip(image, 1)
9️⃣ Color Conversion

OpenCV uses BGR but many ML models use RGB.

Convert using:

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

Your project uses this because MediaPipe requires RGB.

OpenCV → BGR
MediaPipe → RGB
🔟 Drawing Graphics on Video
Demo Code 4
import cv2

cap = cv2.VideoCapture(0)

while True:
ret, frame = cap.read()

    cv2.rectangle(frame,(50,50),(300,200),(0,255,0),3)
    cv2.putText(frame,"Camera Active",(60,90),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

    cv2.imshow("Demo",frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

This is similar to your project:

cv2.rectangle(image, (10, 10), (450, 125), (0, 255, 200), cv2.FILLED)

It creates a UI panel on the video.

1️⃣1️⃣ Frame Processing Concept

Important concept to explain to juniors:

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
1️⃣2️⃣ Why OpenCV is Needed in Your Project

OpenCV handles:

✔ camera input
✔ image processing
✔ drawing landmarks
✔ displaying results

Without OpenCV:

No camera feed
No drawing
No video processing
1️⃣3️⃣ Demo Before MediaPipe (Recommended)

Show this before hand tracking.

Demo Code 5 – Simple Motion Demo
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
⭐ Good 30-Minute Teaching Flow

1️⃣ Intro to OpenCV (5 min)
2️⃣ Image basics (5 min)
3️⃣ Display image demo (5 min)
4️⃣ Webcam demo (10 min)
5️⃣ Drawing shapes demo (5 min)

Then next session:

OpenCV + MediaPipe

💡 If you want, I can also make a very clean 10-slide OpenCV PPT structure specifically tailored for your robotic hand project demo, which will make the session look much more professional.

<br>
