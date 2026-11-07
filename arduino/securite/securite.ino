// Détection PIR / bouton poussoir
int pirPin = 2;

// LEDs
int ledAutorisee = 12;     // LED verte
int ledNonAutorisee = 13;  // LED rouge

void setup() {
  pinMode(pirPin, INPUT_PULLUP);
  pinMode(ledAutorisee, OUTPUT);
  pinMode(ledNonAutorisee, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int etat = digitalRead(pirPin);

  if (etat == LOW) {
    Serial.println("MOTION");
    delay(500);
  }

  // Lecture du message Python
  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();  // enlève les espaces / retours chariot éventuels

    if (msg == "OK") {
      digitalWrite(ledAutorisee, HIGH);
      digitalWrite(ledNonAutorisee, LOW);
    }
    else if (msg == "ALARM") {
      digitalWrite(ledNonAutorisee, HIGH);
      digitalWrite(ledAutorisee, LOW);
    }
  }
}
