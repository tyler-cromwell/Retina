# Retina

## What is Retina?
Retina is a Face Recognition application. It uses OpenCV and has "optimizied" settings for running on several of my machines.

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
- `tools` - Various tools for working with Retina.

## Dependencies
- Python 3.x
- OpenCV >= 3.2.0
- Numpy
- Pillow
- Tkinter (optional)

## Recommended OpenCV dependencies
- [Eigen3][eigen3]
- [FFmpeg][ffmpeg]
- [V4l / V4l2][v4l]
- [TBB][tbb]

## Installing OpenCV
To install OpenCV 3+ for Python 3.x, I've been following the install instructions located [here][install].
If you are working on a Fedora-based machine like I am, simply installing the RPM equivalents of the Step 1 packages and following the rest of the guide should be fine.
You can find OpenCV and OpenCV_Contrib [here][opencv] and [here][opencv_contrib].

[eigen3]: https://en.wikipedia.org/wiki/Eigen_(C%2B%2B_library)
[ffmpeg]: https://en.wikipedia.org/wiki/FFmpeg
[install]: http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/
[opencv]: https://github.com/opencv/opencv
[opencv_contrib]: https://github.com/opencv/opencv_contrib
[tbb]: https://en.wikipedia.org/wiki/Threading_Building_Blocks
[v4l]: https://en.wikipedia.org/wiki/Video4Linux
