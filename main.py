# main.py
# Contains class for controlling scenery robot interfacing with two other thread based classes for manual and network control
# NEEED TO CREATE GUI SIGNALS INSTEAD OF THE MANUAL CHANGES IM DOING
# Version - 0.1
# Author - Brian Nguyen
# Requires Python 2.7

from PyQt4 import QtGui, QtCore # Import QtGui module
from PyQt4.QtCore import QThread, QString
from PyQt4.QtGui import QDialog, QFileDialog
import sys				# Allows for command line arguments to be passed in
import time
import main_window_robot		# Layout file
import server_connect_dialog
import struct

from RoboControl import RoboControl
from RoboNetwork import RoboNetwork

# --------------------- ENUM DEFINITION ---------------------
# Python 2 define enum states http://stackoverflow.com/questions/36932/
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
	
# Global enum variable
States = enum('DISCONNECTED', 'SERVER_ONLY', 'MANUAL', 'RECORDING', 'PLAYBACK')
	

class RobotApp(QtGui.QMainWindow, main_window_robot.Ui_MainWindow):
	def __init__(self):
		super(RobotApp, self).__init__()
		
		# Setup ui from precompiled file
		self.setupUi(self)
		
		# Connect signals to buttons
		self.connect_buttons()
		
		# Initiate controlling applications
		self.control = RoboControl(DEBUG=True)
		self.network = RoboNetwork('192.168.1.2', 29281, 16, '192.168.1.3', 29282, 15, DEBUG=True)
		
		# Run controlling applications
		self.control.start()
		self.network.start()
		
		# Set state flags
		self.controller_connected = False
		self.network_connected = False
		
		# Overall state
		self.state = States.DISCONNECTED
		self.controllerConnect.setEnabled(False)
		self.controllerDisconnect.setEnabled(False)
		self.recordPath.setEnabled(False)
		
		# Queue data
		self.filename = None
		self.queues_data = []
		self.queue = []
		
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
		self.controllerDisconnect.clicked.connect(self.disconnect_controller)
		self.loadQueueSet.clicked.connect(self.open)
		self.queueSetSave.clicked.connect(self.save)
		self.recordPath.clicked.connect(self.record)
		self.button_default_style_sheet = self.recordPath.styleSheet()
		
	def record(self):
		if self.state != States.RECORDING:
			print("Clearing Queue of data")
			self.queue = []
			self.control.recording = True
			self.recordPath.setText("End Recording")
			self.recordPath.setStyleSheet('QPushButton {background-color: red; color:white;}')
		elif self.state == States.RECORDING:
			self.control.recording = False
			self.recordPath.setText("Record New Path")
			self.recordPath.setStyleSheet(self.button_default_style_sheet)
			self.queueList.addItem("Untitled")
			self.queue.insert(0, "Untitled")
			self.queues_data.append(self.queue)

	def open(self):
		path = (".")
		fname = QFileDialog.getOpenFileName(self,
				"Scenery Robot - Open", path,
				"Queue Files (*.txt)")
		if fname.isEmpty():
			return
		self.filename = fname
		file = None
		print("Successful open")
		self.queues_data = self.load_queue_file(self.filename)
		print(self.queues_data)
		self.load_queue_window(self.queues_data)
	
	def save(self):
		path = "."
		fname = QFileDialog.getSaveFileName(self, "Scenery Robot - Save As", path,
			"Queue Files: (*.txt)")
		if fname.isEmpty():
			return
			
		self.filename = fname
		print('queues_data', self.queues_data)
		self.save_new_queue(self.filename, self.queues_data)
		
	def save_new_queue(self, filename, queues_data, queuename="UNTITLED"):
		"""
		This function will open a file and append to it a new queue with a title and data.
		@params: filename: the save file (text file where info will be stored)
			list_to_save: the data of the new queue being saved
			listname: the name of the queue being saved as a list
		"""
		print("SAVING THIS OBJECT:")
		print(queues_data)
		with open(filename, 'w') as f:
			for queue in queues_data:
				for data in queue:
					f.write(str(data))
					f.write('\n')
				f.write('\n')
			f.close()
	
	def load_queue_window(self, queues_data):
		"""
		"""
		self.queueList.clear()
		for queue in queues_data:
			self.queueList.addItem(queue[0])
		
	def load_queue_file(self, filename):
		"""
		This function first reads in an entire list, line by line. It then creates a list of lists where
		each list contains all the points in a list
		@params: filename: the file to be loaded
		"""
		queue_list = []
		with open(filename) as f:
			i = 0
			for line in f:
				if not line.startswith('[') and not line.startswith('\n'):
					queue_list.append([])
					queue_list[i] = [line.rstrip()]
				elif line.startswith('['):
					queue_list[i].append(line.rstrip())
				else:
					i += 1
			f.close()
		return queue_list
	
	def check_events(self):
		"""
		Overall event checking for main thread
		"""
		self.check_controller_events()
		self.check_network_events()
		self.check_app_events()
		
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
	
	def check_app_events(self):
		"""
		Checks variables to update app state
		"""
		# If disconnected, wait until controller and network connected to go into manual mode
		if not self.network_connected and self.state != States.DISCONNECTED:
			print("Robot got disconnected from network")
			self.state == States.DISCONNECTED
			self.robot_control_mode.setText("Robot Control: Disconnected")
			self.controllerConnect.setEnabled(False)
			self.controllerDisconnect.setEnabled(False)
		elif self.network_connected and self.state == States.DISCONNECTED:
			print("Control is SERVER_ONLY")
			self.state = States.SERVER_ONLY
			self.robot_control_mode.setText("Robot Control: Server Control")
			self.controllerConnect.setEnabled(True)
			self.controllerDisconnect.setEnabled(False)
		elif self.network_connected and self.controller_connected and self.state == States.SERVER_ONLY:
			print("Control is manual")
			self.state = States.MANUAL
			
			self.robot_control_mode.setText("Robot Control: Manual Control")
			self.controllerConnect.setEnabled(False)
			self.controllerDisconnect.setEnabled(True)
			self.recordPath.setEnabled(True)
			
		elif (self.state == States.MANUAL or self.state == States.RECORDING) and not self.controller_connected:
			print("Control is SERVER_ONLY")
			self.state = States.SERVER_ONLY
			self.robot_control_mode.setText("Robot Control: Server Control")
			self.controllerConnect.setEnabled(True)
			self.controllerDisconnect.setEnabled(False)
			self.control.recording = False # Controller got disconnected
			
		elif self.state == States.MANUAL and self.control.is_recording():
			print("Control is recording")
			self.state = States.RECORDING
			self.network.receiving = True
			self.robot_control_mode.setText("Robot Control: Recording")
			
		elif self.state == States.RECORDING and not self.control.is_recording():
			self.state = States.MANUAL
			print("Control is manual")
			self.network.receiving = False
			self.robot_control_mode.setText("Robot Control: Manual Control")
	
	def handle_server_box(self):
		"""
		Handle pop up
		"""
		self.dialog = QDialog()
		self.ui = server_connect_dialog.Ui_Dialog()
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
		
	def disconnect_controller(self):
		self.control.disconnect()
		
		
	def check_controller_connected(self):
		"""
		Checks if controller is connected
		Enables or disables connected button accordingly
		Sets label text from control status
		"""
		self.controller_connected = self.control.is_connected()
		#self.controllerConnect.setEnabled(not self.controller_connected)
		self.controllerConnect.setChecked(True)
		
		return self.controller_connected
		
		
