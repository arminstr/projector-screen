from http.server import BaseHTTPRequestHandler, HTTPServer
import time, datetime
import threading
import motor
from motor import Direction
import encoder

HOST = ""
PORT = 80

"""
this value has to be changed according to the length of the projector screen and the number of ticks per revolution.
"""
MAX_ENCODER_TICKS = 10

currentPos = 0
targetPos = 0
rotationDir = 0
lastEncoderTicks = encoder.rotation_ticks
conversionFactor = 8
timeoutPeriod = 5 #number of loops until motor turns of in case no ticks occured
stuckCounter = 0

class Handler(BaseHTTPRequestHandler):
	"""
	GET requests will arrive at http://projector-screen.local/api/v1/pos
	"""
	def do_GET(self):
		global currentPos, targetPos
		if "api/v1/pos/" in self.path:
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			stringPos = self.path.split("/")[-1]
			self.wfile.write(bytes(str(currentPos), "utf-8"))
			targetPos = int(stringPos)/conversionFactor
		elif "api/v1/pos" in self.path:
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write(bytes(str(currentPos*conversionFactor), "utf-8"))
	def log_message(self, format, *args):
		return

def positionController():
	"""
	controls the position of the projector screen.
	depending on the control difference the motor is turned in the matching direction.
	in case the end switch is engaged the motor is not allowed to turn into the upwards direction any further.
	in addition, current position is set to 0.
	"""
	global currentPos, targetPos, lastEncoderTicks, rotationDir, stuckCounter

	if currentPos < targetPos:
		rotationDir = Direction.UP
		currentPos += encoder.rotation_ticks - lastEncoderTicks
	if currentPos > targetPos:
		rotationDir = Direction.DOWN
		currentPos -= encoder.rotation_ticks - lastEncoderTicks

	if abs(targetPos - currentPos) < 1:
		motor.stop()
		time.sleep(0.1)
		stuckCounter = 0
	elif stuckCounter > timeoutPeriod and rotationDir == Direction.UP:
		motor.stop()
		time.sleep(0.1)
		currentPos = 0
		stuckCounter = 0
	else:
		motor.turn(rotationDir)
		if abs(encoder.rotation_ticks - lastEncoderTicks) == 0:
			stuckCounter += 1
		else:
			stuckCounter = 0
	print(rotationDir, targetPos, currentPos, "stuckCounter:", stuckCounter)
	lastEncoderTicks = encoder.rotation_ticks
	print(encoder.rotation_ticks)
def loop():
	next_call = time.time()
	while True:
		positionController()
		next_call = next_call+0.1;
		time.sleep(max(0, next_call - time.time()))

if __name__ == "__main__":
	motor.init()
	print("motor: initialized ...")
	encoder.init()
	print("encoder: initialized ...")
	timerThread = threading.Thread(target=loop)
	timerThread.daemon = True
	timerThread.start()
	print("loop: initialized ...")
	webServer = HTTPServer((HOST, PORT), Handler)
	print("server: initialized at port", PORT, "...")
	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass
	webServer.server_close()
	motor.stop()
	print("server stopped.")
