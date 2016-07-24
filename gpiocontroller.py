import time
import RPi.GPIO as GPIO


class GPIOController:

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
    time.sleep(0.25)

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
    time.sleep(0.25)

  def distanz(self, trigger, echo):
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

    return distanz
