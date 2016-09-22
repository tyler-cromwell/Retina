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
import hashlib
import getopt
import os
import sys

# External libraries
import numpy
from PIL import Image
import cv2

# Local modules
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def opt_label(arg):
    """
    Returns the path of the training set.
    """
    if os.path.isdir(sys.path[1] + '/data/faces/' + arg):
        return arg
    else:
        return None


def print_usage():
    """
    Displays program usage information.
    """
    print('Usage:\t./train_facerecognizer.py [--algorithm=NAME] --label=NAME')
    print('  --help\t\tPrints this text')
    print('  --algorithm=NAME\tThe name of the Face Recognition algorithm to train with')
    print('                  \tValues: Eigen, Fisher, or LBPH (default)')
    print('  --label=NAME\t\tThe name of the person\'s face to recognize')
    exit(0)


def main():
    """
    Main function.
    """
    algorithm = ''
    label = None

    # Parse command-line arguments
    try:
        short_opts = ['']
        long_opts = ['help', 'algorithm=', 'label=']
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as error:
        print('Invalid argument: \'' + str(error) + '\'\n')
        print_usage()

    if len(opts) == 0:
        print_usage()

    for o, a in opts:
        if o == '--help':
            print_usage()
        elif o == '--algorithm':
            algorithm = a
        elif o == '--label':
            label = opt_label(a)

    if not label:
        print('\n  Label not specified!\n')
        print_usage()

    # Initialize variables
    training_path = sys.path[1] + '/data/faces/' + label + '/training/'
    recognizer_path = sys.path[1] + '/data/recognizers/' + label
    filename = None
    faceRecognizer = None
    image_paths = []
    images = []
    labels = []

    # Determine algorithm
    if algorithm == 'Eigen':
        faceRecognizer = cv2.face.createEigenFaceRecognizer()
        recognizer_path = sys.path[1] + '/data/recognizers/' + label + '.eigen.xml'
        filename = label + '.eigen.xml'
    elif algorithm == 'Fisher':
        faceRecognizer = cv2.face.createFisherFaceRecognizer()
        recognizer_path = sys.path[1] + '/data/recognizers/' + label + '.fisher.xml'
        filename = label + '.fisher.xml'
    else:
        if not algorithm == 'LBPH':
            print('Defaulting to LBPH')
        faceRecognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer_path = sys.path[1] + '/data/recognizers/' + label + '.lbph.xml'
        filename = label + '.lbph.xml'

    # Get the absolute path of each image
    print('Collecting training images... ', end='')
    for entry in os.listdir(training_path):
        image_paths.append(os.path.join(training_path, entry))
    print('DONE')

    # Add each of the persons images to the training set
    print('Assigning labels... ', end='')
    for path in image_paths:
        image_pil = Image.open(path)
        image = numpy.array(image_pil)
        (w, h) = image_pil.size
        images.append(image[0: 0+h, 0: 0+w])
        sha1 = hashlib.sha1(label.encode())
        labels.append(int(sha1.hexdigest(), 16) % (10 ** 8))
    print('DONE')

    # Train
    print('Training recognizer... ', end='')
    faceRecognizer.train(images, numpy.array(labels))
    print('DONE')

    # Save the newly trained recognizer
    print('Saving recognizer: ' + filename + '... ', end='')
    os.makedirs(sys.path[1] + '/data/recognizers/', exist_ok=True)
    faceRecognizer.save(recognizer_path)
    print('DONE')


if __name__ == '__main__':
    """
    Program entry.
    """
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
