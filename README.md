# Cerebrum

## What is Cerebrum?
Cerebrum is a Face Recognition application. It uses OpenCV and has "optimizied" settings for running on several of my machines.<br/>
<br/>
The name comes from the part of the Human brain responsible for vision and learning.

## Project Hierarchy
- `modules` - Internal data models and helper functions.
- `settings` - Hardware specific settings for each of my machines.
- `tools` - Various tools for working with Cerebrum.

## Dependencies
- CMake (for building OpenCV)
- GNU Make (also for building OpenCV)
- OpenCV (preferably 3.1 or higher)
- Python 3

## Installation
1) First things first, clone or download OpenCV and OpenCV's extra modules from [here][opencv] and [here][opencv_contrib] (unzip if compressed).<br/>
2) Set the `OPENCV` and `OPENCV_CONTRIB_MODULES` variables in `tools/prepare.sh` to the path of each of the OpenCV directories (if the values differ).<br/>
3) Run `prepare.sh` to configure OpenCV for installation.<br/>
4) Run `make` and `make install` inside of `$OPENCV/build`.<br/>
5) Create a symlink named `cv2.so` pointing to `cv2.cpython-34m.so`. `cv2.so` should be located in the system-wide Python 3 `site-packages` directory. `cv2.cpython-34m.so` is built when OpenCV is installed and will be located somewhere under `/usr/local` in another `site-packages` directory.<br/>
6) Cerebrum is now ready to run, see `./cerebrum.py --help` for details.<br/>

[opencv]: https://github.com/Itseez/opencv
[opencv_contrib]: https://github.com/Itseez/opencv_contrib
