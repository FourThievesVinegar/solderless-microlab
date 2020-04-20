import RPi.GPIO as GPIO

RELAY1 = 19
RELAY2 = 26
RELAY3 = 20
RELAY4 = 21

RELAY_ON = False
RELAY_OFF = True

RELAYS = [RELAY1, RELAY2, RELAY3, RELAY4]

def set_relay(r, state):
    GPIO.output(r, state)

def all_off():
    for r in RELAYS:
        set_relay(r, RELAY_OFF)

def init_relays():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for r in RELAYS:
        GPIO.setup(r, GPIO.OUT)

    all_off()
