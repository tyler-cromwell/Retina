# Settings

Face Detection, Rcognition, and video capture settings for each machine I've tested on.<br/>
The classifiers named each setting file refers to a Symbolic Link under `data/classifiers` that must be created before running the program.<br/>

## Format
- `[General]` - Specifies resolution for video capture.
- `[Detector]` - Specifies location for Face Detection classifier and `detectMultiScale` arguments.
- `[Recognizer]` - Specifies confidence ceiling for Face Recognition.
