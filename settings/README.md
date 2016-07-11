# Settings

Face Detection, Rcognition, and video capture settings for each machine I've tested on.<br/>
The classifiers named each setting file refers to a Symbolic Link under `data/classifiers/` that must be created before running the program.<br/>

## Format
- `[General]` - General program settings, such as video capture resolution.
- `[Detector]` - Face Detection settings. Specifies location for Face Detection classifier and `detectMultiScale` arguments.
- `[Recognizer]` - Face Recognition settings. Specifies confidence ceiling for Face Recognition.
