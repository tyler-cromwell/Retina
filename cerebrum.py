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

import readline
import sys
import cv2

readline.parse_and_bind('tab: complete')

def detectFaces(frame):
    faceCascade = cv2.CascadeClassifier(sys.argv[1])
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        grayscale,
        scaleFactor = 1.5,
        minNeighbors = 3,
        minSize = (64, 64),
        flags = 0
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return faces


def stream(camera):
    print('Capture Resolution: '+
        str(int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))) +'x'+
        str(int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    )

    cv2.namedWindow('Video Stream', cv2.WINDOW_AUTOSIZE)
    
    if not camera.isOpened():
        camera.open(0)

    while True:
        retval, frame = camera.read()

        detectFaces(frame)

        cv2.imshow('Video Stream', frame)

        key = cv2.waitKey(1)

        if key == 27:
            cv2.destroyWindow('Video Stream')
            cv2.waitKey(1); cv2.waitKey(1);
            cv2.waitKey(1); cv2.waitKey(1);
            camera.release();
            break;


if __name__ == '__main__':
    try:
        print('Type \'help\' for information')

        while True:
            user_input = input('> ')

            if user_input == 'help':
                print('Commands:')
                print('  exit: exits the program')
                print('  quit: exits the program')
                print('  stream: opens a video stream')

            elif user_input == 'exit' or user_input == 'quit':
                break

            elif user_input == 'stream':
                camera = cv2.VideoCapture(0)
                camera.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
                stream(camera)

            else:
                print('Unknown command: \"'+ user_input +'\"')

    except EOFError:
        print()
    except KeyboardInterrupt:
        print()
