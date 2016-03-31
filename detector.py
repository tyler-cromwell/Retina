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
import re

""" External libraries """
import cv2


class Detector:
    def __init__(self, classifier, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        self._classifier = cv2.CascadeClassifier(classifier)
        self._width = int(config.get('General', 'width'))
        self._height = int(config.get('General', 'height'))
        self._flags = int(config.get('Classifier', 'flags'))
        self._scaleFactor = float(config.get('Classifier', 'scaleFactor'))
        self._minNeighbors = int(config.get('Classifier', 'minNeighbors'))
        self._minSize = tuple(map(int, re.split('\s*,\s*', config.get('Classifier', 'minSize'))))
        self._maxSize = tuple(map(int, re.split('\s*,\s*', config.get('Classifier', 'maxSize'))))


    def detect(self, frame, grayscale=True):
        temp_frame = frame

        if grayscale:
            temp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = self._classifier.detectMultiScale(
            temp_frame,
            flags = self._flags,
            scaleFactor = self._scaleFactor,
            minNeighbors = self._minNeighbors,
            minSize = self._minSize,
            maxSize = self._maxSize
        )

        for i, (x, y, w, h) in enumerate(objects):
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            cv2.putText(frame, 'Object %d' % i, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

        return objects


    def get_width(self):
        return self._width


    def get_height(self):
        return self._height
