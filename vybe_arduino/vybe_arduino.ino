class Voicecoil {
  int num;
  int pin;
  int val;
  int state = LOW;
  unsigned long currentMillis;
  unsigned long previousMillis;
  
  public:
    void setNumber(int number) {
       num = number;
       pin = num + 13;
    }
    void setValue(int value) {
      val = value;
    }
    void loopUpdate() {
      currentMillis = millis();
      if (currentMillis - previousMillis >= 8) {
        // save the last time you blinked the LED
        previousMillis = currentMillis;
        // if the LED is off turn it on and vice-versa:
        if (state == LOW) {
          analogWrite(pin, val);
            state = HIGH;
        } else {
          analogWrite(pin, 0);
            state = LOW;
        }
      }
    }
} vc[6];

String message, actuator;
int number, value;
const int pwmPin[6] = {3,5,6,9,10,11};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i = 0; i < 6; i++) {
    vc[i].setNumber((i+1));
    vc[i].setValue(0);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  /*if(Serial.available()) {
    message = Serial.readStringUntil('\n');
    actuator = message.substring(0,3);
    message = message.substring(3);
    number = message.substring(0, message.indexOf(" ")).toInt();
    message = message.substring(message.indexOf(" "));
    message.trim();
    value = message.toInt();
  }*/
  actuator = "VCL";
  number = 1;
  value = 255;
  if(actuator == "VCL") {
    vc[(number-1)].setValue(value);
    actuator = "";
  }
  else if(actuator == "MTR") {
    analogWrite(pwmPin[number-1], value);
  }

  for(int j = 0; j < 6; j++) {
    vc[j].loopUpdate();
  }
  
}
