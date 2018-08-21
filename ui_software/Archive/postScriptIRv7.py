import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import (QCoreApplication, QThread, QThreadPool, pyqtSignal, pyqtSlot, Qt, SIGNAL, QTimer, QDateTime)
from PyQt4.QtGui import (QImage, QWidget, QApplication, QLabel, QPixmap, QPushButton, QVBoxLayout, QGridLayout, QSizePolicy, QMessageBox, QFileDialog, QSlider)
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
def dispCDef():
    global toggleUnitState
    toggleUnitState = 'C'

def dispFDef():
    global toggleUnitState
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

class Window(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.initUI()

	def initUI(self):
		self.w = QWidget()
		
		# a figure instance to plot on
		self.figure = plt.figure()

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
		self.playVidBut.clicked.connect(self.playVid)
		self.makeTiffBut.clicked.connect(self.makeTiff)
		self.displayC.clicked.connect(dispCDef)
		self.displayC.clicked.connect(self.displayTempValues)
        	self.displayF.clicked.connect(dispFDef)
		self.displayF.clicked.connect(self.displayTempValues)
		self.sl.valueChanged.connect(self.slValueChange)
		#cid = self.canvas.mpl_connect('button_press_event', self.on_press)
		self.saveAsVideoBut.clicked.connect(self.saveVideo)

	def slValueChange(self):
		global frame
		frame = self.sl.value()
		self.dispImg()
		self.canvas.draw()

	def setSlider(self):
		global lastFrame
		self.sl.setMinimum(1)
      		self.sl.setMaximum(lastFrame)
      		self.sl.setValue(1)
      		self.sl.setTickPosition(QSlider.TicksBelow)
      		self.sl.setTickInterval(9)
		self.slStartF.setText('Frame: 1')
		self.slMidF.setText('Frame: ' + str(lastFrame/2))
		self.slEndF.setText('Frame: ' + str(lastFrame))
		self.slStartT.setText('0 Seconds')
		self.slMidT.setText(str(lastFrame/(2*9)) + ' Seconds')
		self.slEndT.setText(str(lastFrame/9) + ' Seconds')	

	#dpi = 100

	def saveVideo(self):
	    print('Saving Video')	
	    fig = plt.figure()
	    ax = fig.add_subplot(111)
	    ax.set_aspect('equal')
	    ax.get_xaxis().set_visible(False)
	    ax.get_yaxis().set_visible(False)

	    img1 = self.grabDataFrame()
	    im = ax.imshow(img1,cmap='gray',interpolation='nearest')
	    im.set_clim([0,1])
	    fig.set_size_inches([5,5])


	    #tight_layout()


	    def update_img(n):
		global frame
		frame = n
		imgN = self.grabDataFrame()
		#dataCollection = np.dstack((dataCollection,data))
		#tmp = np.random.randn(300,300)
		im.set_data(imgN)
		return im

	    #legend(loc=0)
	    ani = animation.FuncAnimation(fig,update_img,300,interval=30)
	    writer = animation.writers['ffmpeg'](fps=30)

	    ani.save('demo2.mp4',writer=writer,dpi=100)
	    return ani

	def makeTiff(self):
		global lastFrame
		for i in range(1,lastFrame):
			    print('Frame to Tiff: ' + str(i))
			    data = self.f_read[('image'+str(i))][:]
			    if i == 1:
				dataCollection = data
			    else:
				dataCollection = np.dstack((dataCollection,data))
			    i += 1
		filename = ('Lepton TIFF Vid ' + QDateTime.currentDateTime().toString())
		imsave(filename, dataCollection)

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
		xMouse = event.xdata
		yMouse = event.ydata
		cursorVal = self.grabTempValue()
		if xMouse > 1 and xMouse < 640 and yMouse > 0 and yMouse < 480:
			self.cursorTempLabel.setText('Cursor Temp: ' + readTemp(toggleUnitState, 'none'))
		else:
			self.cursorTempLabel.setText('Cursor Temp: MOVE CURSOR OVER IMAGE')

    	def displayTempValues(self):
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
		rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		return(rgbImage)

	def playVid(self):	
		global frame
		global lastFrame
		global fileSelected
		img = None
		for i in range(frame,lastFrame):
			frame = i
			im = self.grabDataFrame()
			print(i)
			if img is None:
        			img = self.ax.imshow(im)
    			else:
        			img.set_data(im)
			plt.pause(0.111)
			#plt.show()

	def playVid2(self):	
		#http://scipyscriptrepo.com/wp/?p=9
		global frame
		global lastFrame
		global fileSelected
		img = None
		def simData():
		# this function is called as the argument for
		# the simPoints function. This function contains
		# (or defines) and iterator---a device that computes
		# a value, passes it back to the main program, and then
		# returns to exactly where it left off in the function upon the
		# next call. I believe that one has to use this method to animate
		# a function using the matplotlib animation package.			
			if img is None:
        			img = self.ax.imshow(im)
    			else:
        			img.set_data(im)
		 
		def simPoints(simData):
		    img.set_data(im)
		 
		##
		##   set up figure for plotting:
		##
		#fig = plt.figure()
		ax = self.figure.add_subplot(111)
		im = self.grabDataFrame()
		# I'm still unfamiliar with the following line of code:
		#line, = ax.plot([], [], 'bo', ms=10)
		#ax.set_ylim(-1, 1)
		#ax.set_xlim(0, 10)
		##
		#time_template = 'Time = %.1f s'    # prints running simulation time
		#time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
		## Now call the animation package: (simData is the user function
		## serving as the argument for simPoints):
		ani = FuncAnimation(self.figure, simPoints, simData, blit=False,\
		     interval=10, repeat=True)
		plt.show()

	def playVid3(self):	
		"""
		This short code snippet utilizes the new animation package in
		matplotlib 1.1.0; it's the shortest snippet that I know of that can
		produce an animated plot in python. I'm still hoping that the
		animate package's syntax can be simplified further. 
		"""
		import numpy as np
		import matplotlib.pyplot as plt
		import matplotlib.animation as animation
		 
		def simData():
		# this function is called as the argument for
		# the simPoints function. This function contains
		# (or defines) and iterator---a device that computes
		# a value, passes it back to the main program, and then
		# returns to exactly where it left off in the function upon the
		# next call. I believe that one has to use this method to animate
		# a function using the matplotlib animation package.
		#
		    t_max = 10.0
		    dt = 0.05
		    x = 0.0
		    t = 0.0
		    print('Ran Sim Data')
		    while t < t_max:
			x = np.sin(np.pi*t)
			t = t + dt
			print('Ran While Loop')
			yield x, t
		 
		def simPoints(simData):
		    print('Ran Sim Points')
		    x, t = simData[0], simData[1]
		    time_text.set_text(time_template%(t))
		    line.set_data(t, x)
		    return line, time_text
		 
		##
		##   set up figure for plotting:
		##
		fig = plt.figure()
		ax = fig.add_subplot(111)
		# I'm still unfamiliar with the following line of code:
		line, = ax.plot([], [], 'bo', ms=10)
		ax.set_ylim(-1, 1)
		ax.set_xlim(0, 10)
		##
		time_template = 'Time = %.1f s'    # prints running simulation time
		time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
		## Now call the animation package: (simData is the user function
		## serving as the argument for simPoints):
		print('Ran before Animation')
		ani = FuncAnimation(fig, simPoints, simData, blit=False,\
		     interval=10, repeat=True)
		plt.show()

	def playVid4(self):
		global frame
		global lastFrame
		global fileSelected
		def simData():
			img = None
		def simPoints(simData):
			im = self.grabDataFrame()
			print(i)
			if img is None:
        			img = self.ax.imshow(im)
    			else:
        			img.set_data(im)
		ani = FuncAnimation(self.figure, simPoints, simData, blit=False,\
		     interval=10, repeat=True)
		plt.show()

	def dispNextImg(self):
		global frame
		global lastFrame
		if lastFrame > frame:
			frame += 1
		else:
			print('You are at Last Frame')
		self.dispImg()
		self.canvas.draw()
		self.sl.setValue(frame)

	def dispPrevImg(self):
		global frame
		if frame > 1:
			frame -= 1
		else:
			print('You are at First Frame')
		self.dispImg()
		self.canvas.draw()
		self.sl.setValue(frame)

	def dispImg(self):
		global frame
		global lastFrame
		global fileSelected
		global maxVal
    		global minVal
		global maxLoc
    		global minLoc
		#print('Display Image at Frame: ' + str(frame))
		self.currentFrameDisp.setText('Current Frame: ' + str(frame))
		data = self.f_read[('image'+str(frame))][:]
		data = cv2.resize(data[:,:], (640, 480))
		minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(data)
		img = cv2.LUT(raw_to_8bit(data), generate_colour_map())
		rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.ax = self.figure.add_subplot(111)
		self.ax.clear()
		self.ax.imshow(rgbImage)
		lastFrame = len(self.f_read)
		self.sl.setValue(frame)
		self.displayTempValues()
		cid = self.canvas.mpl_connect('motion_notify_event', self.hover)
	
	def getFile(self):
		global fileSelected
		fileSelected = QFileDialog.getOpenFileName(self.w, 'Open File', '/')
		self.dispSelectedFile.setText(fileSelected)
		self.f_read = h5py.File(str(fileSelected), 'r')
		self.dispImg()
		self.setSlider()
		self.canvas.draw()

def main():
    app = QtGui.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()