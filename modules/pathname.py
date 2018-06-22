#######################################################################
# Copyright (C) 2016-Present-Present Tyler Cromwell <tjc6185@gmail.com>
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

import os

__ROOT_DIR__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_classifier_root():
    return __ROOT_DIR__ + '/data/classifiers/'


def get_raw_root(label):
    return __ROOT_DIR__ + '/data/faces/' + label + '/raw/'


def get_raw_images(label):
    image_paths = []
    raw_path = get_raw_root(label)
    for path in os.listdir(raw_path):
        image_paths.append(os.path.join(raw_path, path))
    return image_paths


def get_recognizer_root():
    return __ROOT_DIR__ + '/data/recognizers/'


def get_recognizer_file(label):
    return __ROOT_DIR__ + '/data/recognizers/' + label + '.lbph.xml'


def get_settings_root():
    return __ROOT_DIR__ + '/settings/'


def get_training_root(label):
    return __ROOT_DIR__ + '/data/faces/' + label + '/training/'


def get_training_images(label):
    image_paths = []
    training_path = get_training_root(label)
    for path in os.listdir(training_path):
        image_paths.append(os.path.join(training_path, path))
    return image_paths
