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

#### pt1-v4l2-grab

Shows how to grab frames from video stream, saves 20 of them to disk in ppm format

### python

#### opencv-capture.py

Basic video capture from the Pure Thermal 1 with the `cv2.VideoCapture` module
