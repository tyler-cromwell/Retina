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
        camera = config.camera()
        recognizer = config.recognizer()
        file_ = pathname.get_recognizer_file(label)

        self._label = label
        self._hash = hash_label(label)
        self._width = int(camera['width'])
        self._height = int(camera['height'])
        self._threshold = int(recognizer['threshold'])
        self._rwidth = int(recognizer['width'])
        self._rheight = int(recognizer['height'])
        self._recognizer = cv2.face.createLBPHFaceRecognizer(threshold=self._threshold)
        self._recognizer.load(file_)

    def recognize(self, frame):
        confidences = []
        labels = []
        objects = self.detect(frame)

        for (x, y, w, h) in objects:
            face = imgproc.preprocess(
                frame,
                self._rwidth,
                self._rheight,
                x, y, w, h
            )

            predicted_label, confidence = self._recognizer.predict(face)

            if predicted_label == self._hash:
                labels.append(self._label)
                confidences.append(round(confidence))
            else:
                labels.append('Unknown')
                confidences.append(-1)

        return (objects, labels, confidences)

    def recognize_from_file(self, path):
        image_pil = Image.open(path)
        image_org = numpy.array(image_pil)
        image_rgb = cv2.cvtColor(image_org, cv2.COLOR_BGR2RGB)

        (iwidth, iheight) = image_pil.size
        ar_height = int(self._width / (iwidth / iheight))

        image = cv2.resize(image_rgb, (self._width, ar_height))
        objects, labels, confidences = self.recognize(image)
        return (image, objects, labels, confidences)


def identify(frame, classifier, config):
    identities = []

    for f in os.listdir(pathname.get_recognizer_root()):
        if f.endswith('.xml'):
            label = f.split('.')[0]
            recognizer = Recognizer(classifier, label, config)
            image, objects, labels, confidences = recognizer.recognize_from_file(frame)
            identities.append((labels[0], confidences[0]))

    return sorted(identities, key=lambda x: x[1])


def hash_label(label):
    sha1 = hashlib.sha1(label.encode())
    return int(sha1.hexdigest(), 16) % (10 ** 8)
