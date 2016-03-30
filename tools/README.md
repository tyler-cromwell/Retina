# Tools
Various tools for working with Cerebrum.

## Contents
- `prepare.sh` - Configures the OpenCV repository before building.<br/><br/>
- `train_facerecognizer.py` - Creates a Face Recognizer for a specific person.<br/>
  This script takes in the (absolute) path to a Face Detection classifier to detect faces during training, and a Label which is used to both name the face to be recognized and find the training set directory which should be located under `Cerebrum/data/faces/`.<br/>
  The resulting Face Recognizer is saved under `Cerebrum/data/recognizers/` as `LABEL.xml`.<br/><br/>
