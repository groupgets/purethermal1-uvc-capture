# Pure Thermal 1 Examples

## Getting started

If you don't already have them, install development tools. For Ubuntu, that looks like this:

    sudo apt-get install autotools-dev autoconf build-essential

Then run:

    ./autogen.sh
    ./configure
    make

And optionally:

    make install

## examples

### linux

#### gstreamer

No code is required to run this. If you need to install gstreamer:

    sudo apt-get install gstreamer1.0-tools gstreamer1.0-plugins-ugly gstreamer1.0-plugins-bad

To view a live preview:

    gst-launch-1.0 v4l2src device=/dev/video0 ! videoscale ! video/x-raw,width=640,height=480 ! videoconvert ! ximagesink

Note that you can change the width and height as desired. As an exercise for the reader,
gstreamer can also be used to record a video and stills.

#### pt1-v4l2-grab

Shows how to grab frames from video stream, saves 20 of them to disk in ppm format

### python

#### opencv-capture.py

Basic video capture from the Pure Thermal 1 with the `cv2.VideoCapture` module
