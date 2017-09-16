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

import configparser


class Config:
    def __init__(self, file_):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(file_)

        self.__config = []

        for s in config.sections():
            entries = [(o, config.get(s, o)) for o in config.options(s)]
            self.__config.append((s, dict(entries)))

        self.__config = dict(self.__config)

    def camera(self):
        return self.__config['Camera']

    def detector(self):
        return self.__config['Detector']

    def recognizer(self):
        return self.__config['Recognizer']
