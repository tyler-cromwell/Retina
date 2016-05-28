# Tools
Various tools for working with Cerebrum.

## Contents
- `create_face_dataset.py` - Creates a set of images used to train a Face Recognizer.<br/>
  This script takes in a Label to both name the training set and identify the person to recognize.
  It may take in the (absolute) path to a Face Detection classifier and/or the settings for the machine the script is running on.
  See `create_face_dataset.py --help` for details.
  The user will be prompted to look into the attached camera and make specific facial expressions.
  The expressions the used for the data set are: Happy, Sad, Angry, Normal, Right Eye closed, Left Eye closed, and Both Eyes closed.
  Each of these expressions are done with glasses both on and off.
  The finished training set is saved under `Cerebrum/data/faces/LABEL/` where `LABEL` is the given label.<br/><br/>
- `prepare.sh` - Configures the OpenCV repository before building.<br/><br/>
- `train_facerecognizer.py` - Creates a Face Recognizer for a specific person.<br/>
  This script takes in a Label which is used to both name the face to be recognized and read the training set from the directory `Cerebrum/data/faces/LABEL`.
  It may take in the (absolute) path to a Face Detection classifier to detect faces during training and/or the settings for the machine the script is running on.
  See `train_facerecognizer.py --help` for details.
  The resulting Face Recognizer is saved under `Cerebrum/data/recognizers/` as `LABEL.xml` where `LABEL` is the given label.<br/><br/>
