#!/bin/bash

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
