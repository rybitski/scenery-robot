# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_window_robot.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(983, 991)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_6 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.checkWorkingLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkWorkingLabel.sizePolicy().hasHeightForWidth())
        self.checkWorkingLabel.setSizePolicy(sizePolicy)
        self.checkWorkingLabel.setMinimumSize(QtCore.QSize(0, 30))
        self.checkWorkingLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkWorkingLabel.setFont(font)
        self.checkWorkingLabel.setAutoFillBackground(True)
        self.checkWorkingLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.checkWorkingLabel.setLineWidth(3)
        self.checkWorkingLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.checkWorkingLabel.setObjectName(_fromUtf8("checkWorkingLabel"))
        self.gridLayout_6.addWidget(self.checkWorkingLabel, 0, 0, 1, 1)
        self.server_connection_label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.server_connection_label.sizePolicy().hasHeightForWidth())
        self.server_connection_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.server_connection_label.setFont(font)
        self.server_connection_label.setFrameShape(QtGui.QFrame.StyledPanel)
        self.server_connection_label.setObjectName(_fromUtf8("server_connection_label"))
        self.gridLayout_6.addWidget(self.server_connection_label, 0, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.queueControl_5 = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueControl_5.sizePolicy().hasHeightForWidth())
        self.queueControl_5.setSizePolicy(sizePolicy)
        self.queueControl_5.setMinimumSize(QtCore.QSize(0, 200))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.queueControl_5.setFont(font)
        self.queueControl_5.setObjectName(_fromUtf8("queueControl_5"))
        self.verticalLayout = QtGui.QVBoxLayout(self.queueControl_5)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.queueList = QtGui.QListWidget(self.queueControl_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueList.sizePolicy().hasHeightForWidth())
        self.queueList.setSizePolicy(sizePolicy)
        self.queueList.setObjectName(_fromUtf8("queueList"))
        self.verticalLayout.addWidget(self.queueList)
        self.gridLayout.addWidget(self.queueControl_5, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame)
        self.map = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.map.sizePolicy().hasHeightForWidth())
        self.map.setSizePolicy(sizePolicy)
        self.map.setMinimumSize(QtCore.QSize(0, 0))
        self.map.setFrameShape(QtGui.QFrame.StyledPanel)
        self.map.setFrameShadow(QtGui.QFrame.Raised)
        self.map.setObjectName(_fromUtf8("map"))
        self.gridLayout_3 = QtGui.QGridLayout(self.map)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.graphicsView = QtGui.QGraphicsView(self.map)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout_3.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.queueGo = QtGui.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.queueGo.setFont(font)
        self.queueGo.setObjectName(_fromUtf8("queueGo"))
        self.gridLayout_2.addWidget(self.queueGo, 1, 0, 1, 1)
        self.portSpecify = QtGui.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.portSpecify.setFont(font)
        self.portSpecify.setObjectName(_fromUtf8("portSpecify"))
        self.gridLayout_2.addWidget(self.portSpecify, 3, 3, 1, 1)
        self.queueLoad = QtGui.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.queueLoad.setFont(font)
        self.queueLoad.setObjectName(_fromUtf8("queueLoad"))
        self.gridLayout_2.addWidget(self.queueLoad, 0, 0, 1, 1)
        self.ipSpecify = QtGui.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ipSpecify.setFont(font)
        self.ipSpecify.setObjectName(_fromUtf8("ipSpecify"))
        self.gridLayout_2.addWidget(self.ipSpecify, 1, 3, 1, 1)
        self.queueStop = QtGui.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.queueStop.setFont(font)
        self.queueStop.setObjectName(_fromUtf8("queueStop"))
        self.gridLayout_2.addWidget(self.queueStop, 3, 0, 1, 1)
        self.controllerConnect = QtGui.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.controllerConnect.setFont(font)
        self.controllerConnect.setObjectName(_fromUtf8("controllerConnect"))
        self.gridLayout_2.addWidget(self.controllerConnect, 0, 3, 1, 1)
        self.queueAdd = QtGui.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.queueAdd.setFont(font)
        self.queueAdd.setObjectName(_fromUtf8("queueAdd"))
        self.gridLayout_2.addWidget(self.queueAdd, 1, 1, 1, 1)
        self.queueLoadPrev = QtGui.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.queueLoadPrev.setFont(font)
        self.queueLoadPrev.setObjectName(_fromUtf8("queueLoadPrev"))
        self.gridLayout_2.addWidget(self.queueLoadPrev, 0, 1, 1, 1)
        self.serverStart = QtGui.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.serverStart.setFont(font)
        self.serverStart.setObjectName(_fromUtf8("serverStart"))
        self.gridLayout_2.addWidget(self.serverStart, 0, 4, 1, 1)
        self.recordPath = QtGui.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.recordPath.setFont(font)
        self.recordPath.setObjectName(_fromUtf8("recordPath"))
        self.gridLayout_2.addWidget(self.recordPath, 3, 1, 1, 1)
        self.manualControl = QtGui.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.manualControl.setFont(font)
        self.manualControl.setObjectName(_fromUtf8("manualControl"))
        self.gridLayout_2.addWidget(self.manualControl, 0, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.graphicsView.raise_()
        self.horizontalLayout.addWidget(self.map)
        self.gridLayout_6.addLayout(self.horizontalLayout, 1, 0, 1, 3)
        self.frame_3 = QtGui.QFrame(self.centralwidget)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.eStopBox = QtGui.QGroupBox(self.frame_3)
        self.eStopBox.setObjectName(_fromUtf8("eStopBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.eStopBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.eStop1 = QtGui.QPushButton(self.eStopBox)
        self.eStop1.setObjectName(_fromUtf8("eStop1"))
        self.verticalLayout_3.addWidget(self.eStop1)
        self.eStop2 = QtGui.QPushButton(self.eStopBox)
        self.eStop2.setObjectName(_fromUtf8("eStop2"))
        self.verticalLayout_3.addWidget(self.eStop2)
        self.horizontalLayout_2.addWidget(self.eStopBox)
        self.groupBox_3 = QtGui.QGroupBox(self.frame_3)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.progressBar = QtGui.QProgressBar(self.groupBox_3)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout_4.addWidget(self.progressBar)
        self.frame_4 = QtGui.QFrame(self.groupBox_3)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(0, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.timeLabel = QtGui.QLabel(self.frame_4)
        self.timeLabel.setObjectName(_fromUtf8("timeLabel"))
        self.horizontalLayout_3.addWidget(self.timeLabel)
        self.time = QtGui.QTimeEdit(self.frame_4)
        self.time.setReadOnly(True)
        self.time.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.time.setObjectName(_fromUtf8("time"))
        self.horizontalLayout_3.addWidget(self.time)
        spacerItem1 = QtGui.QSpacerItem(7, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.timeLeftLabel = QtGui.QLabel(self.frame_4)
        self.timeLeftLabel.setObjectName(_fromUtf8("timeLeftLabel"))
        self.horizontalLayout_3.addWidget(self.timeLeftLabel)
        self.timeLeft = QtGui.QTimeEdit(self.frame_4)
        self.timeLeft.setReadOnly(True)
        self.timeLeft.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.timeLeft.setObjectName(_fromUtf8("timeLeft"))
        self.horizontalLayout_3.addWidget(self.timeLeft)
        spacerItem2 = QtGui.QSpacerItem(0, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_4.addWidget(self.frame_4)
        self.horizontalLayout_2.addWidget(self.groupBox_3)
        self.gridLayout_6.addWidget(self.frame_3, 2, 0, 1, 3)
        self.controller_connection_label_2 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controller_connection_label_2.sizePolicy().hasHeightForWidth())
        self.controller_connection_label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.controller_connection_label_2.setFont(font)
        self.controller_connection_label_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.controller_connection_label_2.setObjectName(_fromUtf8("controller_connection_label_2"))
        self.gridLayout_6.addWidget(self.controller_connection_label_2, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 983, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_DWG = QtGui.QAction(MainWindow)
        self.actionLoad_DWG.setObjectName(_fromUtf8("actionLoad_DWG"))
        self.actionLoad_DWG_2 = QtGui.QAction(MainWindow)
        self.actionLoad_DWG_2.setObjectName(_fromUtf8("actionLoad_DWG_2"))
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionAhhhhh = QtGui.QAction(MainWindow)
        self.actionAhhhhh.setObjectName(_fromUtf8("actionAhhhhh"))
        self.menuFile.addAction(self.actionLoad_DWG)
        self.menuFile.addAction(self.actionLoad_DWG_2)
        self.menuTools.addAction(self.actionSettings)
        self.menuHelp.addAction(self.actionAhhhhh)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.checkWorkingLabel.setText(_translate("MainWindow", "Path Status: No Issues Detected", None))
        self.server_connection_label.setText(_translate("MainWindow", "Server Connection: Disconnected", None))
        self.queueControl_5.setTitle(_translate("MainWindow", "Queue", None))
        self.queueGo.setText(_translate("MainWindow", "Go", None))
        self.portSpecify.setText(_translate("MainWindow", "Specify Port", None))
        self.queueLoad.setText(_translate("MainWindow", "Load Queue", None))
        self.ipSpecify.setText(_translate("MainWindow", "Specify IP", None))
        self.queueStop.setText(_translate("MainWindow", "Stop", None))
        self.controllerConnect.setText(_translate("MainWindow", "Connect Controller", None))
        self.queueAdd.setText(_translate("MainWindow", "Add New Queue", None))
        self.queueLoadPrev.setText(_translate("MainWindow", "Load Previous Queue", None))
        self.serverStart.setText(_translate("MainWindow", "Start Server", None))
        self.recordPath.setText(_translate("MainWindow", "Record New Path", None))
        self.manualControl.setText(_translate("MainWindow", "Manual Control Mode", None))
        self.eStopBox.setTitle(_translate("MainWindow", "E-Stops", None))
        self.eStop1.setText(_translate("MainWindow", "E-Stop 1", None))
        self.eStop2.setText(_translate("MainWindow", "E-Stop 2", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Progress", None))
        self.timeLabel.setText(_translate("MainWindow", "Time", None))
        self.time.setDisplayFormat(_translate("MainWindow", "mm:ss", None))
        self.timeLeftLabel.setText(_translate("MainWindow", "Time Left", None))
        self.timeLeft.setDisplayFormat(_translate("MainWindow", "mm:ss", None))
        self.controller_connection_label_2.setText(_translate("MainWindow", "Controller Connection: Disconnected", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionLoad_DWG.setText(_translate("MainWindow", "Reset", None))
        self.actionLoad_DWG_2.setText(_translate("MainWindow", "Load DWG", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings", None))
        self.actionAhhhhh.setText(_translate("MainWindow", "Ahhhhh", None))

