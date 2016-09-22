#######################################################################
# Copyright (C) 2016 Tyler Cromwell <tyler@csh.rit.edu>
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

# Python libraries
import configparser
import os


class Config:
    def __init__(self, file_):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(file_)

        self._config = []

        for s in config.sections():
            entries = [(o, config.get(s, o)) for o in config.options(s)]
            self._config.append((s, dict(entries)))

        self._config = dict(self._config)

    def camera(self):
        return self._config['Camera']

    def detector(self):
        return self._config['Detector']

    def recognizer(self):
        return self._config['Recognizer']
