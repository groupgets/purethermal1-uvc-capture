# Pure Thermal 1 Examples

## Linux + V4L2

If you don't already have them, install development tools. For Ubuntu, that looks like this:

    sudo apt-get install autotools-dev autoconf build-essential

Then run:

    ./autogen.sh
    ./configure
    make

And optionally:

    make install

### pt1-v4l2-grab

Shows how to grab frames from video stream, saves 20 of them to disk in ppm format


## Linux + gstreamer

In fact no code is required to run this. If you need to install gstreamer:

    sudo apt-get install gstreamer1.0-tools gstreamer1.0-plugins-ugly gstreamer1.0-plugins-bad

To view a live preview:

    gst-launch-1.0 v4l2src device=/dev/video0 ! videoscale ! video/x-raw,width=640,height=480 ! videoconvert ! ximagesink

Note that you can change the width and height as desired. As an exercise for the reader,
gstreamer can also be used to record a video and stills.


## NOTE: Linux (< 4.0) + V4L + OpenCV

Linux Kernel versions less than 4.0 don't match the UVC format `UVC_GUID_FORMAT_BGR3` with `V4L2_PIX_FMT_BGR24`.
Applications that use libv4l and depend on the BGR24 format (such as the `VideoCapture` module of OpenCV) will not
be able to use this format. Instead, they will use software scaling to convert RGB565 into RGB24/BRG24, at a
loss in color resolution and with expense to CPU.


## Python

### opencv-capture.py

Basic video capture from the Pure Thermal 1 with the `cv2.VideoCapture` module.

See note above for Linux + V4L + OpenCV compatibility.
