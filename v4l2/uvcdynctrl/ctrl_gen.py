#!/usr/bin/env python
import sys
import re

INPUT_REGISTER_DEFINITIONS = """
#define LEP_CID_AGC_ENABLE_STATE                (LEP_AGC_MODULE_BASE + 0x0000 )
#define LEP_CID_AGC_POLICY                      (LEP_AGC_MODULE_BASE + 0x0004 )
#define LEP_CID_AGC_ROI                         (LEP_AGC_MODULE_BASE + 0x0008 )
#define LEP_CID_AGC_STATISTICS                  (LEP_AGC_MODULE_BASE + 0x000C )
#define LEP_CID_AGC_HISTOGRAM_CLIP_PERCENT      (LEP_AGC_MODULE_BASE + 0x0010 )
#define LEP_CID_AGC_HISTOGRAM_TAIL_SIZE         (LEP_AGC_MODULE_BASE + 0x0014 )
#define LEP_CID_AGC_LINEAR_MAX_GAIN             (LEP_AGC_MODULE_BASE + 0x0018 )
#define LEP_CID_AGC_LINEAR_MIDPOINT             (LEP_AGC_MODULE_BASE + 0x001C )
#define LEP_CID_AGC_LINEAR_DAMPENING_FACTOR     (LEP_AGC_MODULE_BASE + 0x0020 )
#define LEP_CID_AGC_HEQ_DAMPENING_FACTOR        (LEP_AGC_MODULE_BASE + 0x0024 )
#define LEP_CID_AGC_HEQ_MAX_GAIN                (LEP_AGC_MODULE_BASE + 0x0028 )
#define LEP_CID_AGC_HEQ_CLIP_LIMIT_HIGH         (LEP_AGC_MODULE_BASE + 0x002C )
#define LEP_CID_AGC_HEQ_CLIP_LIMIT_LOW          (LEP_AGC_MODULE_BASE + 0x0030 )
#define LEP_CID_AGC_HEQ_BIN_EXTENSION           (LEP_AGC_MODULE_BASE + 0x0034 )
#define LEP_CID_AGC_HEQ_MIDPOINT                (LEP_AGC_MODULE_BASE + 0x0038 )
#define LEP_CID_AGC_HEQ_EMPTY_COUNTS            (LEP_AGC_MODULE_BASE + 0x003C )
#define LEP_CID_AGC_HEQ_NORMALIZATION_FACTOR    (LEP_AGC_MODULE_BASE + 0x0040 )
#define LEP_CID_AGC_HEQ_SCALE_FACTOR            (LEP_AGC_MODULE_BASE + 0x0044 )
#define LEP_CID_AGC_CALC_ENABLE_STATE           (LEP_AGC_MODULE_BASE + 0x0048 )
#define LEP_CID_AGC_HEQ_LINEAR_PERCENT          (LEP_AGC_MODULE_BASE + 0x004C )

#define LEP_CID_OEM_POWER_DOWN                  (LEP_OEM_MODULE_BASE + 0x4000 )
#define LEP_CID_OEM_STANDBY                     (LEP_OEM_MODULE_BASE + 0x4004 )
#define LEP_CID_OEM_LOW_POWER_MODE_1            (LEP_OEM_MODULE_BASE + 0x4008 )
#define LEP_CID_OEM_LOW_POWER_MODE_2            (LEP_OEM_MODULE_BASE + 0x400C )
#define LEP_CID_OEM_BIT_TEST                    (LEP_OEM_MODULE_BASE + 0x4010 )
#define LEP_CID_OEM_MASK_REVISION               (LEP_OEM_MODULE_BASE + 0x4014 )
#define LEP_CID_OEM_FLIR_PART_NUMBER            (LEP_OEM_MODULE_BASE + 0x401C )
#define LEP_CID_OEM_SOFTWARE_VERSION            (LEP_OEM_MODULE_BASE + 0x4020 )
#define LEP_CID_OEM_VIDEO_OUTPUT_ENABLE         (LEP_OEM_MODULE_BASE + 0x4024 )
#define LEP_CID_OEM_VIDEO_OUTPUT_FORMAT         (LEP_OEM_MODULE_BASE + 0x4028 )
#define LEP_CID_OEM_VIDEO_OUTPUT_SOURCE         (LEP_OEM_MODULE_BASE + 0x402C )
#define LEP_CID_OEM_VIDEO_OUTPUT_CHANNEL        (LEP_OEM_MODULE_BASE + 0x4030 )
#define LEP_CID_OEM_VIDEO_GAMMA_ENABLE          (LEP_OEM_MODULE_BASE + 0x4034 )
#define LEP_CID_OEM_CUST_PART_NUMBER            (LEP_OEM_MODULE_BASE + 0x4038 )
#define LEP_CID_OEM_VIDEO_OUTPUT_CONSTANT       (LEP_OEM_MODULE_BASE + 0x403C )
#define LEP_CID_OEM_REBOOT                      (LEP_OEM_MODULE_BASE + 0x4040 )
#define LEP_CID_OEM_FFC_NORMALIZATION_TARGET    (LEP_OEM_MODULE_BASE + 0x4044 )
#define LEP_CID_OEM_STATUS                      (LEP_OEM_MODULE_BASE + 0x4048 )
#define LEP_CID_OEM_SCENE_MEAN_VALUE            (LEP_OEM_MODULE_BASE + 0x404C )
#define LEP_CID_OEM_POWER_MODE                  (LEP_OEM_MODULE_BASE + 0x4050 )

#define LEP_CID_OEM_GPIO_MODE_SELECT            (LEP_OEM_MODULE_BASE + 0x4054 )
#define LEP_CID_OEM_GPIO_VSYNC_PHASE_DELAY      (LEP_OEM_MODULE_BASE + 0x4058 )

#define LEP_CID_OEM_USER_DEFAULTS               (LEP_OEM_MODULE_BASE + 0x405C )
#define LEP_CID_OEM_USER_DEFAULTS_RESTORE       (LEP_OEM_MODULE_BASE + 0x4060 )
#define LEP_CID_OEM_SHUTTER_PROFILE_OBJ         (LEP_OEM_MODULE_BASE + 0x4064 )
#define LEP_CID_OEM_THERMAL_SHUTDOWN_ENABLE_STATE (LEP_OEM_MODULE_BASE + 0x4068 )
#define LEP_CID_OEM_BAD_PIXEL_REPLACE_CONTROL   (LEP_OEM_MODULE_BASE + 0x406C )
#define LEP_CID_OEM_TEMPORAL_FILTER_CONTROL     (LEP_OEM_MODULE_BASE + 0x4070 )
#define LEP_CID_OEM_COLUMN_NOISE_ESTIMATE_CONTROL (LEP_OEM_MODULE_BASE + 0x4074 )
#define LEP_CID_OEM_PIXEL_NOISE_ESTIMATE_CONTROL (LEP_OEM_MODULE_BASE + 0x4078 )

#define LEP_CID_RAD_RBFO_INTERNAL               (LEP_RAD_MODULE_BASE + 0x0000 )  /* High Gain */
#define LEP_CID_RAD_RBFO_EXTERNAL               (LEP_RAD_MODULE_BASE + 0x0004 )  /* High Gain */
#define LEP_CID_RAD_DEBUG_TEMP                  (LEP_RAD_MODULE_BASE + 0x0008 )
#define LEP_CID_RAD_DEBUG_FLUX                  (LEP_RAD_MODULE_BASE + 0x000C )
#define LEP_CID_RAD_ENABLE_STATE                (LEP_RAD_MODULE_BASE + 0x0010 )
#define LEP_CID_RAD_GLOBAL_OFFSET               (LEP_RAD_MODULE_BASE + 0x0014 )
#define LEP_CID_RAD_TFPA_CTS_MODE               (LEP_RAD_MODULE_BASE + 0x0018 )
#define LEP_CID_RAD_TFPA_CTS                    (LEP_RAD_MODULE_BASE + 0x001C )
#define LEP_CID_RAD_TEQ_SHUTTER_LUT             (LEP_RAD_MODULE_BASE + 0x0020 )
#define LEP_CID_RAD_TSHUTTER_MODE               (LEP_RAD_MODULE_BASE + 0x0024 )
#define LEP_CID_RAD_TSHUTTER                    (LEP_RAD_MODULE_BASE + 0x0028 )
#define LEP_CID_RAD_RUN_FFC                     (LEP_RAD_MODULE_BASE + 0x002C )
#define LEP_CID_RAD_RUN_STATUS                  (LEP_RAD_MODULE_BASE + 0x0030 )
#define LEP_CID_RAD_RESPONSIVITY_SHIFT          (LEP_RAD_MODULE_BASE + 0x0034 )
#define LEP_CID_RAD_F_NUMBER                    (LEP_RAD_MODULE_BASE + 0x0038 )
#define LEP_CID_RAD_TAU_LENS                    (LEP_RAD_MODULE_BASE + 0x003C )
#define LEP_CID_RAD_RESPONSIVITY_VALUE_LUT      (LEP_RAD_MODULE_BASE + 0x0040 )
#define LEP_CID_RAD_GLOBAL_GAIN                 (LEP_RAD_MODULE_BASE + 0x0044 )
#define LEP_CID_RAD_RADIOMETRY_FILTER           (LEP_RAD_MODULE_BASE + 0x0048 )
#define LEP_CID_RAD_TFPA_LUT                    (LEP_RAD_MODULE_BASE + 0x004C )
#define LEP_CID_RAD_TAUX_LUT                    (LEP_RAD_MODULE_BASE + 0x0050 )
#define LEP_CID_RAD_TAUX_CTS_MODE               (LEP_RAD_MODULE_BASE + 0x0054 )
#define LEP_CID_RAD_TAUX_CTS                    (LEP_RAD_MODULE_BASE + 0x0058 )
#define LEP_CID_RAD_TEQ_SHUTTER_FLUX            (LEP_RAD_MODULE_BASE + 0x005C )
#define LEP_CID_RAD_MFFC_FLUX                   (LEP_RAD_MODULE_BASE + 0x0060 )
#define LEP_CID_RAD_FRAME_MEDIAN_VALUE          (LEP_RAD_MODULE_BASE + 0x007C )
#define LEP_CID_RAD_MLG_LUT                     (LEP_RAD_MODULE_BASE + 0x0088 )
#define LEP_CID_RAD_HOUSING_TCP                 (LEP_RAD_MODULE_BASE + 0x008C )
#define LEP_CID_RAD_SHUTTER_TCP                 (LEP_RAD_MODULE_BASE + 0x0090 )
#define LEP_CID_RAD_LENS_TCP                    (LEP_RAD_MODULE_BASE + 0x0094 )
#define LEP_CID_RAD_PREVIOUS_GLOBAL_OFFSET      (LEP_RAD_MODULE_BASE + 0x0098 )
#define LEP_CID_RAD_PREVIOUS_GLOBAL_GAIN        (LEP_RAD_MODULE_BASE + 0x009C )
#define LEP_CID_RAD_GLOBAL_GAIN_FFC             (LEP_RAD_MODULE_BASE + 0x00A0 )
#define LEP_CID_RAD_CNF_SCALE_FACTOR            (LEP_RAD_MODULE_BASE + 0x00A4 )
#define LEP_CID_RAD_TNF_SCALE_FACTOR            (LEP_RAD_MODULE_BASE + 0x00A8 )
#define LEP_CID_RAD_SNF_SCALE_FACTOR            (LEP_RAD_MODULE_BASE + 0x00AC )
#define LEP_CID_RAD_ARBITRARY_OFFSET            (LEP_RAD_MODULE_BASE + 0x00B8 )

#define LEP_CID_RAD_FLUX_LINEAR_PARAMS          (LEP_RAD_MODULE_BASE + 0x00BC )
#define LEP_CID_RAD_TLINEAR_ENABLE_STATE        (LEP_RAD_MODULE_BASE + 0x00C0 )
#define LEP_CID_RAD_TLINEAR_RESOLUTION          (LEP_RAD_MODULE_BASE + 0x00C4 )
#define LEP_CID_RAD_TLINEAR_AUTO_RESOLUTION     (LEP_RAD_MODULE_BASE + 0x00C8 )
#define LEP_CID_RAD_SPOTMETER_ROI               (LEP_RAD_MODULE_BASE + 0x00CC )
#define LEP_CID_RAD_SPOTMETER_OBJ_KELVIN        (LEP_RAD_MODULE_BASE + 0x00D0 )

#define LEP_CID_RAD_RBFO_INTERNAL_LG            (LEP_RAD_MODULE_BASE + 0x00D4 )  /* Low Gain */
#define LEP_CID_RAD_RBFO_EXTERNAL_LG            (LEP_RAD_MODULE_BASE + 0x00D8 )  /* Low Gain */

#define LEP_CID_RAD_ARBITRARY_OFFSET_MODE       (LEP_RAD_MODULE_BASE + 0x00DC )
#define LEP_CID_RAD_ARBITRARY_OFFSET_PARAMS     (LEP_RAD_MODULE_BASE + 0x00E0 )

#define LEP_CID_RAD_RADIO_CAL_VALUES            (LEP_RAD_MODULE_BASE + 0x00E4 )

#define LEP_CID_SYS_PING                        (LEP_SYS_MODULE_BASE + 0x0000 )
#define LEP_CID_SYS_CAM_STATUS                  (LEP_SYS_MODULE_BASE + 0x0004 )
#define LEP_CID_SYS_FLIR_SERIAL_NUMBER          (LEP_SYS_MODULE_BASE + 0x0008 )
#define LEP_CID_SYS_CAM_UPTIME                  (LEP_SYS_MODULE_BASE + 0x000C )
#define LEP_CID_SYS_AUX_TEMPERATURE_KELVIN      (LEP_SYS_MODULE_BASE + 0x0010 )
#define LEP_CID_SYS_FPA_TEMPERATURE_KELVIN      (LEP_SYS_MODULE_BASE + 0x0014 )
#define LEP_CID_SYS_TELEMETRY_ENABLE_STATE      (LEP_SYS_MODULE_BASE + 0x0018 )
#define LEP_CID_SYS_TELEMETRY_LOCATION          (LEP_SYS_MODULE_BASE + 0x001C )
#define LEP_CID_SYS_EXECTUE_FRAME_AVERAGE       (LEP_SYS_MODULE_BASE + 0x0020 )
#define LEP_CID_SYS_NUM_FRAMES_TO_AVERAGE       (LEP_SYS_MODULE_BASE + 0x0024 )
#define LEP_CID_SYS_CUST_SERIAL_NUMBER          (LEP_SYS_MODULE_BASE + 0x0028 )
#define LEP_CID_SYS_SCENE_STATISTICS            (LEP_SYS_MODULE_BASE + 0x002C )
#define LEP_CID_SYS_SCENE_ROI                   (LEP_SYS_MODULE_BASE + 0x0030 )
#define LEP_CID_SYS_THERMAL_SHUTDOWN_COUNT      (LEP_SYS_MODULE_BASE + 0x0034 )
#define LEP_CID_SYS_SHUTTER_POSITION            (LEP_SYS_MODULE_BASE + 0x0038 )
#define LEP_CID_SYS_FFC_SHUTTER_MODE_OBJ        (LEP_SYS_MODULE_BASE + 0x003C )
#define FLR_CID_SYS_RUN_FFC                     (LEP_SYS_MODULE_BASE + 0x0042 )
#define LEP_CID_SYS_FFC_STATUS                  (LEP_SYS_MODULE_BASE + 0x0044 )
#define LEP_CID_SYS_GAIN_MODE                   (LEP_SYS_MODULE_BASE + 0x0048 )
#define LEP_CID_SYS_FFC_STATE                   (LEP_SYS_MODULE_BASE + 0x004C )
#define LEP_CID_SYS_GAIN_MODE_OBJ               (LEP_SYS_MODULE_BASE + 0x0050 )
#define LEP_CID_SYS_GAIN_MODE_DESIRED_FLAG      (LEP_SYS_MODULE_BASE + 0x0054 )
#define LEP_CID_SYS_BORESIGHT_VALUES            (LEP_SYS_MODULE_BASE + 0x0058 )

#define LEP_CID_VID_POLARITY_SELECT         (LEP_VID_MODULE_BASE + 0x0000 )
#define LEP_CID_VID_LUT_SELECT              (LEP_VID_MODULE_BASE + 0x0004 )
#define LEP_CID_VID_LUT_TRANSFER            (LEP_VID_MODULE_BASE + 0x0008 )
#define LEP_CID_VID_FOCUS_CALC_ENABLE       (LEP_VID_MODULE_BASE + 0x000C )
#define LEP_CID_VID_FOCUS_ROI               (LEP_VID_MODULE_BASE + 0x0010 )
#define LEP_CID_VID_FOCUS_THRESHOLD         (LEP_VID_MODULE_BASE + 0x0014 )
#define LEP_CID_VID_FOCUS_METRIC            (LEP_VID_MODULE_BASE + 0x0018 )
#define LEP_CID_VID_SBNUC_ENABLE            (LEP_VID_MODULE_BASE + 0x001C )
#define LEP_CID_VID_GAMMA_SELECT            (LEP_VID_MODULE_BASE + 0x0020 )
#define LEP_CID_VID_FREEZE_ENABLE           (LEP_VID_MODULE_BASE + 0x0024 )
#define LEP_CID_VID_BORESIGHT_CALC_ENABLE   (LEP_VID_MODULE_BASE + 0x0028 )
#define LEP_CID_VID_BORESIGHT_COORDINATES   (LEP_VID_MODULE_BASE + 0x002C )
#define LEP_CID_VID_VIDEO_OUTPUT_FORMAT     (LEP_VID_MODULE_BASE + 0x0030 )
#define LEP_CID_VID_LOW_GAIN_COLOR_LUT      (LEP_VID_MODULE_BASE + 0x0034 )

---

unit:AGC register:1 length:4
unit:AGC register:2 length:4
unit:AGC register:3 length:8
unit:AGC register:4 length:8
unit:AGC register:5 length:2
unit:AGC register:6 length:2
unit:AGC register:7 length:2
unit:AGC register:8 length:2
unit:AGC register:9 length:2
unit:AGC register:10 length:2
unit:AGC register:11 length:2
unit:AGC register:12 length:2
unit:AGC register:13 length:2
unit:AGC register:14 length:2
unit:AGC register:15 length:2
unit:AGC register:16 length:2
unit:AGC register:17 length:2
unit:AGC register:18 length:4
unit:AGC register:19 length:4
unit:AGC register:20 length:2
unit:OEM register:1 length:1
unit:OEM register:2 length:1
unit:OEM register:3 length:1
unit:OEM register:4 length:1
unit:OEM register:5 length:1
unit:OEM register:6 length:2
unit:OEM register:7 length:2
unit:OEM register:8 length:32
unit:OEM register:9 length:8
unit:OEM register:10 length:4
unit:OEM register:11 length:4
unit:OEM register:12 length:4
unit:OEM register:13 length:4
unit:OEM register:14 length:4
unit:OEM register:15 length:32
unit:OEM register:16 length:2
unit:OEM register:17 length:1
unit:OEM register:18 length:2
unit:OEM register:19 length:4
unit:OEM register:20 length:2
unit:OEM register:21 length:4
unit:OEM register:22 length:4
unit:OEM register:23 length:4
unit:OEM register:24 length:4
unit:OEM register:25 length:1
unit:OEM register:26 length:4
unit:OEM register:27 length:4
unit:OEM register:28 length:4
unit:OEM register:29 length:4
unit:OEM register:30 length:4
unit:OEM register:31 length:4
unit:RAD register:1 length:16
unit:RAD register:2 length:16
unit:RAD register:3 length:2
unit:RAD register:4 length:4
unit:RAD register:5 length:4
unit:RAD register:6 length:2
unit:RAD register:7 length:4
unit:RAD register:8 length:2
unit:RAD register:9 length:256
unit:RAD register:10 length:4
unit:RAD register:11 length:2
unit:RAD register:12 length:1
unit:RAD register:13 length:4
unit:RAD register:14 length:2
unit:RAD register:15 length:2
unit:RAD register:16 length:2
unit:RAD register:17 length:256
unit:RAD register:18 length:2
unit:RAD register:19 length:2
unit:RAD register:20 length:512
unit:RAD register:21 length:512
unit:RAD register:22 length:4
unit:RAD register:23 length:2
unit:RAD register:24 length:4
unit:RAD register:25 length:4
unit:RAD register:26 length:2
unit:RAD register:27 length:2
unit:RAD register:28 length:2
unit:RAD register:29 length:2
unit:RAD register:30 length:2
unit:RAD register:31 length:2
unit:RAD register:32 length:2
unit:RAD register:33 length:2
unit:RAD register:34 length:2
unit:RAD register:35 length:256
unit:RAD register:36 length:8
unit:RAD register:37 length:8
unit:RAD register:38 length:8
unit:RAD register:39 length:2
unit:RAD register:40 length:2
unit:RAD register:41 length:2
unit:RAD register:42 length:2
unit:RAD register:43 length:2
unit:RAD register:44 length:2
unit:RAD register:45 length:2
unit:RAD register:46 length:2
unit:RAD register:47 length:2
unit:RAD register:48 length:16
unit:RAD register:49 length:4
unit:RAD register:50 length:4
unit:RAD register:51 length:4
unit:RAD register:52 length:8
unit:RAD register:53 length:2
unit:RAD register:54 length:16
unit:RAD register:55 length:16
unit:RAD register:56 length:4
unit:RAD register:57 length:4
unit:RAD register:58 length:8
unit:SYS register:1 length:1
unit:SYS register:2 length:8
unit:SYS register:3 length:8
unit:SYS register:4 length:4
unit:SYS register:5 length:2
unit:SYS register:6 length:2
unit:SYS register:7 length:4
unit:SYS register:8 length:4
unit:SYS register:9 length:1
unit:SYS register:10 length:4
unit:SYS register:11 length:32
unit:SYS register:12 length:8
unit:SYS register:13 length:8
unit:SYS register:14 length:2
unit:SYS register:15 length:4
unit:SYS register:16 length:32
unit:SYS register:17 length:2
unit:SYS register:18 length:4
unit:SYS register:19 length:4
unit:SYS register:20 length:4
unit:SYS register:21 length:28
unit:SYS register:22 length:4
unit:SYS register:23 length:12
unit:VID register:1 length:4
unit:VID register:2 length:4
unit:VID register:3 length:1024
unit:VID register:4 length:4
unit:VID register:5 length:8
unit:VID register:6 length:4
unit:VID register:7 length:4
unit:VID register:8 length:4
unit:VID register:9 length:2
unit:VID register:10 length:4
unit:VID register:11 length:4
unit:VID register:12 length:32
unit:VID register:13 length:4
unit:VID register:14 length:4
"""

