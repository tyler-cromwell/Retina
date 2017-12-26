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

import cv2
import numpy

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import configuration
from modules import opt
from modules import pathname
from modules import recognition


def print_usage(message=None):
    """
    Displays program usage information.
    """
    if message: print('>>>', message, end=' <<<\n')
    print('Usage:\t./compare_faces.py [--classifier=PATH] --label1=NAME --label2=NAME [--settings=NAME]')
    print('  --help\t\tPrints this text')
    print('  --classifier=PATH\tThe absolute path of a Face Detection classifier')
    print('  --label1=NAME\t\tThe name of the person to compare FROM')
    print('  --label2=NAME\t\tThe name of the person to compare TO')
    print('  --settings=NAME\tThe name of a file located under \'settings/\'')
    print('        See \'settings/\', without \'.txt\' extension')
    exit(0)


def main():
    """
    Main function.
    """
    label1, label2, classifier = None, None, None
    settings = opt.map_settings()
    key = opt.default_settings()

    try:
        short_opts = 'hc:l:k:s:w'
        long_opts = ['help', 'classifier=', 'label1=', 'label2=', 'settings=', 'show']
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as error:
        print_usage('Invalid argument: \"{}\"'.format(str(error)))

    for o, a in opts:
        if o == '-h' or o == '--help':          print_usage()
        elif o == '-c' or o == '--classifier':  classifier = opt.validate_file(a)
        elif o == '-l' or o == '--label1':      label1 = opt.validate_raw_dataset(a)
        elif o == '-k' or o == '--label2':      label2 = opt.validate_raw_dataset(a)
        elif o == '-s' or o == '--settings':    key = a

    if len(opts) == 0:
        print_usage()
    elif not label1 or not label2:
        print_usage('Label not specified')
    elif key not in settings.keys():
        print_usage('Settings not specified')

    # Initialize variables
    config = configuration.Config(settings[key])
    recognizer = recognition.Recognizer(classifier, label1, config)
    raw_path = pathname.get_raw_root(label2)
    all_confidences, all_widths, all_heights = [], [], []
    percent = 0

    # Get the absolute path of each image
    print('Collecting images of {}... '.format(label2), end='')
    image_paths = pathname.get_raw_images(label2)
    print('DONE')

    # Preprocess each image
    for i, path in enumerate(image_paths):
        percent = ((i+1) / len(image_paths)) * 100
        print("\rCalculating confidence statistics... {:.1f}%".format(percent), end='')
        sys.stdout.flush()
        skip = False

        image, objects, labels, confidences = recognizer.recognize_from_file(path)

        try:
            if len(confidences) > 1:
                all_confidences.append(confidences[1])
                all_widths.append(objects[1][2])
                all_heights.append(objects[1][3])
            else:
                all_confidences.append(confidences[0])
                all_widths.append(objects[0][2])
                all_heights.append(objects[0][3])
        except IndexError:
            skip = True

        if skip:
            continue

    print('\rCalculating confidence statistics... DONE  ')
    print('')
    print('Confidence Summary:')
    print('  Max:\t   {}'.format(numpy.max(all_confidences)))
    print('  Min:\t   {}'.format(numpy.min(all_confidences)))
    print('  Median:  {}'.format(numpy.median(all_confidences)))
    print('  Mean:\t   {}'.format(numpy.mean(all_confidences)))
    print('  StdDev:  {}'.format(numpy.std(all_confidences)))
    print('')
    print('Face Size Summary:')
    print('  Max:\t   {}x{}'.format(numpy.max(all_widths), numpy.max(all_heights)))
    print('  Min:\t   {}x{}'.format(numpy.min(all_widths), numpy.min(all_heights)))
    print('  Median:  {}x{}'.format(int(numpy.median(all_widths)), int(numpy.median(all_heights))))
    print('  Mean:\t   {}x{}'.format(numpy.mean(all_widths), numpy.mean(all_heights)))
    print('  StdDev:  {}x{}'.format(numpy.std(all_widths), numpy.std(all_heights)))


if __name__ == '__main__':
    """
    Program entry.
    """
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
