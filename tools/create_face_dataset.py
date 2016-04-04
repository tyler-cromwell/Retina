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
import tkinter

""" External libraries """
import cv2

""" Setup Cerebrum module path """
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

""" Local modules """
from modules import detector
from modules import misc
from modules import opt

""" Global constants """
CAMERA_DEFAULT = 0


"""
Displays program usage information.
"""
def print_usage():
    print('Usage:\t./create_face_dataset.py --classifier=PATH --label=NAME --settings=MACHINE')
    print('  --help\t\tPrints this text')
    print('  --classifier=PATH\tThe path to a Face Detection classifier')
    print('  --label=NAME\t\tThe name of the person\'s face dataset to create')
    print('  --settings=MACHINE\tA file located under \'settings/\' (no extension)')
    exit(0)


"""
Main function.
"""
def main():
    windowName = 'Camera %d' % (CAMERA_DEFAULT)
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

    for o, a in opts:
        if o == '--help':
            print_usage()
        elif o == '--classifier':
            faceClassifier = opt.opt_classifier(a)
        elif o == '--label':
            label = a
        elif o == '--settings':
            settings = opt.opt_settings(ROOT_DIR, a)

    setDir = ROOT_DIR +'/data/faces/'+ label +'/'

    """ Ensure training set parent directory exists """
    os.makedirs(setDir, exist_ok=True)

    """ Get screen resolution """
    displayWidth, displayHeight = misc.get_display_resolution()
    print('Display resolution: %dx%d' % (displayWidth, displayHeight))

    """ Initialize face detector """
    faceDetector = detector.Detector(faceClassifier, settings)
    width = faceDetector.get_width()
    height = faceDetector.get_height()

    """ Set camera resolution """
    camera = cv2.VideoCapture(CAMERA_DEFAULT)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    print('Capture Resolution: %dx%d' %
        (camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )

    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(windowName, (displayWidth - width) // 2, 0)

    """ Define poses """
    poses = [
        'Happy', 'Sad', 'Angry', 'Surprised', 'Silly', 'Glasses',
        'No Glasses', 'Normal', 'Right eye', 'Left eye', 'Both eyes',
    ]
    t = 0

    """ Begin using the camera """
    if not camera.isOpened():
        if not camera.open(CAMERA_DEFAULT):
            print('Failed to open Camera', CAMERA_DEFAULT)
            exit(1)

    while True:
        retval, frame = camera.read()
        faces = faceDetector.detect(frame)

        if 8 <= t and t <= 10:
            cv2.putText(frame, 'Expected Pose: '+ poses[t] +' closed', (0, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        else:
            cv2.putText(frame, 'Expected Pose: '+ poses[t], (0, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

        cv2.putText(frame, 'Press \'w\' to take photo', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

        cv2.imshow(windowName, frame)
        key = cv2.waitKey(1)

        if key == 27:
            cv2.destroyWindow(windowName)
            cv2.waitKey(1); cv2.waitKey(1);
            cv2.waitKey(1); cv2.waitKey(1);
            camera.release()
            break
        elif key == ord('w') and len(faces) >= 1:
            retval, frame = camera.read()   # Get frame without drawings
            x, y, w, h = faces[0]
            cropped = frame[y: y+h, x: x+w]
            cv2.imwrite(setDir + label +'.'+ poses[t].lower().replace(' ', '') +'.png', cropped)

            if t < 10:
                t = t + 1
            else:
                break


"""
Program entry.
"""
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
