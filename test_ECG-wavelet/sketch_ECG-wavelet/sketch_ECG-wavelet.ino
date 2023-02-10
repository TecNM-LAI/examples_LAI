const char ECG_Pin = 15;
unsigned int ECG = 0;
unsigned char serByte= 0;



void setup() {
  Serial.begin(115200);
  delay(1000);
}

void loop() {
  if(Serial.available() > 0){
    if(Serial.read() == ';'){
      ECG = analogRead(ECG_Pin);
      Serial.println(ECG);
    }
  }
}
