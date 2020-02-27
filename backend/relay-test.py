import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RELAY1 = 19
RELAY2 = 26
RELAY3 = 20
RELAY4 = 21

RELAY_ON = False
RELAY_OFF = True

RELAYS = [RELAY1, RELAY2, RELAY3, RELAY4]
for r in RELAYS:
    GPIO.setup(r, GPIO.OUT)

def all_off():
    for r in RELAYS:
        GPIO.output(r, RELAY_OFF)

try:
    while True:
        for r in RELAYS:
            all_off()
            time.sleep(0.25)
            GPIO.output(r, RELAY_ON)
            time.sleep(1)
except KeyboardInterrupt:
    all_off()
