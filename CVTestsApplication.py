# -*- coding: utf-8 -*-

# Runs the PyQT window, makes some adjustments to UI and sets up callbacks.
# Each algorithm "module" has it's own class defined to do the work.

__author__ = 'Jason Rickwald'

import sys
from Ui_MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QImage, QPixmap


class CVTestApplication(object):
    """
    Application object with the main method to run.
    """

    def __init__(self):
        self.mainWindow = Ui_MainWindow()
        self.imageManager = None

    def main(self):
        qapp = QApplication(sys.argv)
        qw = QMainWindow()
        self.mainWindow.setupUi(qw)
        self.imageManager = ImageManager(qw, self.mainWindow.graphicsView)
        self.mainWindow.loadImageButton.clicked.connect(self.imageManager.openImage)
        self.mainWindow.zoomInButton.clicked.connect(self.imageManager.zoomIn)
        self.mainWindow.zoomOutButton.clicked.connect(self.imageManager.zoomOut)
        self.mainWindow.revertButton.clicked.connect(self.imageManager.revert)
        qw.show()
        sys.exit(qapp.exec_())


class ImageManager(object):

    def __init__(self, mainWindow, graphicsView):
        self.mainWindow = mainWindow
        self.graphicsView = graphicsView
        self.image = None
        self.revertImage = None
        self.pixmapItem = None

    def openImage(self):
        fileName = QFileDialog.getOpenFileName(self.mainWindow, "Open Image File", QDir.homePath(), "Images (*.png *.gif *.jpg *.jpeg")
        if fileName is not None and fileName is not "":
            self.image = QImage(fileName[0])
            if self.image.isNull():
                QMessageBox.information(self.mainWindow, "CVTest Viewer", "Error loading image:\n" + fileName[0])
                self.image = None
                return
            self.revertImage = QImage(self.image)
            self.pixmapItem = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
            graphicsScene = QGraphicsScene()
            graphicsScene.addItem(self.pixmapItem)
            self.graphicsView.setScene(graphicsScene)
            self.graphicsView.fitInView(self.pixmapItem, Qt.KeepAspectRatio)

    def zoomOut(self):
        self.graphicsView.scale(0.9, 0.9)

    def zoomIn(self):
        self.graphicsView.scale(1.1, 1.1)

    def revert(self):
        self.image = QImage(self.revertImage)
        self.pixmapItem = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        graphicsScene = QGraphicsScene()
        graphicsScene.addItem(self.pixmapItem)
        self.graphicsView.setScene(graphicsScene)
        self.graphicsView.fitInView(self.pixmapItem, Qt.KeepAspectRatio)



if __name__ == '__main__':
    testApp = CVTestApplication()
    testApp.main()
