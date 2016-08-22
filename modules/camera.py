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

""" External libraries """
import cv2


class Camera():
    def __init__(self, source, config):
        general = config.general()
        self._source = source
        self._camera = cv2.VideoCapture(source)
        self._width = int(general['width'])
        self._height = int(general['height'])
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)


    def getWidth(self):
        return self._width


    def getHeight(self):
        return self._height


    def open(self):
        if not self._camera.isOpened():
            if not self._camera.open(self._source):
                return False
            else:
                return True
        else:
            return True


    def read(self):
        return self._camera.read()


    def release(self):
        return self._camera.release()
