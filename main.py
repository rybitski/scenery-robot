from PyQt4 import QtGui # Import QtGui module
import sys				# Allows for command line arguments to be passed in
import main_window		# Layout file
from draw_test import *

class RobotApp(QtGui.QMainWindow, main_window.Ui_MainWindow):
	def __init__(self):
		super(RobotApp, self).__init__()
		self.setupUi(self)
		self.map.hide()
		self.mapWidget = Window()
		self.horizontalLayout.addWidget(self.mapWidget)

def main():
	app = QtGui.QApplication(sys.argv)	# New Instance of QApplication
	form = RobotApp()					# Set form as RobotApp
	form.show()
	app.exec_()							# Execute app
	
if __name__ == "__main__":
	main()