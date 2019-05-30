#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uvctypes_ffc import *

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
    print("Attempting to Manual FFC")
    set_manual_ffc(devh)
    #perform_manual_ffc(devh)
    print("Success?")

if __name__ == '__main__':
  main()
