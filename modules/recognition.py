#######################################################################
# Copyright (C) 2016-Present Tyler Cromwell <tjc6185@gmail.com>
#
# This file is part of Retina.
#
# Retina is free software: you can redistribute it and/or modify
# it under Version 2 of the terms of the GNU General Public License
# as published by the Free Software Foundation.
#
# Retina is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY of FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Retina.
# If not, see <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
#######################################################################

import hashlib
import os

import numpy
from PIL import Image
import cv2

from . import detection
from . import imgproc
from . import pathname


class Recognizer(detection.Detector):
    def __init__(self, classifier, label, config):
        super().__init__(classifier, config)
        camera = config['Camera']
        recognizer = config['Recognizer']
        file_ = pathname.get_recognizer_file(label)

        self.__label = label
        self.__hash = hash_label(label)
        self.__width = int(camera['width'])
        self.__height = int(camera['height'])
        self.__threshold = int(recognizer['threshold'])
        self.__rwidth = int(recognizer['width'])
        self.__rheight = int(recognizer['height'])
        self.__recognizer = cv2.face.createLBPHFaceRecognizer(threshold=self.__threshold)
        self.__recognizer.load(file_)

    def recognize(self, frame):
        confidences, labels = [], []
        objects = self.detect(frame)

        for (x, y, w, h) in objects:
            face = imgproc.preprocess(
                frame,
                self.__rwidth,
                self.__rheight,
                x, y, w, h
            )

            predicted_label, confidence = self.__recognizer.predict(face)

            if predicted_label == self.__hash:
                labels.append(self.__label)
                confidences.append(round(confidence))
            else:
                labels.append('Unknown')
                confidences.append(-1)

        return (objects, labels, confidences)

    def recognize_from_file(self, path):
        image_pil = Image.open(path)
        image_org = numpy.array(image_pil)
        image_rgb = cv2.cvtColor(image_org, cv2.COLOR_BGR2RGB)
        ar_height = int(self.__width / (image_pil.size[0] / image_pil.size[1]))
        image = cv2.resize(image_rgb, (self.__width, ar_height))
        objects, labels, confidences = self.recognize(image)
        return (image, objects, labels, confidences)


def identify(frame, classifier, config):
    identities = []

    for f in os.listdir(pathname.get_recognizer_root()):
        if f.endswith('.xml'):
            label = f.split('.')[0]
            recognizer = Recognizer(classifier, label, config)
            image, objects, labels, confidences = recognizer.recognize_from_file(frame)

            if len(labels) > 0:
                identities.append((labels[0], confidences[0]))

    return sorted(identities, key=lambda face: face[1])


def hash_label(label):
    sha1 = hashlib.sha1(label.encode())
    return int(sha1.hexdigest(), 16) % (10 ** 8)
