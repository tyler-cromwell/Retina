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
import numpy
from PIL import Image
import cv2

""" Local modules """
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import detector
from modules import opt
from modules import recognizer


"""
Ensures the given label has a raw dataset to process.
"""
def opt_label(label):
    if os.path.isdir(sys.path[1] +'/data/faces/'+ label +'/raw'):
        return label
    else:
        return None


"""
Displays program usage information.
"""
def print_usage():
    print('Usage:\t./process_raw_images.py [--classifier=PATH] --label=NAME [--settings=MACHINE]')
    print('  --help\t\tPrints this text')
    print('  --classifier=PATH\tThe absolute path of a Face Detection classifier (Optional)')
    print('  --label=NAME\t\tThe name of the person\'s face dataset to create')
    print('  --settings=MACHINE\tThe absolute path of a file located under \'settings/\'')
    print('        Required if not running on a Raspberry Pi 2')
    print('        See \'settings/\', without \'.txt\' extension')
    exit(0)


"""
Main function.
"""
def main():
    faceClassifier = None
    label = None
    settings = opt.map_settings()
    key = opt.default_settings()

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
            label = opt_label(a)
        elif o == '--settings':
            key = a

    if not label:
        print('\n  Label not specified!\n')
        print_usage()
    elif not key in settings.keys():
        print('\n  Settings not specified!\n')

    """ Initialize variables """
    faceDetector = detector.Detector(faceClassifier, settings[key])
    raw_path = sys.path[1] +'/data/faces/'+ label +'/raw/'
    training_path = sys.path[1] +'/data/faces/'+ label +'/training/'
    image_paths = []

    os.makedirs(training_path, exist_ok=True)

    """ Get the absolute path of each image """
    print('Collecting raw images... ', end='')
    for entry in os.listdir(raw_path):
        image_paths.append(os.path.join(raw_path, entry))
    print('DONE')

    """ Preprocess each image """
    print('Preprocessing raw images...', end='')
    for i, path in enumerate(image_paths):
        image_pil = Image.open(path).convert('RGB')
        image = numpy.array(image_pil)
        (x, y, w, h) = faceDetector.detect(image, False)[0]
        face = recognizer.preprocess(image, x, y, w, h)

        if i < 10:
            cv2.imwrite(training_path + label +'.0'+ str(i) +'.png', face);
        else:
            cv2.imwrite(training_path + label +'.'+ str(i) +'.png', face);
    print('DONE')


"""
Program entry.
"""
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
