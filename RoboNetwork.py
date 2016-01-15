# RoboNetwork.py
# Contains class for controlling scenery robot through an x-box controller as a thread-based class
# Version - 0.1
# Author - Brian Nguyen
# Requires pyglet 1.2alpha1 or higher
# pip install --upgrade http://pyglet.googlecode.com/archive/tip.zip
# Requires Python 2.7

import threading
import socket
import json
import struct
from collections import deque
import sys

class RoboNetwork(threading.Thread):
	def __init__(self, tcp_ip, tcp_port, tcp_buff_size, udp_target_ip, udp_target_port, timeout, DEBUG = False):
		"""
		Initiates a socket based TCP network that is thread based
		"""
		threading.Thread.__init__(self)
		
		# Setup initial fields
		self.TCP_IP = tcp_ip
		self.TCP_PORT = tcp_port
		self.BUFFER_SIZE = tcp_buff_size
		self.UDP_TARGET_IP = udp_target_ip
		self.UDP_TARGET_PORT = udp_target_port
		self.timeout = timeout
		
		# Create UDP socket
		self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

		# Set flags
		self.connection_started = False # Indicates the TCP connection is being attempted
		self.connected = False			# Indicates the TCP connection is established
		self.receiving = False			# Indicates data should be received in TCP connection
		self.exit = False				# Indicates this thread should run
		
		# Set status string that can be passed to parent GUI
		self.status = 'Server Connection: Not connected'
		
		self.receive_buffer = deque()

	
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
		# Create TCP socket
		self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		# Set timeout for blocking socket calls
		self.tcp_socket.settimeout(self.timeout)
		
		# Bind socket to ip and port
		self.status = 'Server Connection: Binding Socket'
		try:
			self.tcp_socket.bind((self.TCP_IP, self.TCP_PORT))
		except socket.error:
			print("Failed to bind socket")
			self.status = 'Server Connection: Socket Failed to Bind'
			self.connection_started = False
			self.connected = False
			self.tcp_socket.close()
			return self.connected
		
		self.status = 'Server Connection: Waiting for Client'
		# Set up socket to listen
		self.tcp_socket.listen(1)
	
		# Wait for a new client
		try:
			# Attempt to connect
			print("Waiting for client")
			self.conn, self.addr = self.tcp_socket.accept()
			self.connected = True
			self.status = 'Server Connection: Client Connected'
			print("Client connected")
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
		data = '\xde\xad\xbe\xef' + struct.pack('bb', left_value, right_value)
		
		self.udp_socket.sendto(data, (self.UDP_TARGET_IP, self.UDP_TARGET_PORT))
		
		
	def run(self):
		"""
		Main thread run method
		Runs while exit flag is false
		"""
		# Continually run while exit flag is false
		while not self.exit:
			if self.connected:
				if self.receiving:
					# Attempt to get data from connection
					try:
						data = self.conn.recv(self.BUFFER_SIZE)
						#print(data)
						#data1 = struct.unpack('l', data)
						#print(data1)
						#print(sys.getsizeof(data))
						#pktFormat = 'll'
						#pktSize = struct.calcsize(pktFormat)
						#data1 = struct.unpack(pktFormat, data[:pktSize])
					except socket.timeout:
						# Continue to try again if socket timesout
						print("Recieve timeout")
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
		