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

import os

from . import pathname


def default_settings():
    """
    Use the Mac Address OUI to determine what machine we're running on.
    Defaults to my test machine.
    """
    mac = None

    try:
        mac = open('/sys/class/net/eth0/address').read().rstrip().split(':')
    except OSError as ose:
        return 'default'

    if mac[0:3] == ['b8', '27', 'eb']:
        return 'raspberrypi2'
    else:
        return 'default'


def map_settings():
    """
    Maps simple settings filenames to their absolute paths.
    """
    settings = {}
    ents = os.listdir(pathname.get_settings_root())

    for ent in ents:
        key = ent[0:-4]
        settings[key] = os.path.abspath(pathname.get_settings_root() + ent)

    return settings


def validate_file(path):
    """
    Ensures the given file exists.
    """
    if os.path.isfile(path):
        return path
    else:
        return None


def validate_raw_dataset(label):
    """
    Ensures the given label has a raw dataset.
    """
    if os.path.isdir(pathname.get_raw_root(label)):
        return label
    else:
        return None


def validate_training_dataset(label):
    """
    Ensures the given label has a training dataset.
    """
    if os.path.isdir(pathname.get_training_root(label)):
        return label
    else:
        return None


def validate_recognizer(label):
    """
    Ensures the given label has a recognizer.
    """
    if os.path.isfile(pathname.get_recognizer_file(label)):
        return label
    else:
        return None
