#######################################################################
# Copyright (C) 2016 Tyler Cromwell <tjc6185@gmail.com>
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

import re

import cv2

from . import pathname


class Detector:
    def __init__(self, classifier, config):
        detector = config['Detector']

        if classifier:
            self.__classifier = cv2.CascadeClassifier(classifier)
        else:
            self.__classifier = cv2.CascadeClassifier(pathname.get_classifier_root() + detector['classifier'])

        self.__flags = int(detector['flags'])
        self.__scaleFactor = float(detector['scaleFactor'])
        self.__minNeighbors = int(detector['minNeighbors'])
        self.__minSize = tuple(map(int, re.split('\s*,\s*', detector['minSize'])))
        self.__maxSize = tuple(map(int, re.split('\s*,\s*', detector['maxSize'])))

    def detect(self, frame):
        objects = self.__classifier.detectMultiScale(
            frame,
            flags=self.__flags,
            scaleFactor=self.__scaleFactor,
            minNeighbors=self.__minNeighbors,
            minSize=self.__minSize,
            maxSize=self.__maxSize
        )

        return objects
