<div style= "width: 100%; background-image: linear-gradient(90deg,rgb(20, 0, 36),rgb(31, 0, 56),rgb(66, 13, 94)); background-size: contain;">
<div style= "backdrop-filter: blur(15px) brightness(150%); padding: 25px" >

# 🐦‍🔥🔥 **Instructions** 🔥🐦‍🔥

<br>

## 🐦‍🔥 Arduino Ide

⚡ Latest : Arduino IDE 2.3.8

⚡ Installation:

- Link: `https://www.arduino.cc/en/software/`
- Scroll to find the download button, and click on it
- Run the downloaded exe file
- Click on `Install`

⚡ To support the ESP8266 and ESP32, install the following libraries:

- Got to File > Preferences > Additional Boards Manager URLs
- On the right side of the blank textbox, click on the button
- Paste the following links in new line

```bash
http://arduino.esp8266.com/stable/package_esp8266com_index.json
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

⚡ Download ESP32 Board

- Go to Boards Tab (2nd on left vertical pane)
- Search for `esp32` by espressif and `Arduino ESP32 Boards` by Arduino
- Click on `Install` to install both

## 🐦‍🔥 Python

⚡ Requirement : Python 3.11.0

⚡ Installation:

- Link: `https://www.python.org/downloads/release/python-3110/`
- Click On Windows Installer
- Run the exe file
- Click on last Checkbox: `Add Python to PATH`
- Click on Install Now
- Open Terminal to varify installation
- `python --version` // should return `Python 3.11.0`

## 🐦‍🔥 OpenCV

⚡ Requirement : OpenCV 4.9.0

⚡ Installation:

```bash
pip install opencv-python
```

## 🐦‍🔥 MediaPipe

⚡ Requirement : MediaPipe 0.10.0

⚡ Installation:

```bash
pip install mediapipe==0.10.9
```

<br>

## 🐦‍🔥 Project Libraries

- `numpy`
- `screen_brightness_control`

### 🔥 screen_brightness_control

⚡ Required for the `Mediapipe_Codes/EX1_Brightness.py`

```bash
pip install screen_brightness_control
```

### 🔥 Numpy

```bash
pip install numpy
```

### 🔥 PySerial

⚡ Required for the project to communicate with the arduino

```bash
pip install pyserial
```

### 🔥 Pyfirmata

```bash
pip install pyfirmata2
```

The robotic arm uses the firmata instead of the serial communication

- go to files > examples > firmata > standard firmata
- upload the code to the arduino uno, (doesn't work for the esp32)
- Run the Gesture_complete python script
