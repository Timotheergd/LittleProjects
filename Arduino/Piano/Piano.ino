#include <RGBLed.h>
#include <CapacitiveSensor.h>
#include "pitches.h"

/*
 * Piano 
 */

//CapacitiveSensor cs_1 = CapacitiveSensor(2,3);
CapacitiveSensor cs_1 = CapacitiveSensor(A5,3);//10M Resistor between pins 7 and 8, you may also connect an antenna on pin 8
//CapacitiveSensor cs_2 = CapacitiveSensor(4,5);
CapacitiveSensor cs_2 = CapacitiveSensor(A4,4);
CapacitiveSensor cs_3 = CapacitiveSensor(A3,5);
CapacitiveSensor cs_4 = CapacitiveSensor(A2,6);
CapacitiveSensor cs_5 = CapacitiveSensor(A1,7);
CapacitiveSensor cs_6 = CapacitiveSensor(A0,12);

unsigned long csSum1;
unsigned long csSum2;
unsigned long csSum3;
unsigned long csSum4;
unsigned long csSum5;
unsigned long csSum6;

//definition des pins des buttons
/*int const buttonPin1 = 2;
int const buttonPin2 = 3;
int const buttonPin3 = 4;
int const buttonPin4 = 5;
int const buttonPin5 = 6;
int const buttonPin6 = 7;
int const buttonPin7 = 12;*/

//definition des etats des buttons
boolean buttonState1 = false;
boolean buttonState2 = false;
boolean buttonState3 = false;
boolean buttonState4 = false;
boolean buttonState5 = false;
boolean buttonState6 = false;
boolean buttonState7 = false;

const int c = 261;
const int d = 294;
const int e = 329;
const int f = 349;
const int g = 391;
const int gS = 415;
const int a = 440;
const int aS = 455;
const int b = 466;
const int cH = 523;
const int cSH = 554;
const int dH = 587;
const int dSH = 622;
const int eH = 659;
const int fH = 698;
const int fSH = 740;
const int gH = 784;
const int gSH = 830;
const int aH = 880;

const int ledPin1 = 13;
const int ledPin2 = 13;
 
int counter = 0;

//definition de la pin du buzzer
int buzzerPin = 9;

//definition des pin des rgb
int const redPin = 8;
int const greenPin = 10;
int const bluePin = 11;

int const potarPin = A6;
int const potarPin2 = A7;

int i = 0;
int Vr = 0, Vg = 0, Vb = 0;
int nbRand, old_nbRand;
unsigned long tpsBtt7 = 0;
//unsigned long delayNoTone = millis();

int potar = analogRead(potarPin);
int potar2 = analogRead(potarPin2);

//RGBLed led(redPin, greenPin, bluePin, COMMON_ANODE);


//Bitch lasagna + crab song main theme melody
int melody[] = {
 
  NOTE_FS7, NOTE_FS7, NOTE_GS7,  NOTE_A7,
  NOTE_A7,  NOTE_A7, NOTE_D7, NOTE_D7,
  NOTE_CS7, NOTE_CS7, NOTE_CS7,  NOTE_E7,
  NOTE_E7, NOTE_E7, NOTE_E7, NOTE_E7,
 
  NOTE_FS7, NOTE_FS7, NOTE_GS7,  NOTE_A7,
  NOTE_A7,  NOTE_A7, NOTE_D7, NOTE_D7,
  NOTE_CS7, NOTE_CS7, NOTE_CS7,  NOTE_E7,
  NOTE_E7, NOTE_E7, NOTE_E7, NOTE_E7,
 
  
  /*NOTE_D7, NOTE_AS7, NOTE_G7,  NOTE_G7,
  NOTE_D7,  NOTE_D7, NOTE_A7, NOTE_F7,
  NOTE_F7, NOTE_D7, NOTE_D7,  NOTE_A7,
  NOTE_F7, NOTE_F7, NOTE_C7, NOTE_C7,
 
  NOTE_E7, NOTE_E7, NOTE_F7,
 
  NOTE_D7, NOTE_AS7, NOTE_G7,  NOTE_G7,
  NOTE_D7,  NOTE_D7, NOTE_A7, NOTE_F7,
  NOTE_F7, NOTE_D7, NOTE_D7,  NOTE_A7,
  NOTE_F7, NOTE_F7, NOTE_C7, NOTE_C7,
 
  NOTE_E7, NOTE_E7, NOTE_F7,*/
 
  /*NOTE_D7, NOTE_AS7, NOTE_G7,  NOTE_G7,
  NOTE_D7,  NOTE_D7, NOTE_A7, NOTE_F7,
  NOTE_F7, NOTE_D7, NOTE_D7,  NOTE_A7,
  NOTE_F7, NOTE_F7, NOTE_C7, NOTE_C7,*/
 
  //NOTE_E7, NOTE_E7, NOTE_F7,
 
 
};
//Bitch lasagna + crab song tempo
int tempo[] = {
  6, 6, 6, 6,
  6, 6, 6, 6,
  6, 6, 6, 6,
  6, 6, 6, 6,
 
  6, 6, 6, 6,
  6, 6, 6, 6,
  6, 6, 6, 6,
  6, 6, 6, 6,
 
  8, 8, 8, 12,
  8, 12, 8, 8,
  12, 8, 12, 8,
  8, 12, 8, 8,
  8, 12, 8,
 
  8, 8, 8, 12,
  8, 12, 8, 8,
  12, 8, 12, 8,
  8, 12, 8, 8,
  8, 12, 8,
 
  /*8, 8, 8, 12,
  8, 12, 8, 8,
  12, 8, 12, 8,
  8, 12, 8, 8,
  //8, 12, 8,*/
 
 
};

