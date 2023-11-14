#include <SevSeg_SpecialProgetEric.h>

SevSeg sevseg; //Instantiate a seven segment controller object


//Definition des broches des pins des boutons, des leds et du relais
const int boutonChangeDigitPin  = 39;
const int boutonPlusPin         = 38;
const int boutonMoinsPin        = 37;
const int boutonValiderPin      = 36;

const int LedOn  = 34;
const int LedOff = 35;

const int relaisPin = 40;


int digitCligno = 99;//aucun digit ne clignote

unsigned long TimerDecompte = 0;

//Definition des etats des boutons, des incrementations et des decomptes
bool buttonChangeDigitState  = false;
bool buttonPlusState         = false;
bool buttonMoinsState        = false;
bool boutonValiderState      = false;

bool incrementationPlus  = false;
bool incrementationMoins = false;
bool incrementationDigit = false;

int etatDecompte = 0;
bool etatDecompte2 = 0;

void setup() {
  
  
  Serial.begin(9600);
  
  //******************************
  //initialisation SevSeg
  //******************************
  byte numDigits = 4;//nombre de digits
  byte digitPins[] = {22, 23, 24, 25};// Broches controlant les digits
  byte segmentPins[] = {26, 27, 28, 29, 30, 31, 32, 33};// Broches controlant les segments
  bool resistorsOnSegments = false;     // 'false' means resistors are on digit pins
  byte hardwareConfig = COMMON_CATHODE; // See README.md for options
  bool updateWithDelays = false;        // Default. Recommended
  bool leadingZeros = false;            // Use 'true' if you'd like to keep the leading zeros
  
  sevseg.begin(hardwareConfig, numDigits, digitPins, segmentPins, resistorsOnSegments, updateWithDelays, leadingZeros);
  sevseg.setBrightness(10);//Definit la luminosite de l afficheur
  sevseg.getEtatDecompte(&etatDecompte);
  
  //*******************************
  //initialisation des broches des boutons, des leds et du relais
  //*******************************
  pinMode (boutonChangeDigitPin, OUTPUT);
  pinMode (boutonPlusPin, OUTPUT);
  pinMode (boutonMoinsPin, OUTPUT);
  pinMode (boutonValiderPin, OUTPUT);
  pinMode (LedOn, OUTPUT);
  pinMode (LedOff, OUTPUT);   
  pinMode (relaisPin, OUTPUT);
  
}

void loop() {
  
  static unsigned long temps = millis();
  static int deciSeconds = 30;// Initialise et definit efinit le temps de base de depart du compteur
  static int deciSecondsSave = deciSeconds;// Initialise et sauvegarde le temps afficher 
  

  //****************************************
  //*************** BOUTONS ****************
  //****************************************
  
  //   **************
  //** bouton valider **
  //   **************
  boutonValiderState = digitalRead(boutonValiderPin);
   
  switch (boutonValiderState) {
      
    case HIGH :
      digitalWrite (LedOn, HIGH); 
      etatDecompte2 = 1;
      break;
      
    case LOW :
      if (etatDecompte2 == 1) {
        etatDecompte2 = 0;
        if (etatDecompte == 1) etatDecompte = 0;
        else etatDecompte = 1;
      }
      digitalWrite (LedOn, LOW);
      break;
      
    default : 
      break;
  }

  if (etatDecompte == 0){
   
    digitalWrite (LedOff, LOW);
    digitalWrite (relaisPin, LOW);
    
    
  //   **************
  //*** bouton plus ***
  //   **************
     buttonPlusState    = digitalRead(boutonPlusPin);
     switch (buttonPlusState) {
       case HIGH :
         incrementationPlus = 1;
         break;
       case LOW :
         if (incrementationPlus ==1) {
           incrementationPlus = 0;
           
           switch (digitCligno){
             case 0 :
               if (deciSeconds >= 9000) deciSeconds -=9000;
               else deciSeconds += 1000;
               break;
             
             case 1 :
               if ((deciSeconds/100)%10 == 9) deciSeconds -=900;
               else deciSeconds += 100;
               break;
             
             case 2 :
               if ((((deciSeconds/10)%100)%10) == 9) deciSeconds -=90;
               else deciSeconds += 10;
               
               break;
             
             case 3 :
               if ((((deciSeconds%1000)%100)%10) == 9) deciSeconds -=9;
               else deciSeconds++;
               break;
             
             default:
             break;
           }
          }
          break;
         
         default :
           break;
     }
     
  //   **************
  //*** bouton moins ***
  //   **************
     buttonMoinsState    = digitalRead(boutonMoinsPin);
     if (buttonMoinsState == 1)  deciSecondsSave = deciSeconds;
     
   //     ********************
  //  *** bouton changer digit ***
  //     *********************
  
  buttonChangeDigitState = digitalRead(boutonChangeDigitPin);
  switch (buttonChangeDigitState) {
       case HIGH :
         incrementationDigit = 1;
         break;
       case LOW :
         if (incrementationDigit == 1) {
           incrementationDigit = 0;
           if (digitCligno == 99) digitCligno = 4;
           else {
           digitCligno--;
             if (digitCligno < 0) digitCligno = 99;
           }
         }
         break;
     }
    
  }
  else {
    
  digitalWrite (relaisPin, HIGH);
  digitCligno = 99;//aucun digit ne clignote
  
  //attendre 0.1 secondes
  if (micros() - TimerDecompte > 100000)//Au bout de 1/10 secondes (100"000 microsecondes)
    {
        deciSeconds--;
        TimerDecompte = micros();//reinitialisation du compteur de temps
    }
 } 
    
  
  if (deciSeconds < 0)
  { 
    deciSeconds = 0;
    etatDecompte = 0;
    deciSeconds = deciSecondsSave;
  }
   
   if (etatDecompte == 0)  {
     sevseg.getEtatDecompte(&etatDecompte);
     sevseg.setNumber(deciSeconds, 1);
   }
   else {
     sevseg.blank();
     digitalWrite (LedOn, LOW);
     digitalWrite (LedOff, HIGH); 
   }
   
  sevseg.refreshDisplay(digitCligno); // Must run repeatedly
}
