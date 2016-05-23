# Cerebrum

## What is Cerebrum?
Cerebrum is a Face Recognition application. It uses OpenCV and has "optimizied" settings for running on my Beaglebone Black, Raspberry Pi 2, Laptop (a Thinkpad T420), and my Desktop.<br/>
<br/>
The name comes from the part of the Human brain responsible for vision and learning.

## Project Hierarchy
- `modules` - Internal data models and helper functions.
- `settings` - Hardware specific settings for each of my machines.
- `tools` - Various tools for working with Cerebrum.

## Installation
1) First things first, clone or download OpenCV and OpenCV's extra modules from [here][opencv] and [here][opencv_contrib] (unzip if compressed).<br/>
2) Set the `OPENCV` and `OPENCV_CONTRIB_MODULES` variables in `tools/prepare.sh` to the path of each of the OpenCV directories (if the values differ).<br/>
3) Run `prepare.sh` to configure OpenCV for installation.<br/>
4) Run `make` and `make install` inside of `$OPENCV/build`.<br/>
5) Cerebrum is now ready to run, see `./cerebrum.py --help` for details.<br/>

[opencv]: https://github.com/Itseez/opencv
[opencv_contrib]: https://github.com/Itseez/opencv_contrib