int melody2[] = {
  NOTE_E7, NOTE_E7, 0, NOTE_E7,
  0, NOTE_C7, NOTE_E7, 0,
  NOTE_G7, 0, 0,  0,
  NOTE_G6, 0, 0, 0,
 
  NOTE_C7, 0, 0, NOTE_G6,
  0, 0, NOTE_E6, 0,
  0, NOTE_A6, 0, NOTE_B6,
  0, NOTE_AS6, NOTE_A6, 0,
 
  NOTE_G6, NOTE_E7, NOTE_G7,
  NOTE_A7, 0, NOTE_F7, NOTE_G7,
  0, NOTE_E7, 0, NOTE_C7,
  NOTE_D7, NOTE_B6, 0, 0,
 
  NOTE_C7, 0, 0, NOTE_G6,
  0, 0, NOTE_E6, 0,
  0, NOTE_A6, 0, NOTE_B6,
  0, NOTE_AS6, NOTE_A6, 0,
 
  NOTE_G6, NOTE_E7, NOTE_G7,
  NOTE_A7, 0, NOTE_F7, NOTE_G7,
  0, NOTE_E7, 0, NOTE_C7,
  NOTE_D7, NOTE_B6, 0, 0
};
//Mario main them tempo
int tempo2[] = {
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
};
//Underworld melody
int underworld_melody2[] = {
  NOTE_C4, NOTE_C5, NOTE_A3, NOTE_A4,
  NOTE_AS3, NOTE_AS4, 0,
  0,
  NOTE_C4, NOTE_C5, NOTE_A3, NOTE_A4,
  NOTE_AS3, NOTE_AS4, 0,
  0,
  NOTE_F3, NOTE_F4, NOTE_D3, NOTE_D4,
  NOTE_DS3, NOTE_DS4, 0,
  0,
  NOTE_F3, NOTE_F4, NOTE_D3, NOTE_D4,
  NOTE_DS3, NOTE_DS4, 0,
  0, NOTE_DS4, NOTE_CS4, NOTE_D4,
  NOTE_CS4, NOTE_DS4,
  NOTE_DS4, NOTE_GS3,
  NOTE_G3, NOTE_CS4,
  NOTE_C4, NOTE_FS4, NOTE_F4, NOTE_E3, NOTE_AS4, NOTE_A4,
  NOTE_GS4, NOTE_DS4, NOTE_B3,
  NOTE_AS3, NOTE_A3, NOTE_GS3,
  0, 0, 0
};
//Underwolrd tempo
int underworld_tempo2[] = {
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  6, 18, 18, 18,
  6, 6,
  6, 6,
  6, 6,
  18, 18, 18, 18, 18, 18,
  10, 10, 10,
  10, 10, 10,
  3, 3, 3
};

char names[] = { 'a', 'b', 'c', 'd', 'e', 'f', 'g'};
int tones[] = { 110, 123, 131, 147, 165, 175, 196 };
int tonesDiese[] = {117,0,139,156,0,185,208};
int tempo3 = 120;//double croche
unsigned long delayNoTone = millis();

void playNote(char note, int octave, int duration, boolean diese=false) {
  // play the tone corresponding to the note name
    int i=0;
    while((names[i]!=note) && (i<7)){
     i++; 
    }
    if (diese) {
      tone(buzzerPin,tonesDiese[i] * octave, duration * tempo3);
    }else{
      tone(buzzerPin,(tones[i] * octave), duration * tempo3);
    }
    delay(duration * tempo3);
    noTone(buzzerPin);
}

void setup() {

  Serial.begin(9600);

  //led.off();
  
  //definition des bouttons comme des entrees
  /*pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);
  pinMode(buttonPin4, INPUT);
  pinMode(buttonPin5, INPUT);
  pinMode(buttonPin6, INPUT);
  pinMode(buttonPin7, INPUT);*/

  ///definition du buzzer et des leds comme sorties
  pinMode(buzzerPin, OUTPUT);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  //led.setColor(RGBLed::WHITE);
}

