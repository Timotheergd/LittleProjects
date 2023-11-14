#include <dht.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <RFID.h>
#include <Servo.h>

//******************************************
//********** Déclaration des pins **********
//******************************************

//définition des pins sur lesquelles sont branchées le rfid
#define SS_PIN 53
#define RST_PIN 49

//********************************************
//********** Déclaration des objets **********
//********************************************
/*
Cablage des lcd en I2C:
SDA --> A4
SCL --> A5
*/

LiquidCrystal_I2C lcd1(0x27,16,2);  //définition du lcd utilisé pour afficher des messages diverses (ex : Bienvenue Timothee, Atention Intrusion...)
LiquidCrystal_I2C lcd2(0x3F,16,2);  //définition du lcd utilisé pour afficher diverses informations tel que la date, l'heure, l'humidité, la température et s'il fait jour ou s'il fait nuit

Servo servoMoteur;   //définition du servo moteur permettant d'ouvrir et de fermer la porte
Servo servoMoteur2;  //définition du servo moteur permettant d'ouvrir et de fermer le volet

RFID rfid(SS_PIN,RST_PIN);  //définition du rfid, composant qui permet de lire les badges rfid

dht DHT;  //définition du capteur DHT qui permet de mesurer la température et l'humidité
//#define DHT11_PIN 6***********************************************************************************************************

//*******************************************************
//********** Déclaration des variables d'états **********
//*******************************************************

boolean testMode = 0;

boolean night_ = false;  //déclaration de la variable d'état indiquant s'il fait nuit(= true) ous'il fait jour(=false)

boolean etatActiveAlarm = false;      // déclaration de la variable d'état indiquant si l'on a appuyé sur le bouton
boolean etatPassGerAlarm = false;     // déclaration de la variable d'état indiquant si le programme est passé dans la condition qui est dans gererAlarme pour activer actionAlarme
boolean etatActivationAlarm = false;  // déclaration de la variable d'état qui permet de savoir si ca fait 10 secondes que l'on a enclaché l'alarme pour savoir s'il faut l'activer

boolean etatPorte = false;  //définition de la variable d'état indiquant si la porte et ouverte(= 0) ou fermée(= 1)

boolean etatAccess = false;    //définition de la variable d'état qui permet de savoir si le badge a bien été reconnu et donc si la personne peut entrer
boolean etatIsCard = false;    //définition de la variable d'état qui permet de savoir si le badge est devant le capteur
boolean etatReadCard = false;  //définition de la variable d'état qui permet de savoir si le badge est bien lu

int etatPresenceExterieur = 0;  //variable d'état qui permet d'enregistrer s'il y a une personne devant la porte(= 1) ou s'il y a pernonne(= 0)

boolean etatLockLow = true;  //variable d'état qui permet d'enregistrer si le capteur est passé par un signal bas 
boolean etatTakeLowTime;     //variable d'état qui permet d'enregistrer si le capteur est passé par un signal haut

boolean etatAlarmCheck = false;  //déclaration de la variable d'etat qui permet de savoir si on a deja gerer l'alarme

//définition de la variable d'etat qui indique l'etat de l'alarme
//etatAlarm = 0; -> signifie que l'alarme n'est pas enclancée
//etatAlarm = 1; -> signifie que l'alarme est enclanchée
//etatAlarm = 2; -> signifie que l'alarme est entrain de s'enclanché
//etatAlarm = 3; -> signifie rien*************************************************************************
//etatAlarm = 4; -> signifie que l'alarme sonne -> intrusion
int etatAlarm = 0;

boolean etatLedInterieur = false;  //déclaration de la variable d'état qui sert à savoir s'il faut allumer(= true) ou éteindre((false) les leds interieurs
boolean etatLedExterieur = false;  //déclaration de la variable d'état qui sert à savoir s'il faut allumer(= true) ou éteindre((false) la led exterieur

//**********************************************************
//********** Déclaration des variables de valeurs **********
//**********************************************************

//définition du tableau contenant en :
// - TabLCD1[0] : le message affiché sur la ligne 1
// - TabLCD1[1] : le message affiché sur la ligne 2
// - TabLCD1[2] : le décalage avant le message 1
// - TabLCD1[3] : le décalage avant le message 2
String TabLCD1[4];

//définition du tableau contenant en :
// - TabLCD2[0] : le message affiché sur la ligne 1
// - TabLCD2[1] : le message affiché sur la ligne 2
// - TabLCD2[2] : le décalage avant le message 1
// - TabLCD2[3] : le décalage avant le message 2
String TabLCD2[4];

//Si = 1, passage badge trop rapide
//Si = 2, passage badge non autorisé
int invalideCard = 0;

int message = 0;

int valeurPositionDuServo = 80;   //définition de la variable indiquant la valeur de l'angle du servo moteur qui permet d'ouvrir et de fermer la porte
int valeurPositionDuServo2 = 80;  //définition de la variable indiquant la valeur de l'angle du servo moteur qui permet d'ouvrir et de fermer la porte
 