def parse_unit_reg(unit_reg_id):
  p = re.compile("LEP_CID_([a-zA-Z0-9]+)_(\w+)")
  match = p.findall(unit_reg_id)
  if len(match) == 0:
    return (None, None)
  unit, reg = match[0]
  return (unit, reg)

def parse_registers(register_definitions):
  registers = []
  lengths = { "AGC": {}, "OEM": {}, "RAD": {}, "SYS": {}, "VID": {} }
  p = re.compile("define\s+(\w+)\s+\(\w+\W+(\S+)")
  p2 = re.compile("unit:(\w+)\s+register:(\d+)\s+length:(\d+)")
  for line in register_definitions.split('\n'):
    match = p.findall(line)
    match2 = p2.findall(line)

    if len(match) > 0:
      const, value = match[0]
      value = ((int(value, 0) >> 2) & 0xFF) + 1
      registers += [(const, value)]

    if len(match2) > 0:
      unit, register, length = match2[0]
      lengths[unit][register] = length

  return registers, lengths

def unit_offset(unit):
  if unit == "AGC":
    return 0
  elif unit == "OEM":
    return 1
  elif unit == "RAD":
    return 2
  elif unit == "SYS":
    return 3
  elif unit == "VID":
    return 4
  else:
    return 5

def format_constant(const, value):
  unit,reg = parse_unit_reg(const)
  offset = unit_offset(unit)
  return """
		<constant type="integer">
			<id>XU_{0}</id>
			<value>{1}</value>
		</constant>
		<constant type="integer">
			<id>V4L2_{0}</id>
			<value>0x{2:08x}</value>
		</constant>""".format(const, value, 0x08000000 + (offset << 16) + value)

