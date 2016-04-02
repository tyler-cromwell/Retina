# Tools
Various tools for working with Cerebrum.

## Contents
- `create_face_dataset.py` - Creates a set of images used to train a Face Recognizer.<br/>
  This script takes in the (absolute) path to a Face Detection classifier, a Label to both name the training set and identify the person to recognize, and the settings for the machine the script is running on. This script prompts to look into the attached camera and make specific facial poses. The finished training set is saved under `Cerebrum/data/faces/LABEL/` where `LABEL` is the given label.<br/><br/>
- `prepare.sh` - Configures the OpenCV repository before building.<br/><br/>
- `train_facerecognizer.py` - Creates a Face Recognizer for a specific person.<br/>
  This script takes in the (absolute) path to a Face Detection classifier to detect faces during training, and a Label which is used to both name the face to be recognized and read the training set from the directory `Cerebrum/data/faces/LABEL`.<br/>
  The resulting Face Recognizer is saved under `Cerebrum/data/recognizers/` as `LABEL.xml` where `LABEL` is the given label.<br/><br/>
