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
def opt_classifier(path):
    if os.path.isfile(path):
        return path
    else:
        print('Invalid classifier: '+ arg)
        exit(1)


"""
Ensures the settings file given by 'settings' exists
"""
def opt_settings(root_dir, settings):
    if os.path.isfile(root_dir +'/settings/'+ settings +'.txt'):
        return root_dir +'/settings/'+ settings +'.txt'
    else:
        print('Invalid machine settings: '+ settings)
        exit(1)