def format_constants(registers):
  for register in registers:
    print(format_constant(*register))

def unit_to_entity(unit):
  return "UVC_GUID_LEP_{0}_ID_CONTROL".format(unit)

def format_control(register, lengths):
  unit_reg_id, value = register
  p = re.compile("LEP_CID_([a-zA-Z0-9]+)_(\w+)")
  match = p.findall(unit_reg_id)
  if len(match) == 0:
    return ""
  unit, reg = match[0]
  entity = unit_to_entity(unit)
  length = int(lengths[unit][str(value)])
  if length > 8:
    requests = """
						<request>SET_CUR</request>
						<request>GET_CUR</request>"""
  elif length == 1:
    requests = """
						<request>SET_CUR</request>
						<request>GET_CUR</request>"""
  else:
    requests = """
						<request>SET_CUR</request>
						<request>GET_CUR</request>
						<request>GET_MIN</request>
						<request>GET_MAX</request>
						<request>GET_RES</request>"""

  return """
				<control id="{0}_{1}">
					<entity>{2}</entity>
					<selector>XU_{3}</selector>
					<index>{4}</index>
					<size>{5}</size>
					<requests>{6}
					</requests>
					<description>
						Get/Set {0} module register {1}
					</description>
				</control>""".format(unit, reg, entity, unit_reg_id, (unit_offset(unit) << 16) + (value - 1), length, requests)

