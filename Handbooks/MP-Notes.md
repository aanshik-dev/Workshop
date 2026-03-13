<div style= "width: 100%; background-image: linear-gradient(90deg,rgb(20, 0, 36),rgb(31, 0, 56),rgb(66, 13, 94)); background-size: contain;">
<div style= "backdrop-filter: blur(15px) brightness(150%); padding: 25px" >

# 🐦‍🔥🔥 **Mediapipe Notes** 🔥🐦‍🔥

- By [Aanshik-dev](https://aanshik-dev.vercel.app/)

<br>

## 🐦‍🔥 What is OpenCV?

MediaPipe is a machine learning framework by Google used for real-time perception.

It provides ready-made AI models for:

- Hand tracking
- Face detection
- Pose estimation
- Object detection
- Gesture recognition

Instead of training AI models from scratch, MediaPipe gives pre-trained pipelines.

The gesture controlled robotic hand project uses MediaPipe Hands to detect 21 hand landmarks.

### 🔥 Installing MediaPipe

```bash
pip install mediapipe
```

⚡ Test installation:

```py
import mediapipe as mp
print(mp.__version__)
```

<br>

## 🐦‍🔥 How MediaPipe Works

MediaPipe can be thought of as a black box, which takes frame as input and gives detected output.

While training the black box model, it is fed with a dataset of images and their corresponding hand landmarks

```
                           Input Frame
                               ↓
    (Training)            +-----------+
    Sample Frames   ===>  | Black Box |
    Expected output ===>  |   Model   |
                          +-----------+
                               ↓
                         Predicted Output
```

Pipeline used in upcoming project:

```
Camera Frame
       ↓
OpenCV Capture
       ↓
Convert BGR → RGB
       ↓
MediaPipe Hands Model
       ↓
Detect Hand
       ↓
Return 21 Landmarks
       ↓
OpenCV draws them
```

<br>

## 🐦‍🔥 MediaPipe Hand Landmarks

MediaPipe detects 21 key points, and return them as coordinates in the image.

⚡ Landmark numbers:

| Point | Meaning       |
| ----- | ------------- |
| 0     | Wrist         |
| 1–4   | Thumb         |
| 5–8   | Index finger  |
| 9–12  | Middle finger |
| 13–16 | Ring finger   |
| 17–20 | Little finger |

These coordinates are used to calculate:

- finger angle
- finger length
- finger direction

<br>

## 🐦‍🔥 Basic MediaPipe Hand Detection Code

```py
import cv2
import mediapipe as mp

# mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# webcam
cap = cv2.VideoCapture(0)

with mp_hands.Hands() as hands:

    while True:
        status, frame = cap.read()
        # convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect hands
        results = hands.process(rgb)

        # check if hands are detected
        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:
                # draw landmarks
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )
        frame = cv2.flip(frame,1)
        cv2.imshow("Hand Detection", frame)

        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
```

You should see hand skeleton tracking in real time on your webcam.

<br>

## 🐦‍🔥 Important MediaPipe Parameters

In your project you used:

```py
mp_hands.Hands(
min_detection_confidence=0.5,
min_tracking_confidence=0.5,
max_num_hands=1
)
```

Explanation:

| Parameter                  | Meaning                           |
| -------------------------- | --------------------------------- |
| `min_detection_confidence` | minimum confidence to detect hand |
| `min_tracking_confidence`  | confidence to track hand          |
| `max_num_hands`            | maximum hands detected            |

Example:
max_num_hands = 2
detects both hands.

<br>

## 🐦‍🔥 Getting Landmark Coordinates

Each landmark has: `x`,`y`,`z` coordinates

Example:

```py
for lm in hand_landmarks.landmark:
  print(lm.x, lm.y, lm.z)
```

Meaning:

| Value | Meaning             |
| ----- | ------------------- |
| x     | horizontal position |
| y     | vertical position   |
| z     | depth               |

Coordinates are normalized, between 0 and 1.
To convert to pixels:

```py
h, w, c = frame.shape

x = int(lm.x * w)
y = int(lm.y * h)
```

<br>

## 🐦‍🔥 Print Landmark Positions

import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands() as hands:

    while True:
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                for id, lm in enumerate(hand_landmarks.landmark):

                    h, w, c = frame.shape
                    x, y = int(lm.x*w), int(lm.y*h)

                    print(id, x, y)

        cv2.imshow("Hand", frame)

        if cv2.waitKey(1) == ord('q'):
            break

Students will see landmark coordinates printing in terminal.

9️⃣ Highlight Finger Tips

Useful demonstration before robotics.

Demo Code 3
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

tips = [4,8,12,16,20]

cap = cv2.VideoCapture(0)

with mp_hands.Hands() as hands:

    while True:

        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                for id,lm in enumerate(hand_landmarks.landmark):

                    h,w,c = frame.shape
                    x,y = int(lm.x*w), int(lm.y*h)

                    if id in tips:
                        cv2.circle(frame,(x,y),10,(0,255,0),-1)

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("Finger Tips",frame)

        if cv2.waitKey(1) == ord('q'):
            break

Students will see green dots on finger tips.

🔟 MediaPipe Output Structure

When a hand is detected:

results
├── multi_hand_landmarks
│ └── 21 landmarks
│
└── multi_handedness
└── left / right hand
1️⃣1️⃣ Why MediaPipe is Used in Your Project

MediaPipe provides:

✔ real-time hand detection
✔ finger landmarks
✔ hand skeleton
✔ depth estimation

Your project uses these to compute:

finger angles
finger distances
palm tilt

Then send commands to Arduino servos.

1️⃣2️⃣ Bridge to Your Robotic Hand Code

Explain to juniors:

MediaPipe → detects hand landmarks
↓
Python math → calculate finger angles
↓
Servo angles (0–180)
↓
PyFirmata → Arduino
↓
Robot hand moves
⭐ Best Classroom Demo Order

Teach in this order:

1️⃣ OpenCV webcam
2️⃣ MediaPipe hand detection
3️⃣ Landmark coordinates
4️⃣ Finger tip detection
5️⃣ Finger angle calculation
6️⃣ Servo control

💡 If you want, I can also give you one very powerful demo (only ~80 lines) that shows:

hand detection

finger counting

gesture recognition

which looks super impressive in workshops and helps students understand MediaPipe before your robotic hand code.
