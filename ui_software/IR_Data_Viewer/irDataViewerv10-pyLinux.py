import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import (QCoreApplication, QThread, QThreadPool, pyqtSignal, pyqtSlot, Qt, SIGNAL, QTimer, QDateTime)
from PyQt4.QtGui import (QImage, QWidget, QApplication, QLabel, QPixmap, QPushButton, QVBoxLayout, QGridLayout, QSizePolicy, QMessageBox, QFileDialog, QSlider, QComboBox, QTextCursor)
import numpy as np
import cv2
import h5py
from tifffile import imsave
import time

qtCreatorFile = "ir_post.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import TimedAnimation
import matplotlib.animation as animation
from matplotlib import cm
import matplotlib as mpl
from matplotlib.contour import ContourSet

import random

def generate_colour_map():
    """
    Conversion of the colour map from GetThermal to a numpy LUT:
        https://github.com/groupgets/GetThermal/blob/bb467924750a686cc3930f7e3a253818b755a2c0/src/dataformatter.cpp#L6
    """

    lut = np.zeros((256, 1, 3), dtype=np.uint8)

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
        xrange(0, len(ulist),
               step))

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
    return (1.8 * ktoc(val) + 32.0)

def ktoc(val):
    return (val - 27315) / 100.0

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

def raw_to_8bit(data):
    cv2.normalize(data, data, 0, 65535, cv2.NORM_MINMAX)
    np.right_shift(data, 8, data)
    return cv2.cvtColor(np.uint8(data), cv2.COLOR_GRAY2RGB)

frame = 1
videoState = 'notPlay'
framerate = 1 #(9 frames per second)
timerHz = 111
fileSelected = ""

class Window(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.initUI()

	def initUI(self):
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
	
		#self.history.verticalScrollBar().setValue(self.history.verticalScrollBar().maximum())

		self.timer = QTimer(self)
		self.timer.setInterval(timerHz)
		self.timer.timeout.connect(self.playVid5)
		self.timer.start()

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

	def startTimer(self):
		global hz
		self.timer.stop()
		print(hz)		
		self.timer.setInterval(timerHz)
		self.timer.timeout.connect(self.playVid5)
		self.timer.start()
		print('Re-Started Timer')

	def stopTimer(self):
		self.timer.stop()

	def speed(self):
		global framerate
		hzIndex = self.comboBoxHz.currentIndex()
		if hzIndex == 0: 
			framerate = 0.5
			print('Half Framerate')
		elif hzIndex == 1:
			framerate = 1
			print('Normal Framerate')
		elif hzIndex == 2:
			framerate = 2
			print('Double Framerate')
		else:
			hz = 111
		self.startTimer()

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
		self.slMidF.setText('Mid Frame: ' + str(lastFrame/2))
		self.slEndF.setText('Last Frame: ' + str(lastFrame))
		self.slStartT.setText('0 Seconds')
		self.slMidT.setText(str(lastFrame/(2*9)) + ' Seconds')
		self.slEndT.setText(str(lastFrame/9) + ' Seconds')	

	def saveVideoSS(self):
		global frame
		global editLastFrame
		global videoState
		videoState = 'pause'
		if fileSelected != "":
			fileNameVid = ""
			dlgVid = QFileDialog()
			#dlg.setNameFilter('PNG files (*.png)')
			dlgVid.setDefaultSuffix('.avi')
			fileNameVid = dlgVid.getSaveFileName(self.w, 'Navigate to Directory and Choose a File Name to Save To', 'untitled.avi', 'AVI Video (*.avi)')
			#if self.startEdit.isModified():
			fileNameVid = str(fileNameVid)
			#if fileNameVid.endswith('.avi') == False:
			#	fileNameVid = fileNameVid + '.avi' 
			frame = int(self.startEdit.text())
			#if self.stopEdit.isModified():	
			editLastFrame = int(self.stopEdit.text())
			fourcc = cv2.cv.CV_FOURCC(*'XVID')
			if fileNameVid != "":
				try:
			    		out = cv2.VideoWriter(fileNameVid,fourcc, 9.0, (640,480), True)
					for i in range(frame, editLastFrame):
						frameForVid = self.grabDataFrame()
						out.write(frameForVid)
						if frame <= editLastFrame:
							frame += framerate
						else:
							print('You are at Last Frame')
					out.release()
					print('Saved Video As ' + str(fileNameVid))
					self.history.insertPlainText('SUCCESS: Saved Video\n')
					self.history.moveCursor(QTextCursor.End)
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
			fileNameImage = dlg.getSaveFileName(self.w, 'Navigate to Directory and Choose a File Name to Save To', 'untitled.png', 'PNG Image (*.png)')
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
			fileNameTiff = dlgTiff.getSaveFileName(self.w, 'Navigate to Directory and Choose a File Name to Save To', 'untitled.tiff', 'TIFF File (*.tiff)')
			print(fileNameTiff)
			if fileNameTiff != "":
				self.history.insertPlainText('File Name Selected\n')
				self.history.moveCursor(QTextCursor.End)
				print('Collecting Data Frames...')
				for i in range(1,lastFrame):
					    #print('Frame to Tiff: ' + str(i))
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

	def getFile(self):
		global frame
		global fileSelected
		global editLastFrame
		global lastFrame
		#self.pauseVideo()
		fileSelected = ""
		fileSelected = QFileDialog.getOpenFileName(self.w, 'Open File', '/')
		print(fileSelected)
		#fileTypes = ['hdf5','HDF5','HD5F','hd5f']
		if fileSelected != "":
			#if any(x in fileSelected for x in fileTypes):
			try:
				self.dispSelectedFile.setText(fileSelected)
				self.f_read = h5py.File(str(fileSelected), 'r')
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
    app = QtGui.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()