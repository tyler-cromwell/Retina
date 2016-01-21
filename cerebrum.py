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

print('Importing libraries...')

""" Python libraries """
import configparser
import re
import readline
import sys

""" OpenCV library """
import cv2

""" Readline settings """
readline.parse_and_bind('tab: complete')

""" Global variables """
config = None


def detectFaces(frame):
    faceCascade = cv2.CascadeClassifier(sys.argv[2])
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces_minSize = re.split('\s*,\s*', config.get('Faces', 'minSize'))
    faces_maxSize = re.split('\s*,\s*', config.get('Faces', 'maxSize'))

    faces = faceCascade.detectMultiScale(
        grayscale,
        scaleFactor = float(config.get('Faces', 'scaleFactor')),
        minNeighbors = int(config.get('Faces', 'minNeighbors')),
        flags = 0,
        minSize = tuple(map(int, faces_minSize)),
        maxSize = tuple(map(int, faces_maxSize))
    )

    if len(faces) > 1:
        print(len(faces), 'faces found')

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'Face', (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        print('face of size ('+ str(w) +'x'+ str(h) +') found at ('+ str(x) +', '+ str(y) +')')

    return faces


def stream():
    flags = 0
    windowName = 'Camera 0'

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(config.get('Faces', 'width')))
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(config.get('Faces', 'height')))

    print('Capture Resolution: '+
        str(int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))) +'x'+
        str(int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    )

    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
    
    if not camera.isOpened():
        camera.open(0)

    while True:
        retval, frame = camera.read()

        """ Check flags """
        if flags & 1:
            detectFaces(frame)

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


if __name__ == '__main__':
    try:
        config = configparser.ConfigParser()
        config.read(sys.argv[1])

        print('Type \'help\' for information')

        while True:
            user_input = input('cerebrum> ')

            if user_input == 'help':
                print('Commands:')
                print('  exit: exits the program')
                print('  quit: exits the program')
                print('  stream: opens a video stream')

            elif user_input == 'exit' or user_input == 'quit':
                break

            elif user_input == 'stream':
                stream()

            else:
                print('Unknown command: \"'+ user_input +'\"')

    except EOFError:
        print()
    except KeyboardInterrupt:
        print()
