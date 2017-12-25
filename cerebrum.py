#!/usr/bin/env python3

#######################################################################
# Copyright (C) 2016 Tyler Cromwell <tjc6185@gmail.com>
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

import getopt
import os
import sys
import time

import cv2

from modules import camera
from modules import configuration
from modules import imgproc
from modules import misc
from modules import opt
from modules import recognition


def print_usage():
    """
    Displays program usage information.
    """
    print('Usage:\t./cerebrum.py [-c PATH] [-f PATH] [-i INDEX] --label=NAME [-s NAME]')
    print('  -h --help\t\tPrints this text')
    print('  -c --classifier=PATH\tThe absolute path of a Face Detection classifier (Optional)')
    print('  -f --file=PATH\tPath to a still image (alternative to camera stream)')
    print('              \t\tIf specified without \'label\' option, will attempt to identify the face')
    print('  -i --input=INDEX\tIndex of an attached camera (Optional)')
    print('  -l --label=NAME\tThe name of the person\'s face to recognize')
    print('  -s --settings=NAME\tThe name of a file located under \'settings/\'')
    print('                 \tSee \'settings/\', without \'.txt\' extension')
    exit(0)


def main():
    """
    Main function.
    """
    classifier = None
    flags = 0
    index = 0
    label = None
    path = None
    settings = opt.map_settings()
    key = opt.default_settings()

    try:
        short_opts = 'hc:f:i:l:s:'
        long_opts = ['help', 'classifier=', 'file=', 'input=', 'label=', 'settings=']
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as error:
        print('Invalid argument: \"{}\"\n'.format(str(error)))
        print_usage()

    if len(opts) == 0:
        print_usage()

    # Process command-line arguments
    for o, a, in opts:
        if o == '-h' or o == '--help':
            print_usage()
        elif o == '-c' or o == '--classifier':
            classifier = opt.validate_file(a)
        elif o == '-f' or o == '--file':
            path = opt.validate_file(a)
        elif o == '-i' or o == '--input':
            index = int(a)
        elif o == '-l' or o == '--label':
            label = opt.validate_recognizer(a)
        elif o == '-s' or o == '--settings':
            key = a

    if key not in settings.keys():
        print('\n  Settings file \"{}\" not found!\n'.format(key))
        print_usage()
    if not label:
        print('\n  Label not specified!\n')
        print_usage()

    # Initialize variables
    config = configuration.Config(settings[key])
    recognizer = recognition.Recognizer(classifier, label, config)
    stream = camera.Camera(index, config)
    window_name = stream.get_window_name()
    dwidth, dheight = misc.get_display_resolution()

    if path and not label:
        # Identify face in image
        identities = recognition.identify(path, classifier, config)
        for i in identities:
            print(i)
        return
    elif path and label:
        # Recognize in a still image
        image, objects, labels, confidences = recognizer.recognize_from_file(path)
        imgproc.draw_face_info(image, objects, labels, confidences)
        cv2.imshow(path, image)
        cv2.waitKey(0)
        return
    else:
        print('Capture resolution: {:d}x{:d}'.format(stream.get_width(), stream.get_height()))
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow(window_name, (dwidth - stream.get_width()) // 2, 0)

        if not stream.open():
            print('Failed to open Camera', index)
            exit(1)

    while True:
        start = time.time()
        retval, frame = stream.read()

        if flags & 1:
            objects, labels, confidences = recognizer.recognize(frame)
            imgproc.draw_face_info(frame, objects, labels, confidences)

        end = time.time()
        fps = 1 // (end - start)

        cv2.putText(frame, 'FPS: [{:d}]'.format(int(fps)), (0, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1)

        if key == 27:
            cv2.destroyWindow(window_name)
            stream.release()
            break
        elif key == ord('f'):
            flags = flags ^ 1


if __name__ == '__main__':
    """
    Program entry.
    """
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
