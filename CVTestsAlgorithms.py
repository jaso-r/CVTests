# -*- coding: utf-8 -*-

# This module contains all the image processing algorithms implemented by this applicaiton.

__author__ = 'Jason Rickwald'

from abc import ABCMeta, abstractmethod

class ImageSequence(object):
    """
    A data object that contains a sequence of images to process.
    All images in the sequence should be the same width and height.
    Image data is stored as an array of numpy byte arrays.  Every four bytes are the r, g, b, and a values for
    each pixel in the image.  So the numpy array shape should be (height, width, 4).
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.images = []


class ImageAlgorithm(object):
    """
    The base class for all the image processing algorithms.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def processImages(self, imsq):
        """
        Classes that implement this method should do all their image processing here.
        """
        pass


class EdgeDetectAlgorithm(ImageAlgorithm):
    """
    Performs edge detection.  Still needs to be implemented.
    """

    # for now, as a test, this just does an average of the RGB values
    # and it does it in a pretty slow/dumb way, too
    def processImages(self, imsq):
        for imidx in range(len(imsq.images)):
            for xidx in range(imsq.images[imidx].shape[0]):
                for yidx in range(imsq.images[imidx].shape[1]):
                    xval = imsq.images[imidx][xidx][yidx][0].item()
                    yval = imsq.images[imidx][xidx][yidx][1].item()
                    zval = imsq.images[imidx][xidx][yidx][2].item()
                    avgVal = (xval + yval + zval) / 3
                    imsq.images[imidx][xidx][yidx][0] = avgVal
                    imsq.images[imidx][xidx][yidx][1] = avgVal
                    imsq.images[imidx][xidx][yidx][2] = avgVal



class GaborFilterAlgorithm(ImageAlgorithm):
    """
    Gabor filter of the image.  Still needs to be implemented.
    """

    def processImages(self, imsq):
        pass