void loop() {
/*  V1
  buttonState1 = digitalRead(buttonPin1);
  if(buttonState1){
    Serial.println("1");
    //tone(buzzerPin, NOTE_DO5, 500);
    tone(buzzerPin, NOTE_REd8, 500);
    //delay(N*150);
    led.fadeIn(RGBLed::RED, 5, 25);
    //noTone(buzzerPin);
    //led.fadeIn(RGBLed::RED, 5, 50);
  }
    
  buttonState2 = digitalRead(buttonPin2);
  if(buttonState2){
    Serial.println("2");
    tone(buzzerPin, NOTE_LA4, 500);
    led.fadeIn(RGBLed::GREEN, 5, 40);
    //noTone(buzzerPin);
  }
  
  buttonState3 = digitalRead(buttonPin3);
  if(buttonState3){
    Serial.println("3");
    tone(buzzerPin, NOTE_SOL4, 500);
    led.fadeIn(RGBLed::YELLOW, 5, 40);
    noTone(buzzerPin);
  }
  
  buttonState4 = digitalRead(buttonPin4);
  if(buttonState4){
    Serial.println("4");
    tone(buzzerPin, NOTE_FA4, 500);
    led.fadeIn(RGBLed::RED, 5, 50);
    //noTone(buzzerPin);
  }
  
  buttonState5 = digitalRead(buttonPin5);
  if(buttonState5){
    Serial.println("5");
    tone(buzzerPin, NOTE_RE4, 500);
    led.fadeIn(RGBLed::GREEN, 5, 50);
    //noTone(buzzerPin);
  }
  
  buttonState6 = digitalRead(buttonPin6);
  if(buttonState6)  {
    Serial.println("6");
    tone(buzzerPin, NOTE_DO4, 500);
    led.fadeIn(RGBLed::RED, 5, 50);
    //noTone(buzzerPin);
  }

  buttonState7 = digitalRead(buttonPin7);
  if(buttonState7)  {
    Serial.println("7");
    //tone(buzzerPin, NOTE_LA3, 500);
    tone(buzzerPin, NOTE_SI0, 500);
    led.fadeIn(RGBLed::YELLOW, 5, 40);
    //noTone(buzzerPin);
  }
  */

/*  V2
  buttonState1 = digitalRead(buttonPin1);
  if(buttonState1){
    Serial.println("1");
    tone(buzzerPin, NOTE_DO5, 500);
//    noTone(buzzerPin);
  }
    
  buttonState2 = digitalRead(buttonPin2);
  if(buttonState2){
    Serial.println("2");
    tone(buzzerPin, NOTE_LA4, 500);
//    noTone(buzzerPin);
  }
  
  buttonState3 = digitalRead(buttonPin3);
  if(buttonState3){
    Serial.println("3");
    tone(buzzerPin, NOTE_SOL4, 500);
//    noTone(buzzerPin);
  }
  
  buttonState4 = digitalRead(buttonPin4);
  if(buttonState4){
    Serial.println("4");
    tone(buzzerPin, NOTE_FA4, 500);
//    noTone(buzzerPin);
  }
  
  buttonState5 = digitalRead(buttonPin5);
  if(buttonState5){
    Serial.println("5");
    tone(buzzerPin, NOTE_RE4, 500);
//    noTone(buzzerPin);
  }
  
  buttonState6 = digitalRead(buttonPin6);
  if(buttonState6)  {
    Serial.println("6");
    tone(buzzerPin, NOTE_DO4, 500);
//    noTone(buzzerPin);
  }

  buttonState7 = digitalRead(buttonPin7);
  if(buttonState7)  {
    Serial.println("7");
    tone(buzzerPin, NOTE_LA3, 500);
//    noTone(buzzerPin);
  }

  int nbRand = random(6);
  Serial.println("rand = " + String(nbRand));

  switch(nbRand){

    case 0:
       led.fadeIn(RGBLed::RED, 10, 50);
       break;

    case 1:
       led.fadeIn(RGBLed::GREEN, 10, 50);
       break;

    case 2:
       //led.fadeIn(RGBLed::BLUE, 10, 50);
       break;

    case 3:
       //led.fadeIn(RGBLed::MAGENTA, 5, 50);
       break;

    case 4:
       //led.fadeIn(RGBLed::CYAN, 5, 50);
       break;

    case 5:
       led.fadeIn(RGBLed::YELLOW, 10, 50);
       break;

    case 6:
      // led.fadeIn(RGBLed::WHITE, 5, 50);
       break;
    }
*/

/*  V3
    buttonState1 = digitalRead(buttonPin1);
  if(buttonState1){
    Serial.println("1");
    tone(buzzerPin, NOTE_DO5, 500);
//    noTone(buzzerPin);
  }
    
  buttonState2 = digitalRead(buttonPin2);
  if(buttonState2){
    Serial.println("2");
    tone(buzzerPin, NOTE_LA4, 500);
//    noTone(buzzerPin);
  }
  
  buttonState3 = digitalRead(buttonPin3);
  if(buttonState3){
    Serial.println("3");
    tone(buzzerPin, NOTE_SOL4, 500);
//    noTone(buzzerPin);
  }
  
  buttonState4 = digitalRead(buttonPin4);
  if(buttonState4){
    Serial.println("4");
    tone(buzzerPin, NOTE_FA4, 500);
//    noTone(buzzerPin);
  }
  
  buttonState5 = digitalRead(buttonPin5);
  if(buttonState5){
    Serial.println("5");
    tone(buzzerPin, NOTE_RE4, 500);
//    noTone(buzzerPin);
  }
  
  buttonState6 = digitalRead(buttonPin6);
  if(buttonState6)  {
    Serial.println("6");
    tone(buzzerPin, NOTE_DO4, 500);
//    noTone(buzzerPin);
  }

  buttonState7 = digitalRead(buttonPin7);
  if(buttonState7)  {
    Serial.println("7");
    tone(buzzerPin, NOTE_LA3, 500);
//    noTone(buzzerPin);
  }


  if(i>255){
    while(nbRand == old_nbRand){
      nbRand = random(3);
    }
    old_nbRand = nbRand;
    Serial.println("rand = " + String(nbRand));
    i = 0;
  }
    switch(nbRand){
  
      case 0:
         //led.fadeIn(RGBLed::RED, 10, 50);
         //led.setColor(RGBLed::RED);
         if(Vr >= 255)  analogWrite(redPin, 255-i);
         else analogWrite(redPin, 0);
         if(Vg >= 255)  analogWrite(greenPin, 255);
         else analogWrite(greenPin, i);
         if(Vb >= 255)  analogWrite(bluePin, 255);
         else analogWrite(bluePin, i);
         break;
  
      case 1:
         //led.fadeIn(RGBLed::GREEN, 10, 50);
         //led.setColor(RGBLed::GREEN);
         //Vr = 255;
         //Vg = 0;
         //Vb = 255;
         //analogWrite(redPin, Vr);
         //analogWrite(greenPin, Vg);
         //analogWrite(bluePin, Vb);
         if(Vr >= 255)  analogWrite(redPin, 255);
         else analogWrite(redPin, i);
         if(Vg >= 255)  analogWrite(greenPin, 255-i);
         else analogWrite(greenPin, 0);
         if(Vb >= 255)  analogWrite(bluePin, 255);
         else analogWrite(bluePin, i);
         break;
  
      case 2:
         //led.fadeIn(RGBLed::BLUE, 10, 50);
         //led.setColor(RGBLed::BLUE);
         //Vr = 255;
         //Vg = 255;
         //Vb = 0;
         //analogWrite(redPin, Vr);
         //analogWrite(greenPin, Vg);
         //analogWrite(bluePin, Vb);
         if(Vr >= 255)  analogWrite(redPin, 255);
         else analogWrite(redPin, i);
         if(Vg >= 255)  analogWrite(greenPin, 255);
         else analogWrite(greenPin, i);
         if(Vb >= 255)  analogWrite(bluePin, 255-i);
         else analogWrite(bluePin, 0);
         break;
  
      case 3:
         //led.fadeIn(RGBLed::MAGENTA, 5, 50);
         break;
  
      case 4:
         //led.fadeIn(RGBLed::CYAN, 5, 50);
         break;
  
      case 5:
         //led.fadeIn(RGBLed::YELLOW, 10, 50);
         break;
  
      case 6:
        // led.fadeIn(RGBLed::WHITE, 5, 50);
         break;
      }
    i++;
    if(i%20 == 0) Serial.println("i = " + String(i));
    delay(100);
    */
    
//  V4


  potar = analogRead(potarPin);
  potar = map(potar, 0, 1023, 0, 4500);
 // Serial.println("potar 1 = " + String(potar));
                                                                                                                                                                  
//potar =1500;
  
  CSread1();
  CSread2();
  CSread3();
  CSread4();
  CSread5();
  CSread6();
 

  if(buttonState5 == true && buttonState6 == true){
    buttonState7 = true;
    buttonState5 = false;
    buttonState6 = false;
    tpsBtt7 = millis();
    }
    else if(tpsBtt7 > 1000)  buttonState7 = false;

//buttonState1 = digitalRead(buttonPin1);
  if(buttonState1){
    Serial.println("1");
    tone(buzzerPin, NOTE_LA3);
    delayNoTone = millis();
    Serial.println("BIPPPPPPPPPPP");
    //tone(buzzerPin, NOTE_LA3);
//    noTone(buzzerPin);
  }

    
 // buttonState2 = digitalRead(buttonPin2);
  if(buttonState2){
    Serial.println("2");
    tone(buzzerPin, NOTE_DO4);
    delayNoTone = millis();
    Serial.println("BIPPPPPPPPPPP");
//    noTone(buzzerPin);
  }
  
 // buttonState3 = digitalRead(buttonPin3);
  if(buttonState3){
    Serial.println("3");
    tone(buzzerPin, NOTE_RE4);
    delayNoTone = millis();
    Serial.println("BIPPPPPPPPPPP");
//    noTone(buzzerPin);
  }
 // buttonState4 = digitalRead(buttonPin4);
  if(buttonState4){
    Serial.println("4");
    tone(buzzerPin, NOTE_FA4);
    delayNoTone = millis();
    Serial.println("BIPPPPPPPPPPP");
//    noTone(buzzerPin);
  }
  
//  buttonState5 = digitalRead(buttonPin5);
  if(buttonState5){
    Serial.println("5");
    tone(buzzerPin, NOTE_SOL4);
    delayNoTone = millis();
    Serial.println("BIPPPPPPPPPPP");
//    noTone(buzzerPin);
  }
  
  //buttonState6 = digitalRead(buttonPin6);
  if(buttonState6)  {
    Serial.println("6");
    tone(buzzerPin, NOTE_LA4);
    delayNoTone = millis();
    Serial.println("BIPPPPPPPPPPP");
//    noTone(buzzerPin);
  }

 // buttonState7 = digitalRead(buttonPin7);
  if(buttonState7)  {
    Serial.println("7");
    tone(buzzerPin, NOTE_DO5);
    delayNoTone = millis();
    Serial.println("BIPPPPPPPPPPP");
//    noTone(buzzerPin);

  }

  //Serial.println("delayNoTone = " + String(delayNoTone) + "/// millis = " + String(millis()));
/*  Serial.println("buttonState1 = " + String(buttonState1));
  Serial.println("buttonState2 = " + String(buttonState2));
  Serial.println("buttonState3 = " + String(buttonState3));
  Serial.println("buttonState4 = " + String(buttonState4));
  Serial.println("buttonState5 = " + String(buttonState5));
  Serial.println("buttonState6 = " + String(buttonState6));
  Serial.println("buttonState7 = " + String(buttonState7));*/

  /*if(((delayNoTone + 1000) > millis()) && (!buttonState1) && (!buttonState2) && (!buttonState3) && (!buttonState4) && (!buttonState5) && (!buttonState6) && (!buttonState7))
    {
      noTone(buzzerPin);
      
      Serial.println("stoppppppppppppppppp");
    }*/
//Serial.println("Millis = ");

   if(millis() > (delayNoTone + 250)) 
    {
      noTone(buzzerPin);
      
      //Serial.println("stoppppppppppppppppp");
    }
  
  //Serial.println("rand = " + String(nbRand));
  /*if(buttonState1 || buttonState2 || buttonState3 || buttonState4 || buttonState5 || buttonState6){

    while(nbRand == old_nbRand){
        nbRand = random(3);
      }
      old_nbRand = nbRand;
      
    switch(nbRand){

      case 0:
         led.setColor(RGBLed::RED);
         break;
  
      case 1:
         led.setColor(RGBLed::GREEN);
         break;
  
      case 2:
         //led.setColor(RGBLed::BLUE);
         led.setColor(RGBLed::YELLOW);
         break;
  
      case 3:
         //led.fadeIn(RGBLed::MAGENTA, 5, 50);
         break;
  
      case 4:
         //led.fadeIn(RGBLed::CYAN, 5, 50);
         break;
  
      case 5:
         led.setColor(RGBLed::YELLOW);
         break;
  
      case 6:
        // led.fadeIn(RGBLed::WHITE, 5, 50);
         break;
      }
    }*/


//  V5
 /* unsigned long delayNoTone = millis();

  potar = analogRead(potarPin);
  potar = map(potar, 0, 1023, 0, 4500);
  Serial.println("potar 1 = " + String(potar));

  potar2 = analogRead(potarPin2);
  potar2 = map(potar2, 0, 1023, 0, 4);
  Serial.println("potar 2 = " + String(potar2));
  switch(potar2){

    case 0:
      Serial.println("musique 0");

      CSread1();
      CSread2();
      CSread3();
      CSread4();
      CSread5();
      CSread6();
    
      if(buttonState5 == true && buttonState6 == true){
        buttonState7 = true;
        buttonState5 = false;
        buttonState6 = false;
        tpsBtt7 = millis();
        }
        else if(tpsBtt7 > 1000)  buttonState7 = false;
    
      if(buttonState1){
        Serial.println("1");
        tone(buzzerPin, NOTE_LA3);
      }
        
      if(buttonState2){
        Serial.println("2");
        tone(buzzerPin, NOTE_DO4);
      }
      
      if(buttonState3){
        Serial.println("3");
        tone(buzzerPin, NOTE_RE4);
      }
      
      if(buttonState4){
        Serial.println("4");
        tone(buzzerPin, NOTE_FA4);
      }
      
      if(buttonState5){
        Serial.println("5");
        tone(buzzerPin, NOTE_SOL4);
      }
      
      if(buttonState6)  {
        Serial.println("6");
        tone(buzzerPin, NOTE_LA4);
      }
    
      if(buttonState7)  {
        Serial.println("7");
        tone(buzzerPin, NOTE_DO5);
      }

      if(((delayNoTone + 300) > millis()) && (!buttonState1) && (!buttonState2) && (!buttonState3) && (!buttonState4) && (!buttonState5) && (!buttonState6) && (!buttonState7))
        {
          noTone(buzzerPin);
          delayNoTone = millis();
          //Serial.print("***stop*************************");
        }
      break;
    
    case 1:
      Serial.println("musique 1");
      sing(1);
      break;

    case 2:
      Serial.println("musique 2");
      sing(2);
      sing(2);
      sing(3);
      break;

    case 3:
      Serial.println("musique 3");
      playNianCat();
      break;

    case 4:
      Serial.println("musique 4");
      //Play first section
      firstSection();
     
      //Play second section
      secondSection();
     
      //Variant 1
      beep(f, 250);  
      beep(gS, 500);  
      beep(f, 350);  
      beep(a, 125);
      beep(cH, 500);
      beep(a, 375);  
      beep(cH, 125);
      beep(eH, 650);
     
      delay(500);
     
      //Repeat second section
      secondSection();
     
      //Variant 2
      beep(f, 250);  
      beep(gS, 500);  
      beep(f, 375);  
      beep(cH, 125);
      beep(a, 500);  
      beep(f, 375);  
      beep(cH, 125);
      beep(a, 650);  
     
      delay(650);
      break;

    case 5:
      Serial.println("musique 5");
      break;

    case 6:
      Serial.println("musique 6");
      break;
    
    }*/
}
//**************************************
//*********** FONCTIONS ****************
//**************************************è
  
