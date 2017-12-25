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

import cv2


class Camera():
    def __init__(self, source, config):
        camera = config['Camera']
        self.__source = source
        self.__camera = cv2.VideoCapture(source)
        self.__width = int(camera['width'])
        self.__height = int(camera['height'])
        self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.__width)
        self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__height)

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def open(self):
        if not self.__camera.isOpened():
            if not self.__camera.open(self.__source):
                return False
        return True

    def read(self):
        return self.__camera.read()

    def release(self):
        return self.__camera.release()
