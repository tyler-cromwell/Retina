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
from modules import camera
from modules import detector
from modules import misc
from modules import opt
from modules import recognizer

""" Global constants """
CAMERA_DEFAULT = 0


"""
Displays program usage information.
"""
def print_usage():
    print('Usage:\t./create_face_dataset.py --classifier=PATH --label=NAME --settings=MACHINE')
    print('  --help\t\tPrints this text')
    print('  --classifier=PATH\tThe absolute path of a Face Detection classifier')
    print('  --label=NAME\t\tThe name of the person\'s face dataset to create')
    print('  --settings=MACHINE\tThe absolute path of a file located under \'settings/\'')
    exit(0)


"""
Main function.
"""
def main():
    windowName = 'Camera %d' % (CAMERA_DEFAULT)
    faceClassifier = None
    label = None
    settings = opt.default_settings(ROOT_DIR)

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
            faceClassifier = opt.classifier(a)
        elif o == '--label':
            label = a
        elif o == '--settings':
            settings = opt.settings(a)

    if faceClassifier == None:
        print('\n  Classifier not specified!\n')
        print_usage()
    elif label == None:
        print('\n  Label not specified!\n')
        print_usage()
    elif settings == None:
        print('\n  Settings not specified!\n')
        print_usage()

    """ Setup training set, objects, and window """
    setDir = ROOT_DIR +'/data/faces/'+ label +'/'
    os.makedirs(setDir, exist_ok=True)

    displayWidth, displayHeight = misc.get_display_resolution()
    print('Display resolution: %dx%d' % (displayWidth, displayHeight))

    faceDetector = detector.Detector(faceClassifier, settings)
    stream = camera.Camera(CAMERA_DEFAULT, settings)
    print('Capture Resolution: %dx%d' % (stream.getWidth(), stream.getHeight()))

    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(windowName, (displayWidth - stream.getWidth()) // 2, 0)

    p = 0
    poses = [
        'Happy', 'Sad', 'Angry', 'Surprised', 'Silly', 'Normal',
        'Right eye closed', 'Left eye closed', 'Both eyes closed'
    ]

    """ Begin using the camera """
    if not stream.isOpened():
        if not stream.open(CAMERA_DEFAULT):
            print('Failed to open Camera', CAMERA_DEFAULT)
            exit(1)

    while True:
        retval, frame = stream.read()
        faces = faceDetector.detect(frame)

        for (x, y, w, h) in faces:
             cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)

        if p < len(poses):
            msg_glasses = 'Glasses?: On'
        else:
            msg_glasses = 'Glasses?: Off'

        msg_pose = 'Expected Pose: '+ poses[p % len(poses)]

        cv2.putText(frame, 'Photos remaining: [%d/%d]' % (p, 2 * len(poses)), (0, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.putText(frame, msg_pose, (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.putText(frame, msg_glasses, (0, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.putText(frame, 'Press \'w\' to take photo', (0, 55), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

        cv2.imshow(windowName, frame)
        key = cv2.waitKey(1)

        if key == 27:
            cv2.destroyWindow(windowName)
            cv2.waitKey(1); cv2.waitKey(1);
            cv2.waitKey(1); cv2.waitKey(1);
            stream.release()
            break
        elif key == ord('w') and len(faces) >= 1:
            retval, frame = stream.read()   # Get frame without drawings
            (x, y, w, h) = faces[0]

            image = recognizer.preprocess(frame, x, y, w, h)
            cv2.imwrite(setDir + label +'.'+ str(p) +'.png', image)

            if p < (2 * len(poses)) - 1:
                p = p + 1
            else:
                break

    stream.release()


"""
Program entry.
"""
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
