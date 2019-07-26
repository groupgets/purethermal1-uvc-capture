from ctypes import *
import ctypes
import platform
import gc

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

class uvc_frame_desc(Structure):
  pass

uvc_frame_desc._fields_ = [
              ("parent", POINTER(uvc_format_desc)),
              ("prev", POINTER(uvc_frame_desc)),
              ("next", POINTER(uvc_frame_desc)),
              # /** Type of frame, such as JPEG frame or uncompressed frme */
              ("bDescriptorSubtype", c_uint), # enum uvc_vs_desc_subtype bDescriptorSubtype;
              # /** Index of the frame within the list of specs available for this format */
              ("bFrameIndex", c_uint8),
              ("bmCapabilities", c_uint8),
              # /** Image width */
              ("wWidth", c_uint16),
              # /** Image height */
              ("wHeight", c_uint16),
              # /** Bitrate of corresponding stream at minimal frame rate */
              ("dwMinBitRate", c_uint32),
              # /** Bitrate of corresponding stream at maximal frame rate */
              ("dwMaxBitRate", c_uint32),
              # /** Maximum number of bytes for a video frame */
              ("dwMaxVideoFrameBufferSize", c_uint32),
              # /** Default frame interval (in 100ns units) */
              ("dwDefaultFrameInterval", c_uint32),
              # /** Minimum frame interval for continuous mode (100ns units) */
              ("dwMinFrameInterval", c_uint32),
              # /** Maximum frame interval for continuous mode (100ns units) */
              ("dwMaxFrameInterval", c_uint32),
              # /** Granularity of frame interval range for continuous mode (100ns) */
              ("dwFrameIntervalStep", c_uint32),
              # /** Frame intervals */
              ("bFrameIntervalType", c_uint8),
              # /** number of bytes per line */
              ("dwBytesPerLine", c_uint32),
              # /** Available frame rates, zero-terminated (in 100ns units) */
              ("intervals", POINTER(c_uint32))]

uvc_format_desc._fields_ = [
              ("parent", c_void_p),
              ("prev", POINTER(uvc_format_desc)),
              ("next", POINTER(uvc_format_desc)),
              # /** Type of image stream, such as JPEG or uncompressed. */
              ("bDescriptorSubtype", c_uint), # enum uvc_vs_desc_subtype bDescriptorSubtype;
              # /** Identifier of this format within the VS interface's format list */
              ("bFormatIndex", c_uint8),
              ("bNumFrameDescriptors", c_uint8),
              # /** Format specifier */
              ("guidFormat", c_char * 16), # union { uint8_t guidFormat[16]; uint8_t fourccFormat[4]; }
              # /** Format-specific data */
              ("bBitsPerPixel", c_uint8),
              # /** Default {uvc_frame_desc} to choose given this format */
              ("bDefaultFrameIndex", c_uint8),
              ("bAspectRatioX", c_uint8),
              ("bAspectRatioY", c_uint8),
              ("bmInterlaceFlags", c_uint8),
              ("bCopyProtect", c_uint8),
              ("bVariableSize", c_uint8),
              # /** Available frame specifications for this format */
              ("frame_descs", POINTER(uvc_frame_desc))]

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

class lep_sys_shutter_mode(Structure):
  _fields_ = [("shutterMode", c_uint32),
              ("tempLockoutState", c_uint32),
              ("videoFreezeDuringFFC", c_uint32),
              ("ffcDesired", c_uint32),
              ("elapsedTimeSinceLastFfc", c_uint32),
              ("desiredFfcPeriod", c_uint32),
              ("explicitCmdToOpen", c_bool),
              ("desiredFfcTempDelta", c_uint16),
              ("imminentDelay", c_uint16)]
# LEP_SYS_FFC_SHUTTER_MODE_E shutterMode;   /* defines current mode */
# LEP_SYS_SHUTTER_TEMP_LOCKOUT_STATE_E   tempLockoutState;
# LEP_SYS_ENABLE_E videoFreezeDuringFFC;
# LEP_SYS_ENABLE_E ffcDesired;              /* status of FFC desired */
# LEP_UINT32 elapsedTimeSinceLastFfc;       /* in milliseconds x1 */
# LEP_UINT32 desiredFfcPeriod;              /* in milliseconds x1 */
# LEP_BOOL   explicitCmdToOpen;             /* true or false */
# LEP_UINT16 desiredFfcTempDelta;           /* in Kelvin x100  */
# LEP_UINT16 imminentDelay;                 /* in frame counts x1 */
#
# }LEP_SYS_FFC_SHUTTER_MODE_OBJ_T, *LEP_SYS_FFC_SHUTTER_MODE_OBJ_T_PTR;

