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
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.width = int(self.config.get('Faces', 'width'))
        self.height = int(self.config.get('Faces', 'height'))
        self.scaleFactor = float(self.config.get('Faces', 'scaleFactor'))
        self.minNeighbors = int(self.config.get('Faces', 'minNeighbors'))
        self.minSize = tuple(map(int, re.split('\s*,\s*', self.config.get('Faces', 'minSize'))))
        self.maxSize = tuple(map(int, re.split('\s*,\s*', self.config.get('Faces', 'maxSize'))))
        self.objectCascade = cv2.CascadeClassifier(classifier)


    def search(self, frame):
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = self.objectCascade.detectMultiScale(
            grayscale,
            scaleFactor = self.scaleFactor,
            minNeighbors = self.minNeighbors,
            flags = 0,
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