# --------------------- NETWORK METHODS ---------------------		
	def connect_to_network(self):
		"""
		Opens server to connect to client
		"""
		if not self.network.connection_started:
			self.network.start_connection()
		#self.network_connected = True
		
	def check_network_connected(self):
		"""
		Checks if network is connected
		Enables or disables connect button accordingly
		Sets label text from network status
		"""
		self.server_connection_label.setText(self.network.status)
		#if self.network_connected:
		#	self.server_connection_label.setText('Server Connection: Client Connected')
		self.network_connected = self.network.is_connected()
		self.serverStart.setEnabled(not self.network_connected and not self.network.connection_started)
		return self.network_connected
	
# ------------------- MAIN APP EVENTS ------------------------------
	def closeEvent(self, event):
		"""
		Overriden close event that will terminate main thread
		"""
		self.mainThread.running = False
		super(RobotApp, self).closeEvent(event)
		
# --------------------- MAIN THREAD CLASS ---------------------
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
			if self.app.state == States.MANUAL or self.app.state == States.RECORDING:

			#if self.app.network_connected and self.app.controller_connected:	
				time.sleep(0.1)
				try:
					self.app.network.send_command(self.app.control.left_value, self.app.control.right_value)
					print("sending:", self.app.control.left_value, self.app.control.right_value)
				except Exception as e:
					print("There was an issue")
					continue
				#if len(self.app.network.receive_buffer) > 0:
				if self.app.state == States.RECORDING:
					pass
					#self.app.queue.append([0, 0])
					#print("Got data!")
						
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