# Original default shutter mode below is incorrect due to improper ctypes
# Incorrect Default Shutter Info: (1, 0, 0, 0, 1, 0, 1, 0, 48928)
#  1	 shutterMode
#  0	 tempLockoutState
#  0	 videoFreezeDuringFFC
#  0	 ffcDesired
#  1	 elapsedTimeSinceLastFfc
#  0	 desiredFfcPeriod
#  True	 explicitCmdToOpen
#  0	 desiredFfcTempDelta
#  48928	 imminentDelay

# Correct Default Shutter Info According to IDD: (1, 0, 1, 0, 0, 180000, 0, 150, 52)
#  1	 shutterMode
#  0	 tempLockoutState
#  1	 videoFreezeDuringFFC
#  0	 ffcDesired
#  0	 elapsedTimeSinceLastFfc
#  180000	 desiredFfcPeriod
#  False	 explicitCmdToOpen
#  150	 desiredFfcTempDelta
#  52	 imminentDelay

# Default Shutter Info According to Lepton on Bootup: (1, 0, 1, 0, 0, 180000, 1, 0, 150)
#  1	 shutterMode
#  0	 tempLockoutState
#  1	 videoFreezeDuringFFC
#  0	 ffcDesired
#  0	 elapsedTimeSinceLastFfc
#  180000	 desiredFfcPeriod
#  True	 explicitCmdToOpen
#  0	 desiredFfcTempDelta
#  150	 imminentDelay

explicitCmdToOpenVal = 1
desiredFfcTempDeltaVal = 0
imminentDelayVal = 150

sysShutterManual = lep_sys_shutter_mode(0, 0, 1, 0, 0, 180000, explicitCmdToOpenVal, desiredFfcTempDeltaVal, imminentDelayVal)
sysShutterAuto = lep_sys_shutter_mode(1, 0, 1, 0, 0, 180000, explicitCmdToOpenVal, desiredFfcTempDeltaVal, imminentDelayVal)
sysShutterExternal = lep_sys_shutter_mode(2, 0, 1, 0, 0, 180000, explicitCmdToOpenVal, desiredFfcTempDeltaVal, imminentDelayVal)

def call_extension_unit(devh, unit, control, data, size):
  return libuvc.uvc_get_ctrl(devh, unit, control, data, size, 0x81)

def set_extension_unit(devh, unit, control, data, size):
  return libuvc.uvc_set_ctrl(devh, unit, control, data, size, 0x81)

PT_USB_VID = 0x1e4e
PT_USB_PID = 0x0100

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

VS_FMT_GUID_GREY = create_string_buffer(
    b"Y8  \x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71", 16
)

VS_FMT_GUID_Y16 = create_string_buffer(
    b"Y16 \x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71", 16
)

VS_FMT_GUID_YUYV = create_string_buffer(
    b"UYVY\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71", 16
)

VS_FMT_GUID_NV12 = create_string_buffer(
    b"NV12\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71", 16
)

VS_FMT_GUID_YU12 = create_string_buffer(
    b"I420\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71", 16
)

VS_FMT_GUID_BGR3 = create_string_buffer(
    b"\x7d\xeb\x36\xe4\x4f\x52\xce\x11\x9f\x53\x00\x20\xaf\x0b\xa7\x70", 16
)

VS_FMT_GUID_RGB565 = create_string_buffer(
    b"RGBP\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71", 16
)

libuvc.uvc_get_format_descs.restype = POINTER(uvc_format_desc)

def print_device_info(devh):
  vers = lep_oem_sw_version()
  call_extension_unit(devh, OEM_UNIT_ID, 9, byref(vers), 8)
  print("Version gpp: {0}.{1}.{2} dsp: {3}.{4}.{5}".format(
    vers.gpp_major, vers.gpp_minor, vers.gpp_build,
    vers.dsp_major, vers.dsp_minor, vers.dsp_build,
  ))

  flir_pn = create_string_buffer(32)
  call_extension_unit(devh, OEM_UNIT_ID, 8, flir_pn, 32)
  print("FLIR part #: {0}".format(flir_pn.raw))

  flir_sn = create_string_buffer(8)
  call_extension_unit(devh, SYS_UNIT_ID, 3, flir_sn, 8)
  print("FLIR serial #: {0}".format(repr(flir_sn.raw)))

def uvc_iter_formats(devh):
  p_format_desc = libuvc.uvc_get_format_descs(devh)
  while p_format_desc:
    yield p_format_desc.contents
    p_format_desc = p_format_desc.contents.next

def uvc_iter_frames_for_format(devh, format_desc):
  p_frame_desc = format_desc.frame_descs
  while p_frame_desc:
    yield p_frame_desc.contents
    p_frame_desc = p_frame_desc.contents.next

def print_device_formats(devh):
  for format_desc in uvc_iter_formats(devh):
    print("format: {0}".format(format_desc.guidFormat[0:4]))
    for frame_desc in uvc_iter_frames_for_format(devh, format_desc):
      print("  frame {0}x{1} @ {2}fps".format(frame_desc.wWidth, frame_desc.wHeight, int(1e7 / frame_desc.dwDefaultFrameInterval)))

