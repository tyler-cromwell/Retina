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

""" External libraries """
import cv2


class Camera():
    def __init__(self, source, settings):
        config = configparser.ConfigParser()
        config.read(settings)
        self._source = source
        self._camera = cv2.VideoCapture(source)
        self._width = int(config.get('General', 'width'))
        self._height = int(config.get('General', 'height'))
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)


    def getWidth(self):
        return self._width


    def getHeight(self):
        return self._height


    def isOpened(self):
        return self._camera.isOpened()


    def open(self):
        return self._camera.open(self._source)


    def read(self):
        return self._camera.read()


    def release(self):
        return self._camera.release()
