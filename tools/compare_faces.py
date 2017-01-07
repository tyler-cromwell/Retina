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
import numpy

# Local modules
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import config
from modules import opt
from modules import recognizer
from modules import var


def print_usage():
    """
    Displays program usage information.
    """
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
    label1 = None
    label2 = None
    classifier = None
    settings = opt.map_settings()
    key = opt.default_settings()

    # Parse command-line arguments
    try:
        short_opts = ['']
        long_opts = [
            'help',
            'classifier=',
            'label1=',
            'label2=',
            'settings=',
            'show'
        ]
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
            classifier = opt.validate_file(a)
        elif o == '--label1':
            label1 = opt.validate_raw_dataset(a)
        elif o == '--label2':
            label2 = opt.validate_raw_dataset(a)
        elif o == '--settings':
            key = a

    if not label1 or not label2:
        print('\n  Label not specified!\n')
        print_usage()
    elif key not in settings.keys():
        print('\n  Settings not specified!\n')
        print_usage()

    # Initialize variables
    configuration = config.Config(settings[key])
    recognizer_obj = recognizer.Recognizer(classifier, label1, configuration)
    raw_path = var.get_raw_root(label2)
    image_paths = []
    all_confidences = []
    all_widths = []
    all_heights = []
    percent = 0

    # Get the absolute path of each image
    print('Collecting images of ' + label2 + '... ', end='')
    for entry in os.listdir(raw_path):
        image_paths.append(os.path.join(raw_path, entry))
    print('DONE')

    # Preprocess each image
    for i, path in enumerate(image_paths):
        percent = ((i+1) / len(image_paths)) * 100
        print("\rCalculating confidence statistics... {:.1f}%".format(percent), end='')
        sys.stdout.flush()
        skip = False

        image, objects, labels, confidences = recognizer_obj.recognize_from_file(path)

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
    print('Five Number Summary:')
    print('  Max:\t   {}'.format(numpy.max(all_confidences)))
    print('  Min:\t   {}'.format(numpy.min(all_confidences)))
    print('  Median:  {}'.format(numpy.median(all_confidences)))
    print('  Mean:\t   {}'.format(numpy.mean(all_confidences)))
    print('  StdDev:  {}'.format(numpy.std(all_confidences)))
    print('Mean face size: %dx%d' % (numpy.mean(all_widths), numpy.mean(all_heights)))


if __name__ == '__main__':
    """
    Program entry.
    """
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
