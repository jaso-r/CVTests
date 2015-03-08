# -*- coding: utf-8 -*-

# This module contains all the image processing algorithms implemented by this applicaiton.

__author__ = 'Jason Rickwald'

import numpy as np
from scipy import ndimage
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
    Performs edge detection using Sobel or Canny.
    """

    def __init__(self):
        self.canny = True
        self.sigma = 1.4

    def cannyTraverse(self, i, j, gnh, gnl):
        x = [-1, 0, 1, -1, 1, -1, 0, 1]
        y = [-1, -1, -1, 0, 0, 1, 1, 1]
        for k in range(8):
            if gnh.item(i+x[k], j+y[k]) == 0 and gnl.item(i+x[k], j+y[k])!= 0:
                gnh.itemset((i+x[k], j+y[k]), 1)
                self.cannyTraverse(i+x[k], j+y[k], gnh, gnl)

    # edge detection as sobel or canny
    def processImages(self, imsq):
        for imidx in range(len(imsq.images)):
            npars = np.dsplit(imsq.images[imidx], 4)
            processImg = np.dstack([npars[0], npars[1], npars[2]])
            meanImg = np.mean(processImg, axis=2)
            if self.canny:
                meanImg = ndimage.gaussian_filter(meanImg, self.sigma)
            dx = ndimage.filters.sobel(meanImg, axis=1, mode='constant')
            dy = ndimage.filters.sobel(meanImg, axis=0, mode='constant')
            sobmag = np.hypot(dx, dy)
            if self.canny:
                sobdir = np.arctan2(dx, dy)
                for x in np.nditer(sobdir, op_flags=['readwrite']):
                    if (x < 22.5 and x >= 0) or (x >= 157.5 and x < 202.5) or (x >= 337.5 and x <= 360):
                        x[...] = 0
                    elif (x >= 22.5 and x < 67.5) or (x >= 202.5 and x < 247.5):
                        x[...] = 45
                    elif (x >= 67.5 and x < 112.5)or (x >= 247.5 and x < 292.5):
                        x[...] = 90
                    else:
                        x[...] = 135
                supmag = sobmag.copy()
                for x in range(1, imsq.height - 1):
                    for y in range(1, imsq.width - 1):
                        if sobdir.item(x,y) == 0:
                            if (sobmag.item(x,y) <= sobmag.item(x,y+1)) or (sobmag.item(x,y) <= sobmag.item(x,y-1)):
                                supmag.itemset((x,y), 0)
                        elif sobdir.item(x,y) == 45:
                            if (sobmag.item(x,y) <= sobmag.item(x-1,y+1)) or (sobmag.item(x,y) <= sobmag.item(x+1,y-1)):
                                supmag.itemset((x,y), 0)
                        elif sobdir.item(x,y) == 90:
                            if (sobmag.item(x,y) <= sobmag.item(x+1,y)) or (sobmag.item(x,y) <= sobmag.item(x-1,y)):
                                supmag.itemset((x,y), 0)
                        else:
                            if (sobmag.item(x,y) <= sobmag.item(x+1,y+1)) or (sobmag.item(x,y) <= sobmag.item(x-1,y-1)):
                                supmag.itemset((x,y), 0)
                m = np.max(supmag)
                th = 0.2 * m
                tl = 0.1 * m
                gnh = np.zeros((imsq.height, imsq.width))
                gnl = np.zeros((imsq.height, imsq.width))
                it = np.nditer([supmag, gnh, gnl], op_flags=[['readonly'],['writeonly'],['writeonly']])
                for x, y, z in it:
                    if x >= th:
                        y[...] = x
                    if x >= tl:
                        z[...] = x
                gnl = gnl-gnh
                for i in range(1, imsq.height-1):
                    for j in range(1, imsq.width-1):
                        if gnh.item(i,j) > 0:
                            gnh.itemset((i,j), 1)
                            self.cannyTraverse(i, j, gnh, gnl)
                gnh *= 255.0
                imsq.images[imidx] = np.dstack([gnh, gnh, gnh, npars[3]])
            else:
                sobmag *= 255.0 / np.max(sobmag)
                imsq.images[imidx] = np.dstack([sobmag, sobmag, sobmag, npars[3]])



class BlobDetectAlgorithm(ImageAlgorithm):
    """
    Blob detection.  Right now, just the difference of gaussians.
    """

    def __init__(self):
        self.canny = True
        self.sigma1 = 1.5
        self.sigma2 = 3.0

    def processImages(self, imsq):
        for imidx in range(len(imsq.images)):
            npars = np.dsplit(imsq.images[imidx], 4)
            processImg = np.dstack([npars[0], npars[1], npars[2]])
            meanImg = np.mean(processImg, axis=2)
            sig1 = self.sigma1
            sig2 = self.sigma2
            if sig1 > sig2:
                sig1 = self.sigma2
                sig2 = self.sigma1
            gaus1Img = ndimage.gaussian_filter(meanImg, sig1)
            gaus2Img = ndimage.gaussian_filter(meanImg, sig2)
            gausDiff = gaus2Img - gaus1Img
            gausDiff *= 255.0 / np.max(gausDiff)
            imsq.images[imidx] = np.dstack([gausDiff, gausDiff, gausDiff, npars[3]])

