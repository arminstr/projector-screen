from http.server import BaseHTTPRequestHandler, HTTPServer
import time

import motor


HOST = ""
PORT = 80

currentPos = 42
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

motor.init()
print("motor: initialized...")

if __name__ == "__main__":
	motor.init()
	print("motor: initialized...")
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
