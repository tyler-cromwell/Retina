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
    def __init__(self, classifier, label, config, algorithm=algorithms.Algorithms.LBPH):
        super().__init__(classifier, config)
        general = config.general()
        recognizer = config.recognizer()
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = root_dir +'/data/recognizers/'+ label +'.'+ algorithm.name.lower() +'.xml'

        self._width = int(general['width'])
        self._height = int(general['height'])
        self._threshold = int(recognizer['threshold'])
        self._rwidth = int(recognizer['width'])
        self._rheight = int(recognizer['height'])

        if algorithm.value == algorithms.Algorithms.Eigen.value:
            self._recognizer = cv2.face.createEigenFaceRecognizer(threshold=self._threshold);
        elif algorithm.value == algorithms.Algorithms.Fisher.value:
            self._recognizer = cv2.face.createFisherFaceRecognizer(threshold=self._threshold);
        else:
            self._recognizer = cv2.face.createLBPHFaceRecognizer(threshold=self._threshold)

        self._recognizer.load(path)
        self._label = label
        self._hash = int(hashlib.sha1(label.encode()).hexdigest(), 16) % (10 ** 8)


    def recognize(self, frame):
        confidences = []
        labels = []
        faces = self.detect(frame, False)

        for (x, y, w, h) in faces:
            face = imgproc.preprocess(frame, self._rwidth, self._rheight, x, y, w, h)
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
        image = cv2.resize(image_rgb, (self._width, self._height))
        labels, objects, confidences = self.recognize(image)
        return image, labels, objects, confidences
