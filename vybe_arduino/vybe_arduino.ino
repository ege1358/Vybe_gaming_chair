#define INPUT_SIZE 7

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

//String message,actuator;
char *actuator;
int number, value;
char input[INPUT_SIZE+1];
const int pwmPin[6] = {3,5,6,9,10,11};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  input[INPUT_SIZE] = " ";
  for(int i = 0; i < 6; i++) {
    vc[i].setNumber((i+1));
    vc[i].setValue(0);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) {
    Serial.readBytesUntil('\n',input, INPUT_SIZE);
    actuator = strtok(input, " ");
    Serial.println(actuator);
    number = atoi(strtok(NULL, " "));
    Serial.println(number);
    value = input[6];
    Serial.println(value);
    
    
    /*message = Serial.readBytesUntil('\n');
    actuator = message.substring(0,3);
    Serial.println(actuator);
    number = message.substring(4,5).toInt();
    Serial.println(number);
    message = message.substring(6);
    value = message.toInt();
    Serial.println(value);*/
  }
  if(!strcmp(actuator, "VCL")) {
    vc[(number-1)].setValue(value);
    actuator = "";
  }
  else if(!strcmp(actuator, "MTR")) {
    analogWrite(pwmPin[number-1], value);
  }

  for(int j = 0; j < 6; j++) {
    vc[j].loopUpdate();
  }
  
}
