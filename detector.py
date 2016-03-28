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
        self.classifier = cv2.CascadeClassifier(classifier)
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.width = int(self.config.get('General', 'width'))
        self.height = int(self.config.get('General', 'height'))
        self.flags = int(self.config.get('Classifier', 'flags'))
        self.scaleFactor = float(self.config.get('Classifier', 'scaleFactor'))
        self.minNeighbors = int(self.config.get('Classifier', 'minNeighbors'))
        self.minSize = tuple(map(int, re.split('\s*,\s*', self.config.get('Classifier', 'minSize'))))
        self.maxSize = tuple(map(int, re.split('\s*,\s*', self.config.get('Classifier', 'maxSize'))))


    def detect(self, frame, grayscale=True):
        temp_frame = frame

        if grayscale:
            temp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = self.classifier.detectMultiScale(
            temp_frame,
            flags = self.flags,
            scaleFactor = self.scaleFactor,
            minNeighbors = self.minNeighbors,
            minSize = self.minSize,
            maxSize = self.maxSize
        )

        for i, (x, y, w, h) in enumerate(objects):
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            cv2.putText(frame, 'Object %d' % i, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

        return objects


    def get_width(self):
        return self.width


    def get_height(self):
        return self.height
