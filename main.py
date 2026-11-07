import os
import time

import cv2
import numpy as np
import serial
import face_recognition
from dotenv import load_dotenv
from telegram import Bot

# ===============================
# Configuration (read from the .env file)
# ===============================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ARDUINO_PORT = os.getenv("ARDUINO_PORT", "COM9")
AUTHORIZED_DIR = os.getenv("AUTHORIZED_DIR", "authorized")

if not BOT_TOKEN or not CHAT_ID:
    raise SystemExit(
        "BOT_TOKEN or CHAT_ID is missing. Copy .env.example to .env and fill it in."
    )

bot = Bot(token=BOT_TOKEN)

# ===============================
# Load known faces
# ===============================
known_faces = []
known_names = []

os.makedirs(AUTHORIZED_DIR, exist_ok=True)
files = [f for f in os.listdir(AUTHORIZED_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

for f in files:
    try:
        img = cv2.imread(os.path.join(AUTHORIZED_DIR, f), cv2.IMREAD_UNCHANGED)

        if img is None:
            print(f"⚠ Cannot read {f}, image skipped")
            continue

        if img.dtype != np.uint8:
            img = (255 * img).astype(np.uint8)

        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        elif img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            print(f"⚠ Unknown format for {f}, image skipped")
            continue

        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 0:
            known_faces.append(encodings[0])
            known_names.append(os.path.splitext(f)[0])
        else:
            print(f"⚠ No face detected in {f}")

    except Exception as e:
        print(f"⚠ Error with {f}: {e}")

print(f"✅ {len(known_faces)} known face(s) loaded.")
if not known_faces:
    print("⚠ No authorized faces found: everyone will be treated as unknown.")

# ===============================
# Arduino connection
# ===============================
try:
    arduino = serial.Serial(ARDUINO_PORT, 9600)
    time.sleep(2)
    print(f"✅ Arduino connected on {ARDUINO_PORT}\n")
except Exception as e:
    raise SystemExit(f"⚠ Cannot open {ARDUINO_PORT}: {e}")

# ===============================
# Camera
# ===============================
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    arduino.close()
    raise SystemExit("Cannot open the camera!")


# ===============================
# Face recognition
# ===============================
def recognize(frame):
    """Return the name of the recognized person, or "INCONNU" if unknown."""
    if frame is None or not known_faces:
        return "INCONNU"

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for enc in encodings:
        matches = face_recognition.compare_faces(known_faces, enc)
        distances = face_recognition.face_distance(known_faces, enc)

        if True in matches:
            return known_names[int(np.argmin(distances))]

    return "INCONNU"


# ===============================
# Main loop
# ===============================
try:
    while True:
        if arduino.in_waiting > 0:
            message = arduino.readline().decode(errors="ignore").strip()

            if message == "MOTION":
                print("➡ Motion detected!")

                ret, frame = cam.read()
                if not ret:
                    print("Camera error.")
                    continue

                cv2.imwrite("capture.jpg", frame)

                person = recognize(frame)

                if person != "INCONNU":
                    text = f"✔ Known person: {person}"
                    arduino.write(b"OK\n")      # authorized LED
                else:
                    text = "⚠ Unknown person!!!"
                    arduino.write(b"ALARM\n")   # alarm LED

                # Telegram alert
                try:
                    with open("capture.jpg", "rb") as photo:
                        bot.send_photo(chat_id=CHAT_ID, photo=photo)
                    bot.send_message(chat_id=CHAT_ID, text=text)
                    print(f"📩 Telegram sent: {text}")
                except Exception as e:
                    print(f"Telegram error: {e}")

                time.sleep(3)

        time.sleep(0.05)  # avoid using 100% of the CPU

except KeyboardInterrupt:
    print("Manual stop.")

finally:
    cam.release()
    arduino.close()
    print("Everything closed.")
