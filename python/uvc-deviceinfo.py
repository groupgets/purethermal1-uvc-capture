#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uvctypes import *

def print_device_info(devh):

  vers = lep_oem_sw_version()
  call_extension_unit(devh, OEM_UNIT_ID, 9, byref(vers), 8)
  print "Version gpp: {0}.{1}.{2} dsp: {3}.{4}.{5}".format(
    vers.gpp_major, vers.gpp_minor, vers.gpp_build,
    vers.dsp_major, vers.dsp_minor, vers.dsp_build,
  )

  flir_pn = create_string_buffer(32)
  call_extension_unit(devh, OEM_UNIT_ID, 8, flir_pn, 32)
  print("FLIR part #: {0}".format(flir_pn.raw))

def main():
  ctx = POINTER(uvc_context)()
  dev = POINTER(uvc_device)()
  devh = POINTER(uvc_device_handle)()
  ctrl = uvc_stream_ctrl()

  res = libuvc.uvc_init(byref(ctx), 0)
  if res < 0:
    print("uvc_init error")
    exit(1)

  try:
    res = libuvc.uvc_find_device(ctx, byref(dev), 0, 0, 0)
    if res < 0:
      print("uvc_find_device error")
      exit(1)

    try:
      res = libuvc.uvc_open(dev, byref(devh))
      if res < 0:
        print("uvc_open error")
        exit(1)

      print_device_info(devh)

    finally:
      libuvc.uvc_unref_device(dev)
  finally:
    libuvc.uvc_exit(ctx)

if __name__ == '__main__':
  main()
