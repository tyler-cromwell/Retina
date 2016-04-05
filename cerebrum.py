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
from modules import camera
from modules import misc
from modules import opt
from modules import recognizer

""" Global constants """
CAMERA_DEFAULT = 0
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


"""
Displays program usage information.
"""
def print_usage():
    print('Usage:\t./cerebrum.py --classifier=PATH --label=NAME --settings=MACHINE')
    print('  --help\t\tPrints this text')
    print('  --classifier=PATH\tThe path to a Face Detection classifier')
    print('  --label=NAME\t\tThe name of the person\'s face to recognize')
    print('  --settings=MACHINE\tA file located under \'settings/\' (no extension)')
    exit(0)


"""
Main function.
"""
def main():
    flags = 0
    windowName = 'Camera %d' % (CAMERA_DEFAULT)
    faceClassifier = None
    label = None
    settings = None

    """ Parse command-line arguments """
    try:
        short_opts = ['']
        long_opts = ['help', 'classifier=', 'label=', 'settings=']
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
            faceClassifier = opt.opt_classifier(a)
        elif o == '--label':
            label = a
        elif o == '--settings':
            settings = opt.opt_settings(ROOT_DIR, a)

    """ Setup objects and window """
    displayWidth, displayHeight = misc.get_display_resolution()
    print('Display resolution: %dx%d' % (displayWidth, displayHeight))

    faceRecognizer = recognizer.Recognizer(faceClassifier, label, settings)
    stream = camera.Camera(CAMERA_DEFAULT, settings)
    print('Capture Resolution: %dx%d' % (stream.getWidth(), stream.getHeight()))

    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(windowName, (displayWidth - stream.getWidth()) // 2, 0)

    """ Begin using the camera """
    if not stream.isOpened():
        if not stream.open(CAMERA_DEFAULT):
            print('Failed to open Camera', CAMERA_DEFAULT)
            exit(1)

    while True:
        start = time.time()
        retval, frame = stream.read()

        """ Check flags """
        if flags & 1:
            labels, objects = faceRecognizer.recognize(frame)

            for i, (x, y, w, h) in enumerate(objects):
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                cv2.putText(frame, labels[i], (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

        end = time.time()
        fps = 1 // (end - start)

        print('FPS: [%d]\r' % (fps), end='')
        cv2.imshow(windowName, frame)

        key = cv2.waitKey(1)

        """ Determine action """
        if key == 27:
            cv2.destroyWindow(windowName)
            cv2.waitKey(1); cv2.waitKey(1);
            cv2.waitKey(1); cv2.waitKey(1);
            stream.release()
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
