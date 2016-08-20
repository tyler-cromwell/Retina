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
import configparser
import hashlib
import os

""" External libraries """
import numpy
from PIL import Image
import cv2

""" Local modules """
from modules import algorithms
from modules import detector
from modules import imgproc


class Recognizer(detector.Detector):
    def __init__(self, classifier, label, settings, algorithm=algorithms.Algorithms.LBPH.value):
        super().__init__(classifier, settings)
        config = configparser.ConfigParser()
        config.read(settings)
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = None

        self._threshold = int(config.get('Recognizer', 'threshold'))
        self._width = int(config.get('Recognizer', 'width'))
        self._height = int(config.get('Recognizer', 'height'))

        if algorithm == algorithms.Algorithms.Eigen.value:
            self._recognizer = cv2.face.createEigenFaceRecognizer(threshold=self._threshold);
            path = root_dir +'/data/recognizers/'+ label +'.eigen.xml'
        elif algorithm == algorithms.Algorithms.Fisher.value:
            self._recognizer = cv2.face.createFisherFaceRecognizer(threshold=self._threshold);
            path = root_dir +'/data/recognizers/'+ label +'.fisher.xml'
        else:
            self._recognizer = cv2.face.createLBPHFaceRecognizer(threshold=self._threshold)
            path = root_dir +'/data/recognizers/'+ label +'.lbph.xml'

        self._recognizer.load(path)
        self._label = label
        self._hash = int(hashlib.sha1(label.encode()).hexdigest(), 16) % (10 ** 8)


    def recognize(self, frame):
        confidences = []
        labels = []
        faces = self.detect(frame, False)

        for (x, y, w, h) in faces:
            face = imgproc.preprocess(frame, self._width, self._height, x, y, w, h)
            predicted_label, confidence = self._recognizer.predict(face)

            if predicted_label == self._hash:
                labels.append(self._label)
                confidences.append(str(round(confidence)))
            else:
                labels.append('Unknown')
                confidences.append(str(-1))


        return (labels, faces, confidences)


    def recognizeFromFile(self, path):
        image_pil = Image.open(path)
        image_org = numpy.array(image_pil)
        image_rgb = cv2.cvtColor(image_org, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image_rgb, (800, 600))
        labels, objects, confidences = self.recognize(image)
        return image, labels, objects, confidences
