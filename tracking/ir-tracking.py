#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uvctypes import *
import time
import cv2
import numpy as np
try:
  from queue import Queue
except ImportError:
  from Queue import Queue
import platform

BUF_SIZE = 2
q = Queue(BUF_SIZE)

def py_frame_callback(frame, userptr):

  array_pointer = cast(frame.contents.data, POINTER(c_uint16 * (frame.contents.width * frame.contents.height)))
  data = np.frombuffer(
    array_pointer.contents, dtype=np.dtype(np.uint16)
  ).reshape(
    frame.contents.height, frame.contents.width
  ) # no copy

  # data = np.fromiter(
  #   frame.contents.data, dtype=np.dtype(np.uint8), count=frame.contents.data_bytes
  # ).reshape(
  #   frame.contents.height, frame.contents.width, 2
  # ) # copy

  if frame.contents.data_bytes != (2 * frame.contents.width * frame.contents.height):
    return

  if not q.full():
    q.put(data)

PTR_PY_FRAME_CALLBACK = CFUNCTYPE(None, POINTER(uvc_frame), c_void_p)(py_frame_callback)

def ktof(val):
  return (1.8 * ktoc(val) + 32.0)

def ktoc(val):
  return (val - 27315) / 100.0

def raw_to_8bit(data):
  cv2.normalize(data, data, 0, 65535, cv2.NORM_MINMAX)
  np.right_shift(data, 8, data)
  return cv2.cvtColor(np.uint8(data), cv2.COLOR_GRAY2RGB)

def display_temperature(img, val_k, loc, color):
  val = ktof(val_k)
  cv2.putText(img,"{0:.1f} degF".format(val), loc, cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
  x, y = loc
  cv2.line(img, (x - 2, y), (x + 2, y), color, 1)
  cv2.line(img, (x, y - 2), (x, y + 2), color, 1)

def findBounds(img, fire):
  #print("finding bounds")
  #print(minTemp)
  lower1 = np.array([240,240,240])
  upper1 = np.array([255,255,255])
  mask1 = cv2.inRange(img, lower1, upper1)
  res =cv2.bitwise_and(img, img, mask = mask1)
  image, cnts, hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  cnt = cnts[0]
  size = len(cnts)
  #print(size)
  #M = cv2.moments(cnt)
  #print(M)
  x,y,w,h = cv2.boundingRect(cnt)
  res = cv2.rectangle(res,(x,y),(x+w,y+h),(0,255,0),2)
  
  centres = []
  for i in range(len(cnts)):
    x,y,w,h = cv2.boundingRect(cnts[i])
    if (fire == True):
      print('Location on Image: (' + str(x+w) +  ', ' + str(y+h) + ')')
    res = cv2.rectangle(res,(x,y),(x+w,y+h),(0,255,0),2)
    #moments = cv2.moments(cnts[i])
    #centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
    #cv2.circle(img, centres[-1], 3, (0,0,0), -1)
    
  return res
  
def findMask(img):
  #print("finding bounds")
  #print(minTemp)
  lower1 = np.array([240,240,240])
  upper1 = np.array([255,255,255])
  mask1 = cv2.inRange(img, lower1, upper1)
  res =cv2.bitwise_and(img, img, mask = mask1)
  return res

def main():
  #tracker stuff
  
  #ir stuff
  ctx = POINTER(uvc_context)()
  dev = POINTER(uvc_device)()
  devh = POINTER(uvc_device_handle)()
  ctrl = uvc_stream_ctrl()

  res = libuvc.uvc_init(byref(ctx), 0)
  if res < 0:
    print("uvc_init error")
    exit(1)

  try:
    res = libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0)
    if res < 0:
      print("uvc_find_device error")
      exit(1)

    try:
      res = libuvc.uvc_open(dev, byref(devh))
      if res < 0:
        print("uvc_open error")
        exit(1)

      print("device opened!")

      print_device_info(devh)
      print_device_formats(devh)

      frame_formats = uvc_get_frame_formats_by_guid(devh, VS_FMT_GUID_Y16)
      if len(frame_formats) == 0:
        print("device does not support Y16")
        exit(1)

      libuvc.uvc_get_stream_ctrl_format_size(devh, byref(ctrl), UVC_FRAME_FORMAT_Y16,
        frame_formats[0].wWidth, frame_formats[0].wHeight, int(1e7 / frame_formats[0].dwDefaultFrameInterval)
      )

      res = libuvc.uvc_start_streaming(devh, byref(ctrl), PTR_PY_FRAME_CALLBACK, None, 0)
      if res < 0:
        print("uvc_start_streaming failed: {0}".format(res))
        exit(1)

      i = 0
      fire = False
      val = True
      try:
        while val:
          data = q.get(True, 500)
          indices = np.where(data > 255)
          if data is None:
            break
          data = cv2.resize(data[:,:], (640, 480))
          minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(data)
          img = raw_to_8bit(data)
          myres = findBounds(img, fire)
          mymask = findMask(img)
          display_temperature(img, minVal, minLoc, (255, 0, 0))
          display_temperature(img, maxVal, maxLoc, (0, 0, 255))
          
          maxDisplay = 110 #F
          if (ktof(maxVal) > maxDisplay):
            fire = True
            print('Recording Alert Number: ' + str(i)) 
            i = i + 1
            #grab orientation
            #grab location of center of hot spot(s)
            #locally save image of hot spot (at least once)
            #decide when to beam down image
          else: 
            fire = False
          
          cv2.imshow('Lepton Radiometry', img)
          #cv2.imshow('findMask',mymask)
          cv2.imshow('findBounds',myres)
          
          val = True
          cv2.waitKey(1)

        cv2.destroyAllWindows()
      finally:
        libuvc.uvc_stop_streaming(devh)

      print("done")
    finally:
      libuvc.uvc_unref_device(dev)
  finally:
    libuvc.uvc_exit(ctx)

if __name__ == '__main__':
  main()
