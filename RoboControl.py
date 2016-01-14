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
		
		# Setup variables to maintain real time left and right axis values
		self.left_value = 0
		self.right_value = 0
		
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
		
		self.joysticks = XInputJoystick.enumerate_devices()
		self.j = None
		
		# Flag for running thread to exit
		self.exit = False
		
		# Queue of commands
		self.commands = deque()
		
		# Set status string that can be passed to parent GUI
		self.status = 'Controller Connection: Disconnected'
		
	def is_connected(self):
		"""
		Returns True if controller is connected and false if disconnected
		"""
		return self.connected
		
	def connect(self):
		"""
		Attempt connection to a joystick
		Returns True if connection succeeded
		Returns False if connection fails
		"""
		
		# Grabs 1st available gamepad, logging changes to the screen
		self.joysticks = XInputJoystick.enumerate_devices()
		self.device_numbers = list(map(attrgetter('device_number'), self.joysticks))
		if self.debug:
			print('found %d controller devices: %s' % (len(self.joysticks), self.device_numbers))
			
		# Attempt to connect to first joystick
		if not self.joysticks:
			if self.debug:
				self.status = 'Controller Connection: No controller found'
				print("No joysticks found, exiting")
			self.connected = False
			return False
		else:
			self.j = self.joysticks[0]
			self.connected = True
			self.status = 'Controller Connection: Connected'
		
		""" Define event handlers for axis and buttons """
		@self.j.event
		def on_button(button, pressed):
			self.exit = (button == self.get_button_num('BACK') and pressed)
						
		@self.j.event
		def on_axis(axis, value):
			left_speed = 0
			right_speed = 0
			
			if axis == 'l_thumb_y':
					
				# Maps analog values of -0.5 to 0.5 to -127 to 127 for motor control
				value_convert = int(round(sensitivity_scale(value, 0.5, -0.5, 0.5, -127, 127)))
				
				# Account for noisy deadzone in middle of joysticks
				if (abs(value_convert) <= 10):
					value_convert = 0
				
				self.left_value = value_convert
					
			elif axis == 'r_thumb_y':
					
				# Maps analog values of -0.5 to 0.5 to -127 to 127 for motor control
				value_convert = int(round(sensitivity_scale(value, 0.5, -0.5, 0.5, -127, 127)))
				
				# Account for noisy deadzone in middle of joysticks
				if (abs(value_convert) <= 10):
					value_convert = 0
					
				self.right_value = value_convert
		
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
			# If controller connected, dispatch events, otherwise just loop
			if self.connected:
				try:
					# Register any controller events
					self.j.dispatch_events()
				except RuntimeError:
					print("Controller is not connected!")
					self.status = 'Controller Connection: Controller Disconnected'
					self.connected = False
			time.sleep(0.01)
			
		print("Control Thread Ending")
		
	def close(self):
		"""
		Sets the exit flag to end the main loop
		"""
		self.connected = False
		self.exit = True
		return True

	
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
