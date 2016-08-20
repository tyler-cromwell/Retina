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
Ensures the classifier given by 'path' exists
"""
def classifier(path):
    if os.path.isfile(path):
        return path
    else:
        return None


"""
Use the Mac Address OUI to determine what machine we're running on.
Defaults to the my testing machine.
"""
def default_settings():
    mac = None

    try:
        mac = open('/sys/class/net/eth0/address').read().rstrip().split(':')
    except OSError as ose:
        return 'test-machine'

    if mac[0:3] == ['b8', '27', 'eb']:
        return 'raspberrypi2'
    else:
        return 'test-machine'


"""
Maps simple settings filenames to their absolute paths.
"""
def map_settings():
    settings = {}
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ents = os.listdir(root_dir +'/settings/')

    for ent in ents:
        key = ent[0:-4]
        settings[key] = os.path.abspath(root_dir +'/settings/'+ ent)

    return settings