int serNum[5];  //définition du tableau qui permet d'enregister les cinq numéros d'identité du badge RFID
int x;          //définition de la variable permettant d'enregistrer quelle personne correspond au badge présenté

int cards[][5] = {  //tableau permetant d'enregistrer l'identité de ses badges pour qu'ils puissent ensuite etre reconnus
                 { 54, 9, 65, 73, 55 },
                 { 1, 177, 64, 197, 53 },
                 { 136, 5, 32, 0, 173 },
                 { 186, 178, 89, 137, 216 },
                 { 37, 179, 112, 45, 203 },
                 };

//tableau permettant d'enregistrer les noms des personnes qui ont les badges et qui donc ont l'autorisation d'entrer dans la aison
char personne[][16] = // 1er parametre = nb de pers autorisees
                      // second = longueur maximale du nom
                      {"Timothee Bleu1", "Timothee Blanc1", "Papa", "Timothee Bleu2", "Timothee Blanc2"};

float valeurDistance;  //variable qui permet d'enregistrer quel est la distance qui sépare le capteur ultrason et l'objet (ici la personne) qui y a devant

int calibrationTime = 5;  //temps donner au PIR pour qu'il puisse se calibrer (normalement entre 10 et 60 secondes)

//définition des variables permettants d'enregistrer l'heure, les minutes, le jour, le mois et l'année actuelle
int heure = 23;
int minute = 55;
int jour = 30;
int mois = 8;
int annee = 2018;

int valeurTemperature;  //déclaration de la variable permettant d'enregistrer la température
int valeurHumidite;     //déclaration de la variable permettant d'enregistrer l'humidité

int nbSecAvActAlrm = 0; // déclaration de la variable qui va compter le nomvre de secondes qu'il reste anvant que l'alarme soit active

int tempsDurerActivationAlarm = 10; // définition de la variable qui définit la durer en seconde de la séquence d'enclanchemant de l'alarme

//définition des variables qui contiennent les parties du message de la ligne 1 et 2
String partMessageHeure  = String(heure);
String partMessageMinute = String(minute);
String partMessageJour   = String(jour);
String partMessageMois   = String(mois);
String partMessageNight   = "C-Jour-H=";
//définition des variables qui contiennent le message à afficher sue le lcd2
String ligne1;
String ligne2;

long unsigned int lowIn; //variable qui permet d'enregistrer le temps passé  àpartir du moment où le capteur passe à l'état bas pour permettre de faire comme si le signal durait au moins un temps définit par la variable "pause"
long unsigned int pause = 5000; //variable qui permet de définir quel temps minimun que le signal haut doit durer

unsigned long tempsMinute = millis();  // définition de la variable pertant d'augmenter le temps de 1 minite toutes les minutes

unsigned long tempsClignoREtAl2 = millis(); // définition de la variable qui permet de faire clignoter les leds en rouge quand l'alarme est enclancjé mais pas encore active
unsigned long tempsClignoREtAl4 = millis(); // définition de la variable qui permet de faire clignoter les leds et de faire sonner le buzeur quand l'alarme sonne

unsigned long tempsPorteOuverte = 0;  //définition de la variable permettant d'enregistrer quand la porte a été ouverte pour la fermer un certains temps plus tard

unsigned long tempsActivationAlarm = 0;       // définition de la variable qui permet de savoir si ca fait 10 secondes que l'on a enclanché l'alarme pour savoir s'il faut l'activer

unsigned long tempsPositionageRfid = millis();  //définition de la variable permettant d'attendre un certains temps pour que l'utilisateur ai le temps de placer le badge

unsigned long tempsTemperature = millis();  //définition de la variable permettant d'enregistrer quand a été meusuré l'igrométrie pour la derniere fois afin d'attendre deux secondes avant de relever 
                                            //une nouvelle fois des données car le capteur ne peut relever des données que toute les deux secondes, sinon il donne des informations incohérantes
unsigned long tempsAlarmButton = millis();  //définition de la variable qui permet d'enregistrer quand le boutton a été appuyer car il ne faut pas que l'on puisse appuyer deux fois sur le bouton à moins de deux secondes d'intervales

unsigned long tempsMessage2 = millis();  //définition de la variable permettant d'afficher le message 2 (Presenter votre badge SVP...) tous les [temps définit dans le programme]
unsigned long tempsMessage3 = millis();  //définition de la variable permettant d'afficher le message 3 (Bonjour [insérer nom de la personne]) tous les [temps définit dans le programme]
unsigned long tempsMessage4 = millis();  //définition de la variable permettant d'afficher le message 4
unsigned long tempsMessage5 = millis();  //définition de la variable permettant d'afficher le message 5
unsigned long tempsAffichageDefault2 = millis(); //définition de la variable qui permet de faire varier le message 2 (Presenter votre badge SVP...) et le message 7 (Alarme active) tous les [temps définit dans le programme]
unsigned long tempsAffichageDefault3 = millis(); //définition de la variable qui permet de faire varier le message 1 (maison domotique par timothée !) et le message 7 (Alarme active) tous les [temps définit dans le programme]

