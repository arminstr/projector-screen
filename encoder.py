import RPi.GPIO as GPIO
import time
import signal
import sys

ROTATION_GPIO = 23
ENDSWITCH_GPIO = 24

rotation_ticks = 0
endswitch_ticks = 0

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def rotation_callback(channel):
	global rotation_ticks
	rotation_ticks += 1
def endswitch_callback(channel):
	global endswitch_ticks
	endswitch_ticks += 1

def init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(ROTATION_GPIO, GPIO.IN) # rotation
	GPIO.setup(ENDSWITCH_GPIO, GPIO.IN) # endswitch

	GPIO.add_event_detect(ROTATION_GPIO, GPIO.FALLING, callback=rotation_callback, bouncetime=330)
	GPIO.add_event_detect(ENDSWITCH_GPIO, GPIO.FALLING, callback=endswitch_callback, bouncetime=10)
	signal.signal(signal.SIGINT, signal_handler)
