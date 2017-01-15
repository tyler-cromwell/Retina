#######################################################################
# Copyright (C) 2017 Tyler Cromwell <tyler@csh.rit.edu>
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

import os
import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_classifier_root():
    return sys.path[1] + '/data/classifiers/'


def get_raw_root(label):
    return sys.path[1] + '/data/faces/' + label + '/raw/'


def get_recognizer_root():
    return sys.path[1] + '/data/recognizers/'


def get_recognizer_file(label):
    return sys.path[1] + '/data/recognizers/' + label + '.lbph.xml'


def get_settings_root():
    return sys.path[1] + '/settings/'


def get_training_root(label):
    return sys.path[1] + '/data/faces/' + label + '/training/'


def get_training_images(label):
    image_paths = []
    training_path = get_training_root(label)
    for path in os.listdir(training_path):
        image_paths.append(os.path.join(training_path, path))
    return image_paths
