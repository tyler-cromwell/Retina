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
print('Importing standard libraries...')
import configparser
import re
import sys
import time
import tkinter

""" OpenCV library """
print('Importing OpenCV...')
import cv2

""" Global constants """
CAMERA_DEFAULT = 0

""" Global variables """
config = None
faceCascade = cv2.CascadeClassifier(sys.argv[2])


"""
Searches for faces in the given frame.
"""
def detectFaces(frame, scaleFactor, minNeighbors, minSize, maxSize):
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        grayscale,
        scaleFactor = scaleFactor,
        minNeighbors = minNeighbors,
        flags = 0,
        minSize = tuple(map(int, minSize)),
        maxSize = tuple(map(int, maxSize))
    )

    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.putText(frame, 'Unknown Face %d' % i, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

    return faces


"""
Main "function".
"""
if __name__ == '__main__':
    flags = 0
    windowName = 'Camera %d' % (CAMERA_DEFAULT)

    """ Parse face detection options """
    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    width = int(config.get('Faces', 'width'))
    height = int(config.get('Faces', 'height'))
    scaleFactor = float(config.get('Faces', 'scaleFactor'))
    minNeighbors = int(config.get('Faces', 'minNeighbors'))
    minSize = re.split('\s*,\s*', config.get('Faces', 'minSize'))
    maxSize = re.split('\s*,\s*', config.get('Faces', 'maxSize'))

    """ Set camera resolution """
    camera = cv2.VideoCapture(CAMERA_DEFAULT)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    print('Capture Resolution: %dx%d' %
        (camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )

    """ Get screen resolution """
    tk = tkinter.Tk()
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()

    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(windowName, (screen_width - width) // 2, 0)
    
    if not camera.isOpened():
        camera.open(CAMERA_DEFAULT)

    while True:
        start = time.time()
        retval, frame = camera.read()

        """ Check flags """
        if flags & 1:
            detectFaces(frame, scaleFactor, minNeighbors, minSize, maxSize)

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
