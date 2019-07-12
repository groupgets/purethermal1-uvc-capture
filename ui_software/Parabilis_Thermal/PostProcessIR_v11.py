#!/usr/bin/env python3
# Author: Karl Parks, 2018
# Python 3 and PyQt5 Implementation

import sys
print(sys.version)

from PyQt5 import QtCore, QtGui, uic
print('Successful import of uic') #often reinstallation of PyQt5 is required

from PyQt5.QtCore import (QCoreApplication, QThread, QThreadPool, pyqtSignal, pyqtSlot, Qt, QTimer, QDateTime)
from PyQt5.QtGui import (QImage, QPixmap, QTextCursor)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QGridLayout, QSizePolicy, QMessageBox, QFileDialog, QSlider, QComboBox, QProgressDialog)
import numpy as np
import cv2
import h5py
from tifffile import imsave
import time
import re
print('Successful import of all libraries')

qtCreatorFile = "ir_post_v2.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import TimedAnimation
import matplotlib.animation as animation
from matplotlib import cm
import matplotlib as mpl
from matplotlib.contour import ContourSet
from matplotlib import image
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

import random
colorMapType = 0

import warnings
warnings.filterwarnings("ignore")

def generate_colour_map():
	global colorMapType

	"""
    Conversion of the colour map from GetThermal to a numpy LUT:
        https://github.com/groupgets/GetThermal/blob/bb467924750a686cc3930f7e3a253818b755a2c0/src/dataformatter.cpp#L6
    """
	lut = np.zeros((256, 1, 3), dtype=np.uint8)

	#colorMaps
	colormap_grayscale = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 24, 25, 25, 25, 26, 26, 26, 27, 27, 27, 28, 28, 28, 29, 29, 29, 30, 30, 30, 31, 31, 31, 32, 32, 32, 33, 33, 33, 34, 34, 34, 35, 35, 35, 36, 36, 36, 37, 37, 37, 38, 38, 38, 39, 39, 39, 40, 40, 40, 41, 41, 41, 42, 42, 42, 43, 43, 43, 44, 44, 44, 45, 45, 45, 46, 46, 46, 47, 47, 47, 48, 48, 48, 49, 49, 49, 50, 50, 50, 51, 51, 51, 52, 52, 52, 53, 53, 53, 54, 54, 54, 55, 55, 55, 56, 56, 56, 57, 57, 57, 58, 58, 58, 59, 59, 59, 60, 60, 60, 61, 61, 61, 62, 62, 62, 63, 63, 63, 64, 64, 64, 65, 65, 65, 66, 66, 66, 67, 67, 67, 68, 68, 68, 69, 69, 69, 70, 70, 70, 71, 71, 71, 72, 72, 72, 73, 73, 73, 74, 74, 74, 75, 75, 75, 76, 76, 76, 77, 77, 77, 78, 78, 78, 79, 79, 79, 80, 80, 80, 81, 81, 81, 82, 82, 82, 83, 83, 83, 84, 84, 84, 85, 85, 85, 86, 86, 86, 87, 87, 87, 88, 88, 88, 89, 89, 89, 90, 90, 90, 91, 91, 91, 92, 92, 92, 93, 93, 93, 94, 94, 94, 95, 95, 95, 96, 96, 96, 97, 97, 97, 98, 98, 98, 99, 99, 99, 100, 100, 100, 101, 101, 101, 102, 102, 102, 103, 103, 103, 104, 104, 104, 105, 105, 105, 106, 106, 106, 107, 107, 107, 108, 108, 108, 109, 109, 109, 110, 110, 110, 111, 111, 111, 112, 112, 112, 113, 113, 113, 114, 114, 114, 115, 115, 115, 116, 116, 116, 117, 117, 117, 118, 118, 118, 119, 119, 119, 120, 120, 120, 121, 121, 121, 122, 122, 122, 123, 123, 123, 124, 124, 124, 125, 125, 125, 126, 126, 126, 127, 127, 127, 128, 128, 128, 129, 129, 129, 130, 130, 130, 131, 131, 131, 132, 132, 132, 133, 133, 133, 134, 134, 134, 135, 135, 135, 136, 136, 136, 137, 137, 137, 138, 138, 138, 139, 139, 139, 140, 140, 140, 141, 141, 141, 142, 142, 142, 143, 143, 143, 144, 144, 144, 145, 145, 145, 146, 146, 146, 147, 147, 147, 148, 148, 148, 149, 149, 149, 150, 150, 150, 151, 151, 151, 152, 152, 152, 153, 153, 153, 154, 154, 154, 155, 155, 155, 156, 156, 156, 157, 157, 157, 158, 158, 158, 159, 159, 159, 160, 160, 160, 161, 161, 161, 162, 162, 162, 163, 163, 163, 164, 164, 164, 165, 165, 165, 166, 166, 166, 167, 167, 167, 168, 168, 168, 169, 169, 169, 170, 170, 170, 171, 171, 171, 172, 172, 172, 173, 173, 173, 174, 174, 174, 175, 175, 175, 176, 176, 176, 177, 177, 177, 178, 178, 178, 179, 179, 179, 180, 180, 180, 181, 181, 181, 182, 182, 182, 183, 183, 183, 184, 184, 184, 185, 185, 185, 186, 186, 186, 187, 187, 187, 188, 188, 188, 189, 189, 189, 190, 190, 190, 191, 191, 191, 192, 192, 192, 193, 193, 193, 194, 194, 194, 195, 195, 195, 196, 196, 196, 197, 197, 197, 198, 198, 198, 199, 199, 199, 200, 200, 200, 201, 201, 201, 202, 202, 202, 203, 203, 203, 204, 204, 204, 205, 205, 205, 206, 206, 206, 207, 207, 207, 208, 208, 208, 209, 209, 209, 210, 210, 210, 211, 211, 211, 212, 212, 212, 213, 213, 213, 214, 214, 214, 215, 215, 215, 216, 216, 216, 217, 217, 217, 218, 218, 218, 219, 219, 219, 220, 220, 220, 221, 221, 221, 222, 222, 222, 223, 223, 223, 224, 224, 224, 225, 225, 225, 226, 226, 226, 227, 227, 227, 228, 228, 228, 229, 229, 229, 230, 230, 230, 231, 231, 231, 232, 232, 232, 233, 233, 233, 234, 234, 234, 235, 235, 235, 236, 236, 236, 237, 237, 237, 238, 238, 238, 239, 239, 239, 240, 240, 240, 241, 241, 241, 242, 242, 242, 243, 243, 243, 244, 244, 244, 245, 245, 245, 246, 246, 246, 247, 247, 247, 248, 248, 248, 249, 249, 249, 250, 250, 250, 251, 251, 251, 252, 252, 252, 253, 253, 253, 254, 254, 254, 255, 255, 255];

	colormap_rainbow = [1, 3, 74, 0, 3, 74, 0, 3, 75, 0, 3, 75, 0, 3, 76, 0, 3, 76, 0, 3, 77, 0, 3, 79, 0, 3, 82, 0, 5, 85, 0, 7, 88, 0, 10, 91, 0, 14, 94, 0, 19, 98, 0, 22, 100, 0, 25, 103, 0, 28, 106, 0, 32, 109, 0, 35, 112, 0, 38, 116, 0, 40, 119, 0, 42, 123, 0, 45, 128, 0, 49, 133, 0, 50, 134, 0, 51, 136, 0, 52, 137, 0, 53, 139, 0, 54, 142, 0, 55, 144, 0, 56, 145, 0, 58, 149, 0, 61, 154, 0, 63, 156, 0, 65, 159, 0, 66, 161, 0, 68, 164, 0, 69, 167, 0, 71, 170, 0, 73, 174, 0, 75, 179, 0, 76, 181, 0, 78, 184, 0, 79, 187, 0, 80, 188, 0, 81, 190, 0, 84, 194, 0, 87, 198, 0, 88, 200, 0, 90, 203, 0, 92, 205, 0, 94, 207, 0, 94, 208, 0, 95, 209, 0, 96, 210, 0, 97, 211, 0, 99, 214, 0, 102, 217, 0, 103, 218, 0, 104, 219, 0, 105, 220, 0, 107, 221, 0, 109, 223, 0, 111, 223, 0, 113, 223, 0, 115, 222, 0, 117, 221, 0, 118, 220, 1, 120, 219, 1, 122, 217, 2, 124, 216, 2, 126, 214, 3, 129, 212, 3, 131, 207, 4, 132, 205, 4, 133, 202, 4, 134, 197, 5, 136, 192, 6, 138, 185, 7, 141, 178, 8, 142, 172, 10, 144, 166, 10, 144, 162, 11, 145, 158, 12, 146, 153, 13, 147, 149, 15, 149, 140, 17, 151, 132, 22, 153, 120, 25, 154, 115, 28, 156, 109, 34, 158, 101, 40, 160, 94, 45, 162, 86, 51, 164, 79, 59, 167, 69, 67, 171, 60, 72, 173, 54, 78, 175, 48, 83, 177, 43, 89, 179, 39, 93, 181, 35, 98, 183, 31, 105, 185, 26, 109, 187, 23, 113, 188, 21, 118, 189, 19, 123, 191, 17, 128, 193, 14, 134, 195, 12, 138, 196, 10, 142, 197, 8, 146, 198, 6, 151, 200, 5, 155, 201, 4, 160, 203, 3, 164, 204, 2, 169, 205, 2, 173, 206, 1, 175, 207, 1, 178, 207, 1, 184, 208, 0, 190, 210, 0, 193, 211, 0, 196, 212, 0, 199, 212, 0, 202, 213, 1, 207, 214, 2, 212, 215, 3, 215, 214, 3, 218, 214, 3, 220, 213, 3, 222, 213, 4, 224, 212, 4, 225, 212, 5, 226, 212, 5, 229, 211, 5, 232, 211, 6, 232, 211, 6, 233, 211, 6, 234, 210, 6, 235, 210, 7, 236, 209, 7, 237, 208, 8, 239, 206, 8, 241, 204, 9, 242, 203, 9, 244, 202, 10, 244, 201, 10, 245, 200, 10, 245, 199, 11, 246, 198, 11, 247, 197, 12, 248, 194, 13, 249, 191, 14, 250, 189, 14, 251, 187, 15, 251, 185, 16, 252, 183, 17, 252, 178, 18, 253, 174, 19, 253, 171, 19, 254, 168, 20, 254, 165, 21, 254, 164, 21, 255, 163, 22, 255, 161, 22, 255, 159, 23, 255, 157, 23, 255, 155, 24, 255, 149, 25, 255, 143, 27, 255, 139, 28, 255, 135, 30, 255, 131, 31, 255, 127, 32, 255, 118, 34, 255, 110, 36, 255, 104, 37, 255, 101, 38, 255, 99, 39, 255, 93, 40, 255, 88, 42, 254, 82, 43, 254, 77, 45, 254, 69, 47, 254, 62, 49, 253, 57, 50, 253, 53, 52, 252, 49, 53, 252, 45, 55, 251, 39, 57, 251, 33, 59, 251, 32, 60, 251, 31, 60, 251, 30, 61, 251, 29, 61, 251, 28, 62, 250, 27, 63, 250, 27, 65, 249, 26, 66, 249, 26, 68, 248, 25, 70, 248, 24, 73, 247, 24, 75, 247, 25, 77, 247, 25, 79, 247, 26, 81, 247, 32, 83, 247, 35, 85, 247, 38, 86, 247, 42, 88, 247, 46, 90, 247, 50, 92, 248, 55, 94, 248, 59, 96, 248, 64, 98, 248, 72, 101, 249, 81, 104, 249, 87, 106, 250, 93, 108, 250, 95, 109, 250, 98, 110, 250, 100, 111, 251, 101, 112, 251, 102, 113, 251, 109, 117, 252, 116, 121, 252, 121, 123, 253, 126, 126, 253, 130, 128, 254, 135, 131, 254, 139, 133, 254, 144, 136, 254, 151, 140, 255, 158, 144, 255, 163, 146, 255, 168, 149, 255, 173, 152, 255, 176, 153, 255, 178, 155, 255, 184, 160, 255, 191, 165, 255, 195, 168, 255, 199, 172, 255, 203, 175, 255, 207, 179, 255, 211, 182, 255, 216, 185, 255, 218, 190, 255, 220, 196, 255, 222, 200, 255, 225, 202, 255, 227, 204, 255, 230, 206, 255, 233, 208]

	colourmap_ironblack = [
        255, 255, 255, 253, 253, 253, 251, 251, 251, 249, 249, 249, 247, 247,
        247, 245, 245, 245, 243, 243, 243, 241, 241, 241, 239, 239, 239, 237,
        237, 237, 235, 235, 235, 233, 233, 233, 231, 231, 231, 229, 229, 229,
        227, 227, 227, 225, 225, 225, 223, 223, 223, 221, 221, 221, 219, 219,
        219, 217, 217, 217, 215, 215, 215, 213, 213, 213, 211, 211, 211, 209,
        209, 209, 207, 207, 207, 205, 205, 205, 203, 203, 203, 201, 201, 201,
        199, 199, 199, 197, 197, 197, 195, 195, 195, 193, 193, 193, 191, 191,
        191, 189, 189, 189, 187, 187, 187, 185, 185, 185, 183, 183, 183, 181,
        181, 181, 179, 179, 179, 177, 177, 177, 175, 175, 175, 173, 173, 173,
        171, 171, 171, 169, 169, 169, 167, 167, 167, 165, 165, 165, 163, 163,
        163, 161, 161, 161, 159, 159, 159, 157, 157, 157, 155, 155, 155, 153,
        153, 153, 151, 151, 151, 149, 149, 149, 147, 147, 147, 145, 145, 145,
        143, 143, 143, 141, 141, 141, 139, 139, 139, 137, 137, 137, 135, 135,
        135, 133, 133, 133, 131, 131, 131, 129, 129, 129, 126, 126, 126, 124,
        124, 124, 122, 122, 122, 120, 120, 120, 118, 118, 118, 116, 116, 116,
        114, 114, 114, 112, 112, 112, 110, 110, 110, 108, 108, 108, 106, 106,
        106, 104, 104, 104, 102, 102, 102, 100, 100, 100, 98, 98, 98, 96, 96,
        96, 94, 94, 94, 92, 92, 92, 90, 90, 90, 88, 88, 88, 86, 86, 86, 84, 84,
        84, 82, 82, 82, 80, 80, 80, 78, 78, 78, 76, 76, 76, 74, 74, 74, 72, 72,
        72, 70, 70, 70, 68, 68, 68, 66, 66, 66, 64, 64, 64, 62, 62, 62, 60, 60,
        60, 58, 58, 58, 56, 56, 56, 54, 54, 54, 52, 52, 52, 50, 50, 50, 48, 48,
        48, 46, 46, 46, 44, 44, 44, 42, 42, 42, 40, 40, 40, 38, 38, 38, 36, 36,
        36, 34, 34, 34, 32, 32, 32, 30, 30, 30, 28, 28, 28, 26, 26, 26, 24, 24,
        24, 22, 22, 22, 20, 20, 20, 18, 18, 18, 16, 16, 16, 14, 14, 14, 12, 12,
        12, 10, 10, 10, 8, 8, 8, 6, 6, 6, 4, 4, 4, 2, 2, 2, 0, 0, 0, 0, 0, 9,
        2, 0, 16, 4, 0, 24, 6, 0, 31, 8, 0, 38, 10, 0, 45, 12, 0, 53, 14, 0,
        60, 17, 0, 67, 19, 0, 74, 21, 0, 82, 23, 0, 89, 25, 0, 96, 27, 0, 103,
        29, 0, 111, 31, 0, 118, 36, 0, 120, 41, 0, 121, 46, 0, 122, 51, 0, 123,
        56, 0, 124, 61, 0, 125, 66, 0, 126, 71, 0, 127, 76, 1, 128, 81, 1, 129,
        86, 1, 130, 91, 1, 131, 96, 1, 132, 101, 1, 133, 106, 1, 134, 111, 1,
        135, 116, 1, 136, 121, 1, 136, 125, 2, 137, 130, 2, 137, 135, 3, 137,
        139, 3, 138, 144, 3, 138, 149, 4, 138, 153, 4, 139, 158, 5, 139, 163,
        5, 139, 167, 5, 140, 172, 6, 140, 177, 6, 140, 181, 7, 141, 186, 7,
        141, 189, 10, 137, 191, 13, 132, 194, 16, 127, 196, 19, 121, 198, 22,
        116, 200, 25, 111, 203, 28, 106, 205, 31, 101, 207, 34, 95, 209, 37,
        90, 212, 40, 85, 214, 43, 80, 216, 46, 75, 218, 49, 69, 221, 52, 64,
        223, 55, 59, 224, 57, 49, 225, 60, 47, 226, 64, 44, 227, 67, 42, 228,
        71, 39, 229, 74, 37, 230, 78, 34, 231, 81, 32, 231, 85, 29, 232, 88,
        27, 233, 92, 24, 234, 95, 22, 235, 99, 19, 236, 102, 17, 237, 106, 14,
        238, 109, 12, 239, 112, 12, 240, 116, 12, 240, 119, 12, 241, 123, 12,
        241, 127, 12, 242, 130, 12, 242, 134, 12, 243, 138, 12, 243, 141, 13,
        244, 145, 13, 244, 149, 13, 245, 152, 13, 245, 156, 13, 246, 160, 13,
        246, 163, 13, 247, 167, 13, 247, 171, 13, 248, 175, 14, 248, 178, 15,
        249, 182, 16, 249, 185, 18, 250, 189, 19, 250, 192, 20, 251, 196, 21,
        251, 199, 22, 252, 203, 23, 252, 206, 24, 253, 210, 25, 253, 213, 27,
        254, 217, 28, 254, 220, 29, 255, 224, 30, 255, 227, 39, 255, 229, 53,
        255, 231, 67, 255, 233, 81, 255, 234, 95, 255, 236, 109, 255, 238, 123,
        255, 240, 137, 255, 242, 151, 255, 244, 165, 255, 246, 179, 255, 248,
        193, 255, 249, 207, 255, 251, 221, 255, 253, 235, 255, 255, 24]

	def chunk(
            ulist, step): return map(
        lambda i: ulist[i: i + step],
        range(0, len(ulist), step)) #python 3 requires range not xrange

	if (colorMapType == 1):
		chunks = chunk(colormap_rainbow, 3)
	elif (colorMapType == 2):
		chunks = chunk(colormap_grayscale, 3)
	else:
		chunks = chunk(colourmap_ironblack, 3)

	red = []
	green = []
	blue = []

	for chunk in chunks:
		red.append(chunk[0])
		green.append(chunk[1])
		blue.append(chunk[2])

	lut[:, 0, 0] = blue

	lut[:, 0, 1] = green

	lut[:, 0, 2] = red

	return lut