void CSread1() {
  long cs1 = cs_1.capacitiveSensor(80); //a: Sensor resolution is set to 80
  //long cs1 = 5;
  //Serial.println("cs1 = " + String(cs1)); 
  if (cs1 > potar) { //b: Arbitrary number
    buttonState1 = true;
    csSum1 += cs1;
    Serial.println(cs1); 
    if (csSum1 >= potar) //c: This value is the threshold, a High value means it takes longer to trigger
    {
      Serial.print("Trigger1: ");
      Serial.println(csSum1);
      if (csSum1 > 0) { csSum1 = 0; } //Reset
      cs_1.reset_CS_AutoCal(); //Stops readings
    }
  } else {
    csSum1 = 0; //Timeout caused by bad readings
    buttonState1 = false;
  }
}

void CSread2() {
  long cs2 = cs_2.capacitiveSensor(80); //a: Sensor resolution is set to 80
  if (cs2 > potar) { //b: Arbitrary number
    buttonState2 = true;
    csSum2 += cs2;
    //Serial.println(cs2); 
    if (csSum2 >= potar) //c: This value is the threshold, a High value means it takes longer to trigger
    {
      Serial.print("Trigger2: ");
      Serial.println(csSum2);
      if (csSum2 > 0) { csSum2 = 0; } //Reset
      cs_2.reset_CS_AutoCal(); //Stops readings
    }
  } else {
    csSum2 = 0; //Timeout caused by bad readings
    buttonState2 = false;
  }
}

