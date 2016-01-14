# RoboNetwork.py
# Contains class for controlling scenery robot through an x-box controller as a thread-based class
# Version - 0.1
# Author - Brian Nguyen
# Requires pyglet 1.2alpha1 or higher
# pip install --upgrade http://pyglet.googlecode.com/archive/tip.zip
import threading
import socket
import json
import binascii
import struct

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
		
		# Set flags
		self.connection_started = False
		self.connected = False
		self.exit = False
		
		# Set status string that can be passed to parent GUI
		self.status = 'Server Connection: Not connected'

	
	def start_connection(self):
		"""
		Sets flag to start network connection - Done to avoid blocking calling program
		"""
		self.connection_started = True
	
	def connect(self):
		"""
		Attempts to listen and allow a client to connect
		Returns True if client connected, False if socket timesout
		"""
		# Create socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		# Set timeout for blocking socket calls
		self.s.settimeout(self.timeout)
		
		# Bind socket to ip and port
		self.status = 'Server Connection: Binding Socket'
		try:
			self.s.bind((self.TCP_IP, self.TCP_PORT))
		except socket.error:
			print("Failed to bind socket")
			self.status = 'Server Connection: Socket Failed to Bind'
			self.connection_started = False
			self.connected = False
			self.s.close()
			return self.connected
		
		self.status = 'Server Connection: Waiting for Client'
		# Set up socket to listen
		self.s.listen(1)
	
		# Wait for a new client
		try:
			# Attempt to connect
			print("Waiting for client")
			self.conn, self.addr = self.s.accept()
			self.connected = True
			self.status = 'Server Connection: Client Connected'
		except socket.timeout:
			print("Socket timeout")
			self.status = 'Server Connection: Client timeout'
			# If timmed out, set flag to false
			self.connected = False
		
		self.connection_started = False
		return self.connected
		
	def is_connected(self):
		"""
		"""
		return self.connected
	
	def send_command(self, left_value, right_value):
		"""
		Sends command as byte string with A5 as header 
		"""
		data = '\xA5' + struct.pack('bb', left_value, right_value)
		
		try:
			self.conn.send(data)
		except socket.error:
			return
		
	def run(self):
		"""
		Main thread run method
		Runs while exit flag is false
		"""
		# Continually run while exit flag is false
		while not self.exit:
			if self.connected:
				# Attempt to get data from connection
				try:
					data = self.conn.recv(self.BUFFER_SIZE)
				except socket.timeout:
					# Continue to try again if socket timesout
					continue
				except socket.error:
					continue
			elif self.connection_started:
				self.connect()
			
		print("Network Thread Ending")
	 
	
	def close(self):
		"""
		Close thread
		"""
		self.exit = True
		if self.connected:
			self.conn.close()
			self.connected = False
			return True
		