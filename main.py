from PyQt4 import QtGui # Import QtGui module
from PyQt4.QtCore import QThread
import sys				# Allows for command line arguments to be passed in
import time
import main_window_robot		# Layout file
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
		self.network = RoboNetwork('192.168.1.2', 29281, 20, 5, DEBUG=True)
		
		# Set state flags
		self.controller_connected = False
		self.network_connected = False
		
		self.state = States.DISCONNECTED
		
		self.mainThread = MainThread(self)
		self.mainThread.start()
	
	def connect_buttons(self):
		self.controllerConnect.clicked.connect(self.connect_to_controller)
		self.serverStart.clicked.connect(self.connect_to_network)
	
	def connect_to_controller(self):
		self.controller_connected = self.control.connect()
		if self.controller_connected:
			 #self.controllerStatus.setText("Controller: Connected!")
			 self.control.start()
		else:
			pass
			#self.controllerStatus.setText("Controller: Failed to connect")
		return self.controller_connected
		
	def connect_to_network(self):
		self.network_connected = self.network.connect()
		return self.network_connected
		
	def closeEvent(self, event):
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
		self.app.connect_to_controller()
		while self.running:
			if self.app.state == States.MANUAL:
				if len(self.app.control.commands) > 0:
					command = self.app.control.commands.popleft()
					print(command)
					if network.connected:
						self.app.network.conn.send(command[0])
						self.app.network.conn.send(command[1])
			else:
				if len(self.app.control.commands) > 0:
					command = self.app.control.commands.popleft()
					self.app.network.send_command(command)
		
		# Main thread has ended, end controller and network threads if they are running
		self.app.control.close()
		self.app.network.close()
		
			
def main():
	app = QtGui.QApplication(sys.argv)	# New Instance of QApplication
	form = RobotApp()					# Set form as RobotApp
	form.show()
	app.exec_()							# Execute app
	
if __name__ == "__main__":
	main()