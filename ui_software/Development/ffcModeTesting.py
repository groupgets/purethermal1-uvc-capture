#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uvctypesParabilis_v2 import *
import time

def main():
    ctx = POINTER(uvc_context)()
    dev = POINTER(uvc_device)()
    devh = POINTER(uvc_device_handle)()
    ctrl = uvc_stream_ctrl()

    res = libuvc.uvc_init(byref(ctx), 0)
    if res < 0:
        print("uvc_init error")
        exit(1)
    res = libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0)
    if res < 0:
        print("uvc_find_device error")
        exit(1)
    res = libuvc.uvc_open(dev, byref(devh))
    if res < 0:
        print("uvc_open error")
        exit(1)

    print_device_info(devh)
    print("Attempting to Call Shutter Mode")
    print_shutter_info(devh)
    print('Are things okay?')
    print("Attempting to Call Shutter Mode Again in 2 Seconds")
    time.sleep(2)
    print_shutter_info(devh)
    print('Setting FFC to AUTO')
    set_auto_ffc(devh)
    print('Is it set to Auto?')
    print_shutter_info(devh)
    print('Setting FFC to MANUAL')
    set_manual_ffc(devh)
    print('Is it set to MANUAL?')
    print_shutter_info(devh)
    print('What else changed?')


if __name__ == '__main__':
  main()
