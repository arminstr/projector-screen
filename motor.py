import RPi.GPIO as GPIO
from enum import Enum
import time

class Direction(Enum):
        UP = 0
        DOWN = 1

def init():
	"""
	initializes the motor gpio config
	"""
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(1, GPIO.OUT)
	GPIO.setup(7, GPIO.OUT)
	GPIO.setup(8, GPIO.OUT)
	GPIO.setup(25, GPIO.OUT)

def turn(dir):
	"""
	set the gpios to a specific motor driving direction
	"""
	GPIO.output(1, GPIO.LOW)
	GPIO.output(7, GPIO.LOW)
	GPIO.output(8, GPIO.LOW)
	GPIO.output(25, GPIO.LOW)
	# turns on the motor in the normal voltage config
	if dir == Direction.UP:
		GPIO.output(1, GPIO.HIGH)
		GPIO.output(25, GPIO.HIGH)
	# turns the motor in reverse
	if dir == Direction.DOWN:
		GPIO.output(7, GPIO.HIGH)
		GPIO.output(8, GPIO.HIGH)

def stop():
	"""
	stops the motor rotation
	"""
	GPIO.output(1, GPIO.LOW)
	GPIO.output(7, GPIO.LOW)
	GPIO.output(8, GPIO.LOW)
	GPIO.output(25, GPIO.LOW)
