# Tools
Various tools for working with Retina.

## Contents
- `create_face_dataset.py` - Creates a set of images used to train a Face Recognizer.<br/>
  This script takes in a Label to both name the training set and identify the person to recognize.
  It may take in the (absolute) path to a Face Detection classifier and/or the settings for the machine the script is running on.
  See `create_face_dataset.py --help` for details.
  The user will be prompted to look into the attached camera and make specific facial expressions.
  The expressions the used for the data set are: Happy, Sad, Angry, Normal, Right Eye closed, Left Eye closed, and Both Eyes closed.
  Each of these expressions are done with glasses both on and off.
  The finished training set is saved under `Retina/data/faces/LABEL/training` where `LABEL` is the given label.<br/><br/>
- `prepare.sh` - Configures the OpenCV repository before building.<br/><br/>
- `process_raw_images.py` - Detects faces in raw images and prepares them for training.<br/>
  This script takes in a Label to identify the raw image set, which is located under `Retina/data/faces/LABEL/raw`.
  It may take in the (absolute) path to a Face Detection classifier and/or the settings for the machine the script is running on.
  See `process_raw_images.py --help` for details.
  Once the raw image set is found, this script will preprocess each face it finds and save it under `Retina/data/faces/LABEL/training`.
  <br/><br/>
- `train_facerecognizer.py` - Creates a Face Recognizer for a specific person.<br/>
  This script takes in a Label which is used to both name the face to be recognized and read the training set from the directory `Retina/data/faces/LABEL/training`.
  The resulting Face Recognizer is saved under `Retina/data/recognizers/` as `LABEL.xml` where `LABEL` is the given label.<br/><br/>
