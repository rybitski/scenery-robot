# RoboNetwork.py
# Contains class for controlling scenery robot through an x-box controller as a thread-based class
# Version - 0.1
# Author - Brian Nguyen
# Requires pyglet 1.2alpha1 or higher
# pip install --upgrade http://pyglet.googlecode.com/archive/tip.zip
import threading
import socket

class RoboNetwork(threading.Thread):
	def __init__(self, ip, port, buff_size, timeout, DEBUG = False):
		"""
		Initiates a socket based TCP network that is thread based
		"""
		threading.Thread.__init__(self)
		
		# Setup initial fields
		self.TCP_IP = ip
		self.TCP_PORT = port
		self.BUFFER_SIZE = buff_size
		self.timeout = timeout
		
		# Create socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Bind socket to ip and port
		self.s.bind((self.TCP_IP, self.TCP_PORT))
		
		# Set flags
		self.connected = False
		self.exit = False
		
		# Set timeout for blocking socket calls
		self.s.settimeout(self.timeout)
	
	def connect(self):
		"""
		Attempts to listen and allow a client to connect
		Returns True if client connected, False if socket timesout
		"""
		# Set up socket to listen
		self.s.listen(1)
	
		# Wait for a new client
		try:
			# Attempt to connect
			self.conn, self.addr = self.s.accept()
			self.connected = True
		except socket.timeout:
			# If timmed out, set flag to false
			self.connected = False
		
		return self.connected
		
	def run(self):
		"""
		Main thread run method
		Runs while exit flag is false
		"""
		# If not connected, don't run
		if not self.connected:
			return
		
		# Else run while exit flag is false
		while not self.exit:
			# Attempt to get data from connection
			try:
				data = self.conn.recv(self.BUFFER_SIZE)
			except socket.timeout:
				# Continue to try again if socket timesout
				continue
	
	def close(self):
		"""
		Close connection if one exists
		Returns True if close successful
		Returns False if close failed
		"""
		if self.connected:
			self.conn.close()
			self.connected = False
			return True
		else:
			return False