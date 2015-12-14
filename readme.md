# PureThermal 1 USB Host Examples

The [PureThermal 1 FLIR Lepton development board](https://groupgets.com/manufacturers/groupgets-labs/products/pure-thermal-1-flir-lepton-dev-kit)
by GroupGets supports USB video, and this makes it very easy to capture thermal imaging data from a host PC
using standardard tools and libraries. If you want to prototype quickly, your application demands increasing
processing power, or you simply don't want to hack on the firmware, check out these examples to get started.


## *NOTE* Linux (< 4.0) + V4L (and OpenCV) ##

Linux Kernel versions less than 4.0 don't match the UVC format `UVC_GUID_FORMAT_BGR3` with `V4L2_PIX_FMT_BGR24`.
Applications that use libv4l and depend on the BGR24 format (such as the `VideoCapture` module of OpenCV) will not
be able to use this format. Instead, they will use software scaling to convert RGB565 into RGB24/BRG24, at a
loss in color resolution and with expense to CPU.


## gstreamer (Linux)

No code is required to run this. If you need to install gstreamer:

    sudo apt-get install gstreamer1.0-tools gstreamer1.0-plugins-ugly gstreamer1.0-plugins-bad

To view a live preview:

    gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,format=UYVY \
    videoscale ! video/x-raw,width=640,height=480 ! videoconvert ! ximagesink

Note that you can change the format, width, and height as desired. As an exercise for the reader,
gstreamer can also be used to record a video and stills.


## guvcview (Linux)

guvcview is a simple USB webcam viewer for linux, and is a great way to test the different format and
control capabilities of the PureThermal 1.

    sudo apt-get install guvcview

Then just run:

    guvcview


## Python (OS X, Windows, Linux)

### opencv-capture.py

Basic video capture from the Pure Thermal 1 with the `cv2.VideoCapture` module.

See note above for Linux + V4L + OpenCV compatibility.


## C + V4L2 (Linux)

If you don't already have them, install development tools. For Ubuntu, that looks like this:

    sudo apt-get install autotools-dev autoconf build-essential

You'll also want a few support libraries for V4L:

    sudo apt-get install libv4l-dev v4l-utils

Then:

    cd linux
    ./autogen.sh
    ./configure
    make

### pt1-v4l2-grab

Shows how to grab frames from video stream, saves 20 of them to disk in ppm format


