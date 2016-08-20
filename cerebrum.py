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
import numpy
from PIL import Image
import cv2

""" Local modules """
from modules import camera
from modules import misc
from modules import opt
from modules import recognizer

""" Global constants """
CAMERA_DEFAULT = 0


"""
Ensures the recognizer given by 'path' exists
"""
def opt_label(label):
    if os.path.isfile(sys.path[0] +'/data/recognizers/'+ label +'.lbph.xml'):
        return label
    else:
        return None


"""
Displays program usage information.
"""
def print_usage():
    print('Usage:\t./cerebrum.py [--classifier=PATH] [--image=PATH] --label=NAME [--settings=NAME]')
    print('  --help\t\tPrints this text')
    print('  --classifier=PATH\tThe absolute path of a Face Detection classifier (Optional)')
    print('  --image=PATH\t\tPath to a still image (alternative to camera stream)')
    print('  --label=NAME\t\tThe name of the person\'s face to recognize')
    print('  --settings=NAME\tThe name of a file located under \'settings/\'')
    print('      See \'settings/\', without \'.txt\' extension')
    exit(0)


"""
Main function.
"""
def main():
    flags = 0
    windowName = 'Camera %d' % (CAMERA_DEFAULT)
    faceClassifier = None
    img = None
    label = None
    settings = opt.map_settings()
    key = opt.default_settings()

    """ Parse command-line arguments """
    try:
        short_opts = ['']
        long_opts = ['help', 'classifier=', 'image=', 'label=', 'settings=']
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
            faceClassifier = opt.classifier(a)
        elif o == '--image':
            img = a
        elif o == '--label':
            label = opt_label(a)
        elif o == '--settings':
            key = a

    if not label:
        print('\n  Label not specified!\n')
        print_usage()
    elif not key in settings.keys():
        print('\n  Settings not specified!\n')
        print_usage()

    """ Setup objects and window """
    displayWidth, displayHeight = misc.get_display_resolution()
    print('Display resolution: %dx%d' % (displayWidth, displayHeight))

    faceRecognizer = recognizer.Recognizer(faceClassifier, label, settings[key])
    stream = camera.Camera(CAMERA_DEFAULT, settings[key])
    print('Capture resolution: %dx%d' % (stream.getWidth(), stream.getHeight()))

    """ Recognize in a still image """
    if img:
        image, labels, objects, confidences = faceRecognizer.recognizeFromFile(img)

        for i, (x, y, w, h) in enumerate(objects):
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)
            cv2.putText(image, labels[i].title() +' ('+ confidences[i] +')', (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
            cv2.putText(image, '%dx%d' % (w, h), (x, y+h+13), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

        cv2.imshow(img, image)
        cv2.waitKey(0)
        return

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
        if flags & 4:
            labels, objects, confidences = faceRecognizer.recognize(frame)

            for i, (x, y, w, h) in enumerate(objects):
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                cv2.putText(frame, labels[i].title() +' ('+ confidences[i] +')', (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
                cv2.putText(frame, '%dx%d' % (w, h), (x, y+h+13), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

        if flags & 1:
            frame = cv2.bilateralFilter(frame, 5, 60, 60)

        if flags & 8:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if flags & 2:
                frame = cv2.equalizeHist(frame)

        end = time.time()
        fps = 1 // (end - start)

        cv2.putText(frame, 'FPS: [%d]' % (fps), (0, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.imshow(windowName, frame)

        key = cv2.waitKey(1)

        """ Determine action """
        if key == 27:
            cv2.destroyWindow(windowName)
            cv2.waitKey(1); cv2.waitKey(1);
            cv2.waitKey(1); cv2.waitKey(1);
            stream.release()
            break
        elif key == ord('b'):
            flags = flags ^ 1
        elif key == ord('e'):
            flags = flags ^ 2
        elif key == ord('f'):
            flags = flags ^ 4
        elif key == ord('g'):
            flags = flags ^ 8


"""
Program entry.
"""
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