void CSread3() {
  long cs3 = cs_3.capacitiveSensor(80); //a: Sensor resolution is set to 80
  if (cs3 > potar) { //b: Arbitrary number
    buttonState3 = true;
    csSum3 += cs3;
    //Serial.println(cs3); 
    if (csSum3 >= potar) //c: This value is the threshold, a High value means it takes longer to trigger
    {
      Serial.print("Trigger3: ");
      Serial.println(csSum3);
      if (csSum3 > 0) { csSum3 = 0; } //Reset
      cs_3.reset_CS_AutoCal(); //Stops readings
    }
  } else {
    csSum3 = 0; //Timeout caused by bad readings
    buttonState3 = false;
  }
}

void CSread4() {
  long cs4 = cs_4.capacitiveSensor(80); //a: Sensor resolution is set to 80
  if (cs4 > potar) { //b: Arbitrary number
    buttonState4 = true;
    csSum4 += cs4;
    //Serial.println(cs4); 
    if (csSum4 >= potar) //c: This value is the threshold, a High value means it takes longer to trigger
    {
      Serial.print("Trigger4: ");
      Serial.println(csSum4);
      if (csSum4 > 0) { csSum4 = 0; } //Reset
      cs_4.reset_CS_AutoCal(); //Stops readings
    }
  } else {
    csSum4 = 0; //Timeout caused by bad readings
    buttonState4 = false;
  }
}