toggleUnitState = 'F'



def ktof(val):
    return round(((1.8 * ktoc(val) + 32.0)), 2)

def ktoc(val):
    return round(((val - 27315) / 100.0), 2)

def readTemp(unit, state):
    if state == 'max':
        if unit == 'F':
            return (str(ktof(maxVal)) + ' ' + unit)
        elif unit == 'C':
            return (str(ktoc(maxVal)) + ' ' + unit)
        else:
            display('What are you asking for?')
    elif state == 'min':
        if unit == 'F':
            return (str(ktof(minVal)) + ' ' + unit)
        elif unit == 'C':
            return (str(ktoc(minVal)) + ' ' + unit)
        else:
            display('What are you asking for?')
    elif state == 'none':
        if unit == 'F':
            return (str(ktof(cursorVal)) + ' ' + unit)
        elif unit == 'C':
            return (str(ktoc(cursorVal)) + ' ' + unit)
        else:
            display('What are you asking for?')
    else:
        display('What are you asking for?')

def readTempInt(unit, state):
    if state == 'max':
        if unit == 'F':
            return ktof(maxVal)
        elif unit == 'C':
            return ktoc(maxVal)
        else:
            display('What are you asking for?')
    elif state == 'min':
        if unit == 'F':
            return ktof(minVal)
        elif unit == 'C':
            return ktoc(minVal)
        else:
            display('What are you asking for?')
    elif state == 'none':
        if unit == 'F':
            return ktof(cursorVal)
        elif unit == 'C':
            return ktoc(cursorVal)
        else:
            display('What are you asking for?')
    else:
        display('What are you asking for?')

