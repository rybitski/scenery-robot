# RoboControl.py
# Contains class for connecting to a scenery robot network and send data as a thread-based class
# Version - 0.1
# Author - Brian Nguyen

import sys
import time
import threading
from collections import deque
from xinput import XInputJoystick
from operator import itemgetter, attrgetter

class RoboControl(threading.Thread):
	def __init__(self, DEBUG=False):
		threading.Thread.__init__(self)
		# Set debugging flag
		self.debug = DEBUG
		
		# Grabs 1st available gamepad, logging changes to the screen
		self.joysticks = XInputJoystick.enumerate_devices()
		self.device_numbers = list(map(attrgetter('device_number'), self.joysticks))
	
		# Setup state as normal
		self.state = 'normal'
		
		# Setup connection flag as initially False
		self.connected = False
		
		# Maps internal button integer number to human-readable syntax
		self.button_map = {
					"1": "DUP", "2": "DDOWN", "3": "DLEFT", "4": "DRIGHT",
					"5": "START", "6": "BACK", "7": "LJOYTOGGLE", "8": "RJOYTOGGLE",
					"9": "LB", "10": "RB", "13": "A", "14": "B", "15": "X", "16": "Y",
				}
				
		# Maps human-readable syntax to internal button number
		self.inv_button_map = {v: k for k, v in self.button_map.items()}
		
		if self.debug:
			print('found %d controller devices: %s' % (len(self.joysticks), self.device_numbers))

		# Flag for running thread to exit
		self.exit = False
		
		# Queue of commands
		self.commands = deque()
		
	def connect(self):
		"""
		Attempt connection to a joystick
		Returns True if connection succeeded
		Returns False if connection fails
		"""
		# Attempt to connect to first joystick
		if not self.joysticks:
			if self.debug:
				print("No joysticks found, exiting")
			return False
		else:
			self.j = self.joysticks[0]
			self.connected = True
			
		@self.j.event
		def on_button(button, pressed):
			self.exit = (button == self.get_button_num('BACK') and pressed)
				
			if (button == self.get_button_num('START') and pressed):
				if self.state == 'normal':
					self.state = 'record'
					if self.debug:
						print("Starting to record")
					#self.l_joy_record[:] = []
					#self.r_joy_record[:] = []
				elif self.state == 'record':
					self.state = 'normal'
					if self.debug:
						print("End record")
						"""
						for index in range(0, len(self.l_joy_record)):
							print(("L:%1.5f , R:%1.5f") % (self.l_joy_record[index], self.r_joy_record[index]))
						"""
						
		@self.j.event
		def on_axis(axis, value):
			left_speed = 0
			right_speed = 0

			if self.state == 'record':
				if axis == 'l_thumb_y':
					"""
					self.l_joy_record.append(value)
					if len(self.r_joy_record) > 0:
						self.r_joy_record.append(self.r_joy_record[-1])
					else:
						self.r_joy_record.append(0)
					"""
					# Maps analog values of -0.5 to 0.5 to -127 to 127 for motor control
					value_convert = int(round(sensitivity_scale(value, 0.5, -0.5, 0.5, -127, 127)))
					
					# Account for noisy deadzone in middle of joysticks
					if (abs(value_convert) <= 10):
						value_convert = 0
						
					# Add command to command queue
					self.commands.append(
						('L', value_convert)
					)
				elif axis == 'r_thumb_y':
					"""
					self.r_joy_record.append(value)
					if len(self.l_joy_record) > 0:
						self.l_joy_record.append(self.l_joy_record[-1])
					else:
						self.l_joy_record.append(0)
					"""
					# Maps analog values of -0.5 to 0.5 to -127 to 127 for motor control
					value_convert = int(round(sensitivity_scale(value, 0.5, -0.5, 0.5, -127, 127)))
					
					# Account for noisy deadzone in middle of joysticks
					if (abs(value_convert) <= 10):
						value_convert = 0
						
					# Add command to command queue
					self.commands.append(
						('R', value_convert)
					)
					
			if axis == "left_trigger":
				left_speed = value
			elif axis == "right_trigger":
				right_speed = value
			self.j.set_vibration(left_speed, right_speed)
		
		if self.debug:
			print('Using device %d' % self.j.device_number)
			print('Press back button on controller to quit.')
		return True
	
	def get_button_num(self, name):
		"""
		Returns internal button number based on name
		Ex. "START" -> 5
		"""
		return int(self.inv_button_map[name])

	def run(self):
		"""
		Continually runs thread as long as exit flag is False
		"""
		while not self.exit:
			try:
				# Register any controller events
				self.j.dispatch_events()
			except RuntimeError:
				# Controller was disconnected, exit controller
				print("Controller is not connected!")
				self.connected = False
				self.exit = True
			time.sleep(0.01)
		print("Joystick shutting down!")
	
def sensitivity_scale(x_in, sensitivity, original_min, original_max, desired_min, desired_max):
	"""
	Returns smoothed data point mapped to new range based on sensitivity
	"""
	linear_scale = ((desired_max - desired_min) * (x_in - original_min))/(original_max-original_min) + desired_min
	scale_to_1 = 2 / (original_max-original_min)
	xin_sensitive = sensitivity * (x_in*scale_to_1)**3 + (1-sensitivity) * (x_in*scale_to_1)
	xin_sensitive /= scale_to_1
	sensitivity_scaled = ((desired_max - desired_min) * (xin_sensitive - original_min))/(original_max-original_min) + desired_min
	return sensitivity_scaled
