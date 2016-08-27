# Cerebrum

## What is Cerebrum?
Cerebrum is a Face Recognition application. It uses OpenCV and has "optimizied" settings for running on several of my machines.<br/>
<br/>
The name comes from the part of the Human brain responsible for vision and learning.

## Project Hierarchy
- `data` - Permanent and temporary data used for detection and recognition.
  - `classifiers` - Haar and LBP face detection classifiers.
  - `faces` - Face image sets for specific individuals.
    - `LABEL` - Sets for a specific individual.
      - `raw` - Raw, non-preprocessed, RGB images from an external source.
      - `training` - Preprocessed images ready for recognizer training.
  - `recognizers` - Face recognizer models.
- `modules` - Internal data models and helper functions.
- `settings` - Machine specific settings for video capture, detection, and recognition.
- `tools` - Various tools for working with Cerebrum.

## Dependencies
- Python 3.x
- Numpy
- Pillow
- Tkinter (optional)
- OpenCV > 3.1.0 (3.1.0 does not have the bug fix for exposing confidence values in Python bindings)

## Installing OpenCV
To install OpenCV 3+ for Python 3.x, I've been following the install instructions located [here][install].
If you are working on a Fedora-based machine like I am, simply installing the RPM equivalents of the Step 1 packages and following the rest of the guide should be fine.
You can find OpenCV and OpenCV_Contrib [here][opencv] and [here][opencv_contrib].

[install]: http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/
[opencv]: https://github.com/opencv/opencv
[opencv_contrib]: https://github.com/opencv/opencv_contrib