def raw_to_8bit(data):
    cv2.normalize(data, data, 0, 65535, cv2.NORM_MINMAX)
    np.right_shift(data, 8, data)
    return cv2.cvtColor(np.uint8(data), cv2.COLOR_GRAY2RGB)

frame = 1
videoState = 'notPlay'
framerate = 1 #(1/9 frames per second), do not adjust
timerHz = 115 #ms 1/8.7 = 0.1149 sec, decrease to increase speed
fileSelected = ""
usedOnce = 1

class Window(QMainWindow, Ui_MainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.initUI()

	def initUI(self):
		print('Starting user interface...')
		self.w = QWidget()

		# a figure instance to plot on
		self.figure = Figure()

		# this is the Canvas Widget that displays the `figure`
		# it takes the `figure` instance as a parameter to __init__
		self.canvas = FigureCanvas(self.figure)

		# this is the Navigation widget
		# it takes the Canvas widget and a parent
		self.toolbar = NavigationToolbar(self.canvas, self)

		# set the layout for the main window
		self.dispLayout.addWidget(self.toolbar)
		self.dispLayout.addWidget(self.canvas)

		#buttons
		self.nextFrame.clicked.connect(self.dispNextImg)
		self.prevFrame.clicked.connect(self.dispPrevImg)
		self.selectFileBut.clicked.connect(self.getFile)
		self.playVidBut.clicked.connect(self.play)
		self.makeTiffBut.clicked.connect(self.makeTiff2)
		self.displayC.clicked.connect(self.dispCDef)
		self.displayC.clicked.connect(self.displayTempValues)
		self.displayF.clicked.connect(self.dispFDef)
		self.displayF.clicked.connect(self.displayTempValues)
		self.sl.valueChanged.connect(self.slValueChange)
		self.saveCvImageBut.clicked.connect(self.saveCvImage)
		#cid = self.canvas.mpl_connect('button_press_event', self.on_press)
		self.saveAsVideoSS.clicked.connect(self.saveVideoSS)
		self.pauseVidBut.clicked.connect(self.pauseVideo)
		#self.startEdit.returnPressed(frame = str(self.startEdit.text()))
		#self.startEdit.returnPressed(frame = str(self.startEdit.text()))
		self.cmIronBut.clicked.connect(self.cmIronFunc)
		self.cmGrayBut.clicked.connect(self.cmGrayFunc)
		self.cmRainBut.clicked.connect(self.cmRainFunc)
		self.tempScaleBut.clicked.connect(self.colorBarDisplay)

		#self.history.verticalScrollBar().setValue(self.history.verticalScrollBar().maximum())

		self.timer = QTimer(self)
		self.timer.setInterval(timerHz)
		self.timer.timeout.connect(self.playVid5)
		self.timer.start()

		if (len(sys.argv) > 1):
			self.getFile()

	def cmIronFunc(self):
		global colorMapType
		colorMapType = 0
		self.dispNextImg()
		self.dispPrevImg()
		self.history.insertPlainText('Changed Color Map\n')
		self.history.moveCursor(QTextCursor.End)

	def cmRainFunc(self):
		global colorMapType
		colorMapType = 1
		self.dispNextImg()
		self.dispPrevImg()
		self.history.insertPlainText('Changed Color Map\n')
		self.history.moveCursor(QTextCursor.End)

	def cmGrayFunc(self):
		global colorMapType
		colorMapType = 2
		self.dispNextImg()
		self.dispPrevImg()
		self.history.insertPlainText('Changed Color Map\n')
		self.history.moveCursor(QTextCursor.End)

	def dispCDef(self):
		global toggleUnitState
		toggleUnitState = 'C'
		self.history.insertPlainText('Display ' + str(toggleUnitState) + '\n')
		self.history.moveCursor(QTextCursor.End)

	def dispFDef(self):
		global toggleUnitState
		toggleUnitState = 'F'
		self.history.insertPlainText('Display ' + str(toggleUnitState) + '\n')
		self.history.moveCursor(QTextCursor.End)

	# def startTimer(self):
	# 	global hz
	# 	self.timer.stop()
	# 	print(hz)
	# 	self.timer.setInterval(timerHz)
	# 	self.timer.timeout.connect(self.playVid5)
	# 	self.timer.start()
	# 	print('Re-Started Timer')
	#
	# def stopTimer(self):
	# 	self.timer.stop()

	# def speed(self):
	# 	global framerate
	# 	hzIndex = self.comboBoxHz.currentIndex()
	# 	if hzIndex == 0:
	# 		framerate = 0.5
	# 		print('Half Framerate')
	# 	elif hzIndex == 1:
	# 		framerate = 1
	# 		print('Normal Framerate')
	# 	elif hzIndex == 2:
	# 		framerate = 2
	# 		print('Double Framerate')
	# 	else:
	# 		hz = 111
	# 	self.startTimer()

	def slValueChange(self):
		global frame
		#global fileSelected
		#if fileSelected != "":
		#print('SlValueChange Def Called')
		frame = self.sl.value()
		self.dispImg()
		self.canvas.draw()

	def setSlider(self):
		global lastFrame
		#print('Set Slider Function Called')
		#print('Enable Slider')
		self.sl.setEnabled(True)
		#print('Set Minimum')
		self.sl.setMinimum(1)
		#print(lastFrame)
		#print('Set Maximum')
		self.sl.setMaximum(lastFrame)
		self.sl.setValue(1)
		self.sl.setTickPosition(QSlider.TicksBelow)
		self.sl.setTickInterval(9)
		self.slStartF.setText('First Frame: 1')
		self.slMidF.setText('Mid Frame: ' + str(round(lastFrame/2)))
		self.slEndF.setText('Last Frame: ' + str(lastFrame))
		self.slStartT.setText('0 Seconds')
		self.slMidT.setText(str(round(lastFrame/(2*9),1)) + ' Seconds')
		self.slEndT.setText(str(round(lastFrame/9,1)) + ' Seconds')

	def saveVideoSS(self):
		global frame
		global editLastFrame
		global videoState
		global fileSelected
		videoState = 'pause'
		if fileSelected != "":
			frame = int(self.startEdit.text())
			editLastFrame = int(self.stopEdit.text())
			fileNameVid = ""
			dlgVid = QFileDialog()
			dlgVid.setDefaultSuffix('.avi')
			fileNameVid, filter = dlgVid.getSaveFileName(self.w, 'Navigate to Directory and Choose a File Name to Save To', fileSelected + '_f' + str(frame) + '-' + str(editLastFrame) + '_VIDEO.avi', 'AVI Video (*.avi)')
			fileNameVid = str(fileNameVid)
			fourcc = cv2.VideoWriter_fourcc(*'MJPG')
			if fileNameVid != "":
				try:
					out = cv2.VideoWriter(fileNameVid, fourcc, 8.7, (640,480), True)
					print('past out')

					initialFrame = frame
					rangeVid = editLastFrame - initialFrame
					pd = QProgressDialog("Operation in progress.", "Cancel", 0, 100, self);
					pd.setWindowTitle("Creating AVI Video...")
					pd.setWindowModality(Qt.WindowModal)
					pd.resize(400,100)
					pd.show()
					pd.setValue(0)
					time.sleep(0.25)

					for i in range(frame, editLastFrame):
						print('frame' + str(i))

						percentageComplete = ((i - initialFrame)/rangeVid)*100
						pd.setValue(percentageComplete)
						if pd.wasCanceled():
							break;

						frameForVid = self.grabDataFrame()
						out.write(frameForVid)
						if frame <= editLastFrame:
							frame += framerate
						else:
							print('You are at Last Frame')
					out.release()
					print('out release')
					print('Saved Video As ' + str(fileNameVid))
					self.history.insertPlainText('SUCCESS: Saved Video\n')
					self.history.moveCursor(QTextCursor.End)

					pd.setValue(100)
					time.sleep(1)
					pd.close()

				except:
					self.history.insertPlainText('No AVI Video Generated\n Did Not Specify Proper FileName\n')
					self.history.moveCursor(QTextCursor.End)
					print('Did Not Specify Proper FileName')
					print('No AVI Video Generated')
			else:
				self.history.insertPlainText('No AVI Video Generated\n Did Not Specify Proper FileName\n')
				self.history.moveCursor(QTextCursor.End)
				print('Did Not Specify Proper FileName')
				print('No AVI Video Generated')

	def saveCvImage(self):
		global fileSelected
		global videoState
		videoState = 'pause'
		if fileSelected != "":
			dlg = QFileDialog()
			#dlg.setNameFilter('PNG files (*.png)')
			dlg.setDefaultSuffix('.png')
			fileNameImage, filter = dlg.getSaveFileName(self.w, 'Navigate to Directory and Choose a File Name to Save To', fileSelected + '_f' + str(frame) + '_PNG.png', 'PNG Image (*.png)')
			if fileNameImage != "":
				try:
					print(fileNameImage)
					cv2.imwrite(str(fileNameImage),self.grabDataFrame())
					print('Saved frame ' + str(frame) + ' as .png')
					self.history.insertPlainText('SUCCESS: Saved Frame: ' + str(frame) + ' as PNG\n')
					self.history.moveCursor(QTextCursor.End)
				except:
					self.history.insertPlainText('No PNG Image Generated\n Did Not Specify Proper FileName\n')
					self.history.moveCursor(QTextCursor.End)
					print('Did Not Specify Proper FileName')
					print('No PNG Image Generated')
			else:
				self.history.insertPlainText('No PNG Image Generated\n Did Not Specify Proper FileName\n')
				self.history.moveCursor(QTextCursor.End)
				print('Did Not Specify Proper FileName')
				print('No PNG Image Generated')


	def makeTiff2(self):
		global lastFrame
		global fileSelected
		global videoState
		videoState = 'pause'
		if fileSelected != "":
			dlgTiff = QFileDialog()
			#dlg.setNameFilter('PNG files (*.png)')
			dlgTiff.setDefaultSuffix('.tiff')
			fileNameTiff, filter = dlgTiff.getSaveFileName(self.w, 'Navigate to Directory and Choose a File Name to Save To', fileSelected + '_TIFF.tiff', 'TIFF File (*.tiff)')
			print(fileNameTiff)
			if fileNameTiff != "":
				self.history.insertPlainText('File Name Selected\n')
				self.history.moveCursor(QTextCursor.End)
				print('Collecting Data Frames...')

				initialFrame = 1
				rangeVid = lastFrame - initialFrame
				pd = QProgressDialog("Operation in progress.", "Cancel", 0, 100, self);
				pd.setWindowTitle("Creating TIFF File...")
				pd.setWindowModality(Qt.WindowModal)
				pd.resize(400,100)
				pd.show()
				pd.setValue(0)
				time.sleep(0.25)

				for i in range(1,lastFrame):
					print('Frame to Tiff: ' + str(i))

					percentageComplete = ((i - initialFrame)/rangeVid)*100
					pd.setValue(percentageComplete)
					if pd.wasCanceled():
						break;

					data = self.f_read[('image'+str(i))][:]
					if i == 1:
						dataCollection = data
					else:
						dataCollection = np.dstack((dataCollection,data))
					i += 1
					if i == lastFrame/2:
						print('Half Way Through File...')
				print('Completed Collecting All Data Frames')
				try:
					imsave((str(fileNameTiff)), dataCollection)
					print('Saved Tiff As ' + str(fileNameTiff))
					self.history.insertPlainText(' Saved Tiff\n')
					self.history.moveCursor(QTextCursor.End)
				except:
					self.history.insertPlainText('No Tiff File Generated\n Did Not Specify Proper FileName\n')
					self.history.moveCursor(QTextCursor.End)
					print('Did Not Specify Proper FileName')
					print('No Tiff File Generated')
				pd.setValue(100)
				time.sleep(1)
				pd.close()
			else:
				self.history.insertPlainText('No Tiff File Generated\n Did Not Specify Proper FileName\n')
				self.history.moveCursor(QTextCursor.End)
				print('Did Not Specify Proper FileName')
				print('No Tiff File Generated')

	def grabTempValue(self):
		global frame
		global lastFrame
		global fileSelected
		global xMouse
		global yMouse
		data = self.f_read[('image'+str(frame))][:]
		data = cv2.resize(data[:,:], (640, 480))
		return data[yMouse, xMouse]

	def on_press(self, event):
		global xMouse
		global yMouse
		global cursorVal
		#print('you pressed', event.button, event.xdata, event.ydata)
		xMouse = event.xdata
		yMouse = event.ydata
		cursorVal = self.grabTempValue()
		self.cursorTempLabel.setText('Cursor Temp: ' + readTemp(toggleUnitState, 'none'))

	def hover(self, event):
		global xMouse
		global yMouse
		global cursorVal
		#print('you pressed', event.button, event.xdata, event.ydata)
		if event.xdata != None:
			xMouse = int(round(event.xdata))
			yMouse = int(round(event.ydata))
			cursorVal = int(round(self.grabTempValue()))
			#if xMouse > 1 and xMouse < 640 and yMouse > 0 and yMouse < 480:
			self.cursorTempLabel.setText('Cursor Temp: ' + readTemp(toggleUnitState, 'none'))
			#else:
				#self.cursorTempLabel.setText('Cursor Temp: MOVE CURSOR OVER IMAGE')
		else:
			#print('MOVE CURSOR OVER IMAGE')
			self.cursorTempLabel.setText('Cursor Temp: MOVE CURSOR OVER IMAGE')

	def displayTempValues(self):
		global fileSelected
		global toggleUnitState
		if fileSelected != "":
			self.maxTempLabel.setText('Current Max Temp: ' + readTemp(toggleUnitState, 'max'))
			self.maxTempLocLabel.setText('Max Temp Loc: ' + str(maxLoc))
			self.minTempLabel.setText('Current Min Temp: ' + readTemp(toggleUnitState, 'min'))
			self.minTempLocLabel.setText('Min Temp Loc: ' + str(minLoc))

	def grabDataFrame(self):
		global frame
		global lastFrame
		global fileSelected
		#print('Display Image at Frame: ' + str(frame))
		data = self.f_read[('image'+str(frame))][:]
		data = cv2.resize(data[:,:], (640, 480))
		img = cv2.LUT(raw_to_8bit(data), generate_colour_map())
		img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		rgbImage = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
		return(rgbImage)

	def play(self):
		global frame
		global editLastFrame
		global fileSelected
		global videoState
		self.history.insertPlainText('Play Video\n')
		self.history.moveCursor(QTextCursor.End)
		#print(self.startEdit.text())
		if self.startEdit.isModified():
			frame = int(self.startEdit.text())
			print('Starting at Frame: ' + self.startEdit.text())
		if self.stopEdit.isModified():
			editLastFrame = int(self.stopEdit.text())
		if fileSelected != "":
			self.timer.start()
			videoState = 'play'

	def pauseVideo(self):
		global videoState
		self.history.insertPlainText('Paused Video\n')
		self.history.moveCursor(QTextCursor.End)
		videoState = 'pause'

	def playVid5(self):
		global videoState
		global frame
		global lastFrame
		global editLastFrame
		if videoState == 'play':
			if editLastFrame <= lastFrame:
				if frame <= editLastFrame:
					self.sl.setValue(frame)
					if frame != lastFrame:
						frame += 1
					#print('playing video')
				else:
					print('You are at Stop Frame')
					videoState = 'pause'
			else:
				print('You are at Last Frame')
				videoState = 'pause'

	def dispNextImg(self):
		global frame
		global lastFrame
		global framerate
		global fileSelected
		global videoState
		videoState = 'pause'
		self.history.insertPlainText('Next Frame: ' + str(frame) + '\n')
		self.history.moveCursor(QTextCursor.End)
		if fileSelected != "":
			if lastFrame > frame:
				frame += framerate
			else:
				print('You are at Last Frame')
			#self.dispImg()
			#self.canvas.draw()
			self.sl.setValue(frame)

	def dispPrevImg(self):
		global frame
		global fileSelected
		global videoState
		self.history.insertPlainText('Previous Frame: ' + str(frame) + '\n')
		self.history.moveCursor(QTextCursor.End)
		videoState = 'pause'
		if fileSelected != "":
			if frame > 1:
				frame -= 1
			else:
				print('You are at First Frame')
			#self.dispImg()
			#self.canvas.draw()
			self.sl.setValue(frame)

	def dispImg(self):
		global frame
		global lastFrame
		global fileSelected
		global maxVal
		global minVal
		global maxLoc
		global minLoc
		#if frame > 1:
			#self.cb.remove()
		#print('Display Image at Frame: ' + str(frame))
		self.currentFrameDisp.setText('Current Frame: ' + str(frame))
		data = self.f_read[('image'+str(frame))][:]
		data = cv2.resize(data[:,:], (640, 480))
		minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(data)
		img = cv2.LUT(raw_to_8bit(data), generate_colour_map())
		rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		#rgbImage = img #blue is hot
		self.ax = self.figure.add_subplot(111)
		self.ax.clear()
		#cmap = mpl.cm.cool
		#norm = mpl.colors.Normalize(vmin=5, vmax=10)
		#print('Ran dispImg')
		#print(frame)
		if frame == 1:
			self.figure.tight_layout()
		#colorVals = cm.get_clim(rgbImage)
		#print(colorVals)
		#cax = self.figure.add_axes([0.2, 0.08, 0.6, 0.04])
		#self.figure.colorbar(rgbImage, cax, orientation='horizontal')
		self.cax = self.ax.imshow(rgbImage)
		#self.cb = self.figure.colorbar(self.cax)
		lastFrame = len(self.f_read)
		self.sl.setValue(frame)
		self.displayTempValues()
		self.currentTimeLabel.setText('Current Time: ' + str(round(((frame-1)/9.00),2)))
		cid = self.canvas.mpl_connect('motion_notify_event', self.hover)

	def colorBarDisplay(self):
		global toggleUnitState
		global frame
		rgbImage = self.grabDataFrame()
		rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
		#cm.get_clim(rgbImage)
		#colors = rgbImage.getcolors()
		C = generate_colour_map()
		#print(C)
		C = np.squeeze(C)
		C = C[...,::-1]
		#print(C)
		C2 = C/255.0
		#print(C2)
		ccm = ListedColormap(C2)
		#print(ccm)
		fig = plt.figure()
		plt.title('Frame: ' + str(frame) + '   Max Temp: ' + readTemp(toggleUnitState, 'max'))
		bounds = [0, 50, 100]
		im = plt.imshow(rgbImage, cmap=ccm, clim=(readTempInt(toggleUnitState, 'min'), readTempInt(toggleUnitState, 'max')))
		cbar = fig.colorbar(im);
		cbar.ax.minorticks_on()
		limits = cbar.get_clim()
		cbar.set_label('     [$^\circ$' + toggleUnitState + ']', rotation=0) #270
		plt.show()

	def enableThings(self):
		self.playVidBut.setEnabled(True)
		self.pauseVidBut.setEnabled(True)
		self.nextFrame.setEnabled(True)
		self.prevFrame.setEnabled(True)
		self.startEdit.setEnabled(True)
		self.stopEdit.setEnabled(True)
		self.saveAsVideoSS.setEnabled(True)
		self.saveCvImageBut.setEnabled(True)
		self.makeTiffBut.setEnabled(True)
		self.displayC.setEnabled(True)
		self.displayF.setEnabled(True)
		self.tempScaleBut.setEnabled(True)

	def getFile(self):
		global frame
		global fileSelected
		global editLastFrame
		global lastFrame
		global usedOnce
		#self.pauseVideo()
		if (len(sys.argv) > 1) and (usedOnce == 1):
			print("First file specified from command line")
			fileSelected = sys.argv[1]
			usedOnce = 0
		else:
			lastFileSelected = ""
			if fileSelected != "":
				lastFileSelected = fileSelected
			fileSelected = ""
			dlg = QFileDialog()
			dlg.setDefaultSuffix( '.HDF5' )
			fileSelected, filter = dlg.getOpenFileName(self, 'Open File', lastFileSelected, 'HDF5 (*.HDF5);; All Files (*)')
			print(fileSelected)
			self.dispSelectedFile.setText(fileSelected)
		if fileSelected != "":
			try:
				self.dispSelectedFile.setText(fileSelected)
				self.f_read = h5py.File(str(fileSelected), 'r')
				frame = 1
				self.dispImg()
				self.enableThings()
				self.setSlider()
				editLastFrame = lastFrame
				self.startEdit.setText(str(frame))
				self.stopEdit.setText(str(lastFrame))
				self.history.insertPlainText('Selected File and Displayed First Frame\n')
				self.history.moveCursor(QTextCursor.End)
				print('Selected File and Displayed First Frame')
				self.canvas.draw()
				#else:
			except:
				self.history.insertPlainText('ERROR: Incorrect File Type Selected\n Please select .HDF5 File\n')
				self.history.moveCursor(QTextCursor.End)
				print('Incorrect File Type Selected. Please select .HDF5 File.')
		else:
			self.history.insertPlainText('ERROR: Incorrect File Type Selected\n Please select .HDF5 File\n')
			self.history.moveCursor(QTextCursor.End)
			print('Incorrect File Type Selected. Please select .HDF5 File.')

def main():
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