#include <composants2.h>
#include <MaisonDomotique.h>

void setup(){
  Serial.begin(9600);
  pinMode(AlarmButtonPin, INPUT_PULLUP);
  attachInterrupt(interruptAlarmButtonPin, buttonState, RISING); 
  lcd1.begin();
  lcd2.begin();
  AffLcd(lcd1, TabLCD1, "Bonjour", "!", 4,7);
  AffLcd(lcd2, TabLCD2, "Bonjour", "!", 4,7);
  
  initPorte(rfid, servoMoteur, buzzerPin, valeurPositionDuServo, &etatPorte, 0);
  initUltrason(DOUT_TRIGGER, DIN_ECHO);
  initPIR(pirPin);
  initPIR_Affichage(lcd1, TabLCD1, pirPin, calibrationTime, redPinInterieurs, greenPinInterieurs, bluePinInterieurs, redPinExterieurs, greenPinExterieurs, bluePinExterieurs, testMode);
  initRGB(redPinInterieurs, greenPinInterieurs, bluePinInterieurs);
  initRGB(redPinExterieurs, greenPinExterieurs, bluePinExterieurs);
  initVolet(servoMoteur2, valeurPositionDuServo2);
  initAlarm(AlarmButtonPin);
  lcd2.clear();
}

void loop(){
  // Etat Capteurs
  gererPR(pinPR, &night_);
  x = gererRfid(rfid, cards, serNum, tempsPositionageRfid, x, &etatIsCard, &etatReadCard, &etatPresenceExterieur, &etatPorte, &etatAccess);
  gererUltrason(&valeurDistance, DOUT_TRIGGER, DIN_ECHO, &etatPresenceExterieur, &etatLedExterieur);
  gererPir(pirPin, &lowIn, pause, &etatLockLow, &etatTakeLowTime, &etatAlarm, &night_, &etatLedInterieur);
  gererDHT(DHT, &tempsTemperature, &valeurTemperature, &valeurHumidite);
  
  // Gerer Etats
  gererTemps(&heure, &minute, &jour, &mois, &annee, &tempsMinute);
  gererAlarme(&tempsAlarmButton, &etatAlarm, &etatPassGerAlarm, &etatActiveAlarm, &etatAlarmCheck, &etatLedInterieur, &etatLedExterieur, buzzerPin);
  
  // Gerer Affichage
  gererMessageLcd2(&ligne1, &ligne2, heure, minute, jour, mois, annee, valeurTemperature, valeurHumidite, night_);
  message = gererMessagesLcd1(rfid, etatAlarm, invalideCard, tempsMessage3, tempsMessage4, tempsMessage5, tempsAffichageDefault2, tempsAffichageDefault3, etatIsCard, etatPresenceExterieur, etatPorte, etatAccess);
  
  // Actions
  actionRfid(servoMoteur, &valeurPositionDuServo, serNum, buzzerPin, &invalideCard, redPinInterieurs, greenPinInterieurs, bluePinInterieurs, redPinExterieurs, greenPinExterieurs, bluePinExterieurs, &tempsPositionageRfid, &tempsPorteOuverte, etatAccess, etatPresenceExterieur, &etatPorte, etatIsCard, etatReadCard, &etatAlarm);
  actionLeds(night_, redPinInterieurs, greenPinInterieurs, bluePinInterieurs, redPinExterieurs, greenPinExterieurs, bluePinExterieurs, &etatLedExterieur, &etatLedInterieur);
  actionVolet(servoMoteur2, &valeurPositionDuServo2, etatAlarm, night_);
  actionLcd1(lcd1, TabLCD1, personne, message, nbSecAvActAlrm, tempsDurerActivationAlarm, x, &tempsMessage3, &tempsMessage4, &tempsMessage5, &tempsAffichageDefault2, &tempsAffichageDefault3);
  actionLcd2(lcd2, TabLCD2, ligne1, ligne2);
  actionAlarm(servoMoteur, servoMoteur2, &valeurPositionDuServo, &valeurPositionDuServo2, redPinInterieurs, greenPinInterieurs, bluePinInterieurs, &etatAlarmCheck, &etatAlarm, &nbSecAvActAlrm, tempsDurerActivationAlarm, etatPassGerAlarm, &etatPorte, &etatLedInterieur, &etatLedExterieur, &etatActiveAlarm, &etatActivationAlarm, &tempsActivationAlarm, &tempsClignoREtAl2, &tempsClignoREtAl4);
}

void buttonState(){
    etatActiveAlarm = true;
    Serial.println("Alarme");
}
