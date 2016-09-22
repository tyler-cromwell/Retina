#!/usr/bin/env python3

#######################################################################
# Copyright (C) 2016 Tyler Cromwell <tyler@csh.rit.edu>
#
# This file is part of Cerebrum.
#
# Cerebrum is free software: you can redistribute it and/or modify
# it under Version 2 of the terms of the GNU General Public License
# as published by the Free Software Foundation.
#
# Cerebrum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY of FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cerebrum.
# If not, see <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
#######################################################################

# Python libraries
import getopt
import os
import sys

# External libraries
import cv2

# Local modules
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import camera
from modules import config
from modules import detector
from modules import imgproc
from modules import misc
from modules import opt
from modules import recognizer

# Global constants
CAMERA_DEFAULT = 0


def print_usage():
    """
    Displays program usage information.
    """
    print('Usage:\t./create_face_dataset.py [--classifier=PATH] --label=NAME [--settings=NAME]')
    print('  --help\t\tPrints this text')
    print('  --classifier=PATH\tThe absolute path of a Face Detection classifier (Optional)')
    print('  --label=NAME\t\tThe name of the person\'s face dataset to create')
    print('  --settings=NAME\tThe name of a file located under \'settings/\'')
    print('        See \'settings/\', without \'.txt\' extension')
    exit(0)


def main():
    """
    Main function.
    """
    classifier = None
    label = None
    settings = opt.map_settings()
    key = opt.default_settings()
    window_name = 'Camera %d' % (CAMERA_DEFAULT)

    # Parse command-line arguments
    try:
        short_opts = ['']
        long_opts = ['help', 'classifier=', 'label=', 'settings=']
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as error:
        print('Invalid argument: \'' + str(error) + '\'\n')
        print_usage()

    if len(opts) == 0:
        print_usage()

    for o, a in opts:
        if o == '--help':
            print_usage()
        elif o == '--classifier':
            classifier = opt.classifier(a)
        elif o == '--label':
            label = a
        elif o == '--settings':
            key = a

    if not label:
        print('\n  Label not specified!\n')
        print_usage()
    elif key not in settings.keys():
        print('\n  Settings not specified!\n')
        print_usage()

    # Setup training set, objects, and window
    configuration = config.Config(settings[key])
    recognizer = config.recognizer()
    width = int(recognizer['width'])
    height = int(recognizer['height'])
    training_path = sys.path[1] + '/data/faces/' + label + '/training/'
    os.makedirs(training_path, exist_ok=True)

    dwidth, dheight = misc.get_display_resolution()
    print('Display resolution: %dx%d' % (dwidth, dheight))

    detector_obj = detector.Detector(classifier, configuration)
    stream = camera.Camera(CAMERA_DEFAULT, configuration)
    print('Capture Resolution: %dx%d' % (stream.getWidth(), stream.getHeight()))

    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(window_name, (dwidth - stream.getWidth()) // 2, 0)

    p = 0
    poses = [
        'Happy', 'Sad', 'Angry', 'Surprised', 'Silly', 'Normal',
        'Right eye closed', 'Left eye closed', 'Both eyes closed'
    ]

    # Begin using the camera
    if not stream.open():
        print('Failed to open Camera', CAMERA_DEFAULT)
        exit(1)

    while True:
        retval, frame = stream.read()
        grayed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector_obj.detect(grayed)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)

        if p < len(poses):
            msg_glasses = 'Glasses?: On'
        else:
            msg_glasses = 'Glasses?: Off'

        msg_pose = 'Expected Pose: ' + poses[p % len(poses)]

        cv2.putText(frame, 'Photos remaining: [%d/%d]' % (p, 2 * len(poses)), (0, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.putText(frame, msg_pose, (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.putText(frame, msg_glasses, (0, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.putText(frame, 'Press \'w\' to take photo', (0, 55), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1)

        if key == 27:
            cv2.destroyWindow(window_name)
            cv2.waitKey(1)
            cv2.waitKey(1)
            cv2.waitKey(1)
            cv2.waitKey(1)
            stream.release()
            break
        elif key == ord('w') and len(faces) >= 1:
            retval, frame = stream.read()   # Get frame without drawings
            (x, y, w, h) = faces[0]

            image = imgproc.preprocess(frame, width, height, x, y, w, h)

            if p < 10:
                cv2.imwrite(training_path + label + '.0' + str(p) + '.png', image)
            else:
                cv2.imwrite(training_path + label + '.' + str(p) + '.png', image)

            if p < (2 * len(poses)) - 1:
                p = p + 1
            else:
                break

    stream.release()


if __name__ == '__main__':
    """
    Program entry.
    """
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
