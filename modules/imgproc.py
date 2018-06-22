#######################################################################
# Copyright (C) 2016-Present Tyler Cromwell <tjc6185@gmail.com>
#
# This file is part of Retina.
#
# Retina is free software: you can redistribute it and/or modify
# it under Version 2 of the terms of the GNU General Public License
# as published by the Free Software Foundation.
#
# Retina is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY of FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Retina.
# If not, see <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
#######################################################################

import cv2


def draw_face_info(image, objects, labels, confidences):
    """
    Draws the rectangle, label, and confidence around a face
    """
    for i, (x, y, w, h) in enumerate(objects):
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.putText(image, labels[i].title() + ' (' + str(confidences[i]) + ')', (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv2.putText(image, '{:d}x{:d}'.format(w, h), (x, y+h+13), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))


def preprocess(frame, width, height, x, y, w, h):
    """
    Preprocesses an image for Face Recognition
    """
    cropped = frame[y: y+h, x: x+w]
    grayed = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(grayed, (width, height))
    equalized = cv2.equalizeHist(resized)
    filtered = cv2.bilateralFilter(equalized, 5, 60, 60)
    return filtered
