#!/bin/bash

########################################################################
#  Copyright (C) 2016 Tyler Cromwell <tyler@csh.rit.edu>
#
#  This file is part of Cerebrum.
#
#  Cerebrum is free software: you can redistribute it and/or modify
#  it under Version 2 of the terms of the GNU General Public License
#  as published by the Free Software Foundation.
#
#  Cerebrum is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY of FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cerebrum.
#  If not, see <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
########################################################################

OPENCV=~/opencv
OPENCV_CONTRIB_MODULES=~/opencv_contrib/modules

if [[ -z $OPENCV || -z $OPENCV_CONTRIB_MODULES ]]; then
    echo "Repository path missing!"
    echo $OPENCV
    exit 1
fi

mkdir -p $OPENCV/build
cd $OPENCV/build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D WITH_OPENCL=ON \
      -D WITH_OPENGL=ON \
      -D WITH_TBB=ON \
      -D INSTALL_C_EXAMPLES=OFF \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D OPENCV_EXTRA_MODULES_PATH=$OPENCV_CONTRIB_MODULES \
      -D BUILD_EXAMPLES=OFF $OPENCV
