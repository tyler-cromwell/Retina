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

import numpy
from PIL import Image
import cv2

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import camera
from modules import configuration
from modules import detection
from modules import imgproc
from modules import opt
from modules import pathname


def print_usage():
    """
    Displays program usage information.
    """
    print('Usage:\t./process_raw_images.py [--classifier=PATH] --label=NAME [--settings=NAME] [--show]')
    print('  --help\t\tPrints this text')
    print('  --classifier=PATH\tThe absolute path of a Face Detection classifier (Optional)')
    print('  --label=NAME\t\tThe name of the person\'s face dataset to create')
    print('  --settings=NAME\tThe name of a file located under \'settings/\'')
    print('        See \'settings/\', without \'.txt\' extension')
    print('  --show\t\tOpens a window to show images being processed')
    exit(0)


def main():
    """
    Main function.
    """
    classifier = None
    label = None
    show = False
    settings = opt.map_settings()
    key = opt.default_settings()

    try:
        short_opts = ['']
        long_opts = ['help', 'classifier=', 'label=', 'settings=', 'show']
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as error:
        print('Invalid argument: \"{}\"\n'.format(str(error)))
        print_usage()

    if len(opts) == 0:
        print_usage()

    for o, a in opts:
        if o == '--help':
            print_usage()
        elif o == '--classifier':
            classifier = opt.validate_file(a)
        elif o == '--label':
            label = opt.validate_raw_dataset(a)
        elif o == '--settings':
            key = a
        elif o == '--show':
            show = True

    if key not in settings.keys():
        print('\n  Settings file \"{}\" not found!\n'.format(key))
        print_usage()

    if not label:
        print('\n  Label not specified!\n')
        print_usage()

    # Initialize variables
    config = configuration.Config(settings[key])
    recognizer = config.recognizer()
    width = int(recognizer['width'])
    height = int(recognizer['height'])
    stream = camera.Camera(0, config)
    detector = detection.Detector(classifier, config)
    raw_path = pathname.get_raw_root(label)
    training_path = pathname.get_training_root(label)

    os.makedirs(training_path, exist_ok=True)

    # Get the absolute path of each image
    print('Collecting raw images... ', end='')
    image_paths = pathname.get_raw_images(label)
    print('DONE')

    # Preprocess each image
    l = len(image_paths)
    for i, path in enumerate(image_paths):
        print('\rPreprocessing raw images... ({}/{})'.format(str(i+1), str(l)), end='')
        cont = False
        image_pil = Image.open(path)
        image_org = numpy.array(image_pil)
        image_rgb = cv2.cvtColor(image_org, cv2.COLOR_BGR2RGB)

        (iwidth, iheight) = image_pil.size
        aspect_ratio = iwidth / iheight

        image = cv2.resize(image_rgb, (stream.get_width(), int(stream.get_width() / aspect_ratio)))
        (x, y, w, h) = (0, 0, 0, 0)

        try:
            (x, y, w, h) = detector.detect(image)[0]
        except IndexError:
            print('\nNo faces detected in:', path)
            cont = True

        if show:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)
            cv2.imshow('process_raw_images.py', image)
            cv2.waitKey(1)

        if cont:
            continue

        face = imgproc.preprocess(image, width, height, x, y, w, h)

        if i < 10:
            cv2.imwrite(training_path + label + '.0{}.png'.format(str(i)), face)
        else:
            cv2.imwrite(training_path + label + '.{}.png'.format(str(i)), face)

    print('\rPreprocessing raw images... DONE    ')


if __name__ == '__main__':
    """
    Program entry.
    """
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