void CSread5() {
  long cs5 = cs_5.capacitiveSensor(80); //a: Sensor resolution is set to 80
  if (cs5 > potar) { //b: Arbitrary number
    buttonState5 = true;
    csSum5 += cs5;
    Serial.println("cs5" + String(cs5)); 
    if (csSum5 >= potar) //c: This value is the threshold, a High value means it takes longer to trigger
    {
      Serial.print("Trigger5: ");
      Serial.println(csSum5);
      if (csSum5 > 0) { csSum5 = 0; } //Reset
      cs_5.reset_CS_AutoCal(); //Stops readings
    }
  } else {
    csSum5 = 0; //Timeout caused by bad readings
    buttonState5 = false;
  }
}

void CSread6() {
  long cs6 = cs_6.capacitiveSensor(80); //a: Sensor resolution is set to 80
  if (cs6 > potar) { //b: Arbitrary number
    buttonState6 = true;
    csSum6 += cs6;
    //Serial.println(cs6);
    if (csSum6 >= potar) //c: This value is the threshold, a High value means it takes longer to trigger
    {
      Serial.print("Trigger6: ");
      Serial.println(csSum6);
      if (csSum6 > 0) { csSum6 = 0; } //Reset
      cs_6.reset_CS_AutoCal(); //Stops readings
    }
  } else {
    csSum6 = 0; //Timeout caused by bad readings
    buttonState6 = false;
  }
}