def uvc_get_frame_formats_by_guid(devh, vs_fmt_guid):
  for format_desc in uvc_iter_formats(devh):
    if vs_fmt_guid[0:4] == format_desc.guidFormat[0:4]:
      return [fmt for fmt in uvc_iter_frames_for_format(devh, format_desc)]
  return []

def set_manual_ffc(devh):
    sizeData = 32
    shutter_mode = (c_uint16)(0)
    getSDK = 0x3D
    controlID = (getSDK >> 2) + 1 #formula from Kurt Kiefer
    print('controlID: ' + str(controlID))
    set_extension_unit(devh, SYS_UNIT_ID, controlID, byref(sysShutterManual), sizeData) #set_extension_unit(devh, unit, control, data, size)

def set_auto_ffc(devh):
    sizeData = 32
    shutter_mode = (c_uint16)(1)
    getSDK = 0x3D
    controlID = (getSDK >> 2) + 1 #formula from Kurt Kiefer
    print('controlID: ' + str(controlID))
    set_extension_unit(devh, SYS_UNIT_ID, controlID, byref(sysShutterAuto), sizeData)

def set_external_ffc(devh):
    sizeData = 32
    shutter_mode = (c_uint16)(2) #2 = external
    getSDK = 0x3D
    controlID = (getSDK >> 2) + 1 #formula from Kurt Kiefer
    print('controlID: ' + str(controlID))
    set_extension_unit(devh, SYS_UNIT_ID, controlID, byref(sysShutterExternal), sizeData)

shutter = lep_sys_shutter_mode()
def print_shutter_info(devh):
    getSDK = 0x3C
    controlID = (getSDK >> 2) + 1
    call_extension_unit(devh, SYS_UNIT_ID, controlID, byref(shutter), 32)
    print("Shutter Info:\n {0}\t shutterMode\n {1}\t tempLockoutState\n {2}\t videoFreezeDuringFFC\n\
 {3}\t ffcDesired\n {4}\t elapsedTimeSinceLastFfc\n {5}\t desiredFfcPeriod\n\
 {6}\t explicitCmdToOpen\n {7}\t desiredFfcTempDelta\n {8}\t imminentDelay\n".format(
        shutter.shutterMode, shutter.tempLockoutState, shutter.videoFreezeDuringFFC,
        shutter.ffcDesired, shutter.elapsedTimeSinceLastFfc, shutter.desiredFfcPeriod,
        shutter.explicitCmdToOpen, shutter.desiredFfcTempDelta, shutter.imminentDelay,
    ))

def perform_manual_ffc(devh):
    sizeData = 1
    shutter_mode = create_string_buffer(sizeData)
    #0x200 Module ID VID
    #0x3C get
    #0x3D set
    getSDK = 0x3D
    runFFC = 0x42
    controlID = (runFFC >> 2) + 1 #formula from Kurt Kiefer
    print('controlID: ' + str(controlID))
    set_extension_unit(devh, SYS_UNIT_ID, controlID, shutter_mode, sizeData) #set_extension_unit(devh, unit, control, data, size)

def set_gain_low(devh):
    sizeData = 4
    gain_mode = (c_uint16)(1) #0=HIGH, 1=LOW, 2=AUTO
    setGainSDK = 0x49
    controlID = (setGainSDK >> 2) + 1 #formula from Kurt Kiefer
    print('controlID: ' + str(controlID))
    set_extension_unit(devh, SYS_UNIT_ID, controlID, byref(gain_mode), sizeData) #set_extension_unit(devh, unit, control, data, size)
    perform_manual_ffc(devh)

def set_gain_high(devh):
    sizeData = 4
    gain_mode = (c_uint16)(0) #0=HIGH, 1=LOW, 2=AUTO
    setGainSDK = 0x49
    controlID = (setGainSDK >> 2) + 1 #formula from Kurt Kiefer
    print('controlID: ' + str(controlID))
    set_extension_unit(devh, SYS_UNIT_ID, controlID, byref(gain_mode), sizeData) #set_extension_unit(devh, unit, control, data, size)
    perform_manual_ffc(devh)

def set_gain_auto(devh):
    sizeData = 4
    gain_mode = (c_uint16)(2) #0=HIGH, 1=LOW, 2=AUTO
    setGainSDK = 0x49
    controlID = (setGainSDK >> 2) + 1 #formula from Kurt Kiefer
    print('controlID: ' + str(controlID))
    set_extension_unit(devh, SYS_UNIT_ID, controlID, byref(gain_mode), sizeData) #set_extension_unit(devh, unit, control, data, size)
    perform_manual_ffc(devh)
