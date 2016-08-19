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
import cv2

""" Local modules """
from modules import algorithms
from modules import detector


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
        labels = []
        faces = self.detect(frame, False)

        for (x, y, w, h) in faces:
            face = preprocess(frame, self._width, self._height, x, y, w, h)
            predicted_label, confidence = self._recognizer.predict(face)

            if predicted_label == self._hash:
                labels.append(self._label +' ('+ str(round(confidence)) +')')
            else:
                labels.append('Unknown')

        return (labels, faces)


def preprocess(frame, width, height, x, y, w, h):
    cropped = frame[y: y+h, x: x+w]
    grayed = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(grayed, (width, height))
    equalized = cv2.equalizeHist(resized)
    filtered = cv2.bilateralFilter(equalized, 5, 60, 60)
    return filtered
