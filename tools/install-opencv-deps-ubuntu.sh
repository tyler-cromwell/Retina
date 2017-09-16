#!/bin/bash

########################################################################
#  Copyright (C) 2017 Tyler Cromwell <tjc6185@gmail.com>
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

# Ubuntu 16.04

############################################################
# Install base requirements
############################################################
sudo apt install -y build-essential \
                    cmake \
                    git \
                    pkg-config \
                    libjpeg8-dev \
                    libtiff4-dev \
                    libjasper-dev \
                    libpng12-dev \
                    libavcodec-dev \
                    libavformat-dev \
                    libswscale-dev \
                    libv4l-dev \
                    libatlas-base-dev \
                    gfortran


############################################################
# Install FFmpeg
############################################################
sudo add-apt-repository -y ppa:jonathonf/ffmpeg-3
sudo apt install -y ffmpeg \
                    libav-tools \
                    x264 \
                    x265


############################################################
# Install Eigen
############################################################
sudo apt install -y libeigen3-dev


############################################################
# Install V4l2
############################################################
sudo apt install -y libv4l-dev


############################################################
# Install TBB
############################################################
sudo apt install -y libtbb2 libtbb-dev


############################################################
# Uninstall FFMPG:
############################################################
# sudo apt install ppa-purge
# sudo ppa-purge ppa:jonathonf/ffmpeg-3 && sudo apt autoremove
