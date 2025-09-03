

int trig=10;
int echo=11;
int distance=0;
float ult=0.034;//0.034 cm per microsecond
unsigned long pulsetime;

void setup() {
  pinMode(trig,OUTPUT);
  pinMode(echo,INPUT);
  Serial.begin(9600);
  Serial.println("*****************SPEED IN cm/s*****************"); 
}

void loop() {

digitalWrite(trig,LOW);
digitalWrite(trig,HIGH);
digitalWrite(trig,LOW);

pulsetime=pulseIn(echo,HIGH);
int d;
float speed;
d=(int)(ult*pulsetime)/2;
speed=abs(distance-d)/1;
distance=d;
Serial.println(speed);
delay(1000);

}
