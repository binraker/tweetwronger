//digispark code to act as a latch for the TW ready line so that the hoast computer never misses it.
const int input = 0;
const int output = 1;
const int rset = 2;
void setup() {
  pinMode(input, INPUT);
  pinMode(output, OUTPUT);
  pinMode(rset, INPUT);
  
}
void loop() {
  if (digitalRead(input) == HIGH)
  {
    digitalWrite(output, HIGH);
  }
  if (digitalRead(rset) == HIGH and digitalRead(input) == LOW)
  {
    digitalWrite(output, LOW);
  } 
}
