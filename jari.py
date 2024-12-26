import cv2
import mediapipe as mp
import serial
import time
import math

# Inisialisasi komunikasi serial ke Arduino
try:
    arduino = serial.Serial('COM4', 9600, timeout=1)  # Ganti 'COM5' dengan port yang sesuai
    time.sleep(2)  # Tunggu koneksi serial stabil
except serial.SerialException as e:
    print(f"Error initializing serial connection: {e}")
    exit()

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Fungsi untuk mengirim data ke Arduino
def send_data_to_arduino(index_angle, middle_angle, ring_angle, pinky_angle, thumb_angle):
    try:
        data_str = f"{int(index_angle)},{int(middle_angle)},{int(ring_angle)},{int(pinky_angle)},{int(thumb_angle)}\n"
        arduino.write(data_str.encode())  # Mengirim data sudut ke Arduino
        print(f"Data sent: {data_str}")
        time.sleep(0.1)  # Delay 100 ms setelah mengirim data untuk memberikan waktu pada Arduino memproses data
    except serial.SerialException as e:
        print(f"Error sending data to Arduino: {e}")

# Fungsi untuk menghitung sudut antara tiga titik (landmark)
def calculate_angle(a, b, c):
    angle = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    )
    return angle + 360 if angle < 0 else angle

# Fungsi untuk mendeteksi jari (termasuk kelingking dan jempol) menggunakan MediaPipe
def detect_fingers(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if not results.multi_hand_landmarks:
        return None, None, None, None, None  # Mengembalikan None jika tidak ada tangan yang terdeteksi

    hand_landmarks = results.multi_hand_landmarks[0]

    # Jari Telunjuk (landmark 5, 6, 8)
    index_angle = calculate_angle(
        [hand_landmarks.landmark[5].x, hand_landmarks.landmark[5].y],
        [hand_landmarks.landmark[6].x, hand_landmarks.landmark[6].y],
        [hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y]
    )

    # Jari Tengah (landmark 9, 10, 12)
    middle_angle = calculate_angle(
        [hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y],
        [hand_landmarks.landmark[10].x, hand_landmarks.landmark[10].y],
        [hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y]
    )

    # Jari Manis (landmark 13, 14, 16)
    ring_angle = calculate_angle(
        [hand_landmarks.landmark[13].x, hand_landmarks.landmark[13].y],
        [hand_landmarks.landmark[14].x, hand_landmarks.landmark[14].y],
        [hand_landmarks.landmark[16].x, hand_landmarks.landmark[16].y]
    )

    # Jari Kelingking (landmark 17, 18, 20)
    pinky_angle = calculate_angle(
        [hand_landmarks.landmark[17].x, hand_landmarks.landmark[17].y],
        [hand_landmarks.landmark[18].x, hand_landmarks.landmark[18].y],
        [hand_landmarks.landmark[20].x, hand_landmarks.landmark[20].y]
    )

    # Jari Jempol (landmark 1, 2, 4)
    thumb_angle = calculate_angle(
        [hand_landmarks.landmark[1].x, hand_landmarks.landmark[1].y],
        [hand_landmarks.landmark[2].x, hand_landmarks.landmark[2].y],
        [hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y]
    )

    # Gambar landmark pada frame
    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    return index_angle, middle_angle, ring_angle, pinky_angle, thumb_angle

# Mulai deteksi kamera
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Deteksi jari (termasuk kelingking dan jempol) menggunakan MediaPipe
    index_angle, middle_angle, ring_angle, pinky_angle, thumb_angle = detect_fingers(frame)

    if index_angle is None:
        # Jika tidak ada tangan yang terdeteksi, set semua sudut ke 0
        index_angle = middle_angle = ring_angle = pinky_angle = thumb_angle = 0
    else:
        # Normalisasi sudut antara 0 dan 180 derajat
        index_angle = max(0, min(180, 9 / 8 * (index_angle - 170))) 
        middle_angle = max(0, min(180, 9 / 8 * (middle_angle - 170)))
        ring_angle = max(0, min(180, 29 / 32 * (ring_angle - 170)))
        pinky_angle = max(0, min(180, 3 / 4 * (pinky_angle - 170)))
        thumb_angle = max(0, min(180, 9 / 4 * (180 - thumb_angle)))

    # Kirim data ke Arduino
    send_data_to_arduino(index_angle, middle_angle, ring_angle, pinky_angle, thumb_angle)

    # Tampilkan frame video
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
