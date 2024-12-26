# Robotic Hand Control Using Arduino and Computer Vision

This innovative design is powered by an Arduino microcontroller, which controls the servo motors responsible for the hand’s movements. Each finger is connected to a servo via thread, allowing precise movements as the servo pulls the strings.

What makes it even more fascinating is the integration of camera vision. Using OpenCV and Mediapipe, the system detects hand movements and tracks the angle changes of each finger in real-time. The camera feeds this data to the Arduino, enabling seamless interaction between the user’s hand and the robotic hand. 🚀

A small step towards sustainable tech, a big leap in innovation!

---

## Features

- **Servo-controlled robotic hand**: Each finger is controlled by a servo motor via a thread mechanism.
- **Real-time hand tracking**: Hand movements are detected and tracked using OpenCV and Mediapipe.
- **Seamless integration**: The system enables real-time control and feedback between the user’s hand and the robotic hand.

## System Requirements

- **Hardware**:
  - Arduino board (e.g., Arduino Uno)
  - Servo motors (e.g., 5 x SG90)
  - Camera for vision processing (e.g., USB webcam or Raspberry Pi Camera)
  - Jumper wires and other standard Arduino accessories

- **Software**:
  - Arduino IDE
  - Python (version >= 3.6)
  - OpenCV
  - Mediapipe
  - Required Python libraries (e.g., `numpy`, `serial`)

## Installation

### 1. Arduino Setup
1. Install the [Arduino IDE](https://www.arduino.cc/en/software).
2. Download the Arduino code from the repository and upload it to your Arduino board.
3. Ensure the servo motors are properly wired to the Arduino board.

### 2. Python Setup
1. Install Python (if not already installed): [Python Official Website](https://www.python.org/downloads/).
2. Install the required Python libraries:
   ```bash
   pip install opencv-python mediapipe numpy pyserial
