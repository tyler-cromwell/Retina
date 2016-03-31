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

""" External libraries """
import numpy
from PIL import Image
import cv2

""" Global constants """
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
Returns the path of the classifier file.
"""
def opt_classifier(arg):
    if os.path.isfile(arg):
        return arg
    else:
        print('Invalid classifier: '+ arg)
        exit(1)


"""
Returns the path of the training set.
"""
def opt_label(arg):
    if os.path.isdir(ROOT_DIR +'/data/faces/'+ arg):
        return arg
    else:
        print('Invalid training set: '+ arg)
        exit(1)


"""
Displays program usage information.
"""
def print_usage():
    print('Usage:\t./train_facerecognizer.py --classifier=PATH --label=NAME')
    print('  --help\t\tPrints this text')
    print('  --classifier=PATH\tThe path to a Face Detection classifier')
    print('  --label=NAME\t\tThe name of the person\'s face to recognize')
    exit(0)


"""
Main function.
"""
def main():
    faceClassifier = None
    label = None

    """ Parse command-line arguments """
    try:
        short_opts = ['']
        long_opts = ['help', 'classifier=', 'label=']
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
            faceClassifier = opt_classifier(a)
        elif o == '--label':
            label = opt_label(a)

    """ Initialize variables """
    faceDetector = cv2.CascadeClassifier(faceClassifier)
    faceRecognizer = cv2.createLBPHFaceRecognizer()
    image_paths = []
    images = []
    labels = []

    """ Get the absolute path of each image """
    for entry in os.listdir(ROOT_DIR +'/data/faces/'+ label +'/'):
        image_paths.append(os.path.join(path, entry))

    """ Add each of the persons images to the training set """
    for path in image_paths:
        gray_image = Image.open(path).convert('L')
        image = numpy.array(gray_image, 'uint8')
        faces = faceDetector.detectMultiScale(image)

        for (x, y, w, h) in faces:
            images.append(image[y: y+h, x: x+w])
            labels.append(label)

    """ Train """
    faceRecognizer.train(images, numpy.array(labels))

    """ Save the newly trained recognizer """
    os.makedirs(ROOT_DIR +'/data/recognizers/', exist_ok=True)
    faceRecognizer.save(ROOT_DIR +'/data/recognizers/'+ label +'.xml')


"""
Program entry.
"""
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
