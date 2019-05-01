# PureThermal UVC Capture Examples

The [PureThermal 1 FLIR Lepton development board](https://groupgets.com/manufacturers/groupgets-labs/products/pure-thermal-1-flir-lepton-dev-kit)
by GroupGets supports the USB video class (UVC), and this makes it very easy to capture thermal imaging data
from a host PC using standard tools and libraries. If you want to prototype quickly, your application demands
increasing processing power, or you simply don't want to hack on the firmware, check out these examples to get started.

[PureThermal 2](https://groupgets.com/manufacturers/getlab/products/purethermal-2-flir-lepton-smart-i-o-module) is
an evolution of the PureThermal 1 board, in a more embeddable package and including the ability to update device
firmware over USB. All host-side code leveraging the PureThermal 1 is also compatible with the PureThermal 2.


## *NOTE* Linux (< 4.0) + V4L (and OpenCV) ##

Linux Kernel versions less than 4.0 don't match the UVC format `UVC_GUID_FORMAT_BGR3` with `V4L2_PIX_FMT_BGR24`.
Applications that use libv4l and depend on the BGR24 format (such as the `VideoCapture` module of OpenCV) will not
be able to use this format. Instead, they will use software scaling to convert RGB565 into RGB24/BRG24, at a
loss in color resolution and with expense to CPU.


## gstreamer (Linux)

No code is required to run this. If you need to install gstreamer:

    sudo apt-get install gstreamer1.0-tools gstreamer1.0-plugins-ugly gstreamer1.0-plugins-bad

To view a live preview:

    gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! xvimagesink

If you wish to use fixed scaling, you can use the `videoscale` element and leverage the
lighter-weight `ximagesink`:

    gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,format=UYVY \
    ! videoscale ! video/x-raw,width=640,height=480 ! videoconvert ! ximagesink

The PureThermal1 can natively capture with the following raw types (and a few more):

    video/x-raw,format=BGR    *Note that libv4l2 will emulate this type on Linux < 4.0
    video/x-raw,format=RGB16
    video/x-raw,format=GRAY8
    video/x-raw,format=GRAY16_LE   *RAW IR data, won't look like much on screen due to large range
    video/x-raw,format=UYVY

Gstreamer is very powerful and can be used to record video and stills, and even stream to remote
network locations!


## guvcview (Linux)

guvcview is a simple USB webcam viewer for linux, and is a great way to test the different format and
control capabilities of the PureThermal 1.

    sudo apt-get install guvcview

Then just run:

    guvcview


## AVFoundation (OS X)

### PT1Recorder

Video preview and capture example leveraging AVFoundation on OS X.

Build this example using XCode on OS X, `PT1Recorder.xcodeproj`


## MediaFoundation (Windows)

This example shows how to interact with a PureThermal board using the Windows SDK.

* Read UVC extension unit (e.g. Lepton serial number or part number)
* Write UVC extension unit (e.g. command FFC)
* Demonstrate selection and acquisition of Y16 data type
* Demonstrate use of telemetry data

To build this example, you'll need the [Windows 10 SDK](https://developer.microsoft.com/en-US/windows/downloads/windows-10-sdk) and Microsoft Visual Studio. Note that if you have a different version of the SDK installed, you may need to right-click the solution and select the Retarget Solution, or modify the project properties.

Note that in order for the telemetry features to work, you'll need to have the PureThermal firmware version must be 1.2.2 or greater.


## Python (OS X, Windows, Linux)

    cd python

### opencv-capture.py

Basic video capture from the Pure Thermal 1 with the `cv2.VideoCapture` module.

Install `python-opencv` if you do not have it already:

    sudo apt-get install python-opencv

Run the example:

    ./opencv-capture.py

See note above for Linux + V4L + OpenCV compatibility.

### uvc-deviceinfo.py

This example uses ctypes to hook into `libuvc` to show a cross-platform way of accessing CCI over USB extensions.

You'll need the modified version of `libuvc` from [groupgets/libuvc](https://github.com/groupgets/libuvc).

    git clone https://github.com/groupgets/libuvc
    cd libuvc
    mkdir build
    cd build
    cmake ..
    make && sudo make install

If you don't want to install this system-wide, you can copy the shared library to your working directory.

Then run the example:

    ./uvc-deviceinfo.py

The example prints the Lepton's software and hardware version information.

### uvc-radiometry.py

This example uses ctypes to hook into `libuvc` and circumvents the troubles associated with using OS camera
capture drivers, particularly on Mac OS X, whose standard capture drivers do not support the Y16 data type
for grabbing raw sensor data.

This example leverages the Radiometric Lepton 2.5. The same approach can of course modified to support other Leptons as well.

You'll need the modified version of `libuvc` from [groupgets/libuvc](https://github.com/groupgets/libuvc).

    git clone https://github.com/groupgets/libuvc
    cd libuvc
    mkdir build
    cd build
    cmake ..
    make && sudo make install

If you don't want to install this system-wide, you can copy the shared library to your working directory.

Then run the example:

    ./uvc-radiometry.py

## C + V4L2 (Linux)

If you don't already have them, install development tools. For Ubuntu, that looks like this:

    sudo apt-get install autotools-dev autoconf build-essential

You'll also want a few support libraries for V4L:

    sudo apt-get install libv4l-dev v4l-utils

Then:

    cd v4l2
    ./autogen.sh
    ./configure
    make

### pt1-v4l2-grab

Shows how to grab frames from video stream, saves 20 of them to disk in ppm format

    grab/pt1-v4l2-grab


### uvcdynctrl

This code sets up v4l2 controls for Lepton CCI with UVC extension units with libwebcam/uvcdynctrl.

First install uvcdynctrl:

    sudo apt-get install uvcdynctrl

Now you can load the control definition file:

    cd uvcdynctrl
    uvcdynctrl -v -d /dev/video0 -i pt1.xml

You can now alter Lepton CCI functions using the standard V4L2 APIs. Guvcview is a quick way to try out some of these controls.

List all controls available:

    v4l2-ctl -l

                         brightness 0x00980900 (int)    : min=0 max=255 step=1 default=128 value=128
                           contrast 0x00980901 (int)    : min=0 max=255 step=1 default=128 value=128
           lep_cid_agc_enable_state 0x08000001 (int)    : min=0 max=1 step=1 default=0 value=1
                 lep_cid_agc_policy 0x08000002 (int)    : min=0 max=1 step=1 default=0 value=1
    lep_cid_agc_histogram_clip_perc 0x08000005 (int)    : min=0 max=65535 step=1 default=0 value=0
    lep_cid_agc_histogram_tail_size 0x08000006 (int)    : min=0 max=65535 step=1 default=0 value=0
        lep_cid_agc_linear_max_gain 0x08000007 (int)    : min=0 max=65535 step=1 default=0 value=1
        lep_cid_agc_linear_midpoint 0x08000008 (int)    : min=0 max=65535 step=1 default=0 value=128
    lep_cid_agc_linear_dampening_fa 0x08000009 (int)    : min=0 max=65535 step=1 default=0 value=100
    lep_cid_agc_heq_dampening_facto 0x0800000a (int)    : min=0 max=65535 step=1 default=0 value=0
           lep_cid_agc_heq_max_gain 0x0800000b (int)    : min=0 max=65535 step=1 default=0 value=1
    lep_cid_agc_heq_clip_limit_high 0x0800000c (int)    : min=0 max=65535 step=1 default=0 value=19200
     lep_cid_agc_heq_clip_limit_low 0x0800000d (int)    : min=0 max=65535 step=1 default=0 value=512
    ...

Set a control, for example select a color palette:

    v4l2-ctl -c lep_cid_vid_lut_select=1

Take a look at the Lepton SDK header files for the meanings of enumeration values.
