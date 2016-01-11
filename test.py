import json
import socket
"""
TCP_IP = '192.168.1.100'
TCP_PORT = 39281
BUFFER_SIZE = 20

s = socket.socket(socket.AF_IINET, socket.SOCK_STREAM)
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
from xinput import XInputJoystick
from operator import itemgetter, attrgetter
# Requires pyglet 1.2alpha1 or higher
# pip install --upgrade http://pyglet.googlecode.com/archive/tip.zip

class RoboControl():
	def __init__(self):
	
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
						
		print('found %d devices: %s' % (len(self.joysticks), self.device_numbers))

		if not self.joysticks:
			print("No joysticks found, exiting")
			return None
		
		# Use first joystick
		self.j = self.joysticks[0]
	
		print('Using device %d' % self.j.device_number)
		print('Press back button on controller to quit.')
	
		self.j.quit = False
	
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
						print("true")
					else:
						self.r_joy_record.append(0)
				elif axis == 'r_thumb_y':
					self.r_joy_record.append(value)
					if len(self.l_joy_record) > 0:
						self.l_joy_record.append(self.l_joy_record[-1])
					else:
						self.l_joy_record.append(0)
			
			if axis == "left_trigger":
				left_speed = value
			elif axis == "right_trigger":
				right_speed = value
			self.j.set_vibration(left_speed, right_speed)

	def run(self):
		while not self.j.quit:
			self.j.dispatch_events()
			time.sleep(0.01)
		
	print('Quiting!')
	
if __name__ == "__main__":
	control = RoboControl()
	control.run()
	