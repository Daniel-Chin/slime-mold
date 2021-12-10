#define PEACEFUL_GROWTH 480
#define ON 30
#define OFF 30
#define N_TRAIN_PERIODS 10
#define LED_PIN 3
#define DEBUG true

void setup() {
  pinMode(LED_PIN, OUTPUT);
  if (DEBUG) Serial.begin(9600);
}

void loop() {
  long seconds = millis() / 1000;
  long minutes = seconds / 60;
  if (minutes < PEACEFUL_GROWTH) {
    analogWrite(LED_PIN, 0);
  } else {
    minutes -= PEACEFUL_GROWTH;
    int n_per = minutes / (ON + OFF);
    if (n_per < N_TRAIN_PERIODS) {
      int phase = minutes % (ON + OFF);
      if (phase < ON) {
        analogWrite(LED_PIN, 200);
      } else {
        analogWrite(LED_PIN, 0);
      }
    } else {
      analogWrite(LED_PIN, 0);
    }
  }
  if (DEBUG) {
    Serial.print("ms: ");
    Serial.print(int(millis()));
    Serial.print(" sec: ");
    Serial.print(seconds);
    Serial.print(" min; ");
    Serial.println(minutes);
  }
}
