#!/usr/bin/env python

"""
CV2 video capture example from Pure Thermal 1
"""

try:
    import cv2
except ImportError:
    print "ERROR python-opencv must be installed"
    exit(1)

class OpenCvCapture(object):
    """
    Encapsulate state for capture from Pure Thermal 1 with OpenCV
    """

    def __init__(self):
        # capture from the LAST camera in the system
        # presumably, if the system has a built-in webcam it will be the first
        for i in reversed(range(10)):
            print "Testing for presense of camera #{0}...".format(i)
            cv2_cap = cv2.VideoCapture(i)
            if cv2_cap.isOpened():
                break

        if not cv2_cap.isOpened():
            print "Camera not found!"
            exit(1)

        self.cv2_cap = cv2_cap

    def show_video(self):
        """
        Run loop for cv2 capture from lepton
        """

        cv2.namedWindow("lepton", cv2.WINDOW_NORMAL)
        print "Running, ESC or Ctrl-c to exit..."
        while True:
            ret, img = self.cv2_cap.read()

            if ret == False:
                print "Error reading image"
                break

            cv2.imshow("lepton", cv2.resize(img, (640, 480)))
            if cv2.waitKey(5) == 27:
                break

        cv2.destroyAllWindows()

if __name__ == '__main__':
    OpenCvCapture().show_video()
