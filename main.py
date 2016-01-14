from PyQt4 import QtGui, QtCore # Import QtGui module
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QDialog
import sys				# Allows for command line arguments to be passed in
import time
import main_window_robot		# Layout file
import server_connect_dialog
import struct

from RoboControl import RoboControl
from RoboNetwork import RoboNetwork

# Python 2 define enum states http://stackoverflow.com/questions/36932/
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
	
# Global enum variable
States = enum('DISCONNECTED', 'MANUAL', 'RECORDING', 'PLAYBACK')
	

class RobotApp(QtGui.QMainWindow, main_window_robot.Ui_MainWindow):
	def __init__(self):
		super(RobotApp, self).__init__()
		
		# Setup ui from precompiled file
		self.setupUi(self)
		
		# Connect signals to buttons
		self.connect_buttons()
		
		# Initiate controlling applications
		self.control = RoboControl(DEBUG=True)
		self.network = RoboNetwork('192.168.1.2', 29281, 3, 5, DEBUG=True)
		
		# Run controlling applications
		self.control.start()
		self.network.start()
		
		# Set state flags
		self.controller_connected = False
		self.network_connected = False
		
		# Using this for errors from network control
		self.network_status = 0
		
		# Overall state
		self.state = States.DISCONNECTED
		
		# Start main thread
		self.mainThread = MainThread(self)
		self.mainThread.start()
	
	def connect_buttons(self):
		"""
		Connect buttons to methods
		"""
		self.controllerConnect.clicked.connect(self.connect_to_controller)
		self.serverStart.clicked.connect(self.connect_to_network)
		self.ipSpecify.clicked.connect(self.handle_server_box)
	
	def check_events(self):
		"""
		Overall event checking for main thread
		"""
		self.check_controller_events()
		self.check_network_events()
		
	def check_network_events(self):
		"""
		Checks events related to network server
		"""
		self.check_network_connected()
	
	def check_controller_events(self):
		"""
		Checks events related to controller
		"""
		self.check_controller_connected()
		
	def handle_server_box(self):
		self.dialog = QDialog()
		self.ui = server_connect_dialog.Ui_ServerEntry()
		self.ui.setupUi(self.dialog)
		self.dialog.show()
		
# --------------------- CONTROLLER METHODS ---------------------
	def connect_to_controller(self):
		"""
		Connects to the controller and returns True if connection succeeded
		and False if not
		"""
		self.controller_connected = self.control.connect()	
		return self.controller_connected
		
	def check_controller_connected(self):
		"""
		Checks if controller is connected
		Enables or disables connected button accordingly
		"""
		self.controller_connected = self.control.is_connected()
		self.controllerConnect.setEnabled(not self.controller_connected)
		return self.controller_connected
		
# --------------------- NETWORK METHODS ---------------------		
	def connect_to_network(self):
		"""
		Opens server to connect to client
		"""
		if not self.network.connection_started:
			self.network.start_connection()
		
	def check_network_connected(self):
		"""
		Checks if network is connected
		"""
		self.server_connection_label.setText(self.network.status)
		self.network_connected = self.network.is_connected()
		self.serverStart.setEnabled(not self.network_connected and not self.network.connection_started)
		return self.network_connected
	
	
# ------------------- MAIN APP EVENTS ------------------------------
	def keyPressEvent(self, qKeyEvent):
		if qKeyEvent.key() == QtCore.Qt.Key_Return: 
			print('Enter pressed')
			print("sending:", self.control.left_value, self.control.right_value)
			data = '\xA5' + struct.pack('bb', -127, -127)
			data1 = '\xA5\x81\x81'
			print(data)
			print(data1)
			#self.network.send_command(self.control.left_value, self.control.right_value)
		else:
			super().keyPressEvent(qKeyEvent)
	
	def closeEvent(self, event):
		"""
		Overriden close event that will terminate main thread
		"""
		self.mainThread.running = False
		super(RobotApp, self).closeEvent(event)
		
class MainThread(QThread):

	def __init__(self, app):
		QThread.__init__(self)
		self.app = app
		self.running = True
		
	def __del__(self):
		self.wait()

	def run(self):
		while self.running:
			self.app.check_events()
			
			if self.app.controller_connected and self.app.network_connected:
			#if self.app.controller_connected:
				time.sleep(0.1)
				print("sending:", self.app.control.left_value, self.app.control.right_value)
				self.app.network.send_command(self.app.control.left_value, self.app.control.right_value)
				
				
		# Main thread has ended, end controller and network threads if they are running
		self.app.control.close()
		self.app.network.close()
		print("Ending Main Thread")
		

def main():
	app = QtGui.QApplication(sys.argv)	# New Instance of QApplication
	form = RobotApp()					# Set form as RobotApp
	form.show()
	app.exec_()							# Execute app
	
if __name__ == "__main__":
	main()