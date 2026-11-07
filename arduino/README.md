# Arduino code

Sketch: [`securite/securite.ino`](securite/securite.ino)

Open it in the Arduino IDE, select your board and port, then click **Upload**.
(The sketch must stay inside a folder with the same name, `securite`, for the Arduino IDE to open it.)

## Wiring

| Arduino pin | Connected to |
|---|---|
| 2 | Motion input (push button or sensor), the other side goes to GND |
| 12 | Green LED (authorized), through a resistor (about 220 Ω) |
| 13 | Red LED (alarm), through a resistor (about 220 Ω) |

Pin 2 uses `INPUT_PULLUP`, so motion is detected when the pin goes **LOW** (connected to GND).

## Serial messages (9600 baud)

| Direction | Message | Meaning |
|---|---|---|
| Arduino → PC | `MOTION` | Motion detected |
| PC → Arduino | `OK` | Face recognized: green LED on, red LED off |
| PC → Arduino | `ALARM` | Unknown face: red LED on, green LED off |

Each message ends with a new line (`\n`).
