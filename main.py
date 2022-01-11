from http.server import BaseHTTPRequestHandler, HTTPServer
import time, datetime
import threading
import motor

HOST = ""
PORT = 80

"""
this value has to be changed according to the length of the projector screen and the number of ticks per revolution.
"""
MAX_ENCODER_TICKS = 10

currentPos = 0
targetPos = 0

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
			self.wfile.write(bytes(stringPos, "utf-8"))
			targetPos = int(stringPos)
		elif "api/v1/pos" in self.path:
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			currentPos = targetPos
			self.wfile.write(bytes(str(currentPos), "utf-8"))

def positionController():
	"""
	controls the position of the projector screen.
	depending on the control difference the motor is turned in the matching direction.
	in case the end switch is engaged the motor is not allowed to turn into the upwards direction any further.
	in addition, current position is set to 0.
	"""
	global currentPos, targetPos

	# dummy statement
	print (datetime.datetime.now())

def loop():
	next_call = time.time()
	while True:
		positionController()
		next_call = next_call+0.1;
		time.sleep(max(0, next_call - time.time()))

if __name__ == "__main__":
	motor.init()
	print("motor: initialized...")
	timerThread = threading.Thread(target=loop)
	timerThread.daemon = True
	timerThread.start()
	print("loop: initialized...")
	webServer = HTTPServer((HOST, PORT), Handler)
	print("server initialized at port", PORT)
	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass
	webServer.server_close()
	print("server stopped.")
"""
while 1:
	motor.turn(0)
	time.sleep(1)

	motor.stop()
	time.sleep(1)
	motor.turn(1)
	time.sleep(1)
	motor.stop()
	time.sleep(1)
"""
