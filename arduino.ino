void setup() {
  Serial.begin(9600);
}

void loop() {
  int type = get_int();  // digital - analog
  Serial.println(type);
  int io = get_int();  // output - input
  Serial.println(io);
  int port = get_int();
  Serial.println(port);
  int data = get_int();
  Serial.println(data);
  int value = LOW;
  if (data == 1) {
    value = HIGH;
  }
  if (io == 0) {
    pinMode(port, OUTPUT);
  } else {
    pinMode(port, INPUT);
  }
  if (type == 0) {
    if (io == 0) {
      digitalWrite(port, value);
    } else {
      Serial.println(digitalRead(port));
    }
  } else {
    if (io == 0) {
      analogWrite(port, data);
    } else {
      Serial.println(analogRead(port));
    }
  }
}

int get_int() {
  while (!Serial.available()) {
    continue;
  }
  return Serial.parseInt();
}
