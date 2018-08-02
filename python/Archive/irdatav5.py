from PyQt4.QtCore import (QCoreApplication, QThread, QThreadPool, pyqtSignal, pyqtSlot, Qt)
from PyQt4.QtGui import (QImage, QWidget, QApplication, QLabel, QPixmap, QPushButton)
import sys
import cv2
from tifffile import imsave
import numpy as np
from uvctypes import *
from Queue import Queue
  
BUF_SIZE = 2
q = Queue(BUF_SIZE)

def py_frame_callback(frame, userptr):
  array_pointer = cast(frame.contents.data, POINTER(c_uint16 * (frame.contents.width * frame.contents.height)))
  data = np.frombuffer(
    array_pointer.contents, dtype=np.dtype(np.uint16)).reshape(frame.contents.height, frame.contents.width)
  if frame.contents.data_bytes != (2 * frame.contents.width * frame.contents.height):
    return
  if not q.full():
    q.put(data)

PTR_PY_FRAME_CALLBACK = CFUNCTYPE(None, POINTER(uvc_frame), c_void_p)(py_frame_callback)

def startStream():
    ctx = POINTER(uvc_context)()
    dev = POINTER(uvc_device)()
    devh = POINTER(uvc_device_handle)()
    ctrl = uvc_stream_ctrl()
    res = libuvc.uvc_init(byref(ctx), 0)
    res = libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0)
    res = libuvc.uvc_open(dev, byref(devh))
    print("Device Opened!")
    print_device_info(devh)
    print_device_formats(devh)
    frame_formats = uvc_get_frame_formats_by_guid(devh, VS_FMT_GUID_Y16)
    libuvc.uvc_get_stream_ctrl_format_size(devh, byref(ctrl), UVC_FRAME_FORMAT_Y16,
    frame_formats[0].wWidth, frame_formats[0].wHeight, int(1e7 / frame_formats[0].dwDefaultFrameInterval))
    res = libuvc.uvc_start_streaming(devh, byref(ctrl), PTR_PY_FRAME_CALLBACK, None, 0)

def raw_to_8bit(data):
        cv2.normalize(data, data, 0, 65535, cv2.NORM_MINMAX)
        np.right_shift(data, 8, data)
        return cv2.cvtColor(np.uint8(data), cv2.COLOR_GRAY2RGB)

tiff_frame = 1
def getFrame():
    global tiff_frame
    global dataCollection
    data = q.get(True, 500)
    if data is None:
        print('No Data')
    if tiff_frame == 1:
        dataCollection = data
    else:
        dataCollection = np.dstack((dataCollection,data))
    tiff_frame += 1
    data = cv2.resize(data[:,:], (640, 480))
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(data)
    img = raw_to_8bit(data)
    return img

fileNum = 1
@pyqtSlot(QImage)
def storeData():
    print(dataCollection.shape)
    global fileNum
    try:
        imsave('testPiQt' + `fileNum` + '.tiff',dataCollection)
        print('Saved Content')
        fileNum += 1
    except SaveError:
        print('Try Again')

def endStream():
    ctx = POINTER(uvc_context)()
    dev = POINTER(uvc_device)()
    devh = POINTER(uvc_device_handle)()
    libuvc.uvc_stop_streaming(devh)
    print('done')
    libuvc.uvc_unref_device(dev)
    libuvc.uvc_exit(ctx)

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        # print('Start Stream')
        startStream()
        while True:
            frame = getFrame()
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

class App(QWidget):
    def __init__(self):
        super(App,self).__init__()
        self.title = 'PyQt4 IR Data'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(640, 480)
        # create a label
        # print('Create Label')
        self.label = QLabel(self)
        #self.label.move(280, 120)
        btn = QPushButton('Store Data',self)
        btn.clicked.connect(storeData)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())