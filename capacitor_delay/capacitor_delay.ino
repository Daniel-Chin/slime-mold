void setup() {
  pinMode(9, OUTPUT);
  Serial.begin(9600);
}

bool x = true;
void loop() {/*
  if (Serial.available() > 0) {
    Serial.read();
    x = !x;
    Serial.println(x);
  }
  digitalWrite(9, x);
  return;*/
  int x = analogRead(A0);
  if (x < 150) {
    digitalWrite(9, HIGH);
  }
  if (x > 1023 - 150) {
    digitalWrite(9, LOW);
  }
  Serial.println(x);
}