int song = 0;

void sing(int s) {
  // iterate over the notes of the melody:
  song = s;
  if (song == 1) {
    Serial.println(" 'Bitch lasagna + crab song'");
    int size = sizeof(melody) / sizeof(int);
    for (int thisNote = 0; thisNote < size; thisNote++) {
 
      // to calculate the note duration, take one second
      // divided by the note type.
      //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
      int noteDuration = 1000 / tempo[thisNote];
 
      buzz(buzzerPin, melody[thisNote], noteDuration);
 
      // to distinguish the notes, set a minimum time between them.
      // the note's duration + 30% seems to work well:
      int pauseBetweenNotes = noteDuration * 1.30;
      delay(pauseBetweenNotes);
 
      // stop the tone playing:
      buzz(buzzerPin, 0, noteDuration);
    }
 
  }
  if (song == 2) {
    Serial.println(" 'Underworld Theme'");
    int size = sizeof(underworld_melody2) / sizeof(int);
    for (int thisNote = 0; thisNote < size; thisNote++) {
 
      // to calculate the note duration, take one second
      // divided by the note type.
      //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
      int noteDuration = 1000 / underworld_tempo2[thisNote];
 
      buzz(buzzerPin, underworld_melody2[thisNote], noteDuration);
 
      // to distinguish the notes, set a minimum time between them.
      // the note's duration + 30% seems to work well:
      int pauseBetweenNotes = noteDuration * 1.30;
      delay(pauseBetweenNotes);
 
      // stop the tone playing:
      buzz(buzzerPin, 0, noteDuration);
 
    }
 
  }
  if (song == 3) {
 
    Serial.println(" 'Mario Theme'");
    int size = sizeof(melody2) / sizeof(int);
    for (int thisNote = 0; thisNote < size; thisNote++) {
 
      // to calculate the note duration, take one second
      // divided by the note type.
      //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
      int noteDuration = 1000 / tempo2[thisNote];
 
      buzz(buzzerPin, melody2[thisNote], noteDuration);
 
      // to distinguish the notes, set a minimum time between them.
      // the note's duration + 30% seems to work well:
      int pauseBetweenNotes = noteDuration * 1.30;
      delay(pauseBetweenNotes);
 
      // stop the tone playing:
      buzz(buzzerPin, 0, noteDuration);
 
    }
  }
}
 

void buzz(int targetPin, long frequency, long length) {
  digitalWrite(13, HIGH);
  long delayValue = 1000000 / frequency / 2; // calculate the delay value between transitions
  //// 1 second's worth of microseconds, divided by the frequency, then split in half since
  //// there are two phases to each cycle
  long numCycles = frequency * length / 1000; // calculate the number of cycles for proper timing
  //// multiply frequency, which is really cycles per second, by the number of seconds to
  //// get the total number of cycles to produce
  for (long i = 0; i < numCycles; i++) { // for the calculated length of time...
    digitalWrite(targetPin, HIGH); // write the buzzer pin high to push out the diaphram
    delayMicroseconds(delayValue); // wait for the calculated delay value
    digitalWrite(targetPin, LOW); // write the buzzer pin low to pull back the diaphram
    delayMicroseconds(delayValue); // wait again or the calculated delay value
  }
  digitalWrite(13, LOW);
 
}

