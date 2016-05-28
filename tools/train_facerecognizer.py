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
import hashlib
import getopt
import os
import sys

""" External libraries """
import numpy
from PIL import Image
import cv2

""" Local modules """
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import detector
from modules import opt


"""
Returns the path of the training set.
"""
def opt_label(arg):
    if os.path.isdir(sys.path[1] +'/data/faces/'+ arg):
        return arg
    else:
        return None


"""
Displays program usage information.
"""
def print_usage():
    print('Usage:\t./train_facerecognizer.py [--classifier=PATH] --label=NAME [--settings=MACHINE]')
    print('  --help\t\tPrints this text')
    print('  --classifier=PATH\tThe absolute path of a Face Detection classifier (Optional)')
    print('  --label=NAME\t\tThe name of the person\'s face to recognize')
    print('  --settings=MACHINE\tThe absolute path of a file located under \'settings/\'')
    print('      Required if not running on a Raspberry Pi 2')
    print('      [beagleboneblack, mydesktop, raspberrypi2, thinkpad-t420]')
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
        print('\n  Settings not specified\n')
        print_usage()

    """ Initialize variables """
    filename = label +'.xml'
    training_path = sys.path[1] +'/data/faces/'+ label +'/'
    recognizer_path = sys.path[1] +'/data/recognizers/'+ label +'.xml'
    faceDetector = detector.Detector(faceClassifier, settings[key])
    faceRecognizer = cv2.face.createLBPHFaceRecognizer()
    image_paths = []
    images = []
    labels = []

    """ Get the absolute path of each image """
    print('Collecting training images... ', end='')
    for entry in os.listdir(training_path):
        image_paths.append(os.path.join(training_path, entry))
    print('DONE')

    """ Add each of the persons images to the training set """
    print('Detecting faces and assigning labels... ', end='')
    for path in image_paths:
        gray_image = Image.open(path).convert('L')
        image = numpy.array(gray_image, 'uint8')
        faces = faceDetector.detect(image, False)

        for (x, y, w, h) in faces:
            images.append(image[y: y+h, x: x+w])
            labels.append(int(hashlib.sha1(label.encode()).hexdigest(), 16) % (10 ** 8))
    print('DONE')

    """ Train """
    print('Training recognizer... ', end='')
    faceRecognizer.train(images, numpy.array(labels))
    print('DONE')

    """ Save the newly trained recognizer """
    print('Saving recognizer: '+ filename +'... ', end='')
    os.makedirs(sys.path[1] +'/data/recognizers/', exist_ok=True)
    faceRecognizer.save(recognizer_path)
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
