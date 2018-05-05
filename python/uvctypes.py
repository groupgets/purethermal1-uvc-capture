from ctypes import *
import platform

try:
  if platform.system() == 'Darwin':
    libuvc = cdll.LoadLibrary("libuvc.dylib")
  elif platform.system() == 'Linux':
    libuvc = cdll.LoadLibrary("libuvc.so")
  else:
    libuvc = cdll.LoadLibrary("libuvc")
except OSError:
  print("Error: could not find libuvc!")
  exit(1)

class uvc_context(Structure):
  _fields_ = [("usb_ctx", c_void_p),
              ("own_usb_ctx", c_uint8),
              ("open_devices", c_void_p),
              ("handler_thread", c_ulong),
              ("kill_handler_thread", c_int)]

class uvc_device(Structure):
  _fields_ = [("ctx", POINTER(uvc_context)),
              ("ref", c_int),
              ("usb_dev", c_void_p)]

class uvc_stream_ctrl(Structure):
  _fields_ = [("bmHint", c_uint16),
              ("bFormatIndex", c_uint8),
              ("bFrameIndex", c_uint8),
              ("dwFrameInterval", c_uint32),
              ("wKeyFrameRate", c_uint16),
              ("wPFrameRate", c_uint16),
              ("wCompQuality", c_uint16),
              ("wCompWindowSize", c_uint16),
              ("wDelay", c_uint16),
              ("dwMaxVideoFrameSize", c_uint32),
              ("dwMaxPayloadTransferSize", c_uint32),
              ("dwClockFrequency", c_uint32),
              ("bmFramingInfo", c_uint8),
              ("bPreferredVersion", c_uint8),
              ("bMinVersion", c_uint8),
              ("bMaxVersion", c_uint8),
              ("bInterfaceNumber", c_uint8)]

class uvc_format_desc(Structure):
  pass

class timeval(Structure):
  _fields_ = [("tv_sec", c_long), ("tv_usec", c_long)]

class uvc_frame(Structure):
  _fields_ = [# /** Image data for this frame */
              ("data", POINTER(c_uint8)),
              # /** Size of image data buffer */
              ("data_bytes", c_size_t),
              # /** Width of image in pixels */
              ("width", c_uint32),
              # /** Height of image in pixels */
              ("height", c_uint32),
              # /** Pixel data format */
              ("frame_format", c_uint), # enum uvc_frame_format frame_format
              # /** Number of bytes per horizontal line (undefined for compressed format) */
              ("step", c_size_t),
              # /** Frame number (may skip, but is strictly monotonically increasing) */
              ("sequence", c_uint32),
              # /** Estimate of system time when the device started capturing the image */
              ("capture_time", timeval),
              # /** Handle on the device that produced the image.
              #  * @warning You must not call any uvc_* functions during a callback. */
              ("source", POINTER(uvc_device)),
              # /** Is the data buffer owned by the library?
              #  * If 1, the data buffer can be arbitrarily reallocated by frame conversion
              #  * functions.
              #  * If 0, the data buffer will not be reallocated or freed by the library.
              #  * Set this field to zero if you are supplying the buffer.
              #  */
              ("library_owns_data", c_uint8)]

class uvc_device_handle(Structure):
  _fields_ = [("dev", POINTER(uvc_device)),
              ("prev", c_void_p),
              ("next", c_void_p),
              ("usb_devh", c_void_p),
              ("info", c_void_p),
              ("status_xfer", c_void_p),
              ("status_buf", c_ubyte * 32),
              ("status_cb", c_void_p),
              ("status_user_ptr", c_void_p),
              ("button_cb", c_void_p),
              ("button_user_ptr", c_void_p),
              ("streams", c_void_p),
              ("is_isight", c_ubyte)]

class lep_oem_sw_version(Structure):
  _fields_ = [("gpp_major", c_ubyte),
              ("gpp_minor", c_ubyte),
              ("gpp_build", c_ubyte),
              ("dsp_major", c_ubyte),
              ("dsp_minor", c_ubyte),
              ("dsp_build", c_ubyte),
              ("reserved", c_ushort)]

def call_extension_unit(devh, unit, control, data, size):
  return libuvc.uvc_get_ctrl(devh, unit, control, data, size, 0x81)

AGC_UNIT_ID = 3
OEM_UNIT_ID = 4
RAD_UNIT_ID = 5
SYS_UNIT_ID = 6
VID_UNIT_ID = 7

UVC_FRAME_FORMAT_UYVY = 4
UVC_FRAME_FORMAT_I420 = 5
UVC_FRAME_FORMAT_RGB = 7
UVC_FRAME_FORMAT_BGR = 8
UVC_FRAME_FORMAT_Y16 = 13
