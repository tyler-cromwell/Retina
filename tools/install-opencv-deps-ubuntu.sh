#!/bin/bash

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