void playNianCat(){
  playNote('f',3,1,true);
      delay(tempo3);
      playNote('g',3,1,true);
      delay(tempo3);
      playNote('d',3,1,true);
      playNote('d',3,1,true);
      delay(tempo3);
      playNote('b',3,1,true);
      playNote('d',3,1,false);
      playNote('c',3,1,true);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('c',3,1,true);
      delay(tempo3);
     
       
      playNote('d',3,1,false);
      delay(tempo3);
      playNote('d',3,1,false);
      playNote('c',3,1,true);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('f',3,1,true);
      playNote('g',3,1,true);
      playNote('d',3,1,true);
      playNote('f',3,1,true);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('b',3,1,false);
       
      playNote('d',3,1,true);
      delay(tempo3);
      playNote('f',3,1,true);
      delay(tempo3);
      playNote('g',3,1,true);
      playNote('d',3,1,true);
      playNote('f',3,1,true);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('d',3,1,false);
      playNote('c',3,1,true);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
       
      playNote('d',3,1,false);
      delay(tempo3);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('f',3,1,true);
      playNote('c',3,1,true);
      playNote('d',3,1,false);
      playNote('c',3,1,true);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      delay(tempo3);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('c',3,1,true);
      delay(tempo3);
       
      playNote('f',3,1,true);
      delay(tempo3);
      playNote('g',3,1,true);
      delay(tempo3);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      delay(tempo3);
      playNote('c',3,1,true);
      playNote('d',3,1,false);
      playNote('c',3,1,true);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('c',3,1,true);
      delay(tempo3);
       
       
      playNote('d',3,1,false);
      delay(tempo3);
      playNote('d',3,1,false);
      playNote('c',3,1,true);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('f',3,1,true);
      playNote('g',3,1,true);
      playNote('d',3,1,true);
      playNote('f',3,1,true);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('b',3,1,false); 
      
      
      playNote('d',3,1,true);
      delay(tempo3);
      playNote('f',3,1,true);
      delay(tempo3);
      playNote('g',3,1,true);
      playNote('d',3,1,true);
      playNote('f',3,1,true);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('d',3,1,false);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
       
       
      playNote('d',3,1,false);
      delay(tempo3);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('d',3,1,true); 
      playNote('f',3,1,true);
      playNote('c',3,1,true);
      playNote('d',3,1,false);
      playNote('c',3,1,true);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      delay(tempo3);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('b',3,1,false);
      delay(tempo3);
       
       
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('b',3,1,false);
      playNote('e',3,1,false);
      playNote('d',3,1,true);
      playNote('e',3,1,false);
      playNote('f',3,1,true);
       
       
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('b',3,1,false);
      delay(tempo3);
       playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      playNote('f',2,1,true); 
      playNote('e',3,1,false);
      playNote('d',3,1,true);  
      playNote('c',3,1,true); 
      playNote('b',3,1,false);
      playNote('e',2,1,false);
      playNote('d',2,1,true); 
      playNote('e',2,1,false);
      playNote('f',2,1,true);
     
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('b',3,1,false);
      playNote('f',2,1,true);
      playNote('g',2,1,true);
      playNote('f',2,1,true);
       
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('b',3,1,false);
      playNote('a',3,1,true);
      playNote('b',3,1,false);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      playNote('e',3,1,false);
      playNote('d',3,1,true);
      playNote('e',3,1,false);
      playNote('f',3,1,true);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('a',3,1,true);
      delay(tempo3);
       
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('b',3,1,false);
      playNote('e',3,1,false);
      playNote('d',3,1,true);
      playNote('e',3,1,false);
      playNote('f',3,1,true);
       
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      playNote('f',2,1,true); 
      playNote('e',3,1,false);
      playNote('d',3,1,true); 
      playNote('c',3,1,true); 
      playNote('b',3,1,false);
      playNote('e',2,1,false);
      playNote('d',2,1,true);
      playNote('e',2,1,false);
      playNote('f',2,1,true);
       
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      playNote('b',3,1,false);
      playNote('c',3,1,true);
      playNote('d',3,1,true);
      playNote('b',3,1,false);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('f',2,1,true);
      
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('b',3,1,false);
      playNote('a',3,1,true);
      playNote('b',3,1,false);
      playNote('f',2,1,true); 
      playNote('g',2,1,true);
      playNote('b',3,1,false);
      playNote('e',3,1,false);
      playNote('d',3,1,true);
      playNote('e',3,1,false);
      playNote('f',3,1,true);
      playNote('b',3,1,false);
      delay(tempo3);
      playNote('c',3,1,true);
      delay(tempo3);
  
}

void beep(int note, int duration)
{
  //Play tone on buzzerPin
  tone(buzzerPin, note, duration);
 
  //Play different LED depending on value of 'counter'
  if(counter % 2 == 0)
  {
    digitalWrite(ledPin1, HIGH);
    delay(duration);
    digitalWrite(ledPin1, LOW);
  }else
  {
    digitalWrite(ledPin2, HIGH);
    delay(duration);
    digitalWrite(ledPin2, LOW);
  }
 
  //Stop tone on buzzerPin
  noTone(buzzerPin);
 
  delay(50);
 
  //Increment counter
  counter++;
}
 
void firstSection()
{
  beep(a, 500);
  beep(a, 500);    
  beep(a, 500);
  beep(f, 350);
  beep(cH, 150);  
  beep(a, 500);
  beep(f, 350);
  beep(cH, 150);
  beep(a, 650);
 
  delay(500);
 
  beep(eH, 500);
  beep(eH, 500);
  beep(eH, 500);  
  beep(fH, 350);
  beep(cH, 150);
  beep(gS, 500);
  beep(f, 350);
  beep(cH, 150);
  beep(a, 650);
 
  delay(500);
}
 
void secondSection()
{
  beep(aH, 500);
  beep(a, 300);
  beep(a, 150);
  beep(aH, 500);
  beep(gSH, 325);
  beep(gH, 175);
  beep(fSH, 125);
  beep(fH, 125);    
  beep(fSH, 250);
 
  delay(325);
 
  beep(aS, 250);
  beep(dSH, 500);
  beep(dH, 325);  
  beep(cSH, 175);  
  beep(cH, 125);  
  beep(b, 125);  
  beep(cH, 250);  
 
  delay(350);
}
