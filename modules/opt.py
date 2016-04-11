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
import getopt
import os


"""
Use the Mac Address OUI to determine what machine we're running on.
Defaults to the Raspberry Pi 2 (b8:27:eb:__:__:__).
"""
def default_settings(root_dir):
    defaults = root_dir +'/settings/raspberrypi2.txt'
    mac = open('/sys/class/net/enp0s25/address').read().rstrip().split(':')

    if mac[0:3] == ['b8', '27', 'eb'] and os.path.isfile(defaults):
        return defaults
    else:
        return None


"""
Ensures the classifier given by 'path' exists
"""
def classifier(path):
    if os.path.isfile(path):
        return path
    else:
        print('Invalid classifier: '+ arg)
        exit(1)


"""
Ensures the settings file given by 'settings' exists
"""
def settings(path):
    if os.path.isfile(path):
        return path
    else:
        print('Invalid settings file: '+ path)
        exit(1)
