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
import sys

""" External libraries """
import cv2

""" Setup Cerebrum module path """
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

""" Local modules """
from modules import detector


class Recognizer(detector.Detector):
    def __init__(self, classifier, label, settings):
        detector.Detector.__init__(self, classifier, settings)
        self._recognizer = cv2.face.createLBPHFaceRecognizer(threshold=100)
        self._recognizer.load(ROOT_DIR +'/data/recognizers/'+ label +'.xml')
        self._label = label
        self._hash = int(hashlib.sha1(label.encode()).hexdigest(), 16) % (10 ** 8)


    def recognize(self, frame):
        grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detect(grayframe, False)
        labels = []

        for (x, y, w, h) in faces:
            predicted_label = self._recognizer.predict(grayframe[y: y+h, x: x+w])

            if predicted_label == self._hash:
                labels.append(self._label)
            else:
                labels.append('Unknown')

        return (labels, faces)
