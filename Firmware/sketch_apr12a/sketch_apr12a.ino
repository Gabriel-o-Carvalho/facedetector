const int Tranca = 8;
char comando;

void setup() {
  pinMode(Tranca, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    comando = Serial.read();

    if (comando == '1') {
      digitalWrite(Tranca, HIGH);  // abre a tranca
      delay(5000);                 // mantém aberta por 5 segundos
      digitalWrite(Tranca, LOW);   // fecha a tranca
    }
    else digitalWrite(Tranca,LOW);
  }
}