# Smart Security System

A security system that detects motion, recognizes faces, and sends an alert on Telegram.

**How it works**

1. An Arduino with a motion sensor detects movement and sends `MOTION` to the PC.
2. The PC takes a photo with the webcam.
3. The face is compared with the photos in the `authorized/` folder.
4. The Arduino lights a LED (`OK` = known person, `ALARM` = unknown person).
5. The photo and a message are sent to your Telegram chat.

Documentation: see the [`docs/`](docs) folder (project report and presentation).

## Hardware

- Arduino board (connected by USB)
- Motion input on pin 2 (push button or motion sensor)
- Green LED (pin 12, authorized) and red LED (pin 13, alarm), with resistors
- Webcam

See [`arduino/README.md`](arduino) for the wiring.

## Installation

1. Install **Python 3.10** (recommended).
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. `face_recognition` needs **dlib**, which can be hard to install on Windows.
   If the install fails, install a pre-built dlib wheel for your Python version
   (for example `dlib-19.22.99-cp310-cp310-win_amd64.whl` for Python 3.10 on 64-bit Windows):
   ```bash
   pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
   pip install -r requirements.txt
   ```
   On Linux/macOS you need CMake: `pip install cmake` then `pip install dlib`.
4. Upload `arduino/securite/securite.ino` to your Arduino with the Arduino IDE.

## Configuration

1. Create a Telegram bot: open **@BotFather**, send `/newbot`, and copy the token.
2. Find your chat ID (for example with **@userinfobot**).
3. Copy `.env.example` to `.env` and fill in your values:
   ```
   BOT_TOKEN=your_token_from_botfather
   CHAT_ID=your_chat_id
   ARDUINO_PORT=COM9
   ```
   Change `ARDUINO_PORT` to the port of your Arduino (see the Arduino IDE).
4. Put one clear photo (`.jpg` or `.png`) of each authorized person in the `authorized/` folder.
   The file name is used as the person's name (for example `Sara.jpg`).

> Never share your `.env` file or your bot token.

## Run

```bash
python main.py
```

Press `Ctrl+C` to stop.

## Project structure

```
├── main.py              # Main program
├── requirements.txt     # Python dependencies
├── .env.example         # Example configuration
├── arduino/securite/    # Arduino sketch (securite.ino)
├── authorized/          # Photos of authorized people (not published)
└── docs/                # Report and presentation
```
