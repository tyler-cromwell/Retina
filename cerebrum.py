#!/usr/bin/python3

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  Copyright (C) 2016 Tyler Cromwell <tyler@csh.rit.edu>

  This file is part of Cerebrum.

  Cerebrum is free software: you can redistribute it and/or modify
  it under Version 2 of the terms of the GNU General Public License
  as published by the Free Software Foundation.

  Cerebrum is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY of FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with Cerebrum.
  If not, see <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Python libraries """
import getopt
import os
import sys
import time
import tkinter

""" External libraries """
import cv2

""" Local modules """
from modules import detector
from modules import misc

""" Global constants """
CAMERA_DEFAULT = 0
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


"""
Returns the path of the classifier file.
"""
def opt_classifier(arg):
    if os.path.isfile(arg):
        return arg
    else:
        print('Invalid classifier: '+ arg)
        exit(1)


"""
Returns the path of the settings file.
"""
def opt_settings(arg):
    if os.path.isfile(ROOT_DIR +'/settings/'+ arg +'.txt'):
        return ROOT_DIR +'/settings/'+ arg +'.txt'
    else:
        print('Invalid machine settings: '+ arg)
        exit(1)


"""
Displays program usage information.
"""
def print_usage():
    print('Usage:\t./cerebrum.py --classifier=PATH --settings=MACHINE')
    print('  --help\t\tPrints this text')
    print('  --classifier=PATH\tThe path to a Face Detection classifier')
    print('  --settings=MACHINE\tA file located under \'settings/\' (no extension)')
    exit(0)


"""
Main function.
"""
def main():
    flags = 0
    windowName = 'Camera %d' % (CAMERA_DEFAULT)
    faceClassifier = None
    settings = None

    """ Parse command-line arguments """
    try:
        short_opts = ['']
        long_opts = ['help', 'classifier=', 'settings=']
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as error:
        print('Invalid argument: \''+ str(error) +'\'\n')
        print_usage()

    if len(opts) == 0:
        print_usage()

    for o, a, in opts:
        if o == '--help':
            print_usage()
        elif o == '--classifier':
            faceClassifier = opt_classifier(a)
        elif o == '--settings':
            settings = opt_settings(a)

    """ Initialize face detector """
    faceDetector = detector.Detector(faceClassifier, settings)
    width = faceDetector.get_width()
    height = faceDetector.get_height()

    """ Get screen resolution """
    displayWidth, displayHeight = misc.get_display_resolution()
    print('Display resolution: %dx%d' % (displayWidth, displayHeight))

    """ Set camera resolution """
    camera = cv2.VideoCapture(CAMERA_DEFAULT)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    print('Capture Resolution: %dx%d' %
        (camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )

    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(windowName, (displayWidth - width) // 2, 0)

    """ Begin using the camera """
    if not camera.isOpened():
        if not camera.open(CAMERA_DEFAULT):
            print('Failed to open Camera', CAMERA_DEFAULT)
            exit(1)

    while True:
        start = time.time()
        retval, frame = camera.read()

        """ Check flags """
        if flags & 1:
            faceDetector.detect(frame)

        end = time.time()
        fps = 1 // (end - start)

        print('FPS: %d\r' % (fps), end='')
        cv2.imshow(windowName, frame)

        key = cv2.waitKey(1)

        """ Determine action """
        if key == 27:
            cv2.destroyWindow(windowName)
            cv2.waitKey(1); cv2.waitKey(1);
            cv2.waitKey(1); cv2.waitKey(1);
            camera.release()
            break
        elif key == ord('f'):
            flags = flags ^ 1


"""
Program entry.
"""
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
