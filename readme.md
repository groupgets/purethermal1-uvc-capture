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

    gst-launch-1.0 v4l2src device=/dev/video0 ! xvimagesink

If you wish to use fixed scaling, you can use the `videoscale` element and leverage the
lighter-weight `ximagesink`:

    gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,format=UYVY \
    ! videoscale ! video/x-raw,width=640,height=480 ! videoconvert ! ximagesink

The PureThermal1 can natively capture with the following raw types (and a few more):

    video/x-raw,format=BGR    *Note that libv4l2 will emulate this type on Linux < 4.0
    video/x-raw,format=RGB16
    video/x-raw,format=GRAY8
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
