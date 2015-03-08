# -*- coding: utf-8 -*-

# Runs the PyQT window, makes some adjustments to UI and sets up callbacks.
# Each algorithm "module" has it's own class defined to do the work.

__author__ = 'Jason Rickwald'

import sys
import numpy as np
from Ui_MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QObject, QDir, QEvent
from PyQt5.QtGui import QImage, QPixmap
from CVTestsAlgorithms import EdgeDetectAlgorithm, BlobDetectAlgorithm, ImageSequence


class CVTestApplication(QObject):
    """
    Application object with the main method to run.
    """

    def __init__(self):
        super().__init__()
        self.mainWindow = Ui_MainWindow()
        self.imageManager = None
        self.algorithmManager = None

    def main(self):
        qapp = QApplication(sys.argv)
        qw = QMainWindow()
        self.mainWindow.setupUi(qw)

        # hook things up on the image viewer side
        self.imageManager = ImageManager(qw, self.mainWindow.graphicsView)
        self.mainWindow.loadImageButton.clicked.connect(self.imageManager.openImage)
        self.mainWindow.zoomInButton.clicked.connect(self.imageManager.zoomIn)
        self.mainWindow.zoomOutButton.clicked.connect(self.imageManager.zoomOut)
        self.mainWindow.revertButton.clicked.connect(self.imageManager.revert)
        self.mainWindow.graphicsView.installEventFilter(self)

        # hook up the image processing algorithms
        self.algorithmManager = AlgorithmManager(self.imageManager, self.mainWindow)
        self.mainWindow.edgeDetectApplyButton.clicked.connect(self.algorithmManager.applyEdgeDetect)
        self.mainWindow.blobDetectApplyButton.clicked.connect(self.algorithmManager.applyBlobDetect)

        qw.show()
        sys.exit(qapp.exec_())

    def eventFilter(self, source, event):
        """
        This is used to accept drag-and-drop events from the graphicsView.
        It doesn't seem to be working correctly right now, possibly due to some
        interesting behavior around how QGraphicsView widgets handle drops --
        they try to pass the drop event to the object in the scene that the mouse
        was hovering over.

        TODO: fix this somehow to get drag-and-drop of images working.
        """
        if source is self.mainWindow.graphicsView:
            if event.type() == QEvent.DragEnter:
                event.accept()
            if event.type() == QEvent.Drop:
                # right now we never see this event for some reason
                if len(event.mimeData().urls()) > 0:
                    url = event.mimeData().urls()[0]
                    print(url)
        return False


class AlgorithmManager(object):
    """
    This class handles all the logic of getting the image data from the image manager,
    setting variables the selected algorithm, and running the algorithm on the data.
    The image data is then passed back to the image manager to be displayed.
    """

    def __init__(self, imageManager, mainWindow):
        self.imageManager = imageManager
        self.edgeDetect = EdgeDetectAlgorithm()
        self.blobDetect = BlobDetectAlgorithm()
        self.mainWindow = mainWindow

    def applyEdgeDetect(self):
        imsq = self.imageManager.getImageSequence()
        if imsq is not None:
            self.edgeDetect.canny = self.mainWindow.cannyButton.isChecked()
            self.edgeDetect.sigma = self.mainWindow.sigmaSpinBox.value()
            self.edgeDetect.processImages(imsq)
            self.imageManager.setImage(imsq)

    def applyBlobDetect(self):
        imsq = self.imageManager.getImageSequence()
        if imsq is not None:
            self.blobDetect.sigma1 = self.mainWindow.sigma1SpinBox.value()
            self.blobDetect.sigma2 = self.mainWindow.sigma2SpinBox.value()
            self.blobDetect.processImages(imsq)
            self.imageManager.setImage(imsq)


class ImageManager(object):
    """
    Image viewer logic for the left side of the window.
    Currently the viewer only handles one image, but it should be extended
    in the future to handle an image sequence.
    """

    def __init__(self, mainWindow, graphicsView):
        self.mainWindow = mainWindow
        self.graphicsView = graphicsView
        self.image = None
        self.revertImage = None
        self.pixmapItem = None

    def openImage(self):
        """
        Brings up a file dialog then attempts to load the image file into the viewer.
        """
        fileName = QFileDialog.getOpenFileName(self.mainWindow, "Open Image File", QDir.homePath(), "Images (*.png *.gif *.jpg *.jpeg")
        if fileName is not None and fileName[0] is not None and fileName[0] != "":
            self.image = QImage(fileName[0])
            if self.image is None or self.image.isNull():
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

    def getImageSequence(self):
        """
        Gets and ImageSequence object describing the image dimensions and providing a sequence (currently just 1)
        of images from the viewer.  This data is stored in the ImageSequence object as numpy byte arrays, where
        every four bytes are the r, g, b, and a values for each pixel.
        :return: an ImageSequence containing the image in the viewer, or None if there is no image in the viewer.
        """
        if self.image is None or self.image.isNull():
            return None

        imSq = ImageSequence(self.image.width(), self.image.height())
        ptr = self.image.bits()
        ptr.setsize(self.image.byteCount())
        imSq.images.append(np.asarray(ptr).reshape(self.image.height(), self.image.width(), 4).astype('int32'))
        return imSq

    def setImage(self, imageSequence):
        """
        Sets the current image being displayed by the viewer to whatever data is stored as the first image
        in the ImageSequence object.  This should be modified at some point in the future to handle actual
        sequences of images.
        :param imageSequence: an ImageSequence containing at least one image to display
        """
        if len(imageSequence.images) < 1:
            return

        # right now we only support displaying a single image
        # so pick the first
        imageData = imageSequence.images[0].astype('uint8').flatten().tobytes()
        tmpimage = QImage(imageData, imageSequence.width, imageSequence.height, QImage.Format_ARGB32)
        if tmpimage is None or tmpimage.isNull():
            QMessageBox.information(self.mainWindow, "CVTest Viewer", "Error viewing modified image")
            return
        self.image = tmpimage
        self.pixmapItem = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        graphicsScene = QGraphicsScene()
        graphicsScene.addItem(self.pixmapItem)
        self.graphicsView.setScene(graphicsScene)
        self.graphicsView.fitInView(self.pixmapItem, Qt.KeepAspectRatio)




if __name__ == '__main__':
    testApp = CVTestApplication()
    testApp.main()
