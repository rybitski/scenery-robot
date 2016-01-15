import json
import socket
"""
TCP_IP = '192.168.1.100'
TCP_PORT = 39281
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print "Connection address:", addr
while 1:
	data = conn.recv(BUFFER_SIZE)
	if not data: break
	print "received data:", data
	conn.send(data)
conn.close()	

encoder_array = [][]

#-------------------------------
"""
import sys
import time
import threading
import SocketServer
from collections import deque
from xinput import XInputJoystick
from operator import itemgetter, attrgetter

# Requires pyglet 1.2alpha1 or higher
# pip install --upgrade http://pyglet.googlecode.com/archive/tip.zip
class RoboNetwork(threading.Thread):
	def __init__(self, ip, port, buff_size):
		threading.Thread.__init__(self)
		self.TCP_IP = ip
		self.TCP_PORT = port
		self.BUFFER_SIZE = buff_size
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((self.TCP_IP, self.TCP_PORT))
		self.connected = False
		self.exit = False
		self.s.settimeout(10)
		
	def run(self):
		# Set socket to listen
		self.s.listen(1)
		# Wait for a new client
		try:
			self.conn, self.addr = self.s.accept()
			self.connected = True
		except socket.timeout:
			print("No robot connected")
			self.exit = True
		
		while not self.exit:
			try:
				data = self.conn.recv(self.BUFFER_SIZE)
			except socket.timeout:
				continue
			if not data:break
			print("received data:", data)
			
		if self.connected:
			self.conn.close()
			self.connected = False
		print("Server shutting down!")

		"""
class TCPServerHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)
		self.request.sendall(self.data.upper())
		"""

class RoboControl(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	
		# Grabs 1st available gamepad, logging changes to the screen
		self.joysticks = XInputJoystick.enumerate_devices()
		self.device_numbers = list(map(attrgetter('device_number'), self.joysticks))
	
		self.l_joy_record = []
		self.r_joy_record = []
		
		self.state = 'normal'
		
		self.button_map = {
					"1": "DUP",
					"2": "DDOWN",
					"3": "DLEFT",
					"4": "DRIGHT",
					"5": "START",
					"6": "BACK",
					"7": "LJOYTOGGLE",
					"8": "RJOYTOGGLE",
					"9": "LB",
					"10": "RB",
					"13": "A",
					"14": "B",
					"15": "X",
					"16": "Y",
				}
				
		self.inv_button_map = {v: k for k, v in self.button_map.items()}
	
		self.button_state_map = {
						"0": "RELEASE",
						"1": "PRESSED",
						}
						
		print('found %d controller devices: %s' % (len(self.joysticks), self.device_numbers))

		if not self.joysticks:
			print("No joysticks found, exiting")
			return None
		
		# Use first joystick
		self.j = self.joysticks[0]
	
		print('Using device %d' % self.j.device_number)
		print('Press back button on controller to quit.')
	
		self.j.quit = False
		self.commands = deque()
		
		@self.j.event
		def on_button(button, pressed):
			#print('button %s %s' % (button_map[str(button)], button_state_map[str(pressed)]))
			self.j.quit = (button == int(self.inv_button_map['BACK']) and pressed)
			
			if (button == int(self.inv_button_map['START']) and pressed):
				if self.state == 'normal':
					self.state = 'record'
					print("Starting to record")
					self.l_joy_record[:] = []
					self.r_joy_record[:] = []
				elif self.state == 'record':
					self.state = 'normal'
					print("End record")
					for index in range(0, len(self.l_joy_record)):
						print(("L:%1.5f , R:%1.5f") % (self.l_joy_record[index], 
														self.r_joy_record[index]))
	
		@self.j.event
		def on_axis(axis, value):
			left_speed = 0
			right_speed = 0

			#print('axis', axis, value)
			
			if self.state == 'record':
				if axis == 'l_thumb_y':
					self.l_joy_record.append(value)
					if len(self.r_joy_record) > 0:
						self.r_joy_record.append(self.r_joy_record[-1])
					else:
						self.r_joy_record.append(0)
						
					value_convert = int(round(sensitivity_scale(value, 0.5, -0.5, 0.5, -127, 127)))
					if (abs(value_convert) <= 10):
						value_convert = 0
					self.commands.append(
						('L', value_convert)
					)
				elif axis == 'r_thumb_y':
					self.r_joy_record.append(value)
					if len(self.l_joy_record) > 0:
						self.l_joy_record.append(self.l_joy_record[-1])
					else:
						self.l_joy_record.append(0)
					
					value_convert = int(round(sensitivity_scale(value, 0.5, -0.5, 0.5, -127, 127)))
					
					if (abs(value_convert) <= 10):
						value_convert = 0
						
					self.commands.append(
						('R', value_convert)
					)
					
			if axis == "left_trigger":
				left_speed = value
			elif axis == "right_trigger":
				right_speed = value
			self.j.set_vibration(left_speed, right_speed)
			

	def run(self):
		while not self.j.quit:
			try:
				self.j.dispatch_events()
			except RuntimeError:
				print("Controller is not connected!")
				break
			time.sleep(0.01)
		print("Joystick shutting down!")
		
def map_range(old_min, old_max, new_min, new_max, old_value):
	old_range = old_max - old_min
	new_range = new_max - new_min
	new_value = (((old_value - old_min) * new_range) / old_range) + new_min
	return new_value
	
def sensitivity_scale(x_in, sensitivity, original_min, original_max, desired_min, desired_max):
	linear_scale = ((desired_max - desired_min) * (x_in - original_min))/(original_max-original_min) + desired_min
	scale_to_1 = 2 / (original_max-original_min)
	xin_sensitive = sensitivity * (x_in*scale_to_1)**3 + (1-sensitivity) * (x_in*scale_to_1)
	xin_sensitive /= scale_to_1
	sensitivity_scaled = ((desired_max - desired_min) * (xin_sensitive - original_min))/(original_max-original_min) + desired_min
	return sensitivity_scaled
	
if __name__ == "__main__":
	control = RoboControl()
	control.start()
	network = RoboNetwork('192.168.1.2', 29281, 20)
	network.start()
	while (not control.j.quit):
		#if network.connected and len(control.commands) > 0:
		if len(control.commands) > 0:
			command = control.commands.popleft()
			print(command)
			if network.connected:
				network.conn.send(command[0])
				network.conn.send(command[1])
	network.exit = True
	