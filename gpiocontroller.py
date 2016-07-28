from random import randint
from threading import Thread
import time
import RPi.GPIO as GPIO


class GPIOController:

  MODUS_MANUELL = 0
  MODUS_AUTOMATIK = 1
  MODUS_BREMSASSISTENT = 2
  
  stepCounter = 0
  modus = MODUS_MANUELL
  phase = 0

  distanceSensorResult = {19:10000, 21:10000, 23:10000}
  distanceSensorLastCheckTime = {19:0, 21:0, 23:0}

  def __init__(self):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(22, GPIO.IN)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.IN)
    GPIO.setup(26, GPIO.IN)

  def an(self):
    GPIO.output(11, GPIO.HIGH)

  def vor(self):
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(16, GPIO.HIGH)

  def links(self):
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(16, GPIO.LOW)

  def rechts(self):
    GPIO.output(15, GPIO.LOW)
    GPIO.output(16, GPIO.HIGH)

  def zurueck(self):
    GPIO.output(15, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)

  def aus(self):
    GPIO.output(11, GPIO.LOW)

  def distanz(self, trigger, echo):
    if time.time() - distanceSensorLastCheckTime[trigger] > 0.5: #check max 2 times per Seconds

      # setze Trigger auf HIGH
      GPIO.output(trigger, True)

      # setze Trigger nach 0.01ms aus LOW
      time.sleep(0.00001)
      GPIO.output(trigger, False)

      StartZeit = time.time()
      StopZeit = time.time()

      # speichere Startzeit
      while GPIO.input(echo) == 0:
        if time.time() - StopZeit > 2:
          raise Exception('Timeout trigger '+str(trigger)+' echo '+str(echo))
        StartZeit = time.time()

      # speichere Ankunftszeit
      while GPIO.input(echo) == 1:
        if time.time() - StartZeit > 2:
          raise Exception('Timeout2 trigger '+str(trigger)+' echo '+str(echo))
        StopZeit = time.time()

      # Zeit Differenz zwischen Start und Ankunft
      TimeElapsed = StopZeit - StartZeit
      # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
      # und durch 2 teilen, da hin und zurueck
      distanz = (TimeElapsed * 34300) / 2

      distanceSensorResult[trigger] = distanz
      return distanz
    
    else:  
      return distanceSensorResult[trigger]

  def distanzVorneLinks(self):
    return distanz(19, 22)

  def distanzVorneRechts(self):
    return distanz(21, 24)

  def distanzHinten(self):
    return distanz(23, 26)

  def manuell(self):
    starteModus(MODUS_MANUELL)

  def automatik(self):
    starteModus(MODUS_AUTOMATIK)

  def bremsassistent(self):
    starteModus(MODUS_BREMSASSISTENT)

  def starteModus(self, neuerModus):
    modus = neuerModus
    stepCounter = 0
    phase = 0

    if modus != MODUS_MANUELL:
      thread = Thread(target = modusRunner)
      thread.start()

  def modusRunner(self):
    while modus != MODUS_MANUELL:
      if modus == MODUS_AUTOMATIK:
        automatikStep()
      else:
        bremsassistentStep()

      stepCounter = stepCounter + 1
      time.sleep(0.25)
   
  def setPhase(self, neuePhase):
    phase = neuePhase
    stepCounter = 0

  def automatikStep(self):
    if (phase == 'links' or phase == 'rechts') and stepCounter > 8 and randint(0,9) < 7: #after 2 seconds
      vor()
      phase = 'vor'

    if phase == 'vor' and stepCounter > 4: #check every second
      dVorneLinks = distanzVorneLinks()
      dVorneRechts = distanzVorneRechts()

     
    
       
  def bremsassistentStep(self):
    print('Hello')  
