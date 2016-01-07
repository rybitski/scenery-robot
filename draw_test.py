from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.view = View(self)
        self.button = QtGui.QPushButton('Clear View', self)
        self.button.clicked.connect(self.handleClearView)
        self.textbox = QtGui.QLineEdit(self)
		
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.button)
        layout.addWidget(self.textbox)
		

    def handleClearView(self):
        self.view.scene().clear()
        self.textbox.setText('')

class View(QtGui.QGraphicsView):
    def __init__(self, parent):
        QtGui.QGraphicsView.__init__(self, parent)
        self.setScene(QtGui.QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        self.points = []

    def mousePressEvent(self, event):
        self.lastPos = event.pos()
        self._start = event.pos()
        
    def mouseMoveEvent(self, event):
        self.currPos = event.pos()
        if (self.lastPos.x != self.currPos.x) and (self.lastPos.y != self.currPos.y):
			start = QtCore.QPointF(self.mapToScene(self.lastPos))
			end = QtCore.QPointF(self.mapToScene(self.currPos))
			self.scene().addItem(
            QtGui.QGraphicsLineItem(QtCore.QLineF(start, end)))
			self.lastPos = event.pos()
			self.points.append(self.currPos)
		
    
    def mouseReleaseEvent(self, event):
        self.window().textbox.setText('yay')
        self.window().textbox.setText(','.join(str((e.x(), e.y())) for e in self.points))
        self.points = []
		
if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())