def format_controls(registers, lengths):
  for register in registers:
    print(format_control(register, lengths))


def format_mapping(register, lengths):
  unit_reg_id, value = register
  p = re.compile("LEP_CID_([a-zA-Z0-9]+)_(\w+)")
  match = p.findall(unit_reg_id)
  if len(match) == 0:
    return ""
  unit, reg = match[0]
  entity = unit_to_entity(unit)
  length = int(lengths[unit][str(value)])
  if length > 8:
    uvc_type = "UVC_CTRL_DATA_TYPE_RAW"
    v4l2_type = "V4L2_CTRL_TYPE_STRING"
  elif length == 1:
    uvc_type = "UVC_CTRL_DATA_TYPE_RAW"
    v4l2_type = "V4L2_CTRL_TYPE_BUTTON"
  else:
    uvc_type = "UVC_CTRL_DATA_TYPE_RAW"
    v4l2_type = "V4L2_CTRL_TYPE_INTEGER"
    length = length * 8
  return """
		<mapping>
			<name>{3}</name>
			<uvc>
				<control_ref idref="{0}_{1}"/>
				<size>{5}</size>
				<offset>0</offset>
				<uvc_type>{6}</uvc_type>
			</uvc>
			<v4l2>
				<id>V4L2_{3}</id>
				<v4l2_type>{7}</v4l2_type>
			</v4l2>
		</mapping>""".format(unit, reg, entity, unit_reg_id, value, length, uvc_type, v4l2_type)

