# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Mon Feb 16 15:19:48 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 615)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_4.addWidget(self.graphicsView)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.loadImageButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadImageButton.setObjectName("loadImageButton")
        self.horizontalLayout_4.addWidget(self.loadImageButton)
        self.revertButton = QtWidgets.QPushButton(self.centralwidget)
        self.revertButton.setObjectName("revertButton")
        self.horizontalLayout_4.addWidget(self.revertButton)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.zoomInButton = QtWidgets.QPushButton(self.centralwidget)
        self.zoomInButton.setObjectName("zoomInButton")
        self.horizontalLayout_5.addWidget(self.zoomInButton)
        self.zoomOutButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomOutButton.sizePolicy().hasHeightForWidth())
        self.zoomOutButton.setSizePolicy(sizePolicy)
        self.zoomOutButton.setObjectName("zoomOutButton")
        self.horizontalLayout_5.addWidget(self.zoomOutButton)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.edgeDetect = QtWidgets.QWidget()
        self.edgeDetect.setObjectName("edgeDetect")
        self.tabWidget.addTab(self.edgeDetect, "")
        self.gaborFilter = QtWidgets.QWidget()
        self.gaborFilter.setObjectName("gaborFilter")
        self.tabWidget.addTab(self.gaborFilter, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget, self.loadImageButton)
        MainWindow.setTabOrder(self.loadImageButton, self.revertButton)
        MainWindow.setTabOrder(self.revertButton, self.zoomInButton)
        MainWindow.setTabOrder(self.zoomInButton, self.zoomOutButton)
        MainWindow.setTabOrder(self.zoomOutButton, self.graphicsView)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CVTests"))
        self.loadImageButton.setText(_translate("MainWindow", "Load Image..."))
        self.revertButton.setText(_translate("MainWindow", "Revert"))
        self.zoomInButton.setText(_translate("MainWindow", "+"))
        self.zoomOutButton.setText(_translate("MainWindow", "-"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.edgeDetect), _translate("MainWindow", "Edge Detect"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.gaborFilter), _translate("MainWindow", "Gabor Filter"))

