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

### 🔥 We will use the mediapipe in our project for:

✔ real-time hand detection
✔ finger landmarks
✔ hand skeleton
✔ depth estimation

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

⚡ D1_HandMap.py

```py
import cv2
import mediapipe as mp

# mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# webcam
cap = cv2.VideoCapture(0)

with mp_hands.Hands() as hands:

    while cap.isOpened():
        status, frame = cap.read()
        # convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect hands
        results = hands.process(rgb)

        # check if hands are detected
        if results.multi_hand_landmarks:
            print(results.multi_hand_landmarks)

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

Steps involved:

⚡ Passing image to the model and getting output:

```py
results = hands.process(frame)
# returns an object containing all the detection data
```

```bash
results  # Result Object
│
├── multi_hand_landmarks # collection of hands
│        │
│        ├── Hand_Landmarks 1  # Hand 1
│        │      └── 21 landmarks  # 21 points
│        │
│        ├── Hand_Landmarks 2
│        │      └── 21 landmarks
│        │
│        └── Hand_Landmarks 3 (if visible)
│               └── 21 landmarks
│
├── multi_handedness
│      └── Left / Right classification
│
└── multi_hand_world_landmarks
       └── 3D coordinates
```

⚡ Accessing each hand detected:

```py
for hand_landmarks in results.multi_hand_landmarks:
# for each hand detected
```

⚡ Drawing landmarks:

```py
mp_draw.draw_landmarks(
          frame,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS
        )  # draw skeleton, takes entire hand_landmarks array of 21 points, draws lines between them
```

⚡ Accessing all 21 landmarks:

```py
for idx, lm in enumerate(hand_landmarks.landmark):
    h, w, c = frame.shape
    x, y, z = int(lm.x*w), int(lm.y*h), int(lm.z*w)
    print(id, x, y, z)
```

- Each landmark has: `x`,`y`,`z` coordinates
  | Value | Meaning |
  | ----- | ------------------- |
  | x | horizontal position |
  | y | vertical position |
  | z | depth |

- Coordinates are normalized between 0 and 1, so convert to pixels:

```py
h, w, c = frame.shape

x = int(lm.x * w)
y = int(lm.y * h)
```

> 📝 NOTE : The Z coordinate provides depth, if point is near the screen then it is negative and if away then positive

<br>

## 🐦‍🔥 Print Landmark Positions

⚡ D2_Landmarks.py

```py
import cv2
import mediapipe as mp

# mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# default webcam
cap = cv2.VideoCapture(0)

# Hand detection
with mp_hands.Hands() as hands:

  while cap.isOpened():
    status, frame = cap.read() # read frame
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # BGR to RGB

    results = hands.process(rgb) # calling mediapipe

    if results.multi_hand_landmarks: # check if hands are detected

      # for each hand detedcted
      for hand_landmarks in results.multi_hand_landmarks:
        # draw landmarks
        mp_draw.draw_landmarks(
                frame,
                hand_landmarks, # passing array of 21 landmarks
                mp_hands.HAND_CONNECTIONS
        )
        # for each landmark(x,y,z)
        for idx, lm in enumerate(hand_landmarks.landmark):
          h, w, c = frame.shape  # height, width, channels
          x, y, z = int(lm.x*w), int(lm.y*h), int(lm.z*w)
          print(f"[{idx}] = {x}, {y}, {z}")

    frame = cv2.flip(frame,1)  # flip frame
    cv2.imshow("Hand", frame)

    if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
```

<br>

## 🐦‍🔥 Highlight Finger Tips

⚡ D3_FingerTips.py

```py
tips = [4,8,12,16,20]

if id in tips: # if tip then draw circle
  cv2.circle(frame,(x,y),10,(0,255,0),-1)
```

This is used more often to highlight the finger tips.