def format_mappings(registers, lengths):
  for register in registers:
    print(format_mapping(register, lengths))


def main():
  registers,lengths = parse_registers(INPUT_REGISTER_DEFINITIONS)
  print("""<?xml version="1.0" encoding="UTF-8"?>

<config version="1.0"
	xmlns="http://groupgets.com"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://groupgets.com uvcconfig.xsd"
>

	<meta>
		<version>3.3.13</version>
		<author>GetLab</author>
		<contact>contact@groupgets.com</contact>
		<revision>2</revision>
		<copyright>Copyright (c) GroupGets 2017 </copyright>
		<history>
		  PureThermal 1 FLIR Lepton CCI XU control interface
		</history>
	</meta>

	<constants>

		<constant type="guid">
			<id>UVC_GUID_LEP_AGC_ID_CONTROL</id>
			<value>2d317470-656c-2d70-6167-632d30303030</value>
		</constant>

		<constant type="guid">
			<id>UVC_GUID_LEP_OEM_ID_CONTROL</id>
			<value>2d317470-656c-2d70-6f65-6d2d30303030</value>
		</constant>

		<constant type="guid">
			<id>UVC_GUID_LEP_RAD_ID_CONTROL</id>
			<value>2d317470-656c-2d70-7261-642d30303030</value>
		</constant>

		<constant type="guid">
			<id>UVC_GUID_LEP_SYS_ID_CONTROL</id>
			<value>2d317470-656c-2d70-7379-732d30303030</value>
		</constant>

		<constant type="guid">
			<id>UVC_GUID_LEP_VID_ID_CONTROL</id>
			<value>2d317470-656c-2d70-7669-642d30303030</value>
		</constant>
""")

  format_constants(registers)

  print("""
	</constants>
	
	<devices>
		<device>
			<match>
				<vendor_id>0x1e4e</vendor_id> 
				<product_id>0x0100</product_id>
			</match>

			<controls>""")

  format_controls(registers,lengths)

  print("""
			</controls>
		</device>
	</devices>

	<!-- V4L2 mappings for the UVC controls defined above -->
	<mappings>""")

  format_mappings(registers,lengths)

  print("""
	</mappings>
</config>
""")

if __name__ == '__main__':
  main()
